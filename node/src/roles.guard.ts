import { Injectable, CanActivate, ExecutionContext, SetMetadata } from '@nestjs/common';
import { Reflector } from '@nestjs/core';

export enum Role {
  ADMIN = 'admin',
  USER = 'user',
  MODERATOR = 'moderator',
}

export enum Permission {
  CREATE_USER = 'create:user',
  READ_USER = 'read:user',
  UPDATE_USER = 'update:user',
  DELETE_USER = 'delete:user',
}

export const Roles = (...roles: Role[]) => SetMetadata('roles', roles);
export const Permissions = (...permissions: Permission[]) => SetMetadata('permissions', permissions);

@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredRoles = this.reflector.getAllAndOverride<Role[]>('roles', [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!requiredRoles) return true;
    const { user } = context.switchToHttp().getRequest();
    return requiredRoles.some((role) => user?.roles?.includes(role));
  }
}

@Injectable()
export class PermissionsGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const requiredPermissions = this.reflector.getAllAndOverride<Permission[]>('permissions', [
      context.getHandler(),
      context.getClass(),
    ]);
    if (!requiredPermissions) return true;
    const { user } = context.switchToHttp().getRequest();
    return requiredPermissions.every((permission) => user?.permissions?.includes(permission));
  }
}

@Injectable()
export class RbacService {
  hasRole(user: any, role: Role): boolean {
    return user?.roles?.includes(role);
  }
  hasPermission(user: any, permission: Permission): boolean {
    return user?.permissions?.includes(permission);
  }
}