import pygame

from config import CELL_W, ROWS


class Hud:
    font: pygame.font.Font
    screen: pygame.Surface

    def __init__(self, screen):
        self.screen = screen
        self.center_font = pygame.font.Font(None, 48)
        self.count_font = pygame.font.Font(None, 24)

    def center_text(self, text: str):
        # img = self.font.render(text, True, (255, 255, 255))
        x = self.screen.get_width() // 2
        y = self.screen.get_height() // 2

        text_surface = self.center_font.render(
            text, True, (255, 255, 255)
        )
        text_rect = text_surface.get_rect(center=(x, y))

        self.screen.blit(text_surface, text_rect)

    def show_live_count(self, live_count: int):
        x = CELL_W
        y = CELL_W * (ROWS - 1 + 0.25)

        text_surface = self.count_font.render(
            f"Lives: {live_count}", True, (255, 255, 255)
        )
        self.screen.blit(text_surface, (x, y))

    def show_point_count(self, point_count: int):
        x = CELL_W * 6
        y = CELL_W * (ROWS - 1 + 0.25)

        text_surface = self.count_font.render(
            f"Points: {point_count}", True, (255, 255, 255)
        )
        self.screen.blit(text_surface, (x, y))
