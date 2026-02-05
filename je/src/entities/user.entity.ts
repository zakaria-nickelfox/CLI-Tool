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