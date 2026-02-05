# Django Backend Boilerplate Documentation

This boilerplate provides a complete backend setup for Django with essential features commonly needed in modern applications.

## Features Included

1. **Mail Service** - Email sending functionality
2. **Notification System** - User notifications with database storage
3. **RBAC (Role-Based Access Control)** - Authorization and permissions
4. **File Upload Service** - Document upload handling
5. **Global Error Handling** - Centralized error management
6. **Logging System** - Multi-channel logging (file, database, email)

---

## 1. Mail Service

### Setup

Django's built-in email functionality is used. Configure in `settings.py`:

```python
# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'noreply@yourapp.com'

# Frontend URL for email links
FRONTEND_URL = 'http://localhost:3000'
```

### Usage

```python
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
```


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

### Email Templates

Create templates in `templates/emails/`:

```html
<!-- templates/emails/welcome.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
</head>
<body>
    <h1>Welcome {{ name }}!</h1>
    <p>Thanks for joining us!</p>
</body>
</html>
```

---

## 2. Notification System

### Setup

Add the model to your app:

```python
# models.py
from notification_models import Notification, NotificationType
```

Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Usage

```python
from notification_models import NotificationService, NotificationType

# Create notification
notification = NotificationService.create_notification(
    user=request.user,
    title='New Message',
    message='You have a new message from John',
    notification_type=NotificationType.INFO,
    metadata={'sender_id': 123}
)

# Get user notifications
notifications = NotificationService.get_user_notifications(request.user)

# Get unread notifications only
unread = NotificationService.get_user_notifications(request.user, unread_only=True)

# Mark as read
NotificationService.mark_as_read(notification_id, request.user)

# Mark all as read
NotificationService.mark_all_as_read(request.user)

# Get unread count
count = NotificationService.get_unread_count(request.user)
```

### API Views Example

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_notifications(request):
    notifications = NotificationService.get_user_notifications(request.user)
    return Response([
        {
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'type': n.type,
            'is_read': n.is_read,
            'created_at': n.created_at,
        }
        for n in notifications
    ])

@api_view(['PATCH'])
def mark_notification_read(request, pk):
    success = NotificationService.mark_as_read(pk, request.user)
    if success:
        return Response({'message': 'Marked as read'})
    return Response({'error': 'Not found'}, status=404)
```


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

---

## 3. RBAC (Role-Based Access Control)

### Setup

Add to `MIDDLEWARE` in `settings.py`:

```python
MIDDLEWARE = [
    # ... other middleware
    'rbac.RBACMiddleware',
]
```

### Usage with Decorators

```python
from rbac import role_required, permission_required, Role, PermissionConstants

# Require specific role
@role_required('admin')
def admin_view(request):
    return JsonResponse({'message': 'Admin access granted'})

# Require any of multiple roles
@role_required(['admin', 'moderator'])
def moderator_view(request):
    return JsonResponse({'message': 'Moderator access granted'})

# Require specific permission
@permission_required('create_user')
def create_user_view(request):
    # Create user logic
    pass

# Multiple permissions
@permission_required(['create_user', 'manage_roles'])
def advanced_admin_view(request):
    pass
```

### Using in Views

```python
from rbac import RBACService, Role

# Assign role to user
RBACService.assign_role_to_user(user, Role.ADMIN)

# Remove role
RBACService.remove_role_from_user(user, Role.MODERATOR)

# Check if user has role
if RBACService.user_has_role(user, Role.ADMIN):
    # Admin logic
    pass

# Get permissions for role
permissions = RBACService.get_permissions_for_role(Role.ADMIN)
```

### Using Request Helper Methods

```python
# After RBACMiddleware is applied
def my_view(request):
    if request.user.has_role('admin'):
        # Admin logic
        pass
    
    if request.user.has_perm_custom('create_user'):
        # Create user logic
        pass
```

### Django REST Framework Integration

```python
from rest_framework.permissions import BasePermission
from rbac import Role

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.has_role(Role.ADMIN)

# Use in ViewSet
class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminRole]
    # ...
```


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

---

## 4. File Upload Service

### Setup

Configure in `settings.py`:

```python
# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
```

Update `urls.py` for development:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... your urls
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Usage

```python
from file_upload_service import FileUploadService

# Upload single file
def upload_file_view(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        try:
            result = FileUploadService.upload_file(uploaded_file)
            return JsonResponse(result)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

# Upload multiple files
def upload_multiple_view(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files')
        results = FileUploadService.upload_multiple_files(files)
        return JsonResponse({'results': results})

# Delete file
def delete_file_view(request, filename):
    success = FileUploadService.delete_file(f'uploads/{filename}')
    if success:
        return JsonResponse({'message': 'File deleted'})
    return JsonResponse({'error': 'File not found'}, status=404)
```

### Using the File Model

```python
from file_upload_service import UploadedFileModel

# Save file with metadata
def upload_with_metadata(request):
    if request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        file_record = UploadedFileModel.objects.create(
            user=request.user,
            file=uploaded_file,
            original_name=uploaded_file.name,
            file_size=uploaded_file.size,
            mime_type=uploaded_file.content_type,
            metadata={'description': request.POST.get('description')}
        )
        
        return JsonResponse({
            'id': file_record.id,
            'url': file_record.file_url,
        })

# Get user's files
def get_user_files(request):
    files = UploadedFileModel.objects.filter(user=request.user)
    return JsonResponse({
        'files': [
            {
                'id': f.id,
                'name': f.original_name,
                'url': f.file_url,
                'size': f.file_size,
                'uploaded_at': f.uploaded_at,
            }
            for f in files
        ]
    })
```

### REST Framework Integration

```python
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'No file provided'}, status=400)
        
        try:
            result = FileUploadService.upload_file(file)
            return Response(result)
        except ValueError as e:
            return Response({'error': str(e)}, status=400)
