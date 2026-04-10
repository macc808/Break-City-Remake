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
    1: [  # Level 1
        (64, 64),      # top-left
        (640, 64),     # top-center
        (896, 64),     # top-right
        (64, 576),     # bottom-left
        (640, 576),    # bottom-center
        (896, 576),    # bottom-right
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
# Легко настроювати: змінюйте ai_type (1, 2, 3) та spawn_index (0-5)
WAVES_CONFIG = {
    1: [  # Level 1 - 10 хвиль
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 1x Chase на позиції 0
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 1},  # 2x Chase
                {"ai_type": 1, "spawn_index": 2},
            ]
        },
        {
            "enemies": [
                {"ai_type": 1, "spawn_index": 0},  # 1x Speed + 2x Chase
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 2x Speed + 2x Chase
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 1, "spawn_index": 2},
                {"ai_type": 1, "spawn_index": 3},
            ]
        },
        {
            "enemies": [
                {"ai_type": 2, "spawn_index": 0},  # 3x Speed + 1x Chase
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 2, "spawn_index": 2},
                {"ai_type": 1, "spawn_index": 3},
            ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 1x Sniper + 3x Speed + 1x Chase
                {"ai_type": 2, "spawn_index": 1},
                {"ai_type": 2, "spawn_index": 2},
                {"ai_type": 2, "spawn_index": 3},
                {"ai_type": 1, "spawn_index": 4},
            ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 2x Sniper + 3x Speed
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 2, "spawn_index": 2},
                {"ai_type": 2, "spawn_index": 3},
                {"ai_type": 2, "spawn_index": 4},
            ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 3x Sniper + 2x Speed
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 2, "spawn_index": 3},
                {"ai_type": 2, "spawn_index": 4},
            ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 4x Sniper + 2x Speed
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 2, "spawn_index": 4},
                {"ai_type": 2, "spawn_index": 5},
            ]
        },
        {
            "enemies": [
                {"ai_type": 3, "spawn_index": 0},  # 6x Sniper (найскладніша хвиля!)
                {"ai_type": 3, "spawn_index": 1},
                {"ai_type": 3, "spawn_index": 2},
                {"ai_type": 3, "spawn_index": 3},
                {"ai_type": 3, "spawn_index": 4},
                {"ai_type": 3, "spawn_index": 5},
            ]
        },
    ]
}