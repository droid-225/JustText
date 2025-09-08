import pygame
from .base import Screen
from ..constants import GREEN, WHITE
from ..assets import load_font

class New_Game(Screen):
    name = []
    i1_fin = False # input 1 flag

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
        l_margin = y_margin = x_margin = placeholder.get_height()
        surface.blit(placeholder, (l_margin, y_margin))

        return_prompt = self.font.render("(1) Return to Home Page", 1, WHITE)
        y_margin += 10 + return_prompt.get_height()
        surface.blit(return_prompt, (l_margin, y_margin))

        name_prompt = self.font.render("Enter Your Name: ", 1, WHITE)
        y_margin += 10 + name_prompt.get_height()
        surface.blit(name_prompt, (l_margin, y_margin))

        str_name = "".join(self.name)
        name = self.font.render(f"{str_name}", 1, WHITE)
        surface.blit(name, (x_margin + 10 + name_prompt.get_width(), y_margin))
        
        enter_prompt = self.font.render("Press Enter to Continue", 1, WHITE)
        y_margin += 10 + name_prompt.get_height()
        surface.blit(enter_prompt, (x_margin, y_margin))

        if self.i1_fin:
            confirm_prompt = self.font.render(f"Your Name: {str_name}", 1, GREEN)
            y_margin += 10 + name_prompt.get_height()
            surface.blit(confirm_prompt, (x_margin, y_margin))

            confirm_option = self.font.render("(2) Confirm", 1, 1, WHITE) # not exactly sure what's going on here but it gives the text a background so that's cool
            y_margin += 10 + name_prompt.get_height()
            surface.blit(confirm_option, (x_margin, y_margin))

            cancel_option = self.font.render("(3) Cancel", 1, 1, WHITE)
            surface.blit(cancel_option, (x_margin + 10 + confirm_option.get_width(), y_margin))  
        