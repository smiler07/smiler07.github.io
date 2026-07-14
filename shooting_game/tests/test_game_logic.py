"""Basic unit tests for game logic."""

import math

import pytest


def test_player_power_system():
    from src.entities.player import Player
    from src.config import MAX_POWER

    p = Player("p38")
    assert p.power == 0
    for i in range(1, MAX_POWER + 1):
        p.power_up()
        assert p.power == i
        assert len(p.options) == i
    p.power_up()  # overflow shouldn't exceed max
    assert p.power == MAX_POWER
    p.power_down()
    assert p.power == 0
    assert len(p.options) == 0


def test_bomb_stock():
    from src.entities.player import Player
    from src.config import MAX_BOMBS

    p = Player("p38")
    p.bombs = MAX_BOMBS
    bonus = p.add_bomb()
    assert bonus == 10_000
    p.bombs = 0
    assert p.add_bomb() == 0
    assert p.bombs == 1


def test_bullet_pool_spawn():
    from src.entities.bullet import BulletPool, BulletOwner

    pool = BulletPool()
    pool.spawn_player(100, 200)
    assert len(pool.bullets) == 1
    assert pool.bullets[0].owner == BulletOwner.PLAYER
    pool.spawn_enemy(50, 50, 1, 2)
    assert len(pool.bullets) == 2
    pool.clear_enemy()
    assert len(pool.bullets) == 1
    assert pool.bullets[0].owner == BulletOwner.PLAYER


def test_enemy_drops():
    from src.entities.enemy import make_enemy
    from src.entities.item import ItemType

    red = make_enemy("fighter_red", 100, 100)
    drops = red.drops
    assert (ItemType.POWER, 0) in drops


def test_enemy_variety():
    import pygame
    pygame.init()
    from src.entities.enemy import ENEMY_KINDS, make_enemy
    from src.render.sprite_factory import SpriteFactory

    for type_id in ENEMY_KINDS:
        e = make_enemy(type_id, 100, 100)
        surf = SpriteFactory.enemy_by_kind(type_id)
        assert surf.get_width() > 0
        assert e.type_id == type_id
    pygame.quit()


def test_wave_spawner_timeline():
    from src.entities.enemy import WaveSpawner
    from src.data.stages import STAGES

    spawner = WaveSpawner(0)
    assert spawner.boss_name == STAGES[0]["boss_name"]
    for _ in range(60 * 5):
        spawner.update(1 / 60)
    assert len(spawner.enemies) > 0


def test_all_stages_have_boss():
    from src.data.stages import STAGES

    for stage in STAGES:
        types = [e["type"] for e in stage["events"]]
        assert "boss_warning" in types
        assert "boss" in types
        assert "boss_id" in stage
        assert "boss_name" in stage


def test_enemy_sprites_distinct():
    import pygame
    pygame.init()
    from src.render.sprite_factory import SpriteFactory

    fighter = SpriteFactory.enemy_fighter(False)
    zero = SpriteFactory.enemy_by_kind("zero")
    tank = SpriteFactory.enemy_by_kind("tank")
    ship = SpriteFactory.enemy_by_kind("destroyer")
    player = SpriteFactory.plane("p38")
    assert fighter.get_size() != player.get_size()
    assert tank.get_size() != fighter.get_size()
    assert ship.get_size()[0] > tank.get_size()[0]
    assert zero.get_size() != fighter.get_size()
    pygame.quit()


def test_gold_sizes():
    from src.entities.item import gold_size_for_value, random_gold_value
    from src.config import GOLD_SMALL, GOLD_MEDIUM, GOLD_LARGE

    assert gold_size_for_value(100) == "small"
    assert gold_size_for_value(500) == "medium"
    assert gold_size_for_value(2000) == "large"
    for _ in range(20):
        v = random_gold_value()
        assert v in (GOLD_SMALL, GOLD_MEDIUM, GOLD_LARGE)


def test_charge_shot_tiers():
    from src.entities.player import Player
    from src.config import CHARGE_SHOT_START, CHARGE_SHOT_MID, CHARGE_TIME

    p = Player("p38")
    p.update(0.1, fire_held=True, fire_released=True)
    r = p.update(0, fire_held=False, fire_released=False)
    assert r.charge_tier == 0

    p = Player("p38")
    p.charging = True
    p.charge_time = CHARGE_SHOT_START + 0.1
    r = p.update(0, fire_held=False, fire_released=True)
    assert r.charge_tier == 1

    p = Player("p38")
    p.charging = True
    p.charge_time = CHARGE_SHOT_MID + 0.1
    r = p.update(0, fire_held=False, fire_released=True)
    assert r.charge_tier == 2

    p = Player("p38")
    p.charging = True
    p.charge_time = CHARGE_TIME
    r = p.update(0, fire_held=False, fire_released=True)
    assert r.formation