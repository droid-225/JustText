import pygame
from .base import Screen
from ..constants import WHITE, GREEN, BLACK
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..util.footer import Footer
from ..util.leveling import LevelCalculator
from ..util.itemUtil import *

class Shop(Screen): # main menu inherits from Screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot
        self.state.currentScreen = "shop"
        self.pickPrice = 50 + int((equip_get_level("pickaxe") - 1) * 10)
        self.stoneValue = get_base_value("stone")
        self.options = [f"(1) ({self.pickPrice}g) Upgrade Pickaxe [Requires Mining Level {equip_get_level("pickaxe") + 1}]",
                        f"(2) ({get_base_value("stone")}g) Sell Stone [{inv_count("stone")}]",
                        "(ESC) Go Back to Windhelm"]

    def handle_event(self, event):
        miningLevelCalc = LevelCalculator()
        miningLevel = miningLevelCalc.calculate_level(self.state.mining_xp)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and self.state.gold >= self.pickPrice and miningLevel >= (equip_get_level("pickaxe") + 1):
                self.state.gold -= self.pickPrice
            
                equip_levelup("pickaxe")
                self.pickPrice = 50 + int((equip_get_level("pickaxe") - 1) * 10)
                self.options = [f"(1) ({self.pickPrice}g) Upgrade Pickaxe [Requires Mining Level {equip_get_level("pickaxe") + 1}]",
                                f"(2) ({self.stoneValue}g) Sell Stone [{inv_count("stone")}]",
                                "(ESC) Go Back to Windhelm"]
            elif event.key == pygame.K_2 and inv_count("stone") > 0:
                inv_remove("stone", 1)
                self.state.gold += self.stoneValue
                self.options = [f"(1) ({self.pickPrice}g) Upgrade Pickaxe [Requires Mining Level {equip_get_level("pickaxe") + 1}]",
                                f"(2) ({self.stoneValue}g) Sell Stone [{inv_count("stone")}]",
                                "(ESC) Go Back to Windhelm"]
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
        self.text.draw(surface, "Welcome to the Shop!", GREEN, new_line=False)
        self.text.draw(surface, f"Your Gold: {gold}", WHITE)

        for option in self.options:
            self.text.draw(surface, option, WHITE)

        Footer(surface).draw()