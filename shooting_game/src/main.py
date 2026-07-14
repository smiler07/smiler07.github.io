"""Game entry point and state machine."""

from __future__ import annotations

import sys

import pygame

from src.config import DT, FPS, LOGIC_H, LOGIC_W, SCALE, SCREEN_H, SCREEN_W
from src.core.audio_manager import AudioManager
from src.core.input_manager import InputManager
from src.states.play_state import PlayState
from src.states.select_state import SelectState
from src.states.title_state import TitleState


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Strikers 1945")
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        self.logic_surface = pygame.Surface((LOGIC_W, LOGIC_H))
        self.clock = pygame.time.Clock()
        self.input = InputManager()
        self.audio = AudioManager()
        self.running = True
        self.hi_score = 0
        self.selected_plane = "p38"
        self.stage_index = 0

        self.states = {
            "title": TitleState(self),
            "select": SelectState(self),
            "play": PlayState(self),
        }
        self.current_state_name = "title"
        self.current_state = self.states["title"]
        self.current_state.enter()
        self.audio.start_menu_bgm()

    def change_state(self, name: str) -> None:
        self.current_state.exit()
        self.current_state_name = name
        self.current_state = self.states[name]
        self.current_state.enter()
        if name == "play":
            self.audio.start_bgm()
        else:
            self.audio.start_menu_bgm()

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            dt = min(dt, 0.05)

            events = self.input.poll()
            self.current_state.handle_events(events)

            # Fixed timestep update
            acc = dt
            while acc >= DT:
                self.current_state.update(DT)
                acc -= DT

            self.logic_surface.fill((0, 0, 0))
            self.current_state.draw(self.logic_surface)

            # Scale to screen with optional shake
            shake_x, shake_y = 0, 0
            if isinstance(self.current_state, PlayState):
                shake_x, shake_y = self.current_state.shake_offset

            scaled = pygame.transform.scale(self.logic_surface, (SCREEN_W, SCREEN_H))
            self.screen.fill((0, 0, 0))
            self.screen.blit(scaled, (shake_x, shake_y))
            pygame.display.flip()

        pygame.quit()
        sys.exit()


def main() -> None:
    Game().run()


if __name__ == "__main__":
    main()
