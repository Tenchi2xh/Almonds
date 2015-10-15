# -*- encoding: utf-8 -*-

from plane import Plane


class Params:
    def __init__(self, zoom, max_iterations, log):
        self.log = log
        self.zoom = zoom
        self.max_iterations = max_iterations
        self.palette = 0
        self.dither_type = 0
        self.reverse_palette = False
        self.adaptive_palette = False
        self.mb_cx = -0.5
        self.mb_cy = 0.1
        self.plane = Plane(log)
        self.plane_cx = 0
        self.plane_cy = 0
        self.plane_w = 10
        self.plane_h = 10
        self.plane_ratio = 1.0
        self.char_ratio = 0.43
        self.move_speed = 1

    def resize(self, w, h):
        self.plane_w = w
        self.plane_h = h
        self.plane_ratio = self.char_ratio * w / h

    def __getstate__(self):
        return dict((k, v) for (k, v) in self.__dict__.iteritems() if k != "plane")

    def __setstate__(self, state):
        self.__dict__ = state

    def reload(self, log):
        self.log = log
        self.plane = Plane(log)

