import pygame
from .base import Screen
from ..constants import GREEN, WHITE, BLACK
from ..assets import load_font

class Welcome(Screen):
    prevWidth = 0

    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select

    def draw(self, surface):
        self.drawText(surface, "WELCOME")

    def drawText(self, surface, text, textColor = WHITE, bgColor = 0, l_offset = 0, y_offset = 0, x_offset = 0, newLine = True):
        text = self.font.render(f"{text}", 1, textColor, bgColor)
        
        x_pos = y_pos = l_margin = text.get_height()

        if newLine:
            self.prevWidth = text.get_width()
            y_pos += 10 + text.get_height()

        if x_offset != 0:
            x_pos += x_offset + self.prevWidth

        y_pos += y_offset
        l_margin += l_offset

        surface.blit(text, (x_pos, y_pos))