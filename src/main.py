#!/usr/bin/env python3
"""
Wizard's Hack & Slash Game
A magical hack and slash game with bullet hell and dungeon crawler elements.

Run this file to start the game!
"""

from game import Game

if __name__ == "__main__":
    print("Starting Wizard's Hack & Slash...")
    print("Controls:")
    print("- WASD: Move")
    print("- Mouse Click: Cast Spell")
    print("- 1-6: Switch Spells")
    print("- Survive as long as possible!")
    print()
    
    game = Game()
    game.run()
