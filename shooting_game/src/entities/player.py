"""Player aircraft with power levels, options, bombs, charge shots."""

from __future__ import annotations

import math
from dataclasses import dataclass

import pygame

from src.config import (
    CHARGE_SHOT_MID,
    CHARGE_SHOT_START,
    CHARGE_TIME,
    LOGIC_H,
    LOGIC_W,
    MAX_BOMBS,
    MAX_POWER,
    PLANES,
    PLAYER_HIT_RADIUS,
    PLAYER_SPEED,
    PLAYER_SLOW_MULT,
)
from src.entities.bullet import BulletPool
from src.render.sprite_factory import SpriteFactory
from src.systems.weapons import fire_charge_shot, fire_formation, fire_option, fire_weapon


@dataclass
class FireResult:
    formation: bool = False
    charge_tier: int = 0  # 0=none, 1=medium, 2=large


@dataclass
class OptionDrone:
    offset_x: float
    offset_y: float
    lag_x: float = 0.0
    lag_y: float = 0.0

    def update_position(self, px: float, py: float, speed: float = 0.12) -> tuple[float, float]:
        target_x = px + self.offset_x
        target_y = py + self.offset_y
        self.lag_x += (target_x - self.lag_x) * speed
        self.lag_y += (target_y - self.lag_y) * speed
        return self.lag_x, self.lag_y


