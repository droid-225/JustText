import pygame
from .base import Screen
from ..constants import WHITE, GREEN, InventoryCategory
from ..items import ITEMS
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
        self.state.currentScreen = "inventory"
        self.prevScreen = self.state.prevScreen
        self.current_cat = InventoryCategory.ALL
        self.categories = [cat for cat in InventoryCategory]

    def get_filtered_items(self):
        # Returns items filtered by current category
        items = []
        for item_id, count in self.state.inventory.items():
            if count > 0 and ITEMS[item_id]:
                item = ITEMS[item_id]
                if (self.current_cat == InventoryCategory.ALL or item.type == self.current_cat.name.lower()):
                    items.append((item_id, item, count))
        return items

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.on_select(self.prevScreen)
                self.state.stamina += 1
            elif event.key == pygame.K_TAB:
                # Cycle through categories
                current_idx = self.categories.index(self.current_cat)
                next_idx = (current_idx + 1) % len(self.categories)
                self.current_cat = self.categories[next_idx]
            elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                # Use item in current slot
                items = self.get_filtered_items()
                idx = event.key - pygame.K_1
                if idx < len(items):
                    self.use_item(items[idx][0])

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
            self.text.draw(surface, f"{get_name(key)}: {inv_count(key)} [{get_type(key).capitalize()}]", WHITE, l_offset=15)
        self.text.addOffset("y", 6)

        self.text.draw(surface, f"Equipment:", GREEN)
        for key in equipment:
            self.text.draw(surface, f"({equip_current_durability(key)}/{equip_max_durability(key)}) {get_name(key)} Lv. {equip_get_level(key)} [{get_rarity(key).capitalize()}]", WHITE, l_offset=15)
        self.text.addOffset("y", 10)

        self.text.draw(surface, f"(ESC) Return to {prevScreen.capitalize()}", WHITE, alignment="bottom")