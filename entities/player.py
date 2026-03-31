from keyboard import key
import pygame
from config import img_player, WIDTH, HEIGHT
from entities.base import Base
from map.wall import wall_group as Walls

class Player(Base):
    def __init__(self, images, x, y, size, speed, controls):
        super().__init__(images, x, y, size, speed)
        self.controls = controls  # словник клавіш
    

    def update(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[self.controls["left"]] and self.rect.x > 5:
            dx = -self.speed
            self.image = self.images["left"]
        if keys[self.controls["right"]] and self.rect.x < WIDTH - 50:
            dx = self.speed
            self.image = self.images["right"]
        if keys[self.controls["up"]] and self.rect.y > 5:
            dy = -self.speed
            self.image = self.images["up"]
        if keys[self.controls["down"]] and self.rect.y < HEIGHT - 50:
            dy = self.speed
            self.image = self.images["down"]
        
        self.rect.x += dx
        if any(self.rect.colliderect(w.rect) and not w.is_bush for w in Walls):
            self.rect.x -= dx

        self.rect.y += dy
        if any(self.rect.colliderect(w.rect) and not w.is_bush for w in Walls):
            self.rect.y -= dy