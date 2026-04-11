import pygame
from config import img_player, WIDTH, HEIGHT
from entities.base import Base
from entities.bullet import Bullet
from map.wall import wall_group
from logger import Logger

class Player(Base):
    def __init__(self, images, x, y, width, height=None, speed=None, controls=None):
        # Поддерживаем старый вызов: (images, x, y, size, speed, controls)
        if isinstance(speed, dict):
            controls = speed
            speed = height
            height = width
        if height is None:
            height = width
        if speed is None:
            speed = 0

        super().__init__(images, x, y, width, height, speed)
        self.controls = controls or {}  # словник клавіш
        self.direction = "up"
        self.shoot_cooldown = 0.35
        self._shoot_timer = 0.0
        self.max_health = 1000
        self.health = self.max_health
        self.is_dead = False
    
    def take_damage(self, damage):
        """Зменшити здоров'я гравця"""
        self.health = max(0, self.health - damage)
        Logger().log_message(self.take_damage, f"Player took {damage} damage. Health: {self.health}/{self.max_health}")
        if self.health <= 0:
            self.is_dead = True
            Logger().log_message(self.take_damage, "Player died")
        return self.health
    
    def shoot(self):
        if self._shoot_timer < self.shoot_cooldown:
            return None

        self._shoot_timer = 0.0
        spawn_x = self.rect.centerx - 8
        spawn_y = self.rect.centery - 8
        Logger().log_message(self.shoot, f"Player shooting ({self.direction}) from x={spawn_x}, y={spawn_y}")
        return Bullet(spawn_x, spawn_y, self.direction)

    def update(self, dt):
        self._shoot_timer = min(self._shoot_timer + dt, self.shoot_cooldown)

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        left_pressed = ((self.controls.get("left1") is not None and keys[self.controls.get("left1")])
                        or (self.controls.get("left2") is not None and keys[self.controls.get("left2")]))
        right_pressed = ((self.controls.get("right1") is not None and keys[self.controls.get("right1")])
                         or (self.controls.get("right2") is not None and keys[self.controls.get("right2")]))
        up_pressed = ((self.controls.get("up1") is not None and keys[self.controls.get("up1")])
                      or (self.controls.get("up2") is not None and keys[self.controls.get("up2")]))
        down_pressed = ((self.controls.get("down1") is not None and keys[self.controls.get("down1")])
                        or (self.controls.get("down2") is not None and keys[self.controls.get("down2")]))

        if left_pressed and not right_pressed and self.rect.x > 5:
            dx = -self.speed
            self.set_direction("left")
            Logger().log_message(self.update, f"Moving left to x={self.rect.x + dx}")
        elif right_pressed and not left_pressed and self.rect.x < WIDTH - self.rect.width - 5:
            dx = self.speed
            self.set_direction("right")
            Logger().log_message(self.update, f"Moving right to x={self.rect.x + dx}")
        elif up_pressed and not down_pressed and self.rect.y > 5:
            dy = -self.speed
            self.set_direction("up")
            Logger().log_message(self.update, f"Moving up to y={self.rect.y + dy}")
        elif down_pressed and not up_pressed and self.rect.y < HEIGHT - self.rect.height - 5:
            dy = self.speed
            self.set_direction("down")
            Logger().log_message(self.update, f"Moving down to y={self.rect.y + dy}")

        # Apply horizontal movement with knockback collision
        self.rect.x += dx
        colliding = [w for w in wall_group if self.rect.colliderect(w.rect)]
        if colliding:
            wall = colliding[0]
            knockback_dist = 8  # Pixels to push player away
            if dx > 0:  # Moving right, push left
                self.rect.x = wall.rect.left - self.rect.width - knockback_dist
                Logger().log_message(self.update, f"Right collision: pushed left to x={self.rect.x}")
            elif dx < 0:  # Moving left, push right
                self.rect.x = wall.rect.right + knockback_dist
                Logger().log_message(self.update, f"Left collision: pushed right to x={self.rect.x}")

        # Apply vertical movement with knockback collision
        self.rect.y += dy
        colliding = [w for w in wall_group if self.rect.colliderect(w.rect)]
        if colliding:
            wall = colliding[0]
            knockback_dist = 8  # Pixels to push player away
            if dy > 0:  # Moving down, push up
                self.rect.y = wall.rect.top - self.rect.height - knockback_dist
                Logger().log_message(self.update, f"Down collision: pushed up to y={self.rect.y}")
            elif dy < 0:  # Moving up, push down
                self.rect.y = wall.rect.bottom + knockback_dist
                Logger().log_message(self.update, f"Up collision: pushed down to y={self.rect.y}")