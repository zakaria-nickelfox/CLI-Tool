# NestJS Backend Boilerplate Documentation

This boilerplate provides a complete backend setup for NestJS with essential features commonly needed in modern applications.

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

Install core dependencies:
```bash
npm install @nestjs/config @nestjs/jwt @nestjs/passport passport passport-jwt @nestjs/platform-express reflect-metadata rxjs uuid
npm install -D @types/node @types/express @types/multer @types/passport-jwt @types/uuid
```

Install feature dependencies:
```bash
npm install nodemailer
npm install -D @types/nodemailer
```

### Configuration

Add to `.env`:
```env
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_SECURE=false
MAIL_USER=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=noreply@yourapp.com
FRONTEND_URL=http://localhost:3000
```

### Usage

```typescript
import { MailService } from './mail.service';

@Injectable()
export class UserService {
  constructor(private mailService: MailService) {}

  async createUser(email: string, name: string) {
    // ... user creation logic
    await this.mailService.sendMail(
      email,
      'Welcome!',
      `Welcome ${name}!`,
      `<h1>Welcome ${name}!</h1>`
    );
  }
}
```


### Module Registration

```typescript
import { MailService } from './mail.service';

@Module({
  providers: [MailService],
  exports: [MailService],
})
export class MailModule {}
```

### Implementation Files

#### Mail Service

```typescript
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import * as nodemailer from 'nodemailer';

@Injectable()
export class MailService {
  private transporter: nodemailer.Transporter;

  constructor(private configService: ConfigService) {
    this.transporter = nodemailer.createTransport({
      host: this.configService.get('MAIL_HOST', 'smtp.gmail.com'),
      port: this.configService.get('MAIL_PORT', 587),
      secure: false,
      auth: {
        user: this.configService.get('MAIL_USER'),
        pass: this.configService.get('MAIL_PASSWORD'),
      },
    });
  }

  async sendMail(
    to: string,
    subject: string,
    text?: string,
    html?: string,
  ): Promise<void> {
    try {
      await this.transporter.sendMail({
        from: this.configService.get('MAIL_FROM', 'noreply@example.com'),
        to,
        subject,
        text,
        html,
      });
    } catch (error) {
      console.error('Failed to send email:', error);
      throw new Error('Email sending failed');
    }
  }
}
```

#### Mail Module

```typescript
import { Module } from '@nestjs/common';
import { MailService } from './mail.service';

@Module({
  providers: [MailService],
  exports: [MailService],
})
export class MailModule {}
```

---

## 2. Notification System

### Setup

Create the entity and service in your database:
```bash
# TypeORM migration will create the notifications table
```

### Database Schema

The notification entity includes:
- `id` - UUID primary key
- `userId` - Foreign key to user
- `title` - Notification title
- `message` - Notification content
- `type` - Notification type (info, warning, error, success)
- `isRead` - Read status
- `readAt` - Read timestamp
- `metadata` - Additional JSON data
- `createdAt` - Creation timestamp
- `updatedAt` - Update timestamp

### Usage

```typescript
import { Injectable } from '@nestjs/common';
import { NotificationService } from './notification.service';
import { NotificationType } from '../enums/notification-type.enum';

@Injectable()
export class OrderService {
  constructor(private notificationService: NotificationService) {}

  async createOrder(userId: string) {
    // ... order creation logic
    
    await this.notificationService.create({
      userId,
      title: 'Order Placed',
      message: 'Your order has been successfully placed!',
      type: NotificationType.SUCCESS,
    });
  }
}
```

### API Endpoints Example

```typescript
@Controller('notifications')
export class NotificationController {
  constructor(private notificationService: NotificationService) {}

  @Get()
  async getNotifications(@CurrentUser() user) {
    return this.notificationService.findByUserId(user.id);
  }

  @Patch(':id/read')
  async markAsRead(@Param('id') id: string, @CurrentUser() user) {
    return this.notificationService.markAsRead(id, user.id);
  }
}
```

### Implementation Files

#### Notification Type Enum

```typescript
export enum NotificationType {
  INFO = 'info',
  SUCCESS = 'success',
  WARNING = 'warning',
  ERROR = 'error',
}
```

#### Notification Entity

