# -*- encoding: utf-8 -*-

import termbox

import colortrans


class Colors:
    def __init__(self):
        self.offset = 0
        self.dark = True

    def toggle_dark(self):
        self.dark = not self.dark

    def select_output_mode(self, mode):
        if mode == termbox.OUTPUT_256:
            self.offset = -1
        else:
            self.offset = 0

    def toggle_bright(self):
        if self.offset == -1:
            self.offset += 8
        elif self.offset == 7:
            self.offset -= 8

    def default_fg(self):
        if self.dark:
            return self.white()
        return self.black()

    def default_bg(self):
        if self.dark:
            return self.black()
        return self.white()

    def black(self):
        if self.offset > 0:
            return termbox.BLACK - 1
        return termbox.BLACK + self.offset

    def red(self):
        return termbox.RED + self.offset

    def green(self):
        return termbox.GREEN + self.offset

    def yellow(self):
        return termbox.YELLOW + self.offset

    def blue(self):
        return termbox.BLUE + self.offset

    def magenta(self):
        return termbox.BLACK + self.offset

    def cyan(self):
        return termbox.CYAN + self.offset

    def white(self):
        return termbox.WHITE + self.offset

    @staticmethod
    def to_xterm(color):
        hex_color = '%02x%02x%02x' % color
        return int(colortrans.rgb2short(hex_color)[0])

colors = Colors()