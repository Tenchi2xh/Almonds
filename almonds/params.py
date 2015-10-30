# -*- encoding: utf-8 -*-

from __future__ import division

import os
import sys

from .utils import is_native_windows


class Params(object):
    """
    Class representing the current state of Almonds.
    """
    def __init__(self, log, char_ratio):
        """
        Initializes the parameters.

        :param log: Logger to use in the program.
        :type log: logger.Logger
        """
        self.log = log
        self.char_ratio = char_ratio

        # Mandelbrot parameters
        self.zoom = 1.0                         # Current zoom level factor
        self.max_iterations = 40                # Number of maximum iterations
        self.mb_cx = -0.5                       # Real position center
        self.mb_cy = 0.0                        # Imaginary position center

        # Appearance
        self.palette = 0                        # Color palette used
        self.dither_type = 2                    # Type of text characters used
        self.reverse_palette = False            # If true, palette is read backwards
        self.adaptive_palette = False           # Stretches the palette to what's currently visible
        self.progress = 0                       # Used for progress bars
        self.palette_offset = 0                 # Temporary offset for color cycling
        self.crosshairs = False
        self.crosshairs_coord = None
        if is_native_windows():
            self.dither_type = 0

        # Infinite plane that stores results
        self.plane_x0 = None                    # Plane coordinate of leftmost position on the displayed screen
        self.plane_y0 = None                    # Plane coordinate of rightmost position on the displayed screen
        self.plane_w = None                     # Width of the currently displayed screen
        self.plane_h = None                     # Height of the currently displayed screen
        self.plane_ratio = None                 # Ratio of the current screen, including the char ratio
        self.move_speed = 1                     # Number of skipped plane cells for arrow keys movement

        # Backups for when switching to julia
        self.julia = False
        self.julia_seed = None
        self.old_zoom = 1.0

    def toggle_julia(self):
        if self.julia:
            self.zoom = self.old_zoom
            self.mb_cx = self.julia_seed.real
            self.mb_cy = self.julia_seed.imag
            self.julia_seed = None
            self.julia = False
        else:
            self.old_zoom = self.zoom
            self.zoom = 1.0
            self.julia_seed = self.mb_cx + self.mb_cy * 1j
            self.mb_cx = 0.0
            self.mb_cy = 0.0
            self.julia = True

    def resize(self, w, h):
        """
        Used when resizing the plane, resets the plane ratio factor.

        :param w: New width of the visible section of the plane.
        :param h: New height of the visible section of the plane.
        """
        self.plane_w = w
        self.plane_h = h
        self.plane_ratio = self.char_ratio * w / h

        if self.crosshairs:
            self.crosshairs_coord = ((w + 2) // 2, (h + 2) // 2)
