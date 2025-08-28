import pygame
import sys
import math
import random
from typing import List, Optional
from enum import Enum

from wizard import Wizard
from game_objects import Enemy, EnemyType, PowerUp, Wall, Door, Particle
from spells import SpellType

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

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

class GameState(Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wizard's Hack & Slash")
        self.clock = pygame.time.Clock()
        
        self.state = GameState.MENU
        self.wizard = Wizard(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.enemies: List[Enemy] = []
        self.power_ups: List[PowerUp] = []
        self.walls: List[Wall] = []
        self.doors: List[Door] = []
        self.particles: List[Particle] = []
        
        self.score = 0
        self.wave = 1
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 60
        self.power_up_timer = 0
        self.power_up_delay = 600  # 10 seconds
        
        # Font
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Initialize level
        self.setup_level()

    def setup_level(self):
        # Clear existing objects
        self.enemies.clear()
        self.power_ups.clear()
        self.walls.clear()
        self.doors.clear()
        
        # Add some walls for cover
        self.walls.extend([
            Wall(200, 200, 100, 20),
            Wall(400, 300, 100, 20),
            Wall(600, 400, 100, 20),
            Wall(800, 200, 100, 20),
            Wall(300, 600, 100, 20),
            Wall(700, 600, 100, 20),
        ])
        
        # Add doors
        self.doors.append(Door(SCREEN_WIDTH - 50, SCREEN_HEIGHT // 2, 40, 80, "next_level"))

    def spawn_enemy(self):
        # Spawn enemies from edges
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if side == 'top':
            x = random.randint(0, SCREEN_WIDTH)
            y = -20
        elif side == 'bottom':
            x = random.randint(0, SCREEN_WIDTH)
            y = SCREEN_HEIGHT + 20
        elif side == 'left':
            x = -20
            y = random.randint(0, SCREEN_HEIGHT)
        else:  # right
            x = SCREEN_WIDTH + 20
            y = random.randint(0, SCREEN_HEIGHT)
        
        # Choose enemy type based on wave
        if self.wave < 3:
            enemy_type = EnemyType.GOBLIN
        elif self.wave < 6:
            enemy_type = random.choice([EnemyType.GOBLIN, EnemyType.SKELETON])
        elif self.wave < 10:
            enemy_type = random.choice([EnemyType.GOBLIN, EnemyType.SKELETON, EnemyType.ORC])
        else:
            enemy_type = random.choice([EnemyType.SKELETON, EnemyType.ORC, EnemyType.DEMON])
        
        self.enemies.append(Enemy(x, y, enemy_type))

    def spawn_power_up(self):
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        power_up_type = random.choice(["health", "mana", "speed"])
        self.power_ups.append(PowerUp(x, y, power_up_type))

    def check_collisions(self):
        # Check projectile-enemy collisions
        for projectile in self.wizard.projectiles[:]:
            for enemy in self.enemies[:]:
                if not enemy.active:
                    continue
                    
                distance = math.sqrt((projectile.x - enemy.x)**2 + (projectile.y - enemy.y)**2)
                if distance < projectile.spell.radius + enemy.radius:
                    enemy.take_damage(projectile.spell.damage)
                    projectile.active = False
                    
                    # Create hit particles
                    for _ in range(10):
                        vx = random.uniform(-2, 2)
                        vy = random.uniform(-2, 2)
                        self.particles.append(Particle(enemy.x, enemy.y, vx, vy, projectile.spell.color, 20))
                    
                    if not enemy.active:
                        self.score += 10
                        self.wizard.gain_experience(5)
                        
                        # Chance to drop power up
                        if random.random() < 0.1:  # 10% chance
                            self.spawn_power_up()
                    break
        
        # Check wizard-enemy collisions
        for enemy in self.enemies[:]:
            if not enemy.active:
                continue
                
            distance = math.sqrt((self.wizard.x - enemy.x)**2 + (self.wizard.y - enemy.y)**2)
            if distance < self.wizard.radius + enemy.radius:
                self.wizard.take_damage(enemy.damage)
                if self.wizard.health <= 0:
                    return False  # Game over
        
        # Check wizard-power up collisions
        for power_up in self.power_ups[:]:
            if not power_up.active:
                continue
                
            distance = math.sqrt((self.wizard.x - power_up.x)**2 + (self.wizard.y - power_up.y)**2)
            if distance < self.wizard.radius + power_up.radius:
                if power_up.power_up_type == "health":
                    self.wizard.health = min(self.wizard.max_health, self.wizard.health + 30)
                elif power_up.power_up_type == "mana":
                    self.wizard.mana = min(self.wizard.max_mana, self.wizard.mana + 50)
                elif power_up.power_up_type == "speed":
                    self.wizard.speed = self.wizard.base_speed * 1.5
                    # Reset speed after 5 seconds
                    pygame.time.set_timer(pygame.USEREVENT, 5000)
                
                power_up.active = False
                self.power_ups.remove(power_up)
                
                # Create pickup particles
                for _ in range(15):
                    vx = random.uniform(-1, 1)
                    vy = random.uniform(-1, 1)
                    self.particles.append(Particle(power_up.x, power_up.y, vx, vy, power_up.color, 30))
        
        # Check wizard-door collisions
        for door in self.doors:
            if door.rect.collidepoint(self.wizard.x, self.wizard.y):
                self.next_level()
        
        return True  # Game continues

    def next_level(self):
        self.wave += 1
        self.enemy_spawn_delay = max(20, self.enemy_spawn_delay - 5)  # Faster spawning
        self.setup_level()
        
        # Unlock new spells based on level
        if self.wave == 3:
            self.wizard.unlock_spell(SpellType.LIGHTNING)
        elif self.wave == 5:
            self.wizard.unlock_spell(SpellType.ICE_SHARD)
        elif self.wave == 8:
            self.wizard.unlock_spell(SpellType.FIRE_NOVA)
        elif self.wave == 12:
            self.wizard.unlock_spell(SpellType.TELEPORT)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.wizard.move(keys, self.walls)
        
        # Spell switching
        if keys[pygame.K_1] and SpellType.FIREBALL in self.wizard.spell_manager.unlocked_spells:
            self.wizard.current_spell = SpellType.FIREBALL
        elif keys[pygame.K_2] and SpellType.LIGHTNING in self.wizard.spell_manager.unlocked_spells:
            self.wizard.current_spell = SpellType.LIGHTNING
        elif keys[pygame.K_3] and SpellType.ICE_SHARD in self.wizard.spell_manager.unlocked_spells:
            self.wizard.current_spell = SpellType.ICE_SHARD
        elif keys[pygame.K_4] and SpellType.MAGIC_MISSILE in self.wizard.spell_manager.unlocked_spells:
            self.wizard.current_spell = SpellType.MAGIC_MISSILE
        elif keys[pygame.K_5] and SpellType.FIRE_NOVA in self.wizard.spell_manager.unlocked_spells:
            self.wizard.current_spell = SpellType.FIRE_NOVA
        elif keys[pygame.K_6] and SpellType.TELEPORT in self.wizard.spell_manager.unlocked_spells:
            self.wizard.current_spell = SpellType.TELEPORT

    def update(self):
        self.wizard.update(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.wizard.x, self.wizard.y)
            if not enemy.active:
                self.enemies.remove(enemy)
        
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if not particle.active:
                self.particles.remove(particle)
        
        # Spawn enemies
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
        
        # Spawn power ups
        self.power_up_timer += 1
        if self.power_up_timer >= self.power_up_delay:
            self.spawn_power_up()
            self.power_up_timer = 0
        
        # Check collisions
        return self.check_collisions()

    def draw_menu(self):
        self.screen.fill(BLACK)
        
        title = self.font.render("Wizard's Hack & Slash", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
        
        start_text = self.font.render("Press SPACE to start", True, WHITE)
        self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 300))
        
        controls = [
            "Controls:",
            "WASD - Move",
            "Mouse Click - Cast Spell",
            "1-6 - Switch Spells",
            "Survive as long as possible!"
        ]
        
        for i, control in enumerate(controls):
            text = self.small_font.render(control, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 400 + i * 30))

    def draw_game(self):
        self.screen.fill(BLACK)
        
        # Draw walls
        for wall in self.walls:
            wall.draw(self.screen)
        
        # Draw doors
        for door in self.doors:
            door.draw(self.screen)
        
        # Draw wizard
        self.wizard.draw(self.screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        # Draw power ups
        for power_up in self.power_ups:
            power_up.draw(self.screen)
        
        # Draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        wave_text = self.font.render(f"Wave: {self.wave}", True, WHITE)
        self.screen.blit(wave_text, (10, 50))
        
        level_text = self.font.render(f"Level: {self.wizard.level}", True, WHITE)
        self.screen.blit(level_text, (10, 90))
        
        spell_text = self.font.render(f"Spell: {self.wizard.current_spell.value}", True, WHITE)
        self.screen.blit(spell_text, (10, 130))
        
        # Draw spell info
        spell_info = [
            "1: Fireball (High damage, slow)",
            "2: Lightning (Medium damage, fast)",
            "3: Ice Shard (Low damage, medium speed)",
            "4: Magic Missile (Low damage, fast, low cooldown)",
            "5: Fire Nova (Area damage)",
            "6: Teleport (Escape ability)"
        ]
        
        for i, info in enumerate(spell_info):
            if i < len(self.wizard.spell_manager.unlocked_spells):
                color = WHITE
            else:
                color = (100, 100, 100)  # Grayed out
            info_text = self.small_font.render(info, True, color)
            self.screen.blit(info_text, (10, 170 + i * 20))

    def draw_game_over(self):
        self.screen.fill(BLACK)
        
        game_over_text = self.font.render("GAME OVER!", True, RED)
        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 300))
        
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 350))
        
        wave_text = self.font.render(f"Waves Survived: {self.wave}", True, WHITE)
        self.screen.blit(wave_text, (SCREEN_WIDTH // 2 - wave_text.get_width() // 2, 390))
        
        restart_text = self.font.render("Press R to restart or Q to quit", True, WHITE)
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 450))

    def draw(self):
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.PLAYING:
            self.draw_game()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        
        pygame.display.flip()

    def run(self):
        running = True
        game_over = False
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == GameState.MENU:
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_r and self.state == GameState.GAME_OVER:
                        self.__init__()
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_q and self.state == GameState.GAME_OVER:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.state == GameState.PLAYING:
                    # Cast spell at mouse position
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.wizard.cast_spell(mouse_x, mouse_y)
                elif event.type == pygame.USEREVENT:
                    # Reset speed boost
                    self.wizard.speed = self.wizard.base_speed
            
            if self.state == GameState.PLAYING:
                self.handle_input()
                game_over = not self.update()
                if game_over:
                    self.state = GameState.GAME_OVER
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
