# -*- encoding: utf-8 -*-

from plane import Plane


CHAR_RATIO = 0.428


class Params:
    def __init__(self, log):
        self.log = log

        # Mandelbrot parameters
        self.zoom = 1.0                         # Current zoom level factor
        self.max_iterations = 40                # Number of maximum iterations
        self.mb_cx = -0.5                       # Real position center
        self.mb_cy = 0.0                        # Imaginary position center
        # Appearance
        self.palette = 0                        # Color palette used
        self.dither_type = 0                    # Type of text characters used
        self.reverse_palette = False            # If true, palette is read backwards
        self.adaptive_palette = False           # TODO: palette min and max stretch to local slice's min and max
        self.progress = 0
        self.palette_offset = 0
        # Infinite plane that stores results
        self.plane_x0 = None                    # Plane coordinate of leftmost position on the displayed screen
        self.plane_y0 = None                    # Plane coordinate of rightmost position on the displayed screen
        self.plane_w = None                     # Width of the currently displayed screen
        self.plane_h = None                     # Height of the currently displayed screen
        self.plane_ratio = None                 # Ratio of the current screen, including the char ratio
        self.move_speed = 1                     # Number of skipped plane cells for arrow keys movement

    def resize(self, w, h):
        self.plane_w = w
        self.plane_h = h
        self.plane_ratio = CHAR_RATIO * w / h

    def reload(self, log):
        self.log = log

