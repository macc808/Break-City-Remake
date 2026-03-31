import pygame
import sys

from core.engine import Engine
from core.scene_manager import Scene, SceneManager
from map.level_loader import load_level_from_txt
from map.wall import floor_group, wall_group

LEVEL_PATH = "assets/levels/level_01.txt"


class PlayScene(Scene):
    def __init__(self, name="play"):
        super().__init__(name)
        self.engine = Engine()

    def start(self):
        load_level_from_txt(LEVEL_PATH)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    def update(self, dt):
        self.engine.update(dt)

        # collisions (tile vs tile) is not needed for static map currently
        # place holder for future collisions between player/bullets/enemies

    def draw(self, screen):
        screen.fill((30, 30, 30))
        floor_group.draw(screen)
        wall_group.draw(screen)


class Game:
    def __init__(self, width=960, height=640, fps=60):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("BreakCityRemake - Core Engine")
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


