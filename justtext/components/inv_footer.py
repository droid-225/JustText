from ..constants import WHITE, BLACK
from ..assets import load_font
from ..util.text import TextRenderer
from ..state import get_state

class InvFooter:
    def __init__(self, surface):
        self.font = load_font()
        self.surface = surface
        self.text = TextRenderer(self.font)
        self.state = get_state()
        
    def draw(self):
        surface = self.surface

        # Inventory Screen
        inv = self.font.render(f"(ESC) Return to {self.state.prevScreen.capitalize()}", True, WHITE, BLACK)
        surface.blit(inv, (10, surface.get_height() - inv.get_height() - 6))

        # Stamina Counter
        stamina = self.font.render(str(self.state.stamina + 1), True, WHITE, BLACK)
        surface.blit(stamina, ((surface.get_width() / 2) - stamina.get_width() + 20, surface.get_height() - inv.get_height() - 6))

        # Stats Screen
        stats = self.font.render("(TAB) Change Category", True, WHITE, BLACK)
        surface.blit(stats, (surface.get_width() - stats.get_width() - 10, surface.get_height() - stats.get_height() - 6))