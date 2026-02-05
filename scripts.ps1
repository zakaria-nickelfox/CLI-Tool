# GenInit Script Runner - PowerShell Version
# Similar to npm run commands

param(
    [Parameter(Position=0)]
    [string]$Command = "help"
)

function Show-Help {
    Write-Host ""
    Write-Host "GenInit - Available Commands:" -ForegroundColor Cyan
    Write-Host "  .\scripts install    - Install the package in development mode" -ForegroundColor White
    Write-Host "  .\scripts dev        - Install with development dependencies" -ForegroundColor White
    Write-Host "  .\scripts start      - Run GenInit (after installation)" -ForegroundColor White
    Write-Host "  .\scripts test       - Run tests" -ForegroundColor White
    Write-Host "  .\scripts clean      - Clean build artifacts" -ForegroundColor White
    Write-Host ""
    Write-Host "Quick Start:" -ForegroundColor Yellow
    Write-Host "  1. .\scripts install" -ForegroundColor White
    Write-Host "  2. .\scripts start" -ForegroundColor White
    Write-Host ""
}

function Install-Package {
    Write-Host "Installing GenInit..." -ForegroundColor Cyan
    python -m pip install -e .
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Installation complete!" -ForegroundColor Green
    } else {
        Write-Host "Installation failed" -ForegroundColor Red
    }
}

function Install-Dev {
    Write-Host "Installing GenInit with dev dependencies..." -ForegroundColor Cyan
    python -m pip install -e ".[dev]"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Installation complete!" -ForegroundColor Green
    } else {
        Write-Host "Installation failed" -ForegroundColor Red
    }
}

function Start-GenInit {
    Write-Host "Starting GenInit..." -ForegroundColor Cyan
    geninit
}

function Run-Tests {
    Write-Host "Running tests..." -ForegroundColor Cyan
    pytest tests/ -v
}

function Clean-Build {
    Write-Host "Cleaning build artifacts..." -ForegroundColor Cyan
    
    if (Test-Path "build") { 
        Remove-Item -Recurse -Force "build" 
    }
    if (Test-Path "dist") { 
        Remove-Item -Recurse -Force "dist" 
    }
    
    Get-ChildItem -Path . -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
    Get-ChildItem -Path . -Recurse -File -Filter "*.pyc" -ErrorAction SilentlyContinue | Remove-Item -Force
    Get-ChildItem -Path . -Filter "*.egg-info" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force
    
    Write-Host "Clean complete!" -ForegroundColor Green
}

# Main command router
switch ($Command.ToLower()) {
    "help" { 
        Show-Help 
    }
    "install" { 
        Install-Package 
    }
    "dev" { 
        Install-Dev 
    }
    "start" { 
        Start-GenInit 
    }
    "test" { 
        Run-Tests 
    }
    "clean" { 
        Clean-Build 
    }
    default {
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Write-Host "Run '.\scripts help' for available commands" -ForegroundColor Yellow
    }
}
