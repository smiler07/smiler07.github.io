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
        grow = min(1.0, t * 2.2)
        w = int(28 + grow * 48)
        # Never create a zero-height Surface on the impact frame.
        h = max(1, int(self.y * grow))
        beam = pygame.Surface((w, h), pygame.SRCALPHA)
        for row in range(h):
            fade = 1 - row / h
            alpha = int(210 * fade * (0.75 + 0.25 * math.sin(t * 18 + row * 0.18) ** 2))
            half = max(2, int((w * 0.46) * (0.45 + fade * 0.55)))
            pygame.draw.line(beam, (70, 175, 255, alpha), (w // 2 - half, row), (w // 2 + half, row))
        pygame.draw.rect(beam, (225, 250, 255, int(190 * t)), (w // 2 - max(2, w // 9), 0, max(4, w // 4), h))
        surface.blit(beam, (int(self.x - w // 2), int(self.y - h)))

        # Bright impact reactor and irregular electrical arcs make the direction
        # of the upward blast unmistakable.
        core_r = int(8 + grow * 10)
        core = pygame.Surface((core_r * 2 + 6, core_r * 2 + 6), pygame.SRCALPHA)
        pygame.draw.circle(core, (80, 180, 255, 110), (core_r + 3, core_r + 3), core_r)
        pygame.draw.circle(core, (245, 255, 255, 245), (core_r + 3, core_r + 3), max(3, core_r // 2))
        surface.blit(core, (int(self.x - core_r - 3), int(self.y - core_r - 3)))
        for side in (-1, 1):
            points = [(int(self.x + side * 4), int(self.y - 3))]
            for step in range(1, 5):
                points.append((int(self.x + side * (8 + step * 7)), int(self.y - step * 10 - math.sin(t * 20 + step) * 4)))
            pygame.draw.lines(surface, (180, 235, 255, int(180 * (1 - t * 0.25))), False, points, 1)

    def damages_rect(self) -> list[pygame.Rect]:
        t = 1 - self.life / self.duration
        w = int(32 + min(1.0, t * 2.2) * 54)
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


class NovaBreakerEffect(BombEffect):
    """Raiden: a violet core implodes, then releases a starburst shockwave."""

    duration = 1.35

    def draw(self, surface: pygame.Surface) -> None:
        elapsed = self.duration - self.life
        r = int(14 + elapsed * 150)
        alpha = int(220 * max(0.0, 1 - elapsed / self.duration))
        glow = pygame.Surface((r * 2 + 8, r * 2 + 8), pygame.SRCALPHA)
        pygame.draw.circle(glow, (170, 80, 255, alpha // 3), (r + 4, r + 4), r)
        pygame.draw.circle(glow, (235, 200, 255, alpha), (r + 4, r + 4), max(3, r // 3))
        pygame.draw.circle(glow, (255, 255, 255, alpha), (r + 4, r + 4), max(2, r // 7))
        surface.blit(glow, (int(self.x - r - 4), int(self.y - r - 4)))
        for i in range(12):
            angle = math.tau * i / 12 + elapsed * 2
            inner, outer = r * 0.45, r + 10
            pygame.draw.line(surface, (220, 150, 255, alpha),
                             (int(self.x + math.cos(angle) * inner), int(self.y + math.sin(angle) * inner)),
                             (int(self.x + math.cos(angle) * outer), int(self.y + math.sin(angle) * outer)), 2)

    def damages_rect(self) -> list[pygame.Rect]:
        elapsed = self.duration - self.life
        r = int(35 + elapsed * 135)
        return [pygame.Rect(int(self.x - r), int(self.y - r), r * 2, r * 2)]

    def clears_bullets_in(self) -> list[pygame.Rect]:
        return self.damages_rect()


_BOMB_MAP = {
    "energy": EnergyBlastEffect,
    "gale": GaleForceEffect,
    "stuka": StukaRaidEffect,
    "cluster": ClusterStrikeEffect,
    "typhoon": TyphoonEffect,
    "phantom": PhantomRushEffect,
    "nova": NovaBreakerEffect,
}


class BombDelivery:
    """A visible ordnance run before the bomb's special attack takes effect."""

    _COLORS = {
        "energy": (100, 220, 255), "gale": (180, 235, 255),
        "stuka": (255, 185, 70), "cluster": (255, 125, 55),
        "typhoon": (205, 235, 255), "phantom": (255, 80, 70),
        "nova": (205, 120, 255),
    }

    def __init__(self, bomb_id: str, x: float, y: float) -> None:
        self.bomb_id, self.start_x, self.start_y = bomb_id, x, y
        self.target_x = max(42, min(LOGIC_W - 42, x))
        self.target_y = max(92, y - 210)
        self.duration = 0.42
        self.time = 0.0
        self.done = False

    @property
    def progress(self) -> float:
        return min(1.0, self.time / self.duration)

    def update(self, dt: float) -> None:
        self.time += dt
        self.done = self.time >= self.duration

    def draw(self, surface: pygame.Surface) -> None:
        p = self.progress
        # Ease-out trajectory with a shallow arc: it reads as a launched object,
        # not an effect that simply appears at the target.
        eased = 1 - (1 - p) ** 3
        x = self.start_x + (self.target_x - self.start_x) * eased
        y = self.start_y + (self.target_y - self.start_y) * eased - math.sin(p * math.pi) * 22
        color = self._COLORS.get(self.bomb_id, (255, 190, 80))
        trail = pygame.Surface((32, 54), pygame.SRCALPHA)
        for i in range(5):
            alpha = 25 + i * 20
            pygame.draw.circle(trail, (*color, alpha), (16, 44 - i * 7), max(2, 6 - i), )
        surface.blit(trail, (int(x - 16), int(y - 18)))
        # Ordnance body, fins and hot exhaust.
        body = pygame.Surface((18, 28), pygame.SRCALPHA)
        pygame.draw.polygon(body, (*color, 255), [(9, 1), (15, 12), (13, 24), (9, 27), (5, 24), (3, 12)])
        pygame.draw.polygon(body, (255, 245, 205, 255), [(9, 4), (12, 13), (9, 17), (6, 13)])
        pygame.draw.line(body, (35, 45, 60, 255), (3, 19), (0, 25), 2)
        pygame.draw.line(body, (35, 45, 60, 255), (15, 19), (18, 25), 2)
        surface.blit(body, body.get_rect(center=(int(x), int(y))))
        # Subtle target designator gives the player a clear impact promise.
        r = int(8 + p * 12)
        pygame.draw.circle(surface, (*color, int(80 + p * 100)), (int(self.target_x), int(self.target_y)), r, 1)
        pygame.draw.line(surface, (*color, 120), (int(self.target_x - r - 3), int(self.target_y)), (int(self.target_x + r + 3), int(self.target_y)), 1)


class BombEffectManager:
    def __init__(self) -> None:
        self.effects: list[BombEffect] = []
        self.deliveries: list[BombDelivery] = []
        self.impact_bursts: list[dict] = []

    def trigger(self, bomb_id: str, x: float, y: float) -> None:
        self.deliveries.append(BombDelivery(bomb_id, x, y))

    def _impact(self, delivery: BombDelivery) -> None:
        cls = _BOMB_MAP.get(delivery.bomb_id, EnergyBlastEffect)
        effect = cls(delivery.target_x, delivery.target_y)
        self.effects.append(effect)
        self.impact_bursts.append({"x": delivery.target_x, "y": delivery.target_y, "life": 0.55, "max": 0.55,
                                   "color": BombDelivery._COLORS.get(delivery.bomb_id, (255, 190, 80))})

    def update(self, dt: float) -> list[str]:
        impacts: list[str] = []
        for delivery in self.deliveries:
            delivery.update(dt)
            if delivery.done:
                self._impact(delivery)
                impacts.append(delivery.bomb_id)
        self.deliveries = [d for d in self.deliveries if not d.done]
        for burst in self.impact_bursts:
            burst["life"] -= dt
        self.impact_bursts = [b for b in self.impact_bursts if b["life"] > 0]
        for e in self.effects:
            e.update(dt)
        self.effects = [e for e in self.effects if not e.done]
        return impacts

    def draw(self, surface: pygame.Surface) -> None:
        # A brief, restrained screen flash sells the emergency weapon without
        # obscuring incoming patterns for the entire effect duration.
        for e in self.effects:
            progress = 1.0 - e.life / e.duration
            if progress < 0.16:
                alpha = int(80 * (1.0 - progress / 0.16))
                flash = pygame.Surface((LOGIC_W, LOGIC_H), pygame.SRCALPHA)
                flash.fill((210, 235, 255, alpha))
                surface.blit(flash, (0, 0))
        for e in self.effects:
            e.draw(surface)
        for burst in self.impact_bursts:
            t = burst["life"] / burst["max"]
            radius = int(16 + (1 - t) * 58)
            flash = pygame.Surface((radius * 2 + 8, radius * 2 + 8), pygame.SRCALPHA)
            pygame.draw.circle(flash, (*burst["color"], int(100 * t)), (radius + 4, radius + 4), radius)
            pygame.draw.circle(flash, (255, 245, 210, int(230 * t)), (radius + 4, radius + 4), max(3, radius // 3))
            pygame.draw.circle(flash, (*burst["color"], int(230 * t)), (radius + 4, radius + 4), radius, 2)
            surface.blit(flash, (int(burst["x"] - radius - 4), int(burst["y"] - radius - 4)))
            for i in range(10):
                angle = math.tau * i / 10 + (1 - t) * 1.5
                pygame.draw.line(surface, (*burst["color"], int(170 * t)),
                                 (int(burst["x"] + math.cos(angle) * radius * 0.35), int(burst["y"] + math.sin(angle) * radius * 0.35)),
                                 (int(burst["x"] + math.cos(angle) * (radius + 10)), int(burst["y"] + math.sin(angle) * (radius + 10))), 2)
        for delivery in self.deliveries:
            delivery.draw(surface)

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
        self.deliveries.clear()
        self.impact_bursts.clear()
