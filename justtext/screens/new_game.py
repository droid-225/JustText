import pygame
from .base import Screen
from ..constants import GREEN, WHITE, BLACK
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state, list_slots

class New_Game(Screen):
    name = []
    i1_fin = False # input 1 flag
    choosing_slot = False

    def __init__(self, on_select):
        self.font = load_font()
        self.on_select = on_select
        self.text = TextRenderer(self.font)

    def handle_event(self, event):
        UPPERCASE = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
                     "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z")
        LOWERCASE = ("a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", 
                     "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: self.on_select("main_menu")

            if not self.i1_fin:
                for i in range(0, 26):
                    if event.key == pygame.key.key_code(UPPERCASE[i]) or event.key == pygame.key.key_code(LOWERCASE[i]):
                        self.name.append(UPPERCASE[i])
                        
                if event.key == pygame.K_BACKSPACE and len(self.name) > 0: 
                    self.name.pop()
                    
                if event.key == pygame.K_RETURN:
                    self.i1_fin = True
                    self.choosing_slot = True
            
            if self.i1_fin and self.choosing_slot:
                if event.key == pygame.K_1:
                    slot = 1
                elif event.key == pygame.K_2:
                    slot = 2
                elif event.key == pygame.K_3:
                    slot = 3
                else:
                    slot = None

                if slot is not None:
                    state = get_state()
                    state.name = "".join(self.name)
                    state.current_slot = slot
                    state.gold = 0
                    state.save()
                    self.on_select("welcome_screen")

    def draw(self, surface):
        self.text.reset_layout()
        self.text.draw(surface, "New Game", GREEN, new_line=False)
        self.text.draw(surface, "(ESC) Return to Home Page", WHITE)
        self.text.draw(surface, "Enter Your Name: ", WHITE)
        
        str_name = "".join(self.name)
        self.text.draw(surface, str_name, WHITE, new_line=False, x_offset=10)
        self.text.draw(surface, "Press Enter to Continue", WHITE)

        if self.i1_fin:
            self.text.draw(surface, f"Your Name: {str_name}", GREEN)
            slots = list_slots()
            # Show slot choices and whether they are occupied
            self.text.draw(surface, "Choose a slot to save:", WHITE)
            for idx, entry in enumerate(slots, start=1):
                name = entry["name"] or "<Empty>"
                curScreen = entry["currentScreen"]
                self.text.draw(surface, f"({idx}) Slot {idx}: {name} | {curScreen.capitalize()}", WHITE)
        