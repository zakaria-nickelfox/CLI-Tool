from typing import List
from pydantic import BaseModel, Field

class FileContent(BaseModel):
    path: str = Field(..., description="The relative path of the file including the filename (e.g., 'src/main.py')")
    content: str = Field(..., description="The full code content of the file")

class GeneratedProject(BaseModel):
    files: List[FileContent] = Field(..., description="A list of files to be created in the project")

from dataclasses import dataclass
import re

@dataclass
class ImportStatement:
    """Represents a TypeScript import statement"""
    raw_line: str
    module_path: str
    imported_items: List[str]
    is_relative: bool  # True if starts with ./ or ../
    is_default: bool


# Utility functions for parsing TypeScript imports

# Regex patterns for different import styles
NAMED_IMPORT_PATTERN = re.compile(r"import\s+\{([^}]+)\}\s+from\s+['\"]([^'\"]+)['\"]")
DEFAULT_IMPORT_PATTERN = re.compile(r"import\s+(\w+)\s+from\s+['\"]([^'\"]+)['\"]")
NAMESPACE_IMPORT_PATTERN = re.compile(r"import\s+\*\s+as\s+(\w+)\s+from\s+['\"]([^'\"]+)['\"]")
SIDE_EFFECT_IMPORT_PATTERN = re.compile(r"import\s+['\"]([^'\"]+)['\"]")


def parse_typescript_import(line: str) -> ImportStatement:
    """
    Parse a TypeScript import statement into an ImportStatement object.
    
    Args:
        line: A single line containing an import statement
        
    Returns:
        ImportStatement object with parsed information
    """
    line = line.strip()
    
    # Try named import: import { A, B } from 'module'
    match = NAMED_IMPORT_PATTERN.search(line)
    if match:
        items_str = match.group(1)
        module_path = match.group(2)
        imported_items = [item.strip() for item in items_str.split(',')]
        is_relative = module_path.startswith('./') or module_path.startswith('../')
        return ImportStatement(
            raw_line=line,
            module_path=module_path,
            imported_items=imported_items,
            is_relative=is_relative,
            is_default=False
        )
    
    # Try default import: import Something from 'module'
    match = DEFAULT_IMPORT_PATTERN.search(line)
    if match:
        default_import = match.group(1)
        module_path = match.group(2)
        is_relative = module_path.startswith('./') or module_path.startswith('../')
        return ImportStatement(
            raw_line=line,
            module_path=module_path,
            imported_items=[default_import],
            is_relative=is_relative,
            is_default=True
        )
    
    # Try namespace import: import * as Something from 'module'
    match = NAMESPACE_IMPORT_PATTERN.search(line)
    if match:
        namespace = match.group(1)
        module_path = match.group(2)
        is_relative = module_path.startswith('./') or module_path.startswith('../')
        return ImportStatement(
            raw_line=line,
            module_path=module_path,
            imported_items=[namespace],
            is_relative=is_relative,
            is_default=False
        )
    
    # Try side-effect import: import 'module'
    match = SIDE_EFFECT_IMPORT_PATTERN.search(line)
    if match:
        module_path = match.group(1)
        is_relative = module_path.startswith('./') or module_path.startswith('../')
        return ImportStatement(
            raw_line=line,
            module_path=module_path,
            imported_items=[],
            is_relative=is_relative,
            is_default=False
        )
    
    # If no pattern matches, return a basic ImportStatement
    return ImportStatement(
        raw_line=line,
        module_path='',
        imported_items=[],
        is_relative=False,
        is_default=False
    )


def extract_imports_from_content(content: str) -> List[ImportStatement]:
    """
    Extract all import statements from TypeScript file content.
    
    Args:
        content: Full content of a TypeScript file
        
    Returns:
        List of ImportStatement objects
    """
    imports = []
    lines = content.split('\n')
    
    for line in lines:
        stripped = line.strip()
        # Check if line contains an import statement
        if stripped.startswith('import ') and ('from' in stripped or stripped.endswith("'")):
            import_stmt = parse_typescript_import(stripped)
            if import_stmt.module_path:  # Only add if we successfully parsed a module path
                imports.append(import_stmt)
    
    return imports
