from tile import Tile


class Snake:

    def __init__(self, stdscr) -> None:
        self.stdscr = stdscr
        self.tiles = []
        self._hit = False

    def get_head_tile(self) -> Tile:
        return self.tiles[-1]

    def draw(self):
        head = self.get_head_tile()

        for index, tile in enumerate(self.tiles):

            if index != len(self.tiles) - 1 and head == tile:
                self._hit = True
                return

            tile.draw(self.stdscr)

        self._hit = False

    def append(self, x_pos: int, y_pos: int):
        self.tiles.append(Tile(x_pos, y_pos))

    def was_hit_by_itself(self) -> bool:
        return self._hit

    def was_hit_by_apple(self, apple) -> bool:
        return apple.apple_tile == self.get_head_tile()

    def slide(self):
        self.tiles = self.tiles[1:]
