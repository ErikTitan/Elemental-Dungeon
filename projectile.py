import pygame
import math

class Projectile:
    def __init__(self, x, y, target_x, target_y, element_type):
        self.rect = pygame.Rect(x, y, 16, 16)
        self.element_type = element_type
        self.speed = 10
        self.colors = {
            "fire": (255, 100, 0),
            "water": (0, 100, 255),
            "ground": (165, 82, 23),
            "air": (220, 220, 220)
        }

        # Calculate direction
        dx = target_x - x
        dy = target_y - y
        dist = math.sqrt(dx * dx + dy * dy)
        self.dx = (dx / dist) * self.speed if dist != 0 else 0
        self.dy = (dy / dist) * self.speed if dist != 0 else 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def hits_wall(self, walls):
        return any(self.rect.colliderect(wall) for wall in walls)
