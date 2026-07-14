"""Main gameplay state."""

from __future__ import annotations

import math
import random

import pygame

from src.config import EXTEND_SCORE, LOGIC_H, LOGIC_W, MAX_POWER, TOTAL_STAGES
from src.data.stages import STAGES
from src.entities.bullet import BulletOwner, BulletPool
from src.entities.enemy import WaveSpawner
from src.entities.item import ItemManager, ItemType
from src.entities.player import Player
from src.render.hud import HUD
from src.render.parallax import ParallaxBackground
from src.render.particles import ParticleSystem
from src.states.base_state import GameState
from src.systems.bomb_effects import BombEffectManager


class PlayState(GameState):
    def __init__(self, game) -> None:
        super().__init__(game)
        self.player: Player | None = None
        self.bullets = BulletPool()
        self.spawner = WaveSpawner()
        self.items = ItemManager()
        self.bg = ParallaxBackground()
        self.particles = ParticleSystem()
        self.bombs_fx = BombEffectManager()
        self.hud = HUD()
        self.score = 0
        self.shake = 0.0
        self.paused = False
        self._pattern_t = 0.0
        self._extend_given = False
        self._stage_clear_timer = 0.0
        self._all_clear = False

    def enter(self) -> None:
        plane_id = self.game.selected_plane or "p38"
        stage_index = getattr(self.game, "stage_index", 0)

        if stage_index == 0:
            # New game from plane select
            self.player = Player(plane_id)
            self.score = 0
            self._extend_given = False

        if self.player is None:
            self.player = Player(plane_id)

        self.bullets = BulletPool()
        self.spawner = WaveSpawner(stage_index)
        self.items = ItemManager()
        self.bg = ParallaxBackground()
        self.particles = ParticleSystem()
        self.bombs_fx = BombEffectManager()
        self.hud = HUD()
        self.shake = 0.0
        self.paused = False
        self._pattern_t = 0.0
        self._stage_clear_timer = 0.0
        self._all_clear = False

        stage = STAGES[stage_index]
        self.hud.show_message(f"STAGE {stage['id']}  {stage['name']}", 2.5)
        if self.game.audio:
            self.game.audio.start_bgm()

    def _move_player(self) -> None:
        if not self.player or not self.player.alive:
            return
        dx = dy = 0
        if self.game.input.left:
            dx -= 1
        if self.game.input.right:
            dx += 1
        if self.game.input.up:
            dy -= 1
        if self.game.input.down:
            dy += 1
        if dx and dy:
            dx *= 0.707
            dy *= 0.707
        self.player.move(dx, dy, self.game.input.slow)

    def _enemy_shoot(self, dt: float) -> None:
        if not self.player:
            return
        self._pattern_t += dt
        px, py = self.player.x, self.player.y

        for e in self.spawner.enemies:
            if not e.alive or e.shoot_timer < e.shoot_interval:
                continue
            e.shoot_timer = 0.0

            if e.is_boss:
                self._boss_pattern(e, px, py)
            elif e.type_id == "bomber":
                self.bullets.spawn_enemy_aimed(e.x, e.y + 10, px, py, speed=2.2)
            elif e.type_id == "stuka":
                self.bullets.spawn_enemy_aimed(e.x, e.y + 12, px, py, speed=3.0)
                self.bullets.spawn_enemy(e.x, e.y, 0, 3.5)
            elif e.type_id == "fighter_red":
                for angle in [-20, 0, 20]:
                    rad = math.radians(angle - 90)
                    self.bullets.spawn_enemy(e.x, e.y, math.cos(rad) * 2.5, math.sin(rad) * 2.5)
            elif e.type_id == "zero":
                self.bullets.spawn_enemy_aimed(e.x, e.y, px, py, speed=3.2)
            elif e.type_id == "bf109":
                for off in (-10, 0, 10):
                    self.bullets.spawn_enemy_aimed(e.x + off, e.y, px, py, speed=2.5)
            elif e.type_id in ("tank", "heavy_tank"):
                self.bullets.spawn_enemy_aimed(e.x, e.y, px, py, speed=2.0)
                if e.type_id == "heavy_tank":
                    self.bullets.spawn_enemy(e.x - 8, e.y, -0.5, 2.5)
                    self.bullets.spawn_enemy(e.x + 8, e.y, 0.5, 2.5)
            elif e.type_id == "destroyer":
                for off in (-20, 0, 20):
                    self.bullets.spawn_enemy_aimed(e.x + off, e.y, px, py, speed=2.2)
            elif e.type_id == "pt_boat":
                self.bullets.spawn_enemy_aimed(e.x, e.y, px, py, speed=2.8)
                self.bullets.spawn_enemy_aimed(e.x - 8, e.y, px, py, speed=2.5)
            else:
                self.bullets.spawn_enemy_aimed(e.x, e.y, px, py)

    def _boss_pattern(self, boss, px: float, py: float) -> None:
        phase = boss.boss_phase
        t = self._pattern_t

        if boss.hp < boss.max_hp * 0.5 and phase < 2:
            boss.boss_phase = 2
            self.hud.show_message("BOSS PHASE 2", 1.5)

        if phase < 1:
            # Radial spread
            count = 10
            base = t * 40
            for i in range(count):
                ang = math.radians(base + i * (360 / count))
                self.bullets.spawn_enemy(boss.x, boss.y + 20, math.cos(ang) * 2.8, math.sin(ang) * 2.8)
        elif phase < 2:
            # Aimed triple + spiral
            for off in (-15, 0, 15):
                rad = math.atan2(py - boss.y, px - boss.x) + math.radians(off)
                self.bullets.spawn_enemy(boss.x, boss.y, math.cos(rad) * 3.2, math.sin(rad) * 3.2)
            ang = math.radians(t * 120)
            self.bullets.spawn_enemy(boss.x, boss.y, math.cos(ang) * 2.5, math.sin(ang) * 2.5)
        else:
            # Dense ring + aimed
            for i in range(16):
                ang = math.radians(t * 60 + i * 22.5)
                self.bullets.spawn_enemy(boss.x, boss.y, math.cos(ang) * 3.5, math.sin(ang) * 3.5)
            self.bullets.spawn_enemy_aimed(boss.x, boss.y, px, py, speed=3.8)

    def _collision(self) -> None:
        if not self.player or not self.player.alive:
            return

        # Player bullets vs enemies
        for b in self.bullets.bullets:
            if not b.alive or b.owner != BulletOwner.PLAYER:
                continue
            for e in self.spawner.enemies:
                if not e.alive or not b.rect.colliderect(e.rect):
                    continue
                b.alive = False
                e.hp -= b.damage
                self.particles.emit_trail(b.x, b.y, (120, 220, 255))
                if e.hp <= 0:
                    self._kill_enemy(e)
                else:
                    e.invuln = 0.05
                break

        # Player bullets vs buildings
        for b in self.bullets.bullets:
            if not b.alive or b.owner != BulletOwner.PLAYER:
                continue
            for building in self.bg.get_buildings():
                br = pygame.Rect(int(building["x"]), int(building["y"]),
                                 building["sprite"].get_width(), building["sprite"].get_height())
                if b.rect.colliderect(br):
                    b.alive = False
                    gold = self.bg.damage_building(building)
                    if gold:
                        self.items.spawn(building["x"] + 10, building["y"], ItemType.GOLD, gold)
                        self.particles.emit_explosion(building["x"] + 10, building["y"])
                    break

        # Enemy bullets vs player
        for b in self.bullets.bullets:
            if not b.alive or b.owner != BulletOwner.ENEMY:
                continue
            if b.rect.colliderect(self.player.rect):
                b.alive = False
                result = self.player.hit()
                if result == "death":
                    self.particles.emit_explosion(self.player.x, self.player.y, big=True)
                    self.shake = 0.5
                    self.game.change_state("title")
                elif result in ("power_down", "respawn"):
                    self.particles.emit_explosion(self.player.x, self.player.y)
                    self.shake = 0.3

        # Enemy body vs player
        for e in self.spawner.enemies:
            if not e.alive:
                continue
            if e.rect.colliderect(self.player.rect):
                result = self.player.hit()
                if result == "death":
                    self.game.change_state("title")
                elif result in ("power_down", "respawn"):
                    self.particles.emit_explosion(self.player.x, self.player.y)
                if not e.is_boss:
                    e.alive = False
                    self.particles.emit_explosion(e.x, e.y)

        # Items
        for item in self.items.collect_at(self.player.hit_rect):
            if item.item_type == ItemType.POWER:
                if self.player.power >= MAX_POWER:
                    self.score += 4000
                else:
                    self.player.power_up()
                self.particles.emit_gold_sparkle(item.x, item.y)
                if self.game.audio:
                    self.game.audio.play("powerup")
            elif item.item_type == ItemType.BOMB:
                bonus = self.player.add_bomb()
                self.score += bonus
                self.particles.emit_gold_sparkle(item.x, item.y)
                if self.game.audio:
                    self.game.audio.play("powerup")
            elif item.item_type == ItemType.GOLD:
                self.score += item.value
                self.particles.emit_gold_sparkle(item.x, item.y)
                self.hud.show_gold_popup(item.x, item.y, item.value)

    def _apply_bomb_damage(self) -> None:
        for rect in self.bombs_fx.get_damage_rects():
            for e in self.spawner.enemies:
                if not e.alive:
                    continue
                if e.rect.colliderect(rect):
                    if e.is_boss:
                        e.hp -= 8
                        if e.hp <= 0:
                            self._kill_enemy(e)
                    else:
                        self._kill_enemy(e)

    def _clear_bullets_in_bomb(self) -> None:
        rects = self.bombs_fx.get_bullet_clear_rects()
        if rects:
            self.bullets.clear_enemy_in_rects(rects)

    def _trigger_bomb(self) -> None:
        if not self.player or not self.player.use_bomb(self.bullets):
            return
        bomb_id = self.player.bomb_id
        self.bombs_fx.trigger(bomb_id, self.player.x, self.player.y)
        self.shake = 0.8
        if self.game.audio:
            self.game.audio.play_bomb(bomb_id)
        # Immediate small enemies kill on screen (classic bomb)
        for e in self.spawner.enemies:
            if e.alive and not e.is_boss:
                self._kill_enemy(e)
            elif e.alive and e.is_boss:
                e.hp -= 12
                if e.hp <= 0:
                    self._kill_enemy(e)

    def _kill_enemy(self, e) -> None:
        e.alive = False
        self.score += e.score
        self.particles.emit_explosion(e.x, e.y, big=e.is_boss)
        self.shake = 0.4 if e.is_boss else 0.15
        if self.game.audio:
            self.game.audio.play("explosion_big" if e.is_boss else "explosion_small")

        drops = e.drops
        if drops:
            self.items.spawn_drops(e.x, e.y, drops)

        if e.is_boss:
            self.hud.boss_name = None

    def update(self, dt: float) -> None:
        if self.paused:
            if self.game.input.pause_pressed:
                self.paused = False
            return

        if self.game.input.pause_pressed:
            self.paused = True
            return

        if not self.player:
            return

        self._move_player()

        formation = self.player.update(
            dt,
            self.game.input.fire_held,
            self.game.input.fire_released,
        )

        if self.game.input.fire_held and not formation.formation:
            did_shoot, weapon = self.player.shoot(self.bullets)
            if did_shoot and self.game.audio:
                self.game.audio.play_shoot(weapon)
            elif self.player.is_gathering and self.game.audio:
                if int(self.player._charge_pulse) % 12 == 0:
                    self.game.audio.play("charge_loop")

        if formation.charge_tier > 0:
            self.player.fire_charge(self.bullets, formation.charge_tier)
            self.shake = 0.2 if formation.charge_tier == 1 else 0.35
            if self.game.audio:
                self.game.audio.play("charge_big" if formation.charge_tier >= 2 else "charge_shot")
            tier_name = "CHARGE SHOT!" if formation.charge_tier == 1 else "FULL CHARGE!"
            self.hud.show_message(tier_name, 0.6)

        if formation.formation:
            self.player.fire_formation(self.bullets)
            self.hud.show_message("FORMATION!", 0.8)
            self.shake = 0.45
            if self.game.audio:
                self.game.audio.play("formation")

        if self.game.input.bomb_pressed:
            self._trigger_bomb()

        event = self.spawner.update(dt)
        if event == "boss_warning":
            self.hud.show_message("WARNING!!", 2.0)
            if self.game.audio:
                self.game.audio.play("boss_warning")
        elif event == "boss":
            self.hud.boss_name = self.spawner.boss_name
            self.hud.show_message("BOSS APPROACHING", 2.0)
        elif event == "stage_clear":
            self._stage_clear_timer = 3.0
            if self.game.audio:
                self.game.audio.play("stage_clear")
            if self.game.stage_index >= TOTAL_STAGES - 1:
                self.hud.show_message("ALL STAGES CLEAR!", 3.0)
                self._all_clear = True
            else:
                self.hud.show_message("STAGE CLEAR!", 2.5)

        # Boss HP for HUD
        for e in self.spawner.enemies:
            if e.is_boss and e.alive:
                self.hud.boss_hp_ratio = e.hp / e.max_hp
                if e.hp < e.max_hp * 0.66 and e.boss_phase < 1:
                    e.boss_phase = 1
                    self.hud.show_message("BOSS PHASE 2", 1.5)

        self._enemy_shoot(dt)
        self.bullets.update(dt, self.spawner.enemies)
        self.bombs_fx.update(dt)
        self._clear_bullets_in_bomb()
        self._apply_bomb_damage()
        self.items.update(dt)
        self.bg.update(dt)
        self.particles.update(dt)
        self.hud.update(dt)
        self._collision()

        if self.score >= EXTEND_SCORE and not self._extend_given:
            self.player.lives += 1
            self._extend_given = True
            self.hud.show_message("1UP!", 2.0)

        if self.shake > 0:
            self.shake -= dt

        if self._stage_clear_timer > 0:
            self._stage_clear_timer -= dt
            if self._stage_clear_timer <= 0:
                if self.score > self.game.hi_score:
                    self.game.hi_score = self.score
                if self._all_clear:
                    self.game.stage_index = 0
                    self.game.change_state("title")
                else:
                    self.game.stage_index += 1
                    self.enter()

    def draw(self, surface: pygame.Surface) -> None:
        self.bg.draw(surface)
        self.spawner.draw(surface)
        self.items.draw(surface)
        self.bullets.draw(surface)
        if self.player:
            self.player.draw(surface)
        self.bombs_fx.draw(surface)
        self.particles.draw(surface)

        if self.player:
            from src.config import PLANES
            self.hud.draw(
                surface,
                self.score,
                self.game.hi_score,
                self.player.lives,
                self.player.bombs,
                self.player.power,
                PLANES[self.player.plane_id]["name"],
                stage_id=self.spawner.stage_id,
                total_stages=TOTAL_STAGES,
            )

        if self.paused:
            overlay = pygame.Surface((LOGIC_W, LOGIC_H), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            surface.blit(overlay, (0, 0))
            font = pygame.font.SysFont("consolas", 16, bold=True)
            t = font.render("PAUSED", True, (255, 255, 200))
            surface.blit(t, (LOGIC_W // 2 - t.get_width() // 2, LOGIC_H // 2))

    @property
    def shake_offset(self) -> tuple[int, int]:
        if self.shake <= 0:
            return 0, 0
        return random.randint(-3, 3), random.randint(-3, 3)
