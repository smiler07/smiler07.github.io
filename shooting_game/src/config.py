"""Game configuration and color palette."""

LOGIC_W = 384
LOGIC_H = 448
# A clean 2.5x presentation keeps the arcade playfield compact while avoiding
# the hard pixel enlargement of the original 2x output.
SCALE = 2.5
SCREEN_W = int(LOGIC_W * SCALE)
SCREEN_H = int(LOGIC_H * SCALE)
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
RUBY_VALUE = 200
SAPPHIRE_VALUE = 500
GOLD_VALUE = 1000
DIAMOND_VALUE = 2000
TREASURE_VALUES = (RUBY_VALUE, SAPPHIRE_VALUE, GOLD_VALUE, DIAMOND_VALUE)
TREASURE_WEIGHTS = (45, 30, 18, 7)

PLAYER_SPEED = 3.2
PLAYER_SLOW_MULT = 0.55
PLAYER_HIT_RADIUS = 3
MAX_POWER = 4
MAX_BOMBS = 6
START_LIVES = 3
START_BOMBS = 3
EXTEND_SCORE = 600_000
CHARGE_TIME = 0.9          # full charge → formation attack
CHARGE_SHOT_START = 0.18   # hold longer → stop normal fire, gather energy
CHARGE_SHOT_MID = 0.5      # mid charge tier

PLAYER_BULLET_SPEED = 9.0
ENEMY_BULLET_SPEED = 2.8
MAX_BULLETS = 600
TOTAL_STAGES = 5

C_ENEMY_BODY = (45, 50, 55)
C_ENEMY_WING = (30, 35, 42)
C_ENEMY_ACCENT = (200, 50, 40)
C_ENEMY_RED_BODY = (190, 35, 30)
C_ENEMY_RED_RING = (255, 220, 60)
C_ENEMY_BOMBER = (55, 58, 68)

# ── 6 playable aircraft (Strikers 1945 inspired) ─────────────
PLANE_ORDER = ["p38", "p51", "spitfire", "bf109", "zero", "shinden", "raiden"]

PLANES = {
    "p38": {
        "name": "서율 1호기",
        "model": "P-38 Lightning",
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
        "role": "WIDE CONTROL",
        "weapon_name": "SPREAD ROCKETS",
        "charge_name": "ROCKET LANCE",
        "formation_name": "SATURATION STRIKE",
    },
    "p51": {
        "name": "서율 2호기",
        "model": "P-51 Mustang",
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
        "role": "TARGET HUNTER",
        "weapon_name": "TWIN + HOMING",
        "charge_name": "TWIN LOCK",
        "formation_name": "HUNTER WING",
    },
    "spitfire": {
        "name": "서율 3호기",
        "model": "Spitfire",
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
        "role": "HIGH-SPEED CHASER",
        "weapon_name": "RAPID TRACKERS",
        "charge_name": "TEMPEST BURST",
        "formation_name": "CYCLONE VOLLEY",
    },
    "bf109": {
        "name": "서율 4호기",
        "model": "Bf-109",
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
        "role": "ARMORED BREAKER",
        "weapon_name": "HEAVY CANNON",
        "charge_name": "ARMOR PIERCER",
        "formation_name": "FORTRESS BARRAGE",
    },
    "zero": {
        "name": "서율 5호기",
        "model": "A6M Zero",
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
        "role": "BULLET CONTROL",
        "weapon_name": "FAN PELLETS",
        "charge_name": "GALE RING",
        "formation_name": "SWEEPING FAN",
    },
    "shinden": {
        "name": "서율 6호기",
        "model": "J7W Shinden",
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
        "role": "BOSS MELTER",
        "weapon_name": "PRISM LASER",
        "charge_name": "PRISM BEAM",
        "formation_name": "TRI-LASER RUSH",
    },
    "raiden": {
        "name": "서율 7호기",
        "model": "X-7 Raiden",
        "pilot": "Seo Yul",
        "color": (100, 105, 155),
        "accent": (190, 100, 255),
        "speed_mult": 1.10,
        "shot_spread": 10,
        "weapon": "pulse",
        "bullet_kind": "violet",
        "sub_kind": "rocket",
        "fire_rate": 0.075,
        "bomb_id": "nova",
        "bomb_name": "Nova Breaker",
        "desc": "Pulse salvo · Rocket support",
        "role": "VERSATILE ACE",
        "weapon_name": "VIOLET PULSE",
        "charge_name": "NOVA SPEAR",
        "formation_name": "SEVEN STAR ARRAY",
    },
}
