import pygame
from .base import Screen
from ..constants import GREEN
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..components.footer import Footer
from ..util.leveling import LevelCalculator
from ..util.itemUtil import *
from ..components.options import Options

class Shop(Screen): # main menu inherits from Screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot
        self.state.currentScreen = "shop"
        self.state.save()
        self.surface = None
        self.pickPrice = 50 + int((equip_get_level("pickaxe") - 1) * 10)
        self.stoneValue = get_base_value("stone")
        self.options = []
        # tabs: "buy" or "sell"
        self.current_tab = "buy"
        self.sell_items = []  # cached list of sellable (id, name, qty, value)
        self.refresh_options()

    def refresh_options(self):
        # recompute dynamic values
        self.pickPrice = 50 + int((equip_get_level("pickaxe") - 1) * 10)
        self.stoneValue = get_base_value("stone")
        
        # build the options list
        self.options = [
            "(1) (10g) Buy Bread",
            "(TAB) Switch to Selling",
            "(ESC) Go Back to Windhelm",
        ]

    def build_sell_list(self):
        """Build a list of sellable items from player's inventory.
        Each entry is a tuple (item_id, display_name, qty, unit_value).
        """
        self.sell_items = []
        for item_id, qty in list(self.state.inventory.items()):
            if qty <= 0:
                continue
            # Only list items that have a base value > 0
            try:
                val = get_base_value(item_id)
            except Exception:
                # If an item has no defined value, skip it
                continue

            if val > 0:
                name = get_name(item_id)
                self.sell_items.append((item_id, name, qty, val))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # TAB toggles Buy/Sell
            if event.key == pygame.K_TAB:
                self.current_tab = "sell" if self.current_tab == "buy" else "buy"
                # rebuild sell list when switching to it
                if self.current_tab == "sell":
                    self.build_sell_list()
                self.update(0)
                return

            # If in sell tab, numeric keys map to inventory items
            if self.current_tab == "sell" and event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                idx = event.key - pygame.K_1
                if idx < len(self.sell_items):
                    item_id, name, qty, val = self.sell_items[idx]
                    # sell one unit
                    if qty > 0:
                        inv_remove(item_id, 1)
                        self.state.gold += val
                    # rebuild list and refresh
                    self.build_sell_list()
                    self.update(0)
                return

            if event.key == pygame.K_1 and self.current_tab == "buy" and self.state.gold >= 10:
                self.state.gold -= 10
                inv_add("bread", 1)
                self.update(0)
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
        self.surface = surface
        
        # Refresh options to ensure they show current state
        self.refresh_options()
        
        # rebuild sell list when drawing the sell tab so values are fresh
        if self.current_tab == "sell":
            self.build_sell_list()
        gold = self.state.gold

        self.text.reset_layout()
        
        header = "Welcome to the Shop! - Buy" if self.current_tab == "buy" else "Welcome to the Shop! - Sell"
        self.text.draw(surface, header, GREEN, new_line=False)
        self.text.addOffset("y", 6)
        self.text.draw(surface, f"Your Gold: {gold}", l_offset=10)
        self.text.addOffset("y", 6)
        if self.current_tab == "buy":
            Options(surface).draw(self.options, yOffset=50)
        else:
            # Build display lines for sellable items
            sell_display = []
            if len(self.sell_items) == 0:
                sell_display.append("(TAB) Switch to Buy - No sellable items")
            else:
                for idx, (item_id, name, qty, val) in enumerate(self.sell_items):
                    # Limit to 5 visible options for simplicity (like inventory slots)
                    if idx >= 5:
                        break
                    sell_display.append(f"({idx+1}) {name} x{qty} - {val}g each")

            # Always show instruction to switch back
            sell_display.append("(TAB) Switch to Buying")
            sell_display.append("(ESC) Go Back to Windhelm")

            Options(surface).draw(sell_display, yOffset=50)
        
        Footer(surface).draw()

    def update(self, dt: float = 0):
        """Redraw the screen if we have a surface available."""
        if hasattr(self, 'surface') and self.surface is not None:
            self.draw(self.surface)
