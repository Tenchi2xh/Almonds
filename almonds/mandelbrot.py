# -*- encoding: utf-8 -*-

from __future__ import division

import cmath
import sys

from .utils import *


def mandelbrot_iterate(c, max_iterations, julia_seed=None):
    """
    Returns the number of iterations before escaping the Mandelbrot fractal.

    :param c: Coordinates as a complex number
    :type c: complex
    :param max_iterations: Limit of how many tries are attempted.
    :return: Tuple containing the last complex number in the sequence and the number of iterations.
    """
    z = c
    if julia_seed is not None:
        c = julia_seed
    for iterations in range(max_iterations):
        z = z * z + c
        if abs(z) > 1000:
            return z, iterations
    return z, max_iterations


def get_coords(x, y, params):
    """
    Transforms the given coordinates from plane-space to Mandelbrot-space (real and imaginary).

    :param x: X coordinate on the plane.
    :param y: Y coordinate on the plane.
    :param params: Current application parameters.
    :type params: params.Params
    :return: Tuple containing the re-mapped coordinates in Mandelbrot-space.
    """
    n_x = x * 2.0 / params.plane_w * params.plane_ratio - 1.0
    n_y = y * 2.0 / params.plane_h - 1.0
    mb_x = params.zoom * n_x
    mb_y = params.zoom * n_y
    return mb_x, mb_y


def mandelbrot(x, y, params):
    """
    Computes the number of iterations of the given plane-space coordinates.

    :param x: X coordinate on the plane.
    :param y: Y coordinate on the plane.
    :param params: Current application parameters.
    :type params: params.Params
    :return: Discrete number of iterations.
    """
    mb_x, mb_y = get_coords(x, y, params)
    mb = mandelbrot_iterate(mb_x + 1j * mb_y, params.max_iterations, params.julia_seed)

    return mb[1]


def mandelbrot_capture(x, y, w, h, params):
    """
    Computes the number of iterations of the given pixel-space coordinates,
    for high-res capture purposes.

    Contrary to :func:`mandelbrot`, this function returns a continuous
    number of iterations to avoid banding.

    :param x: X coordinate on the picture
    :param y: Y coordinate on the picture
    :param w: Width of the picture
    :param h: Height of the picture
    :param params: Current application parameters.
    :type params: params.Params
    :return: Continuous number of iterations.
    """

    # FIXME: Figure out why these corrections are necessary or how to make them perfect
    # Viewport is offset compared to window when capturing without these (found empirically)
    if params.plane_ratio >= 1.0:
        x -= params.plane_w
    else:
        x += 3.0 * params.plane_w

    ratio = w / h
    n_x = x * 2.0 / w * ratio - 1.0
    n_y = y * 2.0 / h - 1.0
    mb_x = params.zoom * n_x + params.mb_cx
    mb_y = params.zoom * n_y + params.mb_cy

    mb = mandelbrot_iterate(mb_x + 1j * mb_y, params.max_iterations, params.julia_seed)
    z, iterations = mb

    # Continuous iteration count for no banding
    # https://en.wikipedia.org/wiki/Mandelbrot_set#Continuous_.28smooth.29_coloring
    nu = params.max_iterations
    if iterations < params.max_iterations:
        nu = iterations + 2 - abs(cmath.log(cmath.log(abs(z)) / cmath.log(params.max_iterations), 2))

    return clamp(nu, 0, params.max_iterations)


def update_position(params):
    """
    Computes the center of the viewport's Mandelbrot-space coordinates.

    :param params: Current application parameters.
    :type params: params.Params
    """
    cx = params.plane_x0 + params.plane_w / 2.0
    cy = params.plane_y0 + params.plane_h / 2.0
    params.mb_cx, params.mb_cy = get_coords(cx, cy, params)


def zoom(params, factor):
    """
    Applies a zoom on the current parameters.

    Computes the top-left plane-space coordinates from the Mandelbrot-space coordinates.

    :param params: Current application parameters.
    :param factor: Zoom factor by which the zoom ratio is divided (bigger factor, more zoom)
    """
    params.zoom /= factor

    n_x = params.mb_cx / params.zoom
    n_y = params.mb_cy / params.zoom

    params.plane_x0 = int((n_x + 1.0) * params.plane_w / (2.0 * params.plane_ratio)) - params.plane_w // 2
    params.plane_y0 = int((n_y + 1.0) * params.plane_h / 2.0) - params.plane_h // 2
