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
import { RolesGuard } from './guards/rbac.guard';

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