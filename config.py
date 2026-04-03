import pygame
import sys

WIDTH = 960
HEIGHT = 640
FPS = 60

TILE_SIZE = 64

TILE_IMAGES = {
    0: None,
    1: "assets/images/floor.jpg",
    2: "assets/images/floor1.png",
    3: "assets/images/wall.jpg",
    4: "assets/images/road.jpg",
    5: "assets/images/road1.jpg",
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