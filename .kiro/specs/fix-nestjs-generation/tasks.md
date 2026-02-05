# Implementation Plan: Fix NestJS Project Generation

## Overview

This plan breaks down the implementation into discrete tasks that enhance the existing GenInit codebase to fix NestJS project generation issues. Each task builds incrementally on previous work, with validation checkpoints to ensure correctness.

## Tasks

- [-] 1. Create data models and utilities for import analysis
  - Create ImportStatement dataclass in geninit/models.py
  - Create utility functions for parsing TypeScript imports
  - Add regex patterns for different import styles (named, default, namespace)
  - _Requirements: 1.1_

- [ ] 1.1 Write property test for import extraction
  - **Property 1: Import Extraction Completeness**
  - **Validates: Requirements 1.1**

- [-] 2. Enhance BoilerplateParser with import analysis
  - [x] 2.1 Add extract_imports() method to BoilerplateParser
    - Implement regex-based import parsing
    - Return list of ImportStatement objects
    - Handle edge cases (multi-line imports, comments)
    - _Requirements: 1.1_

  - [x] 2.2 Add find_referenced_files() method
    - Analyze all imports in selected features
    - Identify relative imports (starting with ./ or ../)
    - Return set of unique referenced file paths
    - _Requirements: 1.2, 1.4_

  - [x] 2.3 Add extract_file_by_path() method
    - Search boilerplate for file matching import path
    - Extract file content from code blocks
    - Handle different file naming conventions
    - _Requirements: 1.2, 1.3_

  - [ ] 2.4 Write property test for referenced file extraction
    - **Property 2: Referenced File Extraction**
    - **Validates: Requirements 1.2, 1.3, 1.4**

- [-] 3. Implement TypeORM import fixing
  - [x] 3.1 Add fix_typeorm_imports() method to BoilerplateParser
    - Identify imports from '@nestjs/typeorm'
    - Check if imported items are TypeORM decorators
    - Replace package name with 'typeorm'
    - Preserve other @nestjs/typeorm imports (like TypeOrmModule)
    - _Requirements: 2.1, 2.2, 2.3_

  - [x] 3.2 Integrate TypeORM fixing into get_files_for_features()
    - Apply fix_typeorm_imports() to all TypeScript files
    - Ensure fixing happens before file generation
    - _Requirements: 2.1, 2.2, 2.3_

  - [ ] 3.3 Write property test for TypeORM import correction
    - **Property 3: TypeORM Import Correction**
    - **Validates: Requirements 2.1, 2.2, 2.3**

- [ ] 4. Checkpoint - Ensure parser enhancements work
  - Run existing tests to ensure no regressions
  - Test with sample boilerplate files
  - Verify import extraction and TypeORM fixing
  - Ask user if questions arise

- [ ] 5. Enhance ProjectGenerator with improved file placement
  - [ ] 5.1 Add determine_file_directory() method
    - Analyze file content for decorators and patterns
    - Apply FILE_PLACEMENT_RULES based on file type
    - Return appropriate directory path
    - _Requirements: 4.1_

  - [ ] 5.2 Update _create_feature_files() to use new placement logic
    - Replace existing heuristics with determine_file_directory()
    - Ensure all file types are handled correctly
    - Create directories as needed
    - _Requirements: 4.1_

  - [ ] 5.3 Add fix_all_import_paths() method
    - Iterate through all generated files
    - Parse imports in each file
    - Calculate correct relative paths based on actual file locations
    - Update import statements with corrected paths
    - _Requirements: 4.1, 4.2, 4.4_

  - [ ] 5.4 Write property test for import path resolution
    - **Property 4: Import Path Resolution**
    - **Validates: Requirements 4.1, 4.2, 4.4**

- [-] 6. Implement comprehensive file extraction
  - [x] 6.1 Update generate() method to extract all referenced files
    - Call find_referenced_files() after initial extraction
    - Extract each referenced file using extract_file_by_path()
    - Add extracted files to generation queue
    - Deduplicate files by path
    - _Requirements: 1.2, 1.3, 1.4_

  - [x] 6.2 Call fix_all_import_paths() after file placement
    - Ensure all files are placed before fixing paths
    - Fix paths for all generated files
    - _Requirements: 4.1, 4.2, 4.4_

