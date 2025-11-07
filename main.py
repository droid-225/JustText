import pygame
import pathlib
from justtext.constants import WIDTH, HEIGHT, BLACK, WIN_CAPTION
from justtext.screen_manager import ScreenManager
from justtext.screens.load_game import Load_Game
from justtext.routes import create_routes
from justtext.state import get_state

class Game:
    def __init__(self):
        pygame.init()
        # set window icon (optional)
        try:
            icon_surface = pygame.image.load("assets/icon/icon.png")
            pygame.display.set_icon(icon_surface)
        except Exception:
            pass

        # Create a resizable window and base surface (logical resolution)
        self.window_width, self.window_height = WIDTH, HEIGHT
        self.win = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        pygame.display.set_caption(WIN_CAPTION)

        # Base surface: keep existing screens drawing to this logical size
        self.base_surface = pygame.Surface((WIDTH, HEIGHT))

        # Tile/filler configuration for letterbox areas
        # Use a small pixel-art tile by default for crisp tiling
        self.tile_size = 32  # good default for pixel-art tiles (32, 64, 128 are common)
        self._tile = None
        self._filler_surface = None

        # Try to load a tile image; if missing, generate a simple one and save it
        assets_dir = pathlib.Path(__file__).resolve().parent.parent / "assets"
        tile_path = assets_dir / "bg_tile.png"
        try:
            img = pygame.image.load(str(tile_path))
            # use nearest scaling for pixel art to keep crisp edges
            if img.get_width() != self.tile_size or img.get_height() != self.tile_size:
                img = pygame.transform.scale(img, (self.tile_size, self.tile_size))
            self._tile = img.convert()
        except Exception:
            # generate a pixel-art tile and save it for later runs
            try:
                assets_dir.mkdir(parents=True, exist_ok=True)
                self._tile = self.generate_pixel_tile(self.tile_size)
                pygame.image.save(self._tile, str(tile_path))
            except Exception:
                # worst case: leave _tile as None and fallback to solid fill
                self._tile = None

        # timing and screen manager
        self.clock = pygame.time.Clock()
        self.running = True
        self.manager = ScreenManager(None)

        def set_screen(screen):
            self.manager.set(screen)

        def stop():
            self.running = False

        self.routes = create_routes(set_screen, stop)
        on_select = self.routes["__on_select__"]
        self.manager.set(Load_Game(on_select))

    def generate_pixel_tile(self, size: int) -> pygame.Surface:
        """Generate a small tile suitable for pixel-art tiling (no alpha).
        Produces a seamless-looking checker/dot pattern that tiles cleanly.
        """
        surf = pygame.Surface((size, size)).convert()
        # base colors (dark palette)
        c1 = (28, 28, 34)
        c2 = (36, 36, 46)
        surf.fill(c1)

        # make a small checker pattern (cells of 4x4 pixels) so it tiles
        cell = max(2, size // 8)
        for x in range(0, size, cell):
            for y in range(0, size, cell):
                if (x // cell + y // cell) % 2 == 0:
                    pygame.draw.rect(surf, c2, (x, y, cell, cell))

        # subtle center pixel dot (keeps tile visually interesting but still tiles)
        cx, cy = size // 2, size // 2
        dot_color = (50, 50, 64)
        surf.set_at((cx, cy), dot_color)
        return surf

    def build_tiled_surface(self, window_w: int, window_h: int) -> pygame.Surface:
        """Build and return a surface tiled with the configured tile covering the given window size.
        This is intended to be called at resize time and the result cached.
        """
        if self._tile is None:
            # fallback: solid color
            s = pygame.Surface((window_w, window_h)).convert()
            s.fill((18, 18, 22))
            return s

        # Create a surface matching the display format for best blit performance
        s = pygame.Surface((window_w, window_h)).convert()
        tx, ty = self._tile.get_width(), self._tile.get_height()
        for x in range(0, window_w, tx):
            for y in range(0, window_h, ty):
                s.blit(self._tile, (x, y))
        return s

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
                    # rebuild cached filler for the new window size (cheap relative to per-frame work)
                    try:
                        self._filler_surface = self.build_tiled_surface(self.window_width, self.window_height)
                    except Exception:
                        self._filler_surface = None
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

            # center scaled surface and letterbox the rest with our filler background
            x = (win_w - target_w) // 2
            y = (win_h - target_h) // 2

            # Ensure we have a cached filler surface for this window size
            if self._filler_surface is None:
                self._filler_surface = self.build_tiled_surface(win_w, win_h)

            # blit the cached filler once, then blit the scaled game surface on top
            try:
                self.win.blit(self._filler_surface, (0, 0))
            except Exception:
                # fallback to solid fill
                self.win.fill(BLACK)

            self.win.blit(scaled, (x, y))

            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    Game().run()