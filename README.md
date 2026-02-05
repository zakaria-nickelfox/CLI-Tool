# GenInit

AI-powered project scaffolding tool.

## Installation

### Option 1: Development Installation (Recommended)

1. Clone the repository and navigate to the project directory

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

4. Install GenInit in development mode:
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

5. Set your Gemini API key:
   - Create a `.env` file in the project root:
     ```bash
     GEMINI_API_KEY="your-api-key"
     ```
   - *Alternatively*, set it as an environment variable:
     ```bash
     export GEMINI_API_KEY="your-api-key" # Unix
     set GEMINI_API_KEY=your-api-key      # Windows
     ```

### Option 2: Manual Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set your Gemini API key (same as above)

## Usage

### Quick Start (Recommended)

After installation, you can run GenInit using simple commands:

**Windows:**
```bash
# PowerShell (Recommended)
.\scripts start

# CMD
scripts start
```

**Linux/Mac (with make):**
```bash
make start
```

**Or directly (after installation):**
```bash
geninit init
```

### Alternative Methods

You can still use the traditional Python commands:
```bash
python -m geninit.main
```
Or:
```bash
python geninit/main.py
```

Choose from the interactive menu and let the AI build your project!

## Available Commands

### Windows
- `.\scripts install` (PowerShell) or `scripts install` (CMD) - Install GenInit in development mode
- `.\scripts start` (PowerShell) or `scripts start` (CMD) - Run GenInit
- `.\scripts test` (PowerShell) or `scripts test` (CMD) - Run tests
- `.\scripts clean` (PowerShell) or `scripts clean` (CMD) - Clean build artifacts
- `.\scripts help` (PowerShell) or `scripts help` (CMD) - Show all commands

### Linux/Mac
- `make install` - Install GenInit in development mode
- `make start` - Run GenInit
- `make test` - Run tests
- `make clean` - Clean build artifacts
- `make help` - Show all commands
