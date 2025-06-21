#!/usr/bin/env python3
"""
Emotion Detection Launcher
Choose between full and simple versions of the emotion detector
"""

import sys
import os
import subprocess

def print_banner():
    """Print the application banner"""
    print("=" * 60)
    print("           CAMERA EMOTIONS - EMOTION DETECTION")
    print("=" * 60)
    print()

def print_menu():
    """Print the main menu"""
    print("Choose your emotion detection version:")
    print()
    print("1. Full Version (Recommended)")
    print("   - Uses DeepFace for accurate emotion recognition")
    print("   - Supports 7 emotion categories")
    print("   - Higher accuracy but slower performance")
    print("   - Requires more computational resources")
    print()
    print("2. Simple Version")
    print("   - Uses basic facial feature analysis")
    print("   - Faster performance")
    print("   - Less accurate but good for testing")
    print("   - Works on systems with limited resources")
    print()
    print("3. Exit")
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import cv2
        import numpy as np
        import tkinter
        from PIL import Image
        print("✓ Basic dependencies found")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies using: pip install -r requirements.txt")
        return False

def check_full_version_dependencies():
    """Check if full version dependencies are available"""
    try:
        import mediapipe
        from deepface import DeepFace
        print("✓ Full version dependencies found")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency for full version: {e}")
        print("Full version requires additional dependencies.")
        print("Install with: pip install mediapipe deepface")
        return False

def run_full_version():
    """Run the full emotion detector"""
    print("Starting Full Version...")
    print("This version uses DeepFace for accurate emotion recognition.")
    print("Initial loading may take a moment...")
    print()
    
    try:
        # Import and run the full version
        from emotion_detector import main
        main()
    except Exception as e:
        print(f"Error running full version: {e}")
        print("Try installing missing dependencies or use the simple version.")

def run_simple_version():
    """Run the simple emotion detector"""
    print("Starting Simple Version...")
    print("This version uses basic facial feature analysis.")
    print()
    
    try:
        # Import and run the simple version
        from simple_emotion_detector import main
        main()
    except Exception as e:
        print(f"Error running simple version: {e}")

def main():
    """Main launcher function"""
    print_banner()
    
    # Check basic dependencies
    if not check_dependencies():
        input("Press Enter to exit...")
        return
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == "1":
                print("\nChecking full version dependencies...")
                if check_full_version_dependencies():
                    run_full_version()
                else:
                    print("\nWould you like to try the simple version instead? (y/n): ", end="")
                    if input().lower().startswith('y'):
                        run_simple_version()
                break
                
            elif choice == "2":
                run_simple_version()
                break
                
            elif choice == "3":
                print("Goodbye!")
                break
                
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                print()
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == "__main__":
    main() 