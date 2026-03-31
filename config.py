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
}

img_player = {
    "down": "assets/images/player-down.jpg",
    "up": "assets/images/player-up.jpg",
    "left": "assets/images/player-left.jpg",
    "right": "assets/images/player-right.jpg"
}