```typescript
import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, ManyToOne } from '@nestjs/typeorm';
import { User } from '../entities/user.entity';
import { NotificationType } from '../enums/notification-type.enum';

@Entity('notifications')
export class Notification {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  userId: string;

  @ManyToOne(() => User)
  user: User;

  @Column()
  title: string;

  @Column('text')
  message: string;

  @Column({ type: 'enum', enum: NotificationType, default: NotificationType.INFO })
  type: NotificationType;

  @Column({ default: false })
  isRead: boolean;

  @Column({ nullable: true })
  readAt: Date;

  @Column('jsonb', { nullable: true })
  metadata: any;

  @CreateDateColumn()
  createdAt: Date;

  @UpdateDateColumn()
  updatedAt: Date;
}
```

#### Notification Service

```typescript
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Notification } from './notification.entity';

@Injectable()
export class NotificationService {
  constructor(
    @InjectRepository(Notification)
    private notificationRepository: Repository<Notification>,
  ) {}

  async create(data: Partial<Notification>): Promise<Notification> {
    const notification = this.notificationRepository.create(data);
    return this.notificationRepository.save(notification);
  }

  async findByUserId(userId: string): Promise<Notification[]> {
    return this.notificationRepository.find({
      where: { userId },
      order: { createdAt: 'DESC' },
    });
  }

  async markAsRead(id: string, userId: string): Promise<Notification> {
    const notification = await this.notificationRepository.findOne({
      where: { id, userId },
    });

    if (!notification) {
      throw new Error('Notification not found');
    }

    notification.isRead = true;
    notification.readAt = new Date();
    return this.notificationRepository.save(notification);
  }
}
```

#### Notification Controller

```typescript
import { Controller, Get, Patch, Param } from '@nestjs/common';
import { NotificationService } from './notification.service';
import { CurrentUser } from '../decorators/current-user.decorator';

@Controller('notifications')
export class NotificationController {
  constructor(private notificationService: NotificationService) {}

  @Get()
  async getNotifications(@CurrentUser() user) {
    return this.notificationService.findByUserId(user.id);
  }

  @Patch(':id/read')
  async markAsRead(@Param('id') id: string, @CurrentUser() user) {
    return this.notificationService.markAsRead(id, user.id);
  }
}
```

#### Notification Module

```typescript
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Notification } from './notification.entity';
import { NotificationService } from './notification.service';
import { NotificationController } from './notification.controller';

@Module({
  imports: [TypeOrmModule.forFeature([Notification])],
  providers: [NotificationService],
  controllers: [NotificationController],
  exports: [NotificationService],
})
export class NotificationModule {}
```

---

## 3. RBAC (Role-Based Access Control)

### Setup

```typescript
import { Module } from '@nestjs/common';
import { RolesGuard, PermissionsGuard, RbacService } from '../rbac/rbac.guard';

@Module({
  providers: [RolesGuard, PermissionsGuard, RbacService],
  exports: [RolesGuard, PermissionsGuard, RbacService],
})
export class RbacModule {}
```

### Usage with Decorators

```typescript
import { Controller, Get, Post, UseGuards } from '@nestjs/common';
import { Roles, Permissions, Role, Permission } from '../rbac/rbac.guard';
import { JwtAuthGuard } from '../guards/jwt-auth.guard';
import { RolesGuard, PermissionsGuard } from '../rbac/rbac.guard';

@Controller('users')
@UseGuards(JwtAuthGuard, RolesGuard)
export class UserController {
  // Only admins can access
  @Roles(Role.ADMIN)
  @Get('admin')
  getAdminData() {
    return 'Admin data';
  }

  // Multiple roles allowed
  @Roles(Role.ADMIN, Role.MODERATOR)
  @Get('moderate')
  getModerateData() {
    return 'Moderate data';
  }
}

// Using permissions
@UseGuards(JwtAuthGuard, PermissionsGuard)
@Controller('resources')
export class ResourceController {
  @Permissions(Permission.CREATE_USER)
  @Post()
  create() {
    return 'Create resource';
  }
}
```

### Global Guard Setup

```typescript
// main.ts or app.module.ts
import { Module } from '@nestjs/common';
import { APP_GUARD } from '@nestjs/core';
import { RolesGuard } from '../rbac/rbac.guard';

@Module({
  providers: [
    {
      provide: APP_GUARD,
      useClass: RolesGuard,
    },
  ],
})
export class AppModule {}
```


### Implementation Files

#### RBAC Guard (Complete)

