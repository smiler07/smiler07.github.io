"""Pickup items: power, bombs, and birthday-treasure gems."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from enum import Enum, auto

import pygame

from src.config import DIAMOND_VALUE, GOLD_VALUE, LOGIC_H, RUBY_VALUE, SAPPHIRE_VALUE, TREASURE_WEIGHTS
from src.render.sprite_factory import SpriteFactory


class ItemType(Enum):
    POWER = auto()
    BOMB = auto()
    RUBY = auto()
    SAPPHIRE = auto()
    GOLD = auto()
    DIAMOND = auto()


TREASURES = (
    (ItemType.RUBY, RUBY_VALUE),
    (ItemType.SAPPHIRE, SAPPHIRE_VALUE),
    (ItemType.GOLD, GOLD_VALUE),
    (ItemType.DIAMOND, DIAMOND_VALUE),
)


def random_treasure() -> tuple[ItemType, int]:
    return random.choices(TREASURES, weights=TREASURE_WEIGHTS, k=1)[0]


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
    def rect(self) -> pygame.Rect:
        if self.item_type in {ItemType.RUBY, ItemType.SAPPHIRE, ItemType.GOLD, ItemType.DIAMOND}:
            r = 12 if self.item_type == ItemType.DIAMOND else 9
            return pygame.Rect(int(self.x - r), int(self.y - r), r * 2, r * 2)
        return pygame.Rect(int(self.x - 10), int(self.y - 10), 20, 20)


class ItemManager:
    def __init__(self) -> None:
        self.items: list[Item] = []

    def spawn(self, x: float, y: float, item_type: ItemType, value: int = 0) -> None:
        self.items.append(Item(x, y, item_type, value))

    def spawn_random_treasure(self, x: float, y: float, ox: float = 0.0) -> int:
        item_type, value = random_treasure()
        self.items.append(Item(x + ox, y, item_type, value, vy=0.9 + random.uniform(0, 0.4)))
        return value

    def spawn_drops(self, x: float, y: float, drops: list[tuple[ItemType, int]]) -> None:
        for i, (itype, val) in enumerate(drops):
            ox = random.uniform(-12, 12)
            if itype == ItemType.GOLD and val <= 0:
                self.spawn_random_treasure(x, y, ox)
            else:
                self.items.append(Item(x + ox, y, itype, val, vy=0.8 + i * 0.1))

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
                surf = SpriteFactory.treasure(item.item_type.name.lower())
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
