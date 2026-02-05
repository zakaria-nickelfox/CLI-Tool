"""
Template parser for extracting code blocks and generating project files from boilerplate MD files.
"""
import re
from typing import Dict, List, Tuple
from pathlib import Path


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
                
                files[filename] = content
        return files
    
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
