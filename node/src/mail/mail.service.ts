import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import * as nodemailer from 'nodemailer';

@Injectable()
export class MailService {
  private transporter: nodemailer.Transporter;

  constructor(private configService: ConfigService) {
    this.transporter = nodemailer.createTransport({
      host: this.configService.get('MAIL_HOST', 'smtp.gmail.com'),
      port: this.configService.get('MAIL_PORT', 587),
      secure: false,
      auth: {
        user: this.configService.get('MAIL_USER'),
        pass: this.configService.get('MAIL_PASSWORD'),
      },
    });
  }

  async sendMail(
    to: string,
    subject: string,
    text?: string,
    html?: string,
  ): Promise<void> {
    try {
      await this.transporter.sendMail({
        from: this.configService.get('MAIL_FROM', 'noreply@example.com'),
        to,
        subject,
        text,
        html,
      });
    } catch (error) {
      console.error('Failed to send email:', error);
      throw new Error('Email sending failed');
    }
  }
}