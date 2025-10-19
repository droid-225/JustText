import pygame
from .base import Screen
from ..constants import WHITE, GREEN, BLACK
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..util.footer import Footer
from ..util.leveling import LevelCalculator
from ..util.itemUtil import *

class Inn(Screen): # main menu inherits from Screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot
        self.state.currentScreen = "inn"
        self.state.save()
        self.options = ["(1) (10g) Book Room",
                        "(2) (50g) Book Cozy Room",
                        "(3) (100g) Book Luxury Room",
                        "(ESC) Go Back to Windhelm"]

    def handle_event(self, event):
        miningLevelCalc = LevelCalculator(base_xp=10)
        miningLevel = miningLevelCalc.calculate_level(self.state.mining_xp)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and self.state.gold >= 10:
                self.state.gold -= 10
                self.state.stamina += 20
            if event.key == pygame.K_2 and self.state.gold >= 50:
                self.state.gold -= 50
                self.state.stamina += 100
            if event.key == pygame.K_3 and self.state.gold >= 100:
                self.state.gold -= 100
                self.state.stamina += 200
            elif event.key == pygame.K_ESCAPE: self.on_select("windhelm")
            elif event.key == pygame.K_i or event.key == pygame.key.key_code("I"):
                self.state.prevScreen = self.state.currentScreen
                self.state.save()
                self.on_select("inventory")
            elif event.key == pygame.K_u or event.key == pygame.key.key_code("U"):
                self.state.prevScreen = self.state.currentScreen
                self.state.save()
                self.on_select("stats")

    def draw(self, surface):
        gold = self.state.gold

        self.text.reset_layout()
        self.text.draw(surface, "Welcome to the Inn!", GREEN, new_line=False, alignment="middle")
        self.text.addOffset("y", 6)
        self.text.draw(surface, f"Your Gold: {gold}", l_offset=10)
        self.text.addOffset("y", 6)

        for option in self.options:
            self.text.draw(surface, option, WHITE)

        Footer(surface).draw()