class ScreenManager:
    def __init__(self, screen):
        self.current = screen # current screen being managed
    
    def set(self, screen):
        self.current = screen

    def handle_event(self, event):
        self.current.handle_event(event)

    def update(self, dt):
        self.current.update(dt)

    def draw(self, surface):
        self.current.draw(surface)