from abc import ABC, abstractmethod
import logging
from typing import Dict, Any

from services.mail_service import MailService, MailServiceError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class NotificationChannel(ABC):
    """Abstract base class for all notification channels."""

    @abstractmethod
    def send(self, recipient: str, message: str, **kwargs: Any) -> bool:
        """Sends a notification through this channel."

        Args:
            recipient: The identifier for the recipient (e.g., email address, phone number).
            message: The content of the notification.
            **kwargs: Additional parameters specific to the channel (e.g., subject for email).

        Returns:
            True if the notification was sent successfully, False otherwise.
        """
        pass


class EmailNotificationChannel(NotificationChannel):
    """Notification channel for sending emails using MailService."""

    def __init__(self, mail_service: MailService):
        self.mail_service = mail_service
        logging.info("EmailNotificationChannel initialized.")

    def send(self, recipient: str, message: str, **kwargs: Any) -> bool:
        """Sends an email notification."

        Args:
            recipient: The recipient's email address.
            message: The email body (can be HTML).
            kwargs: Expected: 'subject' (str), 'is_html' (bool).

        Returns:
            True if email sent successfully, False otherwise.
        """
        subject = kwargs.get("subject", "Notification")
        is_html = kwargs.get("is_html", False)

        try:
            self.mail_service.send_email(
                to_email=recipient,
                subject=subject,
                body=message,
                is_html=is_html
            )
            logging.info(f"Email notification sent to {recipient} (Subject: {subject})")
            return True
        except MailServiceError as e:
            logging.error(f"Failed to send email notification to {recipient}: {e}")
            return False
        except Exception as e:
            logging.error(f"An unexpected error occurred sending email notification to {recipient}: {e}")
            return False


class SMSNotificationChannel(NotificationChannel):
    """Placeholder notification channel for sending SMS messages."""

    def send(self, recipient: str, message: str, **kwargs: Any) -> bool:
        """Simulates sending an SMS notification."

        Args:
            recipient: The recipient's phone number.
            message: The SMS message content.
            kwargs: Currently not used.

        Returns:
            Always True for this placeholder.
        """
        logging.info(f"[SMS Placeholder] Sending SMS to {recipient}: {message}")
        # In a real application, integrate with an SMS gateway API here (e.g., Twilio, Nexmo)
        return True


class InAppNotificationChannel(NotificationChannel):
    """Placeholder notification channel for sending in-app notifications."""

    def send(self, recipient: str, message: str, **kwargs: Any) -> bool:
        """Simulates sending an in-app notification."

        Args:
            recipient: The user ID or relevant identifier for the in-app user.
            message: The content of the in-app notification.
            kwargs: Additional data for the in-app notification (e.g., 'link', 'icon').

        Returns:
            Always True for this placeholder.
        """
        data_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        logging.info(f"[In-App Placeholder] Sending in-app notification to user {recipient}: {message} (Data: {data_str})")
        # In a real application, this would typically involve:
        # 1. Storing the notification in a database for the user.
        # 2. Pushing the notification to the user's active sessions via WebSockets.
        return True