```typescript
import { Injectable, CanActivate, ExecutionContext, SetMetadata } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

export enum Role {
  ADMIN = 'admin',
  USER = 'user',
  MODERATOR = 'moderator',
}

export enum Permission {
  CREATE_USER = 'create:user',
  READ_USER = 'read:user',
  UPDATE_USER = 'update:user',
  DELETE_USER = 'delete:user',
}

export const Roles = (...roles: Role[]) => SetMetadata('roles', roles);
export const Permissions = (...permissions: Permission[]) => SetMetadata('permissions', permissions);

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<Role[]>('roles', [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!requiredRoles) return true;
    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some((role) => user?.roles?.includes(role));
  }
}

@Injectable()
export class PermissionsGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredPermissions = this.reflector.getAllAndOverride<Permission[]>('permissions', [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!requiredPermissions) return true;
    const { user } = context.switchToHttp().getRequest();
    return requiredPermissions.every((permission) => user?.permissions?.includes(permission));
  }
}

@Injectable()
export class RbacService {
  hasRole(user: any, role: Role): boolean {
    return user?.roles?.includes(role);
  }
  hasPermission(user: any, permission: Permission): boolean {
    return user?.permissions?.includes(permission);
  }
}
```

#### RBAC Module

```typescript
import { Module } from '@nestjs/common';
import { RolesGuard, PermissionsGuard, RbacService } from './rbac.guard';

@Module({
  providers: [RolesGuard, PermissionsGuard, RbacService],
  exports: [RolesGuard, PermissionsGuard, RbacService],
})
export class RbacModule {}
```


---

## 4. File Upload Service

### Setup

Install dependencies:
```bash
npm install uuid
npm install -D @types/uuid
```

### Configuration

Add to `.env`:
```env
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880
BASE_URL=http://localhost:3000
```

### Usage with Multer

```typescript
import { FileUploadService } from './file-upload.service';
import { FileInterceptor } from '@nestjs/platform-express';

@Controller('upload')
export class UploadController {
  constructor(private fileUploadService: FileUploadService) {}

  @Post()
  @UseInterceptors(FileInterceptor('file'))
  async uploadFile(@UploadedFile() file: Express.Multer.File) {
    const result = await this.fileUploadService.uploadFile(file);
    return result;
  }

  @Post('multiple')
  @UseInterceptors(FilesInterceptor('files'))
  async uploadMultiple(@UploadedFiles() files: Express.Multer.File[]) {
    const results = await this.fileUploadService.uploadMultipleFiles(files);
    return results;
  }

  @Delete(':filename')
  async deleteFile(@Param('filename') filename: string) {
    await this.fileUploadService.deleteFile(filename);
    return { message: 'File deleted successfully' };
  }
}
```
### Implementation Files

#### File Upload Service

```typescript
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import * as fs from 'fs';
import * as path from 'path';
import { v4 as uuidv4 } from 'uuid';

@Injectable()
export class FileUploadService {
  private uploadDir: string;

  constructor(private configService: ConfigService) {
    this.uploadDir = this.configService.get('UPLOAD_DIR', './uploads');
    if (!fs.existsSync(this.uploadDir)) {
      fs.mkdirSync(this.uploadDir, { recursive: true });
    }
  }

  async uploadFile(file: any): Promise<{ filename: string; url: string }> {
    const fileExt = path.extname(file.originalname);
    const filename = `${uuidv4()}${fileExt}`;
    const filePath = path.join(this.uploadDir, filename);

    fs.writeFileSync(filePath, file.buffer);

    const baseUrl = this.configService.get('BASE_URL', 'http://localhost:3000');
    return {
      filename,
      url: `${baseUrl}/uploads/${filename}`,
    };
  }

  async uploadMultipleFiles(files: any[]): Promise<{ filename: string; url: string }[]> {
    return Promise.all(files.map(file => this.uploadFile(file)));
  }

  async deleteFile(filename: string): Promise<void> {
    const filePath = path.join(this.uploadDir, filename);
    if (fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }
  }
}
```

#### File Upload Module

```typescript
import { Module } from '@nestjs/common';
import { FileUploadService } from './file-upload.service';
import { UploadController } from './upload.controller';

@Module({
  providers: [FileUploadService],
  controllers: [UploadController],
  exports: [FileUploadService],
})
export class FileUploadModule {}
```

#### Upload Controller

