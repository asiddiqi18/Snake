import curses

from config import Config
from game import Game


def main(stdscr):
    config = Config(1, 2, 5)
    game = Game(stdscr, config)
    game.run()


if __name__ == '__main__':
    curses.wrapper(main)
