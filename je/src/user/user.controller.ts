import { Controller, Get, Post, UseGuards } from '@nestjs/common';
import { Roles, Permissions, Role, Permission } from '../guards/rbac.guard';
import { JwtAuthGuard } from '../guards/jwt-auth.guard';
import { RolesGuard, PermissionsGuard } from '../guards/rbac.guard';

@Controller('users')
@UseGuards(JwtAuthGuard, RolesGuard)
export class UserController {
  // Only admins can access
  @Roles(Role.ADMIN)
  @Get('admin')
  getAdminData() {
    return 'Admin data';
  }

  // Multiple roles allowed
  @Roles(Role.ADMIN, Role.MODERATOR)
  @Get('moderate')
  getModerateData() {
    return 'Moderate data';
  }
}

// Using permissions
@UseGuards(JwtAuthGuard, PermissionsGuard)
@Controller('resources')
export class ResourceController {
  @Permissions(Permission.CREATE_USER)
  @Post()
  create() {
    return 'Create resource';
  }
}