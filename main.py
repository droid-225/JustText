import pygame
from justtext.constants import WIDTH, HEIGHT, BLACK, WIN_CAPTION
from justtext.screen_manager import ScreenManager
from justtext.screens.main_menu import Main_Menu
from justtext.screens.windhelm import Windhelm
from justtext.routes import create_routes

class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(WIN_CAPTION)
        self.clock = pygame.time.Clock()
        self.running = True
        self.manager = ScreenManager(None)

        def set_screen(screen): self.manager.set(screen)
        def stop(): self.running = False

        self.routes = create_routes(set_screen, stop)
        on_select = self.routes["__on_select__"]
        self.manager.set(Windhelm(on_select))

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.manager.handle_event(event)
            
            self.win.fill(BLACK)
            self.manager.update(dt)
            self.manager.draw(self.win)
            
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    Game().run()