```


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

---

## 5. Global Error Handling

### Setup

For Django REST Framework, configure in `settings.py`:

```python
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'error_handling.custom_exception_handler',
}
```

For regular Django views, add middleware in `settings.py`:

```python
MIDDLEWARE = [
    # ... other middleware
    'error_handling.ErrorHandlingMiddleware',
]
```

### Usage

```python
from error_handling import (
    AppError, 
    ValidationError, 
    NotFoundError, 
    UnauthorizedError,
    ForbiddenError
)

# Raise custom errors
def get_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise NotFoundError('User')
    return JsonResponse({'user': user.email})

def create_user(request):
    email = request.POST.get('email')
    if not email:
        raise ValidationError('Email is required')
    
    if User.objects.filter(email=email).exists():
        raise ValidationError('Email already exists', {'email': 'Duplicate email'})
    
    # Create user logic
    pass

def admin_only_view(request):
    if not request.user.is_staff:
        raise ForbiddenError('Admin access required')
    # Admin logic
    pass
```

### Error Response Format

All errors return JSON in this format:

```json
{
    "statusCode": 404,
    "message": "User not found",
    "code": "NOT_FOUND",
    "path": "/api/users/123",
    "method": "GET"
}
```

For validation errors with details:

```json
{
    "statusCode": 400,
    "message": "Validation error",
    "code": "VALIDATION_ERROR",
    "path": "/api/users/",
    "method": "POST",
    "errors": {
        "email": "Duplicate email"
    }
}
```


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

---

## 6. Logging System

### Setup

Add to `settings.py`:

```python
from logging_system import LOGGING_CONFIG

LOGGING = LOGGING_CONFIG

# Additional settings
SEND_ERROR_EMAILS = True
ADMIN_EMAIL = 'admin@yourapp.com'
```

Create logs directory:

```bash
mkdir logs
```

### Usage

```python
from logging_system import CustomLogger

logger = CustomLogger()

# Log messages
logger.info('User logged in', context='AuthService', user=request.user)

logger.warning('High memory usage', context='SystemMonitor', 
               metadata={'memory': '85%'})

logger.error('Database connection failed', context='DatabaseService',
             exc_info=sys.exc_info())

# Log with metadata
logger.info('Payment processed', 
            context='PaymentService',
            metadata={
                'amount': 100.00,
                'currency': 'USD',
                'transaction_id': 'TXN123'
            },
            user=request.user)
```

### Viewing Logs from Database

```python
from logging_system import CustomLogger, LogLevel

# Get recent error logs
error_logs = CustomLogger.get_recent_logs(level=LogLevel.ERROR, limit=50)

# Get all recent logs
all_logs = CustomLogger.get_recent_logs(limit=100)

# Create admin view
def view_logs(request):
    logs = CustomLogger.get_recent_logs(limit=100)
    return render(request, 'admin/logs.html', {'logs': logs})
```

### Log API Endpoint

```python
from rest_framework.decorators import api_view
from logging_system import LogLevel, CustomLogger

@api_view(['GET'])
@role_required('admin')
def get_logs(request):
    level = request.GET.get('level')
    limit = int(request.GET.get('limit', 100))
    
    logs = CustomLogger.get_recent_logs(level=level, limit=limit)
    
    return Response([
        {
            'id': log.id,
            'level': log.level,
            'message': log.message,
            'context': log.context,
            'timestamp': log.timestamp,
            'metadata': log.metadata,
        }
        for log in logs
    ])
```


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

---

## Complete Django Project Setup

### settings.py

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@yourapp.com')

# Frontend URL
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

# File Upload
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB

# Logging
from logging_system import LOGGING_CONFIG
LOGGING = LOGGING_CONFIG
SEND_ERROR_EMAILS = os.getenv('SEND_ERROR_EMAILS', 'True') == 'True'
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@yourapp.com')

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rbac.RBACMiddleware',
    'error_handling.ErrorHandlingMiddleware',
]

# REST Framework
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'error_handling.custom_exception_handler',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Installed Apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    # Your apps
]
```

### urls.py

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('your_app.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Environment Variables

Create a `.env` file:

```env
# Database
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourapp.com

# Frontend
FRONTEND_URL=http://localhost:3000

# Logging
SEND_ERROR_EMAILS=True
ADMIN_EMAIL=admin@yourapp.com

# Security
SECRET_KEY=your-secret-key-here
DEBUG=True
```

Load environment variables in `settings.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Testing

Example test for mail service:

```python
from django.test import TestCase
from django.core import mail
from mail_service import MailService

class MailServiceTestCase(TestCase):
    def test_send_email(self):
        success = MailService.send_email(
            subject='Test',
            to_emails=['test@example.com'],
            text_content='Test message'
        )
        
        self.assertTrue(success)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test')

    def test_send_welcome_email(self):
        success = MailService.send_welcome_email('user@example.com', 'John')
        self.assertTrue(success)
```

Example test for RBAC:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from rbac import RBACService, Role

class RBACTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test@example.com', password='test')
    
    def test_assign_role(self):
        RBACService.assign_role_to_user(self.user, Role.ADMIN)
        self.assertTrue(RBACService.user_has_role(self.user, Role.ADMIN))
    
    def test_get_permissions(self):
        permissions = RBACService.get_permissions_for_role(Role.ADMIN)
        self.assertIn('create_user', permissions)
```
