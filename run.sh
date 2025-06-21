#!/bin/bash

# Camera Emotions - Emotion Detection Launcher
# For Unix/Linux/macOS systems

echo ""
echo "============================================================"
echo "           CAMERA EMOTIONS - EMOTION DETECTION"
echo "============================================================"
echo ""
echo "Starting Emotion Detection Application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8 or higher"
    echo "On Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "On macOS: brew install python3"
    exit 1
fi

# Check if requirements are installed
echo "Checking dependencies..."
python3 -c "import cv2, numpy, tkinter, PIL" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        echo "Please run: pip3 install -r requirements.txt"
        exit 1
    fi
fi

# Make the script executable
chmod +x run.py

# Run the launcher
echo "Starting application..."
python3 run.py 