import { Test } from '@nestjs/testing';
import { MailService } from './mail/mail.service';
import { ConfigService } from '@nestjs/config';

describe('MailService', () => {
  let service: MailService;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        MailService,
        {
          provide: ConfigService,
          useValue: {
            get: jest.fn((key) => {
              const config = {
                MAIL_HOST: 'smtp.test.com',
                MAIL_PORT: 587,
                MAIL_USER: 'test@test.com',
                MAIL_PASSWORD: 'password',
                MAIL_FROM: 'noreply@test.com',
              };
              return config[key];
            }),
          },
        },
      ],
    }).compile();

    service = module.get<MailService>(MailService);
  });

  it('should send email', async () => {
    await expect(
      service.sendMail(
        'user@test.com',
        'Test',
        'Test message'
      )
    ).resolves.not.toThrow();
  });
});