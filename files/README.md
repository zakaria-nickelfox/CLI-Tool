# Complete Boilerplate Code Collection

This repository contains comprehensive boilerplate code for building full-stack applications with multiple technology stacks.

## 📦 What's Included

### Backend Technologies
- **NestJS (Node.js)** - TypeScript-based progressive Node.js framework
- **Django (Python)** - High-level Python web framework

### Frontend Technologies
- **React Native** - Mobile app development
- **React with Next.js** - Web app development

## 🎯 Features Implemented

All backend implementations include:

1. ✉️ **Mail Service** - Email sending with templates and attachments
2. 🔔 **Notification System** - User notifications with database storage
3. 🔐 **RBAC (Role-Based Access Control)** - Complete authorization system
4. 📁 **File Upload Service** - Document upload with validation
5. ⚠️ **Global Error Handling** - Centralized error management
6. 📊 **Logging System** - Multi-channel logging (file, database, email)

All frontend implementations include:

1. 🎨 **UI Components**
   - Button (with variants, loading states, icons)
   - Input (with validation, icons, multiple variants)
   - Card (container component with header/footer)
   - Table (with pagination, sorting, custom rendering)

2. 🔐 **RBAC Integration**
   - Authentication service
   - Role and permission checking
   - Protected routes/components
   - React hooks and HOCs

## 📂 Directory Structure

```
.
├── nestjs/
│   ├── mail.service.ts
│   ├── notification.service.ts
│   ├── notification.entity.ts
│   ├── rbac.guard.ts
│   ├── file-upload.service.ts
│   ├── global-exception.filter.ts
│   ├── custom-logger.service.ts
│   ├── log-entry.entity.ts
│   └── NESTJS_BOILERPLATE.md
│
├── django/
│   ├── mail_service.py
│   ├── notification_models.py
│   ├── rbac.py
│   ├── file_upload_service.py
│   ├── error_handling.py
│   ├── logging_system.py
│   └── DJANGO_BOILERPLATE.md
│
├── react-native/
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Card.tsx
│   ├── Table.tsx
│   ├── RBACService.tsx
│   └── REACT_NATIVE_BOILERPLATE.md
│
└── react-next/
    ├── Button.tsx
    ├── Input.tsx
    ├── Card.tsx
    ├── Table.tsx
    ├── RBACService.tsx
    └── REACT_NEXT_BOILERPLATE.md
```

## 🚀 Quick Start

### NestJS Backend

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env

# Run development server
npm run start:dev
```

See [nestjs/NESTJS_BOILERPLATE.md](nestjs/NESTJS_BOILERPLATE.md) for detailed setup.

### Django Backend

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

See [django/DJANGO_BOILERPLATE.md](django/DJANGO_BOILERPLATE.md) for detailed setup.

### React Native Frontend

```bash
# Install dependencies
npm install

# iOS
npx pod-install
npx react-native run-ios

# Android
npx react-native run-android
```

See [react-native/REACT_NATIVE_BOILERPLATE.md](react-native/REACT_NATIVE_BOILERPLATE.md) for detailed setup.

### React Next.js Frontend

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

See [react-next/REACT_NEXT_BOILERPLATE.md](react-next/REACT_NEXT_BOILERPLATE.md) for detailed setup.

## 📖 Documentation

Each technology stack has comprehensive documentation:

- **[NestJS Documentation](nestjs/NESTJS_BOILERPLATE.md)** - Complete backend guide
- **[Django Documentation](django/DJANGO_BOILERPLATE.md)** - Complete backend guide
- **[React Native Documentation](react-native/REACT_NATIVE_BOILERPLATE.md)** - Complete mobile guide
- **[React Next.js Documentation](react-next/REACT_NEXT_BOILERPLATE.md)** - Complete web guide

## 🔧 Common Configuration

### Backend Environment Variables

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=postgres
DB_PASSWORD=password

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
EMAIL_FROM=noreply@yourapp.com

# File Upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880

# Logging
LOG_LEVEL=info
SEND_ERROR_EMAILS=true
ADMIN_EMAIL=admin@yourapp.com

# Frontend
FRONTEND_URL=http://localhost:3000
```

### Frontend Environment Variables

```env
NEXT_PUBLIC_API_URL=https://api.yourapp.com
# or for React Native in .env or config
API_URL=https://api.yourapp.com
```

## 💡 Usage Examples

### Backend - Send Email

**NestJS:**
```typescript
await this.mailService.sendMail({
  to: 'user@example.com',
  subject: 'Welcome!',
  html: '<h1>Welcome to our platform!</h1>'
});
```

**Django:**
```python
MailService.send_email(
    subject='Welcome!',
    to_emails=['user@example.com'],
    html_content='<h1>Welcome to our platform!</h1>'
)
```

### Backend - Create Notification

**NestJS:**
```typescript
await this.notificationService.create({
  userId: user.id,
  title: 'New Message',
  message: 'You have a new message',
  type: NotificationType.INFO
});
```

**Django:**
```python
NotificationService.create_notification(
    user=request.user,
    title='New Message',
    message='You have a new message',
    notification_type=NotificationType.INFO
)
```

### Backend - RBAC Protection

**NestJS:**
```typescript
@Roles(Role.ADMIN)
@Get('admin')
getAdminData() {
  return 'Admin data';
}
```

**Django:**
```python
@role_required('admin')
def admin_view(request):
    return JsonResponse({'message': 'Admin access granted'})
```

### Frontend - Protected Component

**React Native:**
```tsx
const { hasRole, Role } = useRBAC();

{hasRole(Role.ADMIN) && (
  <Button title="Admin Panel" onPress={navigateToAdmin} />
)}
```

**React Next.js:**
```tsx
import { Protected, Role } from '@/services/RBACService';

<Protected roles={[Role.ADMIN]}>
  <AdminPanel />
</Protected>
```

## 🎨 UI Component Examples

### Button Usage

```tsx
// React Native & Next.js (similar API)
<Button 
  variant="primary"
  size="large"
  loading={isLoading}
  onPress={handleSubmit} // React Native
  onClick={handleSubmit} // Next.js
>
  Submit
</Button>
```

### Input with Validation

```tsx
<Input 
  label="Email"
  value={email}
  onChange={(e) => setEmail(e.target.value)}
  error={errors.email}
  fullWidth
/>
```

### Table with Data

```tsx
<Table 
  columns={[
    { key: 'name', title: 'Name' },
    { key: 'email', title: 'Email' }
  ]}
  data={users}
  onRowClick={(user) => navigate(`/users/${user.id}`)}
  striped
  hoverable
/>
```

## 🧪 Testing

All components and services include example tests. See documentation for each stack:

- NestJS: Jest + Supertest
- Django: Django Test Framework
- React Native: Jest + React Native Testing Library
- Next.js: Jest + React Testing Library

## 📝 License

MIT License - Feel free to use this boilerplate for your projects.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For questions or issues, please refer to the individual documentation files or create an issue in the repository.

---

**Note:** Remember to:
1. Update environment variables for your specific use case
2. Review security settings before production deployment
3. Configure CORS and authentication properly
4. Set up proper database connections
5. Configure email service with your SMTP credentials
