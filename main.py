import pygame
from justtext.constants import WIDTH, HEIGHT, BLACK, WIN_CAPTION
from justtext.screen_manager import ScreenManager
from justtext.screens.load_game import Load_Game
from justtext.routes import create_routes
from justtext.state import get_state

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
        self.manager.set(Load_Game(on_select))

    def run(self):
        # Use update-on-input: only run game logic when input or timers produce an action.
        # Still poll events and render every frame so UI stays responsive.
        while self.running:
            # limit rendering/polling to a reasonable rate to avoid CPU burn
            dt = self.clock.tick(30) / 1000.0
            # Accumulate play time (in seconds)
            get_state().play_time_seconds += dt

            action_occurred = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # save unless player is viewing a transient screen
                    if (get_state().currentScreen != "inventory" and get_state().currentScreen != "stats"):
                        get_state().save()
                    self.running = False
                else:
                    # forward the event to the active screen
                    self.manager.handle_event(event)

                    # treat keyboard presses and user-timers as actions that should advance game logic
                    if event.type == pygame.KEYDOWN:
                        action_occurred = True
                    elif event.type >= pygame.USEREVENT:
                        action_occurred = True

            # run update only when there was a meaningful action
            if action_occurred:
                # pass 0.0 since turn-based logic doesn't rely on per-frame dt here
                self.manager.update(0.0)

            # render every frame so the UI responds instantly to input
            self.win.fill(BLACK)
            self.manager.draw(self.win)

            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    Game().run()