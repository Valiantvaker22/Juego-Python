"""
BaseScene - All game scenes inherit from this.
"""

import pygame
from abc import ABC, abstractmethod


class BaseScene(ABC):
    def __init__(self, ctx: dict):
        self.game     = ctx["game"]
        self.screen   = ctx["screen"]
        self.settings = ctx["settings"]
        self.bus      = ctx["bus"]
        self.assets   = ctx["assets"]
        self._ctx     = ctx

    def on_enter(self, **kwargs): pass

    @abstractmethod
    def handle_events(self, events: list[pygame.event.Event]): ...

    @abstractmethod
    def update(self, dt: float): ...

    @abstractmethod
    def draw(self, surface: pygame.Surface): ...
