from __future__ import annotations

from abc import ABC, abstractmethod

import pygame


class GameState(ABC):
    def __init__(self, game: "Game") -> None:
        self.game = game

    def enter(self) -> None:
        pass

    def exit(self) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self.game.running = False
