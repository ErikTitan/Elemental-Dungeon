import pygame
from player import Player


class Game:
    def __init__(self):
        pygame.init()
        screen_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        # Scale tiles up for better visibility
        self.TILE_SIZE = 64  # Scaled up from 32
        self.floor_tiles = [
            pygame.transform.scale(pygame.image.load(f"assets/floor{i}.png"), (self.TILE_SIZE, self.TILE_SIZE))
            for i in range(1, 4)]
        self.wall_tiles = [
            pygame.transform.scale(pygame.image.load(f"assets/wall{i}.png"), (self.TILE_SIZE, self.TILE_SIZE))
            for i in range(1, 5)]

        self.create_map()
        # Spawn player in first room
        self.player = Player(3 * self.TILE_SIZE, 3 * self.TILE_SIZE)
        self.camera_x = 0
        self.camera_y = 0

    def create_map(self):
        self.walls = []

        self.layout = [
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "W11111111WW........WW...........................................W",
            "W11111111WW........WW........................WWWWWWWWWWWWWWWWWWWW",
            "W11111111WW........WW........................W222222222222222222W",
            "W11111111WW........WW........................W222222222222222222W",
            "W11111111WW........WWWWWWWWWW...WWWWWWWWWWWWW2222222222222222222W",
            "W11111111WW........................W2222222222222222222222222222W",
            "W11111111WW........................W2222222222222222222222222222W",
            "WWWWWW...WW........................W2222222222222222222222222222W",
            "W........WW........................WWWWWWWWWWWWWWWWWWWWWWWW...WWW",
            "W........WWWWWWWWWWWWWWWWWWWWW..................................W",
            "W...............................................................W",
            "W........................................WWWWWWWWWWWWWWWWWWW....W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW........W33333333333333333333W....W",
            "W11111111111111111111W................W33333333333333333333W....W",
            "W11111111111111111111W................W33333333333333333333W....W",
            "W11111111111111111111.................W33333333333333333333W....W",
            "W11111111111111111111.........WWWWWWWWW33333333333333333333W....W",
            "W11111111111111111111W........W2222222233333333333333333333W....W",
            "W11111111111111111111W........W2222222233333333333333333333W....W",
            "W11111111111111111111W........W2222222233333333333333333333W....W",
            "WWWWWWWWWWWWWWWWWWWWWW........WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW....W",
            "W...............................................................W",
            "W...............................................................W",
            "W...............................................................W",
            "W.WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW................W",
            "W.W11111111111111111111111111111111111111111111W................W",
            "W.W11111111111111111111111111111111111111111111.................W",
            "W.W11111111111111111111111111111111111111111111.................W",
            "W.W11111111111111111111111111111111111111111111W................W",
            "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ]

        for y, row in enumerate(self.layout):
            for x, char in enumerate(row):
                if char == 'W':
                    wall_type = ((x + y) % 4) + 1
                    self.walls.append(pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE,
                                                  self.TILE_SIZE, self.TILE_SIZE))

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            return False

        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * self.player.speed
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * self.player.speed
        self.player.move(dx, dy, self.walls)

        # Camera follows player with some zoom
        self.camera_x = self.player.rect.x - self.screen.get_width() // 2
        self.camera_y = self.player.rect.y - self.screen.get_height() // 2
        return True

    def draw(self):
        self.screen.fill((0, 0, 0))

        # Draw floor and walls
        for y, row in enumerate(self.layout):
            for x, char in enumerate(row):
                screen_x = x * self.TILE_SIZE - self.camera_x
                screen_y = y * self.TILE_SIZE - self.camera_y

                # Only draw tiles that are visible on screen
                if (-self.TILE_SIZE <= screen_x <= self.screen.get_width() and
                        -self.TILE_SIZE <= screen_y <= self.screen.get_height()):
                    if char.isdigit():
                        self.screen.blit(self.floor_tiles[int(char) - 1], (screen_x, screen_y))
                    elif char == 'W':
                        wall_type = ((x + y) % 4)
                        self.screen.blit(self.wall_tiles[wall_type], (screen_x, screen_y))

        # Draw player
        pygame.draw.rect(self.screen, (255, 0, 0),
                         pygame.Rect(self.player.rect.x - self.camera_x,
                                     self.player.rect.y - self.camera_y,
                                     self.TILE_SIZE, self.TILE_SIZE))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            running = self.handle_input()
            self.draw()
            self.clock.tick(60)

        pygame.quit()