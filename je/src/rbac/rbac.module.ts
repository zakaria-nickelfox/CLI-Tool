import { Module } from '@nestjs/common';
import { RolesGuard, PermissionsGuard, RbacService } from '../guards/rbac.guard';

@Module({
  providers: [RolesGuard, PermissionsGuard, RbacService],
  exports: [RolesGuard, PermissionsGuard, RbacService],
})
export class RbacModule {}