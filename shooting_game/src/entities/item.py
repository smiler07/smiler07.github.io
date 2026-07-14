"""Pickup items: Power, Bomb, Gold."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from enum import Enum, auto

import pygame

from src.config import (
    GOLD_LARGE,
    GOLD_MEDIUM,
    GOLD_SMALL,
    GOLD_VALUES,
    GOLD_WEIGHTS,
    LOGIC_H,
)
from src.render.sprite_factory import SpriteFactory


class ItemType(Enum):
    POWER = auto()
    BOMB = auto()
    GOLD = auto()


def gold_size_for_value(value: int) -> str:
    if value >= GOLD_LARGE:
        return "large"
    if value >= GOLD_MEDIUM:
        return "medium"
    return "small"


def random_gold_value() -> int:
    return random.choices(list(GOLD_VALUES), weights=GOLD_WEIGHTS, k=1)[0]


@dataclass
class Item:
    x: float
    y: float
    item_type: ItemType
    value: int = 0
    alive: bool = True
    vy: float = 1.2
    pulse: float = 0.0

    @property
    def gold_size(self) -> str:
        return gold_size_for_value(self.value)

    @property
    def rect(self) -> pygame.Rect:
        if self.item_type == ItemType.GOLD:
            size_map = {"small": 8, "medium": 12, "large": 16}
            r = size_map[self.gold_size]
            return pygame.Rect(int(self.x - r), int(self.y - r), r * 2, r * 2)
        return pygame.Rect(int(self.x - 10), int(self.y - 10), 20, 20)


class ItemManager:
    def __init__(self) -> None:
        self.items: list[Item] = []

    def spawn(self, x: float, y: float, item_type: ItemType, value: int = 0) -> None:
        self.items.append(Item(x, y, item_type, value))

    def spawn_random_gold(self, x: float, y: float, ox: float = 0.0) -> int:
        """Spawn gold with random size. Returns gold value."""
        value = random_gold_value()
        self.items.append(Item(x + ox, y, ItemType.GOLD, value, vy=0.9 + random.uniform(0, 0.4)))
        return value

    def spawn_drops(self, x: float, y: float, drops: list[tuple[ItemType, int]]) -> None:
        for i, (itype, val) in enumerate(drops):
            ox = random.uniform(-12, 12)
            if itype == ItemType.GOLD and val <= 0:
                self.spawn_random_gold(x, y, ox)
            else:
                value = random_gold_value() if itype == ItemType.GOLD and val == 0 else val
                self.items.append(Item(x + ox, y, itype, value, vy=0.8 + i * 0.1))

    def update(self, dt: float) -> None:
        for item in self.items:
            if not item.alive:
                continue
            item.y += item.vy
            item.pulse += dt * 5
            if item.y > LOGIC_H + 20:
                item.alive = False

    def draw(self, surface: pygame.Surface) -> None:
        for item in self.items:
            if not item.alive:
                continue
            scale = 1.0 + math.sin(item.pulse) * 0.08
            if item.item_type == ItemType.POWER:
                surf = SpriteFactory.power_item()
            elif item.item_type == ItemType.BOMB:
                surf = SpriteFactory.bomb_item()
            else:
                surf = SpriteFactory.gold_bar(item.gold_size)
            if scale != 1.0:
                w, h = surf.get_size()
                surf = pygame.transform.scale(surf, (int(w * scale), int(h * scale)))
            surface.blit(surf, surf.get_rect(center=(int(item.x), int(item.y))))

    def collect_at(self, rect: pygame.Rect) -> list[Item]:
        collected = []
        for item in self.items:
            if item.alive and rect.colliderect(item.rect):
                item.alive = False
                collected.append(item)
        return collected
