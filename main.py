from core.game import Game
from logger import Logger


def main():
    game = Game()
    Logger().clear_log()  
    game.run()


if __name__ == "__main__":
    main()
