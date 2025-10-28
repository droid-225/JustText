import pygame
from .base import Screen
from ..constants import WHITE, GREEN, InventoryCategory
from ..items import ITEMS, Consumable
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..util.itemUtil import *
from ..components.inv_footer import InvFooter

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
        category_type_map = {
            InventoryCategory.MATERIALS: "material",
            InventoryCategory.CONSUMABLES: "consumable",
            InventoryCategory.TOOLS: "tool",
            InventoryCategory.ARMOR: "armor"
        }
        
        for item_id, count in self.state.inventory.items():
            if count > 0 and ITEMS[item_id]:
                item = ITEMS[item_id]
                if (self.current_cat == InventoryCategory.ALL or 
                    item.type == category_type_map.get(self.current_cat, "")):
                    items.append((item_id, item, count))
        return items

    def use_item(self, item_id: str) -> None:
        # Handle item usage
        item = ITEMS[item_id]
        
        if item.type != "consumable" or not item.consumable_effect:
            return
        
        if self.state.inventory[item_id] > 0:
            consumable = Consumable(item.consumable_effect)
            # Call the use method to apply the effects
            consumable.use(self.state)
            self.state.inventory[item_id] -= 1

            # Remove item if count reaches 0
            if self.state.inventory[item_id] <= 0:
                del self.state.inventory[item_id]

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
    
        self.text.reset_layout()
        
        # Draw header based on category
        header_text = {
            InventoryCategory.ALL: "<~~~~~~~~~~ Inventory ~~~~~~~~~~>",
            InventoryCategory.MATERIALS: "<~~~~~~~~~~ Materials ~~~~~~~~~~>",
            InventoryCategory.CONSUMABLES: "<~~~~~~~~~~ Consumables ~~~~~~~~~~>",
            InventoryCategory.TOOLS: "<~~~~~~~~~~ Tools ~~~~~~~~~~>",
            InventoryCategory.ARMOR: "<~~~~~~~~~~ Armor ~~~~~~~~~~>"
        }.get(self.current_cat, "<~~~~~~~~~~ Inventory ~~~~~~~~~~>")
        
        self.text.draw(surface, header_text, GREEN, new_line=False, alignment="middle")
        self.text.addOffset("y", 6)

        # Draw gold info
        self.text.draw(surface, f"Your Gold: {gold}", WHITE)
        self.text.addOffset("y", 6)

        # Get filtered items for current category
        items = self.get_filtered_items()
        
        if self.current_cat == InventoryCategory.ALL:
            # Show equipment section
            self.text.draw(surface, f"Equipment:", GREEN)
            for key in self.state.equipment:
                self.text.draw(surface, 
                    f"({equip_current_durability(key)}/{equip_max_durability(key)}) "
                    f"{get_name(key)} Lv. {equip_get_level(key)} [{get_rarity(key).capitalize()}]", 
                    WHITE, l_offset=15)
            self.text.addOffset("y", 6)
            
            # Show all items section
            self.text.draw(surface, f"Items:", GREEN)
            for key in self.state.inventory:
                self.text.draw(surface, 
                    f"{get_name(key)}: {inv_count(key)} [{get_type(key).capitalize()}]", 
                    WHITE, l_offset=15)
        
        elif self.current_cat == InventoryCategory.CONSUMABLES:
            # Show consumables with usage instructions
            self.text.draw(surface, "Available Consumables:", GREEN)
            for idx, (item_id, item, count) in enumerate(items):
                self.text.draw(surface, 
                    f"[{idx + 1}] {get_name(item_id)}: {count} "
                    f"[Restores: {item.consumable_effect.stamina if item.consumable_effect else 0} Stamina]", 
                    WHITE, l_offset=15)
        
        elif self.current_cat == InventoryCategory.TOOLS:
            # Show tools with durability
            self.text.draw(surface, "Tools & Equipment:", GREEN)
            for key in self.state.equipment:
                if get_type(key) == "tool":
                    self.text.draw(surface, 
                        f"{get_name(key)} Lv. {equip_get_level(key)} "
                        f"(Durability: {equip_current_durability(key)}/{equip_max_durability(key)})", 
                        WHITE, l_offset=15)
        
        else:
            # Show items of current category
            category_name = self.current_cat.name.capitalize()
            self.text.draw(surface, f"{category_name}:", GREEN)
            for item_id, item, count in items:
                self.text.draw(surface, 
                    f"{get_name(item_id)}: {count}", 
                    WHITE, l_offset=15)

        self.text.addOffset("y", 10)
        
        InvFooter(surface).draw()