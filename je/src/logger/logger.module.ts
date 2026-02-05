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