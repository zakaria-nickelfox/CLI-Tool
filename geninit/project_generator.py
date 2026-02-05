"""
Project generator that creates complete project structures from boilerplate templates.
"""
import os
import re
import json
from pathlib import Path
from typing import Dict, List
from .template_parser import BoilerplateParser


class ProjectGenerator:
    """Generate complete project structure from selected features."""
    
    # Framework-specific project structures
    DJANGO_STRUCTURE = {
        'manage.py': 'django_manage',
        'requirements.txt': 'requirements',
        '.env.example': 'env_example',
        'README.md': 'readme',
        'config/__init__.py': '',
        'config/settings/__init__.py': 'django_settings_init',
        'config/settings/base.py': 'django_settings_base',
        'config/settings/local.py': 'django_settings_local',
        'config/urls.py': 'django_urls',
        'config/wsgi.py': 'django_wsgi',
        'apps/__init__.py': '',
        'core/__init__.py': '',
        'services/__init__.py': '',
        'run_local.bat': 'django_run_bat',
    }
    
    NESTJS_STRUCTURE = {
        'package.json': 'nestjs_package',
        'tsconfig.json': 'nestjs_tsconfig',
        '.env.example': 'env_example',
        'README.md': 'readme',
        'src/main.ts': 'nestjs_main',
        'src/app.module.ts': 'nestjs_app_module',
        'src/app.controller.ts': 'nestjs_app_controller',
        'src/app.service.ts': 'nestjs_app_service',
    }
    
    def __init__(self, framework: str, project_name: str):
        self.framework = framework
        self.project_name = project_name
        self.project_path = Path(project_name)
        self.generated_files = {}
    
    def generate(self, parser: BoilerplateParser, selected_features: List[str]):
        """Generate the complete project."""
        # Create project directory
        self.project_path.mkdir(exist_ok=True)
        
        # Create base structure
        self._create_base_structure()
        
        # Extract and create feature files
        files = parser.get_files_for_features(selected_features)
        
        # Find all referenced files from imports
        referenced_paths = parser.find_referenced_files(selected_features)
        
        # Extract referenced files that aren't already in our files dict
        for ref_path in referenced_paths:
            # Normalize path to just filename
            filename = Path(ref_path).name
            
            # Skip if we already have this file
            if filename in files:
                continue
            
            # Try to extract this file from the boilerplate
            content = parser.extract_file_by_path(ref_path)
            if content:
                files[filename] = content
        
        # Create all files
        self._create_feature_files(files)
        
        # Create configuration files
        self._create_config_files(parser, selected_features)

        # Fix NestJS imports
        self._fix_import_paths()
        
        # Create README
        self._create_readme(selected_features)
    
    def _create_base_structure(self):
        """Create the base directory structure."""
        if 'Django' in self.framework:
            dirs = ['config/settings', 'apps', 'core', 'services', 'static', 'media', 'logs']
        elif 'NestJS' in self.framework:
            dirs = [
                'src/modules', 'src/filters', 'src/guards', 'src/services', 
                'src/entities', 'src/enums', 'src/decorators', 'src/dtos', 
                'src/interfaces'
            ]
        elif 'React Native' in self.framework:
            dirs = ['src/components', 'src/screens', 'src/services', 'src/hooks', 'src/utils']
        elif 'React' in self.framework and 'Next' in self.framework:
            dirs = ['src/components', 'src/pages', 'src/services', 'src/hooks', 'src/utils', 'public']
        else:
            dirs = ['src']
        
        for dir_path in dirs:
            path = self.project_path / dir_path
            path.mkdir(parents=True, exist_ok=True)
            # Add __init__.py for Django projects
            if 'Django' in self.framework and not str(dir_path).startswith(('static', 'media', 'templates', 'logs')):
                 with open(path / '__init__.py', 'w') as f:
                     pass
    
    def _create_feature_files(self, files: Dict[str, str]):
        """Create files extracted from features."""
        for filename, content in files.items():
            # Determine target directory based on file type
            if 'Django' in self.framework:
                if '_service' in filename or 'file_upload' in filename or 'mail' in filename:
                    target_dir = self.project_path / 'services'
                elif '_models' in filename or 'notification' in filename:
                    target_dir = self.project_path / 'apps'
                elif 'rbac' in filename or 'error' in filename or 'logging' in filename:
                    target_dir = self.project_path / 'core'
                else:
                    target_dir = self.project_path / 'core'
            elif 'NestJS' in self.framework:
                # Enhanced heuristics for feature folders
                if '.enum.ts' in filename:
                    target_dir = self.project_path / 'src/enums'
                elif '.decorator.ts' in filename:
                    target_dir = self.project_path / 'src/decorators'
                elif '.dto.ts' in filename:
                    target_dir = self.project_path / 'src/dtos'
                elif '.interface.ts' in filename:
                    target_dir = self.project_path / 'src/interfaces'
                elif '.guard.ts' in filename:
                    target_dir = self.project_path / 'src/guards'
                elif '.filter.ts' in filename:
                    target_dir = self.project_path / 'src/filters'
                elif 'mail' in filename:
                    target_dir = self.project_path / 'src/mail'
                elif 'notification' in filename:
                    target_dir = self.project_path / 'src/notification'
                elif 'rbac' in filename:
                    target_dir = self.project_path / 'src/rbac'
                elif 'upload' in filename or 'file-upload' in filename:
                    target_dir = self.project_path / 'src/file-upload'
                elif 'logger' in filename or 'logging' in filename or 'log-entry' in filename:
                    target_dir = self.project_path / 'src/logger'
                elif '.entity.ts' in filename:
                    target_dir = self.project_path / 'src/entities'
                elif 'user' in filename and ('.service.ts' in filename or '.controller.ts' in filename):
                    target_dir = self.project_path / 'src/user'
                else:
                    target_dir = self.project_path / 'src'
            else:
                target_dir = self.project_path / 'src'
            
            target_dir.mkdir(parents=True, exist_ok=True)
            file_path = target_dir / filename
            
            # Ensure parent directories exist for nested file paths
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.generated_files[filename] = file_path
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
    
    def _create_config_files(self, parser: BoilerplateParser, selected_features: List[str]):
        """Create configuration files (package.json, requirements.txt, etc.)."""
        if 'Django' in self.framework:
            self._create_django_config(parser, selected_features)
        elif 'NestJS' in self.framework:
            self._create_nestjs_config(parser, selected_features)
    
    def _create_django_config(self, parser: BoilerplateParser, selected_features: List[str]):
        """Create Django-specific configuration files."""
        # Create requirements.txt
        deps = parser.get_dependencies()
        base_deps = ['Django>=4.2', 'djangorestframework>=3.14', 'python-decouple>=3.8', 'dj-database-url>=2.0']
        all_deps = base_deps + deps.get('pip', [])
        
        # Clean dependencies (remove trailing dots, whitespace, etc)
        clean_deps = set()
        for dep in all_deps:
            clean_dep = dep.strip().rstrip('.,;')
            if clean_dep:
                clean_deps.add(clean_dep)
        
        req_file = self.project_path / 'requirements.txt'
        with open(req_file, 'w') as f:
            f.write(chr(10).join(sorted(clean_deps)))
        
        # Create .env.example
        env_content = parser.get_env_template()
        if env_content:
            env_file = self.project_path / '.env.example'
            with open(env_file, 'w') as f:
                f.write(env_content)
        
        # Create manage.py
        manage_py = self.project_path / 'manage.py'
        with open(manage_py, 'w') as f:
            f.write(self._get_django_manage_py())
        
        # Create run_local.bat
        run_bat = self.project_path / 'run_local.bat'
        with open(run_bat, 'w') as f:
            f.write(self._get_django_run_bat())
        
        # Create core config files (urls.py, wsgi.py, settings)
        self._create_django_core_files(selected_features)

    def _create_django_core_files(self, selected_features: List[str]):
        """Create core Django files like urls.py and wsgi.py."""
        config_dir = self.project_path / 'config'
        config_dir.mkdir(exist_ok=True)
        
        # config/__init__.py
        with open(config_dir / '__init__.py', 'w') as f:
            f.write('')
            
        # config/wsgi.py
        with open(config_dir / 'wsgi.py', 'w') as f:
            f.write(self._get_django_wsgi())
            
        # config/urls.py
        with open(config_dir / 'urls.py', 'w') as f:
            f.write(self._get_django_urls(selected_features))
            
        # Settings
        self._create_django_settings(selected_features)

    def _get_django_wsgi(self) -> str:
        return '''import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
'''

    def _get_django_urls(self, selected_features: List[str]) -> str:
        return '''from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # Feature URLs will need to be added here manually or by feature setup
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''
    
    def _create_nestjs_config(self, parser: BoilerplateParser, selected_features: List[str]):
        """Create NestJS-specific configuration files."""
        deps = parser.get_dependencies()
        
        # Create package.json
        package_json = {
            "name": self.project_name,
            "version": "1.0.0",
            "description": "NestJS application with selected features",
            "scripts": {
                "start": "nest start",
                "start:dev": "nest start --watch",
                "start:prod": "node dist/main",
                "build": "nest build"
            },
            "dependencies": {
                "@nestjs/common": "^10.0.0",
                "@nestjs/core": "^10.0.0",
                "@nestjs/platform-express": "^10.0.0",
                "@nestjs/typeorm": "^10.0.0",
                "typeorm": "^0.3.0",
                "pg": "^8.0.0",
                "class-validator": "^0.14.0",
                "class-transformer": "^0.5.0",
                **{dep: "latest" for dep in deps.get('npm', [])}
            },
            "devDependencies": {
                "@nestjs/cli": "^10.0.0",
                "@nestjs/schematics": "^10.0.0",
                "@types/jest": "^29.5.0",
                "jest": "^29.5.0",
                "ts-jest": "^29.1.0",
                "@nestjs/testing": "^10.0.0",
                "@types/supertest": "^2.0.12",
                "@types/node": "^20.0.0",
                "typescript": "^5.0.0",
                **{dep: "latest" for dep in deps.get('npm_dev', [])}
            }
        }
        
        pkg_file = self.project_path / 'package.json'
        with open(pkg_file, 'w') as f:
            json.dump(package_json, f, indent=2)
        
        # Create tsconfig.json
        tsconfig = {
            "compilerOptions": {
                "module": "commonjs",
                "declaration": True,
                "removeComments": True,
                "emitDecoratorMetadata": True,
                "experimentalDecorators": True,
                "allowSyntheticDefaultImports": True,
                "target": "ES2021",
                "sourceMap": True,
                "outDir": "./dist",
                "baseUrl": "./",
                "incremental": True,
                "skipLibCheck": True,
                "strictNullChecks": False,
                "noImplicitAny": False,
                "strictBindCallApply": False,
                "forceConsistentCasingInFileNames": False,
                "noFallthroughCasesInSwitch": False
            }
        }
        
        ts_file = self.project_path / 'tsconfig.json'
        with open(ts_file, 'w') as f:
            json.dump(tsconfig, f, indent=2)
        
        # Create .env.example
        env_content = parser.get_env_template()
        if env_content:
            env_file = self.project_path / '.env.example'
            with open(env_file, 'w') as f:
                f.write(env_content)
    
    def _create_django_settings(self, selected_features: List[str]):
        """Create Django settings files."""
        settings_dir = self.project_path / 'config/settings'
        
        # Create __init__.py
        init_file = settings_dir / '__init__.py'
        with open(init_file, 'w') as f:
            f.write('from .local import *\n')
        
        # Create base.py (simplified)
        base_file = settings_dir / 'base.py'
        with open(base_file, 'w') as f:
            f.write(self._get_django_base_settings(selected_features))
        
        # Create local.py
        local_file = settings_dir / 'local.py'
        with open(local_file, 'w') as f:
            f.write('from .base import *\n\nDEBUG = True\n')
    
    def _get_django_manage_py(self) -> str:
        return '''#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed?"
        ) from exc
    execute_from_command_line(sys.argv)
