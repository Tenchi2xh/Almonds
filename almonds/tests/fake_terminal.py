# -*- encoding: utf-8 -*-

from collections import namedtuple

import pytest

from ..utils import range


Cell = namedtuple('Cell', ['ch', 'fg', 'bg'])


class CurseBox(object):
    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.screen = []
        self.clear()

        self.cursor = (-1, -1)

    def hide_cursor(self):
        self.cursor = (-1, -1)

    def set_cursor(self, x, y):
        self.cursor = (x, y)

    def refresh(self):
        pass

    def put(self, x0, y0, text, fg, bg):
        for x in range(x0, x0 + len(text)):
            if 0 <= x < self.width and 0 <= y0 < self.height:
                self.screen[y0][x] = Cell(text[x - x0], fg, bg)

    def clear(self):
        for y in range(self.height):
            line = []
            for x in range(self.width):
                line.append(Cell(" ", 1, 0))
            self.screen.append(line)

    def get_screen(self):
        chars = ""
        colors = []
        for y in range(self.height):
            line_chars = ""
            line_colors = []
            for x in range(self.width):
                ch, fg, bg = self.screen[y][x]
                line_chars += ch
                line_colors.append((fg, bg))
            chars += line_chars + "\n"
            colors.append(line_colors)
        return chars, colors
