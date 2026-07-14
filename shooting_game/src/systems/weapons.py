"""Per-plane weapon firing patterns."""

from __future__ import annotations

from src.config import PLANES
from src.entities.bullet import BulletPool


def fire_weapon(pool: BulletPool, plane_id: str, x: float, y: float, power: int) -> None:
    info = PLANES[plane_id]
    weapon = info["weapon"]
    spread = info["shot_spread"]
    bullet_kind = info["bullet_kind"]
    sub_kind = info["sub_kind"]

    if weapon == "spread":
        _fire_spread(pool, x, y, power, spread, bullet_kind, sub_kind)
    elif weapon == "twin":
        _fire_twin(pool, x, y, power, bullet_kind, sub_kind)
    elif weapon == "rapid":
        _fire_rapid(pool, x, y, power, spread, bullet_kind, sub_kind)
    elif weapon == "heavy":
        _fire_heavy(pool, x, y, power, bullet_kind)
    elif weapon == "fan":
        _fire_fan(pool, x, y, power, spread, bullet_kind)
    elif weapon == "laser":
        _fire_laser(pool, x, y, power, bullet_kind)
    else:
        pool.spawn_player(x, y, kind=bullet_kind)


def fire_option(pool: BulletPool, plane_id: str, ox: float, oy: float, power: int) -> None:
    kind = PLANES[plane_id]["bullet_kind"]
    pool.spawn_player(ox, oy, kind=kind)


