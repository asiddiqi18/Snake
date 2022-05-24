import curses

from apple import Apple
from snake import Snake

VERTICAL_LEAP = 1
HORIZONTAL_LEAP = 2
INIT_BONUS_LENGTH = 0


class Game:

    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.setup_curses()
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        self.x_pos = self.max_x // 2
        self.x_vel = -HORIZONTAL_LEAP
        self.y_pos = self.max_y // 2

        self.max_x -= 2
        self.max_y -= 2

        self.y_vel = 0
        self.score = 0

        self.snake_entity = Snake(self.stdscr)
        self.snake_entity.append(self.x_pos, self.y_pos)

        self.apple_entity = Apple(self.stdscr)
        self.apple_entity.create(self.snake_entity, self.max_x, self.max_y)

        self.bonuses_added_length = INIT_BONUS_LENGTH

    def setup_curses(self):
        curses.curs_set(0)
        curses.noecho()

        curses.start_color()
        curses.use_default_colors()

        self.stdscr.leaveok(False)
        self.stdscr.nodelay(1)
        self.stdscr.keypad(True)

    def run(self):

        while True:

            key = self.stdscr.getch()

            if key == ord('q'):
                break
            elif key == ord('p'):
                self.stdscr.timeout(-1)
                self.write_center("Game Paused. Enter anything to resume.\n")
                self.stdscr.getch()

            self.find_velocity(key)

            self.slide_snake()

            if self.snake_entity.was_hit_by_apple(self.apple_entity):
                self.apple_entity.create(self.snake_entity, self.max_x, self.max_y)
                self.score += 1
            elif self.bonuses_added_length:
                self.bonuses_added_length -= 1
                self.score += 1
            else:
                self.snake_entity.slide()

            self.snake_entity.append(self.x_pos, self.y_pos)

            self.draw_screen()

            if self.snake_entity.was_hit_by_itself():
                break

            self.stdscr.timeout(65)

        self.write_center("Game Over\n")

        curses.napms(1000)
        curses.endwin()

    def write_center(self, text):
        self.stdscr.addstr(
            self.max_y // 2,
            self.max_x // 2 - len(text) // 2,
            text
        )
        self.stdscr.refresh()

    def slide_snake(self):
        if self.x_pos <= 1 and self.x_vel < 0:  # Left
            self.x_pos = self.max_x

        elif self.x_pos >= self.max_x and self.x_vel > 0:  # Right
            self.x_pos = 0

        elif self.y_pos <= 0 and self.y_vel == -1:  # Top
            self.y_pos = self.max_y

        elif self.y_pos >= self.max_y and self.y_vel == 1:  # Bottom
            self.y_pos = 0
        else:
            self.x_pos += self.x_vel
            self.y_pos += self.y_vel

    def find_velocity(self, key):
        if key == curses.KEY_UP:
            if self.y_vel > 0:
                return
            self.y_vel = -VERTICAL_LEAP
            self.x_vel = 0
        elif key == curses.KEY_DOWN:
            if self.y_vel < 0:
                return
            self.y_vel = VERTICAL_LEAP
            self.x_vel = 0
        elif key == curses.KEY_LEFT:
            if self.x_vel > 0:
                return
            self.y_vel = 0
            self.x_vel = -HORIZONTAL_LEAP
        elif key == curses.KEY_RIGHT:
            if self.x_vel < 0:
                return
            self.y_vel = 0
            self.x_vel = HORIZONTAL_LEAP

    def draw_screen(self):
        self.stdscr.clear()

        self.apple_entity.draw()
        self.snake_entity.draw()

        self.stdscr.addstr(self.max_y + 1, 0, f"Score: {self.score}")
