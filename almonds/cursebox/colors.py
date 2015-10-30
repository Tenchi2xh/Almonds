# -*- encoding: utf-8 -*-

import os
import sys

from .colortrans import rgb2short
from ..utils import is_native_windows

UNIX_COLORS = {
    "black": 0,
    "red": 1,
    "green": 2,
    "yellow": 3,
    "blue": 4,
    "magenta": 5,
    "cyan": 6,
    "white": 7
}

WIN_COLORS = {
    "black": 0,
    "blue": 1,
    "green": 2,
    "cyan": 3,
    "red": 4,
    "magenta": 5,
    "yellow": 6,
    "white": 7
}


class Colors(object):
    def __init__(self):
        self.dark = True
        self.bright = True
        if is_native_windows():
            self.codes = WIN_COLORS
        else:
            self.codes = UNIX_COLORS

    def toggle_dark(self):
        self.dark = not self.dark

    def toggle_bright(self):
        self.bright = not self.bright

    def default_fg(self):
        if self.dark:
            return self.white()
        return 0

    def default_bg(self):
        if self.dark:
            return 0
        return self.white()

    @property
    def offset(self):
        return 8 if self.bright else 0

    def black(self):
        return 0

    def red(self):
        return self.codes["red"] + self.offset

    def green(self):
        return self.codes["green"] + self.offset

    def yellow(self):
        return self.codes["yellow"] + self.offset

    def blue(self):
        return self.codes["blue"] + self.offset

    def magenta(self):
        return self.codes["magenta"] + self.offset

    def cyan(self):
        return self.codes["cyan"] + self.offset

    def white(self):
        return self.codes["white"] + self.offset

    @staticmethod
    def to_xterm(color):
        hex_color = '%02x%02x%02x' % color
        return int(rgb2short(hex_color)[0])

colors = Colors()