def fire_charge_shot(
    pool: BulletPool,
    plane_id: str,
    x: float,
    y: float,
    power: int,
    tier: int,
) -> None:
    """Fire a charged shot. tier 1 = medium, tier 2 = large."""
    info = PLANES[plane_id]
    weapon = info["weapon"]
    sub = info["sub_kind"]
    bullet = info["bullet_kind"]
    kind = "charge_s" if tier == 1 else "charge_m" if tier == 2 else "charge_l"
    base_dmg = (3 + power // 2) if tier == 1 else (5 + power)
    speed = 11.0 if tier == 1 else 13.0

    if weapon == "spread":
        pool.spawn_player(x, y, kind=kind, damage=base_dmg, speed_mult=speed / 9.0)
        if tier >= 2:
            pool.spawn_player(x - 14, y, -8, kind=sub, damage=3, speed_mult=1.1)
            pool.spawn_player(x + 14, y, 8, kind=sub, damage=3, speed_mult=1.1)
    elif weapon == "twin":
        pool.spawn_player(x - 8, y, kind=kind, damage=base_dmg, speed_mult=speed / 9.0)
        pool.spawn_player(x + 8, y, kind=kind, damage=base_dmg, speed_mult=speed / 9.0)
        if tier >= 2:
            pool.spawn_player(x, y, 0, kind=sub, damage=4, homing=True, speed_mult=1.0)
    elif weapon == "rapid":
        pool.spawn_player(x, y, kind=kind, damage=base_dmg, speed_mult=speed / 9.0)
        for off in (-10, 10) if tier >= 2 else ():
            pool.spawn_player(x + off, y, 0, kind=bullet, damage=2)
    elif weapon == "heavy":
        pool.spawn_player(x, y, kind="charge_l" if tier >= 2 else kind, damage=base_dmg + 2, speed_mult=0.9)
        if tier >= 2:
            pool.spawn_player(x, y - 6, 0, kind="heavy", damage=4, speed_mult=0.85)
    elif weapon == "fan":
        angles = [-15, 0, 15] if tier == 1 else [-25, -12, 0, 12, 25]
        for ang in angles:
            pool.spawn_player(x, y, ang, kind=kind if ang == 0 else bullet, damage=base_dmg if ang == 0 else 2)
    elif weapon == "laser":
        pool.spawn_player(x, y, kind="charge_l", damage=base_dmg + 2, speed_mult=1.6)
        if tier >= 2:
            pool.spawn_player(x - 10, y, kind="laser", damage=3, speed_mult=1.5)
            pool.spawn_player(x + 10, y, kind="laser", damage=3, speed_mult=1.5)
    else:
        pool.spawn_player(x, y, kind=kind, damage=base_dmg, speed_mult=speed / 9.0)


def fire_formation(pool: BulletPool, plane_id: str, x: float, y: float, options: list) -> None:
    info = PLANES[plane_id]
    sub = info["sub_kind"]
    weapon = info["weapon"]

    if weapon == "laser":
        for angle in [-8, 0, 8]:
            pool.spawn_player(x, y, angle, kind="laser", damage=4, speed_mult=1.3)
    elif weapon == "fan":
        for angle in range(-40, 41, 10):
            pool.spawn_player(x, y, angle, kind="pellet", damage=3)
    elif weapon == "heavy":
        for angle in [-10, 0, 10]:
            pool.spawn_player(x, y, angle, kind="heavy", damage=4)
    else:
        for angle in [-30, -15, 0, 15, 30]:
            pool.spawn_player(x, y, angle, kind=sub, damage=3)

    for opt in options:
        ox, oy = opt.lag_x, opt.lag_y
        for angle in [-20, 0, 20]:
            pool.spawn_player(ox, oy, angle, kind=sub, damage=2)


def _fire_spread(pool, x, y, power, spread, kind, sub):
    if power == 0:
        pool.spawn_player(x, y, kind=kind)
    elif power == 1:
        pool.spawn_player(x - 8, y, kind=kind)
        pool.spawn_player(x + 8, y, kind=kind)
    elif power == 2:
        pool.spawn_player(x, y, kind=kind)
        pool.spawn_player(x - 12, y, -spread, kind=kind)
        pool.spawn_player(x + 12, y, spread, kind=kind)
    else:
        pool.spawn_player(x, y, kind=kind)
        pool.spawn_player(x - 14, y, -spread, kind=kind)
        pool.spawn_player(x + 14, y, spread, kind=kind)
        if power >= 3:
            pool.spawn_player(x, y - 4, 0, kind=sub, damage=2)
        if power >= 4:
            pool.spawn_player(x - 6, y, -spread // 2, kind=sub, damage=2)
            pool.spawn_player(x + 6, y, spread // 2, kind=sub, damage=2)


def _fire_twin(pool, x, y, power, kind, sub):
    offsets = [(-10, 0), (10, 0)]
    if power >= 2:
        offsets = [(-12, 0), (12, 0), (0, -4)]
    if power >= 4:
        offsets.append((-6, -6))
        offsets.append((6, -6))
    for ox, oy in offsets:
        pool.spawn_player(x + ox, y + oy, kind=kind)
    if power >= 3:
        pool.spawn_player(x, y - 6, 0, kind=sub, damage=2, homing=True)


def _fire_rapid(pool, x, y, power, spread, kind, sub):
    count = 1 + power
    for i in range(count):
        off = (i - count // 2) * 5
        angle = 0 if power < 2 else (spread if i % 2 else -spread) * (i > 0)
        pool.spawn_player(x + off, y, angle, kind=kind)
    if power >= 3:
        pool.spawn_player(x, y - 4, 0, kind=sub, damage=2, homing=True)


def _fire_heavy(pool, x, y, power, kind):
    dmg = 2 if power >= 2 else 1
    if power == 0:
        pool.spawn_player(x, y, kind=kind, damage=dmg, speed_mult=0.75)
    elif power == 1:
        pool.spawn_player(x - 8, y, kind=kind, damage=dmg, speed_mult=0.75)
        pool.spawn_player(x + 8, y, kind=kind, damage=dmg, speed_mult=0.75)
    else:
        for ox in (-12, 0, 12)[:1 + power // 2]:
            pool.spawn_player(x + ox, y, kind=kind, damage=dmg, speed_mult=0.8)


def _fire_fan(pool, x, y, power, spread, kind):
    rays = 3 + power
    step = spread / max(rays - 1, 1)
    start = -spread / 2
    for i in range(rays):
        pool.spawn_player(x, y, start + step * i, kind=kind, damage=1)


def _fire_laser(pool, x, y, power, kind):
    beams = 1 + power // 2
    for i in range(beams):
        off = (i - beams // 2) * 8
        pool.spawn_player(x + off, y, kind=kind, damage=1 + power // 3, speed_mult=1.4)
