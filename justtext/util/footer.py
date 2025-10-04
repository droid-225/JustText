from ..constants import WHITE, BLACK
from ..assets import load_font

class Footer:
    def __init__(self, surface):
        self.font = load_font()
        self.surface = surface
        
    def draw(self):
        surface = self.surface

        # Inventory Screen
        inv = self.font.render("(I) Inventory", True, WHITE, BLACK)
        surface.blit(inv, (10, surface.get_height() - inv.get_height() - 6))

        # Stats Screen
        stats = self.font.render("(U) Stats", True, WHITE, BLACK)
        surface.blit(stats, (surface.get_width() - stats.get_width() - 10, surface.get_height() - stats.get_height() - 6))