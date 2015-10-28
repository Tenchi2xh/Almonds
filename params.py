# -*- encoding: utf-8 -*-

from __future__ import division

# Unlike pixels, terminal characters do not have a 1:1 ratio
CHAR_RATIO = 0.428


class Params(object):
    """
    Class representing the current state of Almonds.
    """
    def __init__(self, log):
        """
        Initializes the parameters.

        :param log: Logger to use in the program.
        :type log: logger.Logger
        """
        self.log = log

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

        # Infinite plane that stores results
        self.plane_x0 = None                    # Plane coordinate of leftmost position on the displayed screen
        self.plane_y0 = None                    # Plane coordinate of rightmost position on the displayed screen
        self.plane_w = None                     # Width of the currently displayed screen
        self.plane_h = None                     # Height of the currently displayed screen
        self.plane_ratio = None                 # Ratio of the current screen, including the char ratio
        self.move_speed = 1                     # Number of skipped plane cells for arrow keys movement

    def resize(self, w, h):
        """
        Used when resizing the plane, resets the plane ratio factor.

        :param w: New width of the visible section of the plane.
        :param h: New height of the visible section of the plane.
        """
        self.plane_w = w
        self.plane_h = h
        self.plane_ratio = CHAR_RATIO * w / h
