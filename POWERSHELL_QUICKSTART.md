# PowerShell Quick Start for GenInit

## ⚡ The Issue You Encountered

When you ran `scripts install` in PowerShell, you got this error:
```
scripts : The term 'scripts' is not recognized...
```

## ✅ The Solution

In **PowerShell**, you need to use `.\` before the script name:

```powershell
.\scripts install    # ✅ Correct for PowerShell
```

In **CMD**, you don't need the `.\`:
```cmd
scripts install      # ✅ Correct for CMD
```

## 🚀 Quick Start (PowerShell)

### 1. Activate Virtual Environment
```powershell
venv\Scripts\activate
```

### 2. Install GenInit
```powershell
.\scripts install
```

### 3. Run GenInit
```powershell
.\scripts start
```

That's it! 🎉

## 📋 All PowerShell Commands

| Command | What it does |
|---------|--------------|
| `.\scripts install` | Install GenInit |
| `.\scripts dev` | Install with dev tools |
| `.\scripts start` | Run GenInit |
| `.\scripts test` | Run tests |
| `.\scripts clean` | Clean build files |
| `.\scripts help` | Show help |

## 🔄 Alternative: Direct Commands

After installation, you can also use:
```powershell
geninit init         # Run GenInit directly
geninit --help       # Show help
```

## 💡 Why the `.\` ?

PowerShell requires `.\` to run scripts in the current directory for security reasons. This tells PowerShell "run the script in THIS folder" rather than searching your PATH.

## 🎯 Quick Reference

### PowerShell vs CMD vs Linux

| Task | PowerShell | CMD | Linux/Mac |
|------|------------|-----|-----------|
| Install | `.\scripts install` | `scripts install` | `make install` |
| Run | `.\scripts start` | `scripts start` | `make start` |
| Test | `.\scripts test` | `scripts test` | `make test` |

## 🆘 Still Having Issues?

### Option 1: Use the full filename
```powershell
.\scripts.ps1 install
```

### Option 2: Use CMD instead
```cmd
scripts install
```

### Option 3: Run directly
```powershell
pip install -e .
geninit init
```

## ✨ What's New?

I created **two** script files for you:

1. **scripts.ps1** - PowerShell version (colorful output, better for PowerShell)
2. **scripts.bat** - CMD version (works in CMD and PowerShell with `.\`)

Both do the same thing, but `scripts.ps1` has nicer colors and formatting in PowerShell!

## 🎨 Try the PowerShell Version

For the best experience in PowerShell, use:
```powershell
.\scripts.ps1 install
.\scripts.ps1 start
```

Or just:
```powershell
.\scripts install    # This works too!
```

Happy coding! 🚀
