import pygame
from player import Player
from enemy import Enemy
from projectile import Projectile
import random

class Game:
    def __init__(self):
        pygame.init()
        screen_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.BASE_TILE_SIZE = 16
        self.TILE_SIZE = 64   # velkost tile

        self.floor_tiles = [
            pygame.transform.scale(
                pygame.image.load(f"assets/map/floor{i}.png"),
                (self.TILE_SIZE, self.TILE_SIZE)
            ) for i in range(1, 5)
        ]
        self.random_wall_tiles = {
            'T': [pygame.transform.scale(pygame.image.load(f"assets/map/wall{i}.png"),
                                         (self.TILE_SIZE, self.TILE_SIZE)) for i in range(1, 5)],
            'H': [pygame.transform.scale(pygame.image.load(f"assets/map/wall_half{i}.png"),
                                         (self.TILE_SIZE, self.TILE_SIZE)) for i in range(1, 3)]
        }

        self.single_wall_tiles = {
            'L': pygame.transform.scale(pygame.image.load("assets/map/wall_left_angle.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            'R': pygame.transform.scale(pygame.image.load("assets/map/wall_right_angle.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            'C': pygame.transform.scale(pygame.image.load("assets/map/TL_single_corner.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            'D': pygame.transform.scale(pygame.image.load("assets/map/TR_single_corner.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            'E': pygame.transform.scale(pygame.image.load("assets/map/TR_corner.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            'F': pygame.transform.scale(pygame.image.load("assets/map/TL_corner.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE))
        }

        self.decoration_tiles = {
            'W': pygame.transform.scale(pygame.image.load("assets/decorations/cobweb.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            'T': pygame.transform.scale(pygame.image.load("assets/decorations/torch1.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            'B': pygame.transform.scale(pygame.image.load("assets/decorations/torch2.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            'V': pygame.transform.scale(pygame.image.load("assets/decorations/bones1.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            'J': pygame.transform.scale(pygame.image.load("assets/decorations/bones2.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            'X': pygame.transform.scale(pygame.image.load("assets/decorations/flag.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            'Y': pygame.transform.scale(pygame.image.load("assets/decorations/chain.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
        }

        self.create_map()
        self.player = Player(3 * self.TILE_SIZE, 3 * self.TILE_SIZE)
        self.camera_x = 0
        self.camera_y = 0

        self.enemies = []
        self.projectiles = []
        self.player_element = "fire" # default element
        self.spawn_timer = 0
        self.spawn_delay = 180
        self.can_shoot = True
        self.shoot_cooldown = 300
        self.last_shot_time = 0

    def create_map(self):
        self.walls = []

        # T: Top wall (full wall)
        # L: Left angled wall
        # R: Right angled wall
        # H: Half wall
        # C: Top left single corner
        # D: Top right single corner
        # E: Top right corner
        # F: Top left corner
        # .: Floor
        self.layout = [
            "LTTTTTTTTTTTTTTTTTTTTTTTTTTTTTR      LTTTTTTTTTTTTTTTTTTTTTTTTTTR",
            "L.............................R      L..........................R",
            "L.............................R      L..........................R",
            "L.............................R      L..........................R",
            "L.............................R      L..........................R",
            "L.............................TTTTTTTT..........................R",
            "L...............................................................R",
            "L...............................................................R",
            "DHHHHHHHHHE.....................................................R",
            "          L...............FHHHHHHHHHHHHHHE......................R",
            "LTTTTTTTTTT...............R              L......................R",
            "L.........................R              L......................R",
            "L.........................R              L...........FHHHHHHHHHHC",
            "L.........................TTTTTTTTTTTTTTTT...........R           ",
            "L....................................................R           ",
            "L....................................................TTTTTTTTTTTR",
            "L...............................................................R",
            "L...............................................................R",
            "L...............................................................R",
            "L...............................................................R",
            "L...............................................................R",
            "L...............................................................R",
            "DHHHHHHHHHHHE..............FHHHHHHHHHHE.........................R",
            "            L..............R          L.........................R",
            "            L..............R          L.........................R",
            "            L..............R          L.........................R",
            "            L..............R          L.........................R",
            "            L..............R          L.........................R",
            "            L..............R          L.........................R",
            "            L..............R          L.........................R",
            "            DHHHHHHHHHHHHHHC          DHHHHHHHHHHHHHHHHHHHHHHHHHC"
        ]

        # W: cobweb
        # T: torch1
        # B: torch2
        # V: bones1
        # J: bones2
        # X: flag
        # Y: chain
        self.decoration_layout = [
            " WT  Y         T       Y   T          W Y     T          Y   T  ",
            "                                                                 ",
            "                             V                                   ",
            "                                                                 ",
            "                                                                 ",
            "                                  X                              ",
            "                                                         J       ",
            "                  V                                              ",
            "                                                                 ",
            "                                                                 ",
            " W                                                               ",
            "                                                                 ",
            "                   J                                             ",
            " B                           Y   X   Y                           ",
            "                                               J                 ",
            "                                                                 ",
            " B                                                               ",
            "                                                                 ",
            "                                                                 ",
            " B                                                               ",
            "                       V                                         ",
            "                                                                 ",
            "                                                                 ",
            "                                       B                         ",
            "                                                                 ",
            "                                                                 ",
            "              J                        B               V         ",
            "                                                                 ",
            "                                                                 ",
            "                                       B                         ",
            "                                                                 "
        ]

        self.floor_layout = []
        self.wall_layout = []

        for y, row in enumerate(self.layout):
            floor_row = []
            wall_row = []
            for x, tile in enumerate(row):
                # podlaha
                if tile in '.LRHTCD':
                    floor_row.append(random.randint(0, len(self.floor_tiles) - 1))
                else:
                    floor_row.append(-1)

                # steny
                if tile in self.random_wall_tiles:
                    wall_row.append(random.randint(0, len(self.random_wall_tiles[tile]) - 1))
                    self.walls.append(pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE,
                                                  self.TILE_SIZE, self.TILE_SIZE))
                # single steny
                elif tile in self.single_wall_tiles:
                    wall_row.append(0)
                    self.walls.append(pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE,
                                                  self.TILE_SIZE, self.TILE_SIZE))
                else:
                    wall_row.append(-1)

            self.floor_layout.append(floor_row)
            self.wall_layout.append(wall_row)

    def get_random_spawn_position(self):
        while True:
            x = random.randint(0, len(self.layout[0]) - 1) * self.TILE_SIZE
            y = random.randint(0, len(self.layout) - 1) * self.TILE_SIZE

            # tile pozicia
            tile_x = x // self.TILE_SIZE
            tile_y = y // self.TILE_SIZE

            # validacia pozicie
            if (tile_y < len(self.layout) and
                    tile_x < len(self.layout[tile_y]) and
                    self.layout[tile_y][tile_x] == '.'):

                test_rect = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)
                if not any(test_rect.colliderect(wall) for wall in self.walls):
                    return x, y

    def spawn_enemy(self):
        if len(self.enemies) < 10 and self.spawn_timer <= 0:
            spawn_pos = self.get_random_spawn_position()
            element = random.choice(["fire", "water", "ground", "air"])
            self.enemies.append(Enemy(*spawn_pos, element))
            self.spawn_timer = self.spawn_delay

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * self.player.speed
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * self.player.speed
        self.camera_x = self.player.rect.x - self.screen.get_width() // 2
        self.camera_y = self.player.rect.y - self.screen.get_height() // 2
        self.player.move(dx, dy, self.walls)
        if keys[pygame.K_ESCAPE]:
            return False

        # prepinanie elementov
        if keys[pygame.K_1]:
            self.player_element = "fire"
        elif keys[pygame.K_2]:
            self.player_element = "water"
        elif keys[pygame.K_3]:
            self.player_element = "ground"
        elif keys[pygame.K_4]:
            self.player_element = "air"

        # strielanie
        current_time = pygame.time.get_ticks()
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            target_x = mouse_x + self.camera_x
            target_y = mouse_y + self.camera_y
            self.projectiles.append(Projectile(
                self.player.rect.centerx,
                self.player.rect.centery,
                target_x,
                target_y,
                self.player_element
            ))
            self.last_shot_time = current_time
            self.can_shoot = False

        # cooldown pre strelbu
        if not self.can_shoot:
            if current_time - self.last_shot_time >= self.shoot_cooldown:
                self.can_shoot = True

        return True

    def update(self):
        # posunut nepriatelov
        for enemy in self.enemies[:]:
            enemy.move_towards_player(
                (self.player.rect.x, self.player.rect.y),
                self.walls,
                self.enemies
            )

        # posunut strely
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.hits_wall(self.walls):
                self.projectiles.remove(projectile)
            else:
                # kontrola zasahu
                for enemy in self.enemies[:]:
                    if projectile.rect.colliderect(enemy.rect):
                        if self.is_effective_against(projectile.element_type, enemy.element_type):
                            self.enemies.remove(enemy)
                        self.projectiles.remove(projectile)
                        break

        # spawn enemy
        self.spawn_timer -= 1
        self.spawn_enemy()

    def is_effective_against(self, attacker, defender):
        effectiveness = {
            "fire": "water",
            "water": "fire",
            "ground": "air",
            "air": "ground"
        }
        return effectiveness[attacker] == defender

    def draw(self):
        self.screen.fill((37, 19, 26))

        for y, row in enumerate(self.layout):
            for x, tile in enumerate(row):
                screen_x = x * self.TILE_SIZE - self.camera_x
                screen_y = y * self.TILE_SIZE - self.camera_y

                # Draw floor
                if self.floor_layout[y][x] != -1:
                    self.screen.blit(self.floor_tiles[self.floor_layout[y][x]], (screen_x, screen_y))

                # Draw walls
                if tile in self.random_wall_tiles:
                    self.screen.blit(self.random_wall_tiles[tile][self.wall_layout[y][x]], (screen_x, screen_y))
                elif tile in self.single_wall_tiles:
                    self.screen.blit(self.single_wall_tiles[tile], (screen_x, screen_y))

        for y, row in enumerate(self.decoration_layout):
            for x, decoration in enumerate(row):
                if decoration in self.decoration_tiles:
                    screen_x = x * self.TILE_SIZE - self.camera_x
                    screen_y = y * self.TILE_SIZE - self.camera_y
                    self.screen.blit(self.decoration_tiles[decoration], (screen_x, screen_y))

        # Draw player
        self.player.draw(self.screen, self.camera_x, self.camera_y)

        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x, self.camera_y)

        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(self.screen, self.camera_x, self.camera_y)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()