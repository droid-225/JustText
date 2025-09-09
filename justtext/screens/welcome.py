import pygame
from .base import Screen
from ..constants import GREEN, WHITE, BLACK
from ..assets import load_font
from ..ui.text import TextRenderer
from ..state import get_state

class Welcome(Screen):

    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot     

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.on_select("main_menu")
            elif event.key == pygame.K_1:
                self.state.count += 1
            elif event.key == pygame.K_2:
                self.state.count -= 1
            elif event.key == pygame.K_3:
                self.state.save()

    def draw(self, surface):
        name = self.state.name
        count = self.state.count

        self.text.reset_layout()
        slot_label = self.slot if self.slot is not None else "<None>"
        self.text.draw(surface, f"WELCOME {name}", GREEN, new_line=False)
        self.text.draw(surface, f"Count: {count}", WHITE)
        self.text.draw(surface, f"Slot: {slot_label}", WHITE)
        self.text.draw(surface, "(1) Count Up", WHITE)
        self.text.draw(surface, "(2) Count Down", WHITE)
        self.text.draw(surface, "(3) Save", WHITE)

        self.text.draw(surface, "(ESC) Return to Home Page", WHITE)