import pygame
from .base import Screen
from ..constants import GREEN, WHITE
from ..assets import load_font

class New_Game(Screen):
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: self.on_select("main_menu")

    def draw(self, surface):
        y_margin = x_margin = 0

        placeholder = self.font.render("New Game Screen is Under Construction", 1, GREEN)
        y_margin = x_margin = placeholder.get_height()
        surface.blit(placeholder, (x_margin, y_margin))

        return_prompt = self.font.render("(1) Return to Home", 1, WHITE)
        y_margin += 10 + return_prompt.get_height()
        surface.blit(return_prompt, (x_margin, y_margin))
