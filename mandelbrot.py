# -*- encoding: utf-8 -*-

import cmath
import threading

from graphics import draw_progress_bar
from utils import clamp


class MBWorker(threading.Thread):
    def __init__(self, coords, params, capture_resolution=None, t=None, lock=None):
        self.coords = coords
        self.params = params
        self.results = []
        self.capture_resolution = capture_resolution
        self.t = t
        self.lock = lock
        if self.capture_resolution is not None:
            self.total = capture_resolution[0] * capture_resolution[1]
        threading.Thread.__init__(self)

    def update_progress(self, i):
        with self.lock:
            self.params.progress += i
            draw_progress_bar(self.t, "Capturing current scene...", self.params.progress, self.total)
            self.t.present()

    def run(self):
        if self.capture_resolution is not None:
            w, h = self.capture_resolution
            i = 0
            for c in self.coords:
                self.results.append(mandelbrot_capture(c[0], c[1], w, h, self.params))
                i += 1
                if i > 1000:
                    self.update_progress(i)
                    i = 0
            self.update_progress(i)

        else:
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
    mb_x = params.zoom * n_x
    mb_y = params.zoom * n_y
    return mb_x, mb_y


def mandelbrot(x, y, params):
    """
    :type params: Params
    """
    mb_x, mb_y = get_coords(x, y, params)
    mb = mandelbrot_iterate(0, mb_x + 1j * mb_y, params.max_iterations)

    z, iterations = mb

    return iterations


def mandelbrot_capture(x, y, w, h, params):

    # FIXME: Figure out why these corrections are necessary
    if params.plane_ratio >= 1.0:
        x -= params.plane_w
    else:
        x += 3.0 * params.plane_w

    ratio = float(w) / h
    n_x = x * 2.0 / w * ratio - 1.0
    n_y = y * 2.0 / h - 1.0
    mb_x = params.zoom * n_x + params.mb_cx
    mb_y = params.zoom * n_y + params.mb_cy

    mb = mandelbrot_iterate(0, mb_x + 1j * mb_y, params.max_iterations)
    z, iterations = mb

    # Continuous iteration count for no banding
    nu = params.max_iterations
    if iterations < params.max_iterations:
        nu = iterations + 2 - abs(cmath.log(cmath.log(abs(z)) / cmath.log(params.max_iterations), 2))

    return clamp(nu, 0, params.max_iterations)


def update_position(params):
    """
    :type params: Params
    """
    cx = params.plane_x0 + params.plane_w / 2.0
    cy = params.plane_y0 + params.plane_h / 2.0
    params.mb_cx, params.mb_cy = get_coords(cx, cy, params)


def zoom(params, factor):

    params.zoom /= factor

    n_x = params.mb_cx / params.zoom
    n_y = params.mb_cy / params.zoom

    params.plane_x0 = int((n_x + 1.0) * params.plane_w / (2.0 * params.plane_ratio)) - params.plane_w / 2
    params.plane_y0 = int((n_y + 1.0) * params.plane_h / 2.0) - params.plane_h / 2

    params.plane.reset()
