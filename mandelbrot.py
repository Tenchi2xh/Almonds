# -*- encoding: utf-8 -*-

import cmath
import threading

from graphics import *
from plane import Plane
from utils import clamp


MB_CENTER_X = -0.5
MB_CENTER_Y = 0.0


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


class MBWorker(threading.Thread):
    def __init__(self, coords, params):
        self.coords = coords
        self.params = params
        self.results = []
        threading.Thread.__init__(self)

    def run(self):
        for c in self.coords:
            self.results.append(mandelbrot(c[0], c[1], self.params))


def mandelbrot_iterate(z, c, max_iterations, iteration=0):
    if abs(z) > 1000:
        return z, iteration
    elif iteration < max_iterations:
        return mandelbrot_iterate(z * z + c, c, max_iterations, iteration + 1)
    else:
        return z * z + c, iteration


def get_coords(x, y, params):
    n_x = x * 2.0 / params.plane_w * params.plane_ratio - 1.0
    n_y = y * 2.0 / params.plane_h - 1.0
    mb_x = params.zoom * n_x + MB_CENTER_X
    mb_y = params.zoom * n_y + MB_CENTER_Y
    return mb_x, mb_y


def mandelbrot(x, y, params):
    """
    :type params: Params
    """
    mb_x, mb_y = get_coords(x, y, params)
    mb = mandelbrot_iterate(0, mb_x + 1j * mb_y, params.max_iterations)

    z, iterations = mb
    # Continuous iteration count
    nu = params.max_iterations
    if iterations < params.max_iterations:
        nu = iterations + 2 - abs(cmath.log(cmath.log(abs(z)) / cmath.log(params.max_iterations), 2))

    return clamp(nu, 0, params.max_iterations)


def update_position(params):
    """
    :type params: Params
    """
    cx = params.plane_cx + params.plane_w / 2
    cy = params.plane_cy + params.plane_h / 2
    params.mb_cx, params.mb_cy = get_coords(cx, cy, params)


def zoom(params, factor):

    params.zoom /= factor

    n_x = (params.mb_cx - MB_CENTER_X) / params.zoom
    n_y = (params.mb_cy - MB_CENTER_Y) / params.zoom

    params.plane_cx = int((n_x + 1.0) * params.plane_w / (2.0 * params.plane_ratio)) - params.plane_w / 2
    params.plane_cy = int((n_y + 1.0) * params.plane_h / 2.0) - params.plane_h / 2

    params.plane.reset()
