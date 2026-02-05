import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { CustomLoggerService } from '../logger/custom-logger.service';
import { CreateUserDto } from './create-user-dto.dto';
import { User } from '../entities/user.entity';

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