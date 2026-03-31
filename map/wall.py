import pygame
from config import TILE_SIZE

class FloorTile(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, size=TILE_SIZE):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

class Wall(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, size=TILE_SIZE, is_breakable=False):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_breakable = is_breakable

class Tile(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, size=TILE_SIZE):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert_alpha(), (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

floor_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
