from ..constants import WHITE, BLACK
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state

class WildsRandomEvents:
    def __init__(self, surface):
        self.font = load_font()
        self.surface = surface
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.distTraveled = 0
        self.smallEvent = False
        self.mediumEvent = False
        
    def moveForward(dist=1):
        distTraveled += dist

    def draw(self):
        surface = self.surface

        if self.smallEvent:
            self.text.draw(surface, "Something small happens!")
        elif self.mediumEvent:
            self.text.draw(surface, "Something medium happens!")
        