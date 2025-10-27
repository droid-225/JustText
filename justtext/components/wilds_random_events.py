from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state
from .options import Options

class WildsRandomEvents:
    def __init__(self, surface, yOffset=0):
        self.font = load_font()
        self.surface = surface
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.yOffset = yOffset
        
    def _draw_event(self, event_type: str, eventID: int):
        """Common logic for drawing events"""
        self.text.draw(self.surface, f"{event_type} Event {eventID} Occurred!", y_offset=self.yOffset)
        Options(self.surface).draw(["(1) Keep Traveling"], yOffset=213)

    def smallEvent(self, eventID: int):
        self._draw_event("Small", eventID)
        
    def mediumEvent(self, eventID: int):
        self._draw_event("Medium", eventID)

    def bigEvent(self, eventID: int):
        self._draw_event("Big", eventID)

    def caravan(self):
        self.text.draw(self.surface, "You have reached a friendly caravan", y_offset=self.yOffset)

        options = ["(1) Keep Traveling", 
                    "(ESC) Go to Windhelm"]

        Options(self.surface).draw(options, yOffset=213)
