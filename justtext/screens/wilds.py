import pygame

from .base import Screen
from ..constants import RED, WHITE, GREEN, BLUE, BLACK
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..components.footer import Footer
from ..components.options import Options
from ..components.wilds_random_events import WildsRandomEvents
import random

class Wilds(Screen): # main menu inherits from Screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.slot = self.state.current_slot
        self.state.currentScreen = "wilds"
        self.state.save()
        self.distTraveled = 19
        self.smallEvent = False
        self.mediumEvent = False
        self.bigEvent = False
        self.caravan = False
        self.eventID = 0
        self.inputFlags = {
            'windhelmable': False,
            'collectable': False,
            'attackable': False
        }
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.distTraveled += 1
                self.state.stamina -= 1

                if self.distTraveled % 50 == 0:
                    self.caravan = False
                    self.smallEvent = False
                    self.mediumEvent = False
                    self.bigEvent = True
                    self.eventID = random.randint(1, 5)

                elif self.distTraveled % 20 == 0:
                    self.caravan = True
                    self.smallEvent = False
                    self.mediumEvent = False
                    self.bigEvent = False
                    self.inputFlags['windhelmable'] = True

                elif self.distTraveled % 10 == 0:
                    self.caravan = False
                    self.smallEvent = False
                    self.mediumEvent = True
                    self.bigEvent = False
                    self.eventID = random.randint(1, 5)

                else:
                    self.caravan = False
                    self.smallEvent = True
                    self.mediumEvent = False
                    self.bigEvent = False
                    self.eventID = random.randint(1, 5)
                    
            elif event.key == pygame.K_ESCAPE and self.inputFlags['windhelmable']:
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

        self.text.draw(surface, f"Distance Traveled: {self.distTraveled}", l_offset=10, alignment="middle")
        self.text.addOffset("y", 6)

        randomEvents = WildsRandomEvents(surface, yOffset=40)

        if self.smallEvent:
            randomEvents.smallEvent(self.eventID)
        elif self.mediumEvent:
            randomEvents.mediumEvent(self.eventID)
        elif self.bigEvent:
            randomEvents.bigEvent(self.eventID)
        elif self.caravan:
            randomEvents.caravan()

        if self.distTraveled % 20 != 0: # placeholder, change later
            self.text.draw(surface, "(1) Keep Traveling", y_offset=165)

        Footer(surface).draw()