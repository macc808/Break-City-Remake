import pygame
from config import img_player, WIDTH, HEIGHT
from entities.base import Base
from map.wall import wall_group
from logger import Logger

class Enemy(Base):
    def __init__(self, images, x, y, size, speed, ai_type):
        super().__init__(images, x, y, size, speed)
        self.ai_type = ai_type  # тип ИИ (например, "patrol", "chase", "random")
    
    def update(self):
        # Здесь можно реализовать логику ИИ для врага
        # Например, патрулирование, преследование игрока или случайное движение
        pass