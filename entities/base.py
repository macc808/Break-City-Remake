import pygame

class Base:
    def __init__(self, images, x, y, size, speed):
        super().__init__()
        self.images = {k: pygame.transform.scale(pygame.image.load(v), (size, size)) for k, v in images.items()}
        self.image = self.images["right"]
        self.speed = speed
        self.rect = self.image.get_rect(topleft=(x, y))
    
    def reset(self, surface=None):
        if surface is not None:
            surface.blit(self.image, self.rect.topleft)