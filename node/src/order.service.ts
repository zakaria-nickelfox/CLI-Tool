import { Injectable } from '@nestjs/common';
import { NotificationService } from './notification/notification.service';

@Injectable()
export class OrderService {
  constructor(private notificationService: NotificationService) {}

  async createOrder(userId: string) {
    // ... order creation logic
    
    await this.notificationService.create({
      userId,
      title: 'Order Placed',
      message: 'Your order has been successfully placed!',
      type: NotificationType.SUCCESS,
    });
  }
}