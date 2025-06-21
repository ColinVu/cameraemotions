#!/usr/bin/env python3
"""
Python and pip installation checker for Windows
"""

import sys
import subprocess
import os

def check_command(command):
    """Check if a command is available"""
    try:
        result = subprocess.run([command, '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return True, result.stdout.strip()
        else:
            return False, result.stderr.strip()
    except FileNotFoundError:
        return False, "Command not found"
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 50)
    print("    PYTHON & PIP INSTALLATION CHECKER")
    print("=" * 50)
    print()
    
    print("Python Version Check:")
    print("-" * 20)
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    print()
    
    print("Command Availability Check:")
    print("-" * 30)
    
    # Check python command
    python_ok, python_output = check_command("python")
    if python_ok:
        print(f"✓ python: {python_output}")
    else:
        print(f"✗ python: {python_output}")
    
    # Check python3 command
    python3_ok, python3_output = check_command("python3")
    if python3_ok:
        print(f"✓ python3: {python3_output}")
    else:
        print(f"✗ python3: {python3_output}")
    
    # Check pip command
    pip_ok, pip_output = check_command("pip")
    if pip_ok:
        print(f"✓ pip: {pip_output}")
    else:
        print(f"✗ pip: {pip_output}")
    
    # Check pip3 command
    pip3_ok, pip3_output = check_command("pip3")
    if pip3_ok:
        print(f"✓ pip3: {pip3_output}")
    else:
        print(f"✗ pip3: {pip3_output}")
    
    print()
    print("Python Module Check:")
    print("-" * 20)
    
    # Check if we can run pip as a module
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✓ python -m pip: {result.stdout.strip()}")
            module_pip_ok = True
        else:
            print(f"✗ python -m pip: {result.stderr.strip()}")
            module_pip_ok = False
    except Exception as e:
        print(f"✗ python -m pip: {e}")
        module_pip_ok = False
    
    print()
    print("RECOMMENDATIONS:")
    print("-" * 20)
    
    if python_ok and pip_ok:
        print("✓ Python and pip are working correctly!")
        print("  You can run: pip install -r requirements.txt")
    elif python_ok and module_pip_ok:
        print("✓ Python is working, pip works as a module!")
        print("  You can run: python -m pip install -r requirements.txt")
    elif python_ok:
        print("✓ Python is working, but pip needs to be installed.")
        print("  Try: python -m ensurepip --upgrade")
    else:
        print("✗ Python is not properly installed or not in PATH.")
        print("  Please install Python from https://python.org")
        print("  Make sure to check 'Add Python to PATH' during installation.")
    
    print()
    print("Alternative Installation Methods:")
    print("-" * 35)
    print("1. Use the batch file: Double-click run.bat")
    print("2. Use python -m pip: python -m pip install -r requirements.txt")
    print("3. Install Python from Microsoft Store (Windows 10/11)")
    
    print()
    input("Press Enter to exit...")

if __name__ == "__main__":
    main() 