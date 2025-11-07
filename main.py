import pygame
from justtext.constants import WIDTH, HEIGHT, BLACK, WIN_CAPTION
from justtext.screen_manager import ScreenManager
from justtext.screens.load_game import Load_Game
from justtext.routes import create_routes
from justtext.state import get_state

class Game:
    def __init__(self):
        pygame.init()
        icon_surface = pygame.image.load("assets/icon/icon.png")
        pygame.display.set_icon(icon_surface)
        # Create a resizable window and base surface (logical resolution)
        self.window_width, self.window_height = WIDTH, HEIGHT
        self.win = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption(WIN_CAPTION)

        # Base surface: keep existing screens drawing to this logical size
        self.base_surface = pygame.Surface((WIDTH, HEIGHT))
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
                elif event.type == pygame.VIDEORESIZE:
                    # update window size and recreate display surface
                    self.window_width, self.window_height = event.w, event.h
                    self.win = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
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
            # Draw to the fixed logical/base surface first
            self.base_surface.fill(BLACK)
            self.manager.draw(self.base_surface)

            # Scale the base surface to the current window size while preserving aspect ratio
            base_w, base_h = WIDTH, HEIGHT
            win_w, win_h = self.window_width, self.window_height
            scale = min(win_w / base_w, win_h / base_h)
            target_w = max(1, int(base_w * scale))
            target_h = max(1, int(base_h * scale))

            scaled = pygame.transform.smoothscale(self.base_surface, (target_w, target_h))

            # center scaled surface and letterbox the rest with background
            x = (win_w - target_w) // 2
            y = (win_h - target_h) // 2
            self.win.fill(BLACK)
            self.win.blit(scaled, (x, y))

            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    Game().run()