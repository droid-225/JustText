import pygame
from .base import Screen
from ..constants import WHITE, GREEN
from ..assets import load_font
from ..ui.text import TextRenderer

class Main_Menu(Screen): # main menu inherits from Screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.options = ["(1) New Game", "(2) Load Game", "(3) Settings", "(ESC) Quit"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: self.on_select("new_game")
            elif event.key == pygame.K_2: self.on_select("load_game")
            elif event.key == pygame.K_3: self.on_select("main_settings")
            elif event.key == pygame.K_ESCAPE: self.on_select("quit")

    def draw(self, surface):
        self.text.reset_layout()
        self.text.draw(surface, "Welcome to Just Text!", GREEN, new_line=False)

        for option in self.options:
            self.text.draw(surface, option, WHITE)