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
        self.prevScreen = self.state.prevScreen

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.on_select(self.prevScreen)

    def draw(self, surface):
        gold = self.state.gold
        autoMinerLevel = self.state.autoMinerLevel
        prevScreen = self.prevScreen

        self.text.reset_layout()
        self.text.draw(surface, "Inventory", GREEN, new_line=False)
        self.text.draw(surface, f"Your Gold: {gold}", WHITE)
        self.text.draw(surface, f"Auto Miner Level: {autoMinerLevel}", WHITE)
        self.text.draw(surface, f"(ESC) Return to {prevScreen}", WHITE)