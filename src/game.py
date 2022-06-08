import curses

from apple import Apple
from snake import Snake


class Game:

    def __init__(self, stdscr, config):
        self.stdscr = stdscr
        self.config = config

        self.setup_curses()

        # get the maximum sizes of the terminals, place initial position at center
        self.max_y, self.max_x = self.stdscr.getmaxyx()
        self.x_pos = self.max_x // 2
        self.y_pos = self.max_y // 2

        # set initial velocity to negative X direction, no velocity for Y
        self.x_vel = -config.horizontal_step
        self.y_vel = 0

        # subtract from maximums by 2 since pixels near edges behave oddly with curses
        self.max_x -= 2
        self.max_y -= 2

        # if horizontal steps are even and initial x position is odd,
        # change position to even for alignment
        if (not config.horizontal_step & 1) and self.x_pos & 1:
            self.x_pos += 1

        self.score = 0

        # create first snake tilt at initial location
        self.snake_entity = Snake(self.stdscr)
        self.snake_entity.add_tile(self.x_pos, self.y_pos)

        # create first apple and generate location within (x, y) bounds
        self.apple_entity = Apple(self.stdscr)
        self.apple_entity.create(self.snake_entity, self.max_x, self.max_y)

        # will be subtracted by 1 each frame
        self.bonuses_added_length = config.initial_bonus_length

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

            self.snake_entity.add_tile(self.x_pos, self.y_pos)

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
            self.y_vel = -self.config.vertical_step
            self.x_vel = 0
        elif key == curses.KEY_DOWN:
            if self.y_vel < 0:
                return
            self.y_vel = self.config.vertical_step
            self.x_vel = 0
        elif key == curses.KEY_LEFT:
            if self.x_vel > 0:
                return
            self.y_vel = 0
            self.x_vel = -self.config.horizontal_step
        elif key == curses.KEY_RIGHT:
            if self.x_vel < 0:
                return
            self.y_vel = 0
            self.x_vel = self.config.horizontal_step

    def draw_screen(self):
        self.stdscr.clear()

        self.apple_entity.draw()
        self.snake_entity.draw()

        self.stdscr.addstr(self.max_y + 1, 0, f"Score: {self.score}")
