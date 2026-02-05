import os
from pathlib import Path
from .models import GeneratedProject

def create_project_files(project: GeneratedProject, base_path: str = "."):
    for file_info in project.files:
        path = Path(base_path) / file_info.path
        
        # Create directories if they don't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the file content
        with open(path, "w", encoding="utf-8") as f:
            f.write(file_info.content)
            
        print(f"Created: {file_info.path}")
    
    # Add a standalone run_local.bat for single-click execution on Windows
    run_bat_path = Path(base_path) / "run_local.bat"
    bat_content = """@echo off
setlocal
echo ===================================================
echo   Local Run Script for Django Project
echo ===================================================
cd /d "%~dp0"
if not exist venv (
    echo [1/5] Creating virtual environment...
    python -m venv venv
)
echo [2/5] Activating virtual environment...
call venv\\Scripts\\activate
echo [3/5] Installing dependencies...
pip install -r requirements.txt
echo [4/5] Configuring environment for SQLite...
if exist .env (
    powershell -Command "(gc .env) -replace 'DATABASE_URL=postgres://user:password@db:5432/mydatabase', 'DATABASE_URL=sqlite:///db.sqlite3' | Out-File -encoding ASCII .env"
)
echo [5/5] Running migrations...
python manage.py migrate
echo ===================================================
echo   SETUP COMPLETE! Starting the server...
echo   App URL: http://127.0.0.1:8000
echo ===================================================
python manage.py runserver
pause
"""
    with open(run_bat_path, "w", encoding="utf-8") as f:
        f.write(bat_content)
    print(f"Created: run_local.bat (Local execution script)")
