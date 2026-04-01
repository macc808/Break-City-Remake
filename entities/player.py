import pygame
from config import img_player, WIDTH, HEIGHT
from entities.base import Base
from map.wall import wall_group
from logger import Logger

class Player(Base):
    def __init__(self, images, x, y, size, speed, controls):
        super().__init__(images, x, y, size, speed)
        self.controls = controls  # словник клавіш
    

    def update(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        left_pressed = keys[self.controls.get("left1")] or keys[self.controls.get("left2")]
        right_pressed = keys[self.controls.get("right1")] or keys[self.controls.get("right2")]
        up_pressed = keys[self.controls.get("up1")] or keys[self.controls.get("up2")]
        down_pressed = keys[self.controls.get("down1")] or keys[self.controls.get("down2")]

        if left_pressed and self.rect.x > 5:
            dx = -self.speed
            self.image = self.images["left"]
            Logger().log_message(self.update, f"Moving left to x={self.rect.x + dx}")
        if right_pressed and self.rect.x < WIDTH - 50:
            dx = self.speed
            self.image = self.images["right"]
            Logger().log_message(self.update, f"Moving right to x={self.rect.x + dx}")
        if up_pressed and self.rect.y > 5:
            dy = -self.speed
            self.image = self.images["up"]
            Logger().log_message(self.update, f"Moving up to y={self.rect.y + dy}")
        if down_pressed and self.rect.y < HEIGHT - 50:
            dy = self.speed
            self.image = self.images["down"]
            Logger().log_message(self.update, f"Moving down to y={self.rect.y + dy}")

        self.rect.x += dx
        if any(self.rect.colliderect(w.rect) for w in wall_group):
            self.rect.x -= dx
            Logger().log_message(self.update, f"Collision detected at x={self.rect.x}, reverting to x={self.rect.x - dx}")

        self.rect.y += dy
        if any(self.rect.colliderect(w.rect) for w in wall_group):
            self.rect.y -= dy
            Logger().log_message(self.update, f"Collision detected at y={self.rect.y}, reverting to y={self.rect.y - dy}")