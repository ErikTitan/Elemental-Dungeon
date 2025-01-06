import pygame


class Player:
    def __init__(self, x, y):
        # nacitat spritesheet
        self.spritesheet = pygame.image.load("assets/characters/Player.png").convert_alpha()

        # spritesheet ma 4 framy kazdy je 16x16
        self.frames = []
        for i in range(4):
            # vybrat frame zo spritesheetu
            frame = self.spritesheet.subsurface((i * 16, 0, 16, 16))
            # zvacsit frame na 64x64
            frame = pygame.transform.scale(frame, (64, 64))
            self.frames.append(frame)

        # animacne premenne
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_delay = 150  # cas medzi framami

        # vytvorit rect pre hraca
        self.rect = self.frames[0].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 8

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

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.frames[self.current_frame],
                    (self.rect.x - camera_x,
                     self.rect.y - camera_y))
