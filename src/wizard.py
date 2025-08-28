import pygame
import math
from typing import List, Tuple
from spells import SpellManager, SpellType, Projectile
from game_objects import Particle
import random

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

class Wizard:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.radius = 25
        self.base_speed = 5
        self.speed = self.base_speed
        self.health = 100
        self.max_health = 100
        self.mana = 100
        self.max_mana = 100
        self.mana_regen = 0.5
        
        # Experience and leveling
        self.experience = 0
        self.level = 1
        self.experience_to_next = 100
        
        # Spell management
        self.spell_manager = SpellManager()
        self.projectiles: List[Projectile] = []
        
        # Effects
        self.particles: List[Particle] = []
        self.invulnerable = False
        self.invulnerability_timer = 0
        
        # Stats
        self.stats = {
            'fire_mastery': 0,
            'ice_mastery': 0,
            'lightning_mastery': 0,
            'mana_efficiency': 0,
            'spell_power': 0
        }

    def move(self, keys, walls=None):
        new_x = self.x
        new_y = self.y
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            new_y = max(self.radius, new_y - self.speed)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            new_y = min(800 - self.radius, new_y + self.speed)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            new_x = max(self.radius, new_x - self.speed)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            new_x = min(1200 - self.radius, new_x + self.speed)
        
        # Check wall collisions
        if walls:
            can_move = True
            for wall in walls:
                if wall.rect.collidepoint(new_x, new_y):
                    can_move = False
                    break
            
            if can_move:
                self.x = new_x
                self.y = new_y
        else:
            self.x = new_x
            self.y = new_y

    def cast_spell(self, target_x: float, target_y: float):
        if self.current_spell == SpellType.TELEPORT:
            self.teleport(target_x, target_y)
            return
        
        new_projectiles = self.spell_manager.cast_spell(
            self.x, self.y, target_x, target_y, self.mana
        )
        
        if new_projectiles:
            self.projectiles.extend(new_projectiles)
            spell = self.spell_manager.spells[self.current_spell]
            self.mana -= spell.mana_cost
            
            # Create casting particles
            self.create_casting_particles()

    def teleport(self, target_x: float, target_y: float):
        spell = self.spell_manager.spells[SpellType.TELEPORT]
        
        if spell.current_cooldown <= 0 and self.mana >= spell.mana_cost:
            # Create teleport particles at current location
            for _ in range(20):
                vx = random.uniform(-3, 3)
                vy = random.uniform(-3, 3)
                self.particles.append(Particle(self.x, self.y, vx, vy, CYAN, 30))
            
            # Teleport
            self.x = target_x
            self.y = target_y
            
            # Create teleport particles at new location
            for _ in range(20):
                vx = random.uniform(-3, 3)
                vy = random.uniform(-3, 3)
                self.particles.append(Particle(self.x, self.y, vx, vy, CYAN, 30))
            
            spell.current_cooldown = spell.cooldown
            self.mana -= spell.mana_cost

    def create_casting_particles(self):
        spell = self.spell_manager.spells[self.current_spell]
        for _ in range(10):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.particles.append(Particle(self.x, self.y, vx, vy, spell.color, 20))

    def take_damage(self, damage: int):
        if self.invulnerable:
            return
            
        self.health -= damage
        self.invulnerable = True
        self.invulnerability_timer = 60  # 1 second at 60 FPS
        
        # Create damage particles
        for _ in range(15):
            vx = random.uniform(-2, 2)
            vy = random.uniform(-2, 2)
            self.particles.append(Particle(self.x, self.y, vx, vy, RED, 30))

    def gain_experience(self, amount: int):
        self.experience += amount
        
        while self.experience >= self.experience_to_next:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.experience -= self.experience_to_next
        self.experience_to_next = int(self.experience_to_next * 1.5)
        
        # Increase stats
        self.max_health += 10
        self.health = self.max_health
        self.max_mana += 15
        self.mana = self.max_mana
        
        # Create level up particles
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            self.particles.append(Particle(self.x, self.y, vx, vy, YELLOW, 45))

    def update(self, screen_width: int, screen_height: int):
        # Update cooldowns
        self.spell_manager.update_cooldowns()
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update(screen_width, screen_height)
            if not projectile.active:
                self.projectiles.remove(projectile)
        
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if not particle.active:
                self.particles.remove(particle)
        
        # Update invulnerability
        if self.invulnerable:
            self.invulnerability_timer -= 1
            if self.invulnerability_timer <= 0:
                self.invulnerable = False
        
        # Regenerate mana
        self.mana = min(self.max_mana, self.mana + self.mana_regen)

    def draw(self, screen):
        # Draw wizard with invulnerability effect
        if self.invulnerable and self.invulnerability_timer % 10 < 5:
            # Flash effect when invulnerable
            return
        
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), self.radius)
        
        # Draw health bar
        health_ratio = self.health / self.max_health
        bar_width = 60
        bar_height = 8
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.radius - 25
        
        # Background
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height))
        # Health
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))
        
        # Draw mana bar
        mana_ratio = self.mana / self.max_mana
        mana_bar_y = bar_y - 12
        
        # Background
        pygame.draw.rect(screen, BLACK, (bar_x, mana_bar_y, bar_width, bar_height))
        # Mana
        pygame.draw.rect(screen, CYAN, (bar_x, mana_bar_y, int(bar_width * mana_ratio), bar_height))
        
        # Draw level
        level_y = mana_bar_y - 12
        pygame.draw.rect(screen, BLACK, (bar_x, level_y, bar_width, bar_height))
        level_ratio = self.experience / self.experience_to_next
        pygame.draw.rect(screen, YELLOW, (bar_x, level_y, int(bar_width * level_ratio), bar_height))
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(screen)

    @property
    def current_spell(self):
        return self.spell_manager.current_spell

    @current_spell.setter
    def current_spell(self, spell_type: SpellType):
        if spell_type in self.spell_manager.unlocked_spells:
            self.spell_manager.current_spell = spell_type

    def unlock_spell(self, spell_type: SpellType):
        self.spell_manager.unlock_spell(spell_type)

    def get_spell_info(self) -> str:
        return self.spell_manager.get_spell_info(self.current_spell)
