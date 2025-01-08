import pygame
import math

class Player:
    def __init__(self, x, y):
        self.frames = []
        self.hurt_frames = []
        # nacitat spritesheet
        self.spritesheet = pygame.image.load("assets/characters/Player.png").convert_alpha()

        # spritesheet ma 4 frames kazdy je 16x16

        for i in range(4):
            # vybrat frame zo spritesheetu
            frame = self.spritesheet.subsurface((i * 16, 0, 16, 16))
            # zvacsit frame na 64x64
            frame = pygame.transform.scale(frame, (64, 64))
            self.frames.append(frame)

            hurt_frame = frame.copy()
            # Tint the frame red (multiply by red color)
            hurt_frame.fill((255, 0, 0, 128), special_flags=pygame.BLEND_RGBA_MULT)
            self.hurt_frames.append(hurt_frame)

        # animacne premenne
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_delay = 150  # cas medzi framami

        # vytvorit rect pre hraca
        self.rect = self.frames[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 8

        # health
        self.max_health = 3
        self.current_health = self.max_health
        self.is_alive = True
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 1000

        #kockback
        self.knockback_distance = 50
        self.knockback_speed = 15
        self.knockback_dx = 0
        self.knockback_dy = 0
        self.is_knocked_back = False

    def animate(self):
        # aktualizovat frame podla casu
        current_time = pygame.time.get_ticks()
        if current_time - self.animation_timer > self.animation_delay:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.animation_timer = current_time

    def move(self, dx, dy, walls):
        self.rect.x += dx
        if self.check_collision(walls):
            self.rect.x -= dx

        self.rect.y += dy
        if self.check_collision(walls):
            self.rect.y -= dy

        # animovat len ked sa hybe
        if dx != 0 or dy != 0:
            self.animate()

    def check_collision(self, walls):
        return any(self.rect.colliderect(wall) for wall in walls)

    def take_damage(self, enemy_pos):
        if not self.invulnerable:
            self.current_health -= 1
            if self.current_health <= 0:
                self.is_alive = False

            # nesmrtelnost a knockback
            self.invulnerable = True
            self.invulnerable_timer = pygame.time.get_ticks()

            # vypocet knockback
            dx = self.rect.centerx - enemy_pos[0]
            dy = self.rect.centery - enemy_pos[1]
            distance = math.sqrt(dx * dx + dy * dy)
            if distance != 0:
                self.knockback_dx = (dx / distance) * self.knockback_speed
                self.knockback_dy = (dy / distance) * self.knockback_speed
            self.is_knocked_back = True
            return True
        return False

    def apply_knockback(self, walls):
        if self.is_knocked_back:
            # originalna pozicia
            original_x = self.rect.x
            original_y = self.rect.y

            # pokus knockback
            self.rect.x += self.knockback_dx
            if self.check_collision(walls):
                self.rect.x = original_x

            self.rect.y += self.knockback_dy
            if self.check_collision(walls):
                self.rect.y = original_y

            self.knockback_dx *= 0.8
            self.knockback_dy *= 0.8

            # Stop knockback
            if abs(self.knockback_dx) < 0.5 and abs(self.knockback_dy) < 0.5:
                self.is_knocked_back = False
                self.knockback_dx = 0
                self.knockback_dy = 0

    def update(self):
        current_time = pygame.time.get_ticks()
        if self.invulnerable:
            if current_time - self.invulnerable_timer >= self.invulnerable_duration:
                self.invulnerable = False
                self.hurt_effect = False

    def draw(self, screen, camera_x, camera_y):
        # Choose between normal and hurt frames
        current_frames = self.hurt_frames if self.invulnerable else self.frames
        screen.blit(current_frames[self.current_frame],
                   (self.rect.x - camera_x,
                    self.rect.y - camera_y))