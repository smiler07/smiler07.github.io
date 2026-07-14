"""Title screen with animated background."""

from __future__ import annotations

import math
import random

import pygame

from src.config import C_HUD, C_HUD_ACCENT, LOGIC_H, LOGIC_W, PLANES
from src.states.base_state import GameState


class TitleState(GameState):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.time = 0.0
        self.blink = 0.0
        self.stars = [(random.uniform(0, LOGIC_W), random.uniform(0, LOGIC_H),
                       random.uniform(0.3, 1.5)) for _ in range(60)]

    def enter(self) -> None:
        self.time = 0.0

    def update(self, dt: float) -> None:
        self.time += dt
        self.blink += dt
        if self.game.input.confirm_pressed:
            self.game.change_state("select")

    def draw(self, surface: pygame.Surface) -> None:
        # Animated gradient sky
        for y in range(LOGIC_H):
            t = y / LOGIC_H
            wave = math.sin(self.time * 0.5 + y * 0.02) * 8
            r = int(15 + t * 80 + wave)
            g = int(20 + t * 40 + wave * 0.5)
            b = int(50 + (1 - t) * 60)
            pygame.draw.line(surface, (r, g, b), (0, y), (LOGIC_W, y))

        for sx, sy, spd in self.stars:
            ny = (sy + self.time * spd * 30) % LOGIC_H
            brightness = int(150 + 100 * math.sin(self.time * 2 + sx))
            pygame.draw.circle(surface, (brightness, brightness, 200), (int(sx), int(ny)), 1)

        # Title
        font_title = pygame.font.SysFont("impact", 42)
        font_sub = pygame.font.SysFont("consolas", 12)

        title = font_title.render("STRIKERS", True, C_HUD_ACCENT)
        year = font_title.render("1945", True, (255, 100, 60))
        shadow = font_title.render("STRIKERS", True, (40, 20, 10))
        surface.blit(shadow, (LOGIC_W // 2 - title.get_width() // 2 + 2, 82))
        surface.blit(title, (LOGIC_W // 2 - title.get_width() // 2, 80))
        surface.blit(year, (LOGIC_W // 2 - year.get_width() // 2 + 60, 115))

        sub = font_sub.render("VERTICAL SCROLL SHOOTER", True, (150, 170, 200))
        surface.blit(sub, (LOGIC_W // 2 - sub.get_width() // 2, 155))

        if int(self.blink * 2) % 2 == 0:
            prompt = font_sub.render("PRESS ENTER / Z TO START", True, C_HUD)
            surface.blit(prompt, (LOGIC_W // 2 - prompt.get_width() // 2, 340))

        controls = font_sub.render("ARROWS:Move  Z:Shoot/Hold-Charge  X:Bomb  SHIFT:Slow", True, (100, 120, 150))
        surface.blit(controls, (LOGIC_W // 2 - controls.get_width() // 2, 400))

        hi = font_sub.render(f"HI-SCORE {self.game.hi_score:07d}", True, C_HUD_ACCENT)
        surface.blit(hi, (LOGIC_W // 2 - hi.get_width() // 2, 370))
