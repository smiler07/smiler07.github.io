"""Particle effects for explosions, trails, and bomb flashes."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass

import pygame


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    max_life: float
    color: tuple[int, int, int]
    size: float
    kind: str = "circle"  # circle | spark | ring


class ParticleSystem:
    def __init__(self) -> None:
        self.particles: list[Particle] = []

    def emit_explosion(self, x: float, y: float, big: bool = False) -> None:
        count = 28 if big else 14
        colors = [(255, 200, 60), (255, 120, 40), (255, 80, 30), (255, 255, 180)]
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(1.5, 5.5 if big else 3.5)
            life = random.uniform(0.3, 0.8 if big else 0.5)
            self.particles.append(
                Particle(
                    x, y,
                    math.cos(angle) * speed,
                    math.sin(angle) * speed,
                    life, life,
                    random.choice(colors),
                    random.uniform(2, 5 if big else 3),
                    random.choice(["circle", "spark"]),
                )
            )
        # Shock ring
        self.particles.append(Particle(x, y, 0, 0, 0.4, 0.4, (255, 220, 100), 4, "ring"))

    def emit_trail(self, x: float, y: float, color: tuple[int, int, int]) -> None:
        self.particles.append(
            Particle(x, y, random.uniform(-0.3, 0.3), random.uniform(0.5, 1.5),
                     0.25, 0.25, color, random.uniform(1, 2), "circle")
        )

    def emit_bomb_flash(self) -> None:
        self.particles.append(Particle(192, 224, 0, 0, 0.6, 0.6, (255, 255, 220), 200, "flash"))

    def emit_gold_sparkle(self, x: float, y: float) -> None:
        for _ in range(6):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(0.5, 2)
            self.particles.append(
                Particle(x, y, math.cos(angle) * speed, math.sin(angle) * speed,
                         0.35, 0.35, (255, 220, 80), 2, "spark")
            )

    def update(self, dt: float) -> None:
        alive = []
        for p in self.particles:
            p.life -= dt
            if p.life <= 0:
                continue
            p.x += p.vx
            p.y += p.vy
            if p.kind != "flash":
                p.vy += 0.05
                p.vx *= 0.98
            alive.append(p)
        self.particles = alive

    def draw(self, surface: pygame.Surface) -> None:
        for p in self.particles:
            t = p.life / p.max_life
            alpha = int(255 * t)
            if p.kind == "flash":
                overlay = pygame.Surface((384, 448), pygame.SRCALPHA)
                overlay.fill((255, 255, 200, int(180 * t)))
                surface.blit(overlay, (0, 0))
            elif p.kind == "ring":
                r = int((1 - t) * 40 + 4)
                s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*p.color, int(200 * t)), (r, r), r, 2)
                surface.blit(s, (int(p.x - r), int(p.y - r)))
            elif p.kind == "spark":
                end = (int(p.x - p.vx * 3), int(p.y - p.vy * 3))
                pygame.draw.line(surface, (*p.color, alpha), (int(p.x), int(p.y)), end, 1)
            else:
                sz = max(1, int(p.size * t))
                s = pygame.Surface((sz * 2, sz * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*p.color, alpha), (sz, sz), sz)
                surface.blit(s, (int(p.x - sz), int(p.y - sz)))
