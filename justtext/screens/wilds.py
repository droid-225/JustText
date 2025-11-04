import pygame

from .base import Screen
from ..constants import RED, WHITE, GREEN, BLUE, BLACK
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from ..components.footer import Footer
from ..components.options import Options
from ..components.wilds_random_events import WildsRandomEvents
from ..components.event_system import EventSystem, EventType, Event, EventOption
from ..util.itemUtil import inv_add
import random

class Wilds(Screen): # main menu inherits from Screen
    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.state.currentScreen = "wilds"
        self.distTraveled = self.state.wilds_dist
        etype, eid = self.state.get_wilds_event()
        self.current_event = (etype, eid) if etype != EventType.NONE else None
        # Create a fresh EventSystem each time
        self.event_system = EventSystem()
        # Track the original event descriptions so we can restore them
        self.original_events = {}
        self.collected = False  # Initialize as False so first collection is possible
        self.collected_item = None
        self.collected_amount = 0
        
    def handle_travel(self):
        """Handle player movement and determine next event"""
        self.distTraveled += 1
        self.state.stamina -= 1

        # Reset any previously modified events to their original descriptions
        for key, desc in self.original_events.items():
            event = self.event_system.get_event(key[0], key[1])
            if event:
                event.description = desc
        self.original_events.clear()  # Clear stored originals

        # Reset collection state when moving to new event
        self.collected = False
        self.collected_item = None
        self.collected_amount = 0

        if self.distTraveled % 50 == 0:
            self.current_event = (EventType.BIG, random.randint(1, 5))
        elif self.distTraveled % 20 == 0:
            self.current_event = (EventType.CARAVAN, 0)
        elif self.distTraveled % 10 == 0:
            self.current_event = (EventType.MEDIUM, random.randint(1, 5))
        else:
            self.current_event = (EventType.SMALL, random.randint(1, 4))
        
    def handle_event(self, event):
        if self.state.stamina <= 0:
            self.state.gold = (int)(self.state.gold / 2)
            self.on_select("windhelm")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.handle_travel()
            
            if self.current_event and self.current_event[0] == EventType.SMALL:
                event_id = self.current_event[1]
                if event_id == 2:
                    if event.key == pygame.K_2: # Slime fight start
                        pass # TODO: Implement fight
                    elif event.key == pygame.K_3: # Slime interact
                        pass # TODO: Implement interaction
                elif event_id == 3 and not self.collected:  # Stone collection
                    if event.key == pygame.K_2:
                        self.collected_amount = random.randint(1, 10)
                        inv_add("stone", self.collected_amount)
                        self.collected_item = "stone"
                        # Switch to a collection result event
                        self.current_event = (EventType.COLLECTION, 0)
                        self.collected = True
                        # Force a redraw to show collection
                        if hasattr(self, 'surface'):
                            self.draw(self.surface)
                elif event_id == 4 and not self.collected: # Gold collection
                    if event.key == pygame.K_2:
                        self.collected_amount = random.randint(1, 10)
                        self.state.gold += self.collected_amount
                        self.collected_item = "gold"
                        # Switch to a collection result event
                        self.current_event = (EventType.COLLECTION, 0)
                        self.collected = True
                        # Force a redraw to show collection
                        if hasattr(self, 'surface'):
                            self.draw(self.surface)

            if event.key == pygame.K_ESCAPE and self.current_event and self.current_event[0] == EventType.CARAVAN:
                self.state.wilds_dist = 0
                self.state.set_wilds_event(EventType.NONE, 0)
                self.state.save()
                self.on_select("windhelm")

            if event.key == pygame.K_i: # Goto Inventory Screen
                if self.current_event:
                    self.state.set_wilds_event(self.current_event[0], self.current_event[1])
                else:
                    self.state.set_wilds_event(EventType.NONE, 0)

                self.state.prevScreen = self.state.currentScreen
                self.state.wilds_dist = self.distTraveled
                self.state.save()
                self.on_select("inventory")

            if event.key == pygame.K_u: # Goto Stats Screen
                if self.current_event:
                    self.state.set_wilds_event(self.current_event[0], self.current_event[1])
                else:
                    self.state.set_wilds_event(EventType.NONE, 0)

                self.state.prevScreen = self.state.currentScreen
                self.state.wilds_dist = self.distTraveled
                self.state.save()
                self.on_select("stats")

    def draw(self, surface):
        # Store surface for redrawing after collection
        self.surface = surface
        
        self.text.reset_layout()
        self.text.draw(surface, "\\/\\/\\/\\/\\/\\/\\/ Wastrel Wilds \\/\\/\\/\\/\\/\\/\\/", color=RED, bg=GREEN, new_line=False, alignment="middle")
        self.text.addOffset("y", 6)

        self.text.draw(surface, f"Distance Traveled: {self.distTraveled}", l_offset=10, alignment="middle")
        self.text.addOffset("y", 6)

        randomEvents = WildsRandomEvents(surface, yOffset=40)

        if self.current_event:
            event_type, event_id = self.current_event
            if event_type == EventType.COLLECTION and self.collected_item:
                event = self.event_system.create_collection_event(self.collected_amount, self.collected_item)
                self.text.draw(surface, event.description, y_offset=40)
                # Add more space between description and options
                self.text.draw(surface, "(1) Keep traveling", y_offset=80)
            elif event_type == EventType.SMALL:
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