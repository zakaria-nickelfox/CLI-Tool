import typer
from InquirerPy import inquirer
import os
import json
import re
from pathlib import Path

app = typer.Typer(help="GenInit - Template-Based Project Scaffolding Tool")

# Map of available languages/frameworks to their boilerplate files
BOILERPLATE_MAP = {
    "Django (Python Backend)": "DJANGO_BOILERPLATE.md",
    "NestJS (Node.js Backend)": "NESTJS_BOILERPLATE.md",
    "React Native (Mobile App)": "REACT_NATIVE_BOILERPLATE.md",
    "React with Next.js (Web App)": "REACT_NEXT_BOILERPLATE.md",
}

def parse_boilerplate_file(filepath: str) -> dict:
    """
    Parse a boilerplate markdown file to extract features and their code.
    Returns a dictionary with feature names as keys and their code blocks as values.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    features = {}
    current_feature = None
    current_code_blocks = []
    
    lines = content.split('\n')
    in_code_block = False
    code_block_content = []
    code_block_lang = None
    
    for line in lines:
        # Detect feature headers (## 1. Feature Name or ## Feature Name)
        if line.startswith('## ') and not line.startswith('###'):
            # Save previous feature if exists
            if current_feature and current_code_blocks:
                features[current_feature] = current_code_blocks
            
            # Extract feature name
            feature_match = re.match(r'##\s+(?:\d+\.\s+)?(.+)', line)
            if feature_match:
                current_feature = feature_match.group(1).strip()
                current_code_blocks = []
        
        # Detect code blocks
        if line.startswith('```'):
            if not in_code_block:
                # Starting a code block
                in_code_block = True
                code_block_lang = line[3:].strip() or 'text'
                code_block_content = []
            else:
                # Ending a code block
                in_code_block = False
                if current_feature and code_block_content:
                    current_code_blocks.append({
                        'language': code_block_lang,
                        'code': '\n'.join(code_block_content)
                    })
                code_block_content = []
        elif in_code_block:
            code_block_content.append(line)
    
    # Save last feature
    if current_feature and current_code_blocks:
        features[current_feature] = current_code_blocks
    
    return features

def extract_file_from_code_block(code_block: dict) -> dict:
    """
    Extract filename and content from a code block.
    Returns dict with 'filename' and 'content' keys.
    """
    code = code_block['code']
    lines = code.split('\n')
    
    # Check for comment indicating filename
    filename = None
    content_start = 0
    
    # Look for filename in first few lines (e.g., # filename.py or // filename.js)
    for i, line in enumerate(lines[:5]):
        if line.strip().startswith('#') and any(ext in line for ext in ['.py', '.ts', '.js', '.tsx', '.jsx']):
            filename = line.strip().lstrip('#').strip()
            content_start = i + 1
            break
        elif line.strip().startswith('//') and any(ext in line for ext in ['.ts', '.js', '.tsx', '.jsx']):
            filename = line.strip().lstrip('//').strip()
            content_start = i + 1
            break
    
    content = '\n'.join(lines[content_start:])
    
    return {
        'filename': filename,
        'content': content,
        'language': code_block['language']
    }

@app.command()
def init():
    """
    Initialize a new project by selecting language and features.
    """
    typer.echo("Welcome to GenInit!")
    
    # Step 1: Select programming language/framework
    language_choice = inquirer.select(
        message="Select your programming language/framework:",
        choices=list(BOILERPLATE_MAP.keys()),
    ).execute()
    
    if not language_choice:
        typer.echo("No language selected. Exiting.")
        raise typer.Exit()
    
    # Step 2: Get project name
    project_name = inquirer.text(
        message="Enter your project name:",
        validate=lambda result: len(result.strip()) > 0,
        invalid_message="Project name cannot be empty.",
    ).execute()
    
    if not project_name:
        typer.echo("Project name is required. Exiting.")
        raise typer.Exit()
    
    # Step 3: Load boilerplate file
    boilerplate_file = BOILERPLATE_MAP[language_choice]
    files_dir = Path(__file__).parent.parent / "files"
    boilerplate_path = files_dir / boilerplate_file
    
    if not boilerplate_path.exists():
        typer.echo(f"Error: Boilerplate file not found: {boilerplate_path}")
        raise typer.Exit(code=1)
    
    typer.echo(f"Loading features from {boilerplate_file}...")
    features_dict = parse_boilerplate_file(str(boilerplate_path))
    
    if not features_dict:
        typer.echo("Error: No features found in boilerplate file.")
        raise typer.Exit(code=1)
    
    # Step 4: Select features
    feature_names = list(features_dict.keys())
    selected_features = inquirer.checkbox(
        message="Select the features you want to include:",
        choices=feature_names,
        validate=lambda result: len(result) > 0,
        invalid_message="You must select at least one feature.",
    ).execute()
    
    if not selected_features:
        typer.echo("No features selected. Exiting.")
        raise typer.Exit()
    
    typer.echo(f"Selected features: {', '.join(selected_features)}")
    
    # Step 5: Generate project structure
    typer.echo("Generating project files...")
    
    try:
        # Create project directory
        project_path = Path(project_name)
        project_path.mkdir(exist_ok=True)
        
        # Generate files for each selected feature
        for feature in selected_features:
            code_blocks = features_dict[feature]
            typer.echo(f"Creating files for: {feature}")
            
            for block in code_blocks:
                file_info = extract_file_from_code_block(block)
                
                if file_info['filename']:
                    # Create file with extracted content
                    file_path = project_path / file_info['filename']
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(file_info['content'])
                    
                    typer.echo(f"Created: {file_info['filename']}")
        
        typer.echo(f"\\nProject '{project_name}' initialized successfully!")
        typer.echo(f"Location: {project_path.absolute()}")
        
    except Exception as e:
        typer.echo(f"An error occurred during generation: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
