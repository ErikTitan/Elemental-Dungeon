import pygame
import math

class Enemy:
    def __init__(self, x, y, element_type):
        self.rect = pygame.Rect(x, y, 64, 64)
        self.element_type = element_type  # "fire", "water", "ground", "air"
        self.speed = 4
        self.colors = {
            "fire": (255, 0, 0),
            "water": (0, 0, 255),
            "ground": (139, 69, 19),
            "air": (200, 200, 200)
        }

    def move_towards_player(self, player_pos, walls):
        dx = player_pos[0] - self.rect.x
        dy = player_pos[1] - self.rect.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist != 0:
            dx = dx / dist * self.speed
            dy = dy / dist * self.speed

            # Try horizontal movement
            self.rect.x += dx
            if any(self.rect.colliderect(wall) for wall in walls):
                self.rect.x -= dx

            # Try vertical movement
            self.rect.y += dy
            if any(self.rect.colliderect(wall) for wall in walls):
                self.rect.y -= dy
