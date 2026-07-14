"""Per-plane bomb visual and damage effects."""

from __future__ import annotations

import math
import random
from abc import ABC, abstractmethod

import pygame

from src.config import LOGIC_H, LOGIC_W


class BombEffect(ABC):
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.life = self.duration
        self.done = False

    @property
    @abstractmethod
    def duration(self) -> float:
        pass

    def update(self, dt: float) -> None:
        self.life -= dt
        if self.life <= 0:
            self.done = True
        self._update(dt)

    def _update(self, dt: float) -> None:
        pass

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass

    def damages_rect(self) -> list[pygame.Rect]:
        return []

    def clears_bullets_in(self) -> list[pygame.Rect]:
        return []


class EnergyBlastEffect(BombEffect):
    """P-38: massive forward energy beam."""

    duration = 1.2

    def _update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        t = 1 - self.life / self.duration
        w = int(24 + t * 40)
        h = int((LOGIC_H - self.y) * t)
        beam = pygame.Surface((w, h), pygame.SRCALPHA)
        for row in range(h):
            alpha = int(200 * (1 - row / max(h, 1)) * (1 - abs(self.life / self.duration - 0.5) * 0.5))
            color = (100, 200, 255, alpha)
            pygame.draw.line(beam, color, (w // 2, row), (w // 2, row), max(2, w // 3))
        pygame.draw.rect(beam, (200, 240, 255, int(180 * t)), (w // 4, 0, w // 2, h))
        surface.blit(beam, (int(self.x - w // 2), int(self.y)))

    def damages_rect(self) -> list[pygame.Rect]:
        t = 1 - self.life / self.duration
        w = int(30 + t * 50)
        h = LOGIC_H
        return [pygame.Rect(int(self.x - w // 2), 0, w, h)]

    def clears_bullets_in(self) -> list[pygame.Rect]:
        return self.damages_rect()


class GaleForceEffect(BombEffect):
    """Spitfire: horizontal wind tunnels from both sides."""

    duration = 1.5

    def draw(self, surface: pygame.Surface) -> None:
        t = 1 - self.life / self.duration
        for side in (-1, 1):
            ox = 0 if side < 0 else LOGIC_W - int(80 * t)
            wind = pygame.Surface((int(80 * t), LOGIC_H), pygame.SRCALPHA)
            for i in range(8):
                y = int(i * LOGIC_H / 8 + self.life * 200) % LOGIC_H
                alpha = int(120 * t)
                pygame.draw.line(wind, (180, 220, 255, alpha), (0, y), (wind.get_width(), y + 20), 3)
            surface.blit(wind, (ox, 0))

    def damages_rect(self) -> list[pygame.Rect]:
        t = 1 - self.life / self.duration
        w = int(70 * t)
        return [pygame.Rect(0, 0, w, LOGIC_H), pygame.Rect(LOGIC_W - w, 0, w, LOGIC_H)]

    def clears_bullets_in(self) -> list[pygame.Rect]:
        return self.damages_rect()


class StukaRaidEffect(BombEffect):
    """P-51: dive bombers from top."""

    duration = 2.0

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.divers = [
            {"x": 60 + i * 90, "y": -40 - i * 20, "vy": 4 + i * 0.5}
            for i in range(4)
        ]

    def _update(self, dt: float) -> None:
        for d in self.divers:
            d["y"] += d["vy"] * dt * 60

    def draw(self, surface: pygame.Surface) -> None:
        for d in self.divers:
            cx, cy = int(d["x"]), int(d["y"])
            pygame.draw.polygon(surface, (60, 65, 75), [(cx, cy + 12), (cx + 10, cy), (cx, cy - 4), (cx - 10, cy)])
            pygame.draw.circle(surface, (255, 100, 40, 180), (cx, cy + 14), 6)

    def damages_rect(self) -> list[pygame.Rect]:
        rects = []
        for d in self.divers:
            if 0 < d["y"] < LOGIC_H:
                rects.append(pygame.Rect(int(d["x"] - 30), int(d["y"] - 20), 60, 60))
        return rects

    def clears_bullets_in(self) -> list[pygame.Rect]:
        return [pygame.Rect(0, 0, LOGIC_W, LOGIC_H)]


class ClusterStrikeEffect(BombEffect):
    """Bf-109: grid of explosions."""

    duration = 1.8

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.explosions = []
        for row in range(3):
            for col in range(4):
                self.explosions.append({
                    "x": 50 + col * 90 + random.uniform(-10, 10),
                    "y": 60 + row * 110 + random.uniform(-10, 10),
                    "delay": (row * 4 + col) * 0.12,
                    "fired": False,
                })

    def _update(self, dt: float) -> None:
        elapsed = self.duration - self.life
        for ex in self.explosions:
            if not ex["fired"] and elapsed >= ex["delay"]:
                ex["fired"] = True

    def draw(self, surface: pygame.Surface) -> None:
        elapsed = self.duration - self.life
        for ex in self.explosions:
            if not ex["fired"]:
                continue
            age = elapsed - ex["delay"]
            if age > 0.5:
                continue
            r = int(age * 50)
            alpha = int(200 * (1 - age / 0.5))
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 150, 50, alpha), (r, r), r)
            pygame.draw.circle(s, (255, 220, 100, alpha), (r, r), r // 2)
            surface.blit(s, (int(ex["x"] - r), int(ex["y"] - r)))

    def damages_rect(self) -> list[pygame.Rect]:
        elapsed = self.duration - self.life
        rects = []
        for ex in self.explosions:
            if ex["fired"]:
                age = elapsed - ex["delay"]
                if 0 < age < 0.4:
                    r = int(age * 45) + 10
                    rects.append(pygame.Rect(int(ex["x"] - r), int(ex["y"] - r), r * 2, r * 2))
        return rects

    def clears_bullets_in(self) -> list[pygame.Rect]:
        return self.damages_rect()


class TyphoonEffect(BombEffect):
    """Zero: expanding shockwave rings."""

    duration = 1.6

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.rings = [0.0, 0.25, 0.5]

    def draw(self, surface: pygame.Surface) -> None:
        elapsed = self.duration - self.life
        for delay in self.rings:
            age = elapsed - delay
            if age < 0 or age > 0.8:
                continue
            r = int(age * 200)
            alpha = int(180 * (1 - age / 0.8))
            s = pygame.Surface((r * 2 + 4, r * 2 + 4), pygame.SRCALPHA)
            pygame.draw.circle(s, (200, 230, 255, alpha), (r + 2, r + 2), r, 3)
            surface.blit(s, (int(self.x - r - 2), int(self.y - r - 2)))

    def damages_rect(self) -> list[pygame.Rect]:
        elapsed = self.duration - self.life
        rects = []
        for delay in self.rings:
            age = elapsed - delay
            if 0 < age < 0.6:
                r = int(age * 180) + 15
                rects.append(pygame.Rect(int(self.x - r), int(self.y - r), r * 2, r * 2))
        return rects

    def clears_bullets_in(self) -> list[pygame.Rect]:
        return [pygame.Rect(0, 0, LOGIC_W, LOGIC_H)]


class PhantomRushEffect(BombEffect):
    """Shinden: ghost silhouette dashes upward."""

    duration = 1.4

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y)
        self.ghosts = [
            {"x": x + off, "y": y, "vy": -12 - abs(off) * 0.2}
            for off in (-40, 0, 40)
        ]

    def _update(self, dt: float) -> None:
        for g in self.ghosts:
            g["y"] += g["vy"] * dt * 60

    def draw(self, surface: pygame.Surface) -> None:
        for g in self.ghosts:
            cx, cy = int(g["x"]), int(g["y"])
            ghost = pygame.Surface((36, 36), pygame.SRCALPHA)
            pygame.draw.polygon(ghost, (255, 80, 60, 160), [(18, 4), (30, 20), (18, 32), (6, 20)])
            pygame.draw.polygon(ghost, (255, 150, 80, 200), [(18, 10), (24, 20), (18, 26), (12, 20)])
            surface.blit(ghost, (cx - 18, cy - 18))
            trail = pygame.Surface((8, 30), pygame.SRCALPHA)
            trail.fill((255, 100, 50, 100))
            surface.blit(trail, (cx - 4, cy + 10))

    def damages_rect(self) -> list[pygame.Rect]:
        rects = []
        for g in self.ghosts:
            if 0 < g["y"] < LOGIC_H:
                rects.append(pygame.Rect(int(g["x"] - 18), int(g["y"] - 18), 36, 50))
        return rects

    def clears_bullets_in(self) -> list[pygame.Rect]:
        return self.damages_rect()


_BOMB_MAP = {
    "energy": EnergyBlastEffect,
    "gale": GaleForceEffect,
    "stuka": StukaRaidEffect,
    "cluster": ClusterStrikeEffect,
    "typhoon": TyphoonEffect,
    "phantom": PhantomRushEffect,
}


class BombEffectManager:
    def __init__(self) -> None:
        self.effects: list[BombEffect] = []

    def trigger(self, bomb_id: str, x: float, y: float) -> BombEffect:
        cls = _BOMB_MAP.get(bomb_id, EnergyBlastEffect)
        effect = cls(x, y)
        self.effects.append(effect)
        return effect

    def update(self, dt: float) -> None:
        for e in self.effects:
            e.update(dt)
        self.effects = [e for e in self.effects if not e.done]

    def draw(self, surface: pygame.Surface) -> None:
        for e in self.effects:
            e.draw(surface)

    def get_damage_rects(self) -> list[pygame.Rect]:
        rects = []
        for e in self.effects:
            rects.extend(e.damages_rect())
        return rects

    def get_bullet_clear_rects(self) -> list[pygame.Rect]:
        rects = []
        for e in self.effects:
            rects.extend(e.clears_bullets_in())
        return rects

    def clear(self) -> None:
        self.effects.clear()
