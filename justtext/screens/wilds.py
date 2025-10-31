import pygame

from .base import Screen
from ..constants import RED, WHITE, GREEN, BLUE, BLACK
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..components.footer import Footer
from ..components.options import Options
from ..components.wilds_random_events import WildsRandomEvents
from ..components.event_system import EventSystem, EventType
from ..util.itemUtil import inv_add
import random

class Wilds(Screen): # main menu inherits from Screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.state.currentScreen = "wilds"
        self.distTraveled = 0
        self.current_event = None
        self.event_system = EventSystem()
        self.collected = False
        
    def _handle_travel(self):
        """Handle player movement and determine next event"""
        self.distTraveled += 1
        self.state.stamina -= 1

        if self.distTraveled % 50 == 0:
            self.current_event = (EventType.BIG, random.randint(1, 5))
        elif self.distTraveled % 20 == 0:
            self.current_event = (EventType.CARAVAN, 0)
        elif self.distTraveled % 10 == 0:
            self.current_event = (EventType.MEDIUM, random.randint(1, 5))
        else:
            self.current_event = (EventType.SMALL, random.randint(1, 4))
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self._handle_travel()
                self.collected = False
            
            # Handle combat/collection events
            elif event.key == pygame.K_2:
                if self.current_event and self.current_event[0] == EventType.SMALL:
                    event_id = self.current_event[1]
                    if event_id == 2:  # Start Slime combat
                        pass # TODO: Implement combat
                    elif event_id == 3:  # Stone collection
                        inv_add("stone", random.randint(1, 10))
                        self.collected = True
                    elif event_id == 4: # Gold collection
                        self.state.gold += random.randint(1, 10)
                        self.collected = True
            
            elif event.key == pygame.K_3:
                if self.current_event and self.current_event[0] == EventType.SMALL:
                    event_id = self.current_event[1]
                    if event_id == 2:  # Slime interaction
                        pass # TODO: Implement interaction

            # Handle navigation events
            elif event.key == pygame.K_ESCAPE and self.current_event and self.current_event[0] == EventType.CARAVAN:
                self.state.save() 
                self.on_select("windhelm")
            elif event.key == pygame.K_i:
                self.state.prevScreen = self.state.currentScreen
                self.state.save()
                self.on_select("inventory")
            elif event.key == pygame.K_u:
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

        if self.current_event:
            event_type, event_id = self.current_event
            if event_type == EventType.SMALL:
                randomEvents.smallEvent(event_id)
            elif event_type == EventType.MEDIUM:
                randomEvents.mediumEvent(event_id)
            elif event_type == EventType.BIG:
                randomEvents.bigEvent(event_id)
            elif event_type == EventType.CARAVAN:
                randomEvents.caravan()

        if self.distTraveled == 0:
            self.text.draw(surface, "(1) Start traveling", y_offset=165)

        Footer(surface).draw()