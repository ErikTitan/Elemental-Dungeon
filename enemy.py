import pygame
import math

class Enemy:
    def __init__(self, x, y, element_type):
        self.element_type = element_type

        sprite_paths = {
            "fire": "assets/characters/FireElemental.png",
            "water": "assets/characters/WaterElemental.png",
            "ground": "assets/characters/EarthElemental.png",
            "air": "assets/characters/AirElemental.png",
        }

        # nacitanie obrazku podla elementu
        self.spritesheet = pygame.image.load(sprite_paths[element_type]).convert_alpha()

        # extrakcia a zvacsenie obrazkov
        self.frames = []
        for i in range(4):
            frame = self.spritesheet.subsurface((i * 16, 0, 16, 16))
            frame = pygame.transform.scale(frame, (64, 64))
            self.frames.append(frame)

        # premenne pre animaciu
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_delay = 150

        # rect pre enemy
        self.rect = self.frames[0].get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 4

    def animate(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.animation_timer = current_time

    def move_towards_player(self, player_pos, walls, enemies):  # Add enemies parameter
        player_x, player_y = player_pos
        dx = player_x - self.rect.x
        dy = player_y - self.rect.y
        distance = math.sqrt(dx * dx + dy * dy)

        if distance != 0:
            # normalizovany smer
            dx = (dx / distance) * self.speed
            dy = (dy / distance) * self.speed

        # originalna pozicia pre kolizie
        original_x = self.rect.x
        original_y = self.rect.y

        # skus horizontalny pohyb
        self.rect.x += dx
        if self.check_collisions(walls, enemies):
            self.rect.x = original_x

        # skus horizontalny pohyb
        self.rect.y += dy
        if self.check_collisions(walls, enemies):
            self.rect.y = original_y

        self.animate()

    def check_collisions(self, walls, enemies):
        # kolizia so stenou
        if any(self.rect.colliderect(wall) for wall in walls):
            return True

        # kolizia s enemy
        for enemy in enemies:
            if enemy != self and self.rect.colliderect(enemy.rect):
                return True

        return False

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.frames[self.current_frame],
                    (self.rect.x - camera_x,
                     self.rect.y - camera_y))
