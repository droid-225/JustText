import pygame
from abc import ABC, abstractmethod

class Screen(ABC):
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None: ...

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...

    @abstractmethod
    def update(self, dt: float) -> None: ...