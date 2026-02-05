import os
import logging
from io import BytesIO
from services.mail_service import MailService, MailServiceError
from services.notification_service import NotificationService
from services.upload_service import UploadService, UploadServiceError
import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def demo_mail_service():
    """Demonstrates the Mail Service functionality."""
    print("\n--- Demonstrating Mail Service ---")
    mail_service = MailService()

    # Create a dummy file for attachment test
    dummy_attachment_path = "./temp_attachment.txt"
    with open(dummy_attachment_path, "w") as f:
        f.write("This is a test attachment for the mail service demo.")

    try:
        # 1. Send a plain text email
        print("Attempting to send a plain text email...")
        mail_service.send_email(
            to_email="recipient@example.com", # Replace with a real recipient for testing
            subject="Demo: Plain Text Email from Python",
            body="Hello, this is a plain text email sent from the Python mail service demo."
        )

        # 2. Send an HTML email
        print("Attempting to send an HTML email...")
        html_body = """
        <html>
        <body>
            <h1>Hello from Python Mailer!</h1>
            <p>This is an <b>HTML</b> email sent from your robust mail service demo.</p>
            <p>Regards,<br>Python Mailer</p>
        </body>
        </html>
        """
        mail_service.send_email(
            to_email="recipient@example.com", # Replace with a real recipient for testing
            subject="Demo: HTML Email from Python",
            body=html_body,
            is_html=True
        )

        # 3. Send an email with an attachment
        print("Attempting to send an email with an attachment...")
        mail_service.send_email(
            to_email="recipient@example.com", # Replace with a real recipient for testing
            subject="Demo: Email with Attachment",
            body="Please find the attached document in this demo email.",
            attachments=[{"filepath": dummy_attachment_path, "filename": "demo_document.txt"}]
        )

        logging.info("Mail service demonstrations completed. Check your inbox (and spam!) if using real credentials.")

    except MailServiceError as e:
        logging.error(f"Mail Service Demo Error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during mail service demo: {e}")
    finally:
        if os.path.exists(dummy_attachment_path):
            os.remove(dummy_attachment_path)


def demo_notification_service():
    """Demonstrates the Notification Service functionality."""
    print("\n--- Demonstrating Notification Service ---")
    notification_service = NotificationService()

    try:
        # 1. Dispatch a 'welcome' notification (should go to email and in-app)
        print("Attempting to dispatch a 'welcome' notification...")
        welcome_html_message = """
        <html><body><h1>Welcome, New User!</h1><p>Thanks for joining our platform.</p></body></html>
        """
        results = notification_service.dispatch_notification(
            notification_type="welcome",
            recipient="new_user@example.com", # For email
            message=welcome_html_message,
            user_id="user_456" # For in-app
        )
        print(f"Welcome Notification Results: {results}")

        # 2. Dispatch an 'alert' notification (should go to email, SMS, in-app)
        print("Attempting to dispatch an 'alert' notification...")
        results = notification_service.dispatch_notification(
            notification_type="alert",
            recipient="admin@example.com", # For email
            message="Critical system overload detected! Action required.",
            phone_number="+15551112222", # For SMS
            user_id="admin_123", # For in-app
            severity="high"
        )
        print(f"Alert Notification Results: {results}")

        # 3. Send a direct notification to a specific channel (SMS)
        print("Attempting to send a direct SMS notification...")
        success = notification_service.send_notification(
            recipient="+15559998888",
            message="Your one-time code is 123456.",
            channel_name="sms"
        )
        print(f"Direct SMS Notification Success: {success}")

        logging.info("Notification service demonstrations completed. Check console for placeholder outputs and logs.")

    except Exception as e:
        logging.error(f"An error occurred during notification service demo: {e}")


def demo_upload_documents():
    """Demonstrates the Upload Documents functionality."""
    print("\n--- Demonstrating Upload Documents Service ---")
    upload_service = UploadService()

    # Ensure the upload directory exists for cleanup
    os.makedirs(config.UPLOAD_DIR, exist_ok=True)

    # 1. Create a dummy text file for upload
    dummy_text_content = b"This is a sample document for upload testing.\nIt contains multiple lines of text."
    dummy_text_filename = "sample_doc.txt"
    dummy_text_stream = BytesIO(dummy_text_content)

    # 2. Create a dummy image file for upload (requires Pillow if running standalone)
    dummy_image_stream = None
    dummy_image_filename = "profile.png"
    try:
        from PIL import Image
        img = Image.new('RGB', (100, 50), color = 'blue')
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        dummy_image_stream = img_byte_arr
        logging.info("Pillow found, dummy image created for upload demo.")
    except ImportError:
        logging.warning("Pillow not installed. Skipping dummy image upload demo.")

    try:
        # Test successful text file upload
        print(f"Attempting to upload '{dummy_text_filename}'...")
        uploaded_path = upload_service.upload_file(
            file_stream=dummy_text_stream,
            filename=dummy_text_filename,
            content_type="text/plain"
        )
        print(f"Successfully uploaded text file to: {uploaded_path}")

        # Test successful image file upload
        if dummy_image_stream:
            print(f"Attempting to upload '{dummy_image_filename}'...")
            uploaded_path = upload_service.upload_file(
                file_stream=dummy_image_stream,
                filename=dummy_image_filename,
                content_type="image/png"
            )
            print(f"Successfully uploaded image file to: {uploaded_path}")

        # Test disallowed extension
        print("Attempting to upload a file with a disallowed extension (should fail)...")
        bad_file_content = b"This should not be allowed."
        bad_file_stream = BytesIO(bad_file_content)
        try:
            upload_service.upload_file(
                file_stream=bad_file_stream,
                filename="virus.exe",
                content_type="application/x-msdownload"
            )
        except UploadServiceError as e:
            print(f"Caught expected error for 'virus.exe': {e}")

        # Test file too large
        print("Attempting to upload a file that is too large (should fail)...")
        large_content = b"A" * (config.MAX_FILE_SIZE_BYTES + 1024) # Exceed max size by 1KB
        large_file_stream = BytesIO(large_content)
        try:
            upload_service.upload_file(
                file_stream=large_file_stream,
                filename="very_large_doc.pdf",
                content_type="application/pdf"
            )
        except UploadServiceError as e:
            print(f"Caught expected error for 'very_large_doc.pdf': {e}")

        logging.info(f"Upload service demonstrations completed. Check the '{config.UPLOAD_DIR}' directory.")

    except UploadServiceError as e:
        logging.error(f"Upload Service Demo Error: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred during upload service demo: {e}")
    finally:
        # Clean up uploaded files in the test directory
        if os.path.exists(config.UPLOAD_DIR):
            for filename in os.listdir(config.UPLOAD_DIR):
                if filename.startswith(("sample_doc", "profile", "very_large_doc")):
                    try:
                        os.remove(os.path.join(config.UPLOAD_DIR, filename))
                        logging.info(f"Cleaned up '{filename}' from upload directory.")
                    except OSError as e:
                        logging.warning(f"Could not remove '{filename}': {e}")
            # Optionally remove the directory if empty
            try:
                os.rmdir(config.UPLOAD_DIR)
                logging.info(f"Removed empty upload directory: {config.UPLOAD_DIR}")
            except OSError:
                pass # Directory not empty, or other error


if __name__ == "__main__":
    print("Starting combined feature demonstration...")

    # Run Mail Service Demo
    demo_mail_service()

    # Run Notification Service Demo
    demo_notification_service()

    # Run Upload Documents Demo
    demo_upload_documents()

    print("\nAll feature demonstrations completed.")
