import pygame
from pygame import Surface

class ShopItem:
    def __init__(self, name: str, description: str, cost: int, max_level: int, icon_path: str):
        self.name = name
        self.description = description
        self.cost = cost
        self.level = 0
        self.max_level = max_level
        self.base_cost = cost
        self.icon = pygame.transform.scale(
            pygame.image.load(icon_path).convert_alpha(),
            (48, 48)
        )

    def get_current_cost(self) -> int:
        if self.name == "Healing":
            return self.base_cost
        else:
            return self.base_cost * (self.level + 1)

    def can_upgrade(self, coins: int) -> bool:
        if self.name == "Healing":
            return coins >= self.base_cost
        return self.level < self.max_level and coins >= self.get_current_cost()

    def get_effect_description(self) -> str:
        effects = {
            "Fire Rate": f"-{self.level * 20}% Cooldown",
            "Max Health": f"+{self.level} HP",
            "Movement Speed": f"+{self.level * 10}% Speed",
            "Healing": "Restore Full HP"
        }
        return effects.get(self.name, "")

class Shop:
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.background_color = (37, 19, 26)  # #25131A
        self.gold_color = (255, 215, 0)
        self.silver_color = (192, 192, 192)

        self.title_font = pygame.font.Font(None, 64)
        self.item_font = pygame.font.Font(None, 36)
        self.desc_font = pygame.font.Font(None, 24)

        self.items = [
            ShopItem("Fire Rate", "Decrease time between shots", 2, 3, "assets/projectiles/Fire1.png"),
            ShopItem("Max Health", "Increase maximum health", 2, 3, "assets/HUD/health_bar1.png"),
            ShopItem("Movement Speed", "Increase movement speed", 2, 3, "assets/characters/Player.png"),
            ShopItem("Healing", "Restore health to maximum", 2, 4, "assets/decorations/coin.png")
        ]

        # Selected item
        self.selected_index = 0

        self.continue_button = pygame.Rect(
            screen_width // 2 - 100,
            screen_height - 100,
            200,
            50
        )

        self.confirm_button = pygame.Rect(
            screen_width // 2 - 100,
            screen_height - 150,
            200,
            50
        )

    def draw(self, screen: Surface, coins: int, current_health: int, max_health: int):
        screen.fill(self.background_color)

        title = self.title_font.render("Shop", True, self.gold_color)
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 50))

        coins_text = self.item_font.render(f"Coins: {coins}", True, self.gold_color)
        screen.blit(coins_text, (50, 50))

        health_text = self.item_font.render(f"Health: {current_health}/{max_health}", True, self.silver_color)
        screen.blit(health_text, (50, 90))

        for i, item in enumerate(self.items):
            y_pos = 150 + i * 120
            container_rect = pygame.Rect(self.screen_width // 2 - 300, y_pos, 600, 100)

            if i == self.selected_index:
                pygame.draw.rect(screen, (60, 30, 45), container_rect)
                pygame.draw.rect(screen, self.gold_color, container_rect, 2)
            else:
                pygame.draw.rect(screen, (45, 25, 35), container_rect)
                pygame.draw.rect(screen, self.silver_color, container_rect, 1)

            screen.blit(item.icon, (container_rect.x + 10, container_rect.y + 26))

            name_text = self.item_font.render(
                f"{item.name} (Level {item.level}/{item.max_level})",
                True,
                self.gold_color
            )
            screen.blit(name_text, (container_rect.x + 70, container_rect.y + 10))

            desc_text = self.desc_font.render(item.description, True, self.silver_color)
            screen.blit(desc_text, (container_rect.x + 70, container_rect.y + 40))

            effect_text = self.desc_font.render(item.get_effect_description(), True, self.silver_color)
            screen.blit(effect_text, (container_rect.x + 70, container_rect.y + 65))

            if item.level < item.max_level:
                cost_text = self.item_font.render(
                    f"Cost: {item.get_current_cost()}",
                    True,
                    self.gold_color if coins >= item.get_current_cost() else (150, 150, 150)
                )
                screen.blit(cost_text, (container_rect.right - cost_text.get_width() - 20, container_rect.y + 35))
            elif item.name != "Healing":
                max_text = self.item_font.render("MAX", True, self.gold_color)
                screen.blit(max_text, (container_rect.right - max_text.get_width() - 20, container_rect.y + 35))

        pygame.draw.rect(screen, (60, 30, 45), self.confirm_button)
        pygame.draw.rect(screen, self.gold_color, self.confirm_button, 2)
        confirm_text = self.item_font.render("Confirm", True, self.gold_color)
        screen.blit(confirm_text, confirm_text.get_rect(center=self.confirm_button.center))

        pygame.draw.rect(screen, (60, 30, 45), self.continue_button)
        pygame.draw.rect(screen, self.gold_color, self.continue_button, 2)
        continue_text = self.item_font.render("Continue", True, self.gold_color)
        text_rect = continue_text.get_rect(center=self.continue_button.center)
        screen.blit(continue_text, text_rect)

    def handle_input(self, event: pygame.event.Event, game, coins: int) -> tuple[bool, int]:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif event.key == pygame.K_SPACE:
                return self.process_purchase(game, coins)
            return False, coins

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.confirm_button.collidepoint(mouse_pos):
                return self.process_purchase(game, coins)

            if self.continue_button.collidepoint(mouse_pos):
                return True, coins

            for i, item in enumerate(self.items):
                item_rect = pygame.Rect(
                    self.screen_width // 2 - 300,
                    150 + i * 120,
                    600,
                    100
                )
                if item_rect.collidepoint(mouse_pos):
                    self.selected_index = i
                    return False, coins
        return False, coins

    def process_purchase(self, game, coins):
        item = self.items[self.selected_index]

        if item.name == "Healing":
            healing_cost = 2
            if (game.player.current_health < game.player.max_health
                    and coins >= healing_cost):
                coins -= healing_cost
                game.player.current_health = game.player.max_health
        else:
            if item.can_upgrade(coins):
                coins -= item.get_current_cost()
                item.level += 1
                self.apply_upgrade(item, game)

        return False, coins

    def apply_upgrade(self, item: ShopItem, game):
        if item.name == "Fire Rate":
            game.fire_rate_level = item.level
            game.base_shoot_cooldown = int(300 * (1 - game.fire_rate_level * 0.2))
        elif item.name == "Max Health":
            game.max_health_level = item.level
            game.player.max_health = 3 + game.max_health_level
            game.player.current_health = game.player.max_health
        elif item.name == "Movement Speed":
            game.movement_speed_level = item.level
            game.player.speed = game.player.base_speed * (1 + game.movement_speed_level * 0.1)
