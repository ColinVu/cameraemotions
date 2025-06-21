@echo off
title Camera Emotions - Emotion Detection
echo.
echo ============================================================
echo           CAMERA EMOTIONS - EMOTION DETECTION
echo ============================================================
echo.
echo Starting Emotion Detection Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo.
    echo Please install Python 3.8 or higher from https://python.org
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    echo Alternative: Install Python from Microsoft Store (Windows 10/11)
    pause
    exit /b 1
)

echo Python found! Checking dependencies...

REM Try different pip commands
echo Checking pip availability...

REM First try: python -m pip (most reliable)
python -m pip --version >nul 2>&1
if not errorlevel 1 (
    echo Using: python -m pip
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies with python -m pip
        goto :pip_error
    )
    goto :deps_ok
)

REM Second try: pip command
pip --version >nul 2>&1
if not errorlevel 1 (
    echo Using: pip
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies with pip
        goto :pip_error
    )
    goto :deps_ok
)

REM Third try: pip3 command
pip3 --version >nul 2>&1
if not errorlevel 1 (
    echo Using: pip3
    echo Installing dependencies...
    pip3 install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies with pip3
        goto :pip_error
    )
    goto :deps_ok
)

:pip_error
echo.
echo ERROR: Could not find pip or install dependencies
echo.
echo Please try one of these solutions:
echo 1. Run: python -m ensurepip --upgrade
echo 2. Install pip manually: https://pip.pypa.io/en/stable/installation/
echo 3. Use the Python installer from python.org and check "Add Python to PATH"
echo.
echo You can also try running the installation test:
echo python check_python.py
echo.
pause
exit /b 1

:deps_ok
echo.
echo Dependencies installed successfully!
echo.

REM Run the launcher
echo Starting application...
python run.py

pause 