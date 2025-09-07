import pygame, pathlib
from .constants import FONT_NAME, FONT_SIZE

ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"

def load_font():
    pygame.font.init()
    ttf = ASSETS_PATH / "fonts" / f"{FONT_NAME}.ttf"

    if ttf.exists():
        return pygame.font.Font(str(ttf), FONT_SIZE)
    
    return pygame.font.SysFont("comicsans", FONT_SIZE)