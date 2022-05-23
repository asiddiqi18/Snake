import icons
from snake import Snake
from tile import Tile


class Apple:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.apple_tile = None

    def create(self, snake: Snake, max_x: int, max_y: int):
        apple_tile = Tile.random(max_x, max_y)

        while True:
            for tile in snake.tiles:
                if tile == self.apple_tile:
                    apple_tile = Tile.random(max_x, max_y)
                    break
            break

        self.apple_tile = apple_tile

    def draw(self):
        self.stdscr.addch(self.apple_tile.y, self.apple_tile.x, icons.APPLE)
