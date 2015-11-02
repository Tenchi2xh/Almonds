# -*- encoding: utf-8 -*-

from ..mandelbrot import *


def test_inside():
    max_iterations = 100
    # (0, 0) and (-1, 0) should be in the set
    z0, it0 = mandelbrot_iterate( 0 + 0 * 1j, max_iterations)
    z1, it1 = mandelbrot_iterate(-1 + 0 * 1j, max_iterations)
    assert it0 == max_iterations
    assert it1 == max_iterations


def test_outside():
    max_iterations = 100
    # (0, 2) and (-2, 2) should be outside the set
    z0, it0 = mandelbrot_iterate( 0 + 2 * 1j, max_iterations)
    z1, it1 = mandelbrot_iterate(-2 + 2 * 1j, max_iterations)
    assert it0 < max_iterations
    assert it1 < max_iterations
