# -*- encoding: utf-8 -*-

import collections
import curses

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


class CurseBox(object):
    def __init__(self):
        self.pairs = Pairs()

    def hide_cursor(self):
        curses.curs_set(0)

    def set_cursor(self, x, y):
        curses.curs_set(1)
        self.screen.move(x, y)

    def present(self):
        self.screen.refresh()

    def change_cell(self, x, y, ch, fg, bg):
        self.screen.addch(y, x, ch, self.pairs[fg, bg])

    def __init_colors(self):
        pass

    def __enter__(self):
        self.screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        curses.start_color()
        curses.use_default_colors()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
