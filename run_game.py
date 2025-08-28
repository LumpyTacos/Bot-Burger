#!/usr/bin/env python3
"""
Wizard's Hack & Slash Game Launcher
Simple launcher script to start the game with proper setup.
"""

import sys
import os
import subprocess

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import pygame
        import numpy
        print("✓ All dependencies are installed!")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def main():
    print("=" * 50)
    print("🧙‍♂️ Wizard's Hack & Slash Game Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("src/main.py"):
        print("✗ Error: Please run this script from the project root directory")
        print("   (where src/main.py is located)")
        return
    
    # Check dependencies
    if not check_dependencies():
        return
    
    print("\n🎮 Starting Wizard's Hack & Slash...")
    print("Controls:")
    print("  WASD - Move")
    print("  Mouse Click - Cast Spell")
    print("  1-6 - Switch Spells")
    print("  SPACE - Start Game")
    print("  R - Restart (after game over)")
    print("  Q - Quit")
    print("\n" + "=" * 50)
    
    try:
        # Run the game
        subprocess.run([sys.executable, "src/main.py"])
    except KeyboardInterrupt:
        print("\n👋 Game stopped by user")
    except Exception as e:
        print(f"\n❌ Error running game: {e}")

if __name__ == "__main__":
    main()
