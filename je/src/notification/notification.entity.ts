import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, UpdateDateColumn, ManyToOne } from 'typeorm';
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