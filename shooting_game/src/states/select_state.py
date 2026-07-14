"""Plane selection screen — carousel for 6 aircraft."""

from __future__ import annotations

import math

import pygame

from src.config import C_HUD, C_HUD_ACCENT, LOGIC_W, PLANE_ORDER, PLANES
from src.render.sprite_factory import SpriteFactory
from src.states.base_state import GameState


class SelectState(GameState):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.index = 0
        self.time = 0.0
        self._nav_cooldown = 0.0

    def enter(self) -> None:
        self.index = 0
        self.time = 0.0
        self._nav_cooldown = 0.0

    def update(self, dt: float) -> None:
        self.time += dt
        self._nav_cooldown = max(0, self._nav_cooldown - dt)
        inp = self.game.input
        if self._nav_cooldown <= 0:
            if inp.left or inp.up_pressed:
                self.index = (self.index - 1) % len(PLANE_ORDER)
                self._nav_cooldown = 0.18
                if self.game.audio:
                    self.game.audio.play("select")
            if inp.right or inp.down_pressed:
                self.index = (self.index + 1) % len(PLANE_ORDER)
                self._nav_cooldown = 0.18
                if self.game.audio:
                    self.game.audio.play("select")
        if inp.confirm_pressed:
            self.game.selected_plane = PLANE_ORDER[self.index]
            self.game.stage_index = 0
            if self.game.audio:
                self.game.audio.play("confirm")
            self.game.change_state("play")

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((15, 20, 45))

        font_title = pygame.font.SysFont("consolas", 16, bold=True)
        font_info = pygame.font.SysFont("consolas", 10)
        font_small = pygame.font.SysFont("consolas", 9)

        title = font_title.render("SELECT AIRCRAFT", True, C_HUD_ACCENT)
        surface.blit(title, (LOGIC_W // 2 - title.get_width() // 2, 20))

        count_t = font_small.render(f"{self.index + 1} / {len(PLANE_ORDER)}", True, (100, 120, 150))
        surface.blit(count_t, (LOGIC_W // 2 - count_t.get_width() // 2, 42))

        # Draw carousel — show prev, current, next
        for offset in (-1, 0, 1):
            idx = (self.index + offset) % len(PLANE_ORDER)
            pid = PLANE_ORDER[idx]
            info = PLANES[pid]
            cx = LOGIC_W // 2 + offset * 130
            cy = 210
            selected = offset == 0
            scale = 1.0 if selected else 0.65
            alpha_card = 220 if selected else 90

            card_w, card_h = int(160 * scale), int(240 * scale)
            card = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
            border = C_HUD_ACCENT if selected else (50, 60, 90)
            card.fill((20, 30, 60, alpha_card))
            pygame.draw.rect(card, border, (0, 0, card_w, card_h), 2 if selected else 1, border_radius=6)
            surface.blit(card, (cx - card_w // 2, cy - card_h // 2))

            if selected:
                bob = math.sin(self.time * 3) * 4
                surf = SpriteFactory.plane(pid)
                big = pygame.transform.scale(surf, (64, 64))
                surface.blit(big, big.get_rect(center=(cx, int(cy - 40 + bob))))

                name = font_title.render(info["name"], True, C_HUD)
                surface.blit(name, name.get_rect(center=(cx, cy + 30)))

                pilot = font_info.render(info["pilot"], True, (150, 160, 180))
                surface.blit(pilot, pilot.get_rect(center=(cx, cy + 52)))

                desc = font_info.render(info["desc"], True, (100, 180, 220))
                surface.blit(desc, desc.get_rect(center=(cx, cy + 72)))

                weapon = font_small.render(f"Weapon: {info['weapon'].upper()}", True, (120, 200, 255))
                surface.blit(weapon, weapon.get_rect(center=(cx, cy + 92)))

                bomb = font_small.render(f"Bomb: {info['bomb_name']}", True, (255, 160, 80))
                surface.blit(bomb, bomb.get_rect(center=(cx, cy + 108)))
            else:
                surf = SpriteFactory.plane(pid)
                small = pygame.transform.scale(surf, (int(36 * scale * 2), int(36 * scale * 2)))
                surface.blit(small, small.get_rect(center=(cx, cy - 10)))

        # Arrow hints
        if int(self.time * 2) % 2 == 0:
            arr_l = font_title.render("<", True, C_HUD_ACCENT)
            arr_r = font_title.render(">", True, C_HUD_ACCENT)
            surface.blit(arr_l, (20, 200))
            surface.blit(arr_r, (LOGIC_W - 30, 200))

        hint = font_info.render("< > CHANGE    ENTER START", True, (100, 120, 150))
        surface.blit(hint, (LOGIC_W // 2 - hint.get_width() // 2, 400))
