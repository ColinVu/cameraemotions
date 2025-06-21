#!/usr/bin/env python3
"""
Installation Test Script
Tests if all required dependencies are properly installed
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✓ {package_name or module_name}")
        return True
    except ImportError:
        print(f"✗ {package_name or module_name} - NOT FOUND")
        return False

def main():
    """Test all required dependencies"""
    print("=" * 50)
    print("    CAMERA EMOTIONS - INSTALLATION TEST")
    print("=" * 50)
    print()
    
    print("Testing basic dependencies...")
    print("-" * 30)
    
    basic_deps = [
        ("cv2", "OpenCV"),
        ("numpy", "NumPy"),
        ("tkinter", "Tkinter"),
        ("PIL", "Pillow"),
    ]
    
    basic_ok = True
    for module, name in basic_deps:
        if not test_import(module, name):
            basic_ok = False
    
    print()
    print("Testing full version dependencies...")
    print("-" * 30)
    
    full_deps = [
        ("mediapipe", "MediaPipe"),
        ("deepface", "DeepFace"),
        ("tensorflow", "TensorFlow"),
    ]
    
    full_ok = True
    for module, name in full_deps:
        if not test_import(module, name):
            full_ok = False
    
    print()
    print("=" * 50)
    print("TEST RESULTS:")
    print("=" * 50)
    
    if basic_ok:
        print("✓ Basic dependencies: OK")
        print("  You can run the simple version of the emotion detector.")
    else:
        print("✗ Basic dependencies: FAILED")
        print("  Please install basic dependencies:")
        print("  pip install opencv-python numpy Pillow")
    
    if full_ok:
        print("✓ Full version dependencies: OK")
        print("  You can run the full version with DeepFace.")
    else:
        print("✗ Full version dependencies: FAILED")
        print("  Please install full version dependencies:")
        print("  pip install mediapipe deepface tensorflow")
    
    print()
    print("RECOMMENDATIONS:")
    print("-" * 20)
    
    if basic_ok and full_ok:
        print("✓ All dependencies installed successfully!")
        print("  You can run either version of the emotion detector.")
        print("  Use 'python run.py' to start the application.")
    elif basic_ok:
        print("✓ Basic version ready!")
        print("  You can run the simple emotion detector.")
        print("  Use 'python simple_emotion_detector.py' to start.")
    else:
        print("✗ Installation incomplete.")
        print("  Please install all dependencies:")
        print("  pip install -r requirements.txt")
    
    print()
    print("For more help, see the README.md file.")

if __name__ == "__main__":
    main() 