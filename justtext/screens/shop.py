from ast import While
import pygame
from .base import Screen
from ..constants import WHITE, GREEN
from ..assets import load_font
from ..ui.text import TextRenderer
from ..state import get_state

class Shop(Screen): # main menu inherits from Screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot
        self.autoMinerPrice = 10
        self.options = ["(1) Sell Gold",
                        "(2) Upgrade Autominer (" + str(self.autoMinerPrice) + ")",
                        "(ESC) Go Back to Town"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: self.state.count -= 1
            elif event.key == pygame.K_2:
                if self.state.count >= self.autoMinerPrice:
                    self.state.autoMinerLevel += 1
                    self.state.count -= self.autoMinerPrice
                    self.autoMinerPrice *= 1.5 * self.state.autoMinerLevel
            elif event.key == pygame.K_ESCAPE: self.on_select("windhelm")

    def draw(self, surface):
        count = self.state.count

        self.text.reset_layout()
        self.text.draw(surface, "Welcome to the Shop!", GREEN, new_line=False)
        self.text.draw(surface, f"Your Gold: {count}", WHITE)

        for option in self.options:
            self.text.draw(surface, option, WHITE)