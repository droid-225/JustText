from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from .options import Options
from .event_system import EventSystem, EventType

class WildsRandomEvents:
    def __init__(self, surface, yOffset=0):
        self.font = load_font()
        self.surface = surface
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.yOffset = yOffset
        self.event_system = EventSystem()
        
    def _draw_event(self, event):
        """Helper to draw any event type with consistent formatting"""
        self.text.draw(self.surface, event.description, y_offset=self.yOffset)
        
        options = [f"({opt.key}) {opt.text}" for opt in event.get_available_options()]
        Options(self.surface).draw(options, yOffset=213)
        
    def smallEvent(self, eventID: int):
        event = self.event_system.get_event(EventType.SMALL, eventID)
        if event:
            self._draw_event(event)
        
    def mediumEvent(self, eventID: int):
        event = self.event_system.get_event(EventType.MEDIUM, eventID)
        if event:
            self._draw_event(event)

    def bigEvent(self, eventID: int):
        event = self.event_system.get_event(EventType.BIG, eventID)
        if event:
            self._draw_event(event)

    def caravan(self):
        event = self.event_system.get_caravan_event()
        self._draw_event(event)
