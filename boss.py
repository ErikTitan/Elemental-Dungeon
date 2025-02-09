import pygame
import math
from game_settings import GameSettings

class Boss:
    def __init__(self, x, y):
        self.health = 30
        self.state = "flying"
        self.speed = 3
        self.attack_cooldown = 0
        self.last_hit_time = 0
        self.hurt_duration = 200  # ms
        self.attack_duration = 1000  # ms
        self.animation_frame = 0
        self.animation_timer = 0
        self.has_shot = False
        self.settings = GameSettings()
        self.last_fly_sound_time = 0

        # Load spritesheets
        self.load_animations()
        self.rect = pygame.Rect(x, y, 128, 128)

    def load_animations(self):
        self.animations = {
            "hurt": self.load_spritesheet("assets/boss/HURT.png", 4),
            "flying": self.load_spritesheet("assets/boss/FLYING.png", 4),
            "attack": self.load_spritesheet("assets/boss/ATTACK.png", 8)
        }

    def load_spritesheet(self, path, frame_count):
        sheet = pygame.image.load(path).convert_alpha()
        frames = []
        frame_width = sheet.get_width() // frame_count
        for i in range(frame_count):
            frame = sheet.subsurface((i * frame_width, 0, 64, 64))
            frames.append(pygame.transform.scale(frame, (128, 128)))
        return frames

    def update(self, player_pos, projectiles):
        current_time = pygame.time.get_ticks()

        # State management
        if self.state == "hurt" and current_time - self.last_hit_time > self.hurt_duration:
            self.state = "flying"

        if self.state == "attack" and current_time - self.last_hit_time > self.attack_duration:
            self.state = "flying"

        if self.state == "flying" and current_time - self.last_fly_sound_time >= 1000:
            self.settings.boss_fly_sound.play()
            self.last_fly_sound_time = current_time

        if self.state == "attack":
            self.settings.boss_fly_sound.stop()

        if self.state != "hurt" and self.state != "attack":
            self.state = "flying"
            self.move_towards_player(player_pos)

        px, py = player_pos
        distance = math.hypot(px - self.rect.centerx, py - self.rect.centery)

        if self.attack_cooldown <= 0 and distance < 500:
            self.state = "attack"
            self.attack_cooldown = 3000
            self.last_hit_time = current_time
            self.has_shot = False
        else:
            self.attack_cooldown -= 1000 / 60

        # Animation update
        self.animate(current_time)

        # projectile hit
        for projectile in projectiles[:]:
            if self.rect.colliderect(projectile.rect):
                self.take_damage()
                projectiles.remove(projectile)

    def take_damage(self):
        self.health -= 1
        self.state = "hurt"
        self.last_hit_time = pygame.time.get_ticks()

    def move_towards_player(self, player_pos):
        px, py = player_pos
        dx = px - self.rect.centerx
        dy = py - self.rect.centery
        distance = math.hypot(dx, dy)

        if distance > 0:
            self.rect.x += (dx / distance) * self.speed
            self.rect.y += (dy / distance) * self.speed

    def animate(self, current_time):
        anim = self.animations[self.state]
        if current_time - self.animation_timer > 100:
            self.animation_frame = (self.animation_frame + 1) % len(anim)
            self.animation_timer = current_time

    def shoot_projectile(self, player_pos):
        if self.state == "attack" and self.animation_frame == 4 and not self.has_shot:
            self.has_shot = True
            self.settings.boss_fire_sound.play()
            return BossProjectile(
                self.rect.centerx,
                self.rect.centery,
                player_pos[0],
                player_pos[1]
            )
        return None

    def draw(self, screen, camera_x, camera_y):
        current_anim = self.animations[self.state]
        self.animation_frame = min(self.animation_frame, len(current_anim) - 1)
        frame = current_anim[self.animation_frame]
        screen.blit(frame, (self.rect.x - camera_x, self.rect.y - camera_y))

class BossProjectile:
    def __init__(self, x, y, target_x, target_y):
        self.rect = pygame.Rect(x, y, 96, 64)
        self.speed = 7

        self.base_image = pygame.image.load("assets/boss/projectile.png").convert_alpha()
        self.base_image = pygame.transform.scale(self.base_image, (96, 64))

        # direction and angle
        dx = target_x - x
        dy = target_y - y
        self.angle = math.degrees(math.atan2(dy, dx))
        self.image = pygame.transform.rotate(self.base_image, -self.angle)

        self.rect = self.image.get_rect(center=self.rect.center)

        # movement
        dist = math.hypot(dx, dy)
        if dist > 0:
            self.dx = (dx / dist) * self.speed
            self.dy = (dy / dist) * self.speed
        else:
            self.dx = self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y - camera_y))

    def hits_wall(self, walls):
        return any(self.rect.colliderect(wall) for wall in walls)