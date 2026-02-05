# NPM-Style Commands for GenInit

## Overview

Your GenInit platform now supports npm-style commands! Instead of typing `python -m geninit.main`, you can now use simple commands like `scripts start` (Windows) or `make start` (Linux/Mac).

## What Was Added

### 1. **setup.py** - Python Package Configuration
- Configures GenInit as an installable Python package
- Creates the `geninit` command-line tool
- Manages dependencies automatically

### 2. **pyproject.toml** - Modern Python Project Configuration
- Modern Python packaging standard (PEP 518)
- Defines project metadata and dependencies
- Supports development dependencies

### 3. **scripts.bat** - Windows Command Runner
- NPM-style script runner for Windows
- Simple commands like `scripts start`, `scripts install`
- Similar to `npm run` commands

### 4. **Makefile** - Linux/Mac Command Runner
- Traditional Unix-style commands
- Simple commands like `make start`, `make install`
- Works on Linux, Mac, and Windows (with make installed)

### 5. **test_installation.py** - Installation Verification
- Tests that GenInit is installed correctly
- Checks all imports and command availability
- Provides helpful error messages

### 6. **Documentation Files**
- **QUICKSTART.md** - Quick start guide with examples
- **SETUP_GUIDE.txt** - Simple text-based setup instructions
- **Updated README.md** - Complete documentation

## How to Use

### First Time Setup

1. **Activate your virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Install GenInit:**
   ```bash
   # PowerShell (Recommended)
   .\scripts install
   
   # CMD
   scripts install
   
   # Linux/Mac
   make install
   
   # Or manually
   pip install -e .
   ```

3. **Verify installation (optional):**
   ```bash
   python test_installation.py
   ```

### Running GenInit

Now you can use any of these methods:

**Method 1: Simple Commands (Recommended)**
```bash
# PowerShell
.\scripts start

# CMD
scripts start

# Linux/Mac
make start
```

**Method 2: Direct Command**
```bash
geninit init
```

**Method 3: Traditional Python (still works)**
```bash
python -m geninit.main
# or
python geninit/main.py
```

## Command Reference

### Windows Commands

**PowerShell (Recommended):**

| Command | What it does | NPM Equivalent |
|---------|--------------|----------------|
| `.\scripts install` | Install GenInit | `npm install` |
| `.\scripts dev` | Install with dev tools | `npm install --dev` |
| `.\scripts start` | Run GenInit | `npm run start` |
| `.\scripts test` | Run tests | `npm test` |
| `.\scripts clean` | Clean build files | `npm run clean` |
| `.\scripts help` | Show help | `npm run` |

**CMD (Alternative):**

| Command | What it does |
|---------|--------------|
| `scripts install` | Install GenInit |
| `scripts dev` | Install with dev tools |
| `scripts start` | Run GenInit |
| `scripts test` | Run tests |
| `scripts clean` | Clean build files |
| `scripts help` | Show help |

### Linux/Mac Commands (Makefile)

| Command | What it does | NPM Equivalent |
|---------|--------------|----------------|
| `make install` | Install GenInit | `npm install` |
| `make dev` | Install with dev tools | `npm install --dev` |
| `make start` | Run GenInit | `npm run start` |
| `make test` | Run tests | `npm test` |
| `make clean` | Clean build files | `npm run clean` |
| `make help` | Show help | `npm run` |

## Benefits

### Before (Old Way)
```bash
python -m geninit.main
```
- Long command to type
- Need to remember the module path
- Not intuitive for developers from other ecosystems

### After (New Way)
```bash
scripts start    # Windows
make start       # Linux/Mac
geninit init     # Direct command
```
- Short, memorable commands
- Similar to npm/yarn workflows
- Professional and intuitive

## Technical Details

### How It Works

1. **setup.py** registers `geninit` as a console script
2. When you run `pip install -e .`, it creates a `geninit` executable
3. The executable is added to your PATH (within the virtual environment)
4. You can now run `geninit` from anywhere (while venv is active)

### Entry Point

The entry point is defined in setup.py:
```python
entry_points={
    "console_scripts": [
        "geninit=geninit.main:app",
    ],
}
```

This tells Python to create a `geninit` command that runs the `app` object from `geninit.main`.

## Troubleshooting

### "geninit: command not found"

**Solution:**
1. Make sure your virtual environment is activated
2. Run: `pip install -e .`
3. If still not working, use: `python -m geninit.main`

### "No module named 'typer'"

**Solution:**
1. Install dependencies: `pip install -r requirements.txt`
2. Then install GenInit: `pip install -e .`

### "scripts: command not found" (Windows)

**Solution:**
1. Use full name: `scripts.bat install`
2. Or run directly: `pip install -e .`

### "make: command not found" (Windows)

**Solution:**
1. Use scripts.bat instead: `scripts install`
2. Or install make for Windows (optional)
3. Or run commands directly: `pip install -e .`

## Next Steps

1. **Install GenInit:**
   ```bash
   scripts install    # Windows
   make install       # Linux/Mac
   ```

2. **Test it:**
   ```bash
   python test_installation.py
   ```

3. **Run it:**
   ```bash
   scripts start      # Windows
   make start         # Linux/Mac
   geninit init       # Direct
   ```

4. **Start building projects!** 🚀

## Files Created

- ✅ `setup.py` - Package configuration
- ✅ `pyproject.toml` - Modern Python project config
- ✅ `scripts.bat` - Windows command runner
- ✅ `Makefile` - Linux/Mac command runner
- ✅ `test_installation.py` - Installation test
- ✅ `QUICKSTART.md` - Quick start guide
- ✅ `SETUP_GUIDE.txt` - Simple setup instructions
- ✅ `NPM_STYLE_COMMANDS.md` - This file
- ✅ Updated `README.md` - Complete documentation
- ✅ Updated `requirements.txt` - Added missing dependencies

## Summary

You now have a professional, npm-style command interface for your GenInit platform! Instead of typing long Python commands, you can use simple, memorable commands like `scripts start` or `make start`. This makes your tool more accessible and professional, especially for developers coming from JavaScript/Node.js backgrounds.

Enjoy your new workflow! 🎉
