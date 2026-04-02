import pygame

class Base:
    def __init__(self, images, x, y, width, height=None, speed=0):
        super().__init__()
        if height is None:
            height = width
        self.base_width = width
        self.base_height = height
        self.speed = speed

        # Сохраняем исходные изображения, чтобы менять масштаб при повороте
        self.original_images = {k: pygame.image.load(v) for k, v in images.items()}
        self.set_direction("right")

        self.rect = self.image.get_rect(topleft=(x, y))

    def _rescale_images(self, width, height):
        self.images = {
            k: pygame.transform.scale(img, (width, height))
            for k, img in self.original_images.items()
        }

    def set_direction(self, direction):
        if direction not in self.original_images:
            return
        self.direction = direction

        if direction in ("left", "right"):
            width, height = self.base_width, self.base_height
        else:
            width, height = self.base_height, self.base_width

        center = None
        if hasattr(self, 'rect'):
            center = self.rect.center

        self._rescale_images(width, height)
        self.image = self.images[direction]

        if center is not None:
            self.rect = self.image.get_rect(center=center)
        else:
            self.rect = self.image.get_rect()

    def reset(self, surface=None):
        if surface is not None:
            surface.blit(self.image, self.rect.topleft)