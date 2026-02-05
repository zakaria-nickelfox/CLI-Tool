# GenInit Quick Start Guide

## Installation & First Run

### Step 1: Install GenInit

Open your terminal in the project directory and run:

**Windows:**
```bash
# PowerShell (Recommended)
# Activate virtual environment (if not already active)
venv\Scripts\activate

# Install GenInit
.\scripts install
```

**CMD:**
```bash
# Activate virtual environment (if not already active)
venv\Scripts\activate

# Install GenInit
scripts install
```

**Linux/Mac:**
```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Install GenInit
make install
```

### Step 2: Run GenInit

**Windows PowerShell:**
```bash
.\scripts start
```

**Windows CMD:**
```bash
scripts start
```

**Linux/Mac:**
```bash
make start
```

**Or use the command directly:**
```bash
geninit init
```

## What Happens Next?

1. You'll see a welcome screen
2. Select your framework (Django, NestJS, React Native, or Next.js)
3. Enter your project name
4. Choose the features you want
5. GenInit will generate your project!

## Example Session

```
============================================================
  Welcome to GenInit - Template-Based Project Generator
============================================================

? Select your programming language/framework:
  > NestJS (Node.js Backend)
    Django (Python Backend)
    React Native (Mobile App)
    React with Next.js (Web App)

✓ Selected: NestJS (Node.js Backend)

? Enter your project name: my-awesome-api

✓ Project name: my-awesome-api

📖 Loading features from NESTJS_BOILERPLATE.md...
✓ Found 6 features

? Select the features you want to include:
  [x] Mail Service
  [x] Notification System
  [ ] RBAC (Role-Based Access Control)
  [x] File Upload Service
  [ ] Global Error Handling
  [ ] Logging System

🚀 Generating project 'my-awesome-api'...

============================================================
  ✅ Project 'my-awesome-api' created successfully!
============================================================

📁 Location: C:\Users\YourName\Desktop\my-awesome-api

📝 Next steps:
  1. cd my-awesome-api
  2. npm install
  3. npm run start:dev

💡 Check the README.md file for more details!
```

## All Available Commands

### Windows Commands

**PowerShell (Recommended):**

| Command | Description |
|---------|-------------|
| `.\scripts install` | Install GenInit in development mode |
| `.\scripts dev` | Install with development dependencies |
| `.\scripts start` | Run GenInit |
| `.\scripts test` | Run tests |
| `.\scripts clean` | Clean build artifacts |
| `.\scripts help` | Show all commands |

**CMD:**

| Command | Description |
|---------|-------------|
| `scripts install` | Install GenInit in development mode |
| `scripts dev` | Install with development dependencies |
| `scripts start` | Run GenInit |
| `scripts test` | Run tests |
| `scripts clean` | Clean build artifacts |
| `scripts help` | Show all commands |

### Linux/Mac Commands

| Command | Description |
|---------|-------------|
| `make install` | Install GenInit in development mode |
| `make dev` | Install with development dependencies |
| `make start` | Run GenInit |
| `make test` | Run tests |
| `make clean` | Clean build artifacts |
| `make help` | Show all commands |

## Troubleshooting

### Command not found: geninit

If you get "command not found" after installation:

1. Make sure your virtual environment is activated
2. Reinstall: `pip install -e .`
3. Try using the full path: `python -m geninit.main`

### Import errors

If you get import errors:

1. Make sure all dependencies are installed: `pip install -r requirements.txt`
2. Reinstall in development mode: `pip install -e .`

### Permission errors on Windows

If you get permission errors running scripts:

1. Run your terminal as Administrator, or
2. Use the Python commands directly: `python -m geninit.main`

## Next Steps

- Check out the [README.md](README.md) for detailed documentation
- Explore the generated projects
- Customize the boilerplate files in the `files/` directory
- Report issues or contribute on GitHub

Happy coding! 🚀
