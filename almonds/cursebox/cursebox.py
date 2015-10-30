# -*- encoding: utf-8 -*-

import curses
import os

from .constants import *
from .symbols import symbols
from .pairs import Pairs


class Cursebox(object):
    def __init__(self):
        self.pairs = Pairs()
        import locale
        locale.setlocale(locale.LC_ALL, "")

    def hide_cursor(self):
        curses.curs_set(0)

    def set_cursor(self, x, y):
        curses.curs_set(1)
        self.screen.move(y, x)

    def present(self):
        self.screen.refresh()

    def change_cell(self, x, y, ch, fg, bg):
        if x < self.width and y < self.height:
            try:
                self.screen.addstr(y, x, symbols.encode(ch), self.pairs[fg, bg])
            except curses.error:
                pass

    @property
    def width(self):
        return self.screen.getmaxyx()[1]

    @property
    def height(self):
        return self.screen.getmaxyx()[0]

    def clear(self):
        self.screen.clear()

    def poll_event(self):
        curses.flushinp()
        ch = self.screen.getch()

        if ch == 27:
            return EVENT_ESC
        elif ch == -1 or ch == curses.KEY_RESIZE:
            return EVENT_RESIZE
        elif ch == 10 or ch == curses.KEY_ENTER:
            return EVENT_ENTER
        elif ch == 127 or ch == curses.KEY_BACKSPACE:
            return EVENT_BACKSPACE
        elif ch == curses.KEY_UP:
            return EVENT_UP
        elif ch == curses.KEY_DOWN:
            return EVENT_DOWN
        elif ch == curses.KEY_LEFT:
            return EVENT_LEFT
        elif ch == curses.KEY_RIGHT:
            return EVENT_RIGHT
        elif ch == 3:
            return EVENT_CTRL_C
        else:
            # self.change_cell(0, 0, str(ch), 15, 0)
            return chr(ch)

    def __enter__(self):
        os.environ["ESCDELAY"] = "25"
        self.screen = curses.initscr()
        curses.noecho()
        curses.raw()
        self.screen.keypad(True)
        curses.start_color()
        curses.use_default_colors()
        self.hide_cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        curses.noraw()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
