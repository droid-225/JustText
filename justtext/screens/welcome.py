import pygame
from .base import Screen
from ..constants import GREEN, WHITE, BLACK
from ..assets import load_font
from ..ui.text import TextRenderer

class Welcome(Screen):
    prevWidth = 0

    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)

    def draw(self, surface):
        self.text.reset_layout()
        self.text.draw(surface, "WELCOME", WHITE, new_line=False)