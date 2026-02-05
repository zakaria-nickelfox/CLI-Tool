import os
from dotenv import load_dotenv

load_dotenv()

# --- Mail Service Configuration ---
MAIL_HOST = os.getenv("MAIL_HOST", "smtp.example.com")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
MAIL_USERNAME = os.getenv("MAIL_USERNAME", "your_email@example.com")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "your_email_password")
MAIL_SENDER_EMAIL = os.getenv("MAIL_SENDER_EMAIL", "noreply@example.com")
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "True").lower() == "true"

# --- Upload Service Configuration ---
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "pdf", "doc", "docx", "txt"}
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 5))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# --- Notification Service Configuration ---
# Define default channels or routing rules if needed
# For simplicity, channels are explicitly chosen in the example below.
