# -*- encoding: utf-8 -*-

from types import IntType


class Plane:
    """
    Represents a 2D array spanning from -infinity to +infinity in all directions
    """
    def __init__(self, filler=None):

        self.filler = filler
        self.plane = {}

    def reset(self):
        self.plane = {}

    def slice(self, x0, y0, x1, y1):
        pass

    def __getitem__(self, pos):
        x, y = pos
        assert type(x) is IntType
        assert type(y) is IntType

        line = self.plane.get(y, self.filler)
        if line is not self.filler:
            return line.get(x, self.filler)
        return self.filler

    def __setitem__(self, pos, value):
        x, y = pos
        assert type(x) is IntType
        assert type(y) is IntType

        line = self.plane.get(y, self.filler)
        if line is self.filler:
            self.plane[y] = {}
            line = self.plane[y]

        line[x] = value
