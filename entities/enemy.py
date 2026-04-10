import pygame
import random
import math
from config import img_enemy, WIDTH, HEIGHT
from entities.base import Base
from entities.bullet import Bullet
from map.wall import wall_group
from logger import Logger
from utils.math_helpers import calculate_distance, calculate_direction_to_target, get_perpendicular_direction

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
        
        # Маппінг числових типів AI на рядкові (відповідно до config.py ENEMY_AI_TYPES)
        ai_type_map = {
            1: "sniper",     # Тип 1 - стріляє здалеку
            2: "speed",      # Тип 2 - підїжджає близько і кружляє
            3: "chase"       # Тип 3 - просто їде на гравця
        }
        
        # Якщо ai_type число, конвертуємо в рядок
        if isinstance(ai_type, int):
            self.ai_type = ai_type_map.get(ai_type, "chase")
        else:
            self.ai_type = ai_type or "chase"
        
        self.direction = "down"
        self.shoot_cooldown = 1.5 if self.ai_type == "sniper" else 1.0  # Снайпер рідше стріляє
        self._shoot_timer = 0.0
        self._move_timer = 0.0
        self.max_health = 30
        self.health = self.max_health
        self.is_dead = False
        
        # Параметри для различних AI типов
        self._target_player = None  # Посилання на гравця
        self._orbit_direction = random.choice(["clockwise", "counterclockwise"])  # Для speed типу
        self._orbit_timer = 0.0
        
        # Для chase типу - чергування рухів по осях
        self._move_horizontally = random.choice([True, False])
        self._direction_change_timer = 0.0
        
        # Для розумної системи стрільби
        self._can_see_player = False  # Чи бачить ворог гравця
        self._shoot_decision_timer = 0.0  # Таймер для випадкового вибору стрільби
        self._last_player_pos = None  # Для передбачення

    def take_damage(self, damage):
        """Зменшити здоров'я ворога"""
        self.health = max(0, self.health - damage)
        Logger().log_message(self.take_damage, f"Enemy took {damage} damage. Health: {self.health}/{self.max_health}")
        if self.health <= 0:
            self.is_dead = True
            Logger().log_message(self.take_damage, "Enemy died")
        return self.health
    
    def shoot(self, dt=0, player=None):
        """
        Розумна система стрільби з видимістю гравця та розворотом.
        
        Args:
            dt: Дельта часу
            player: Посилання на об'єкт гравця (для розрахунку випалу)
        """
        if self.is_dead or not player:
            return None
        
        # Розраховуємо видимість гравця та дистанцію
        distance = calculate_distance(
            self.rect.centerx, self.rect.centery,
            player.rect.centerx, player.rect.centery
        )
        
        # Визначити напрямок до гравця
        direction_to_player = calculate_direction_to_target(
            self.rect.centerx, self.rect.centery,
            player.rect.centerx, player.rect.centery
        )
        
        # **Новий напрямок = напрямок до гравця (розворот перед стрілянням)**
        self.direction = direction_to_player
        self.set_direction(self.direction)
        
        self._shoot_timer += dt
        self._shoot_decision_timer += dt
        
        # Різні умови стрільби для різних типів AI
        should_shoot = False
        
        if self.ai_type == "chase":
            # Chase танк: стріляє коли близько до гравця (< 200px) та рідко (50% шанс)
            if distance < 200 and self._shoot_timer >= self.shoot_cooldown:
                should_shoot = random.random() < 0.5  # 50% шанс стрільби
        
        elif self.ai_type == "speed":
            # Speed танк: стріляє коли на оптимальній дистанції та часто
            if 100 < distance < 250 and self._shoot_timer >= self.shoot_cooldown:
                should_shoot = random.random() < 0.7  # 70% шанс стрільби
        
        elif self.ai_type == "sniper":
            # Sniper: стріляє тільки на дистанції > 300px, рідко але точно
            if distance > 300 and self._shoot_timer >= self.shoot_cooldown:
                should_shoot = random.random() < 0.6  # 60% шанс стрільби
        
        if not should_shoot:
            return None
        
        # Передбічення ходу гравця - розраховуємо напрямок
        # де гравець найімовірніше буде через 0.5 сек
        predicted_pos = self._predict_player_position(player, 0.5)
        
        # Якщо передбічення відповідає напрямку - стріляємо в передбачене місце
        predicted_direction = calculate_direction_to_target(
            self.rect.centerx, self.rect.centery,
            predicted_pos[0], predicted_pos[1]
        )
        
        # 60% шанс стрільби в передбачене місце, 40% в поточне
        if random.random() < 0.6:
            self.direction = predicted_direction
        else:
            self.direction = direction_to_player
        
        self.set_direction(self.direction)
        
        self._shoot_timer = 0.0
        
        spawn_x = self.rect.centerx - 8
        spawn_y = self.rect.centery - 8
        Logger().log_message(self.shoot, f"Enemy ({self.ai_type}) shooting ({self.direction}) at distance {distance:.0f}px")
        return Bullet(spawn_x, spawn_y, self.direction, speed=8)
    
    def _predict_player_position(self, player, time_ahead=0.5):
        """
        Передбачити позицію гравця через заданий час.
        Використовується для попередуючого вогню.
        
        Args:
            player: Об'єкт гравця
            time_ahead: Час в секундах для передбічення
        
        Returns:
            tuple: (x, y) передбачена позиція
        """
        # Простий передбічення на основі напрямку руху гравця
        predicted_x = player.rect.centerx
        predicted_y = player.rect.centery
        
        # Якщо гравець рухається, додаємо його напрямок
        move_distance = player.speed * time_ahead * 60  # FPS ~60
        
        if player.direction == "up":
            predicted_y -= move_distance
        elif player.direction == "down":
            predicted_y += move_distance
        elif player.direction == "left":
            predicted_x -= move_distance
        elif player.direction == "right":
            predicted_x += move_distance
        
        # Обмежити до екрану
        predicted_x = max(0, min(predicted_x, WIDTH))
        predicted_y = max(0, min(predicted_y, HEIGHT))
        
        return (predicted_x, predicted_y)

    def update(self, dt=0, player=None):
        """
        Оновити позицію та поведінку ворога залежно від типу AI.
        
        Args:
            dt: Дельта часу
            player: Посилання на об'єкт гравця
        """
        if self.is_dead:
            return
        
        # Зберегти посилання на гравця для мети
        self._target_player = player
        
        dx, dy = 0, 0
        
        if self.ai_type == "chase":
            # CHASE: Просто їде на гравця - БЕЗ ДІАГОНАЛЕЙ
            # Рухається чергово по горизонталі та вертикалі (WASD стиль)
            if player:
                dx_to_player = player.rect.centerx - self.rect.centerx
                dy_to_player = player.rect.centery - self.rect.centery
                
                # Накопичуємо таймер для контролю частоти переключення напрямків
                self._direction_change_timer += dt
                
                # Визначити, рухатися горизонтально чи вертикально
                if abs(dx_to_player) > abs(dy_to_player) and self._move_horizontally:
                    # Рухатися по горизонталі
                    if dx_to_player > 0:
                        self.direction = "right"
                    else:
                        self.direction = "left"
                    # Перейти на вертикальний рух що 0.4 секунди або після невеликої відстані
                    if self._direction_change_timer > 0.4 and abs(dx_to_player) < 50:
                        self._move_horizontally = False
                        self._direction_change_timer = 0
                elif abs(dy_to_player) > abs(dx_to_player) or not self._move_horizontally:
                    # Рухатися по вертикалі
                    if dy_to_player > 0:
                        self.direction = "down"
                    else:
                        self.direction = "up"
                    # Перейти на горизонтальний рух що 0.4 секунди або після невеликої відстані
                    if self._direction_change_timer > 0.4 and abs(dy_to_player) < 50:
                        self._move_horizontally = True
                        self._direction_change_timer = 0
            else:
                # Якщо гравця нема (не повинно бути), рухатися випадково
                self._move_timer += dt
                if self._move_timer > 0.8:
                    self._move_timer = 0
                    self.direction = random.choice(["up", "down", "left", "right"])
        
        elif self.ai_type == "speed":
            # SPEED: Підїжджає близько (150px), кружляє та СТРІЛЯЄ
            if player:
                distance = calculate_distance(
                    self.rect.centerx, self.rect.centery,
                    player.rect.centerx, player.rect.centery
                )
                
                # Якщо далі за 150px - наближуватися
                if distance > 150:
                    self.direction = calculate_direction_to_target(
                        self.rect.centerx, self.rect.centery,
                        player.rect.centerx, player.rect.centery
                    )
                else:
                    # Якщо близько - АКТИВНО кружляти навколо (більше рухів)
                    self._orbit_timer += dt
                    if self._orbit_timer > 0.3:  # Частіше змінює напрямок
                        self._orbit_timer = 0
                        primary_direction = calculate_direction_to_target(
                            self.rect.centerx, self.rect.centery,
                            player.rect.centerx, player.rect.centery
                        )
                        
                        if self._orbit_direction == "clockwise":
                            # За годинниковою: вверх -> право -> вниз -> вліво
                            self.direction = get_perpendicular_direction(primary_direction)
                        else:
                            # Проти годинника: вверх -> вліво -> вниз -> право
                            opposite_map = {"right": "left", "left": "right", "up": "down", "down": "up"}
                            self.direction = opposite_map.get(
                                get_perpendicular_direction(primary_direction), "right"
                            )
        
        elif self.ai_type == "sniper":
            # SNIPER: Утримує дистанцію (300px) та стріляє
            if player:
                distance = calculate_distance(
                    self.rect.centerx, self.rect.centery,
                    player.rect.centerx, player.rect.centery
                )
                
                # Якщо ближче за 300px - відступати
                if distance < 300:
                    # Рухатися у протилежному напрямку від гравця
                    direction_to_player = calculate_direction_to_target(
                        self.rect.centerx, self.rect.centery,
                        player.rect.centerx, player.rect.centery
                    )
                    opposite_map = {
                        "up": "down", "down": "up",
                        "left": "right", "right": "left"
                    }
                    self.direction = opposite_map.get(direction_to_player, "up")
                else:
                    # Якщо на оптимальній дистанції - стояти та стріляти
                    self._move_timer += dt
                    if self._move_timer > 1.0:
                        self._move_timer = 0
                        # Нечасто рухатися
                        self.direction = random.choice(["up", "down", "left", "right", "stay", "stay", "stay"])
        
        # Застосувати рух на основі напрямку
        self.set_direction(self.direction)
        
        if self.direction == "up":
            dy = -self.speed
        elif self.direction == "down":
            dy = self.speed
        elif self.direction == "left":
            dx = -self.speed
        elif self.direction == "right":
            dx = self.speed
        # "stay" не змінює положення

        # Перевірити зіткнення стін
        self.rect.x += dx
        if any(self.rect.colliderect(w.rect) for w in wall_group):
            self.rect.x -= dx
        # Перевірити зіткнення з гравцем - враг не може залізти на гравця
        if player and self.rect.colliderect(player.rect):
            self.rect.x -= dx

        self.rect.y += dy
        if any(self.rect.colliderect(w.rect) for w in wall_group):
            self.rect.y -= dy
        # Перевірити зіткнення з гравцем по вертикалі
        if player and self.rect.colliderect(player.rect):
            self.rect.y -= dy

        # Обмежити положення до екрану
        self.rect.x = max(5, min(self.rect.x, WIDTH - self.rect.width - 5))
        self.rect.y = max(5, min(self.rect.y, HEIGHT - self.rect.height - 5))
