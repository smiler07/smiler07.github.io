"""Bullet pool for player and enemy projectiles."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum, auto

import pygame

from src.config import ENEMY_BULLET_SPEED, LOGIC_H, LOGIC_W, PLAYER_BULLET_SPEED
from src.render.sprite_factory import SpriteFactory


class BulletOwner(Enum):
    PLAYER = auto()
    ENEMY = auto()


@dataclass
class Bullet:
    x: float
    y: float
    vx: float
    vy: float
    owner: BulletOwner
    damage: int = 1
    alive: bool = True
    kind: str = "normal"
    homing: bool = False

    @property
    def rect(self) -> pygame.Rect:
        if self.kind == "charge_l":
            r = 12
        elif self.kind == "charge_m":
            r = 9
        elif self.kind == "charge_s":
            r = 6
        elif self.kind == "heavy":
            r = 6
        elif self.kind in ("laser",):
            r = 2
        elif self.owner == BulletOwner.ENEMY:
            r = 4
        else:
            r = 3
        return pygame.Rect(int(self.x - r), int(self.y - r), r * 2, r * 2)


class BulletPool:
    def __init__(self) -> None:
        self.bullets: list[Bullet] = []

    def clear_enemy(self) -> None:
        self.bullets = [b for b in self.bullets if b.owner != BulletOwner.ENEMY]

    def clear_enemy_in_rects(self, rects: list[pygame.Rect]) -> None:
        for b in self.bullets:
            if b.owner != BulletOwner.ENEMY or not b.alive:
                continue
            for r in rects:
                if r.collidepoint(int(b.x), int(b.y)):
                    b.alive = False
                    break

    def spawn_player(
        self,
        x: float,
        y: float,
        angle: float = 0,
        kind: str = "normal",
        damage: int = 1,
        speed_mult: float = 1.0,
        homing: bool = False,
    ) -> None:
        rad = math.radians(angle)
        speed = PLAYER_BULLET_SPEED * speed_mult
        if angle == 0:
            vx, vy = math.sin(rad) * speed * 0.3, -speed
        else:
            vx = math.sin(rad) * speed * 0.5
            vy = -math.cos(rad) * speed
        self.bullets.append(Bullet(
            x, y - 8, vx, vy,
            BulletOwner.PLAYER,
            damage=damage,
            kind=kind,
            homing=homing or kind == "homing",
        ))

    def spawn_enemy(self, x: float, y: float, vx: float, vy: float) -> None:
        self.bullets.append(Bullet(x, y, vx, vy, BulletOwner.ENEMY))

    def spawn_enemy_aimed(self, x: float, y: float, tx: float, ty: float, speed: float = ENEMY_BULLET_SPEED) -> None:
        dx, dy = tx - x, ty - y
        dist = math.hypot(dx, dy) or 1
        self.spawn_enemy(x, y, dx / dist * speed, dy / dist * speed)

    def update(
        self,
        dt: float,
        enemies: list | None = None,
    ) -> None:
        alive = []
        for b in self.bullets:
            if not b.alive:
                continue
            if b.homing and b.owner == BulletOwner.PLAYER and enemies:
                target = _nearest_enemy(b.x, b.y, enemies)
                if target:
                    dx, dy = target.x - b.x, target.y - b.y
                    dist = math.hypot(dx, dy) or 1
                    steer = 0.08
                    b.vx += (dx / dist * PLAYER_BULLET_SPEED - b.vx) * steer
                    b.vy += (dy / dist * PLAYER_BULLET_SPEED - b.vy) * steer
            b.x += b.vx
            b.y += b.vy
            if b.x < -10 or b.x > LOGIC_W + 10 or b.y < -20 or b.y > LOGIC_H + 10:
                continue
            alive.append(b)
        self.bullets = alive

    def draw(self, surface: pygame.Surface) -> None:
        for b in self.bullets:
            if not b.alive:
                continue
            if b.owner == BulletOwner.PLAYER:
                surf = SpriteFactory.player_bullet_kind(b.kind)
            else:
                surf = SpriteFactory.enemy_bullet()
            surface.blit(surf, surf.get_rect(center=(int(b.x), int(b.y))))


def _nearest_enemy(x: float, y: float, enemies: list):
    best, best_d = None, float("inf")
    for e in enemies:
        if not e.alive:
            continue
        d = (e.x - x) ** 2 + (e.y - y) ** 2
        if d < best_d:
            best_d, best = d, e
    return best
