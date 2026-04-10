import os
import sys
import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d
from entities.player import Player
from entities.enemy import Enemy
from entities.bullet import Bullet
from entities.factory import WaveManager
from config import img_player, WIDTH, HEIGHT, img_enemy, TILE_SIZE
from core.engine import Engine
from core.scene_manager import Scene, SceneManager
from map.level_loader import load_level_from_txt
from map.wall import floor_group, wall_group
from logger import Logger
from ui.elements import HealthBar, PauseButton, PauseMenu


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

LEVEL_PATH = "assets/levels/level_01.txt"


class PlayScene(Scene):
    def __init__(self, name="play", level=1):
        super().__init__(name)
        self.level = level
        self.engine = Engine()
        self.player = Player(img_player, WIDTH - 70, HEIGHT - 50, 55, 35, 5, {
            "up1": K_UP, "down1": K_DOWN, "left1": K_LEFT, "right1": K_RIGHT,
            "up2": K_w, "down2": K_s, "left2": K_a, "right2": K_d,
        })
        self.wave_manager = WaveManager(level)
        self.enemies = []
        self.player_bullets = []
        self.enemy_bullets = []
        
        # UI елементи
        self.health_bar = HealthBar(self.player.max_health, x=10, y=10, width=300, height=30)
        self.health_bar.update(self.player.health)  # Ініціалізуємо здоров'я
        self.pause_button = PauseButton()
        self.pause_menu = PauseMenu()
        
        # Стан паузи
        self.is_paused = False

    def start(self):
        load_level_from_txt(LEVEL_PATH)
        self._reset_game_state()
    
    def _reset_game_state(self):
        """Скинути стан гри до початкових значень"""
        # Скинути гравця
        self.player.health = self.player.max_health
        self.player.is_dead = False
        self.player.rect.x = WIDTH - 70
        self.player.rect.y = HEIGHT - 50
        
        # Скинути ворогів
        self.enemies.clear()
        self.player_bullets.clear()
        self.enemy_bullets.clear()
        
        # Скинути хвилі
        self.wave_manager = WaveManager(self.level)
        
        # Скинути UI
        self.health_bar.update(self.player.health)
        self.is_paused = False

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        
        # Обробка паузи
        if self.is_paused:
            action = self.pause_menu.handle_click(event)
            if action == "continue":
                self.is_paused = False
            elif action == "menu":
                Game._current_instance.scene_manager.set_scene("menu")
            elif action == "quit":
                pygame.quit()
                sys.exit(0)
        else:
            # Перевірка кліку на кнопку паузи
            if self.pause_button.is_clicked(event):
                self.is_paused = True

    def update(self, dt):
        # Якщо гра на паузі, не оновлюємо
        if self.is_paused:
            return
        
        self.engine.update(dt)
        self.player.update(dt)
        
        # Обновить wave manager и спавнить новых врагов
        new_enemies = self.wave_manager.update(dt)
        self.enemies.extend(new_enemies)
        
        for enemy in self.enemies:
            enemy.update(dt, self.player)

        # ===== КОЛІЗІЯ ГРАВЦЯ З ВОРОГАМИ =====
        # Гравець не може залізти на ворогів
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect) and not enemy.is_dead:
                # Повернути гравця на попередню позицію залежно від його напрямку
                if self.player.direction == "up":
                    self.player.rect.y += self.player.speed
                elif self.player.direction == "down":
                    self.player.rect.y -= self.player.speed
                elif self.player.direction == "left":
                    self.player.rect.x += self.player.speed
                elif self.player.direction == "right":
                    self.player.rect.x -= self.player.speed

        # ===== КОЛІЗІЯ ТАНКІВ =====
        # Ворожні танки не можуть проїжджати один через одного
        for i, enemy in enumerate(self.enemies):
            for other_enemy in self.enemies[i+1:]:
                if enemy.rect.colliderect(other_enemy.rect) and not enemy.is_dead and not other_enemy.is_dead:
                    # Розштовхати танки в різні боки
                    dx = other_enemy.rect.centerx - enemy.rect.centerx
                    dy = other_enemy.rect.centery - enemy.rect.centery
                    
                    # Який напрямок важливіший
                    if abs(dx) > abs(dy):
                        # Розштовхати по горизонталі
                        if dx > 0:
                            enemy.rect.x -= 2
                            other_enemy.rect.x += 2
                        else:
                            enemy.rect.x += 2
                            other_enemy.rect.x -= 2
                    else:
                        # Розштовхати по вертикалі
                        if dy > 0:
                            enemy.rect.y -= 2
                            other_enemy.rect.y += 2
                        else:
                            enemy.rect.y += 2
                            other_enemy.rect.y -= 2

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bullet = self.player.shoot()
            if bullet:
                self.player_bullets.append(bullet)

        for enemy in self.enemies:
            enemy_shot = enemy.shoot(dt, self.player)
            if enemy_shot:
                self.enemy_bullets.append(enemy_shot)

        for bullet in self.player_bullets[:]:
            remove = bullet.update()
            if remove:
                self.player_bullets.remove(bullet)
                continue
            
            # Перевірка зіткнення з ворогами
            for enemy in self.enemies[:]:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.take_damage(10)  # 10 урону за попадання
                    Logger().log_message(self.update, f"Enemy hit! Health: {enemy.health}")
                    if bullet in self.player_bullets:
                        self.player_bullets.remove(bullet)
                    if enemy.is_dead:
                        Logger().log_message(self.update, "Enemy defeated!")
                        self.enemies.remove(enemy)
                    break

        for bullet in self.enemy_bullets[:]:
            remove = bullet.update()
            if remove:
                self.enemy_bullets.remove(bullet)
                continue
            
            # Перевірка зіткнення з гравцем
            if bullet.rect.colliderect(self.player.rect):
                self.player.take_damage(15)  # 15 урону за попадання
                # Оновлюємо display здоров'я
                self.health_bar.update(self.player.health)
                Logger().log_message(self.update, f"Player hit! Health: {self.player.health}")
                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(bullet)
                if self.player.is_dead:
                    Logger().log_message(self.update, "Player defeated!")
        
        # Оновити статус хвилі на основі живих врагів
        self.wave_manager.update_wave_status(self.enemies)
        
        # ===== ПЕРЕВІРКА WIN/LOSS УМОВ =====
        # Гравець програв
        if self.player.is_dead:
            Logger().log_message(self.update, "Player defeated! Going to lose screen.")
            Game._current_instance.scene_manager.set_scene("lose")
            return
        
        # Гравець виграв (всі хвилі закінчились і нема живих ворогів)
        if self.wave_manager.is_finished() and len(self.enemies) == 0:
            Logger().log_message(self.update, "All waves defeated! Going to win screen.")
            Game._current_instance.scene_manager.set_scene("win")
            return

    def draw(self, screen):
        screen.fill((30, 30, 30))
        floor_group.draw(screen)
        wall_group.draw(screen)
        self.player.reset(screen)
        for enemy in self.enemies:
            enemy.reset(screen)

        for bullet in self.player_bullets + self.enemy_bullets:
            bullet.reset(screen)
        
        # Отобразить информацию о волне
        self._draw_wave_info(screen)
        
        # Отобразить жизни гравца
        self.health_bar.draw(screen)
        
        # Отобразить кнопку паузи
        mouse_pos = pygame.mouse.get_pos()
        self.pause_button.update(mouse_pos)
        self.pause_button.draw(screen)
        
        # Если игра на паузе, вывести меню паузи
        if self.is_paused:
            self.pause_menu.update(mouse_pos)
            self.pause_menu.draw(screen)
    
    def _draw_wave_info(self, screen):
        """Отобразить информацию о текущей волне на экране"""
        font = pygame.font.Font(None, 36)
        wave_text = f"Wave: {self.wave_manager.get_current_wave()}/{self.wave_manager.get_total_waves()}"
        text_surface = font.render(wave_text, True, (255, 255, 255))
        screen.blit(text_surface, (WIDTH - 250, 20))


