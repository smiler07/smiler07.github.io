"""Multi-layer parallax scrolling background."""

from __future__ import annotations

import math
import random

import pygame

from src.config import (
    C_GROUND,
    C_GROUND_LIGHT,
    GOLD_VALUES,
    C_SKY_BOT,
    C_SKY_MID,
    C_SKY_TOP,
    LOGIC_H,
    LOGIC_W,
)
from src.render.sprite_factory import SpriteFactory


class Cloud:
    def __init__(self, x: float, y: float, speed: float, scale: float) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.scale = scale
        self._build()

    def _build(self) -> None:
        w, h = int(60 * self.scale), int(20 * self.scale)
        self.surface = pygame.Surface((w, h), pygame.SRCALPHA)
        for i, ox in enumerate([0.2, 0.45, 0.7]):
            r = int(8 * self.scale * (1 + i * 0.3))
            alpha = 40 + i * 15
            pygame.draw.ellipse(self.surface, (255, 200, 150, alpha), (int(ox * w) - r, h // 2 - r, r * 2, r * 2))

    def update(self, dt: float, scroll: float) -> None:
        self.y += (self.speed + scroll) * dt * 60

    def draw(self, surface: pygame.Surface) -> None:
        if -20 < self.y < LOGIC_H + 20:
            surface.blit(self.surface, (int(self.x), int(self.y)))


class ParallaxBackground:
    def __init__(self) -> None:
        self.scroll = 1.2
        self.time = 0.0
        self.clouds: list[Cloud] = []
        self.buildings: list[dict] = []
        self._init_clouds()
        self._init_buildings()
        self._sky_cache: pygame.Surface | None = None

    def _init_clouds(self) -> None:
        for _ in range(12):
            self.clouds.append(Cloud(
                random.uniform(0, LOGIC_W),
                random.uniform(-LOGIC_H, LOGIC_H),
                random.uniform(0.15, 0.5),
                random.uniform(0.6, 1.4),
            ))

    def _init_buildings(self) -> None:
        x = 0
        while x < LOGIC_W + 40:
            variant = random.randint(0, 2)
            sprite = SpriteFactory.building(variant)
            self.buildings.append({
                "x": x,
                "y": LOGIC_H - sprite.get_height() - 30,
                "sprite": sprite,
                "hp": 2,
                "alive": True,
                "gold": random.choice(GOLD_VALUES),
            })
            x += sprite.get_width() + random.randint(8, 24)

    def _make_sky(self) -> pygame.Surface:
        sky = pygame.Surface((LOGIC_W, LOGIC_H))
        for y in range(LOGIC_H):
            t = y / LOGIC_H
            if t < 0.5:
                tt = t * 2
                c = tuple(int(C_SKY_TOP[i] * (1 - tt) + C_SKY_MID[i] * tt) for i in range(3))
            else:
                tt = (t - 0.5) * 2
                c = tuple(int(C_SKY_MID[i] * (1 - tt) + C_SKY_BOT[i] * tt) for i in range(3))
            pygame.draw.line(sky, c, (0, y), (LOGIC_W, y))
        # Sun glow
        for r in range(40, 0, -1):
            alpha = int(30 * (1 - r / 40))
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 180, 80, alpha), (r, r), r)
            sky.blit(s, (LOGIC_W // 2 - r, int(LOGIC_H * 0.72) - r))
        return sky

    def get_buildings(self) -> list[dict]:
        return [b for b in self.buildings if b["alive"]]

    def damage_building(self, building: dict) -> int | None:
        building["hp"] -= 1
        if building["hp"] <= 0:
            building["alive"] = False
            return building["gold"]
        return None

    def update(self, dt: float) -> None:
        self.time += dt
        if self._sky_cache is None:
            self._sky_cache = self._make_sky()

        for c in self.clouds:
            c.update(dt, self.scroll * 0.3)
            if c.y > LOGIC_H + 30:
                c.y = -30
                c.x = random.uniform(0, LOGIC_W)

        # Scroll buildings
        for b in self.buildings:
            if b["alive"]:
                b["y"] += self.scroll * dt * 60
                if b["y"] > LOGIC_H:
                    b["alive"] = False

        # Recycle buildings at top
        alive = [b for b in self.buildings if b["alive"]]
        if len(alive) < 4:
            variant = random.randint(0, 2)
            sprite = SpriteFactory.building(variant)
            self.buildings.append({
                "x": random.uniform(0, LOGIC_W - sprite.get_width()),
                "y": -sprite.get_height(),
                "sprite": sprite,
                "hp": 2,
                "alive": True,
                "gold": random.choice(GOLD_VALUES),
            })

    def draw(self, surface: pygame.Surface) -> None:
        if self._sky_cache:
            surface.blit(self._sky_cache, (0, 0))

        for c in self.clouds:
            c.draw(surface)

        # Ocean strip
        water_y = LOGIC_H - 28
        for y in range(water_y, LOGIC_H):
            wave = math.sin(self.time * 3 + y * 0.2) * 2
            shade = int(30 + 15 * math.sin(self.time * 2 + y * 0.1))
            pygame.draw.line(surface, (20, 50 + shade, 90), (0, y), (LOGIC_W, y))
        pygame.draw.rect(surface, C_GROUND, (0, LOGIC_H - 28, LOGIC_W, 6))
        pygame.draw.rect(surface, C_GROUND_LIGHT, (0, LOGIC_H - 22, LOGIC_W, 22))

        for b in self.buildings:
            if b["alive"]:
                surface.blit(b["sprite"], (int(b["x"]), int(b["y"])))
