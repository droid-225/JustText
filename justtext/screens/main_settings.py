import pygame
from .base import Screen
from ..constants import WHITE, GREEN
from ..assets import load_font
from ..ui.text import TextRenderer

class Main_Settings(Screen):
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: self.on_select("main_menu")

    def draw(self, surface):
        self.text.reset_layout()
        self.text.draw(surface, "Main Settings Screen is Under Construction", GREEN, new_line=False)
        self.text.draw(surface, "(ESC) Return to Home Page", WHITE)