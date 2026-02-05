import typer
from InquirerPy import inquirer
from pathlib import Path
from .template_parser import BoilerplateParser
from .project_generator import ProjectGenerator

app = typer.Typer(help="GenInit - Template-Based Project Scaffolding Tool")

# Map of available languages/frameworks to their boilerplate files
BOILERPLATE_MAP = {
    "Django (Python Backend)": "DJANGO_BOILERPLATE.md",
    "NestJS (Node.js Backend)": "NESTJS_BOILERPLATE.md",
    "React Native (Mobile App)": "REACT_NATIVE_BOILERPLATE.md",
    "React with Next.js (Web App)": "REACT_NEXT_BOILERPLATE.md",
}

@app.command(name="")
def init():
    """
    Initialize a new project by selecting language and features.
    """
    typer.echo("=" * 60)
    typer.echo("  Welcome to GenInit - Template-Based Project Generator")
    typer.echo("=" * 60)
    typer.echo()
    
    # Step 1: Select programming language/framework
    language_choice = inquirer.select(
        message="Select your programming language/framework:",
        choices=list(BOILERPLATE_MAP.keys()),
    ).execute()
    
    if not language_choice:
        typer.echo("No language selected. Exiting.")
        raise typer.Exit()
    
    typer.echo(f"\n✓ Selected: {language_choice}")
    
    # Step 2: Get project name
    project_name = inquirer.text(
        message="Enter your project name:",
        validate=lambda result: len(result.strip()) > 0 and ' ' not in result,
        invalid_message="Project name cannot be empty or contain spaces.",
    ).execute()
    
    if not project_name:
        typer.echo("Project name is required. Exiting.")
        raise typer.Exit()
    
    typer.echo(f"✓ Project name: {project_name}")
    
    # Step 3: Load boilerplate file
    boilerplate_file = BOILERPLATE_MAP[language_choice]
    files_dir = Path(__file__).parent.parent / "files"
    boilerplate_path = files_dir / boilerplate_file
    
    if not boilerplate_path.exists():
        typer.echo(f"❌ Error: Boilerplate file not found: {boilerplate_path}")
        raise typer.Exit(code=1)
    
    typer.echo(f"\n📖 Loading features from {boilerplate_file}...")
    
    try:
        parser = BoilerplateParser(str(boilerplate_path))
        feature_names = parser.get_feature_names()
        
        if not feature_names:
            typer.echo("❌ Error: No features found in boilerplate file.")
            raise typer.Exit(code=1)
        
        typer.echo(f"✓ Found {len(feature_names)} features")
        
        # Step 4: Select features
        selected_features = inquirer.checkbox(
            message="Select the features you want to include:",
            choices=feature_names,
            validate=lambda result: len(result) > 0,
            invalid_message="You must select at least one feature.",
        ).execute()
        
        if not selected_features:
            typer.echo("No features selected. Exiting.")
            raise typer.Exit()
        
        typer.echo(f"\n✓ Selected {len(selected_features)} features:")
        for feature in selected_features:
            typer.echo(f"  • {feature}")
        
        # Step 5: Generate project
        typer.echo(f"\n🚀 Generating project '{project_name}'...")
        
        generator = ProjectGenerator(language_choice, project_name)
        generator.generate(parser, selected_features)
        
        typer.echo("\n" + "=" * 60)
        typer.echo(f"  ✅ Project '{project_name}' created successfully!")
        typer.echo("=" * 60)
        typer.echo(f"\n📁 Location: {Path(project_name).absolute()}")
        typer.echo("\n📝 Next steps:")
        typer.echo(f"  1. cd {project_name}")
        
        if 'Django' in language_choice:
            typer.echo("  2. python -m venv venv")
            typer.echo("  3. venv\\Scripts\\activate  (Windows) or source venv/bin/activate (Linux/Mac)")
            typer.echo("  4. pip install -r requirements.txt")
            typer.echo("  5. python manage.py migrate")
            typer.echo("  6. python manage.py runserver")
        elif 'NestJS' in language_choice:
            typer.echo("  2. npm install")
            typer.echo("  3. npm run start:dev")
        elif 'React' in language_choice:
            typer.echo("  2. npm install")
            typer.echo("  3. npm run dev" if 'Next' in language_choice else "npm start")
        
        typer.echo("\n💡 Check the README.md file for more details!")
        typer.echo()
        
    except Exception as e:
        typer.echo(f"\n❌ An error occurred during generation: {e}")
        import traceback
        traceback.print_exc()
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