class MenuScene(Scene):
    """Головне меню гри"""
    def __init__(self, name="menu"):
        super().__init__(name)
        self.font_title = pygame.font.Font(None, 72)
        self.font_button = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Кнопка START
        self.start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 60)
        self.start_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_hovered:
                # Переходимо до гри
                from core.game import Game as GameClass
                if hasattr(GameClass, '_current_instance'):
                    GameClass._current_instance.scene_manager.set_scene("play")

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.start_hovered = self.start_button.collidepoint(mouse_pos)

    def draw(self, screen):
        screen.fill((20, 20, 30))
        
        # Заголовок
        title = self.font_title.render("BATTLE CITY", True, (0, 255, 0))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title, title_rect)
        
        # Кнопка START
        button_color = (100, 200, 100) if self.start_hovered else (70, 150, 70)
        pygame.draw.rect(screen, button_color, self.start_button)
        pygame.draw.rect(screen, (255, 255, 255), self.start_button, 3)
        
        start_text = self.font_button.render("START GAME", True, (255, 255, 255))
        start_rect = start_text.get_rect(center=self.start_button.center)
        screen.blit(start_text, start_rect)
        
        # Інструкція
        instructions = self.font_small.render("Стрілки або WASD - рух | SPACE - стріляти | PAUSE - пауза", True, (200, 200, 200))
        screen.blit(instructions, (20, HEIGHT - 40))


