import os
import sys
import pygame
from pygame.locals import K_UP, K_DOWN, K_LEFT, K_RIGHT, K_w, K_s, K_a, K_d
from entities.player import Player
from entities.enemy import Enemy
from entities.bullet import Bullet
from config import img_player, WIDTH, HEIGHT
from core.engine import Engine
from core.scene_manager import Scene, SceneManager
from map.level_loader import load_level_from_txt
from map.wall import floor_group, wall_group
from logger import Logger

# Якщо запускаєте цей файл напряму (не через main.py), то підключимо корінь проекту
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

LEVEL_PATH = "assets/levels/level_01.txt"


class PlayScene(Scene):
    def __init__(self, name="play"):
        super().__init__(name)
        self.engine = Engine()
        self.player = Player(img_player, WIDTH - 70, HEIGHT - 50, 50, 40, 5, {
            "up1": K_UP, "down1": K_DOWN, "left1": K_LEFT, "right1": K_RIGHT,
            "up2": K_w, "down2": K_s, "left2": K_a, "right2": K_d,
        })
        self.enemy = Enemy(img_player, 80, 80, 50, 40, 2, "random")
        self.player_bullets = []
        self.enemy_bullets = []

    def start(self):
        load_level_from_txt(LEVEL_PATH)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    def update(self, dt):
        self.engine.update(dt)
        self.player.update(dt)
        self.enemy.update(dt)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bullet = self.player.shoot()
            if bullet:
                self.player_bullets.append(bullet)

        enemy_shot = self.enemy.shoot(dt)
        if enemy_shot:
            self.enemy_bullets.append(enemy_shot)

        for bullet in self.player_bullets[:]:
            remove = bullet.update()
            if remove:
                self.player_bullets.remove(bullet)
                continue
            if bullet.rect.colliderect(self.enemy.rect):
                Logger().log_message(self.update, "Enemy hit by player bullet")
                self.player_bullets.remove(bullet)

        for bullet in self.enemy_bullets[:]:
            remove = bullet.update()
            if remove:
                self.enemy_bullets.remove(bullet)
                continue
            if bullet.rect.colliderect(self.player.rect):
                Logger().log_message(self.update, "Player hit by enemy bullet")
                self.enemy_bullets.remove(bullet)

    def draw(self, screen):
        screen.fill((30, 30, 30))
        floor_group.draw(screen)
        wall_group.draw(screen)
        self.player.reset(screen)
        self.enemy.reset(screen)

        for bullet in self.player_bullets + self.enemy_bullets:
            bullet.reset(screen)


class Game:
    def __init__(self, width=960, height=640, fps=60):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("BreakCityRemake-CoreEngine")
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.scene_manager = SceneManager()
        self.scene_manager.register_scene(PlayScene())
        self.scene_manager.set_scene("play")

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


