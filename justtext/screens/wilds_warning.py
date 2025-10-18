import pygame
from .base import Screen
from ..constants import GREEN, WHITE
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state

class WildsWarning(Screen):

    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot
        self.state.currentScreen = "wilds_warning"

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y or event.key == pygame.key.key_code("Y"):
                self.on_select("wilds")
            if event.key == pygame.K_n or event.key == pygame.key.key_code("N"):
                self.on_select("windhelm")

    def draw(self, surface):
        self.text.reset_layout()
        self.text.draw(surface, f"!!!WARNING!!!", GREEN, alignment="middle", new_line=False)
        self.text.draw(surface, "")

        lines = ["You are about to enter the Wastrel Wilds!",
                 "Once you enter, you cannot return to Windhelm",
                 "unless you reach the carriage stops along the way!",
                 "If you run out of stamina or passout in the wilds,", 
                 "you will lose all of your gold.",
                 "Do you want to continue?"]

        for line in lines: 
            self.text.draw(surface, line, alignment="middle")

        self.text.draw(surface, "(Y) Continue to the Wastrel Wilds", alignment="middle", y_offset=20)
        self.text.draw(surface, "(N) Go back to Windhelm", alignment="middle", y_offset=20)
        