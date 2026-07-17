"""Multi-layer parallax scrolling background."""

from __future__ import annotations

import math
import random

import pygame

from src.config import (
    C_GROUND,
    C_GROUND_LIGHT,
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
    """Stage-specific layered environments behind the shared combat field."""

    THEMES = (
        {"name": "coast", "top": (10, 25, 65), "mid": (55, 105, 165), "bot": (235, 125, 62)},
        {"name": "airfield", "top": (8, 14, 28), "mid": (28, 48, 72), "bot": (75, 78, 62)},
        {"name": "final", "top": (24, 8, 38), "mid": (96, 24, 54), "bot": (230, 72, 35)},
        {"name": "storm", "top": (12, 20, 32), "mid": (34, 58, 74), "bot": (85, 95, 105)},
        {"name": "void", "top": (6, 4, 20), "mid": (27, 12, 55), "bot": (95, 30, 105)},
    )

    def __init__(self, stage_index: int = 0) -> None:
        self.stage_index = stage_index
        self.theme = self.THEMES[stage_index % len(self.THEMES)]
        self.scroll = 1.2
        self.time = 0.0
        self.clouds: list[Cloud] = []
        self.buildings: list[dict] = []
        self.stars = [(random.randrange(LOGIC_W), random.randrange(LOGIC_H), random.uniform(0.2, 0.9)) for _ in range(46)]
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
            })
            x += sprite.get_width() + random.randint(8, 24)

    def _make_sky(self) -> pygame.Surface:
        sky = pygame.Surface((LOGIC_W, LOGIC_H))
        top, mid, bot = self.theme["top"], self.theme["mid"], self.theme["bot"]
        for y in range(LOGIC_H):
            t = y / LOGIC_H
            if t < 0.5:
                tt = t * 2
                c = tuple(int(top[i] * (1 - tt) + mid[i] * tt) for i in range(3))
            else:
                tt = (t - 0.5) * 2
                c = tuple(int(mid[i] * (1 - tt) + bot[i] * tt) for i in range(3))
            pygame.draw.line(sky, c, (0, y), (LOGIC_W, y))
        # Theme focal light: sun, searchlight moon, or final-stage red eclipse.
        light = (255, 180, 80) if self.theme["name"] == "coast" else (180, 215, 255) if self.theme["name"] == "airfield" else (255, 85, 50)
        for r in range(40, 0, -1):
            alpha = int(30 * (1 - r / 40))
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*light, alpha), (r, r), r)
            sky.blit(s, (LOGIC_W // 2 - r, int(LOGIC_H * 0.72) - r))
        return sky

    def get_buildings(self) -> list[dict]:
        return [b for b in self.buildings if b["alive"]]

    def damage_building(self, building: dict) -> bool:
        building["hp"] -= 1
        if building["hp"] <= 0:
            building["alive"] = False
            return True
        return False

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
            })

    def draw(self, surface: pygame.Surface) -> None:
        if self._sky_cache:
            surface.blit(self._sky_cache, (0, 0))

        for c in self.clouds:
            c.draw(surface)

        if self.theme["name"] == "coast":
            self._draw_coast(surface)
        elif self.theme["name"] == "airfield":
            self._draw_airfield(surface)
        elif self.theme["name"] == "final":
            self._draw_final_sky(surface)
        elif self.theme["name"] == "storm":
            self._draw_storm(surface)
        else:
            self._draw_void(surface)

        for b in self.buildings:
            if b["alive"]:
                surface.blit(b["sprite"], (int(b["x"]), int(b["y"])))

    def _draw_coast(self, surface: pygame.Surface) -> None:
        water_y = LOGIC_H - 28
        for y in range(water_y, LOGIC_H):
            shade = int(30 + 15 * math.sin(self.time * 2 + y * 0.1))
            pygame.draw.line(surface, (20, 50 + shade, 90), (0, y), (LOGIC_W, y))
        pygame.draw.rect(surface, C_GROUND, (0, LOGIC_H - 28, LOGIC_W, 6))
        pygame.draw.rect(surface, C_GROUND_LIGHT, (0, LOGIC_H - 22, LOGIC_W, 22))

    def _draw_airfield(self, surface: pygame.Surface) -> None:
        runway_y = LOGIC_H - 96
        pygame.draw.polygon(surface, (31, 35, 40), [(0, LOGIC_H), (LOGIC_W, LOGIC_H), (LOGIC_W // 2 + 42, runway_y), (LOGIC_W // 2 - 42, runway_y)])
        for i in range(7):
            y = runway_y + i * 17 + int(self.time * 34) % 17
            width = 28 + i * 36
            pygame.draw.line(surface, (95, 112, 120), (LOGIC_W // 2 - width, y), (LOGIC_W // 2 + width, y), 1)
        for side in (-1, 1):
            for i in range(6):
                y = runway_y + i * 22
                x = LOGIC_W // 2 + side * (48 + i * 30)
                pygame.draw.circle(surface, (255, 205, 95), (x, y), 2)

    def _draw_final_sky(self, surface: pygame.Surface) -> None:
        for x, y, speed in self.stars:
            yy = int((y + self.time * speed * 22) % (LOGIC_H - 52))
            glow = int(100 + 100 * math.sin(self.time * 2 + x))
            pygame.draw.circle(surface, (glow, 80, 125), (x, yy), 1)
        horizon = LOGIC_H - 50
        for i in range(9):
            x = i * 48 + 8
            h = 14 + (i % 3) * 11
            pygame.draw.rect(surface, (30, 18, 35), (x, horizon - h, 32, h))
            pygame.draw.rect(surface, (255, 90, 48), (x + 6, horizon - h + 6, 3, 2))
        pygame.draw.rect(surface, (55, 22, 30), (0, horizon, LOGIC_W, 50))

    def _draw_storm(self, surface: pygame.Surface) -> None:
        horizon = LOGIC_H - 74
        # Soft cloud banks replace the old linear rain bands, which could look
        # like rendering artifacts on a scaled display.
        clouds = pygame.Surface((LOGIC_W, horizon), pygame.SRCALPHA)
        for row in range(4):
            y = 38 + row * 60 + int(math.sin(self.time * 0.7 + row) * 9)
            for col in range(7):
                x = col * 66 - 24 + int(math.sin(self.time * 0.35 + col) * 8)
                w, h = 78 + (col % 2) * 16, 26 + row * 5
                pygame.draw.ellipse(clouds, (35 + row * 8, 54 + row * 8, 68 + row * 7, 88), (x, y, w, h))
        surface.blit(clouds, (0, 0))
        # Distant lightning glow, intentionally soft rather than a hard line.
        glow = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.circle(glow, (205, 230, 255, int(20 + 15 * math.sin(self.time * 2) ** 2)), (50, 50), 45)
        surface.blit(glow, (LOGIC_W // 2 - 50, 54))
        pygame.draw.rect(surface, (32, 42, 48), (0, horizon, LOGIC_W, 74))

    def _draw_void(self, surface: pygame.Surface) -> None:
        for x, y, speed in self.stars:
            yy = int((y + self.time * speed * 38) % LOGIC_H)
            pygame.draw.circle(surface, (190, 110, 255), (x, yy), 1)
        r = 58
        eclipse = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        pygame.draw.circle(eclipse, (180, 70, 255, 75), (r, r), r)
        pygame.draw.circle(eclipse, (8, 4, 20, 255), (r - 9, r - 5), r - 11)
        surface.blit(eclipse, (LOGIC_W // 2 - r, 68))
        pygame.draw.rect(surface, (18, 8, 30), (0, LOGIC_H - 46, LOGIC_W, 46))
