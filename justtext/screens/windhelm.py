import pygame
from .base import Screen
from ..constants import WHITE, GREEN, BLUE, BLACK
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state

class Windhelm(Screen): # main menu inherits from Screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot
        self.state.currentScreen = "windhelm"
        self.options = ["(1) Go to the Shop", 
                        "(2) Go to the Mine", 
                        "(S) Save", 
                        "(ESC) Save and Exit to Main Menu"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: self.on_select("shop")
            elif event.key == pygame.K_2: self.on_select("mine")
            elif event.key == pygame.K_3: self.state.save()
            elif event.key == pygame.K_ESCAPE:
                self.state.save() 
                self.on_select("main_menu")
            elif event.key == pygame.K_i or event.key == pygame.key.key_code("I"):
                self.state.prevScreen = "windhelm"
                self.state.save()
                self.on_select("inventory")
            elif event.key == pygame.K_u or event.key == pygame.key.key_code("U"):
                self.state.prevScreen = "windhelm"
                self.state.save()
                self.on_select("stats")

    def draw(self, surface):
        self.text.reset_layout()
        self.text.draw(surface, "<~~~ Windhelm ~~~>", GREEN, new_line=False)

        for option in self.options:
            self.text.draw(surface, option, WHITE)

        # Inventory Screen
        inv = self.font.render("(I) Inventory", True, WHITE, BLACK)
        surface.blit(inv, (10, surface.get_height() - inv.get_height() - 6))

        # Stats Screen
        stats = self.font.render("(U) Stats", True, WHITE, BLACK)
        surface.blit(stats, (surface.get_width() - stats.get_width() - 10, surface.get_height() - stats.get_height() - 6))