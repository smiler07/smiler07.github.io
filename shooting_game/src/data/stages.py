"""Stage definitions — each stage ends with a unique boss."""

STAGES: list[dict] = [
    {
        "id": 1,
        "name": "COASTAL ASSAULT",
        "boss_id": "tank",
        "boss_name": "IRON MECHA TANK",
        "boss_hp": 80,
        "events": [
            {"time": 3,  "type": "wave", "pattern": "line",        "count": 4, "kind": "fighter"},
            {"time": 10, "type": "wave", "pattern": "fleet",       "count": 2, "kind": "pt_boat"},
            {"time": 18, "type": "wave", "pattern": "red_pair",    "count": 2, "kind": "fighter_red"},
            {"time": 26, "type": "wave", "pattern": "convoy",      "count": 3, "kind": "tank"},
            {"time": 35, "type": "wave", "pattern": "v_formation", "count": 4, "kind": "zero"},
            {"time": 44, "type": "wave", "pattern": "bomber_line", "count": 2, "kind": "stuka"},
            {"time": 52, "type": "wave", "pattern": "sine",        "count": 5, "kind": "bf109"},
            {"time": 60, "type": "boss_warning"},
            {"time": 65, "type": "boss"},
        ],
    },
    {
        "id": 2,
        "name": "ENEMY AIRFIELD",
        "boss_id": "fortress",
        "boss_name": "SKY FORTRESS",
        "boss_hp": 100,
        "events": [
            {"time": 3,  "type": "wave", "pattern": "v_formation", "count": 5, "kind": "bf109"},
            {"time": 12, "type": "wave", "pattern": "bomber_line", "count": 3, "kind": "bomber"},
            {"time": 20, "type": "wave", "pattern": "red_swarm",   "count": 4, "kind": "fighter_red"},
            {"time": 28, "type": "wave", "pattern": "convoy",      "count": 2, "kind": "heavy_tank"},
            {"time": 36, "type": "wave", "pattern": "sine",        "count": 5, "kind": "zero"},
            {"time": 44, "type": "wave", "pattern": "bomber_line", "count": 3, "kind": "stuka"},
            {"time": 52, "type": "wave", "pattern": "line",        "count": 4, "kind": "fighter"},
            {"time": 58, "type": "boss_warning"},
            {"time": 63, "type": "boss"},
        ],
    },
    {
        "id": 3,
        "name": "FINAL STRIKE",
        "boss_id": "ace",
        "boss_name": "ACE SQUADRON",
        "boss_hp": 120,
        "events": [
            {"time": 3,  "type": "wave", "pattern": "fleet",       "count": 2, "kind": "destroyer"},
            {"time": 12, "type": "wave", "pattern": "red_swarm",   "count": 5, "kind": "fighter_red"},
            {"time": 20, "type": "wave", "pattern": "convoy",      "count": 3, "kind": "heavy_tank"},
            {"time": 28, "type": "wave", "pattern": "v_formation", "count": 6, "kind": "zero"},
            {"time": 36, "type": "wave", "pattern": "bomber_line", "count": 4, "kind": "bomber"},
            {"time": 44, "type": "wave", "pattern": "fleet",       "count": 3, "kind": "pt_boat"},
            {"time": 52, "type": "wave", "pattern": "sine",        "count": 6, "kind": "bf109"},
            {"time": 58, "type": "boss_warning"},
            {"time": 63, "type": "boss"},
        ],
    },
]

TOTAL_STAGES = len(STAGES)
