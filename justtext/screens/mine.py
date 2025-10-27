import pygame
from .base import Screen
from ..constants import GREEN
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..components.footer import Footer
from ..util.itemUtil import *
from ..components.options import Options

class Mine(Screen):

    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot
        self.state.currentScreen = "mine"
        self.state.save()
        self.options = ["(1) Mine Stone", 
                        "(ESC) Go Back to Windhelm"]
             
    def update(self, dt: float) -> None:
        pass

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1 and equip_current_durability("pickaxe") > 0:
                self.state.stamina -= 1
                inv_add("stone", equip_get_level("pickaxe"))
                self.state.mining_xp += equip_get_level("pickaxe")
                equip_durability_down("pickaxe")
            elif event.key == pygame.K_ESCAPE:
                self.state.prevScreen = "mine"
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
        stone = inv_count("stone")

        self.text.reset_layout()
        self.text.draw(surface, f"/\\~~~~~~~~~~ Mine ~~~~~~~~~~/\\", GREEN, new_line=False, alignment="middle")
        self.text.addOffset("y", 6)
        self.text.draw(surface, f"Stone: {stone}", l_offset=10)
        self.text.addOffset("y", 6)

        Options(surface).draw(self.options, yOffset=50)

        Footer(surface).draw()