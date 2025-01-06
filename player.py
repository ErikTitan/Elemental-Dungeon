import pygame


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 64, 64)  # Scaled to match tile size
        self.speed = 8  # Increased speed for larger map

    def move(self, dx, dy, walls):
        self.rect.x += dx
        if self.check_collision(walls):
            self.rect.x -= dx

        self.rect.y += dy
        if self.check_collision(walls):
            self.rect.y -= dy

    def check_collision(self, walls):
        return any(self.rect.colliderect(wall) for wall in walls)