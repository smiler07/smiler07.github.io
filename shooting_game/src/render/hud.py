"""In-game HUD overlay."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from src.config import C_GOLD, C_HUD, C_HUD_ACCENT, C_HUD_DANGER, GOLD_LARGE, GOLD_MEDIUM, GOLD_SMALL, LOGIC_H, LOGIC_W, MAX_BOMBS, MAX_POWER


@dataclass
class ScorePopup:
    x: float
    y: float
    text: str
    life: float
    color: tuple[int, int, int]


class HUD:
    def __init__(self) -> None:
        self.font = pygame.font.SysFont("consolas", 11)
        self.font_big = pygame.font.SysFont("consolas", 14, bold=True)
        self.font_popup = pygame.font.SysFont("consolas", 12, bold=True)
        self.boss_name: str | None = None
        self.boss_hp_ratio: float = 1.0
        self.message: str = ""
        self.message_timer: float = 0.0
        self.popups: list[ScorePopup] = []

    def show_message(self, text: str, duration: float = 2.0) -> None:
        self.message = text
        self.message_timer = duration

    def show_gold_popup(self, x: float, y: float, value: int) -> None:
        if value >= GOLD_LARGE:
            color = (255, 240, 120)
            label = f"+{GOLD_LARGE}"
        elif value >= GOLD_MEDIUM:
            color = (255, 200, 80)
            label = f"+{GOLD_MEDIUM}"
        else:
            color = C_GOLD
            label = f"+{GOLD_SMALL}"
        self.popups.append(ScorePopup(x, y, label, 1.2, color))

    def update(self, dt: float) -> None:
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""
        alive = []
        for p in self.popups:
            p.life -= dt
            p.y -= dt * 35
            if p.life > 0:
                alive.append(p)
        self.popups = alive

    def draw(
        self,
        surface: pygame.Surface,
        score: int,
        hi_score: int,
        lives: int,
        bombs: int,
        power: int,
        plane_name: str,
        stage_id: int = 1,
        total_stages: int = 3,
    ) -> None:
        # Top bar background
        bar = pygame.Surface((LOGIC_W, 22), pygame.SRCALPHA)
        bar.fill((0, 0, 20, 140))
        surface.blit(bar, (0, 0))

        score_t = self.font.render(f"SCORE {score:07d}", True, C_HUD)
        hi_t = self.font.render(f"HI {hi_score:07d}", True, C_HUD_ACCENT)
        stage_t = self.font.render(f"ST {stage_id}/{total_stages}", True, C_HUD_ACCENT)
        surface.blit(score_t, (6, 4))
        surface.blit(hi_t, (LOGIC_W // 2 - hi_t.get_width() // 2, 4))
        surface.blit(stage_t, (LOGIC_W - stage_t.get_width() - 6, 4))

        # Lives (left of bombs)
        for i in range(lives):
            pygame.draw.polygon(surface, C_HUD_ACCENT,
                              [(LOGIC_W - 110 + i * 14, 14), (LOGIC_W - 104 + i * 14, 6), (LOGIC_W - 98 + i * 14, 14)])

        # Bombs
        bomb_t = self.font.render("B", True, (100, 180, 255))
        for i in range(min(bombs, MAX_BOMBS)):
            surface.blit(bomb_t, (LOGIC_W - 148 + i * 10, 5))

        # Power gauge
        gauge_y = 418
        pygame.draw.rect(surface, (30, 30, 50), (10, gauge_y, LOGIC_W - 20, 10), border_radius=3)
        fill_w = int((LOGIC_W - 24) * (power / MAX_POWER))
        if fill_w > 0:
            color = C_HUD_DANGER if power == MAX_POWER else (255, 100, 80)
            pygame.draw.rect(surface, color, (12, gauge_y + 2, fill_w, 6), border_radius=2)
        power_t = self.font.render(f"POWER {power}/{MAX_POWER}", True, C_HUD)
        surface.blit(power_t, (12, gauge_y - 12))

        plane_t = self.font.render(plane_name, True, (150, 170, 200))
        surface.blit(plane_t, (LOGIC_W - plane_t.get_width() - 8, gauge_y - 12))

        # Boss bar
        if self.boss_name and self.boss_hp_ratio > 0:
            bw = LOGIC_W - 60
            pygame.draw.rect(surface, (40, 20, 20), (30, 30, bw, 8), border_radius=2)
            pygame.draw.rect(surface, (255, 60, 40), (32, 32, int((bw - 4) * self.boss_hp_ratio), 4), border_radius=1)
            name_t = self.font_big.render(self.boss_name, True, C_HUD_DANGER)
            surface.blit(name_t, (LOGIC_W // 2 - name_t.get_width() // 2, 18))

        # Center message
        if self.message:
            msg = self.font_big.render(self.message, True, (255, 255, 200))
            bg = pygame.Surface((msg.get_width() + 16, msg.get_height() + 8), pygame.SRCALPHA)
            bg.fill((0, 0, 0, 160))
            surface.blit(bg, (LOGIC_W // 2 - bg.get_width() // 2, LOGIC_H // 2 - 40))
            surface.blit(msg, (LOGIC_W // 2 - msg.get_width() // 2, LOGIC_H // 2 - 36))

        # Floating gold score popups
        for p in self.popups:
            alpha = min(255, int(255 * (p.life / 1.2)))
            t = self.font_popup.render(p.text, True, p.color)
            t.set_alpha(alpha)
            surface.blit(t, (int(p.x - t.get_width() // 2), int(p.y)))
