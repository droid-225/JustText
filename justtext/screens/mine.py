import pygame
from .base import Screen
from ..constants import GREEN, WHITE, BLACK
from ..assets import load_font
from ..ui.text import TextRenderer
from ..state import get_state

class Mine(Screen):

    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot
        self.auto_on = False
        self._accum = 0.0            
        self.options = ["(1) Mine Gold", 
                        "(2) Start Auto-Miner", 
                        "(3) Stop Auto-Miner", 
                        "(4) Go Back to Town"]
             
    def update(self, dt: float) -> None:
        if self.auto_on:
            self._accum += dt
            if self._accum >= 0.25:
                self.state.count += 1
                self._accum = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.state.count += 1
            elif event.key == pygame.K_2:
                self.auto_on = True
            elif event.key == pygame.K_3:
                self.auto_on = False
            elif event.key == pygame.K_4:
                self.auto_on = False
                self.state.save()
                self.on_select("windhelm")

    def draw(self, surface):
        count = self.state.count

        self.text.reset_layout()
        self.text.draw(surface, f"Mine", GREEN, new_line=False)
        self.text.draw(surface, f"Gold: {count}", WHITE)

        for option in self.options:
            self.text.draw(surface, option, WHITE)