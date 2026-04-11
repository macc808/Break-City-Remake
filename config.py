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

# Фіксовані позиції спавнення для рівнів
SPAWN_POSITIONS = {
    1: [  # Level 1 - Outskirts (Легкий)
        (128, 0*64),      # top-left area (col 2, row 0)
        (384, 0*64),      # top-center area (col 6, row 0)
        (640, 0*64),      # top-right area (col 10, row 0)
        (128, 10*64),     # bottom-left area (col 2, row 10)
        (384, 10*64),     # bottom-center area (col 6, row 10)
        (640, 10*64),     # bottom-right area (col 10, row 10)
    ],
    2: [  # Level 2 - Suburbs (Середній)
        (64, 11*64),      # bottom-left safe (col 1, row 11)
        (256, 11*64),     # bottom-center-left safe (col 4, row 11)
        (512, 11*64),     # bottom-center safe (col 8, row 11)
        (704, 11*64),     # bottom-center-right safe (col 11, row 11)
        (832, 11*64),     # bottom-right safe (col 13, row 11)
        (896, 11*64),     # bottom-far-right safe (col 14, row 11)
    ],
    3: [  # Level 3 - Downtown (Складний)
        (64, 11*64),      # bottom-left safe (col 1, row 11)
        (256, 11*64),     # bottom-center-left safe (col 4, row 11)
        (512, 11*64),     # bottom-center safe (col 8, row 11)
        (704, 11*64),     # bottom-center-right safe (col 11, row 11)
        (832, 11*64),     # bottom-right safe (col 13, row 11)
        (896, 11*64),     # bottom-far-right safe (col 14, row 11)
    ],
    4: [  # Level 4 - City Center (Дуже Складний)
        (64, 11*64),      # bottom-left safe (col 1, row 11)
        (192, 11*64),     # bottom-center-left safe (col 3, row 11)
        (384, 11*64),     # bottom-center safe (col 6, row 11)
        (576, 11*64),     # bottom-center-right safe (col 9, row 11)
        (768, 11*64),     # bottom-right safe (col 12, row 11)
        (896, 11*64),     # bottom-far-right safe (col 14, row 11)
    ],
    5: [  # Level 5 - Downtown Center (Екстремально Складний)
        (64, 1*64),       # top-left safe (col 1, row 1)
        (320, 1*64),      # top-center-left safe (col 5, row 1)
        (576, 1*64),      # top-center-right safe (col 9, row 1) - FIXED from (512, 64)
        (832, 1*64),      # top-right safe (col 13, row 1) - CHANGED from (704, 64)
        (64, 9*64),       # bottom-left safe (col 1, row 9)
        (832, 9*64),      # bottom-right safe (col 13, row 9)
    ]
}

# ========================================
# ТИПИ AI ДЛЯ ВОРОГІВ
# ========================================
# 1 = "chase"  - гонитися за гравцем (просто їде вперед)
# 2 = "speed"  - підїжджати близько (150px) та кружляти навколо
# 3 = "sniper" - утримувати дистанцію (300px) та стріляти
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
                {"ai_type": 1, "spawn_index": 0},  # 2x Sniper
                {"ai_type": 1, "spawn_index": 1},
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 3x Sniper
                {"ai_type": 1, "spawn_index": 1},
                {"ai_type": 1, "spawn_index": 2},
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 3x Sniper + 1x Speed
                {"ai_type": 1, "spawn_index": 1},
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
                {"ai_type": 2, "spawn_index": 0},  # 2x Speed + 2x Chase
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 1x Speed + 3x Chase
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
            ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 4x Chase
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
            ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 5x Chase (босс хвиля!)
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
            ]
        },
    ],
    
    # ========== LEVEL 2: SUBURBS (Передмістя) - Середній ==========
    2: [
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 2x Sniper
                {"ai_type": 1, "spawn_index": 1},
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 3x Sniper
                {"ai_type": 1, "spawn_index": 1},
                {"ai_type": 1, "spawn_index": 2},
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
                {"ai_type": 2, "spawn_index": 0},  # 2x Speed + 2x Chase
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 1x Speed + 4x Chase
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
            ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 5x Chase
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
            ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 5x Chase (босс)
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
            ]
        },
    ],
    
    # ========== LEVEL 3: DOWNTOWN (Центр міста) - Складний ==========
    3: [
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 3x Sniper
                {"ai_type": 1, "spawn_index": 1},
                {"ai_type": 1, "spawn_index": 2},
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
                {"ai_type": 2, "spawn_index": 0},  # 2x Speed + 3x Chase
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
            ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 5x Chase
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
            ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 5x Chase (босс хвиля!)
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
            ]
        },
    ],
    
    # ========== LEVEL 4: CITY CENTER (Центр, Дуже Складний) ==========
    4: [
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
                {"ai_type": 1, "spawn_index": 0},  # 1x Sniper + 4x Speed
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 2, "spawn_index": 2},
                {"ai_type": 2, "spawn_index": 3},
                {"ai_type": 2, "spawn_index": 4},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 2x Speed + 4x Chase
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
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
                {"ai_type": 3, "spawn_index": 0},  # 6x Chase
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
                {"ai_type": 3, "spawn_index": 0},  # 6x Chase (босс!)
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
                {"ai_type": 3, "spawn_index": 5},
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