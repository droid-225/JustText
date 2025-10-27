import pygame
from .base import Screen
from ..constants import GREEN
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..components.footer import Footer
from ..util.itemUtil import *
from ..components.options import Options

class Blacksmith(Screen): # main menu inherits from Screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot
        self.state.currentScreen = "blacksmith"
        self.state.save()
        self.curr_pick_dura = equip_current_durability("pickaxe")
        self.max_pick_dura = equip_max_durability("pickaxe")
        self.repairPrice = self.max_pick_dura - self.curr_pick_dura 
        self.options = [f"(1) ({self.repairPrice}g) Repair Pickaxe",
                        "(ESC) Go Back to Windhelm"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and self.state.gold >= self.repairPrice:
                self.state.gold -= self.repairPrice
                equip_full_repair("pickaxe")
                self.curr_pick_dura = equip_current_durability("pickaxe")
                self.repairPrice = self.max_pick_dura - self.curr_pick_dura 
                self.options = [f"(1) ({self.repairPrice}g) Repair Pickaxe",
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
        self.text.draw(surface, "<<<<<\<<<<</BLACKSMITH\>>>>>/>>>>>", GREEN, new_line=False, alignment="middle")
        self.text.addOffset("y", 6)
        self.text.draw(surface, f"Your Gold: {gold}", l_offset=10)
        self.text.addOffset("y", 6)

        Options(surface).draw(self.options, yOffset=50)

        Footer(surface).draw()