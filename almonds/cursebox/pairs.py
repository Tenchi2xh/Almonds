# -*- encoding: utf-8 -*-

import collections
import curses

from .constants import *


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
