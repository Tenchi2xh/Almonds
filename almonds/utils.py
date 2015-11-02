# -*- encoding: utf-8 -*-

import sys
import os
import subprocess


def clamp(n, lower, upper):
    """
    Restricts the given number to a lower and upper bound (inclusive)

    :param n:     input number
    :param lower: lower bound (inclusive)
    :param upper: upper bound (inclusive)
    :return:      clamped number
    """
    if lower > upper:
        lower, upper = upper, lower
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


def is_native_windows():
    return os.name == "nt" and sys.platform != "cygwin"


def is_python3():
    return sys.version_info[0] > 2


def range(*args, **kwargs):
    if is_python3():
        import builtins
        return builtins.range(*args, **kwargs)
    else:
        return xrange(*args, **kwargs)
