import pygame
import sys
from map.level_loader import load_level_from_txt
from map.wall import floor_group, wall_group

LEVEL_PATH = "assets/levels/level_01.txt"


def main():
    pygame.init()
    screen = pygame.display.set_mode((960, 640))
    pygame.display.set_caption("BreakCityRemake - Level Loader")
    clock = pygame.time.Clock()

    try:
        load_level_from_txt(LEVEL_PATH)
    except FileNotFoundError as exc:
        print(exc)
        pygame.quit()
        sys.exit(1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30, 30, 30))

        floor_group.draw(screen)
        wall_group.draw(screen)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
