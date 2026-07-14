"""Procedural sprite generation — cohesive WWII shmup aesthetic."""

from __future__ import annotations

import math
from typing import Callable

import pygame

from src.config import (
    C_BOMB,
    C_ENEMY_ACCENT,
    C_ENEMY_BOMBER,
    C_ENEMY_BODY,
    C_ENEMY_BULLET,
    C_ENEMY_BULLET_CORE,
    C_ENEMY_RED_BODY,
    C_ENEMY_RED_RING,
    C_ENEMY_WING,
    C_GOLD,
    C_PLAYER_BULLET,
    C_PLAYER_BULLET_CORE,
    C_POWER,
)


def _glow_circle(
    radius: int,
    core: tuple[int, int, int],
    glow: tuple[int, int, int],
    alpha: int = 200,
) -> pygame.Surface:
    size = radius * 4
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    for r in range(radius * 2, 0, -1):
        t = r / (radius * 2)
        color = (
            int(glow[0] * t + core[0] * (1 - t)),
            int(glow[1] * t + core[1] * (1 - t)),
            int(glow[2] * t + core[2] * (1 - t)),
            int(alpha * (1 - t * 0.5)),
        )
        pygame.draw.circle(surf, color, (cx, cy), r)
    pygame.draw.circle(surf, (*core, 255), (cx, cy), max(1, radius // 2))
    return surf


class SpriteFactory:
    """Cache of procedurally drawn sprites."""

    _cache: dict[str, pygame.Surface] = {}

    @classmethod
    def get(cls, key: str, factory: Callable[[], pygame.Surface]) -> pygame.Surface:
        if key not in cls._cache:
            cls._cache[key] = factory()
        return cls._cache[key]

    @classmethod
    def player_bullet_kind(cls, kind: str) -> pygame.Surface:
        return cls.get(f"pb_{kind}", lambda: cls._draw_player_bullet(kind))

    @classmethod
    def _draw_player_bullet(cls, kind: str) -> pygame.Surface:
        specs = {
            "normal": ((255, 255, 255), (120, 220, 255), 3),
            "cyan": ((255, 255, 255), (80, 200, 255), 3),
            "silver": ((255, 255, 255), (180, 190, 210), 3),
            "green": ((220, 255, 200), (80, 220, 80), 3),
            "heavy": ((255, 240, 150), (255, 160, 40), 6),
            "pellet": ((255, 220, 180), (255, 120, 60), 3),
            "laser": ((255, 200, 200), (255, 60, 80), 2),
            "rocket": None,
            "homing": None,
        }
        if kind in ("rocket",):
            return cls.rocket()
        if kind in ("homing",):
            return cls.homing_missile()
        if kind.startswith("charge"):
            return cls._draw_charge_bullet(kind)
        core, glow, r = specs.get(kind, specs["normal"])
        return _glow_circle(r, core, glow)

    @classmethod
    def _draw_charge_bullet(cls, kind: str) -> pygame.Surface:
        tiers = {
            "charge_s": (6, (255, 240, 200), (255, 180, 80)),
            "charge_m": (9, (255, 255, 255), (120, 220, 255)),
            "charge_l": (12, (255, 255, 255), (255, 120, 60)),
        }
        r, core, glow = tiers.get(kind, tiers["charge_m"])
        s = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
        cx, cy = r * 2, r * 2
        for ring in range(r * 2, 0, -1):
            t = ring / (r * 2)
            color = (
                int(glow[0] * t + core[0] * (1 - t)),
                int(glow[1] * t + core[1] * (1 - t)),
                int(glow[2] * t + core[2] * (1 - t)),
                int(220 * (1 - t * 0.3)),
            )
            pygame.draw.circle(s, color, (cx, cy), ring)
        pygame.draw.circle(s, (*core, 255), (cx, cy), max(2, r // 2))
        return s

    @classmethod
    def player_bullet(cls) -> pygame.Surface:
        return cls.player_bullet_kind("normal")

    @classmethod
    def enemy_bullet(cls) -> pygame.Surface:
        return cls.get("eb", lambda: _glow_circle(4, C_ENEMY_BULLET_CORE, C_ENEMY_BULLET))

    @classmethod
    def rocket(cls) -> pygame.Surface:
        def _make() -> pygame.Surface:
            s = pygame.Surface((8, 16), pygame.SRCALPHA)
            pygame.draw.polygon(s, (255, 140, 60, 230), [(4, 0), (7, 14), (4, 12), (1, 14)])
            pygame.draw.polygon(s, (255, 220, 100, 255), [(4, 2), (5, 10), (4, 9), (3, 10)])
            return s

        return cls.get("rocket", _make)

    @classmethod
    def homing_missile(cls) -> pygame.Surface:
        def _make() -> pygame.Surface:
            s = pygame.Surface((10, 14), pygame.SRCALPHA)
            pygame.draw.polygon(s, (100, 200, 255, 240), [(5, 0), (9, 12), (5, 10), (1, 12)])
            pygame.draw.circle(s, (200, 240, 255, 255), (5, 4), 2)
            return s

        return cls.get("homing", _make)

    @classmethod
    def plane(cls, plane_id: str) -> pygame.Surface:
        return cls.get(f"plane_{plane_id}", lambda: cls._draw_plane(plane_id))

    @classmethod
    def _draw_plane(cls, plane_id: str) -> pygame.Surface:
        from src.config import PLANES

        info = PLANES[plane_id]
        body, accent = info["color"], info["accent"]
        s = pygame.Surface((40, 40), pygame.SRCALPHA)

        if plane_id == "p38":
            pygame.draw.polygon(s, body, [(20, 2), (28, 18), (26, 36), (20, 30), (14, 36), (12, 18)])
            pygame.draw.polygon(s, accent, [(20, 6), (24, 16), (20, 26), (16, 16)])
            pygame.draw.rect(s, body, (8, 14, 6, 20), border_radius=2)
            pygame.draw.rect(s, body, (26, 14, 6, 20), border_radius=2)
            pygame.draw.circle(s, (255, 200, 80, 200), (20, 8), 3)
        elif plane_id == "p51":
            pygame.draw.ellipse(s, body, (6, 16, 28, 10))
            pygame.draw.polygon(s, accent, [(20, 4), (26, 20), (20, 30), (14, 20)])
            pygame.draw.rect(s, (100, 105, 115), (17, 18, 6, 14), border_radius=2)
            pygame.draw.circle(s, (255, 200, 80, 200), (20, 10), 2)
        elif plane_id == "spitfire":
            pygame.draw.ellipse(s, body, (4, 14, 32, 12))
            pygame.draw.polygon(s, accent, [(20, 4), (24, 22), (20, 28), (16, 22)])
            pygame.draw.ellipse(s, (60, 80, 50), (10, 16, 20, 6))
            pygame.draw.circle(s, (255, 200, 80, 200), (20, 10), 2)
        elif plane_id == "bf109":
            pygame.draw.ellipse(s, body, (8, 15, 24, 11))
            pygame.draw.polygon(s, accent, [(20, 3), (25, 18), (20, 28), (15, 18)])
            pygame.draw.rect(s, (70, 75, 65), (18, 14, 4, 16))
            pygame.draw.circle(s, (200, 50, 40), (20, 20), 3)
        elif plane_id == "zero":
            pygame.draw.ellipse(s, body, (2, 14, 36, 11))
            pygame.draw.polygon(s, accent, [(20, 5), (24, 20), (20, 30), (16, 20)])
            pygame.draw.circle(s, (200, 40, 35), (20, 18), 4)
            pygame.draw.line(s, (255, 255, 255), (12, 18), (28, 18), 1)
        elif plane_id == "shinden":
            pygame.draw.polygon(s, body, [(20, 2), (34, 22), (20, 34), (6, 22)])
            pygame.draw.polygon(s, accent, [(20, 8), (28, 22), (20, 28), (12, 22)])
            pygame.draw.rect(s, (80, 85, 95), (16, 16, 8, 14), border_radius=1)
            pygame.draw.circle(s, (255, 80, 50, 220), (20, 12), 3)
        else:
            pygame.draw.ellipse(s, body, (4, 14, 32, 12))
            pygame.draw.polygon(s, accent, [(20, 4), (24, 22), (20, 28), (16, 22)])

        # Outline for crisp look
        mask = pygame.mask.from_surface(s)
        outline = mask.to_surface(setcolor=(255, 255, 255, 80), unsetcolor=(0, 0, 0, 0))
        s.blit(outline, (-1, 0))
        return s

    @classmethod
    def _outline(cls, s: pygame.Surface, color: tuple = (0, 0, 0)) -> pygame.Surface:
        mask = pygame.mask.from_surface(s)
        outline = mask.to_surface(setcolor=(*color, 220), unsetcolor=(0, 0, 0, 0))
        result = pygame.Surface(s.get_size(), pygame.SRCALPHA)
        result.blit(outline, (1, 1))
        result.blit(s, (0, 0))
        return result

    @classmethod
    def enemy_fighter(cls, red: bool = False) -> pygame.Surface:
        key = "enemy_fighter_red_v2" if red else "enemy_fighter_v2"
        return cls.get(key, lambda: cls._draw_enemy_fighter(red))

    @classmethod
    def _draw_enemy_fighter(cls, red: bool) -> pygame.Surface:
        """Downward-facing enemy fighter — nose points toward player."""
        w, h = 36, 40
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        cx = w // 2

        body = C_ENEMY_RED_BODY if red else C_ENEMY_BODY
        wing = (140, 30, 25) if red else C_ENEMY_WING

        # Wings (wide, top of sprite — enemy flies down)
        pygame.draw.polygon(s, wing, [(cx, 10), (w - 2, 18), (cx, 22), (2, 18)])
        # Fuselage nose down
        pygame.draw.polygon(s, body, [(cx, 8), (cx + 8, 22), (cx + 4, h - 4), (cx - 4, h - 4), (cx - 8, 22)])
        # Cockpit canopy (dark)
        pygame.draw.ellipse(s, (15, 15, 20), (cx - 5, 14, 10, 12))
        # Engine exhaust glow (bottom = toward player)
        pygame.draw.ellipse(s, (255, 120, 40, 200), (cx - 5, h - 8, 10, 6))
        pygame.draw.ellipse(s, (255, 200, 80, 255), (cx - 3, h - 6, 6, 4))

        # Enemy insignia — red X on wings
        insignia = (220, 40, 40) if not red else (255, 255, 255)
        pygame.draw.line(s, insignia, (cx - 10, 14), (cx - 4, 18), 2)
        pygame.draw.line(s, insignia, (cx - 4, 14), (cx - 10, 18), 2)
        pygame.draw.line(s, insignia, (cx + 4, 14), (cx + 10, 18), 2)
        pygame.draw.line(s, insignia, (cx + 10, 14), (cx + 4, 18), 2)

        if red:
            # Power-carrier marker (1945 style red plane ring)
            pygame.draw.circle(s, C_ENEMY_RED_RING, (cx, 20), 11, 2)
            pygame.draw.circle(s, (255, 80, 60, 180), (cx, 20), 7, 1)
            pygame.draw.line(s, (255, 255, 200), (cx, 16), (cx, 22), 2)
            pygame.draw.circle(s, (255, 255, 200), (cx, 24), 2)

        return cls._outline(s)

    @classmethod
    def enemy_bomber(cls) -> pygame.Surface:
        return cls.get("enemy_bomber_v2", cls._draw_enemy_bomber)

    @classmethod
    def _draw_enemy_bomber(cls) -> pygame.Surface:
        """Heavy bomber facing downward — large and menacing."""
        w, h = 52, 44
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        cx = w // 2

        # Wide wings
        pygame.draw.polygon(s, C_ENEMY_WING, [(cx, 12), (w - 2, 20), (cx, 26), (2, 20)])
        # Fat fuselage
        pygame.draw.ellipse(s, C_ENEMY_BOMBER, (cx - 10, 10, 20, h - 8))
        pygame.draw.rect(s, (40, 42, 50), (cx - 8, 16, 16, h - 18), border_radius=3)
        # Twin engine nacelles
        pygame.draw.ellipse(s, (35, 38, 45), (6, 18, 12, 18))
        pygame.draw.ellipse(s, (35, 38, 45), (w - 18, 18, 12, 18))
        # Propeller glow under each engine
        for ex in (12, w - 12):
            pygame.draw.circle(s, (255, 100, 30, 180), (ex, h - 6), 4)
            pygame.draw.circle(s, (255, 180, 60, 255), (ex, h - 6), 2)
        # Bomb bay doors
        pygame.draw.rect(s, (20, 20, 25), (cx - 6, h - 14, 12, 8), border_radius=1)
        pygame.draw.line(s, C_ENEMY_ACCENT, (cx - 4, h - 10), (cx + 4, h - 10), 1)
        # Skull-ish nose art
        pygame.draw.circle(s, (200, 50, 40), (cx, h - 4), 3)

        return cls._outline(s)

    @classmethod
    def enemy_by_kind(cls, kind: str) -> pygame.Surface:
        drawers = {
            "fighter": lambda: cls._draw_enemy_fighter(False),
            "fighter_red": lambda: cls._draw_enemy_fighter(True),
            "zero": cls._draw_enemy_zero,
            "bf109": cls._draw_enemy_bf109,
            "bomber": cls._draw_enemy_bomber,
            "stuka": cls._draw_enemy_stuka,
            "tank": cls._draw_enemy_tank,
            "heavy_tank": cls._draw_enemy_heavy_tank,
            "destroyer": cls._draw_enemy_destroyer,
            "pt_boat": cls._draw_enemy_pt_boat,
        }
        key = f"enemy_unit_{kind}"
        fn = drawers.get(kind, drawers["fighter"])
        return cls.get(key, fn)

    @classmethod
    def _draw_enemy_zero(cls) -> pygame.Surface:
        w, h = 34, 38
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        cx = w // 2
        pygame.draw.ellipse(s, (210, 215, 200), (2, 14, 30, 10))
        pygame.draw.polygon(s, (190, 195, 180), [(cx, 10), (cx + 6, 24), (cx, h - 4), (cx - 6, 24)])
        pygame.draw.circle(s, (15, 15, 20), (cx, 18), 4)
        pygame.draw.circle(s, (200, 40, 35), (cx, 20), 5, 1)
        pygame.draw.ellipse(s, (255, 110, 40, 200), (cx - 4, h - 7, 8, 5))
        return cls._outline(s)

    @classmethod
    def _draw_enemy_bf109(cls) -> pygame.Surface:
        w, h = 36, 40
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        cx = w // 2
        pygame.draw.polygon(s, C_ENEMY_WING, [(cx, 12), (w - 2, 20), (cx, 24), (2, 20)])
        pygame.draw.polygon(s, (75, 80, 70), [(cx, 10), (cx + 7, 22), (cx, h - 4), (cx - 7, 22)])
        pygame.draw.polygon(s, (230, 200, 50), [(cx, h - 6), (cx + 4, h - 2), (cx - 4, h - 2)])
        pygame.draw.ellipse(s, (20, 20, 25), (cx - 4, 16, 8, 9))
        pygame.draw.line(s, (200, 50, 40), (cx - 8, 18), (cx + 8, 18), 1)
        return cls._outline(s)

    @classmethod
    def _draw_enemy_stuka(cls) -> pygame.Surface:
        w, h = 40, 42
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        cx = w // 2
        pygame.draw.polygon(s, (65, 70, 75), [(cx, 14), (4, 22), (cx, 26), (w - 4, 22)])
        pygame.draw.polygon(s, (85, 90, 95), [(cx, 8), (cx + 6, 20), (cx, h - 4), (cx - 6, 20)])
        pygame.draw.rect(s, (50, 55, 60), (cx - 3, 10, 6, 18))
        pygame.draw.line(s, (40, 40, 45), (cx - 8, 28), (cx - 8, h - 2), 2)
        pygame.draw.line(s, (40, 40, 45), (cx + 8, 28), (cx + 8, h - 2), 2)
        pygame.draw.circle(s, (200, 50, 40), (cx, h - 3), 3)
        return cls._outline(s)

    @classmethod
    def _draw_enemy_tank(cls) -> pygame.Surface:
        w, h = 38, 44
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        cx = w // 2
        pygame.draw.rect(s, (45, 50, 42), (4, 28, w - 8, 14), border_radius=3)
        for i in range(6):
            pygame.draw.circle(s, (30, 32, 28), (8 + i * 5, 36), 3)
        pygame.draw.rect(s, (60, 65, 55), (8, 16, w - 16, 16), border_radius=2)
        pygame.draw.rect(s, (50, 55, 48), (cx - 4, 8, 8, 20))
        pygame.draw.rect(s, (40, 42, 38), (cx - 2, 4, 4, 10))
        pygame.draw.circle(s, (200, 50, 40, 200), (cx, h - 4), 3)
        return cls._outline(s)

    @classmethod
    def _draw_enemy_heavy_tank(cls) -> pygame.Surface:
        w, h = 48, 52
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        cx = w // 2
        pygame.draw.rect(s, (38, 42, 38), (2, 34, w - 4, 16), border_radius=4)
        for i in range(8):
            pygame.draw.circle(s, (25, 28, 24), (6 + i * 5, 42), 3)
        pygame.draw.rect(s, (55, 60, 52), (6, 18, w - 12, 20), border_radius=3)
        pygame.draw.rect(s, (45, 50, 42), (cx - 5, 6, 10, 24))
        pygame.draw.polygon(s, (70, 75, 65), [(cx, 20), (cx + 14, 24), (cx + 14, 28), (cx, 26)])
        return cls._outline(s)

    @classmethod
    def _draw_enemy_destroyer(cls) -> pygame.Surface:
        w, h = 56, 48
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        cx = w // 2
        pygame.draw.polygon(s, (50, 55, 65), [(cx, 6), (w - 4, 28), (cx + 8, h - 4), (cx - 8, h - 4), (4, 28)])
        pygame.draw.rect(s, (40, 45, 55), (cx - 6, 14, 12, 20))
        for tx in (cx - 16, cx, cx + 16):
            pygame.draw.rect(s, (70, 75, 85), (tx - 2, 18, 4, 8))
        pygame.draw.circle(s, (200, 50, 40, 180), (cx, h - 6), 4)
        return cls._outline(s)

    @classmethod
    def _draw_enemy_pt_boat(cls) -> pygame.Surface:
        w, h = 36, 40
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        cx = w // 2
        pygame.draw.polygon(s, (55, 58, 50), [(cx, 8), (w - 2, 24), (cx + 4, h - 4), (cx - 4, h - 4), (2, 24)])
        pygame.draw.rect(s, (40, 42, 38), (cx - 2, 12, 4, 14))
        pygame.draw.circle(s, (255, 100, 40, 200), (cx - 10, 28), 3)
        pygame.draw.circle(s, (255, 100, 40, 200), (cx + 10, 28), 3)
        return cls._outline(s)

    @classmethod
    def boss(cls, boss_id: str = "tank") -> pygame.Surface:
        return cls.get(f"boss_{boss_id}_v2", lambda: cls._draw_boss(boss_id))

    @classmethod
    def _draw_boss(cls, boss_id: str) -> pygame.Surface:
        if boss_id == "fortress":
            return cls._draw_boss_fortress()
        if boss_id == "ace":
            return cls._draw_boss_ace()
        return cls._draw_boss_tank()

    @classmethod
    def _draw_boss_tank(cls) -> pygame.Surface:
        s = pygame.Surface((88, 72), pygame.SRCALPHA)
        # Treads
        pygame.draw.rect(s, (35, 38, 45), (4, 48, 80, 20), border_radius=4)
        pygame.draw.rect(s, (50, 52, 60), (8, 52, 72, 12), border_radius=2)
        for i in range(8):
            pygame.draw.circle(s, (25, 28, 35), (14 + i * 10, 58), 4)
        # Hull
        pygame.draw.rect(s, (60, 65, 80), (12, 28, 64, 28), border_radius=4)
        pygame.draw.rect(s, (45, 50, 65), (20, 12, 48, 22), border_radius=3)
        # Core weak point
        pygame.draw.circle(s, (255, 50, 30, 240), (44, 40), 12)
        pygame.draw.circle(s, (255, 160, 50, 220), (44, 40), 7)
        # Cannons
        for tx in (22, 44, 66):
            pygame.draw.rect(s, (80, 85, 100), (tx - 3, 8, 6, 18))
            pygame.draw.rect(s, (30, 32, 40), (tx - 2, 4, 4, 8))
        return cls._outline(s, (0, 0, 0))

    @classmethod
    def _draw_boss_fortress(cls) -> pygame.Surface:
        s = pygame.Surface((96, 80), pygame.SRCALPHA)
        cx = 48
        # Massive wings
        pygame.draw.polygon(s, (40, 42, 55), [(cx, 16), (94, 30), (cx, 40), (2, 30)])
        pygame.draw.polygon(s, (55, 58, 72), [(cx, 20), (80, 30), (cx, 36), (16, 30)])
        # Body
        pygame.draw.ellipse(s, (50, 52, 68), (cx - 18, 18, 36, 56))
        pygame.draw.rect(s, (35, 38, 50), (cx - 14, 30, 28, 36), border_radius=4)
        # Four engines
        for ex in (16, 32, 64, 80):
            pygame.draw.ellipse(s, (30, 32, 42), (ex - 6, 50, 12, 16))
            pygame.draw.circle(s, (255, 90, 30, 200), (ex, 68), 5)
        # Tail gunner turret
        pygame.draw.circle(s, (70, 75, 90), (cx, 22), 8)
        pygame.draw.circle(s, (255, 60, 40, 220), (cx, 22), 4)
        return cls._outline(s, (0, 0, 0))

    @classmethod
    def _draw_boss_ace(cls) -> pygame.Surface:
        s = pygame.Surface((72, 72), pygame.SRCALPHA)
        cx = 36
        # Large ace fighter — aggressive downward V
        pygame.draw.polygon(s, (50, 20, 25), [(cx, 8), (68, 28), (cx, 36), (4, 28)])
        pygame.draw.polygon(s, (160, 35, 30), [(cx, 12), (cx + 22, 28), (cx, 58), (cx - 22, 28)])
        pygame.draw.polygon(s, (100, 25, 20), [(cx, 16), (cx + 10, 28), (cx, 48), (cx - 10, 28)])
        # Cockpit
        pygame.draw.ellipse(s, (10, 10, 15), (cx - 8, 24, 16, 14))
        # Triple exhaust
        for ox in (-8, 0, 8):
            pygame.draw.circle(s, (255, 100, 40, 220), (cx + ox, 64), 5)
            pygame.draw.circle(s, (255, 220, 100, 255), (cx + ox, 64), 2)
        # Ace marking
        pygame.draw.polygon(s, (255, 220, 60), [(cx, 30), (cx + 6, 42), (cx, 38), (cx - 6, 42)])
        return cls._outline(s, (0, 0, 0))

    @classmethod
    def enemy_shadow(cls, large: bool = False) -> pygame.Surface:
        key = "enemy_shadow_lg" if large else "enemy_shadow"
        def _make() -> pygame.Surface:
            w = 56 if large else 40
            s = pygame.Surface((w, 12), pygame.SRCALPHA)
            pygame.draw.ellipse(s, (0, 0, 0, 80), (0, 0, w, 12))
            return s
        return cls.get(key, _make)

    @classmethod
    def gold_bar(cls, size: str = "small") -> pygame.Surface:
        key = f"gold_{size}"
        return cls.get(key, lambda: cls._draw_gold_bar(size))

    @classmethod
    def _draw_gold_bar(cls, size: str) -> pygame.Surface:
        specs = {
            "small": (12, 8, (200, 150, 20), C_GOLD),
            "medium": (18, 12, (210, 160, 25), (255, 220, 70)),
            "large": (26, 16, (220, 170, 30), (255, 235, 100)),
        }
        w, h, dark, bright = specs.get(size, specs["small"])
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(s, dark, (0, 1, w, h - 2), border_radius=2)
        pygame.draw.rect(s, bright, (1, 2, w - 2, h - 4), border_radius=1)
        pygame.draw.line(s, (255, 250, 180, 220), (2, 3), (w - 3, 3), 1)
        if size == "large":
            pygame.draw.line(s, (255, 255, 220, 180), (3, h // 2), (w - 4, h // 2), 1)
        return s

    @classmethod
    def power_item(cls) -> pygame.Surface:
        def _make() -> pygame.Surface:
            s = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(s, (*C_POWER, 200), (10, 10), 9)
            pygame.draw.circle(s, (255, 120, 120, 255), (10, 10), 6)
            font = pygame.font.SysFont("arial", 12, bold=True)
            t = font.render("P", True, (255, 255, 255))
            s.blit(t, t.get_rect(center=(10, 10)))
            return s

        return cls.get("power", _make)

    @classmethod
    def bomb_item(cls) -> pygame.Surface:
        def _make() -> pygame.Surface:
            s = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(s, (*C_BOMB, 200), (10, 10), 9)
            pygame.draw.circle(s, (120, 200, 255, 255), (10, 10), 6)
            font = pygame.font.SysFont("arial", 12, bold=True)
            t = font.render("B", True, (255, 255, 255))
            s.blit(t, t.get_rect(center=(10, 10)))
            return s

        return cls.get("bomb", _make)

    @classmethod
    def building(cls, variant: int = 0) -> pygame.Surface:
        key = f"bld_{variant}"
        return cls.get(key, lambda: cls._draw_building(variant))

    @classmethod
    def _draw_building(cls, variant: int) -> pygame.Surface:
        w, h = 24 + variant * 8, 20 + variant * 12
        s = pygame.Surface((w, h), pygame.SRCALPHA)
        base = (55 + variant * 10, 48, 40)
        pygame.draw.rect(s, base, (0, h - 16, w, 16))
        pygame.draw.rect(s, (base[0] + 20, base[1] + 15, base[2] + 10), (2, h - 16 - variant * 8, w - 4, 8 + variant * 8))
        for i in range(2 + variant):
            pygame.draw.rect(s, (255, 200, 80, 120), (4 + i * 8, h - 12, 4, 4))
        return s

    @classmethod
    def option_drone(cls, plane_id: str) -> pygame.Surface:
        key = f"opt_{plane_id}"
        return cls.get(key, lambda: cls._draw_option(plane_id))

    @classmethod
    def _draw_option(cls, plane_id: str) -> pygame.Surface:
        from src.config import PLANES

        accent = PLANES[plane_id]["accent"]
        s = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(s, (*accent, 200), (8, 8), 7)
        pygame.draw.circle(s, (255, 255, 255, 180), (8, 8), 3)
        return s
