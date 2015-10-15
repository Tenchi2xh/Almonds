# -*- encoding: utf-8 -*-

from types import IntType

PLANE_STEP = 100


class Plane:
    """
    Represents a 2D array spanning from -infinity to +infinity in all directions
    """
    def __init__(self, log, filler=None):
        #  3 | 0
        # ---+---
        #  2 | 1
        self.log = log
        self.filler = filler
        self.quadrants = []
        self.resetted = False
        for i in xrange(4):
            self.quadrants.append([])
            for j in xrange(PLANE_STEP):
                self.quadrants[i].append([filler] * PLANE_STEP)

    def __init_quadrants(self):
        self.quadrants = []
        for i in xrange(4):
            self.quadrants.append([])
            for j in xrange(PLANE_STEP):
                self.quadrants[i].append([self.filler] * PLANE_STEP)

    def reset(self):
        self.log("Resetting plane")
        self.__init_quadrants()
        self.resetted = True

    def slice(self, x0, y0, x1, y1):
        pass

    def __grow(self, quadrant, pos):
        x, y = pos
        if x >= len(self.quadrants[quadrant][0]):
            # Extend all the lines
            amount = 1 + (x - len(self.quadrants[quadrant][0])) / PLANE_STEP
            for i in xrange(len(self.quadrants[quadrant])):
                self.quadrants[quadrant][i].extend([self.filler] * (amount * PLANE_STEP))
        if y >= len(self.quadrants[quadrant]):
            # Add more lines
            amount = 1 + (y - len(self.quadrants[quadrant])) / PLANE_STEP
            for i in xrange(amount * PLANE_STEP):
                new_line = [self.filler] * len(self.quadrants[quadrant][0])
                self.quadrants[quadrant].append(new_line)

    def __get(self, quadrant, pos):
        x, y = pos
        self.__grow(quadrant, pos)
        return self.quadrants[quadrant][y][x]

    def __set(self, quadrant, pos, value):
        x, y = pos
        self.__grow(quadrant, pos)
        self.quadrants[quadrant][y][x] = value

    def __getitem__(self, pos):
        x, y = pos
        assert type(x) is IntType
        assert type(y) is IntType
        if x >= 0 and y >= 0:
            return self.__get(0, (x, y))
        elif x >= 0 and y < 0:
            return self.__get(1, (x, abs(y) - 1))
        elif x < 0 and y < 0:
            return self.__get(2, (abs(x) - 1, abs(y) - 1))
        elif x < 0 and y >= 0:
            return self.__get(3, (abs(x) - 1, y))
        else:
            raise IndexError

    def __setitem__(self, pos, value):
        x, y = pos
        assert type(x) is IntType
        assert type(y) is IntType
        if x >= 0 and y >= 0:
            return self.__set(0, (x, y), value)
        elif x >= 0 and y < 0:
            return self.__set(1, (x, abs(y) - 1), value)
        elif x < 0 and y < 0:
            return self.__set(2, (abs(x) - 1, abs(y) - 1), value)
        elif x < 0 and y >= 0:
            return self.__set(3, (abs(x) - 1, y), value)
        else:
            raise IndexError
