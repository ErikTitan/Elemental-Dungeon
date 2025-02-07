import math
import time
import pygame
from player import Player
from enemy import Enemy
from projectile import Projectile
import random
from game_settings import GameSettings

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        screen_info = pygame.display.Info()
        self.screen = pygame.display.set_mode((screen_info.current_w, screen_info.current_h), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.settings = GameSettings()

        # attributes from settings
        self.TILE_SIZE = self.settings.TILE_SIZE
        self.floor_tiles = self.settings.floor_tiles
        self.random_wall_tiles = self.settings.random_wall_tiles
        self.single_wall_tiles = self.settings.single_wall_tiles
        self.decoration_tiles = self.settings.decoration_tiles
        self.health_bars = self.settings.health_bars
        self.element_indicators = self.settings.element_indicators
        self.hit_sound = self.settings.hit_sound
        self.shoot_sounds = self.settings.shoot_sounds
        self.background_music = self.settings.background_music
        self.layout = self.settings.layout
        self.decoration_layout = self.settings.decoration_layout
        self.effectiveness = self.settings.get_element_effectiveness()

        # Game state
        self.game_duration = self.settings.GAME_DURATION
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 48)
        self.game_started = False
        self.game_over = False
        self.game_won = False

        # Level progression
        self.has_key = False
        self.key_position = None
        self.ladder_position = None
        self.ladder_cover_position = None
        self.conditions = self.settings.get_key_spawn_conditions()

        self.background_music.play(loops=-1)
        self.create_map()
        self.player = Player(3 * self.TILE_SIZE, 3 * self.TILE_SIZE)
        self.camera_x = 0
        self.camera_y = 0

        # Enemy and projectile settings
        self.enemies = []
        self.projectiles = []
        self.player_element = "fire"
        self.spawn_timer = 0
        self.spawn_delay = self.settings.SPAWN_DELAY
        self.can_shoot = True
        self.shoot_cooldown = self.settings.SHOOT_COOLDOWN
        self.last_shot_time = 0

        self.reset_game()

    def create_map(self):
        self.layout = self.settings.layout
        self.decoration_layout = self.settings.decoration_layout

        self.floor_layout, self.wall_layout, self.walls = self.settings.generate_floor_wall_layouts()

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

    def spawn_key(self):
        valid_positions = []
        for y, row in enumerate(self.layout):
            for x, tile in enumerate(row):
                if tile == '.':
                    world_x, world_y = x * self.TILE_SIZE, y * self.TILE_SIZE
                    distance = math.sqrt((world_x - self.player.rect.x) ** 2 + (world_y - self.player.rect.y) ** 2)
                    if self.conditions['min_distance'] <= distance <= self.conditions['max_distance']:
                        valid_positions.append((world_x, world_y))

        if valid_positions:
            self.key_position = random.choice(valid_positions)
        else:
            return

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if not self.game_over:
            dx = (keys[pygame.K_d] - keys[pygame.K_a]) * self.player.speed
            dy = (keys[pygame.K_s] - keys[pygame.K_w]) * self.player.speed
            self.camera_x = self.player.rect.x - self.screen.get_width() // 2
            self.camera_y = self.player.rect.y - self.screen.get_height() // 2
            self.player.move(dx, dy, self.walls)

        # start screen
        if not self.game_started:
            if any(keys):
                self.game_started = True
                return True
            return True

        # end screen
        if self.game_over:
            if keys[pygame.K_ESCAPE]:
                return False
            if keys[pygame.K_r]:
                self.reset_game()
                return True
            return True

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

            self.shoot_sounds[self.player_element].play()

            self.last_shot_time = current_time
            self.can_shoot = False

        # cooldown pre strelbu
        if not self.can_shoot:
            if current_time - self.last_shot_time >= self.shoot_cooldown:
                self.can_shoot = True

        return True

    def update(self):
        if not self.game_started or self.game_over:
            return

        # update hraca
        self.player.update()
        self.player.apply_knockback(self.walls)

        # player-enemy kolizia
        if self.player.is_alive:
            for enemy in self.enemies[:]:
                if self.player.rect.colliderect(enemy.rect):
                    enemy_pos = (enemy.rect.centerx, enemy.rect.centery)
                    if self.player.take_damage(enemy_pos):
                        self.hit_sound.play()
                    if not self.player.is_alive:
                        self.end_game()
                        break

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
                        if self.effectiveness[projectile.element_type] == enemy.element_type:
                            self.coins.append((enemy.rect.x, enemy.rect.y))
                            self.enemies.remove(enemy)
                        self.projectiles.remove(projectile)
                        break

        # key collect
        if self.key_position:
            key_rect = pygame.Rect(self.key_position[0], self.key_position[1], self.TILE_SIZE, self.TILE_SIZE)
            if self.player.rect.colliderect(key_rect):
                self.has_key = True
                self.key_position = None

        # coin collect
        for coin in self.coins[:]:
            coin_rect = pygame.Rect(coin[0], coin[1], self.TILE_SIZE, self.TILE_SIZE)
            if self.player.rect.colliderect(coin_rect):
                self.coin_count += 1
                self.coins.remove(coin)

        # odomknutie ladder_cover
        if self.ladder_cover_position and self.has_key:
            cover_rect = pygame.Rect(self.ladder_cover_position[0], self.ladder_cover_position[1], self.TILE_SIZE,
                                     self.TILE_SIZE)
            if self.player.rect.colliderect(cover_rect):
                self.has_key = False
                self.ladder_cover_removed_time = time.time()
                self.ladder_cover_position = None

        # ladder vstup
        if self.ladder_cover_removed_time and (time.time() - self.ladder_cover_removed_time >= 2):
            ladder_rect = pygame.Rect(self.ladder_position[0], self.ladder_position[1], self.TILE_SIZE, self.TILE_SIZE)
            if self.player.rect.colliderect(ladder_rect):
                self.progress_to_next_level()

        # spawn enemy
        self.spawn_timer -= 1
        self.spawn_enemy()

    def update_timer(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        remaining_time = max(0, self.game_duration - elapsed_time)

        if remaining_time == 0 and not self.game_over:
            self.end_game()

        return remaining_time

    def progress_to_next_level(self):
        if self.settings.progress_level():
            self.reset_game()
        else:
            self.win_game()

    def win_game(self):
        self.game_over = True
        self.game_won = True
        self.background_music.stop()

    def end_game(self):
        self.game_over = True
        self.background_music.stop()
        self.player.is_alive = False

    def reset_game(self):
        self.create_map()
        self.game_over = False
        self.start_time = pygame.time.get_ticks()
        self.player = Player(3 * self.TILE_SIZE, 3 * self.TILE_SIZE)
        self.camera_x = 0
        self.camera_y = 0
        self.enemies = []
        self.projectiles = []
        self.player_element = "fire"
        self.spawn_timer = 0
        self.spawn_delay = 180
        self.can_shoot = True
        self.shoot_cooldown = 300
        self.last_shot_time = 0

        # key and coin spawn
        self.has_key = False
        self.key_position = None
        self.coins = []
        self.coin_count = 0
        self.ladder_cover_removed_time = None
        self.spawn_key()

        # ladder cover
        for y, row in enumerate(self.decoration_layout):
            for x, decoration in enumerate(row):
                if decoration == 'Z':
                    self.ladder_cover_position = (x * self.TILE_SIZE, y * self.TILE_SIZE)

        # ladder pozicia
        for y, row in enumerate(self.layout):
            for x, tile in enumerate(row):
                if tile == 'Q':
                    self.ladder_position = (x * self.TILE_SIZE, y * self.TILE_SIZE)

        self.background_music.stop()
        self.background_music.play(loops=-1)

    def draw(self):
        self.screen.fill((37, 19, 26))

        # start screen
        if not self.game_started:
            font = pygame.font.Font(None, 74)
            title_text = font.render('Elemental Dungeon', True, (255, 255, 255))
            start_text = font.render('Press Any Key to Start', True, (255, 255, 255))
            controls_font = pygame.font.Font(None, 48)  # Using existing font size

            # Controls text
            move_text = controls_font.render('WASD - Move Character', True, (255, 255, 255))
            element_text = controls_font.render('1-4 - Switch Elements', True, (255, 255, 255))
            shoot_text = controls_font.render('Left Mouse Button - Shoot', True, (255, 255, 255))

            # Position calculations
            title_rect = title_text.get_rect(center=(self.screen.get_width() // 2,
                                                     self.screen.get_height() // 2 - 150))
            start_rect = start_text.get_rect(center=(self.screen.get_width() // 2,
                                                     self.screen.get_height() // 2 - 50))
            move_rect = move_text.get_rect(center=(self.screen.get_width() // 2,
                                                   self.screen.get_height() // 2 + 50))
            element_rect = element_text.get_rect(center=(self.screen.get_width() // 2,
                                                         self.screen.get_height() // 2 + 100))
            shoot_rect = shoot_text.get_rect(center=(self.screen.get_width() // 2,
                                                     self.screen.get_height() // 2 + 150))

            self.screen.blit(title_text, title_rect)
            self.screen.blit(start_text, start_rect)
            self.screen.blit(move_text, move_rect)
            self.screen.blit(element_text, element_rect)
            self.screen.blit(shoot_text, shoot_rect)

            pygame.display.flip()
            return

        # mapa
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

        # dekoracie
        for y, row in enumerate(self.decoration_layout):
            for x, decoration in enumerate(row):
                if decoration in self.decoration_tiles:
                    screen_x = x * self.TILE_SIZE - self.camera_x
                    screen_y = y * self.TILE_SIZE - self.camera_y
                    self.screen.blit(self.decoration_tiles[decoration], (screen_x, screen_y))

        # kluc
        if self.key_position:
            screen_x = self.key_position[0] - self.camera_x
            screen_y = self.key_position[1] - self.camera_y
            self.screen.blit(self.decoration_tiles['K'], (screen_x, screen_y))

        # coin
        for coin in self.coins:
            screen_x = coin[0] - self.camera_x
            screen_y = coin[1] - self.camera_y
            self.screen.blit(self.decoration_tiles['C'], (screen_x, screen_y))

        # ladder
        if self.ladder_cover_position:
            screen_x = self.ladder_cover_position[0] - self.camera_x
            screen_y = self.ladder_cover_position[1] - self.camera_y
            self.screen.blit(self.decoration_tiles['Z'], (screen_x, screen_y))

        # ladder cover
        if self.ladder_position and not self.ladder_cover_position:
            screen_x = self.ladder_position[0] - self.camera_x
            screen_y = self.ladder_position[1] - self.camera_y
            self.screen.blit(self.decoration_tiles['Q'], (screen_x, screen_y))

        if not self.game_over:
            # Draw player
            self.player.draw(self.screen, self.camera_x, self.camera_y)

            # Draw enemies
            for enemy in self.enemies:
                enemy.draw(self.screen, self.camera_x, self.camera_y)

            # Draw projectiles
            for projectile in self.projectiles:
                projectile.draw(self.screen, self.camera_x, self.camera_y)

            # Timer
            remaining_time = self.update_timer()
            timer_text = self.font.render(f"Time: {remaining_time}", True, (255, 255, 255))
            self.screen.blit(timer_text, (20, 100))

            # Element indicator
            current_element = self.element_indicators[self.player_element]
            element_text = self.font.render("Current Element:", True, (255, 255, 255))
            self.screen.blit(element_text, (20, 150))
            self.screen.blit(current_element, (300, 150))

            # Draw health bar
            if self.player.is_alive and not self.game_over:
                current_health_bar = self.health_bars[self.player.current_health - 1]
                self.screen.blit(current_health_bar, (10, -90))

            # Draw coin counter
            coin_text = self.font.render(f"Coins: {self.coin_count}", True, (255, 255, 0))
            self.screen.blit(coin_text, (20, 200))

            # Key indicator
            if self.has_key:
                self.screen.blit(self.decoration_tiles['K'], (10, 220))

        # Game over
        if self.game_over and not self.game_won:
            font = pygame.font.Font(None, 74)
            game_over_text = font.render('Game Over', True, (255, 0, 0))
            text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2,
                                                        self.screen.get_height() // 2))
            self.screen.blit(game_over_text, text_rect)

            instruction_font = pygame.font.Font(None, 36)
            quit_text = instruction_font.render('Press ESC to quit', True, (255, 255, 255))
            restart_text = instruction_font.render('Press R to restart', True, (255, 255, 255))

            quit_rect = quit_text.get_rect(center=(self.screen.get_width() // 2,
                                                   self.screen.get_height() // 2 + 50))
            restart_rect = restart_text.get_rect(center=(self.screen.get_width() // 2,
                                                         self.screen.get_height() // 2 + 90))

            self.screen.blit(quit_text, quit_rect)
            self.screen.blit(restart_text, restart_rect)

        if self.game_over and self.game_won:
            font = pygame.font.Font(None, 74)
            win_text = font.render('Congratulations!', True, (0, 255, 0))
            text_rect = win_text.get_rect(center=(self.screen.get_width() // 2,
                                                  self.screen.get_height() // 2))
            self.screen.blit(win_text, text_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEWHEEL:
                    elements = ["fire", "water", "ground", "air"]
                    current_index = elements.index(self.player_element)
                    if event.y > 0:  # Scroll up
                        self.player_element = elements[(current_index + 1) % len(elements)]
                    elif event.y < 0:  # Scroll down
                        self.player_element = elements[(current_index - 1) % len(elements)]

            running = self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        pygame.mixer.quit()

if __name__ == "__main__":
    game = Game()
    game.run()