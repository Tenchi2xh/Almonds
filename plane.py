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

    def extrema(self, x0, y0, w, h, maximum_iterations):
        minimum = maximum_iterations
        maximum = 0
        for y in xrange(y0, y0 + h):
            for x in xrange(x0, x0 + w):
                value = self[x, y]
                if value != self.filler:
                    minimum = min(minimum, value)
                    maximum = max(maximum, value)
        return minimum, maximum

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
