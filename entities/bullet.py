import pygame
from config import img_player, WIDTH, HEIGHT
from entities.base import Base
from map.wall import wall_group
from logger import Logger

class Bullet(Base):
    def __init__(self, images, x, y, size, speed, direction):
        super().__init__(images, x, y, size, speed)
        self.direction = direction  # направление движения (например, "up", "down", "left", "right")
    
    def update(self):
        dx, dy = 0, 0
        if self.direction == "up":
            dy = -self.speed
        elif self.direction == "down":
            dy = self.speed
        elif self.direction == "left":
            dx = -self.speed
        elif self.direction == "right":
            dx = self.speed

        self.rect.x += dx
        if any(self.rect.colliderect(w.rect) for w in wall_group):
            Logger().log_message(self.update, f"Bullet collided with wall at x={self.rect.x}, removing bullet")
            # Здесь можно добавить логику для удаления пули из игры

        self.rect.y += dy
        if any(self.rect.colliderect(w.rect) for w in wall_group):
            Logger().log_message(self.update, f"Bullet collided with wall at y={self.rect.y}, removing bullet")
            # Здесь можно добавить логику для удаления пули из игры