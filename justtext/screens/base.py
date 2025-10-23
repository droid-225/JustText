import pygame
from abc import abstractmethod

class Screen():
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None: ...

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...

    @abstractmethod
    def update(self, dt: float) -> None: ...