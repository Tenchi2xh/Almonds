# -*- encoding: utf-8 -*-


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
