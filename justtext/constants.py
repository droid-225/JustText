from enum import Enum, auto

class InventoryCategory(Enum):
    ALL = auto()
    MATERIALS = auto()
    CONSUMABLES = auto()
    TOOLS = auto()
    ARMOR = auto()

# Window Constants
WIDTH, HEIGHT = 700, 500
WIN_CAPTION = "Just Text" # window caption

# Color Constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Font Constants
FONT_NAME = "pixelpurl"
FONT_SIZE = 30