class Player:
    def __init__(self, plane_id: str = "p38") -> None:
        self.plane_id = plane_id
        self.info = PLANES[plane_id]
        self.x = LOGIC_W / 2
        self.y = LOGIC_H - 80
        self.power = 0
        self.bombs = 3
        self.lives = 3
        self.alive = True
        self.invuln = 0.0
        self.shoot_cooldown = 0.0
        self.charge_time = 0.0
        self.charging = False
        self.formation_active = 0.0
        self.options: list[OptionDrone] = []
        self._history: list[tuple[float, float]] = []
        self._charge_pulse = 0.0

    @property
    def rect(self) -> pygame.Rect:
        r = PLAYER_HIT_RADIUS
        return pygame.Rect(int(self.x - r), int(self.y - r), r * 2, r * 2)

    @property
    def hit_rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x - 14), int(self.y - 14), 28, 28)

    @property
    def bomb_id(self) -> str:
        return self.info["bomb_id"]

    @property
    def charge_ratio(self) -> float:
        return min(1.0, self.charge_time / CHARGE_TIME)

    @property
    def is_gathering(self) -> bool:
        """Holding fire long enough that normal shots stop and energy gathers."""
        return self.charging and self.charge_time >= CHARGE_SHOT_START

    @property
    def charge_tier_preview(self) -> int:
        if self.charge_time < CHARGE_SHOT_START:
            return 0
        if self.charge_time < CHARGE_SHOT_MID:
            return 1
        if self.charge_time < CHARGE_TIME:
            return 2
        return 3  # formation ready

    def reset_position(self) -> None:
        self.x = LOGIC_W / 2
        self.y = LOGIC_H - 80
        self.invuln = 2.5
        self.charge_time = 0.0
        self.charging = False

    def _sync_options(self) -> None:
        while len(self.options) < self.power:
            idx = len(self.options)
            side = -1 if idx % 2 == 0 else 1
            layer = idx // 2 + 1
            self.options.append(OptionDrone(side * 20 * layer, -10 * layer))
        while len(self.options) > self.power:
            self.options.pop()

    def power_up(self) -> None:
        if self.power < MAX_POWER:
            self.power += 1
            self._sync_options()

    def power_down(self) -> None:
        self.power = 0
        self.options.clear()

    def add_bomb(self) -> int:
        if self.bombs < MAX_BOMBS:
            self.bombs += 1
            return 0
        return 10_000

    def move(self, dx: float, dy: float, slow: bool) -> None:
        if not self.alive:
            return
        speed = PLAYER_SPEED * self.info["speed_mult"]
        if slow:
            speed *= PLAYER_SLOW_MULT
        self.x = max(16, min(LOGIC_W - 16, self.x + dx * speed))
        self.y = max(30, min(LOGIC_H - 20, self.y + dy * speed))
        self._history.append((self.x, self.y))
        if len(self._history) > 20:
            self._history.pop(0)

    def update(self, dt: float, fire_held: bool, fire_released: bool) -> FireResult:
        result = FireResult()
        if self.invuln > 0:
            self.invuln -= dt
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt
        if self.formation_active > 0:
            self.formation_active -= dt

        if self.is_gathering:
            self._charge_pulse += dt * 8

        if fire_held:
            self.charging = True
            self.charge_time += dt
        else:
            self.charging = False

        if fire_released and self.charge_time > 0:
            if self.charge_time >= CHARGE_TIME:
                result.formation = True
                self.formation_active = 1.5
            elif self.charge_time >= CHARGE_SHOT_START:
                result.charge_tier = 1 if self.charge_time < CHARGE_SHOT_MID else 2
            self.charge_time = 0.0
            self.charging = False
            self._charge_pulse = 0.0

        return result

    def shoot(self, pool: BulletPool) -> tuple[bool, str]:
        if not self.alive or self.shoot_cooldown > 0 or self.is_gathering:
            return False, ""
        fire_weapon(pool, self.plane_id, self.x, self.y, self.power)
        for opt in self.options:
            ox, oy = opt.update_position(self.x, self.y)
            fire_option(pool, self.plane_id, ox, oy, self.power)

        rate = self.info["fire_rate"]
        if self.power >= 3:
            rate *= 0.85
        self.shoot_cooldown = rate
        return True, self.info["weapon"]

    def fire_charge(self, pool: BulletPool, tier: int) -> None:
        fire_charge_shot(pool, self.plane_id, self.x, self.y, self.power, tier)
        for opt in self.options:
            if tier >= 2:
                ox, oy = opt.lag_x, opt.lag_y
                kind = "charge_s" if tier == 1 else "charge_m"
                pool.spawn_player(ox, oy, kind=kind, damage=2 + self.power, speed_mult=1.1)

    def fire_formation(self, pool: BulletPool) -> None:
        fire_formation(pool, self.plane_id, self.x, self.y, self.options)

    def use_bomb(self, pool: BulletPool) -> bool:
        if self.bombs <= 0 or not self.alive:
            return False
        self.bombs -= 1
        pool.clear_enemy()
        self.invuln = 2.0
        return True

    def hit(self) -> str:
        if self.invuln > 0:
            return "invuln"
        if self.power > 0:
            self.power_down()
            self.invuln = 2.0
            return "power_down"
        self.lives -= 1
        if self.lives <= 0:
            self.alive = False
            return "death"
        self.power_down()
        self.reset_position()
        return "respawn"

    def draw(self, surface: pygame.Surface) -> None:
        if not self.alive:
            return
        if self.invuln > 0 and int(self.invuln * 10) % 2 == 0:
            return

        for opt in self.options:
            ox, oy = opt.update_position(self.x, self.y)
            surf = SpriteFactory.option_drone(self.plane_id)
            surface.blit(surf, surf.get_rect(center=(int(ox), int(oy))))

        if self.is_gathering:
            self._draw_charge_aura(surface)

        surf = SpriteFactory.plane(self.plane_id)
        surface.blit(surf, surf.get_rect(center=(int(self.x), int(self.y))))

    def _draw_charge_aura(self, surface: pygame.Surface) -> None:
        ratio = self.charge_ratio
        tier = self.charge_tier_preview
        pulse = math.sin(self._charge_pulse) * 0.15

        # Color ramps: yellow → cyan → white as charge builds
        if tier <= 1:
            color = (255, int(200 - 80 * ratio), 80)
        elif tier == 2:
            color = (int(100 + 155 * ratio), 220, 255)
        else:
            color = (255, 255, 200)

        base_r = int(18 + ratio * 28 + pulse * 8)
        for i in range(3):
            r = base_r + i * 6
            alpha = int((120 - i * 30) * ratio)
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*color, alpha), (r, r), r, 2)
            surface.blit(s, (int(self.x - r), int(self.y - r - 8)))

        # Energy orbs spiraling inward
        for i in range(4):
            ang = self._charge_pulse + i * (math.tau / 4)
            dist = 24 - ratio * 10
            ox = self.x + math.cos(ang) * dist
            oy = self.y - 8 + math.sin(ang) * dist * 0.6
            pygame.draw.circle(surface, (*color, int(180 * ratio)), (int(ox), int(oy)), 3)

        # Charge tier text hint rings
        if tier >= 2:
            pygame.draw.circle(surface, (255, 255, 255, int(80 + pulse * 40)),
                               (int(self.x), int(self.y - 8)), base_r + 4, 1)
