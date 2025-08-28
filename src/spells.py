import pygame
import math
import random
from enum import Enum
from typing import List, Tuple, Optional

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
PINK = (255, 192, 203)

class SpellType(Enum):
    FIREBALL = "fireball"
    LIGHTNING = "lightning"
    ICE_SHARD = "ice_shard"
    MAGIC_MISSILE = "magic_missile"
    FIRE_NOVA = "fire_nova"
    LIGHTNING_CHAIN = "lightning_chain"
    ICE_STORM = "ice_storm"
    TELEPORT = "teleport"

class Spell:
    def __init__(self, spell_type: SpellType, damage: int, speed: float, cooldown: int, 
                 mana_cost: int, color: Tuple[int, int, int], radius: int = 8):
        self.spell_type = spell_type
        self.damage = damage
        self.speed = speed
        self.cooldown = cooldown
        self.mana_cost = mana_cost
        self.color = color
        self.radius = radius
        self.current_cooldown = 0

class Projectile:
    def __init__(self, x: float, y: float, target_x: float, target_y: float, spell: Spell):
        self.x = x
        self.y = y
        self.spell = spell
        self.active = True
        
        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        self.dx = (dx / distance) * spell.speed if distance > 0 else 0
        self.dy = (dy / distance) * spell.speed if distance > 0 else 0
        
        # Special effects based on spell type
        if spell.spell_type == SpellType.LIGHTNING:
            self.lifetime = 30
            self.max_lifetime = 30
        elif spell.spell_type == SpellType.ICE_SHARD:
            self.lifetime = 60
            self.max_lifetime = 60
        else:
            self.lifetime = 120
            self.max_lifetime = 120

    def update(self, screen_width: int, screen_height: int):
        self.x += self.dx
        self.y += self.dy
        
        # Update lifetime
        if hasattr(self, 'lifetime'):
            self.lifetime -= 1
            if self.lifetime <= 0:
                self.active = False
        
        # Deactivate if off screen
        if self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height:
            self.active = False

    def draw(self, screen):
        if not self.active:
            return
            
        # Draw based on spell type
        if self.spell.spell_type == SpellType.LIGHTNING:
            # Lightning effect
            alpha = int(255 * (self.lifetime / self.max_lifetime))
            lightning_surface = pygame.Surface((self.spell.radius * 2, self.spell.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(lightning_surface, (*self.spell.color, alpha), 
                             (self.spell.radius, self.spell.radius), self.spell.radius)
            screen.blit(lightning_surface, (int(self.x - self.spell.radius), int(self.y - self.spell.radius)))
        elif self.spell.spell_type == SpellType.ICE_SHARD:
            # Ice shard effect
            points = [
                (self.x, self.y - self.spell.radius),
                (self.x - self.spell.radius//2, self.y + self.spell.radius//2),
                (self.x + self.spell.radius//2, self.y + self.spell.radius//2)
            ]
            pygame.draw.polygon(screen, self.spell.color, points)
        else:
            # Standard projectile
            pygame.draw.circle(screen, self.spell.color, (int(self.x), int(self.y)), self.spell.radius)

class SpellManager:
    def __init__(self):
        self.spells = {
            SpellType.FIREBALL: Spell(SpellType.FIREBALL, 30, 8, 20, 15, ORANGE),
            SpellType.LIGHTNING: Spell(SpellType.LIGHTNING, 25, 12, 15, 12, YELLOW),
            SpellType.ICE_SHARD: Spell(SpellType.ICE_SHARD, 20, 10, 10, 10, CYAN),
            SpellType.MAGIC_MISSILE: Spell(SpellType.MAGIC_MISSILE, 15, 6, 5, 8, PURPLE),
            SpellType.FIRE_NOVA: Spell(SpellType.FIRE_NOVA, 40, 0, 60, 25, RED, 50),
            SpellType.LIGHTNING_CHAIN: Spell(SpellType.LIGHTNING_CHAIN, 20, 10, 30, 20, YELLOW),
            SpellType.ICE_STORM: Spell(SpellType.ICE_STORM, 15, 5, 45, 30, CYAN),
            SpellType.TELEPORT: Spell(SpellType.TELEPORT, 0, 0, 90, 35, PINK)
        }
        
        self.unlocked_spells = {SpellType.FIREBALL, SpellType.MAGIC_MISSILE}
        self.current_spell = SpellType.FIREBALL

    def cast_spell(self, caster_x: float, caster_y: float, target_x: float, target_y: float, 
                   mana: int) -> List[Projectile]:
        spell = self.spells[self.current_spell]
        
        if spell.current_cooldown > 0 or mana < spell.mana_cost:
            return []
        
        projectiles = []
        
        if spell.spell_type == SpellType.FIRE_NOVA:
            # Cast fire nova in all directions
            for angle in range(0, 360, 30):
                rad = math.radians(angle)
                target_x = caster_x + math.cos(rad) * 100
                target_y = caster_y + math.sin(rad) * 100
                projectiles.append(Projectile(caster_x, caster_y, target_x, target_y, spell))
        
        elif spell.spell_type == SpellType.ICE_STORM:
            # Cast multiple ice shards in a cone
            base_angle = math.atan2(target_y - caster_y, target_x - caster_x)
            for i in range(-2, 3):
                angle = base_angle + math.radians(i * 15)
                target_x = caster_x + math.cos(angle) * 100
                target_y = caster_y + math.sin(angle) * 100
                projectiles.append(Projectile(caster_x, caster_y, target_x, target_y, spell))
        
        elif spell.spell_type == SpellType.TELEPORT:
            # Teleport to target location
            # This will be handled by the wizard class
            pass
        
        else:
            # Standard single projectile
            projectiles.append(Projectile(caster_x, caster_y, target_x, target_y, spell))
        
        spell.current_cooldown = spell.cooldown
        return projectiles

    def update_cooldowns(self):
        for spell in self.spells.values():
            if spell.current_cooldown > 0:
                spell.current_cooldown -= 1

    def unlock_spell(self, spell_type: SpellType):
        self.unlocked_spells.add(spell_type)

    def get_spell_info(self, spell_type: SpellType) -> str:
        spell = self.spells[spell_type]
        return f"{spell_type.value}: {spell.damage} damage, {spell.mana_cost} mana, {spell.cooldown} cooldown"
