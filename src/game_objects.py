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
GRAY = (128, 128, 128)

class EnemyType(Enum):
    GOBLIN = "goblin"
    ORC = "orc"
    SKELETON = "skeleton"
    DEMON = "demon"

class Enemy:
    def __init__(self, x: float, y: float, enemy_type: EnemyType):
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.active = True
        
        # Set stats based on enemy type
        if enemy_type == EnemyType.GOBLIN:
            self.health = 30
            self.max_health = 30
            self.speed = 2.0
            self.radius = 15
            self.color = GREEN
            self.damage = 5
        elif enemy_type == EnemyType.ORC:
            self.health = 60
            self.max_health = 60
            self.speed = 1.5
            self.radius = 25
            self.color = ORANGE
            self.damage = 10
        elif enemy_type == EnemyType.SKELETON:
            self.health = 40
            self.max_health = 40
            self.speed = 2.5
            self.radius = 18
            self.color = GRAY
            self.damage = 8
        elif enemy_type == EnemyType.DEMON:
            self.health = 100
            self.max_health = 100
            self.speed = 1.0
            self.radius = 30
            self.color = RED
            self.damage = 15

    def update(self, player_x: float, player_y: float):
        if not self.active:
            return
            
        # Move towards player
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed

    def take_damage(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.active = False

    def draw(self, screen):
        if not self.active:
            return
            
        # Draw enemy
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Draw health bar
        health_ratio = self.health / self.max_health
        bar_width = 40
        bar_height = 5
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.radius - 10
        
        # Background
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height))
        # Health
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(bar_width * health_ratio), bar_height))

class PowerUp:
    def __init__(self, x: float, y: float, power_up_type: str):
        self.x = x
        self.y = y
        self.power_up_type = power_up_type
        self.radius = 12
        self.active = True
        
        if power_up_type == "health":
            self.color = GREEN
        elif power_up_type == "mana":
            self.color = CYAN
        elif power_up_type == "speed":
            self.color = YELLOW

    def draw(self, screen):
        if not self.active:
            return
            
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius, 2)

class Particle:
    def __init__(self, x: float, y: float, vx: float, vy: float, color: Tuple[int, int, int], lifetime: int):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.active = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        
        if self.lifetime <= 0:
            self.active = False

    def draw(self, screen):
        if not self.active:
            return
            
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color_with_alpha = (*self.color, alpha)
        
        # Create a surface with alpha
        particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, color_with_alpha, (2, 2), 2)
        screen.blit(particle_surface, (int(self.x - 2), int(self.y - 2)))

class Wall:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

class Door:
    def __init__(self, x: float, y: float, width: float, height: float, leads_to: str):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.leads_to = leads_to
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (139, 69, 19)  # Brown

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
