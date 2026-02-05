# Design Document: Fix NestJS Project Generation

## Overview

This design addresses the core issues in GenInit's NestJS project generation by implementing comprehensive import analysis, file extraction, and path resolution. The solution enhances the existing `BoilerplateParser` and `ProjectGenerator` classes to extract all referenced files, fix TypeORM imports, and validate generated projects.

## Architecture

The fix follows a three-phase approach:

1. **Enhanced Parsing Phase**: Extend `BoilerplateParser` to analyze imports and extract all referenced files
2. **Generation Phase**: Improve `ProjectGenerator` to place files correctly and fix import paths
3. **Validation Phase**: Add post-generation validation to detect and report issues

### Component Interaction

```
Boilerplate MD File
        ↓
BoilerplateParser (Enhanced)
  - Extract features
  - Analyze imports
  - Extract supporting files
  - Fix TypeORM imports
        ↓
ProjectGenerator (Enhanced)
  - Create directory structure
  - Generate all files
  - Fix import paths
  - Add missing dependencies
        ↓
ProjectValidator (New)
  - Check for missing files
  - Validate imports
  - Report issues
        ↓
Generated Project
```

## Components and Interfaces

### 1. Enhanced BoilerplateParser

**New Methods:**

```python
class BoilerplateParser:
    def extract_imports(self, code: str) -> List[ImportStatement]:
        """Extract all import statements from TypeScript code."""
        pass
    
    def find_referenced_files(self, selected_features: List[str]) -> Set[str]:
        """Find all files referenced by imports in selected features."""
        pass
    
    def extract_file_by_path(self, import_path: str) -> Optional[Tuple[str, str]]:
        """Extract a specific file from boilerplate by its import path."""
        pass
    
    def fix_typeorm_imports(self, code: str) -> str:
        """Replace @nestjs/typeorm decorator imports with typeorm."""
        pass
```

**ImportStatement Data Structure:**

```python
@dataclass
class ImportStatement:
    raw_line: str
    module_path: str
    imported_items: List[str]
    is_relative: bool  # True if starts with ./ or ../
    is_default: bool
```

### 2. Enhanced ProjectGenerator

**New Methods:**

```python
class ProjectGenerator:
    def determine_file_directory(self, filename: str, content: str) -> Path:
        """Determine the correct directory for a file based on its type and content."""
        pass
    
    def fix_all_import_paths(self):
        """Fix import paths in all generated files after placement."""
        pass
    
    def add_missing_dependencies(self, generated_files: Dict[str, str]):
        """Add dependencies based on generated file types."""
        pass
```

### 3. New ProjectValidator Component

```python
class ProjectValidator:
    def __init__(self, project_path: Path, generated_files: Dict[str, Path]):
        self.project_path = project_path
        self.generated_files = generated_files
        self.issues = []
    
    def validate(self) -> ValidationResult:
        """Run all validation checks."""
        pass
    
    def check_missing_imports(self) -> List[str]:
        """Check for imports that reference non-existent files."""
        pass
    
    def check_typescript_syntax(self) -> List[str]:
        """Basic TypeScript syntax validation."""
        pass
    
    def generate_report(self) -> str:
        """Generate human-readable validation report."""
        pass
```

## Data Models

### File Placement Rules

```python
FILE_PLACEMENT_RULES = {
    'entity': 'src/entities',
    'dto': 'src/dtos',
    'decorator': 'src/decorators',
    'enum': 'src/enums',
    'interface': 'src/interfaces',
    'guard': 'src/guards',
    'filter': 'src/filters',
    'service': 'src/services',
    'controller': 'src/controllers',
    'module': 'src/modules',
}
```

### TypeORM Decorator Mapping

```python
TYPEORM_DECORATORS = {
    'Entity', 'Column', 'PrimaryGeneratedColumn', 
    'CreateDateColumn', 'UpdateDateColumn',
    'ManyToOne', 'OneToMany', 'ManyToMany', 'JoinColumn', 'JoinTable'
}
```

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Import Extraction Completeness
*For any* TypeScript code block in the boilerplate, all import statements (both relative and absolute) should be correctly identified and parsed into ImportStatement objects with accurate module paths and imported items.
**Validates: Requirements 1.1**

### Property 2: Referenced File Extraction
*For any* set of selected features, all files referenced by relative imports ('./' or '../') should be extracted from the boilerplate and included in the generated project, with each unique file generated exactly once even if referenced by multiple features.
**Validates: Requirements 1.2, 1.3, 1.4**

### Property 3: TypeORM Import Correction
*For any* generated TypeScript file containing TypeORM decorators (Entity, Column, PrimaryGeneratedColumn, CreateDateColumn, UpdateDateColumn, ManyToOne, OneToMany, ManyToMany), the import statement for these decorators should reference 'typeorm' package and not '@nestjs/typeorm'.
**Validates: Requirements 2.1, 2.2, 2.3**

