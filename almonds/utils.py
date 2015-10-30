# -*- encoding: utf-8 -*-

import sys
import os
import subprocess

from .cursebox import symbols

b = lambda n: tuple([symbols.dither1[0] * 2] * n)
splash = ["                                                                             ",
          "                %s                                                           " % b(1),
          "          %s  %s%s%s  %s   .d8b.  db                              db         " % b(5),
          "            %s%s%s%s%s    d8' `8b 88 .88b  d88. .d88b. .888b  .d8888 .d8888  " % b(5),
          "      %s  %s%s%s%s%s%s%s  88ooo88 88 88  88  88 8P  Y8 88  88 88  88 `8bo.   " % b(8),
          "  %s%s%s%s%s%s%s%s%s%s    88   88 88 88  88  88 8b  d8 88  88 88  8D   `Y8b  " % b(10),
          "      %s  %s%s%s%s%s%s%s  YP   YP YP YP  YP  YP `Y88P' VP  VP Y888D' `8888Y  " % b(8),
          "            %s%s%s%s%s                                                       " % b(5),
          "          %s  %s%s%s  %s    T e r m i n a l   f r a c t a l   v i e w e r    " % b(5),
          "                %s                                                           " % b(1),
          "                                                                             "]


def clamp(n, lower, upper):
    """
    Restricts the given number to a lower and upper bound (inclusive)

    :param n:     input number
    :param lower: lower bound (inclusive)
    :param upper: upper bound (inclusive)
    :return:      clamped number
    """
    return max(min(upper, n), lower)


def screen_resolution():
    """
    Returns the current screen's resolution.

    Should be multi-platform.

    :return: A tuple containing the width and height of the screen.
    """
    w = 0
    h = 0
    try:
        # Windows
        import ctypes
        user32 = ctypes.windll.user32
        w, h = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    except AttributeError:
        try:
            # Mac OS X
            import AppKit
            size = AppKit.NSScreen.screens()[0].frame().size
            w, h = int(size.width), int(size.height)
        except ImportError:
            try:
                # Linux
                import Xlib
                import Xlib.display
                display = Xlib.display.Display()
                root = display.screen().root
                size = root.get_geometry()
                w, h = size.width, size.height
            except ImportError:
                w = 1920
                h = 1080

    return w, h


def open_file(filename):
    """
    Multi-platform way to make the OS open a file with its default application
    """
    if sys.platform.startswith("darwin"):
        subprocess.call(("open", filename))
    elif sys.platform == "cygwin":
        subprocess.call(("cygstart", filename))
    elif os.name == "nt":
        os.system("start %s" % filename)
    elif os.name == "posix":
        subprocess.call(("xdg-open", filename))
