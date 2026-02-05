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