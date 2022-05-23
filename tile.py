import random

import icons


class Tile:

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Tile):
            return NotImplemented
        return self.x == o.x and self.y == o.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"

    def draw(self, stdscr):
        stdscr.move(self.y, self.x)
        stdscr.addstr(icons.SQUARE)

    @staticmethod
    def random(max_x, max_y):
        rand_x = random.randint(0, max_x)
        rand_y = random.randint(0, max_y)

        if rand_x & 1:
            rand_x += 1

        return Tile(rand_x, rand_y)
