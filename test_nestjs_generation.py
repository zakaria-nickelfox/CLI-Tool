#!/usr/bin/env python3
"""
Test script to verify NestJS project generation fixes.
This script generates a test project and checks for common import errors.
"""

import os
import subprocess
import sys
from pathlib import Path
import shutil

def run_command(cmd, cwd=None):
    """Run a shell command and return the result."""
    result = subprocess.run(
        cmd,
        shell=True,
        cwd=cwd,
        capture_output=True,
        text=True
    )
    return result

def test_project_generation():
    """Test generating a NestJS project with all features."""
    print("=" * 60)
    print("Testing NestJS Project Generation")
    print("=" * 60)
    
    test_project_name = "test-nestjs-project"
    test_project_path = Path(test_project_name)
    
    # Clean up any existing test project
    if test_project_path.exists():
        print(f"\n🧹 Cleaning up existing test project: {test_project_name}")
        shutil.rmtree(test_project_path)
    
    print(f"\n✨ Generating new NestJS project: {test_project_name}")
    print("   (This will be done manually - script provides instructions)")
    print("\n📋 Instructions:")
    print("   1. Run: python -m geninit")
    print("   2. Select: NestJS")
    print("   3. Project name: test-nestjs-project")
    print("   4. Select ALL features")
    print("\n⏸️  Press Enter after you've generated the project...")
    input()
    
    if not test_project_path.exists():
        print(f"\n❌ Error: Project directory '{test_project_name}' not found!")
        print("   Please generate the project first.")
        return False
    
    print(f"\n✅ Project directory found: {test_project_name}")
    
    # Check for required files
    print("\n📁 Checking file structure...")
    required_files = {
        'src/rbac/rbac.guard.ts': 'RBAC guard file',
        'src/entities/log-entry.entity.ts': 'LogEntry entity',
        'src/logger/custom-logger.service.ts': 'Logger service',
        'src/guards/jwt-auth.guard.ts': 'JWT guard',
        'src/enums/notification-type.enum.ts': 'NotificationType enum',
        'src/main.ts': 'Main entry point',
        'src/app.module.ts': 'App module',
        'package.json': 'Package.json',
        'tsconfig.json': 'TypeScript config',
    }
    
    missing_files = []
    for file_path, description in required_files.items():
        full_path = test_project_path / file_path
        if full_path.exists():
            print(f"   ✅ {description}: {file_path}")
        else:
            print(f"   ❌ {description}: {file_path} - MISSING!")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n❌ Missing {len(missing_files)} required files!")
        return False
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    result = run_command("npm install", cwd=test_project_path)
    if result.returncode != 0:
        print(f"   ❌ npm install failed!")
        print(f"   Error: {result.stderr}")
        return False
    print("   ✅ Dependencies installed successfully")
    
    # Run TypeScript build
    print("\n🔨 Building project...")
    result = run_command("npm run build", cwd=test_project_path)
    
    if result.returncode != 0:
        print(f"   ❌ Build failed!")
        print(f"\n📋 Build errors:")
        print(result.stdout)
        print(result.stderr)
        
        # Analyze errors
        errors = result.stdout + result.stderr
        error_types = {
            "Cannot find module": 0,
            "Cannot find name": 0,
            "TS2307": 0,  # Cannot find module
            "TS2304": 0,  # Cannot find name
            "TS2552": 0,  # Cannot find name (did you mean)
        }
        
        for error_type in error_types:
            count = errors.count(error_type)
            if count > 0:
                error_types[error_type] = count
        
        print(f"\n📊 Error Summary:")
        for error_type, count in error_types.items():
            if count > 0:
                print(f"   • {error_type}: {count} occurrences")
        
        return False
    
    print("   ✅ Build successful!")
    
    # Check for specific import issues
    print("\n🔍 Checking for common import issues...")
    issues_found = []
    
    files_to_check = [
        ('src/main.ts', ['NestFactory', 'AppModule']),
        ('src/app.module.ts', ['RolesGuard']),
        ('src/user/user.controller.ts', ['JwtAuthGuard', 'RolesGuard']),
        ('src/order.service.ts', ['NotificationType']),
        ('src/logger/custom-logger.service.ts', ['LogEntry', 'LogLevel']),
    ]
    
    for file_path, required_imports in files_to_check:
        full_path = test_project_path / file_path
        if full_path.exists():
            content = full_path.read_text()
            for imp in required_imports:
                if imp not in content:
                    issues_found.append(f"{file_path}: Missing '{imp}' in imports")
                    print(f"   ⚠️  {file_path}: Missing '{imp}'")
    
    if issues_found:
        print(f"\n⚠️  Found {len(issues_found)} potential import issues")
        for issue in issues_found:
            print(f"   • {issue}")
    else:
        print("   ✅ All required imports found")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print(f"\n🎉 The generated project builds successfully!")
    print(f"   Project location: {test_project_path.absolute()}")
    print(f"\n🚀 To run the project:")
    print(f"   cd {test_project_name}")
    print(f"   npm run start:dev")
    
    return True

if __name__ == "__main__":
    success = test_project_generation()
    sys.exit(0 if success else 1)
