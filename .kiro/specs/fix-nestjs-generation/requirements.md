# Requirements Document

## Introduction

The GenInit platform generates NestJS projects from boilerplate templates, but generated projects have compilation errors due to missing files, broken imports, and incomplete dependency extraction. This feature will fix the project generation to produce working, error-free NestJS projects.

## Glossary

- **GenInit**: The AI-powered project scaffolding tool
- **Boilerplate_Parser**: Component that extracts features from markdown boilerplate files
- **Project_Generator**: Component that creates project structure and files
- **Feature_File**: A code file extracted from a feature section in the boilerplate
- **Supporting_File**: Files referenced by feature files but not explicitly in boilerplate (DTOs, decorators, enums)
- **Import_Path**: Relative path used in TypeScript import statements

## Requirements

### Requirement 1: Extract All Referenced Files

**User Story:** As a developer, I want all files referenced in imports to be generated, so that my project compiles without missing module errors.

#### Acceptance Criteria

1. WHEN the Boilerplate_Parser extracts feature code, THE System SHALL identify all import statements in the code
2. WHEN an import references a local file (starts with './' or '../'), THE System SHALL extract that file from the boilerplate if it exists
3. WHEN a supporting file (DTO, decorator, enum, interface) is referenced, THE System SHALL generate it from the boilerplate
4. WHEN multiple features reference the same supporting file, THE System SHALL generate it only once

### Requirement 2: Fix TypeORM Decorator Imports

**User Story:** As a developer, I want TypeORM decorators to be imported correctly, so that entity files compile without errors.

#### Acceptance Criteria

1. WHEN generating entity files, THE System SHALL import decorators from 'typeorm' package
2. WHEN the boilerplate uses '@nestjs/typeorm' for decorators, THE System SHALL replace it with 'typeorm'
3. THE System SHALL ensure Entity, Column, PrimaryGeneratedColumn, CreateDateColumn, UpdateDateColumn, ManyToOne, OneToMany, ManyToMany decorators are imported from 'typeorm'

### Requirement 3: Generate Missing Supporting Files

**User Story:** As a developer, I want all supporting files (decorators, DTOs, enums) to be generated, so that imports resolve correctly.

#### Acceptance Criteria

1. WHEN a feature references a decorator file, THE System SHALL extract and generate the decorator file
2. WHEN a feature references a DTO file, THE System SHALL extract and generate the DTO file
3. WHEN a feature references an enum file, THE System SHALL extract and generate the enum file
4. WHEN a feature references an interface file, THE System SHALL extract and generate the interface file

### Requirement 4: Fix Import Path Resolution

**User Story:** As a developer, I want import paths to be correct relative to file locations, so that TypeScript can resolve all modules.

#### Acceptance Criteria

1. WHEN files are placed in different directories, THE System SHALL update import paths to reflect actual file locations
2. WHEN calculating relative paths, THE System SHALL use correct path separators for the target platform
3. WHEN an import cannot be resolved, THE System SHALL log a warning but continue generation
4. THE System SHALL handle both './' and '../' style imports correctly

### Requirement 5: Extract Complete Dependencies

**User Story:** As a developer, I want all npm dependencies to be included in package.json, so that npm install works without errors.

#### Acceptance Criteria

1. WHEN parsing boilerplate features, THE System SHALL extract all npm install commands
2. WHEN generating package.json, THE System SHALL include all extracted dependencies
3. THE System SHALL separate dependencies and devDependencies correctly
4. THE System SHALL include TypeORM in dependencies when entity files are generated

### Requirement 6: Handle Missing bootstrap() Call

**User Story:** As a developer, I want main.ts to have a complete bootstrap function, so that the application starts correctly.

#### Acceptance Criteria

1. WHEN generating main.ts, THE System SHALL include the bootstrap() function call
2. THE System SHALL ensure bootstrap() is invoked at the end of main.ts
3. THE System SHALL handle async/await correctly in the bootstrap function

### Requirement 7: Validate Generated Projects

**User Story:** As a developer, I want generated projects to be validated before completion, so that I know they will compile.

#### Acceptance Criteria

1. WHEN project generation completes, THE System SHALL check for common import errors
2. WHEN missing files are detected, THE System SHALL report them to the user
3. THE System SHALL provide a summary of generated files and their locations
4. THE System SHALL warn about any unresolved imports
