import pygame
from config import img_bullet, WIDTH, HEIGHT
from entities.base import Base
from map.wall import wall_group
from logger import Logger

class Bullet(Base):
    def __init__(self, x, y, direction, width=16, height=None, speed=10):
        super().__init__(img_bullet, x, y, width, height, speed)
        self.set_direction(direction)
        self.direction = direction  # направление движения ("up", "down", "left", "right")

    def update(self):
        dx, dy = 0, 0
        if self.direction == "up":
            dy = -self.speed
            self.set_direction("up")
        elif self.direction == "down":
            dy = self.speed
            self.set_direction("down")
        elif self.direction == "left":
            dx = -self.speed
            self.set_direction("left")
        elif self.direction == "right":
            dx = self.speed
            self.set_direction("right")

        self.rect.x += dx
        if any(self.rect.colliderect(w.rect) for w in wall_group):
            Logger().log_message(self.update, f"Bullet collided with wall at x={self.rect.x}, removing bullet")
            return True

        self.rect.y += dy
        if any(self.rect.colliderect(w.rect) for w in wall_group):
            Logger().log_message(self.update, f"Bullet collided with wall at y={self.rect.y}, removing bullet")
            return True

        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            Logger().log_message(self.update, f"Bullet left screen at x={self.rect.x}, y={self.rect.y}")
            return True

        return False