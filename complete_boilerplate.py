import os

file_path = r'c:\Users\Anshul\Desktop\CLI tool (2)\CLI tool\files\NESTJS_BOILERPLATE.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Implementations to add

# 1. File Upload Service
upload_impl = """
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
"""

# 2. Global Error Handling
error_impl = """
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
"""

# 3. Logging System
logging_impl = """
### Implementation Files

#### Custom Logger Service

```typescript
import { Injectable, LoggerService, Scope } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import * as winston from 'winston';
import 'winston-daily-rotate-file';
import { LogEntry, LogLevel } from './log-entry.entity';

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

  log(message: string, context?: string) {
    this.logger.info(message, { context });
    this.saveToDb(LogLevel.INFO, message, context);
  }

  error(message: string, trace?: string, context?: string) {
    this.logger.error(message, { trace, context });
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
import { CustomLoggerService } from './custom-logger.service';
import { LogLevel } from './log-entry.entity';

@Controller('logs')
export class LogController {
  constructor(private logger: CustomLoggerService) {}

  @Get()
  async getLogs(@Query('level') level?: LogLevel) {
    return this.logger.getRecentLogs(level);
  }
}
```
"""

# 4. Supporting Components
supporting_impl = """
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
"""

# Main Application and Entry
main_app_impl = """
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
"""

# Insertion logic
# File upload is section 4
# Error handling is section 5
# Logging system is section 6

# Insert File Upload
upload_marker = 'await this.fileUploadService.deleteFile(filename);\n    return { message: \'File deleted successfully\' };\n  }\n}\n```'
if upload_marker in content:
    content = content.replace(upload_marker, upload_marker + upload_impl)

# Insert Error Handling
error_marker = '    // ... creation logic\n  }\n}\n```'
if error_marker in content:
    content = content.replace(error_marker, error_marker + error_impl)

# Insert Logging
logging_marker = 'async getLogs(@Query(\'level\') level?: LogLevel) {\n    return this.logger.getRecentLogs(level);\n  }\n}\n```'
if logging_marker in content:
    content = content.replace(logging_marker, logging_marker + logging_impl)

# Append Supporting and Main App
content += "\n---\n" + supporting_impl
content += "\n---\n" + main_app_impl

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated NESTJS_BOILERPLATE.md with all implementations!")
