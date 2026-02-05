"""
Quick test to verify GenInit installation
"""
import sys

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import typer
        print("✓ typer imported successfully")
    except ImportError:
        print("✗ typer not found - run: pip install typer")
        return False
    
    try:
        from InquirerPy import inquirer
        print("✓ InquirerPy imported successfully")
    except ImportError:
        print("✗ InquirerPy not found - run: pip install InquirerPy")
        return False
    
    try:
        from geninit.main import app
        print("✓ geninit.main imported successfully")
    except ImportError as e:
        print(f"✗ geninit.main import failed: {e}")
        return False
    
    try:
        from geninit.template_parser import BoilerplateParser
        print("✓ geninit.template_parser imported successfully")
    except ImportError as e:
        print(f"✗ geninit.template_parser import failed: {e}")
        return False
    
    try:
        from geninit.project_generator import ProjectGenerator
        print("✓ geninit.project_generator imported successfully")
    except ImportError as e:
        print(f"✗ geninit.project_generator import failed: {e}")
        return False
    
    return True

def test_command():
    """Test that the geninit command is available"""
    import subprocess
    try:
        result = subprocess.run(
            ["geninit", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ 'geninit' command is available")
            return True
        else:
            print("✗ 'geninit' command failed")
            return False
    except FileNotFoundError:
        print("✗ 'geninit' command not found")
        print("  Run: pip install -e .")
        return False
    except Exception as e:
        print(f"✗ Error testing command: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("  GenInit Installation Test")
    print("=" * 60)
    print()
    
    print("Testing imports...")
    imports_ok = test_imports()
    print()
    
    print("Testing command availability...")
    command_ok = test_command()
    print()
    
    print("=" * 60)
    if imports_ok and command_ok:
        print("  ✅ All tests passed! GenInit is ready to use.")
        print("  Run: geninit init")
    elif imports_ok:
        print("  ⚠️  Imports OK, but command not available.")
        print("  Run: pip install -e .")
    else:
        print("  ❌ Installation incomplete.")
        print("  Run: pip install -r requirements.txt")
        print("  Then: pip install -e .")
    print("=" * 60)
    
    sys.exit(0 if (imports_ok and command_ok) else 1)
