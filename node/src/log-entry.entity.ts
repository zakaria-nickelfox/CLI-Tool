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