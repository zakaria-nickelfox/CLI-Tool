import os
import mimetypes
import logging
from typing import BinaryIO, Set, Optional
from werkzeug.utils import secure_filename # Using werkzeug for robust filename security

import config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class UploadServiceError(Exception):
    """Custom exception for upload service errors."""
    pass


class UploadService:
    """Handles file upload functionality including validation and storage."""

    def __init__(self):
        """Initializes the UploadService with configuration from config.py."""
        self.upload_dir = config.UPLOAD_DIR
        self.allowed_extensions: Set[str] = config.ALLOWED_EXTENSIONS
        self.max_file_size_bytes = config.MAX_FILE_SIZE_BYTES

        # Ensure the upload directory exists
        os.makedirs(self.upload_dir, exist_ok=True)
        logging.info(f"UploadService initialized. Target directory: {self.upload_dir}")

    def _allowed_file(self, filename: str) -> bool:
        """Checks if a file's extension is allowed."""
        return "." in filename and filename.rsplit(".", 1)[1].lower() in self.allowed_extensions

    def _validate_file(self, filename: str, file_size: int, content_type: Optional[str]) -> None:
        """Performs validation checks on the file."

        Args:
            filename: The original filename provided by the user.
            file_size: The size of the file in bytes.
            content_type: The MIME type of the file.

        Raises:
            UploadServiceError: If any validation fails.
        """
        if not filename:
            raise UploadServiceError("No file selected or invalid filename.")

        # Filename extension validation
        if not self._allowed_file(filename):
            raise UploadServiceError(
                f"File type for '{filename}' not allowed. Allowed types: {', '.join(self.allowed_extensions)}"
            )

        # File size validation
        if file_size > self.max_file_size_bytes:
            max_mb = self.max_file_size_bytes / (1024 * 1024)
            raise UploadServiceError(f"File size exceeds limit of {max_mb:.1f} MB.")

        # Basic content type validation (can be more robust)
        if content_type and not mimetypes.guess_extension(content_type):
            logging.warning(f"Content type '{content_type}' for '{filename}' is unusual or unknown.")
            # You might choose to block it or allow with warning

        logging.info(f"File '{filename}' passed basic validation.")

    def upload_file(self, file_stream: BinaryIO, filename: str, content_type: Optional[str] = None) -> str:
        """Uploads a file, validates it, and saves it to the configured directory."

        Args:
            file_stream: A file-like object (e.g., from an HTTP request body) opened in binary read mode.
            filename: The original filename provided by the user.
            content_type: The MIME type of the file (e.g., 'image/png').

        Returns:
            The relative path to the saved file.

        Raises:
            UploadServiceError: If validation fails or saving encounters an error.
        """
        # To get file size without reading the whole stream first, one might need to wrap the stream
        # or rely on the web framework providing it. For this example, we'll read a chunk to get size.
        # In a real scenario, a web framework would often provide file size directly.
        
        # Seek to end to get size, then back to beginning for reading
        original_position = file_stream.tell()
        file_stream.seek(0, os.SEEK_END)
        file_size = file_stream.tell()
        file_stream.seek(original_position, os.SEEK_SET)

        self._validate_file(filename, file_size, content_type)

        # Secure the filename to prevent directory traversal attacks
        safe_filename = secure_filename(filename)
        if not safe_filename:
            raise UploadServiceError(f"Could not secure filename for: {filename}")

        target_path = os.path.join(self.upload_dir, safe_filename)

        try:
            # Write the file in chunks to handle large files efficiently
            with open(target_path, "wb") as f_out:
                while True:
                    chunk = file_stream.read(8192)  # Read in 8KB chunks
                    if not chunk:
                        break
                    f_out.write(chunk)
            logging.info(f"File '{filename}' (size: {file_size} bytes) saved to '{target_path}'.")
            return target_path
        except IOError as e:
            logging.error(f"Failed to save file '{filename}' to '{target_path}': {e}")
            raise UploadServiceError(f"Failed to save file: {e}") from e
        except Exception as e:
            logging.error(f"An unexpected error occurred during file upload for '{filename}': {e}")
            raise UploadServiceError(f"An unexpected error occurred during upload: {e}") from e

    # Placeholder for cloud storage integration
    # def upload_to_cloud(self, file_stream: BinaryIO, filename: str, bucket_name: str) -> str:
    #     """Uploads a file to a cloud storage provider (e.g., S3, GCS)."""
    #     logging.info(f"[Cloud Placeholder] Uploading '{filename}' to bucket '{bucket_name}'")
    #     # Integrate with respective cloud SDKs here (boto3 for S3, google-cloud-storage for GCS)
    #     # Example (S3): s3_client.upload_fileobj(file_stream, bucket_name, filename)
    #     return f"https://cloud.storage.provider/{bucket_name}/{filename}"

