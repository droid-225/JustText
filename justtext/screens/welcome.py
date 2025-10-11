import pygame
from .base import Screen
from ..constants import GREEN, WHITE
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state

class Welcome(Screen):

    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot
        self.auto_on = False
        self._accum = 0.0       
        self.start_time = pygame.time.get_ticks()  
             
    def update(self, dt: float) -> None:
        if self.auto_on:
            self._accum += dt
            if self._accum >= 0.25:
                self.state.count += 1
                self._accum = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state.newGame = 0
                self.on_select("windhelm")

    def draw(self, surface):
        name = self.state.name

        self.text.reset_layout()
        self.text.draw(surface, f"WELCOME {name}, TO JUST TEXT!", GREEN, alignment="middle", new_line=False)
        self.text.draw(surface, "")

        lines = ["You are an adventurer looking for fame and",
                 "fortune. Your destination now is Windhelm,",
                 "a bustling and vibrant town where you",
                 "begin your journey. Along your adventure", 
                 "you will face many foes and beasts.",
                 "Stay determined and conquer the world of", 
                 "JUST TEXT!"]

        for line in lines: 
            self.text.draw(surface, line, alignment="middle")

        elapsed = pygame.time.get_ticks() - self.start_time  # elapsed time in ms

        if elapsed >= 5000:  # after 5 seconds
            self.text.draw(surface, "(ENTER) Go to Windhelm", alignment="middle", y_offset=20)