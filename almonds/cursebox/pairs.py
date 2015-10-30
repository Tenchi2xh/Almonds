# -*- encoding: utf-8 -*-

import collections
import curses

from .constants import *


class Pairs(object):
    """
    Collection object that stores curses color pairs.

    When a color pair is needed, it can be retrieved by calling __getitem__:

    >>> pairs = Pairs()
    >>> a_pair = pairs[0, 3]

    If the pair does not exist, it is created and pushed in a FIFO dictionary
    of limited size (32767 entries). A very big terminal will never have more
    than 10000 characters displayed, so this enables to use virtually all color
    combinations at all times.
    """
    def __init__(self):
        self.counter = 1
        self.pair_numbers = collections.OrderedDict({})

    def __getitem__(self, pair):
        fg, bg = pair
        assert type(fg) is int and -1 <= fg < 256
        assert type(bg) is int and -1 <= bg < 256

        if pair in self.pair_numbers:
            # If pair is stored, retrieve it.
            return curses.color_pair(self.pair_numbers[pair])
        elif self.counter < MAX_PAIRS:
            # If we still haven't filled our queue, add the new pair.
            curses.init_pair(self.counter, fg, bg)
            self.pair_numbers[pair] = self.counter
            self.counter += 1
            return curses.color_pair(self.counter - 1)
        else:
            # If the queue is full, pop the oldest one out
            # and use its pair number to create the new one.
            _, oldest = self.pair_numbers.popitem(last=False)
            curses.init_pair(oldest, fg, bg)
            self.pair_numbers[pair] = oldest
            return curses.color_pair(oldest)
