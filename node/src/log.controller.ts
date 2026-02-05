import { Controller, Get, Query } from '@nestjs/common';
import { CustomLoggerService } from './logger/custom-logger.service';
import { LogLevel } from './log-entry.entity';

@Controller('logs')
export class LogController {
  constructor(private logger: CustomLoggerService) {}

  @Get()
  async getLogs(@Query('level') level?: LogLevel) {
    return this.logger.getRecentLogs(level);
  }
}