### Property 4: Import Path Resolution
*For any* two generated files where one imports the other, the import path should be a valid relative path using forward slashes that correctly navigates from the importing file's directory to the imported file's location.
**Validates: Requirements 4.1, 4.2, 4.4**

### Property 5: Dependency Extraction
*For any* boilerplate with npm install commands, all package names (excluding flags like -D and --save-dev) should be extracted and categorized correctly as dependencies or devDependencies based on the presence of development flags.
**Validates: Requirements 5.1, 5.2, 5.3**

### Property 6: Conditional TypeORM Dependency
*For any* generated project, TypeORM should be included in package.json dependencies if and only if at least one entity file (containing @Entity decorator) was generated.
**Validates: Requirements 5.4**

### Property 7: Bootstrap Function Completeness
*For any* generated main.ts file, it should contain an async bootstrap function that uses await for NestFactory.create(), and the bootstrap() function should be invoked at the end of the file.
**Validates: Requirements 6.1, 6.2, 6.3**

### Property 8: Validation and Reporting
*For any* completed project generation, the system should perform validation checks for missing imports, generate a summary of all created files with their paths, and produce warnings for any unresolved imports without halting generation.
**Validates: Requirements 7.1, 7.2, 7.3, 7.4**

## Error Handling

### Import Resolution Errors
- **Missing File**: Log warning, continue generation, report in validation
- **Circular Imports**: Detect and warn, but allow (TypeScript handles this)
- **Invalid Path**: Log error, skip path fixing for that import

### File Extraction Errors
- **File Not Found in Boilerplate**: Log warning, add to missing files report
- **Duplicate Filenames**: Use first occurrence, log warning
- **Invalid Filename**: Sanitize and log transformation

### Validation Errors
- **Non-blocking**: All validation errors are warnings, not failures
- **Comprehensive Reporting**: Collect all issues before reporting
- **User Guidance**: Provide actionable suggestions for fixing issues

## Testing Strategy

### Unit Tests
- Test import regex patterns with various TypeScript import syntaxes
- Test file placement logic with different file types
- Test relative path calculation with various directory structures
- Test TypeORM import replacement with edge cases
- Test dependency extraction with complex npm install commands

### Property-Based Tests
Each correctness property will be implemented as a property-based test with minimum 100 iterations:

1. **Import Extraction Test**: Generate random TypeScript code with various import styles
2. **File Extraction Test**: Generate random feature sets with cross-references
3. **TypeORM Import Test**: Generate random entity files with various decorator combinations
4. **Path Resolution Test**: Generate random file placements and verify relative paths
5. **Dependency Test**: Generate random npm install commands with various flags
6. **TypeORM Conditional Test**: Generate projects with/without entities
7. **Bootstrap Test**: Verify main.ts structure across different configurations
8. **Validation Test**: Generate projects with intentional issues and verify reporting

### Integration Tests
- Generate complete NestJS projects and run `npm install` and `npm run build`
- Verify generated projects compile without TypeScript errors
- Test with actual boilerplate files from the repository

## Implementation Notes

### Import Analysis Algorithm

```python
def extract_imports(code: str) -> List[ImportStatement]:
    # Regex patterns for different import styles
    patterns = [
        r"import\s+{([^}]+)}\s+from\s+['\"]([^'\"]+)['\"]",  # Named imports
        r"import\s+(\w+)\s+from\s+['\"]([^'\"]+)['\"]",      # Default import
        r"import\s+\*\s+as\s+(\w+)\s+from\s+['\"]([^'\"]+)['\"]",  # Namespace import
    ]
    # Parse and return ImportStatement objects
```

### File Placement Logic

1. Analyze file content for decorators (@Entity, @Injectable, @Controller, etc.)
2. Check filename patterns (.entity.ts, .dto.ts, .guard.ts, etc.)
3. Apply placement rules based on file type
4. Create directory if it doesn't exist

### Path Resolution Algorithm

```python
def calculate_relative_path(from_file: Path, to_file: Path) -> str:
    # Use os.path.relpath to calculate relative path
    # Convert backslashes to forward slashes for TypeScript
    # Ensure path starts with ./ or ../
    # Remove .ts extension from import path
```

## Migration Path

1. **Phase 1**: Enhance BoilerplateParser with import analysis (backward compatible)
2. **Phase 2**: Update ProjectGenerator to use enhanced parser
3. **Phase 3**: Add ProjectValidator as optional post-generation step
4. **Phase 4**: Make validation mandatory and improve error messages

## Performance Considerations

- **Import Analysis**: O(n) where n is lines of code, acceptable for typical boilerplates
- **File Extraction**: Cache extracted files to avoid re-parsing boilerplate
- **Path Resolution**: O(f²) where f is number of files, acceptable for typical projects (<100 files)
- **Validation**: O(f) for file checks, O(i) for import checks where i is total imports

## Future Enhancements

- Support for barrel exports (index.ts files)
- Automatic generation of missing files based on imports
- Integration with TypeScript compiler API for better validation
- Support for path aliases (@app/, @shared/, etc.)
- Incremental generation (add features to existing projects)
