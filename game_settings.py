import pygame
import random

from levels import LevelData


class GameSettings:
    def __init__(self):
        # Base settings
        self.BASE_TILE_SIZE = 16
        self.TILE_SIZE = 64

        # Game settings
        self.GAME_DURATION = 60
        self.MAX_ENEMIES = 10
        self.SPAWN_DELAY = 180
        self.SHOOT_COOLDOWN = 300

        # Audio settings
        self.BACKGROUND_MUSIC_VOLUME = 0
        self.HIT_SOUND_VOLUME = 0.6

        # Initialize assets
        self.load_tiles()
        self.load_audio()
        self.load_hud()
        self.level_data = LevelData()
        self.create_layouts()


    def load_tiles(self):
        # Floor tiles
        self.floor_tiles = [
            pygame.transform.scale(
                pygame.image.load(f"assets/map/floor{i}.png"),
                (self.TILE_SIZE, self.TILE_SIZE)
            ) for i in range(1, 5)
        ]

        # Wall tiles
        self.random_wall_tiles = {
            'T': [pygame.transform.scale(pygame.image.load(f"assets/map/wall{i}.png"),
                                         (self.TILE_SIZE, self.TILE_SIZE)) for i in range(1, 5)],
            'H': [pygame.transform.scale(pygame.image.load(f"assets/map/wall_half{i}.png"),
                                         (self.TILE_SIZE, self.TILE_SIZE)) for i in range(1, 3)]
        }

        # Single wall tiles
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

        # Decoration tiles
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
            'C': pygame.transform.scale(pygame.image.load("assets/decorations/coin.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
        }

        self.decoration_tiles.update({
            'K': pygame.transform.scale(pygame.image.load("assets/decorations/key.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            'Q': pygame.transform.scale(pygame.image.load("assets/map/ladder.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE)),
            'Z': pygame.transform.scale(pygame.image.load("assets/decorations/ladder_cover.png"),
                                        (self.TILE_SIZE, self.TILE_SIZE))
        })

    def load_audio(self):
        self.hit_sound = pygame.mixer.Sound("assets/audio/Hit.wav")
        self.hit_sound.set_volume(self.HIT_SOUND_VOLUME)

        self.shoot_sounds = {
            "fire": pygame.mixer.Sound("assets/audio/Fire.wav"),
            "water": pygame.mixer.Sound("assets/audio/Water.wav"),
            "ground": pygame.mixer.Sound("assets/audio/Ground.wav"),
            "air": pygame.mixer.Sound("assets/audio/Air.wav")
        }

        self.coin_sound = pygame.mixer.Sound("assets/audio/Coin.wav")
        self.cover_sound = pygame.mixer.Sound("assets/audio/Cover.wav")

        self.background_music = pygame.mixer.Sound("assets/audio/Background.wav")
        self.background_music.set_volume(self.BACKGROUND_MUSIC_VOLUME)

    def load_hud(self):
        # Health bars
        health_bar_width = 410
        health_bar_height = 355
        self.health_bars = [
            pygame.transform.scale(
                pygame.image.load(f"assets/HUD/health_bar{i}.png"),
                (health_bar_width, health_bar_height)
            ) for i in range(1, 4)
        ]

        # Element indicators
        self.element_indicators = {
            "fire": pygame.transform.scale(pygame.image.load("assets/projectiles/Fire1.png"), (96, 36)),
            "water": pygame.transform.scale(pygame.image.load("assets/projectiles/Water1.png"), (96, 36)),
            "ground": pygame.transform.scale(pygame.image.load("assets/projectiles/Ground1.png"), (96, 36)),
            "air": pygame.transform.scale(pygame.image.load("assets/projectiles/Air1.png"), (96, 36))
        }

    def create_layouts(self):
        current_level = self.level_data.get_current_level()
        self.layout = current_level['layout']
        self.decoration_layout = current_level['decoration_layout']

    def progress_level(self):
        if self.level_data.next_level():
            self.create_layouts()
            return True
        return False

    def get_element_effectiveness(self):
        return {
            "fire": "water",
            "water": "fire",
            "ground": "air",
            "air": "ground"
        }

    def generate_floor_wall_layouts(self):
        floor_layout = []
        wall_layout = []
        walls = []

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
                    walls.append(pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE,
                                             self.TILE_SIZE, self.TILE_SIZE))
                # single steny
                elif tile in self.single_wall_tiles:
                    wall_row.append(0)
                    walls.append(pygame.Rect(x * self.TILE_SIZE, y * self.TILE_SIZE,
                                             self.TILE_SIZE, self.TILE_SIZE))
                else:
                    wall_row.append(-1)

            floor_layout.append(floor_row)
            wall_layout.append(wall_row)

        return floor_layout, wall_layout, walls

    def get_key_spawn_conditions(self):
        return {
            'min_distance': 20 * self.TILE_SIZE,
            'max_distance': 70 * self.TILE_SIZE
        }