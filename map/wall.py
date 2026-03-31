from pygame import *
from config import block_img

class block:
    def __init__(self, block_img, x, y, size):
        super().__init__()
        self.images = {k: transform.scale(image.load(v), (size, size)) for k, v in block_img.items()}
        self.rect = self.image.get_rect(topleft=(x, y))

class Wall:
    def __init__(self, image_path, x, y, size_x, size_y, is_breakble=False):
        super().__init__()
        self.image = transform.scale(image.load(image_path), (size_x, size_y))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_breakble = is_breakble
    def add(self, image_path, x, y, size_x, size_y, is_breakble):
        Walls.add(Wall(image_path, x, y, size_x, size_y, is_breakble))

class Title:
    def __init__(self, image_path, x, y, size_x, size_y, is_breakble=False):
        super().__init__()
        self.image = transform.scale(image.load(image_path), (size_x, size_y))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.layer = 1

Walls = block.Group()