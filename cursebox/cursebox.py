# -*- encoding: utf-8 -*-

import collections
import curses
import os

MAX_PAIRS = 32767


class Pairs(object):
    def __init__(self):
        self.counter = 1
        self.pair_numbers = collections.OrderedDict({})

    def __getitem__(self, pair):
        fg, bg = pair
        assert type(fg) is int and -1 <= fg < 256
        assert type(bg) is int and -1 <= bg < 256

        if pair in self.pair_numbers:
            return curses.color_pair(self.pair_numbers[pair])
        elif self.counter < MAX_PAIRS:
            curses.init_pair(self.counter, fg, bg)
            self.pair_numbers[pair] = self.counter
            self.counter += 1
            return curses.color_pair(self.counter - 1)
        else:
            _, oldest = self.pair_numbers.popitem(last=False)
            curses.init_pair(oldest, fg, bg)
            self.pair_numbers[pair] = oldest
            return curses.color_pair(oldest)


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
                self.screen.addstr(y, x, ch.encode("utf-8"), self.pairs[fg, bg])
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
        ch = self.screen.getch()

        if ch == 27:
            return "ESC"
        elif ch == -1 or ch == curses.KEY_RESIZE:
            return "RESIZE"
        elif ch == 10 or ch == curses.KEY_ENTER:
            return "ENTER"
        elif ch == 127 or ch == curses.KEY_BACKSPACE:
            return "BACKSPACE"
        elif ch == curses.KEY_UP:
            return "UP"
        elif ch == curses.KEY_DOWN:
            return "DOWN"
        elif ch == curses.KEY_LEFT:
            return "LEFT"
        elif ch == curses.KEY_RIGHT:
            return "RIGHT"
        elif ch == 3:
            return "CTRL+C"
        else:
            # self.change_cell(0, 0, str(ch), 15, 0)
            return chr(ch)

    def __enter__(self):
        os.environ['ESCDELAY'] = '25'
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
