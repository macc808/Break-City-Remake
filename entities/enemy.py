import pygame
import random
from config import img_enemy, WIDTH, HEIGHT
from entities.base import Base
from entities.bullet import Bullet
from map.wall import wall_group
from logger import Logger

class Enemy(Base):
    def __init__(self, images, x, y, width, height=None, speed=None, ai_type=None):
        # Поддерживаем старий виклик: (images, x, y, size, speed, ai_type)
        if isinstance(speed, str):
            ai_type = speed
            speed = height
            height = width
        if height is None:
            height = width
        if speed is None:
            speed = 0

        super().__init__(images, x, y, width, height, speed)
        self.ai_type = ai_type or "random"  # тип ІІ (наприклад, "patrol", "chase", "random")
        self.direction = "down"
        self.shoot_cooldown = 1.0
        self._shoot_timer = 0.0
        self._move_timer = 0.0
        self.max_health = 30
        self.health = self.max_health
        self.is_dead = False

    def take_damage(self, damage):
        """Зменшити здоров'я ворога"""
        self.health = max(0, self.health - damage)
        Logger().log_message(self.take_damage, f"Enemy took {damage} damage. Health: {self.health}/{self.max_health}")
        if self.health <= 0:
            self.is_dead = True
            Logger().log_message(self.take_damage, "Enemy died")
        return self.health
    
    def shoot(self, dt=0):
        if self.is_dead:
            return None
        self._shoot_timer += dt
        if self._shoot_timer < self.shoot_cooldown:
            return None

        self._shoot_timer = 0.0
        spawn_x = self.rect.centerx - 8
        spawn_y = self.rect.centery - 8
        Logger().log_message(self.shoot, f"Enemy shooting ({self.direction}) from x={spawn_x}, y={spawn_y}")
        return Bullet(spawn_x, spawn_y, self.direction, speed=8)

    def update(self, dt=0):
        self._move_timer += dt
        if self._move_timer > 0.8:
            self._move_timer = 0
            self.direction = random.choice(["up", "down", "left", "right"])

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
            self.rect.x -= dx

        self.rect.y += dy
        if any(self.rect.colliderect(w.rect) for w in wall_group):
            self.rect.y -= dy

        # Clamp to screen
        self.rect.x = max(5, min(self.rect.x, WIDTH - self.rect.width - 5))
        self.rect.y = max(5, min(self.rect.y, HEIGHT - self.rect.height - 5))
