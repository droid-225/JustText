from ast import While
import pygame
from .base import Screen
from ..constants import WHITE, GREEN, BLACK
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
        self.state.currentScreen = "shop"
        self.autoMinerPrice = 10 + int(5 * (self.state.autoMinerLevel - 1))
        self.options = ["(1) Sell Gold",
                        "(2) Upgrade Autominer (" + str(self.autoMinerPrice) + "g)",
                        "(ESC) Go Back to Windhelm"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: self.state.gold -= 1
            elif event.key == pygame.K_2:
                if self.state.gold >= self.autoMinerPrice:
                    self.state.autoMinerLevel += 1
                    self.state.gold -= self.autoMinerPrice
                    self.autoMinerPrice = 10 + int(5 * (self.state.autoMinerLevel - 1))
                    self.options = ["(1) Sell Gold",
                                    "(2) Upgrade Autominer (" + str(self.autoMinerPrice) + "g)",
                                    "(ESC) Go Back to Town"]
            elif event.key == pygame.K_ESCAPE: self.on_select("windhelm")

    def draw(self, surface):
        gold = self.state.gold

        self.text.reset_layout()
        self.text.draw(surface, "Welcome to the Shop!", GREEN, new_line=False)
        self.text.draw(surface, f"Your Gold: {gold}", WHITE)

        for option in self.options:
            self.text.draw(surface, option, WHITE)

        # Inventory Screen
        inv = self.font.render("(I) Inventory", True, WHITE, BLACK)
        surface.blit(inv, (10, surface.get_height() - inv.get_height() - 6))