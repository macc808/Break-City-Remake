import pygame
from config import img_bullet, WIDTH, HEIGHT
from entities.base import Base
from map.wall import wall_group
from logger import Logger

class Bullet(Base):
    def __init__(self, x, y, direction, width=16, height=None, speed=10, is_enemy=False, damage=15):
        super().__init__(img_bullet, x, y, width, height, speed)
        self.direction = direction  # направление движения ("up", "down", "left", "right")
        self.damage = damage  # Шкода, яку наносить пуля
        self.set_direction(direction)

    def set_direction(self, direction):
        # Установить направление и визуально разворачивать пулю
        super().set_direction(direction)

        center = self.rect.center
        if direction == "up":
            self.image = pygame.transform.rotate(self.image, 90)
        elif direction == "down":
            self.image = pygame.transform.rotate(self.image, -90)
        elif direction == "left":
            self.image = pygame.transform.rotate(self.image, 180)
        elif direction == "right":
            self.image = self.image  # уже вправо

        self.rect = self.image.get_rect(center=center)

    def update(self):
        """
        Обновить позицію пулі та розрахувати колізії.
        
        Returns:
            bool: True якщо пулю потрібно видалити, False інакше
        """
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

        # Перевірити границі екрану ПЕРЕД рухом
        if self.rect.right + dx < 0 or self.rect.left + dx > WIDTH or \
           self.rect.bottom + dy < 0 or self.rect.top + dy > HEIGHT:
            Logger().log_message(self.update, f"Bullet left screen at x={self.rect.x}, y={self.rect.y}")
            return True

        # Рух по горизонталі
        self.rect.x += dx
        # Перевірити зіткнення зі стінами по горизонталі
        if any(self.rect.colliderect(w.rect) for w in wall_group):
            Logger().log_message(self.update, f"Bullet blocked by wall at x={self.rect.x}")
            return True

        # Рух по вертикалі
        self.rect.y += dy
        # Перевірити зіткнення зі стінами по вертикалі
        if any(self.rect.colliderect(w.rect) for w in wall_group):
            Logger().log_message(self.update, f"Bullet blocked by wall at y={self.rect.y}")
            return True

        return False