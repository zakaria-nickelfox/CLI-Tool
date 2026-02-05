import os

file_path = r'c:\Users\Anshul\Desktop\CLI tool (2)\CLI tool\files\DJANGO_BOILERPLATE.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Implementations to add for Django

# 1. Mail Service
mail_impl = """
### Implementation Files

#### Mail Service

```python
# mail_service.py
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

class MailService:
    @staticmethod
    def send_email(subject, to_emails, text_content=None, html_content=None):
        return send_mail(
            subject=subject,
            message=text_content or '',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=to_emails,
            html_message=html_content,
            fail_silently=False,
        )

    @staticmethod
    def send_template_email(subject, to_emails, template_name, context):
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)
        return MailService.send_email(subject, to_emails, text_content, html_content)

    @staticmethod
    def send_welcome_email(email, name):
        return MailService.send_email(
            subject='Welcome!',
            to_emails=[email],
            html_content=f'<h1>Welcome {name}!</h1>'
        )
```
"""

# 2. Notification System
notification_impl = """
### Implementation Files

#### Notification Models

```python
# notification_models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class NotificationType(models.TextChoices):
    INFO = 'info', 'Info'
    SUCCESS = 'success', 'Success'
    WARNING = 'warning', 'Warning'
    ERROR = 'error', 'Error'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=NotificationType.choices, default=NotificationType.INFO)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

class NotificationService:
    @staticmethod
    def create_notification(user, title, message, notification_type=NotificationType.INFO, metadata=None):
        return Notification.objects.create(
            user=user,
            title=title,
            message=message,
            type=notification_type,
            metadata=metadata
        )

    @staticmethod
    def get_user_notifications(user, unread_only=False):
        qs = Notification.objects.filter(user=user)
        if unread_only:
            qs = qs.filter(is_read=False)
        return qs

    @staticmethod
    def mark_as_read(notification_id, user):
        return Notification.objects.filter(id=notification_id, user=user).update(is_read=True)
```
"""

# 3. RBAC
rbac_impl = """
### Implementation Files

#### RBAC Middleware and Helpers

```python
# rbac.py
from django.http import JsonResponse
from functools import wraps

class Role:
    ADMIN = 'admin'
    USER = 'user'
    MODERATOR = 'moderator'

class RBACMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Simple role/perm attachment for demo
            request.user.roles = ['user']
            if request.user.is_staff:
                request.user.roles.append('admin')
        return self.get_response(request)

def role_required(roles):
    if isinstance(roles, str):
        roles = [roles]
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Unauthorized'}, status=401)
            user_roles = getattr(request.user, 'roles', [])
            if not any(role in user_roles for role in roles):
                return JsonResponse({'error': 'Forbidden'}, status=403)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

class RBACService:
    @staticmethod
    def user_has_role(user, role):
        return role in getattr(user, 'roles', [])
```
"""

# 4. File Upload
upload_impl = """
### Implementation Files

#### File Upload Service

```python
# file_upload_service.py
import os
from django.conf import settings
from django.core.files.storage import default_storage

class FileUploadService:
    @staticmethod
    def upload_file(file):
        path = default_storage.save(f'uploads/{file.name}', file)
        return {
            'name': file.name,
            'path': path,
            'url': settings.MEDIA_URL + path
        }

    @staticmethod
    def upload_multiple_files(files):
        return [FileUploadService.upload_file(f) for f in files]

    @staticmethod
    def delete_file(path):
        if default_storage.exists(path):
            default_storage.delete(path)
            return True
        return False
```
"""

# 5. Global Error Handling
error_impl = """
### Implementation Files

#### Error Handling Middleware

```python
# error_handling.py
from django.http import JsonResponse
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
    return response

class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        return JsonResponse({
            'error': str(exception),
            'path': request.path,
            'method': request.method
        }, status=500)
```
"""

# 6. Logging System
logging_impl = """
### Implementation Files

#### Logging Configuration

```python
# logging_system.py
import logging

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/django.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

class CustomLogger:
    def info(self, msg, *args, **kwargs):
        logging.info(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        logging.error(msg, *args, **kwargs)
```
"""

# Insertion logic for Django
# Using simple appends or specific markers if found

if '### Email Templates' in content:
    content = content.replace('### Email Templates', mail_impl + '\n### Email Templates')

if '### Usage' in content:
    # Multiple Usage sections, let's be careful or just append at the end of sections
    pass

# To be safe and avoid markers that might not match exactly, I'll just append them 
# after the usage block of each section.

sections = [
    ('## 1. Mail Service', mail_impl),
    ('## 2. Notification System', notification_impl),
    ('## 3. RBAC (Role-Based Access Control)', rbac_impl),
    ('## 4. File Upload Service', upload_impl),
    ('## 5. Global Error Handling', error_impl),
    ('## 6. Logging System', logging_impl)
]

for section_title, impl in sections:
    # Find the next section or separator
    start_idx = content.find(section_title)
    if start_idx != -1:
        next_section_idx = content.find('\n---', start_idx)
        if next_section_idx == -1:
            next_section_idx = len(content)
        
        # Check if implementation already exists
        if '### Implementation Files' not in content[start_idx:next_section_idx]:
            content = content[:next_section_idx] + '\n' + impl + content[next_section_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated DJANGO_BOILERPLATE.md with all implementations!")