- [ ] 7. Enhance dependency management
  - [ ] 7.1 Add add_missing_dependencies() method to ProjectGenerator
    - Scan generated files for entity decorators
    - Add 'typeorm' to dependencies if entities found
    - Add 'reflect-metadata' and 'rxjs' as base dependencies
    - _Requirements: 5.4_

  - [ ] 7.2 Update _create_nestjs_config() to call add_missing_dependencies()
    - Integrate dependency addition into package.json generation
    - Ensure no duplicate dependencies
    - _Requirements: 5.1, 5.2, 5.3, 5.4_

  - [ ] 7.3 Write property test for dependency extraction
    - **Property 5: Dependency Extraction**
    - **Validates: Requirements 5.1, 5.2, 5.3**

  - [ ] 7.4 Write property test for conditional TypeORM dependency
    - **Property 6: Conditional TypeORM Dependency**
    - **Validates: Requirements 5.4**

- [x] 8. Fix main.ts bootstrap function
  - [ ] 8.1 Create template for correct main.ts structure
    - Include async bootstrap function
    - Add NestFactory.create() with await
    - Add bootstrap() invocation at end
    - _Requirements: 6.1, 6.2, 6.3_

  - [ ] 8.2 Update NestJS project generation to use correct main.ts
    - Replace existing main.ts generation
    - Ensure bootstrap function is complete
    - _Requirements: 6.1, 6.2, 6.3_

  - [ ] 8.3 Write property test for bootstrap function completeness
    - **Property 7: Bootstrap Function Completeness**
    - **Validates: Requirements 6.1, 6.2, 6.3**

- [ ] 9. Checkpoint - Ensure generation improvements work
  - Generate a test NestJS project with multiple features
  - Verify all files are created in correct locations
  - Check that imports are resolved correctly
  - Ask user if questions arise

- [ ] 10. Create ProjectValidator component
  - [ ] 10.1 Create geninit/validator.py with ProjectValidator class
    - Add __init__ method to store project path and generated files
    - Create ValidationResult dataclass for results
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [ ] 10.2 Implement check_missing_imports() method
    - Parse all imports in generated files
    - Check if imported files exist in project
    - Return list of missing import paths
    - _Requirements: 7.1, 7.4_

  - [ ] 10.3 Implement generate_report() method
    - Create summary of all generated files
    - List any missing imports as warnings
    - Provide actionable suggestions
    - _Requirements: 7.2, 7.3, 7.4_

  - [ ] 10.4 Implement validate() method
    - Call all validation checks
    - Collect results into ValidationResult
    - Return comprehensive validation result
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [ ] 10.5 Write property test for validation and reporting
    - **Property 8: Validation and Reporting**
    - **Validates: Requirements 7.1, 7.2, 7.3, 7.4**

- [ ] 11. Integrate validation into project generation
  - [ ] 11.1 Update ProjectGenerator.generate() to run validation
    - Create ProjectValidator instance after generation
    - Run validation checks
    - Print validation report
    - _Requirements: 7.1, 7.2, 7.3, 7.4_

  - [ ] 11.2 Update CLI output to show validation results
    - Display file summary
    - Show warnings for any issues
    - Provide next steps based on validation
    - _Requirements: 7.2, 7.3_

- [ ] 12. Final integration and testing
  - [ ] 12.1 Test with actual NESTJS_BOILERPLATE.md
    - Generate project with all features
    - Run npm install
    - Run npm run build
    - Verify no TypeScript errors
    - _Requirements: All_

  - [ ] 12.2 Test with subset of features
    - Generate project with 2-3 features
    - Verify correct file extraction
    - Check import resolution
    - _Requirements: All_

  - [ ] 12.3 Write integration tests
    - Test complete generation workflow
    - Verify generated projects compile
    - Test with different feature combinations

- [ ] 13. Final checkpoint - Ensure all tests pass
  - Run all unit tests
  - Run all property-based tests
  - Run integration tests
  - Verify no regressions in Django/React generation
  - Ask user if questions arise

## Notes

- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Integration tests ensure the complete system works end-to-end
