# -*- encoding: utf-8 -*-

from .colortrans import rgb2short


class Colors(object):
    def __init__(self):
        self.dark = True
        self.bright = True

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
        return 1 + self.offset

    def green(self):
        return 2 + self.offset

    def yellow(self):
        return 3 + self.offset

    def blue(self):
        return 4 + self.offset

    def magenta(self):
        return 5 + self.offset

    def cyan(self):
        return 6 + self.offset

    def white(self):
        return 7 + self.offset

    @staticmethod
    def to_xterm(color):
        hex_color = '%02x%02x%02x' % color
        return int(rgb2short(hex_color)[0])

colors = Colors()
