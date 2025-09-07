import pygame
from .base import Screen
from ..constants import WHITE, GREEN
from ..assets import load_font

class Main_Menu(Screen): # main menu inherits from Screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.options = ["(1) New Game", "(2) Load Game", "(3) Settings", "(4) Quit"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: self.on_select("new_game")
            elif event.key == pygame.K_2: self.on_select("load_game")
            elif event.key == pygame.K_3: self.on_select("main_settings")
            elif event.key == pygame.K_4: self.on_select("quit")

    def draw(self, surface):
        y_margin = x_margin = 0

        title = self.font.render("Welcome to Just Text!", 1, GREEN)
        y_margin = x_margin = title.get_height()
        surface.blit(title, (x_margin, y_margin))

        for option in self.options:
            text = self.font.render(option, 1, WHITE)
            y_margin += 10 + text.get_height()
            surface.blit(text, (x_margin, y_margin))