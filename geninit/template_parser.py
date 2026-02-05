"""
Template parser for extracting code blocks and generating project files from boilerplate MD files.
"""
import re
from typing import Dict, List, Tuple, Set
from pathlib import Path
from geninit.models import ImportStatement, extract_imports_from_content


class BoilerplateParser:
    """Parse boilerplate markdown files to extract features and code."""
    
    # Mapping of code block languages to file extensions
    LANG_TO_EXT = {
        'python': '.py',
        'typescript': '.ts',
        'javascript': '.js',
        'bash': '.sh',
        'env': '.env',
        'json': '.json',
        'yaml': '.yml',
        'html': '.html',
        'css': '.css',
        'tsx': '.tsx',
        'jsx': '.jsx',
    }
    
    # Common filename patterns in code blocks
    FILENAME_PATTERNS = [
        r'#\s+(.+\.py)',  # Python: # filename.py
        r'//\s+(.+\.(?:ts|js|tsx|jsx))',  # JS/TS: // filename.ts
        r'<!--\s+(.+\.html)\s+-->',  # HTML: <!-- filename.html -->
    ]
    
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        with open(filepath, 'r', encoding='utf-8') as f:
            self.content = f.read()
        
        self.features = {}
        self._parse()
    
    def _parse(self):
        """Parse the markdown file to extract features and their code blocks."""
        lines = self.content.split('\n')
        current_feature = None
        current_section = None
        code_blocks = []
        
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Detect main feature headers (## 1. Feature Name or ## Feature Name)
            if line.startswith('## ') and not line.startswith('###'):
                # Save previous feature
                if current_feature and code_blocks:
                    self.features[current_feature] = {
                        'code_blocks': code_blocks,
                        'section': current_section
                    }
                
                # Extract feature name
                feature_match = re.match(r'##\s+(?:\d+\.\s+)?(.+)', line)
                if feature_match:
                    current_feature = feature_match.group(1).strip()
                    current_section = current_feature
                    code_blocks = []
            
            # Detect code blocks
            if line.startswith('```'):
                lang = line[3:].strip() or 'text'
                code_lines = []
                i += 1
                
                # Collect code block content
                while i < len(lines) and not lines[i].startswith('```'):
                    code_lines.append(lines[i])
                    i += 1
                
                if code_lines and current_feature:
                    code_blocks.append({
                        'language': lang,
                        'code': '\n'.join(code_lines),
                        'raw_lines': code_lines
                    })
            
            i += 1
        
        # Save last feature
        if current_feature and code_blocks:
            self.features[current_feature] = {
                'code_blocks': code_blocks,
                'section': current_section
            }
    
    def get_feature_names(self) -> List[str]:
        """Get list of all feature names."""
        return list(self.features.keys())
    
    def extract_filename_from_code(self, code: str, language: str) -> str:
        """Try to extract filename from code comments."""
        lines = code.split('\n')
        
        # Check first few lines for filename patterns
        for line in lines[:5]:
            for pattern in self.FILENAME_PATTERNS:
                match = re.search(pattern, line)
                if match:
                    return match.group(1)
        
        return None
    
    def infer_filename(self, feature_name: str, language: str, code: str = "", index: int = 0) -> str:
        """Infer filename based on feature name and language."""
        # Clean feature name
        clean_name = feature_name.lower()
        clean_name = re.sub(r'[^\w\s-]', '', clean_name)
        clean_name = re.sub(r'[-\s]+', '-', clean_name).strip('-')
        
        # Get file extension
        ext = self.LANG_TO_EXT.get(language, '.txt')
        is_ts = language in ['typescript', 'ts', 'tsx', 'jsx']
        separator = '.' if is_ts else '_'

        # Content-based detection for NestJS/TS
        if is_ts and code:
            def to_kebab(name):
                return re.sub(r'(?<!^)(?=[A-Z])', '-', name).lower()

            # Check for RBAC guard file FIRST (contains multiple guards and enums)
            # This must be checked before individual enum/guard checks
            if ('export enum Role' in code and 'export enum Permission' in code and 
                'RolesGuard' in code and 'PermissionsGuard' in code):
                return "rbac.guard.ts"
            
            # Check for LogEntry entity (contains both enum and entity)
            if 'export enum LogLevel' in code and 'export class LogEntry' in code:
                return "log-entry.entity.ts"

            # Check for enum
            if 'export enum' in code:
                match = re.search(r'export\s+enum\s+(\w+)', code)
                if match:
                    base = to_kebab(match.group(1))
                    return f"{base}.enum.ts"
            
            # Check for decorator
            if 'createParamDecorator' in code or 'SetMetadata' in code:
                match = re.search(r'export\s+const\s+(\w+)\s*=\s*createParamDecorator', code)
                if match:
                    base = to_kebab(match.group(1))
                    return f"{base}.decorator.ts"
            
            # Check for DTO
            if 'export class' in code and ('Dto' in code or 'DTO' in code):
                match = re.search(r'export\s+class\s+(\w+)', code)
                if match:
                    base = to_kebab(match.group(1))
                    return f"{base}.dto.ts"
            
            # Check for interface
            if 'export interface' in code:
                match = re.search(r'export\s+interface\s+(\w+)', code)
                if match:
                    base = to_kebab(match.group(1))
                    return f"{base}.interface.ts"

            if '@Module' in code:
                 match = re.search(r'class\s+(\w+)Module', code)
                 base = to_kebab(match.group(1)) if match else clean_name.replace('-system', '').replace('-service', '')
                 return f"{base}.module.ts"
            elif '@Controller' in code:
                 match = re.search(r'class\s+(\w+)Controller', code)
                 base = to_kebab(match.group(1)) if match else clean_name.replace('-system', '').replace('-service', '')
                 return f"{base}.controller.ts"
            elif '@Entity' in code:
                 match = re.search(r'class\s+(\w+)', code)
                 base = to_kebab(match.group(1)) if match else clean_name
                 return f"{base}.entity.ts"
            elif '@Injectable' in code:
                 if 'implements CanActivate' in code or 'Guard' in code:
                      match = re.search(r'class\s+(\w+)Guard', code)
                      base = to_kebab(match.group(1)) if match else 'rbac'
                      return f"{base}.guard.ts"
                 if 'implements ExceptionFilter' in code or 'Filter' in code:
                      return "global-exception.filter.ts"
                 if 'LoggerService' in code or 'winston' in code:
                      return "custom-logger.service.ts"
                 # Default service
                 match = re.search(r'class\s+(\w+)Service', code)
                 base = to_kebab(match.group(1)) if match else clean_name.replace('-system', '').replace('-service', '')
                 return f"{base}.service.ts"

        # Fallback to feature name logic
        if 'service' in clean_name or 'mail' in clean_name:
            base = clean_name.replace('_', '-').replace('service', '').strip('-')
            return f"{base}.service{ext}" if is_ts else f"{base}_service{ext}"
        elif 'model' in clean_name or 'entity' in clean_name:
            base = clean_name.replace('model', '').replace('entity', '').strip('-_')
            return f"{base}.entity{ext}" if is_ts else f"{base}_model{ext}"
        elif 'controller' in clean_name:
            base = clean_name.replace('controller', '').strip('-_')
            return f"{base}.controller{ext}"
        elif 'guard' in clean_name or 'rbac' in clean_name:
            return f"rbac.guard{ext}" if is_ts else f"rbac{ext}"
        elif 'error' in clean_name or 'exception' in clean_name:
            return f"global-exception.filter{ext}" if is_ts else f"error_handling{ext}"
        elif 'log' in clean_name:
            return f"custom-logger.service{ext}" if is_ts else f"logging_system{ext}"
        elif 'upload' in clean_name or 'file' in clean_name:
            return f"file-upload.service{ext}" if is_ts else f"file_upload_service{ext}"
        elif 'notification' in clean_name:
            if 'model' in clean_name or index == 0:
                return f"notification.entity{ext}" if is_ts else f"notification_models{ext}"
            else:
                return f"notification.service{ext}" if is_ts else f"notification_service{ext}"
        else:
            suffix = f"{separator}{index}" if index > 0 else ""
            return f"{clean_name}{suffix}{ext}"
    
    def _fix_nestjs_imports(self, code: str) -> str:
        """Add missing NestJS imports if detected."""
        missing = []
        # Common decorators and symbols from @nestjs/common
        symbols = ['Module', 'Controller', 'Injectable', 'Get', 'Post', 'Put', 'Delete', 'Patch', 'Param', 'Body', 'Query', 'UseGuards', 'UseInterceptors', 'UploadedFile', 'UploadedFiles']
        
        for sym in symbols:
            # Check if symbol is used (e.g. @Module or implements Module?)
            # Naive check: @Symbol or Symbol
            if (f'@{sym}' in code or f'implements {sym}' in code) and not re.search(rf'import\s+{{[^}}]*\b{sym}\b[^}}]*}}\s+from', code):
                missing.append(sym)
        
        if missing:
             # Check if @nestjs/common already imported
             if "from '@nestjs/common'" in code or 'from "@nestjs/common"' in code:
                 # It's hard to inject into existing import without parsing. 
                 # We'll just add a new line. TS allows multiple imports from same module.
                 code = f"import {{ {', '.join(missing)} }} from '@nestjs/common';\n" + code
             else:
                 code = f"import {{ {', '.join(missing)} }} from '@nestjs/common';\n" + code
        
        # Fix main.ts - ensure bootstrap() is called
        if 'async function bootstrap()' in code and 'bootstrap()' not in code.split('async function bootstrap()')[1]:
            code = code.rstrip() + '\nbootstrap();\n'
        
        return code

    def get_files_for_features(self, selected_features: List[str]) -> Dict[str, str]:
        files = {}
        for feature in selected_features:
            if feature not in self.features: continue
            
            feature_data = self.features[feature]
            code_blocks = feature_data['code_blocks']
            
            for idx, block in enumerate(code_blocks):
                lang = block['language']
                code = block['code']
                if lang in ['bash', 'env', 'text', '']: continue
                
                filename = self.extract_filename_from_code(code, lang)
                if not filename:
                    filename = self.infer_filename(feature, lang, code, idx)
                
                # Clean up code
                code_lines = code.split('\n')
                cleaned_lines = []
                for line in code_lines:
                    if any(re.match(pattern, line) for pattern in self.FILENAME_PATTERNS): continue
                    cleaned_lines.append(line)
                
                content = '\n'.join(cleaned_lines)
                
                # Fix imports for NestJS
                if lang in ['typescript', 'ts']:
                    content = self._fix_nestjs_imports(content)
                    content = self.fix_typeorm_imports(content)
                
                files[filename] = content
        return files
    
    def fix_typeorm_imports(self, code: str) -> str:
        """Replace @nestjs/typeorm decorator imports with typeorm package."""
        # TypeORM decorators that should come from 'typeorm' not '@nestjs/typeorm'
        TYPEORM_DECORATORS = {
            'Entity', 'Column', 'PrimaryGeneratedColumn', 
            'CreateDateColumn', 'UpdateDateColumn',
            'ManyToOne', 'OneToMany', 'ManyToMany', 'JoinColumn', 'JoinTable',
            'PrimaryColumn', 'Index', 'Unique', 'Check', 'Exclusion',
            'Generated', 'VersionColumn', 'ObjectIdColumn', 'BeforeInsert',
            'AfterInsert', 'BeforeUpdate', 'AfterUpdate', 'BeforeRemove',
            'AfterRemove', 'AfterLoad', 'EventSubscriber', 'EntityRepository'
        }
        
        # Find all imports from @nestjs/typeorm
        import_pattern = r"import\s+{([^}]+)}\s+from\s+['\"]@nestjs/typeorm['\"]"
        
        def replace_import(match):
            imported_items = [item.strip() for item in match.group(1).split(',')]
            
            # Separate TypeORM decorators from NestJS-specific imports
            typeorm_items = []
            nestjs_items = []
            
            for item in imported_items:
                # Remove 'type' keyword if present
                clean_item = item.replace('type ', '').strip()
                if clean_item in TYPEORM_DECORATORS:
                    typeorm_items.append(item)
                else:
                    nestjs_items.append(item)
            
            # Build replacement imports
            result = []
            if typeorm_items:
                result.append(f"import {{ {', '.join(typeorm_items)} }} from 'typeorm'")
            if nestjs_items:
                result.append(f"import {{ {', '.join(nestjs_items)} }} from '@nestjs/typeorm'")
            
            return ';\n'.join(result) if result else ''
        
        code = re.sub(import_pattern, replace_import, code)
        return code
    
    def get_env_template(self) -> str:
        """Extract environment variable template."""
        env_content = []
        
        for feature_data in self.features.values():
            for block in feature_data['code_blocks']:
                if block['language'] == 'env':
                    env_content.append(block['code'])
        
        return '\n\n'.join(env_content) if env_content else ""
    
    def get_dependencies(self) -> Dict[str, List[str]]:
        """Extract dependencies from bash/npm install commands."""
        deps = {
            'npm': [],
            'pip': [],
            'npm_dev': []
        }
        
        for feature_data in self.features.values():
            for block in feature_data['code_blocks']:
                if block['language'] == 'bash':
                    code = block['code']
                    
                    # Extract npm dependencies
                    npm_match = re.findall(r'npm install\s+([^\n]+)', code)
                    for match in npm_match:
                        if '-D' in match or '--save-dev' in match:
                            packages = match.replace('-D', '').replace('--save-dev', '').strip().split()
                            deps['npm_dev'].extend(packages)
                        else:
                            deps['npm'].extend(match.strip().split())
                    
                    # Extract pip dependencies
                    pip_match = re.findall(r'pip install\s+([^\n]+)', code)
                    for match in pip_match:
                        # Split by space and filter out flags/options
                        args = match.strip().split()
                        valid_packages = []
                        for arg in args:
                            arg = arg.strip()
                            # Skip flags, file paths, and common non-packages
                            if (arg.startswith('-') or 
                                arg.endswith('.txt') or 
                                arg.endswith('.md') or 
                                arg == '.' or 
                                '/' in arg or 
                                '\\' in arg):
                                continue
                            valid_packages.append(arg)
                        deps['pip'].extend(valid_packages)
        
        # Remove duplicates
        deps['npm'] = list(set(deps['npm']))
        deps['pip'] = list(set(deps['pip']))
        deps['npm_dev'] = list(set(deps['npm_dev']))
        
        return deps
    
    def extract_imports(self, code: str) -> List[ImportStatement]:
        """
        Extract all import statements from TypeScript code.
        
        Args:
            code: TypeScript file content
            
        Returns:
            List of ImportStatement objects
        """
        return extract_imports_from_content(code)
    
    def find_referenced_files(self, selected_features: List[str]) -> Set[str]:
        """
        Find all files referenced by relative imports in selected features.
        
        Args:
            selected_features: List of feature names to analyze
            
        Returns:
            Set of unique relative file paths referenced in imports
        """
        referenced_files = set()
        
        # Get all code blocks for selected features
        for feature in selected_features:
            if feature not in self.features:
                continue
            
            feature_data = self.features[feature]
            code_blocks = feature_data['code_blocks']
            
            for block in code_blocks:
                lang = block['language']
                code = block['code']
                
                # Only analyze TypeScript/JavaScript files
                if lang not in ['typescript', 'ts', 'tsx', 'javascript', 'js', 'jsx']:
                    continue
                
                # Extract imports from this code block
                imports = self.extract_imports(code)
                
                # Collect relative imports
                for imp in imports:
                    if imp.is_relative and imp.module_path:
                        # Normalize the path (remove ./ and ../)
                        path = imp.module_path
                        # Add common extensions if not present
                        if not any(path.endswith(ext) for ext in ['.ts', '.js', '.tsx', '.jsx']):
                            # Try with .ts extension (most common for NestJS)
                            referenced_files.add(f"{path}.ts")
                        else:
                            referenced_files.add(path)
        
        return referenced_files
    
    def extract_file_by_path(self, file_path: str) -> str:
        """
        Extract a specific file from the boilerplate by searching for its path.
        
        Args:
            file_path: The relative path to search for (e.g., './rbac/rbac.guard')
            
        Returns:
            File content if found, empty string otherwise
        """
        # Normalize the path - remove leading ./ and ../
        normalized_path = file_path.replace('./', '').replace('../', '')
        
        # Extract just the filename
        filename = Path(normalized_path).name
        
        # Search through all features for a code block that might be this file
        for feature_name, feature_data in self.features.items():
            code_blocks = feature_data['code_blocks']
            
            for block in code_blocks:
                lang = block['language']
                code = block['code']
                
                # Skip non-code blocks
                if lang in ['bash', 'env', 'text', '']:
                    continue
                
                # Check if this code block matches the file we're looking for
                # Method 1: Check for explicit filename in comments
                extracted_filename = self.extract_filename_from_code(code, lang)
                if extracted_filename and extracted_filename == filename:
                    return code
                
                # Method 2: Infer filename and check if it matches
                inferred_filename = self.infer_filename(feature_name, lang, code, 0)
                if inferred_filename == filename:
                    return code
                
                # Method 3: Check if the feature name or code content suggests this file
                # For example, if looking for 'rbac.guard.ts', check features with 'rbac' or 'guard'
                if filename.replace('.ts', '').replace('.js', '').replace('-', '').replace('.', '') in feature_name.lower().replace(' ', '').replace('-', ''):
                    # Additional validation: check if code contains expected patterns
                    if 'guard' in filename.lower() and ('Guard' in code or 'CanActivate' in code):
                        return code
                    if 'decorator' in filename.lower() and ('createParamDecorator' in code or 'SetMetadata' in code):
                        return code
                    if 'enum' in filename.lower() and 'export enum' in code:
                        return code
                    if 'entity' in filename.lower() and '@Entity' in code:
                        return code
        
        return ""