class WinScene(Scene):
    """Екран перемоги"""
    def __init__(self, name="win"):
        super().__init__(name)
        self.font_title = pygame.font.Font(None, 72)
        self.font_button = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 48)
        
        # Кнопка CONTINUE
        self.continue_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 50, 240, 60)
        self.continue_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.continue_hovered:
                # Повернутись до меню
                from core.game import Game as GameClass
                if hasattr(GameClass, '_current_instance'):
                    GameClass._current_instance.scene_manager.set_scene("menu")

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.continue_hovered = self.continue_button.collidepoint(mouse_pos)

    def draw(self, screen):
        screen.fill((20, 30, 20))
        
        # Заголовок
        title = self.font_title.render("YOU WIN!", True, (0, 255, 0))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title, title_rect)
        
        # Повідомлення
        msg = self.font_medium.render("Всі хвилі переможені!", True, (200, 255, 100))
        msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        screen.blit(msg, msg_rect)
        
        # Кнопка CONTINUE
        button_color = (100, 200, 100) if self.continue_hovered else (70, 150, 70)
        pygame.draw.rect(screen, button_color, self.continue_button)
        pygame.draw.rect(screen, (255, 255, 255), self.continue_button, 3)
        
        continue_text = self.font_button.render("CONTINUE", True, (255, 255, 255))
        continue_rect = continue_text.get_rect(center=self.continue_button.center)
        screen.blit(continue_text, continue_rect)


class LoseScene(Scene):
    """Екран поразки"""
    def __init__(self, name="lose"):
        super().__init__(name)
        self.font_title = pygame.font.Font(None, 72)
        self.font_button = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 48)
        
        # Кнопка RETRY
        self.retry_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 30, 200, 60)
        self.retry_hovered = False
        
        # Кнопка MENU
        self.menu_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 110, 200, 60)
        self.menu_hovered = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            from core.game import Game as GameClass
            if hasattr(GameClass, '_current_instance'):
                if self.retry_hovered:
                    # Перезавантажити гру
                    GameClass._current_instance.scene_manager.set_scene("play")
                elif self.menu_hovered:
                    # До меню
                    GameClass._current_instance.scene_manager.set_scene("menu")

    def update(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        self.retry_hovered = self.retry_button.collidepoint(mouse_pos)
        self.menu_hovered = self.menu_button.collidepoint(mouse_pos)

    def draw(self, screen):
        screen.fill((30, 20, 20))
        
        # Заголовок
        title = self.font_title.render("GAME OVER", True, (255, 0, 0))
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title, title_rect)
        
        # Повідомлення
        msg = self.font_medium.render("Ви програли!", True, (255, 100, 100))
        msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 30))
        screen.blit(msg, msg_rect)
        
        # Кнопка RETRY
        retry_color = (150, 100, 100) if self.retry_hovered else (100, 70, 70)
        pygame.draw.rect(screen, retry_color, self.retry_button)
        pygame.draw.rect(screen, (255, 255, 255), self.retry_button, 3)
        
        retry_text = self.font_button.render("RETRY", True, (255, 255, 255))
        retry_rect = retry_text.get_rect(center=self.retry_button.center)
        screen.blit(retry_text, retry_rect)
        
        # Кнопка MENU
        menu_color = (100, 150, 200) if self.menu_hovered else (70, 120, 170)
        pygame.draw.rect(screen, menu_color, self.menu_button)
        pygame.draw.rect(screen, (255, 255, 255), self.menu_button, 3)
        
        menu_text = self.font_button.render("MENU", True, (255, 255, 255))
        menu_rect = menu_text.get_rect(center=self.menu_button.center)
        screen.blit(menu_text, menu_rect)


class Game:
    _current_instance = None  # Для доступу сцен до game instance
    
    def __init__(self, width=960, height=640, fps=60):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("BreakCityRemake-CoreEngine")
        self.clock = pygame.time.Clock()
        self.fps = fps

        Game._current_instance = self  # Зберігаємо посилання на поточний екземпляр
        
        self.scene_manager = SceneManager()
        self.scene_manager.register_scene(MenuScene())
        self.scene_manager.register_scene(PlayScene())
        self.scene_manager.register_scene(WinScene())
        self.scene_manager.register_scene(LoseScene())
        self.scene_manager.set_scene("menu")

    def run(self):
        while True:
            dt = self.clock.tick(self.fps) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                self.scene_manager.handle_event(event)

            self.scene_manager.update(dt)
            self.scene_manager.draw(self.screen)

            pygame.display.flip()


