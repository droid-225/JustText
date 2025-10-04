import pygame
from .base import Screen
from ..constants import WHITE, GREEN
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..util.leveling import LevelCalculator

class Stats(Screen): # Stats screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot
        self.state.currentScreen = "stats"
        self.prevScreen = self.state.prevScreen

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.on_select(self.prevScreen)

    def draw(self, surface):
        level = LevelCalculator().calculate_level(self.state.total_xp)
        mining_level = LevelCalculator().calculate_level(self.state.mining_xp)
        prevScreen = self.prevScreen

        xp_for_next_level = LevelCalculator().get_xp_for_next_level(self.state.total_xp)
        mining_xp_for_next_level = LevelCalculator().get_xp_for_next_level(self.state.mining_xp)
        
        self.text.reset_layout()
        self.text.draw(surface, "Statistics", GREEN, new_line=False)

        self.text.draw(surface, f"Level: {level}", WHITE)
        self.text.draw(surface, f"XP Needed to Level Up: {xp_for_next_level}", GREEN, l_offset=30)
        
        self.text.draw(surface, f"Mining Level: {mining_level}", WHITE)
        self.text.draw(surface, f"XP Needed to Level Up: {mining_xp_for_next_level}", GREEN, l_offset=30)

        self.text.draw(surface, f"(ESC) Return to {prevScreen.capitalize()}", WHITE)