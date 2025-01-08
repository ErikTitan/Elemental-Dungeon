import pygame
import math

class Projectile:
    def __init__(self, x, y, target_x, target_y, element_type):
        # rect tvar
        self.rect = pygame.Rect(x, y, 64, 24)
        self.element_type = element_type
        self.speed = 10

        self.sprites = []
        for i in range(1, 5):
            sprite = pygame.image.load(f"assets/projectiles/{element_type.capitalize()}{i}.png")
            sprite = pygame.transform.scale(sprite, (64, 24))
            # mirror
            sprite = pygame.transform.flip(sprite, True, False)
            self.sprites.append(sprite)

        self.current_frame = 0
        self.animation_speed = 0.2
        self.animation_timer = 0

        dx = target_x - x
        dy = target_y - y
        self.angle = math.degrees(math.atan2(-dy, dx))
        dist = math.sqrt(dx * dx + dy * dy)
        self.dx = (dx / dist) * self.speed if dist != 0 else 0
        self.dy = (dy / dist) * self.speed if dist != 0 else 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen, camera_x, camera_y):
        sprite = self.sprites[self.current_frame]
        rotated_sprite = pygame.transform.rotate(sprite, self.angle)

        sprite_rect = rotated_sprite.get_rect(center=(
            self.rect.centerx - camera_x,
            self.rect.centery - camera_y
        ))

        screen.blit(rotated_sprite, sprite_rect)

    def hits_wall(self, walls):
        return any(self.rect.colliderect(wall) for wall in walls)