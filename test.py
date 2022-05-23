import curses
from curses import wrapper
from time import sleep


def main(stdscr):
    curses.noecho()
    curses.cbreak()
    curses.start_color()
    stdscr.keypad(True)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    stdscr.addstr(10, 10, "This text should be red", curses.color_pair(1))
    stdscr.refresh()
    sleep(2)
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()


wrapper(main)
