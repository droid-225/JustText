from hashlib import blake2b
import pygame
from .base import Screen
from ..constants import GREEN, WHITE, BLACK
from ..assets import load_font

class New_Game(Screen):
    name = []
    i1_fin = False # input 1 flag
    y_pos = x_pos = l_margin = prevWidth = 0

    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select

    def handle_event(self, event):
        UPPERCASE = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
                     "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")
        LOWERCASE = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
                     "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: self.on_select("main_menu")

            if not self.i1_fin:
                for i in range(0, 26):
                    if event.key == pygame.key.key_code(UPPERCASE[i]) or event.key == pygame.key.key_code(LOWERCASE[i]):
                        self.name.append(UPPERCASE[i])
                        
                if event.key == pygame.K_BACKSPACE and len(self.name) > 0: 
                    self.name.pop()
                    
                if event.key == pygame.K_RETURN: self.i1_fin = True

    def draw(self, surface):
        placeholder = self.font.render("New Game:", 1, GREEN)
        self.l_margin = self.y_pos = self.x_pos = placeholder.get_height()
        surface.blit(placeholder, (self.l_margin, self.y_pos))

        self.drawText(surface, "(1) Return to Home Page")

        self.drawText(surface, "Enter Your Name: ")

        str_name = "".join(self.name)
        self.drawText(surface, str_name, newLine = False, x_offset = 10)

        self.drawText(surface, "Press Enter to Continue")

        if self.i1_fin:
            self.drawText(surface, f"Your Name: {str_name}", GREEN)

            self.drawText(surface, "(2) Confirm", BLACK, WHITE)

            self.drawText(surface, "(3) Cancel", BLACK, WHITE, newLine = False, x_offset = 10)

    def drawText(self, surface, text, textColor = WHITE, bgColor = 0, y_offset = 0, x_offset = 0, newLine = True, xReset = False):
        text = self.font.render(f"{text}", 1, textColor, bgColor)
        
        if newLine:
            self.prevWidth = text.get_width()

        if newLine:
            self.y_pos += 10 + text.get_height()
        if x_offset != 0:
            self.x_pos += x_offset + self.prevWidth
        else:
            self.x_pos = self.l_margin
        self.y_pos += y_offset

        surface.blit(text, (self.x_pos, self.y_pos))