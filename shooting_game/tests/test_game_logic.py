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


def test_life_loss_resets_power_and_new_game_resets_stock():
    from src.config import START_BOMBS, START_LIVES
    from src.entities.player import Player

    p = Player("p38")
    p.power_up()
    assert p.hit() == "power_down"
    assert p.power == 0 and p.lives == START_LIVES
    p.invuln = 0
    assert p.hit() == "respawn"
    assert p.lives == START_LIVES - 1
    # Bombs carry across a respawn but reset with a genuinely new game.
    assert p.bombs == START_BOMBS
    p.bombs = 0
    p.power_up()
    p.reset_for_new_game()
    assert (p.lives, p.bombs, p.power, p.alive) == (START_LIVES, START_BOMBS, 0, True)


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


def test_treasure_drops_only_from_aircraft(monkeypatch):
    from src.entities.enemy import make_enemy
    from src.entities.item import ItemType

    monkeypatch.setattr("src.entities.enemy.random.random", lambda: 0.0)
    treasures = {ItemType.RUBY, ItemType.SAPPHIRE, ItemType.GOLD, ItemType.DIAMOND}
    assert any(kind in treasures for kind, _ in make_enemy("fighter", 0, 0).drops)
    assert not any(kind in treasures for kind, _ in make_enemy("tank", 0, 0).drops)
    assert not any(kind in treasures for kind, _ in make_enemy("destroyer", 0, 0).drops)


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


def test_five_stages_ramp_wave_density_and_boss_health():
    from src.data.stages import STAGES

    assert len(STAGES) == 5
    boss_hp = [stage["boss_hp"] for stage in STAGES]
    wave_counts = [sum(event.get("count", 0) for event in stage["events"] if event["type"] == "wave") for stage in STAGES]
    assert boss_hp == sorted(boss_hp) and len(set(boss_hp)) == 5
    assert wave_counts == sorted(wave_counts) and len(set(wave_counts)) == 5


def test_late_stage_enemies_are_tuned_more_aggressively():
    from src.entities.enemy import WaveSpawner, make_enemy

    enemy = make_enemy("fighter", 0, 0)
    baseline = (enemy.hp, enemy.vy, enemy.shoot_interval)
    WaveSpawner(4)._apply_stage_difficulty(enemy)
    assert enemy.hp > baseline[0]
    assert enemy.vy > baseline[1]
    assert enemy.shoot_interval < baseline[2]


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


def test_treasure_values_match_design():
    from src.config import DIAMOND_VALUE, GOLD_VALUE, RUBY_VALUE, SAPPHIRE_VALUE
    from src.entities.item import ItemType, random_treasure

    assert (ItemType.DIAMOND, DIAMOND_VALUE) == (ItemType.DIAMOND, 2000)
    assert (ItemType.GOLD, GOLD_VALUE) == (ItemType.GOLD, 1000)
    assert (ItemType.SAPPHIRE, SAPPHIRE_VALUE) == (ItemType.SAPPHIRE, 500)
    assert (ItemType.RUBY, RUBY_VALUE) == (ItemType.RUBY, 200)
    for _ in range(20):
        kind, value = random_treasure()
        assert kind in {ItemType.RUBY, ItemType.SAPPHIRE, ItemType.GOLD, ItemType.DIAMOND}
        assert value in (200, 500, 1000, 2000)


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


def test_formations_have_distinct_aircraft_signatures():
    from src.entities.bullet import BulletPool
    from src.systems.weapons import fire_formation

    signatures = {}
    for plane_id in ("p38", "p51", "spitfire", "bf109", "zero", "shinden", "raiden"):
        pool = BulletPool()
        fire_formation(pool, plane_id, 192, 360, [])
        signatures[plane_id] = tuple(b.kind for b in pool.bullets)
    assert len(set(signatures.values())) == 7


def test_seoyul_seven_is_selectable_and_has_unique_bomb():
    from src.config import PLANE_ORDER, PLANES

    assert PLANE_ORDER[-1] == "raiden"
    assert PLANES["raiden"]["name"] == "서율 7호기"
    assert PLANES["raiden"]["bomb_id"] == "nova"


def test_stage_backgrounds_have_distinct_themes():
    import pygame
    from src.config import LOGIC_H, LOGIC_W
    from src.render.parallax import ParallaxBackground

    pygame.init()
    colors = []
    for stage_index in range(5):
        bg = ParallaxBackground(stage_index)
        bg.update(1 / 60)
        surface = pygame.Surface((LOGIC_W, LOGIC_H))
        bg.draw(surface)
        colors.append(tuple(surface.get_at((10, 10))))
    assert len(set(colors)) == 5
    pygame.quit()


def test_pause_input_is_keydown_edge_triggered():
    import pygame
    from src.core.input_manager import InputManager

    pygame.init()
    inp = InputManager()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
    inp.poll()
    assert inp.pause_pressed
    inp.poll()
    assert not inp.pause_pressed
    pygame.quit()


def test_space_input_is_keydown_edge_triggered():
    import pygame
    from src.core.input_manager import InputManager

    pygame.init()
    inp = InputManager()
    pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE))
    inp.poll()
    assert inp.space_pressed
    inp.poll()
    assert not inp.space_pressed
    pygame.quit()


def test_energy_blast_draws_safely_at_impact():
    import pygame
    from src.config import LOGIC_H, LOGIC_W
    from src.systems.bomb_effects import EnergyBlastEffect

    pygame.init()
    effect = EnergyBlastEffect(LOGIC_W / 2, 150)
    surface = pygame.Surface((LOGIC_W, LOGIC_H), pygame.SRCALPHA)
    effect.draw(surface)
    effect.update(1 / 60)
    effect.draw(surface)
    assert surface.get_bounding_rect().width > 0
    pygame.quit()


def test_boss_is_larger_and_bomb_damage_is_not_frame_repeated():
    import pygame
    from src.entities.enemy import make_enemy
    from src.render.sprite_factory import SpriteFactory
    from src.states.play_state import PlayState

    pygame.init()
    boss = make_enemy("boss", 192, 100, boss_hp=80)
    assert SpriteFactory.boss("tank").get_width() >= 110
    assert boss.rect.width == 120

    state = PlayState(None)
    state.spawner.enemies = [boss]
    state.bombs_fx = type("BombRects", (), {"get_damage_rects": lambda self: [pygame.Rect(0, 0, 384, 448)]})()
    state._apply_bomb_damage()
    state._apply_bomb_damage()
    assert boss.hp == 53  # ceil(80 / 3), applied once despite two update frames
    pygame.quit()


def test_stage_five_has_the_largest_final_boss():
    import pygame
    from src.data.stages import STAGES
    from src.entities.enemy import make_enemy
    from src.render.sprite_factory import SpriteFactory

    pygame.init()
    final_stage = STAGES[-1]
    assert final_stage["boss_id"] == "final"
    assert final_stage["boss_hp"] > max(stage["boss_hp"] for stage in STAGES[:-1])
    final_boss = make_enemy("boss", 192, 100, boss_id="final", boss_hp=final_stage["boss_hp"])
    assert final_boss.rect.width == 180
    assert SpriteFactory.boss("final").get_width() > SpriteFactory.boss("ace").get_width()
    pygame.quit()
