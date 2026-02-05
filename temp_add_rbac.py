"""
Script to append complete implementations to NESTJS_BOILERPLATE.md
"""

implementations = """

### Implementation Files

#### RBAC Guard (Complete)

```typescript
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

export const Roles = (...roles: Role[]) => SetData('roles', roles);
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
```

#### RBAC Module

```typescript
import { Module } from '@nestjs/common';
import { RolesGuard, PermissionsGuard, RbacService } from './rbac.guard';

@Module({
  providers: [RolesGuard, PermissionsGuard, RbacService],
  exports: [RolesGuard, PermissionsGuard, RbacService],
})
export class RbacModule {}
```

"""

# Read the current file
with open(r'c:\Users\Anshul\Desktop\CLI tool (2)\CLI tool\files\NESTJS_BOILERPLATE.md', 'r', encoding='utf-8') as f:
   content = f.read()

# Find insertion point (after "export class AppModule {}")
insertion_point = content.find('export class AppModule {}\n```\n\n---\n\n## 4. File Upload Service')

if insertion_point != -1:
    # Insert implementations
    new_content = content[:insertion_point] + 'export class AppModule {}\n```\n' + implementations + '\n---\n\n## 4. File Upload Service' + content[insertion_point + len('export class AppModule {}\n```\n\n---\n\n## 4. File Upload Service'):]
    
    with open(r'c:\Users\Anshul\Desktop\CLI tool (2)\CLI tool\files\NESTJS_BOILERPLATE.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully added RBAC implementations!")
else:
    print("Could not find insertion point")