```typescript
import { Controller, Post, UseInterceptors, UploadedFile, UploadedFiles, Delete, Param } from '@nestjs/common';
import { FileInterceptor, FilesInterceptor } from '@nestjs/platform-express';
import { FileUploadService } from './file-upload.service';

@Controller('upload')
export class UploadController {
  constructor(private fileUploadService: FileUploadService) {}

  @Post()
  @UseInterceptors(FileInterceptor('file'))
  async uploadFile(@UploadedFile() file: any) {
    return this.fileUploadService.uploadFile(file);
  }

  @Post('multiple')
  @UseInterceptors(FilesInterceptor('files'))
  async uploadMultiple(@UploadedFiles() files: any[]) {
    return this.fileUploadService.uploadMultipleFiles(files);
  }

  @Delete(':filename')
  async deleteFile(@Param('filename') filename: string) {
    await this.fileUploadService.deleteFile(filename);
    return { message: 'File deleted successfully' };
  }
}
```


---

## 5. Global Error Handling

### Setup

Register the filter globally:

```typescript
// main.ts
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { GlobalExceptionFilter } from './filters/global-exception.filter';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalFilters(new GlobalExceptionFilter());
  await app.listen(3000);
}
bootstrap();
```

### Usage

```typescript
import { AppError, NotFoundError, ValidationError } from './global-exception.filter';

@Injectable()
export class UserService {
  async findById(id: string) {
    const user = await this.userRepository.findOne({ where: { id } });
    
    if (!user) {
      throw new NotFoundError('User');
    }
    
    return user;
  }

  async createUser(dto: CreateUserDto) {
    if (!dto.email) {
      throw new ValidationError('Email is required');
    }
    
    // ... creation logic
  }
}
```
### Implementation Files

#### Global Exception Filter

```typescript
import { ExceptionFilter, Catch, ArgumentsHost, HttpException, HttpStatus } from '@nestjs/common';
import { Response, Request } from 'express';

@Catch()
export class GlobalExceptionFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();
    
    const status = exception instanceof HttpException
      ? exception.getStatus()
      : HttpStatus.INTERNAL_SERVER_ERROR;

    const message = exception instanceof HttpException
      ? exception.getResponse()
      : 'Internal server error';

    response.status(status).json({
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      message,
    });
  }
}

export class AppError extends Error {
  constructor(public message: string, public status: HttpStatus) {
    super(message);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super(`${resource} not found`, HttpStatus.NOT_FOUND);
  }
}

export class ValidationError extends AppError {
  constructor(message: string) {
    super(message, HttpStatus.BAD_REQUEST);
  }
}
```


---

## 6. Logging System

### Setup

Install dependencies:
```bash
npm install winston winston-daily-rotate-file
```

### Module Registration

```typescript
import { Module, Global } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { CustomLoggerService } from '../logger/custom-logger.service';
import { LogEntry } from '../entities/log-entry.entity';

@Global()
@Module({
  imports: [TypeOrmModule.forFeature([LogEntry])],
  providers: [CustomLoggerService],
  exports: [CustomLoggerService],
})
export class LoggerModule {}
```

### Configuration

Add to `.env`:
```env
LOG_LEVEL=info
SEND_ERROR_EMAILS=true
ADMIN_EMAIL=admin@yourapp.com
```

### Usage

```typescript
import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { CustomLoggerService } from './custom-logger.service';
import { CreateUserDto } from './dtos/create-user-dto.dto';
import { User } from './entities/user.entity';

@Injectable()
export class UserService {
  constructor(
    private logger: CustomLoggerService,
    @InjectRepository(User)
    private userRepository: Repository<User>,
  ) {}

  async createUser(dto: CreateUserDto) {
    this.logger.log('Creating new user', 'UserService', { email: dto.email });
    
    try {
      const user = await this.userRepository.save(dto);
      this.logger.log('User created successfully', 'UserService', { userId: user.id });
      return user;
    } catch (error) {
      this.logger.error(
        'Failed to create user',
        error.stack,
        'UserService',
        { email: dto.email }
      );
      throw error;
    }
  }
}
```

### Viewing Logs

```typescript
import { Controller, Get, Query } from '@nestjs/common';
import { CustomLoggerService } from '../logger/custom-logger.service';
import { LogLevel } from '../entities/log-entry.entity';

@Controller('logs')
export class LogController {
  constructor(private logger: CustomLoggerService) {}

  @Get()
  async getLogs(@Query('level') level?: LogLevel) {
    return this.logger.getRecentLogs(level);
  }
}
```
### Implementation Files

