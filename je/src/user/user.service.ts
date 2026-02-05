import { Injectable } from '@nestjs/common';
import { MailService } from '../mail/mail.service';

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