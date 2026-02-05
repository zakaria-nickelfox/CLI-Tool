import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import logging
from typing import List, Dict, Optional

import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MailServiceError(Exception):
    """Custom exception for mail service errors."""
    pass


class MailService:
    """A robust mail service for sending various types of emails."""

    def __init__(self):
        """Initializes the MailService with SMTP configuration from config.py."""
        self.smtp_host = config.MAIL_HOST
        self.smtp_port = config.MAIL_PORT
        self.smtp_username = config.MAIL_USERNAME
        self.smtp_password = config.MAIL_PASSWORD
        self.sender_email = config.MAIL_SENDER_EMAIL
        self.use_tls = config.MAIL_USE_TLS

        if not all([self.smtp_host, self.smtp_port, self.smtp_username, self.smtp_password, self.sender_email]):
            logging.warning(
                "Mail service credentials are not fully configured. Sending emails might fail."
            )

    def _create_message(self, to_email: str, subject: str, body: str, is_html: bool) -> MIMEMultipart:
        """Creates a MIMEMultipart message object with specified content."""
        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        # Attach body based on content type
        msg.attach(MIMEText(body, "html" if is_html else "plain"))
        return msg

    def _add_attachments(self, msg: MIMEMultipart, attachments: Optional[List[Dict[str, str]]]):
        """Adds attachments to the MIMEMultipart message."

        Args:
            msg: The MIMEMultipart message object.
            attachments: A list of dictionaries, where each dict has 'filepath' and 'filename' (optional).
                         Example: [{'filepath': '/path/to/file.pdf', 'filename': 'document.pdf'}]
        """
        if not attachments:
            return

        for attachment_data in attachments:
            filepath = attachment_data.get("filepath")
            custom_filename = attachment_data.get("filename")

            if not filepath or not os.path.exists(filepath):
                logging.warning(f"Attachment file not found or path not provided: {filepath}. Skipping.")
                continue

            try:
                with open(filepath, "rb") as f:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(f.read())
                encoders.encode_base64(part)

                filename = custom_filename if custom_filename else os.path.basename(filepath)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}",
                )
                msg.attach(part)
            except IOError as e:
                logging.error(f"Could not read attachment file {filepath}: {e}")
                raise MailServiceError(f"Failed to add attachment {filepath}: {e}") from e
            except Exception as e:
                logging.error(f"An unexpected error occurred while adding attachment {filepath}: {e}")
                raise MailServiceError(f"Failed to add attachment {filepath}: {e}") from e

    def send_email(
        self,
        to_email: str,
        subject: str,
        body: str,
        is_html: bool = False,
        attachments: Optional[List[Dict[str, str]]] = None,
    ):
        """Sends an email to the specified recipient."

        Args:
            to_email: The recipient's email address.
            subject: The subject of the email.
            body: The content of the email. Can be plain text or HTML.
            is_html: Set to True if the body contains HTML content.
            attachments: A list of dictionaries for attachments.
                         Each dict should have 'filepath' and optionally 'filename'.

        Raises:
            MailServiceError: If there's an issue with sending the email.
        """
        if not self.sender_email:
            raise MailServiceError("Sender email is not configured.")
        if not to_email:
            raise MailServiceError("Recipient email cannot be empty.")

        msg = self._create_message(to_email, subject, body, is_html)
        self._add_attachments(msg, attachments)

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()  # Secure the connection
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            logging.info(f"Email sent successfully to {to_email} with subject: '{subject}'")
        except smtplib.SMTPAuthenticationError as e:
            logging.error(f"SMTP authentication error: {e}. Check username and password.")
            raise MailServiceError(f"Authentication failed: {e}") from e
        except smtplib.SMTPConnectError as e:
            logging.error(f"SMTP connection error: {e}. Check host and port.")
            raise MailServiceError(f"Connection failed: {e}") from e
        except smtplib.SMTPException as e:
            logging.error(f"SMTP error occurred: {e}")
            raise MailServiceError(f"Failed to send email: {e}") from e
        except Exception as e:
            logging.error(f"An unexpected error occurred while sending email: {e}")
            raise MailServiceError(f"An unexpected error occurred: {e}") from e

# Example usage (for testing/demonstration, typically not directly run):
# if __name__ == "__main__":
#     mail_service = MailService()

#     # Create a dummy file for attachment test
#     with open("test_attachment.txt", "w") as f:
#         f.write("This is a test attachment.")

#     try:
#         # Send a plain text email
#         mail_service.send_email(
#             to_email="recipient@example.com",
#             subject="Test Plain Email from Python",
#             body="Hello, this is a plain text email sent from a Python mail service."
#         )

#         # Send an HTML email
#         html_body = """
#         <html>
#         <body>
#             <h1>Hello from Python!</h1>
#             <p>This is an <b>HTML</b> email sent from your robust mail service.</p>
#             <p>Regards,<br>Python Mailer</p>
#         </body>
#         </html>
#         """
#         mail_service.send_email(
#             to_email="recipient@example.com",
#             subject="Test HTML Email from Python",
#             body=html_body,
#             is_html=True
#         )

#         # Send an email with an attachment
#         mail_service.send_email(
#             to_email="recipient@example.com",
#             subject="Test Email with Attachment",
#             body="Please find the attached document.",
#             attachments=[{"filepath": "test_attachment.txt", "filename": "my_document.txt"}]
#         )

#         print("All test emails attempted. Check logs for status.")

#     except MailServiceError as e:
#         print(f"Mail Service Error during test: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred during test: {e}")
#     finally:
#         # Clean up dummy file
#         if os.path.exists("test_attachment.txt"):
#             os.remove("test_attachment.txt")
