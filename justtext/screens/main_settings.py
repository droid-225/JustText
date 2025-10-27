import pygame
from .base import Screen
from ..constants import WHITE, GREEN
from ..assets import load_font
from ..util.text import TextRenderer
from ..components.options import Options
from ..state import get_state

class Main_Settings(Screen):
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.options = [
            "(ESC) Return to Home Page"
        ]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.on_select("main_menu")

    def draw(self, surface):
        self.text.reset_layout()
        self.text.draw(surface, "<~~~~~~~~~~ Settings ~~~~~~~~~~>", GREEN, new_line=False, alignment="middle")
        self.text.addOffset("y", 6)

        Options(surface).draw(self.options)