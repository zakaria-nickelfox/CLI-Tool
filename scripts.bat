@echo off
REM GenInit Script Runner - Similar to npm run

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="dev" goto dev
if "%1"=="start" goto start
if "%1"=="test" goto test
if "%1"=="clean" goto clean
goto unknown

:help
echo.
echo GenInit - Available Commands:
echo   scripts install    - Install the package in development mode
echo   scripts dev        - Install with development dependencies
echo   scripts start      - Run GenInit (after installation)
echo   scripts test       - Run tests
echo   scripts clean      - Clean build artifacts
echo.
echo Quick Start:
echo   1. scripts install
echo   2. scripts start
echo.
goto end

:install
echo Installing GenInit...
pip install -e .
goto end

:dev
echo Installing GenInit with dev dependencies...
pip install -e ".[dev]"
goto end

:start
echo Starting GenInit...
geninit
goto end

:test
echo Running tests...
pytest tests/ -v
goto end

:clean
echo Cleaning build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist geninit.egg-info rmdir /s /q geninit.egg-info
for /d /r . %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
del /s /q *.pyc 2>nul
echo Clean complete!
goto end

:unknown
echo Unknown command: %1
echo Run "scripts help" for available commands
goto end

:end
