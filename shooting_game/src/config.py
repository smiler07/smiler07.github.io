"""Game configuration and color palette."""

LOGIC_W = 384
LOGIC_H = 448
SCALE = 2
SCREEN_W = LOGIC_W * SCALE
SCREEN_H = LOGIC_H * SCALE
FPS = 60
DT = 1.0 / FPS

# ── Palette ──────────────────────────────────────────────────
C_SKY_TOP = (12, 18, 48)
C_SKY_MID = (35, 55, 110)
C_SKY_BOT = (180, 90, 45)
C_CLOUD = (255, 200, 140, 60)
C_GROUND = (45, 38, 28)
C_GROUND_LIGHT = (70, 58, 40)

C_PLAYER_BULLET = (120, 220, 255)
C_PLAYER_BULLET_CORE = (255, 255, 255)
C_ENEMY_BULLET = (255, 80, 60)
C_ENEMY_BULLET_CORE = (255, 200, 100)

C_HUD = (220, 230, 255)
C_HUD_ACCENT = (255, 200, 60)
C_HUD_DANGER = (255, 70, 70)

C_POWER = (255, 60, 80)
C_BOMB = (80, 160, 255)
C_GOLD = (255, 210, 50)
GOLD_SMALL = 100
GOLD_MEDIUM = 500
GOLD_LARGE = 2000
GOLD_VALUES = (GOLD_SMALL, GOLD_MEDIUM, GOLD_LARGE)
GOLD_WEIGHTS = (55, 30, 15)  # random drop weights

PLAYER_SPEED = 3.2
PLAYER_SLOW_MULT = 0.55
PLAYER_HIT_RADIUS = 3
MAX_POWER = 4
MAX_BOMBS = 6
START_LIVES = 3
EXTEND_SCORE = 600_000
CHARGE_TIME = 0.9          # full charge → formation attack
CHARGE_SHOT_START = 0.18   # hold longer → stop normal fire, gather energy
CHARGE_SHOT_MID = 0.5      # mid charge tier

PLAYER_BULLET_SPEED = 9.0
ENEMY_BULLET_SPEED = 2.8
MAX_BULLETS = 600
TOTAL_STAGES = 3

C_ENEMY_BODY = (45, 50, 55)
C_ENEMY_WING = (30, 35, 42)
C_ENEMY_ACCENT = (200, 50, 40)
C_ENEMY_RED_BODY = (190, 35, 30)
C_ENEMY_RED_RING = (255, 220, 60)
C_ENEMY_BOMBER = (55, 58, 68)

# ── 6 playable aircraft (Strikers 1945 inspired) ─────────────
PLANE_ORDER = ["p38", "p51", "spitfire", "bf109", "zero", "shinden"]

PLANES = {
    "p38": {
        "name": "P-38 Lightning",
        "pilot": "Cindy Volton",
        "color": (180, 190, 200),
        "accent": (100, 140, 200),
        "speed_mult": 1.0,
        "shot_spread": 14,
        "weapon": "spread",
        "bullet_kind": "cyan",
        "sub_kind": "rocket",
        "fire_rate": 0.09,
        "bomb_id": "energy",
        "bomb_name": "Energy Blast",
        "desc": "Wide spread · Penetrating rockets",
    },
    "p51": {
        "name": "P-51 Mustang",
        "pilot": "Tina Prize",
        "color": (160, 165, 175),
        "accent": (120, 125, 140),
        "speed_mult": 1.05,
        "shot_spread": 6,
        "weapon": "twin",
        "bullet_kind": "silver",
        "sub_kind": "homing",
        "fire_rate": 0.08,
        "bomb_id": "stuka",
        "bomb_name": "Stuka Raid",
        "desc": "Twin fire · Homing missiles",
    },
    "spitfire": {
        "name": "Spitfire",
        "pilot": "Alice Herring",
        "color": (90, 120, 70),
        "accent": (140, 160, 90),
        "speed_mult": 1.08,
        "shot_spread": 8,
        "weapon": "rapid",
        "bullet_kind": "green",
        "sub_kind": "homing",
        "fire_rate": 0.06,
        "bomb_id": "gale",
        "bomb_name": "Gale Force",
        "desc": "Rapid fire · Tracking missiles",
    },
    "bf109": {
        "name": "Bf-109",
        "pilot": "Lean Beirer",
        "color": (140, 145, 130),
        "accent": (90, 95, 85),
        "speed_mult": 0.98,
        "shot_spread": 4,
        "weapon": "heavy",
        "bullet_kind": "heavy",
        "sub_kind": "heavy",
        "fire_rate": 0.14,
        "bomb_id": "cluster",
        "bomb_name": "Cluster Strike",
        "desc": "Heavy cannon · Area barrage",
    },
    "zero": {
        "name": "A6M Zero",
        "pilot": "Ai Mikami",
        "color": (200, 210, 195),
        "accent": (160, 50, 45),
        "speed_mult": 0.92,
        "shot_spread": 18,
        "weapon": "fan",
        "bullet_kind": "pellet",
        "sub_kind": "pellet",
        "fire_rate": 0.1,
        "bomb_id": "typhoon",
        "bomb_name": "Typhoon",
        "desc": "Fan spread · Bullet-null wind",
    },
    "shinden": {
        "name": "J7W Shinden",
        "pilot": "Ainzaemon",
        "color": (130, 135, 150),
        "accent": (200, 60, 50),
        "speed_mult": 1.15,
        "shot_spread": 2,
        "weapon": "laser",
        "bullet_kind": "laser",
        "sub_kind": "laser",
        "fire_rate": 0.05,
        "bomb_id": "phantom",
        "bomb_name": "Phantom Rush",
        "desc": "Laser burst · Shadow dash",
    },
}
