# Wizard's Hack & Slash

A magical hack and slash game with bullet hell and dungeon crawler elements, featuring a powerful wizard fighting off waves of enemies with various spells and abilities.

## Features

### 🧙‍♂️ Wizard Character
- **Multiple Spells**: Fireball, Lightning, Ice Shard, Magic Missile, Fire Nova, and Teleport
- **Experience System**: Level up to unlock new spells and increase stats
- **Health & Mana Management**: Strategic resource management
- **Invulnerability Frames**: Brief invincibility after taking damage

### ⚔️ Combat System
- **Hack & Slash**: Fast-paced melee-style combat with magical projectiles
- **Bullet Hell Elements**: Multiple enemies and projectiles to dodge
- **Dungeon Crawler**: Explore levels with walls, doors, and power-ups
- **Progressive Difficulty**: Enemies get stronger and spawn faster over time

### 🎮 Gameplay
- **Wave-based Survival**: Survive increasingly difficult waves of enemies
- **Multiple Enemy Types**: Goblins, Skeletons, Orcs, and Demons with unique stats
- **Power-ups**: Health, Mana, and Speed boosts
- **Particle Effects**: Visual feedback for spells, damage, and level-ups

## Controls

- **WASD** or **Arrow Keys**: Move the wizard
- **Mouse Click**: Cast spell at cursor position
- **1-6**: Switch between unlocked spells
- **SPACE**: Start game (from menu)
- **R**: Restart game (after game over)
- **Q**: Quit game

## Spells

1. **Fireball** (1): High damage, slow projectile
2. **Lightning** (2): Medium damage, fast projectile
3. **Ice Shard** (3): Low damage, medium speed
4. **Magic Missile** (4): Low damage, fast, low cooldown
5. **Fire Nova** (5): Area damage in all directions
6. **Teleport** (6): Instant movement to cursor position

## Installation

1. Install Python 3.7 or higher
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python src/main.py
   ```

## Game Mechanics

### Progression
- Start with Fireball and Magic Missile
- Unlock Lightning at Wave 3
- Unlock Ice Shard at Wave 5
- Unlock Fire Nova at Wave 8
- Unlock Teleport at Wave 12

### Enemy Types
- **Goblin**: Fast, low health, low damage
- **Skeleton**: Medium speed, medium health, medium damage
- **Orc**: Slow, high health, high damage
- **Demon**: Very slow, very high health, very high damage

### Power-ups
- **Health** (Green): Restore 30 health
- **Mana** (Cyan): Restore 50 mana
- **Speed** (Yellow): 1.5x speed for 5 seconds

## Development

The game is built with Python and Pygame, organized into modular components:

- `main.py`: Entry point
- `game.py`: Main game loop and state management
- `wizard.py`: Player character with spells and abilities
- `spells.py`: Spell system and projectiles
- `game_objects.py`: Enemies, power-ups, and environmental objects

## Future Enhancements

- [ ] More spell types and combinations
- [ ] Boss battles
- [ ] Multiple levels and environments
- [ ] Sound effects and music
- [ ] Save/load system
- [ ] Multiplayer support
- [ ] More enemy types and behaviors
- [ ] Equipment and inventory system

## Requirements

- Python 3.7+
- Pygame 2.5.2
- NumPy 1.24.3

Enjoy casting spells and surviving the magical onslaught! 🔥⚡❄️