'''
    
    def _get_django_run_bat(self) -> str:
        return '''@echo off
echo Creating virtual environment...
python -m venv venv
call venv\\Scripts\\activate
echo Installing dependencies...
pip install -r requirements.txt
echo Running migrations...
python manage.py migrate
echo Starting server...
python manage.py runserver
'''
    
    def _get_django_base_settings(self, selected_features: List[str]) -> str:
        return f'''import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATES = [
    {{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {{
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        }},
    }},
]

ROOT_URLCONF = 'config.urls'

DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }}
}}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
'''
    
    def _create_readme(self, selected_features: List[str]):
        """Create README file."""
        readme_content = f'''# {self.project_name}

Generated with GenInit

## Features Included

{chr(10).join(f"- {feature}" for feature in selected_features)}

## Setup

### Installation

'''
        
        if 'Django' in self.framework:
            readme_content += '''```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\\Scripts\\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```
'''
        elif 'NestJS' in self.framework:
            readme_content += '''```bash
# Install dependencies
npm install

# Start development server
npm run start:dev

# Build for production
npm run build
```
'''
        
        readme_file = self.project_path / 'README.md'
        with open(readme_file, 'w') as f:
            f.write(readme_content)

    def _fix_import_paths(self):
        """Fix import paths for generated NestJS files."""
        if 'NestJS' not in self.framework: 
            return

        # Build a comprehensive file map: filename (without extension) -> full path
        file_map = {}
        for filename, file_path in self.generated_files.items():
            if str(file_path).endswith('.ts'):
                # Store both with and without extension
                base_name = filename.replace('.ts', '')
                file_map[base_name] = file_path
                file_map[filename] = file_path
        
        # Also scan the src directory for any files we might have missed
        src_dir = self.project_path / 'src'
        if src_dir.exists():
            for ts_file in src_dir.rglob('*.ts'):
                rel_to_src = ts_file.relative_to(src_dir)
                base_name = ts_file.stem
                file_map[base_name] = ts_file
                file_map[ts_file.name] = ts_file

        # Fix imports in each file
        for filename, file_path in self.generated_files.items():
            if not str(file_path).endswith('.ts'): 
                continue
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # Pattern to match import statements
            import_pattern = r"from\s+['\"]([^'\"]+)['\"]"
            
            def replace_import(match):
                import_path = match.group(1)
                
                # Skip non-relative imports (npm packages, @nestjs/*, etc.)
                if not import_path.startswith('.'):
                    return match.group(0)
                
                # Extract the target filename from the import path
                # Handle cases like './rbac.guard', '../entities/log-entry.entity', etc.
                parts = import_path.split('/')
                target_name = parts[-1]  # Get the last part (filename without path)
                
                # Try to find the target file in our file map
                target_file = None
                
                # Try exact match first
                if target_name in file_map:
                    target_file = file_map[target_name]
                # Try with .ts extension
                elif f"{target_name}.ts" in file_map:
                    target_file = file_map[f"{target_name}.ts"]
                # Try searching by base name
                else:
                    for key, path in file_map.items():
                        if key.replace('.ts', '') == target_name or key == target_name:
                            target_file = path
                            break
                
                if target_file and target_file.exists():
                    try:
                        # Calculate the correct relative path
                        rel_path = os.path.relpath(target_file, file_path.parent)
                        
                        # Normalize path separators to forward slashes
                        rel_path = rel_path.replace('\\', '/')
                        
                        # Remove .ts extension
                        rel_path = rel_path.replace('.ts', '')
                        
                        # Ensure it starts with ./  or ../
                        if not rel_path.startswith('.'):
                            rel_path = './' + rel_path
                        
                        return f"from '{rel_path}'"
                    except (ValueError, OSError):
                        pass
                
                # If we couldn't find or fix the import, return original
                return match.group(0)
            
            # Replace all imports
            new_content = re.sub(import_pattern, replace_import, content)
            
            # Write back if changed
            if new_content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
