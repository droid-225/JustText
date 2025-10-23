from ..constants import WHITE, BLACK
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state

class WildsRandomEvents:
    def __init__(self, surface, yOffset=0):
        self.font = load_font()
        self.surface = surface
        self.text = TextRenderer(self.font)
        self.state = get_state()
        self.yOffset = yOffset
        
    def smallEvent(self):
        self.text.draw(self.surface, "Small Event Occured!", y_offset=self.yOffset)

    def mediumEvent(self):
        self.text.draw(self.surface, "Medium Event Occured!", y_offset=self.yOffset)
        