#### Custom Logger Service

```typescript
import { Injectable, LoggerService, Scope } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import * as winston from 'winston';
import 'winston-daily-rotate-file';
import { LogEntry, LogLevel } from '../entities/log-entry.entity';

@Injectable({ scope: Scope.TRANSIENT })
export class CustomLoggerService implements LoggerService {
  private logger: winston.Logger;

  constructor(
    @InjectRepository(LogEntry)
    private logRepository: Repository<LogEntry>,
  ) {
    this.logger = winston.createLogger({
      level: process.env.LOG_LEVEL || 'info',
      format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.json(),
      ),
      transports: [
        new winston.transports.Console({
          format: winston.format.combine(
            winston.format.colorize(),
            winston.format.simple(),
          ),
        }),
        new winston.transports.DailyRotateFile({
          filename: 'logs/application-%DATE%.log',
          datePattern: 'YYYY-MM-DD',
          zippedArchive: true,
          maxSize: '20m',
          maxFiles: '14d',
        }),
      ],
    });
  }

  log(message: string, context?: string, metadata?: any) {
    this.logger.info(message, { context, ...metadata });
    this.saveToDb(LogLevel.INFO, message, context);
  }

  error(message: string, trace?: string, context?: string, metadata?: any) {
    this.logger.error(message, { trace, context, ...metadata });
    this.saveToDb(LogLevel.ERROR, message, context, trace);
  }

  warn(message: string, context?: string) {
    this.logger.warn(message, { context });
    this.saveToDb(LogLevel.WARN, message, context);
  }

  private async saveToDb(level: LogLevel, message: string, context?: string, trace?: string) {
    try {
      const logEntry = this.logRepository.create({ level, message, context, trace });
      await this.logRepository.save(logEntry);
    } catch (err) {
      console.error('Failed to save log to DB', err);
    }
  }

  async getRecentLogs(level?: LogLevel, limit: number = 100): Promise<LogEntry[]> {
    const query = this.logRepository.createQueryBuilder('log');
    if (level) {
      query.where('log.level = :level', { level });
    }
    return query.orderBy('log.timestamp', 'DESC').limit(limit).getMany();
  }
}
```

#### Log Entry Entity

```typescript
import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from 'typeorm';

export enum LogLevel {
  INFO = 'info',
  WARN = 'warn',
  ERROR = 'error',
  DEBUG = 'debug',
}

@Entity('logs')
export class LogEntry {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ type: 'enum', enum: LogLevel })
  level: LogLevel;

  @Column('text')
  message: string;

  @Column({ nullable: true })
  context: string;

  @Column('text', { nullable: true })
  trace: string;

  @CreateDateColumn()
  timestamp: Date;
}
```

#### Logger Module

```typescript
import { Module, Global } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { LogEntry } from './log-entry.entity';
import { CustomLoggerService } from './custom-logger.service';

@Global()
@Module({
  imports: [TypeOrmModule.forFeature([LogEntry])],
  providers: [CustomLoggerService],
  exports: [CustomLoggerService],
})
export class LoggerModule {}
```

#### Log Controller

```typescript
import { Controller, Get, Query } from '@nestjs/common';
import { CustomLoggerService } from '../logger/custom-logger.service';
import { LogLevel } from '../entities/log-entry.entity';

@Controller('logs')
export class LogController {
  constructor(private logger: CustomLoggerService) {}

  @Get()
  async getLogs(@Query('level') level?: LogLevel) {
    return this.logger.getRecentLogs(level);
  }
}
```


---

## Complete Application Module Example

```typescript
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { MailModule } from './mail/mail.module';
import { NotificationModule } from './notification/notification.module';
import { RbacModule } from './rbac/rbac.module';
import { FileUploadModule } from './file-upload/file-upload.module';
import { LoggerModule } from './logger/logger.module';
import { APP_FILTER } from '@nestjs/core';
import { GlobalExceptionFilter } from './filters/global-exception.filter';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: process.env.DB_HOST,
      port: parseInt(process.env.DB_PORT),
      username: process.env.DB_USERNAME,
      password: process.env.DB_PASSWORD,
      database: process.env.DB_NAME,
      autoLoadEntities: true,
      synchronize: process.env.NODE_ENV === 'development',
    }),
    MailModule,
    NotificationModule,
    RbacModule,
    FileUploadModule,
    LoggerModule,
  ],
  providers: [
    {
      provide: APP_FILTER,
      useClass: GlobalExceptionFilter,
    },
  ],
})
export class AppModule {}
```

