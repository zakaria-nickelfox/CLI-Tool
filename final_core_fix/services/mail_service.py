from mail_service import MailService

# Send simple email
MailService.send_email(
    subject='Welcome!',
    to_emails=['user@example.com'],
    html_content='<h1>Welcome to our platform!</h1>'
)

# Send template email
MailService.send_template_email(
    subject='Welcome!',
    to_emails=['user@example.com'],
    template_name='emails/welcome.html',
    context={'name': 'John Doe'}
)

# Send welcome email
MailService.send_welcome_email('user@example.com', 'John Doe')

# Send password reset email
MailService.send_password_reset_email('user@example.com', 'reset-token-123')