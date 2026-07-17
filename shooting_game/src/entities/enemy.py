"""Enemy entities, wave spawner, and per-stage boss."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from enum import Enum, auto

import pygame

from src.config import LOGIC_H, LOGIC_W
from src.data.stages import STAGES
from src.entities.item import ItemType, random_treasure
from src.render.sprite_factory import SpriteFactory

# kind string → stats: hp, vy, shoot_interval, score, category
ENEMY_KINDS: dict[str, dict] = {
    "fighter":      {"hp": 2, "vy": 1.8, "interval": 2.0, "score": 300,  "cat": "air", "gold_drop": 0.12},
    "fighter_red":  {"hp": 2, "vy": 1.6, "interval": 2.5, "score": 500,  "cat": "air", "gold_drop": 0.20},
    "zero":         {"hp": 2, "vy": 2.2, "interval": 1.6, "score": 400,  "cat": "air", "gold_drop": 0.14},
    "bf109":        {"hp": 3, "vy": 1.7, "interval": 2.2, "score": 450,  "cat": "air", "gold_drop": 0.18},
    "bomber":       {"hp": 4, "vy": 1.0, "interval": 3.0, "score": 800,  "cat": "air", "gold_drop": 0.32},
    "stuka":        {"hp": 3, "vy": 2.4, "interval": 2.8, "score": 600,  "cat": "air", "gold_drop": 0.24},
    "spark_drone":  {"hp": 2, "vy": 2.5, "interval": 1.4, "score": 360,  "cat": "air", "gold_drop": 0.16},
    "orbiter":      {"hp": 3, "vy": 1.9, "interval": 1.7, "score": 560,  "cat": "air", "gold_drop": 0.20},
    "comet":        {"hp": 4, "vy": 1.35,"interval": 2.1, "score": 760,  "cat": "air", "gold_drop": 0.28},
    "tank":         {"hp": 5, "vy": 0.7, "interval": 2.5, "score": 700,  "cat": "ground"},
    "heavy_tank":   {"hp": 8, "vy": 0.5, "interval": 3.0, "score": 1200, "cat": "ground"},
    "destroyer":    {"hp": 10, "vy": 0.6, "interval": 2.0, "score": 1500, "cat": "naval"},
    "pt_boat":      {"hp": 3, "vy": 1.2, "interval": 1.5, "score": 500,  "cat": "naval"},
}


class EnemyCategory(Enum):
    AIR = auto()
    GROUND = auto()
    NAVAL = auto()
    BOSS = auto()


class EnemyCategory(Enum):
    AIR = auto()
    GROUND = auto()
    NAVAL = auto()
    BOSS = auto()


@dataclass
class Enemy:
    x: float
    y: float
    type_id: str
    hp: int
    max_hp: int
    vx: float = 0.0
    vy: float = 1.5
    shoot_timer: float = 0.0
    shoot_interval: float = 1.8
    alive: bool = True
    score: int = 500
    invuln: float = 0.0
    boss_phase: int = 0
    boss_id: str = "tank"
    category: EnemyCategory = EnemyCategory.AIR

    @property
    def is_boss(self) -> bool:
        return self.type_id == "boss"

    @property
    def rect(self) -> pygame.Rect:
        if self.is_boss:
            if self.boss_id == "final":
                return pygame.Rect(int(self.x - 90), int(self.y - 72), 180, 144)
            return pygame.Rect(int(self.x - 60), int(self.y - 50), 120, 100)
        sizes = {
            "bomber": (22, 18), "stuka": (20, 18), "heavy_tank": (24, 24),
            "destroyer": (28, 22), "tank": (19, 20), "pt_boat": (18, 18),
            "bf109": (14, 16), "zero": (12, 16),
            "spark_drone": (15, 15), "orbiter": (17, 17), "comet": (20, 18),
        }
        rw, rh = sizes.get(self.type_id, (14, 16))
        return pygame.Rect(int(self.x - rw), int(self.y - rh), rw * 2, rh * 2)

    @property
    def drops(self) -> list[tuple[ItemType, int]]:
        drops: list[tuple[ItemType, int]] = []
        # Gold comes only from aircraft defeats, with better odds for tougher air units.
        if self.category == EnemyCategory.AIR:
            chance = ENEMY_KINDS[self.type_id].get("gold_drop", 0.0)
            if random.random() < chance:
                drops.append(random_treasure())
        if self.type_id == "fighter_red":
            drops.append((ItemType.POWER, 0))
        if self.type_id == "bomber" and random.random() < 0.35:
            drops.append((ItemType.BOMB, 0))
        if self.type_id in ("tank", "heavy_tank") and random.random() < 0.25:
            drops.append((ItemType.BOMB, 0))
        if self.is_boss:
            drops.extend([(ItemType.POWER, 0), (ItemType.BOMB, 0)])
        return drops

    def sprite(self) -> pygame.Surface:
        if self.is_boss:
            return SpriteFactory.boss(self.boss_id)
        return SpriteFactory.enemy_by_kind(self.type_id)

    @property
    def is_large(self) -> bool:
        return self.type_id in ("bomber", "heavy_tank", "destroyer", "boss")


def make_enemy(type_id: str, x: float, y: float, boss_id: str = "tank", boss_hp: int = 80) -> Enemy:
    if type_id == "boss":
        return Enemy(
            x, y, "boss", boss_hp, boss_hp,
            vy=0.3, shoot_interval=1.0, score=50000,
            boss_id=boss_id, category=EnemyCategory.BOSS,
        )
    spec = ENEMY_KINDS.get(type_id, ENEMY_KINDS["fighter"])
    cat_map = {"air": EnemyCategory.AIR, "ground": EnemyCategory.GROUND, "naval": EnemyCategory.NAVAL}
    return Enemy(
        x, y, type_id, spec["hp"], spec["hp"],
        vy=spec["vy"], shoot_interval=spec["interval"], score=spec["score"],
        category=cat_map[spec["cat"]],
    )


class WaveSpawner:
    def __init__(self, stage_index: int = 0) -> None:
        self.stage_index = stage_index
        self.stage_data = STAGES[stage_index]
        self.events: list[dict] = self.stage_data["events"]
        self.elapsed = 0.0
        self.event_index = 0
        self.enemies: list[Enemy] = []
        self.boss_active = False
        self.stage_clear = False
        self._sine_t = 0.0

    def load_stage(self, stage_index: int) -> None:
        self.stage_index = stage_index
        self.stage_data = STAGES[stage_index]
        self.events = self.stage_data["events"]
        self.elapsed = 0.0
        self.event_index = 0
        self.enemies.clear()
        self.boss_active = False
        self.stage_clear = False
        self._sine_t = 0.0

    @property
    def boss_name(self) -> str:
        return self.stage_data["boss_name"]

    @property
    def stage_name(self) -> str:
        return self.stage_data["name"]

    @property
    def stage_id(self) -> int:
        return self.stage_data["id"]

    def _spawn_wave(self, event: dict) -> None:
        start_index = len(self.enemies)
        type_id = event.get("kind", "fighter")
        pattern = event["pattern"]
        count = event["count"]

        if pattern == "line":
            for i in range(count):
                self.enemies.append(make_enemy(type_id, 60 + i * 65, -30 - i * 20))
        elif pattern == "v_formation":
            cx = LOGIC_W // 2
            for i in range(count):
                offset = (i - count // 2) * 40
                self.enemies.append(make_enemy(type_id, cx + offset, -30 - abs(offset) * 0.3))
        elif pattern == "red_pair":
            for i in range(count):
                self.enemies.append(make_enemy(type_id, 100 + i * 180, -40 - i * 30))
        elif pattern == "bomber_line":
            for i in range(count):
                self.enemies.append(make_enemy(type_id, 80 + i * 100, -50))
        elif pattern == "sine":
            for i in range(count):
                self.enemies.append(make_enemy(type_id, 40 + i * 55, -20 - i * 25))
        elif pattern == "red_swarm":
            for i in range(count):
                self.enemies.append(make_enemy(type_id, random.uniform(40, LOGIC_W - 40), -30 - i * 18))
        elif pattern == "convoy":
            for i in range(count):
                self.enemies.append(make_enemy(type_id, 50 + i * 70, -40 - i * 15))
        elif pattern == "fleet":
            cx = LOGIC_W // 2
            for i in range(count):
                self.enemies.append(make_enemy(type_id, cx + (i - count // 2) * 80, -50 - i * 25))

        for enemy in self.enemies[start_index:]:
            self._apply_stage_difficulty(enemy)

    def _apply_stage_difficulty(self, enemy: Enemy) -> None:
        """Layer mechanical pressure on top of denser late-stage wave scripts."""
        level = self.stage_index
        if level <= 0:
            return
        enemy.shoot_interval *= max(0.62, 1.0 - level * 0.09)
        enemy.vy *= 1.0 + level * 0.045
        if not enemy.is_boss:
            bonus_hp = level // 2
            enemy.hp += bonus_hp
            enemy.max_hp += bonus_hp

    def update(self, dt: float) -> str | None:
        if self.stage_clear:
            return None

        self.elapsed += dt
        triggered = None

        while self.event_index < len(self.events):
            ev = self.events[self.event_index]
            if self.elapsed < ev["time"]:
                break
            self.event_index += 1
            etype = ev["type"]
            if etype == "wave":
                self._spawn_wave(ev)
            elif etype == "boss_warning":
                triggered = "boss_warning"
            elif etype == "boss":
                self.boss_active = True
                self.enemies.append(make_enemy(
                    "boss", LOGIC_W // 2, -70,
                    boss_id=self.stage_data["boss_id"],
                    boss_hp=self.stage_data["boss_hp"],
                ))
                self._apply_stage_difficulty(self.enemies[-1])
                triggered = "boss"

        self._sine_t += dt
        alive = []
        for e in self.enemies:
            if not e.alive:
                continue
            if e.invuln > 0:
                e.invuln -= dt

            if e.is_boss:
                e.x = LOGIC_W // 2 + math.sin(self._sine_t * 0.8) * 50
                if e.y < 90:
                    e.y += e.vy * dt * 60
            else:
                e.x += e.vx
                e.y += e.vy * dt * 60
                if e.type_id in ("fighter_red", "zero", "spark_drone"):
                    e.x += math.sin(self._sine_t * 3 + e.y * 0.05) * 0.9
                elif e.type_id == "orbiter":
                    e.x += math.cos(self._sine_t * 4 + e.y * 0.04) * 1.3
                elif e.type_id == "comet":
                    e.x += math.sin(self._sine_t * 2.2 + e.y * 0.03) * 1.5
                elif e.type_id == "stuka":
                    e.x += math.sin(self._sine_t * 2) * 1.2
                elif e.category == EnemyCategory.GROUND:
                    e.x += math.sin(self._sine_t * 0.5 + e.y * 0.02) * 0.3

            if e.y > LOGIC_H + 80:
                continue
            e.shoot_timer += dt
            alive.append(e)
        self.enemies = alive

        if self.boss_active and not any(e.is_boss and e.alive for e in self.enemies):
            self.stage_clear = True
            triggered = "stage_clear"

        return triggered

    def draw(self, surface: pygame.Surface) -> None:
        for e in self.enemies:
            if not e.alive:
                continue
            if e.invuln > 0 and int(e.invuln * 20) % 2 == 0:
                continue
            surf = e.sprite()
            cx, cy = int(e.x), int(e.y)
            if not e.is_boss:
                shadow = SpriteFactory.enemy_shadow(e.is_large)
                sy = 16 if e.category == EnemyCategory.GROUND else 14
                surface.blit(shadow, shadow.get_rect(center=(cx, cy + sy)))
            surface.blit(surf, surf.get_rect(center=(cx, cy)))
