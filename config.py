import pygame
import sys

WIDTH = 960
HEIGHT = 640
FPS = 60

TILE_SIZE = 64

TILE_IMAGES = {
    0: None,
    1: "assets/images/floor.jpg",
    2: "assets/images/wall.jpg",
    3: "assets/images/road.jpg",
}

ENEMY_AI_TYPES = {
    1: "sniper",
    2: "speed",
    3: "chase"
}

img_player = {
    "down": "assets/images/player-down.jpg",
    "up": "assets/images/player-up.jpg",
    "left": "assets/images/player-left.jpg",
    "right": "assets/images/player-right.jpg"
}

img_enemy = {
    "down": "assets/images/enemy-down.jpg",
    "up": "assets/images/enemy-up.jpg",
    "left": "assets/images/enemy-left.jpg",
    "right": "assets/images/enemy-right.jpg"
}

img_bullet = {
    "down": "assets/images/bullet.png",
    "up": "assets/images/bullet.png",
    "left": "assets/images/bullet.png",
    "right": "assets/images/bullet.png"
}

# Фіксовані позиції спавнення для рівнів (15x15 GRID: 960x960 px)
SPAWN_POSITIONS = {
    1: [  # Level 1 - Outskirts (Легкий)
        (128, 0*64),      # top-left (col 2, row 0)
        (384, 0*64),      # top-center (col 6, row 0)
        (640, 0*64),      # top-right (col 10, row 0)
        (128, 14*64),     # bottom-left (col 2, row 14)
        (384, 14*64),     # bottom-center (col 6, row 14)
        (640, 14*64),     # bottom-right (col 10, row 14)
    ],
    2: [  # Level 2 - Suburbs (Середній)
        (64, 1*64),      # top-left (col 2, row 0)
        (7*64, 0*64),      # top-center (col 6, row 0)
        (13*64, 1*64),      # top-right (col 10, row 0)
        (2*64, 9*64),      # bottom-left (col 2, row 9)
        (7*64, 9*64),      # bottom-center (col 6, row 9)
        (13*64, 9*64),   # bottom-right (col 14, row 14)
    ],
    3: [  # Level 3 - Downtown (Складний)
        (64, 1*64),       # upper-left (col 1, row 1)
        (7*64, 3*64),      # upper-center-left (col 4, row 1)
        (13*64, 1*64),      # upper-center (col 8, row 1)
        (1*64, 9*64),       # middle-left (col 1, row 7)
        (7*64, 7*64),      # middle-center (col 10, row 7)
        (13*64, 9*64),     # bottom-right (col 14, row 14)
    ],
    4: [  # Level 4 - City Center (Дуже Складний)
        (64, 1*64),       # upper-left (col 1, row 1)
        (192, 1*64),      # upper-left-center (col 3, row 1)
        (384, 1*64),      # upper-center (col 6, row 1)
        (576, 1*64),      # upper-right-center (col 9, row 1)
        (768, 14*64),     # bottom-right-center (col 12, row 14)
        (896, 14*64),     # bottom-far-right (col 14, row 14)
    ],
    5: [  # Level 5 - Downtown Center (Екстремально Складний)
        (64, 1*64),       # upper-left (col 1, row 1)
        (320, 1*64),      # upper-center-left (col 5, row 1)
        (576, 1*64),      # upper-center-right (col 9, row 1)
        (832, 1*64),      # upper-right (col 13, row 1)
        (64, 14*64),      # bottom-left (col 1, row 14)
        (832, 14*64),     # bottom-right (col 13, row 14)
    ]
}

# ========================================
# ТИПИ AI ДЛЯ ВОРОГІВ
# ========================================
# 1 = "sniper"  - утримувати дистанцію (300px) та стріляти
# 2 = "speed"  - підїжджати близько (150px) та кружляти навколо
# 3 = "chase" - гонитися за гравцем (просто їде вперед)
# ========================================

