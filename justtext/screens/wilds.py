import pygame
from .base import Screen
from ..constants import RED, WHITE, GREEN, BLUE, BLACK
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..util.footer import Footer

class Wilds(Screen): # main menu inherits from Screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot
        self.state.currentScreen = "wilds"
        self.distTraveled = 0
        self.options = ["(1) Keep Traveling", 
                        "(ESC) Go to Windhelm"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                distTraveled += 1
                self.state.stamina -= 1
            elif event.key == pygame.K_ESCAPE:
                self.state.save() 
                self.on_select("windhelm")
            elif event.key == pygame.K_i or event.key == pygame.key.key_code("I"):
                self.state.prevScreen = self.state.currentScreen
                self.state.save()
                self.on_select("inventory")
            elif event.key == pygame.K_u or event.key == pygame.key.key_code("U"):
                self.state.prevScreen = self.state.currentScreen
                self.state.save()
                self.on_select("stats")

    def draw(self, surface):
        self.text.reset_layout()
        self.text.draw(surface, "\\/\\/\\/\\/\\/\\/\\/ Wastrel Wilds \\/\\/\\/\\/\\/\\/\\/", color=RED, bg=GREEN, new_line=False, alignment="middle")
        self.text.addOffset("y", 6)

        for option in self.options:
            self.text.draw(surface, option)

        Footer(surface).draw()