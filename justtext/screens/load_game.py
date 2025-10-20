import pygame
from .base import Screen
from ..constants import WHITE, GREEN
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import list_slots, load_active_slot, get_state

class Load_Game(Screen):
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.on_select("main_menu")
            elif event.key == pygame.K_1:
                load_active_slot(1)
                self.state = get_state()
                if self.state.newGame == 1:
                    self.on_select("welcome_screen")
                else:
                    self.on_select(self.state.currentScreen)
                    self.state.stamina += 1
            elif event.key == pygame.K_2:
                load_active_slot(2)
                self.state = get_state()
                if self.state.newGame == 1:
                    self.on_select("welcome_screen")
                else:
                    self.on_select(self.state.currentScreen)
                    self.state.stamina += 1
            elif event.key == pygame.K_3:
                load_active_slot(3)
                self.state = get_state()
                if self.state.newGame == 1:
                    self.on_select("welcome_screen")
                else:
                    self.on_select(self.state.currentScreen)
                    self.state.stamina += 1

    def draw(self, surface):
        self.text.reset_layout()
        self.text.draw(surface, "<~~~~~~~~~~ Load Game ~~~~~~~~~~>", GREEN, new_line=False, alignment="middle")
        self.text.addOffset("y", 6)

        slots = list_slots()
        for idx, entry in enumerate(slots, start=1):
            name = entry["name"] or "<Empty>"
            curScreen = entry["currentScreen"]
            self.text.draw(surface, f"({idx}) Slot {idx}: {name} | {curScreen.capitalize()}", WHITE)

        self.text.draw(surface, "(ESC) Return to Home Page", WHITE)