# Конфігурація хвиль для рівнів
# AI типи: 1 = sniper (найслабкіший), 2 = speed, 3 = chase (найсильніший)
# Рівні 1-3: максимум 5 ворогів за хвилю
# Рівні 4-5: максимум 6 ворогів за хвилю
WAVES_CONFIG = {
    # ========== LEVEL 1: OUTSKIRTS (Окраїна міста) - Легкий ==========
    1: [
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 1x Sniper (найслабкіший)
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 1x Sniper
                {"ai_type": 2, "spawn_index": 1},  # 1x speed
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 2x Sniper 1x Speed
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 1, "spawn_index": 2},
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 2x Sniper + 2x Speed
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 1, "spawn_index": 2},
                {"ai_type": 2, "spawn_index": 3},
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 2x Sniper + 2x Speed
                {"ai_type": 1, "spawn_index": 1},
                {"ai_type": 2, "spawn_index": 2},
                {"ai_type": 2, "spawn_index": 3},
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 1x Sniper + 3x Speed
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 2, "spawn_index": 2},
                {"ai_type": 2, "spawn_index": 3},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 3x Speed + 2x sniper
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 2, "spawn_index": 2},
                {"ai_type": 1, "spawn_index": 3},
                {"ai_type": 1, "spawn_index": 4},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 1x Speed + 3x sniper + 1x chase
                {"ai_type": 1, "spawn_index": 1},
                {"ai_type": 1, "spawn_index": 2},
                {"ai_type": 1, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 2x Chase + 3x Sniper
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 1, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 1, "spawn_index": 4},
                ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 3x Chase + 2x speed (босс хвиля!)
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 2, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
            ]
        },
    ],
    
    # ========== LEVEL 2: SUBURBS (Передмістя) - Середній ==========
    2: [
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 1x Sniper + 1x Speed + 1x Chase
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 2x Speed + 1x Chase
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 1x Speed + 1x Sniper + 2x Chase
                {"ai_type": 1, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 2x Speed + 2x Chase
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 3x Speed + 2x Chase
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 2, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 2x Speed + 1x Sniper + 2x Chase
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 1, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 3x Sniper + 2x Chase
                {"ai_type": 1, "spawn_index": 1},
                {"ai_type": 1, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 3x Sniper + 3x Chase (босс)
                {"ai_type": 1, "spawn_index": 1},
                {"ai_type": 1, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
                {"ai_type": 3, "spawn_index": 5},
            ]
        },
    ],
    
    # ========== LEVEL 3: DOWNTOWN (Центр міста) - Складний ==========
    3: [
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 2x Sniper + 1x Chase
                {"ai_type": 1, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 1x Sniper + 2x Chase
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 4x Sniper
                {"ai_type": 1, "spawn_index": 1},
                {"ai_type": 1, "spawn_index": 2},
                {"ai_type": 1, "spawn_index": 3},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 4x Speed
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 2, "spawn_index": 2},
                {"ai_type": 2, "spawn_index": 3},
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 1x Sniper + 4x Chase
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
            ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 6x Chase (босс хвиля!)
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
                {"ai_type": 3, "spawn_index": 5},
            ]
        },
    ],
    
    # ========== LEVEL 4: CITY CENTER (Центр, Дуже Складний) ==========
    4: [
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 2x Sniper + 2x Speed
            ]
        },
    ],
    
    # ========== LEVEL 5: DOWNTOWN CENTER (Екстремально Складний) ==========
    5: [
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 1x Sniper + 4x Speed
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 2, "spawn_index": 2},
                {"ai_type": 2, "spawn_index": 3},
                {"ai_type": 2, "spawn_index": 4},
                {"ai_type": 2, "spawn_index": 5},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 3x Speed + 3x Chase
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 2, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
                {"ai_type": 3, "spawn_index": 5},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 1x Speed + 5x Chase
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
                {"ai_type": 3, "spawn_index": 5},
            ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 6x Chase (сильна)
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
                {"ai_type": 3, "spawn_index": 5},
            ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 6x Chase (босс хвиля!)
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
                {"ai_type": 3, "spawn_index": 5},
            ]
        },
    ],
}