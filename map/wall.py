import pygame
from config import TILE_SIZE

def load_tile_image(image_path, size):
    image = pygame.image.load(image_path).convert_alpha()
    w, h = image.get_size()

    # Обрізати артефактні білі облямівки по краях (якщо вони є)
    if w > 2 and h > 2:
        image = image.subsurface((1, 1, w - 2, h - 2)).copy()

    # Уникаємо прямих артефактів масштабування. Якість краще, якщо smoothscale.
    image = pygame.transform.smoothscale(image, (size, size))
    return image

class FloorTile(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, size=TILE_SIZE):
        super().__init__()
        self.image = load_tile_image(image_path, size)
        self.rect = self.image.get_rect(topleft=(x, y))

class Wall(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, size=TILE_SIZE, is_breakable=False):
        super().__init__()
        self.image = load_tile_image(image_path, size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_breakable = is_breakable

class Tile(pygame.sprite.Sprite):
    def __init__(self, image_path, x, y, size=TILE_SIZE):
        super().__init__()
        self.image = load_tile_image(image_path, size)
        self.rect = self.image.get_rect(topleft=(x, y))

floor_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
