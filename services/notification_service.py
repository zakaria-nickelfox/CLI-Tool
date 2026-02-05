import logging
from typing import Dict, Any, List, Union

from services.notification_channels import (
    NotificationChannel,
    EmailNotificationChannel,
    SMSNotificationChannel,
    InAppNotificationChannel,
)
from services.mail_service import MailService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class NotificationService:
    """Manages and dispatches notifications through various channels."""

    def __init__(self):
        """Initializes the NotificationService and registers default channels."""
        self._channels: Dict[str, NotificationChannel] = {}
        self._initialize_default_channels()
        logging.info("NotificationService initialized with default channels.")

    def _initialize_default_channels(self):
        """Initializes and registers standard notification channels."""
        # Initialize MailService for EmailNotificationChannel
        mail_service = MailService()
        self.register_channel("email", EmailNotificationChannel(mail_service))
        self.register_channel("sms", SMSNotificationChannel())
        self.register_channel("in_app", InAppNotificationChannel())

    def register_channel(self, name: str, channel: NotificationChannel):
        """Registers a new notification channel."

        Args:
            name: A unique name for the channel (e.g., 'email', 'sms').
            channel: An instance of a class that inherits from NotificationChannel.
        """
        if not isinstance(channel, NotificationChannel):
            raise TypeError("Channel must be an instance of NotificationChannel.")
        self._channels[name.lower()] = channel
        logging.info(f"Notification channel '{name}' registered.")

    def get_channel(self, name: str) -> Optional[NotificationChannel]:
        """Retrieves a registered notification channel by name."

        Args:
            name: The name of the channel.

        Returns:
            The NotificationChannel instance if found, None otherwise.
        """
        return self._channels.get(name.lower())

    def send_notification(
        self, recipient: str, message: str, channel_name: str, **kwargs: Any
    ) -> bool:
        """Sends a notification using a specific channel."

        Args:
            recipient: The identifier for the recipient.
            message: The content of the notification.
            channel_name: The name of the channel to use.
            **kwargs: Additional parameters specific to the chosen channel.

        Returns:
            True if the notification was sent successfully, False otherwise.
        """
        channel = self.get_channel(channel_name)
        if not channel:
            logging.error(f"Notification channel '{channel_name}' not found.")
            return False

        try:
            success = channel.send(recipient, message, **kwargs)
            if success:
                logging.info(f"Notification successfully dispatched via '{channel_name}'.")
            else:
                logging.warning(f"Notification failed to dispatch via '{channel_name}'.")
            return success
        except Exception as e:
            logging.error(f"Error sending notification via '{channel_name}': {e}")
            return False

    def dispatch_notification(
        self, 
        notification_type: str, 
        recipient: str, 
        message: str, 
        preferred_channels: Optional[Union[str, List[str]]] = None,
        **kwargs: Any
    ) -> Dict[str, bool]:
        """Dispatches a notification based on type, potentially using preferred channels."

        This method implements logic to decide which channel(s) to use.

        Args:
            notification_type: A string identifying the type of notification (e.g., 'welcome', 'password_reset', 'alert').
            recipient: The primary identifier for the recipient (e.g., email, user ID).
            message: The core content of the notification.
            preferred_channels: Optional. A string or list of strings indicating channel preferences.
                                If None, default routing logic will apply.
            **kwargs: Additional data to pass to the channel's send method.

        Returns:
            A dictionary showing the success status for each channel attempted.
        """
        results = {}
        channels_to_use: List[str] = []

        if preferred_channels:
            channels_to_use = [preferred_channels] if isinstance(preferred_channels, str) else preferred_channels
        else:
            # Default routing logic based on notification_type
            if notification_type == "welcome":
                channels_to_use = ["email", "in_app"]
                kwargs.setdefault("subject", "Welcome!")
                kwargs.setdefault("is_html", True) # Assuming welcome emails are often HTML
            elif notification_type == "password_reset":
                channels_to_use = ["email"]
                kwargs.setdefault("subject", "Password Reset Request")
            elif notification_type == "alert":
                # For critical alerts, try multiple channels
                channels_to_use = ["email", "sms", "in_app"]
                kwargs.setdefault("subject", "Urgent Alert!")
            elif notification_type == "promotion":
                channels_to_use = ["email"]
                kwargs.setdefault("subject", "Special Offer!")
            else:
                logging.warning(f"Unknown notification type '{notification_type}'. No default channels defined.")
                return results

        logging.info(f"Dispatching '{notification_type}' notification to {recipient} via channels: {channels_to_use}")

        for channel_name in channels_to_use:
            success = self.send_notification(recipient, message, channel_name, **kwargs)
            results[channel_name] = success

        return results

# Example usage (for testing/demonstration):
# if __name__ == "__main__":
#     notification_service = NotificationService()

#     # Test welcome notification (HTML email, in-app)
#     print("\n--- Sending Welcome Notification ---")
#     html_welcome_message = """
#     <html><body><h1>Welcome to our service!</h1><p>We're glad to have you.</p></body></html>
#     """
#     notification_service.dispatch_notification(
#         notification_type="welcome",
#         recipient="test_user@example.com",
#         message=html_welcome_message,
#         user_id="user_123" # For in-app recipient
#     )

#     # Test password reset (plain email)
#     print("\n--- Sending Password Reset Notification ---")
#     notification_service.dispatch_notification(
#         notification_type="password_reset",
#         recipient="test_user@example.com",
#         message="Click this link to reset your password: http://example.com/reset/token123"
#     )

#     # Test urgent alert (email, SMS, in-app)
#     print("\n--- Sending Urgent Alert Notification ---")
#     notification_service.dispatch_notification(
#         notification_type="alert",
#         recipient="test_user@example.com",
#         message="System critical alert! Please check immediately.",
#         phone_number="+15551234567", # For SMS recipient
#         user_id="user_123", # For in-app recipient
#         link="/dashboard/alerts"
#     )

#     # Test direct send to SMS channel
#     print("\n--- Sending Direct SMS Notification ---")
#     notification_service.send_notification(
#         recipient="+15559876543",
#         message="This is a direct SMS notification.",
#         channel_name="sms"
#     )

#     # Test sending to an unregistered channel (should fail)
#     print("\n--- Sending to Unknown Channel ---")
#     notification_service.send_notification(
#         recipient="user@example.com",
#         message="Should not go through.",
#         channel_name="unregistered_channel"
#     )
