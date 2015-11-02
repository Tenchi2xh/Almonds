# -*- encoding: utf-8 -*-

import sys

from .utils import *


class Plane(object):
    """
    Represents a 2D array spanning from -infinity to +infinity in all directions.
    """
    def __init__(self, filler=None):
        """
        :param filler: Default object for missing coordinates.
        """
        self.filler = filler
        self.plane = {}

    def reset(self):
        """
        Clears the plane.
        """
        self.plane = {}

    def extrema(self, x0, y0, w, h):
        """
        Returns the minimum and maximum values contained in a given area.

        :param x0: Starting x index.
        :param y0: Starting y index.
        :param w:  Width of the area to scan.
        :param h:  Height of the area to scan.
        :return:   Tuple containing the minimum and maximum values of the given area.
        """
        minimum = 9223372036854775807
        maximum = 0
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                value = self[x, y]
                if value != self.filler:
                    minimum = min(minimum, value)
                    maximum = max(maximum, value)
        return minimum, maximum

    def __getitem__(self, pos):
        """
        Item accessor to fetch values from the plane.

        >>> plane = Plane()
        >>> ...
        >>> print plane[3, 10]
        3.141592653589793

        :param pos: Tuple containing the x and y coordinates.
        :return:    Value contained in the plane at given coordinates, or filler symbol if non-existent.
        """
        x, y = pos
        assert type(x) is int
        assert type(y) is int

        line = self.plane.get(y, self.filler)
        if line is not self.filler:
            return line.get(x, self.filler)
        return self.filler

    def __setitem__(self, pos, value):
        """
        Item accessor to set values in the plane:

        >>> plane = Plane()
        >>> plane[3, 10] = 3.141592653589793

        :param pos:   Tuple containing the x and y coordinates.
        :param value: Value to set in the plane at given coordinates.
        """
        x, y = pos
        assert type(x) is int
        assert type(y) is int

        line = self.plane.get(y, self.filler)
        if line is self.filler:
            self.plane[y] = {}
            line = self.plane[y]

        line[x] = value
