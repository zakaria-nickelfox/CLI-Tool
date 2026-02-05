import { Controller, Get, Patch, Param } from '@nestjs/common';
import { NotificationService } from './notification.service';
import { CurrentUser } from '../decorators/current-user.decorator';

@Controller('notifications')
export class NotificationController {
  constructor(private notificationService: NotificationService) {}

  @Get()
  async getNotifications(@CurrentUser() user) {
    return this.notificationService.findByUserId(user.id);
  }

  @Patch(':id/read')
  async markAsRead(@Param('id') id: string, @CurrentUser() user) {
    return this.notificationService.markAsRead(id, user.id);
  }
}