from ast import While
import pygame
from .base import Screen
from ..constants import WHITE, GREEN
from ..assets import load_font
from ..ui.text import TextRenderer
from ..state import get_state

class Inventory(Screen):
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot

    def handle_event(self, event):
        # TODO: return to previous screen

    def draw(self, surface):
        count = self.state.count
        autoMinerLevel = self.state.autoMinerLevel

        self.text.reset_layout()
        self.text.draw(surface, "Inventory", GREEN, new_line=False)
        self.text.draw(surface, f"Your Gold: {count}", WHITE)
        self.text.draw(surface, f"Auto Miner Level: {autoMinerLevel}", WHITE)