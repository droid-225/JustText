import pygame
from .base import Screen
from ..constants import WHITE, GREEN, BLUE, BLACK
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..components.footer import Footer
from ..components.options import Options

class Windhelm(Screen): # main menu inherits from Screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.state.currentScreen = "windhelm"
        self.options = ["(1) Go to the Inn",
                        "(2) Go to the Shop", 
                        "(3) Go to the Mine",
                        "(4) Go to the Blacksmith",
                        "(5) Travel the Wastrel Wilds",
                        "(ESC) Save and Exit to Main Menu"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: self.on_select("inn")
            elif event.key == pygame.K_2: self.on_select("shop")
            elif event.key == pygame.K_3: self.on_select("mine")
            elif event.key == pygame.K_4: self.on_select("blacksmith")
            elif event.key == pygame.K_5: self.on_select("wilds_warning")
            elif event.key == pygame.K_ESCAPE:
                self.state.save() 
                self.on_select("main_menu")
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
        self.text.draw(surface, "<~~~~~~~~~~ Windhelm ~~~~~~~~~~>", GREEN, new_line=False, alignment="middle")
        self.text.addOffset("y", 6)

        Options(surface).draw(self.options, yOffset=10)

        Footer(surface).draw()