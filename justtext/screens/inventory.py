import pygame
from .base import Screen
from ..constants import WHITE, GREEN
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..util.itemUtil import *

class Inventory(Screen):
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot
        self.state.currentScreen = "inventory"
        self.state.save()
        self.prevScreen = self.state.prevScreen

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.on_select(self.prevScreen)

    def draw(self, surface):
        gold = self.state.gold
        prevScreen = self.prevScreen
        state = self.state
        inventory = state.inventory
        equipment = state.equipment
    
        self.text.reset_layout()
        self.text.draw(surface, "<~~~~~~~~~~ Inventory ~~~~~~~~~~>", GREEN, new_line=False, alignment="middle")
        self.text.addOffset("y", 6)

        self.text.draw(surface, f"Your Gold: {gold}", WHITE)
        self.text.addOffset("y", 6)

        self.text.draw(surface, f"Items:", GREEN)
        for key in inventory:
            self.text.draw(surface, f"{get_name(key)}: {inv_count(key)}", WHITE, l_offset=15)
        self.text.addOffset("y", 6)

        self.text.draw(surface, f"Equipment:", GREEN)
        for key in equipment:
            self.text.draw(surface, f"[{equip_current_durability(key)}/{equip_max_durability(key)}] {get_name(key)} Lv. {equip_get_level(key)} {get_rarity(key)}", WHITE, l_offset=15)
        self.text.addOffset("y", 10)

        self.text.draw(surface, f"(ESC) Return to {prevScreen.capitalize()}", WHITE)