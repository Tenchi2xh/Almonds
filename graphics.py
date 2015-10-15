# -*- encoding: utf-8 -*-

import math
import termbox

# Box drawing symbols

BOX_TOP_LEFT     = ord(u"┌")
BOX_TOP_RIGHT    = ord(u"┐")
BOX_BOTTOM_LEFT  = ord(u"└")
BOX_BOTTOM_RIGHT = ord(u"┘")
BOX_CORNERS      = [BOX_TOP_LEFT, BOX_TOP_RIGHT, BOX_BOTTOM_LEFT, BOX_BOTTOM_RIGHT]

BOX_HORIZONTAL   = ord(u"─")
BOX_VERTICAL     = ord(u"│")

BOX_X_LEFT       = ord(u"├")
BOX_X_RIGHT      = ord(u"┤")
BOX_X_TOP        = ord(u"┬")
BOX_X_BOTTOM     = ord(u"┴")
BOX_X_MIDDLE     = ord(u"┼")

# Block drawing symbols

DITHER_1 = u"█▓▒░ "
DITHER_2 = u"#&X$x=+;:,. "
DITHER_TYPES = [("ANSI", DITHER_1),
                ("ASCII Art", DITHER_2)]

# Palettes

PALETTE_1 = [termbox.BLACK, termbox.BLUE, termbox.CYAN, termbox.WHITE]
PALETTE_2 = [termbox.BLACK, termbox.RED, termbox.YELLOW, termbox.BLACK]
PALETTE_3 = [termbox.BLACK, termbox.GREEN, termbox.CYAN, termbox.YELLOW, termbox.WHITE]
PALETTE_4 = [termbox.BLACK, termbox.BLACK, termbox.WHITE, termbox.WHITE, termbox.WHITE]
PALETTE_5 = [termbox.BLACK, termbox.BLUE, termbox.YELLOW, termbox.WHITE]
PALETTE_6 = [termbox.WHITE, termbox.MAGENTA, termbox.BLACK, termbox.BLACK, termbox.WHITE]
PALETTES = [("Moonlight", PALETTE_1),
            ("Magma", PALETTE_2),
            ("Radioactive", PALETTE_3),
            ("Monochrome", PALETTE_4),
            ("Neon", PALETTE_5),
            ("Hello Kitty", PALETTE_6)]

# Colors

COLORS = {termbox.BLACK:   (  0,   0,   0),
          termbox.RED:     (255,   0,   0),
          termbox.GREEN:   (  0, 255,   0),
          termbox.BLUE:    (  0,   0, 255),
          termbox.YELLOW:  (255, 255,   0),
          termbox.MAGENTA: (255,   0, 255),
          termbox.CYAN:    (0,   255, 255),
          termbox.WHITE:   (255, 255, 255)}


def dither_symbol(value, dither):
    """
    Returns the appropriate block drawing symbol for the given intensity.
    :param value: intensity of the color, in the range [0.0, 1.0]
    :return: dithered symbol representing that intensity
    """
    dither = DITHER_TYPES[dither][1]
    return ord(dither[int(round(value * (len(dither) - 1)))])


def draw_dithered_color(t, x, y, palette, dither, n, n_max):
    """
    Draws a dithered color block on the terminal, given a palette.
    :type t: termbox.Termbox
    """
    i = n * float(len(palette) - 1) / n_max
    c1 = palette[int(math.floor(i))]
    c2 = palette[int(math.ceil(i))]
    value = i - int(math.floor(i))

    symbol = dither_symbol(value, dither)
    t.change_cell(x, y, symbol, c1, c2)


def draw_gradient(t, x0, y0, w, h, palette, dither):
    """
    Test function that draws a gradient in the given rect.
    :type t: termbox.Termbox
    """
    for x in xrange(w - 1):
        for y in xrange(h - 1):
            draw_dithered_color(t, x0 + x, y0 + y, palette, dither, x, w - 1)


def draw_box(t, x0, y0, w, h, fg=termbox.DEFAULT, bg=termbox.BLACK, h_seps=[], v_seps=[]):
    """
    Draws a box in the given terminal.
    :type t: termbox.Termbox
    """
    w -= 1
    h -= 1
    corners = [(x0, y0), (x0 + w, y0), (x0, y0 + h), (x0 + w, y0 + h)]

    for i, c in enumerate(corners):
        t.change_cell(c[0], c[1], BOX_CORNERS[i], fg, bg)
    for x in xrange(1, w):
        for s in h_seps + [0, h]:
            t.change_cell(x0 + x, y0 + s, BOX_HORIZONTAL, fg, bg)
    for y in xrange(1, h):
        for s in v_seps + [0, w]:
            t.change_cell(x0 + s, y0 + y, BOX_VERTICAL, fg, bg)
    for s in h_seps:
        t.change_cell(x0,     y0 + s, BOX_X_LEFT,  fg, bg)
        t.change_cell(x0 + w, y0 + s, BOX_X_RIGHT, fg, bg)
    for s in v_seps:
        t.change_cell(x0 + s, y0,     BOX_X_TOP,    fg, bg)
        t.change_cell(x0 + s, y0 + h, BOX_X_BOTTOM, fg, bg)


def draw_text(t, x0, y0, string, fg=termbox.WHITE, bg=termbox.BLACK):
    markup_compensation = 0
    for i, c in enumerate(string):
        if c == "$":
            fg, bg = bg, fg
            markup_compensation += 1
            continue
        t.change_cell(x0 + i - markup_compensation, y0, ord(c), fg, bg)


def interpolate(c1, c2, factor):
    return (int(c1[0] * (1 - factor) + c2[0] * factor),
            int(c1[1] * (1 - factor) + c2[1] * factor),
            int(c1[2] * (1 - factor) + c2[2] * factor))


def get_color(count, max_iterations, palette):
    i = count * (len(palette) - 1.0) / max_iterations
    c1 = COLORS[palette[int(math.floor(i))]]
    c2 = COLORS[palette[int(math.ceil(i))]]
    return interpolate(c1, c2, i - int(math.floor(i)))