---

## Environment Variables Summary

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=password
DB_NAME=myapp

# Mail
MAIL_HOST=smtp.gmail.com
MAIL_PORT=587
MAIL_SECURE=false
MAIL_USER=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_FROM=noreply@yourapp.com

# File Upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=5242880
BASE_URL=http://localhost:3000

# Logging
LOG_LEVEL=info
SEND_ERROR_EMAILS=true
ADMIN_EMAIL=admin@yourapp.com

# Frontend
FRONTEND_URL=http://localhost:3000
```

---

## Testing

Example test for the mail service:

```typescript
import { Test } from '@nestjs/testing';
import { MailService } from './mail.service';
import { ConfigService } from '@nestjs/config';

describe('MailService', () => {
  let service: MailService;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        MailService,
        {
          provide: ConfigService,
          useValue: {
            get: jest.fn((key) => {
              const config = {
                MAIL_HOST: 'smtp.test.com',
                MAIL_PORT: 587,
                MAIL_USER: 'test@test.com',
                MAIL_PASSWORD: 'password',
                MAIL_FROM: 'noreply@test.com',
              };
              return config[key];
            }),
          },
        },
      ],
    }).compile();

    service = module.get<MailService>(MailService);
  });

  it('should send email', async () => {
    await expect(
      service.sendMail(
        'user@test.com',
        'Test',
        'Test message'
      )
    ).resolves.not.toThrow();
  });
});
```

---

## 7. Supporting Components

### Implementation Files

#### Current User Decorator

```typescript
import { createParamDecorator, ExecutionContext } from '@nestjs/common';

export const CurrentUser = createParamDecorator(
  (data: unknown, ctx: ExecutionContext) => {
    const request = ctx.switchToHttp().getRequest();
    return request.user;
  },
);
```

#### JWT Auth Guard

```typescript
import { Injectable } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';

@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {}
```

#### User Entity

```typescript
import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from 'typeorm';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column({ unique: true })
  email: string;

  @Column({ select: false })
  password: string;

  @Column('simple-array', { default: 'user' })
  roles: string[];

  @Column('simple-array', { default: '' })
  permissions: string[];

  @CreateDateColumn()
  createdAt: Date;
}
```

#### Create User DTO

```typescript
import { IsEmail, IsString, MinLength, IsOptional, IsArray } from 'class-validator';

export class CreateUserDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(6)
  password: string;

  @IsOptional()
  @IsArray()
  roles?: string[];

  @IsOptional()
  @IsArray()
  permissions?: string[];
}
```

---

## Complete Application Setup

#### Main Entry Point

```typescript
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { GlobalExceptionFilter } from './filters/global-exception.filter';
import { ValidationPipe } from '@nestjs/common';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.useGlobalFilters(new GlobalExceptionFilter());
  app.useGlobalPipes(new ValidationPipe({ whitelist: true, transform: true }));
  await app.listen(process.env.PORT || 3000);
}
bootstrap();
```

#### Application Module

```typescript
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { MailModule } from './mail/mail.module';
import { NotificationModule } from './notification/notification.module';
import { RbacModule } from './rbac/rbac.module';
import { FileUploadModule } from './file-upload/file-upload.module';
import { LoggerModule } from './logger/logger.module';
import { APP_FILTER, APP_GUARD } from '@nestjs/core';
import { GlobalExceptionFilter } from './filters/global-exception.filter';
import { RolesGuard } from './rbac/rbac.guard';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }),
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT) || 5432,
      username: process.env.DB_USERNAME || 'postgres',
      password: process.env.DB_PASSWORD || 'password',
      database: process.env.DB_NAME || 'myapp',
      autoLoadEntities: true,
      synchronize: true, // Only for development
    }),
    MailModule,
    NotificationModule,
    RbacModule,
    FileUploadModule,
    LoggerModule,
  ],
  providers: [
    {
      provide: APP_FILTER,
      useClass: GlobalExceptionFilter,
    },
    {
      provide: APP_GUARD,
      useClass: RolesGuard,
    },
  ],
})
export class AppModule {}
```
