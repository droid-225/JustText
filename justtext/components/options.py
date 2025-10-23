from ..constants import WHITE, BLACK
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state

class Options:
    def __init__(self, surface):
        self.font = load_font()
        self.surface = surface
        self.text = TextRenderer(self.font)
        self.state = get_state()
        
    def draw(self, options, lOffset=0, yOffset=0):
        surface = self.surface

        for option in options:
            self.text.draw(surface, option, l_offset=lOffset, y_offset=yOffset)