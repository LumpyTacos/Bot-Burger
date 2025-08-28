#!/usr/bin/env python3
"""
Setup script for Wizard's Hack & Slash Game
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing dependencies: {e}")
        return False

def main():
    print("=" * 50)
    print("🧙‍♂️ Wizard's Hack & Slash Game Setup")
    print("=" * 50)
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("✗ Error: requirements.txt not found!")
        print("   Please run this script from the project root directory")
        return
    
    # Install dependencies
    if install_requirements():
        print("\n🎉 Setup complete! You can now run the game with:")
        print("   python run_game.py")
        print("   or")
        print("   python src/main.py")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