# Example usage (for testing/demonstration, typically integrated with a web framework):
# if __name__ == "__main__":
#     upload_service = UploadService()

#     # Create a dummy file for testing
#     dummy_content = b"This is a test file content." * 10
#     dummy_file_path = "test_upload.txt"
#     with open(dummy_file_path, "wb") as f:
#         f.write(dummy_content)

#     # Create a dummy image file for testing
#     dummy_image_path = "test_image.png"
#     try:
#         from PIL import Image
#         img = Image.new('RGB', (60, 30), color = 'red')
#         img.save(dummy_image_path)
#     except ImportError:
#         print("Pillow not installed, skipping dummy image creation. 'test_image.png' will not be created.")
#         dummy_image_path = None


#     print("\n--- Testing File Uploads ---")
#     try:
#         # Test successful upload
#         with open(dummy_file_path, "rb") as f_stream:
#             uploaded_path = upload_service.upload_file(
#                 file_stream=f_stream,
#                 filename="my_document.txt",
#                 content_type="text/plain"
#             )
#             print(f"Successfully uploaded: {uploaded_path}")

#         if dummy_image_path and os.path.exists(dummy_image_path):
#             with open(dummy_image_path, "rb") as f_stream:
#                 uploaded_path = upload_service.upload_file(
#                     file_stream=f_stream,
#                     filename="profile_pic.png",
#                     content_type="image/png"
#                 )
#                 print(f"Successfully uploaded: {uploaded_path}")

#         # Test disallowed extension
#         with open(dummy_file_path, "rb") as f_stream:
#             try:
#                 upload_service.upload_file(
#                     file_stream=f_stream,
#                     filename="malicious.exe",
#                     content_type="application/x-msdownload"
#                 )
#             except UploadServiceError as e:
#                 print(f"Caught expected error for malicious.exe: {e}")

#         # Test large file size (adjust dummy_content if needed to exceed config.MAX_FILE_SIZE_BYTES)
#         large_dummy_content = b"A" * (config.MAX_FILE_SIZE_BYTES + 1024)
#         large_dummy_file_path = "large_file.txt"
#         with open(large_dummy_file_path, "wb") as f:
#             f.write(large_dummy_content)
#         with open(large_dummy_file_path, "rb") as f_stream:
#             try:
#                 upload_service.upload_file(
#                     file_stream=f_stream,
#                     filename="too_large.txt",
#                     content_type="text/plain"
#                 )
#             except UploadServiceError as e:
#                 print(f"Caught expected error for too_large.txt: {e}")

#     except UploadServiceError as e:
#         print(f"Upload Service Error during test: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred during test: {e}")
#     finally:
#         # Clean up dummy files
#         if os.path.exists(dummy_file_path):
#             os.remove(dummy_file_path)
#         if os.path.exists(large_dummy_file_path):
#             os.remove(large_dummy_file_path)
#         if dummy_image_path and os.path.exists(dummy_image_path):
#             os.remove(dummy_image_path)
#         # Clean up uploaded files for test
#         for f in os.listdir(config.UPLOAD_DIR):
#             if f.startswith("my_document") or f.startswith("profile_pic") or f.startswith("malicious") or f.startswith("too_large"):
#                 os.remove(os.path.join(config.UPLOAD_DIR, f))
