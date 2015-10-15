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

BLOCKS = u"█▓▒░ "

# Palettes

PALETTE_1 = [termbox.BLACK, termbox.BLUE, termbox.CYAN, termbox.WHITE]
PALETTE_2 = [termbox.RED, termbox.YELLOW, termbox.BLACK]
PALETTE_3 = [termbox.GREEN, termbox.YELLOW, termbox.CYAN, termbox.WHITE]
PALETTE_4 = [termbox.BLACK, termbox.WHITE]
PALETTE_5 = [termbox.BLUE, termbox.YELLOW, termbox.BLACK]
PALETTES = [("Moonlight", PALETTE_1),
            ("Magma", PALETTE_2),
            ("Radioactive", PALETTE_3),
            ("Monochrome", PALETTE_4),
            ("Neon", PALETTE_5)]


def dither_symbol(value):
    """
    Returns the appropriate block drawing symbol for the given intensity.
    :param value: intensity of the color, in the range [0.0, 1.0]
    :return: dithered symbol representing that intensity
    """
    return ord(BLOCKS[int(round(value * 4))])


def draw_dithered_color(t, x, y, palette, n, n_max):
    """
    Draws a dithered color block on the terminal, given a palette.
    :type t: termbox.Termbox
    """
    i = n * float(len(palette) - 1) / n_max
    c1 = palette[int(math.floor(i))]
    c2 = palette[int(math.ceil(i))]
    value = i - int(math.floor(i))

    symbol = dither_symbol(value)
    t.change_cell(x, y, symbol, c1, c2)


def draw_gradient(t, x0, y0, w, h, palette):
    """
    Test function that draws a gradient in the given rect.
    :type t: termbox.Termbox
    """
    for x in xrange(w - 1):
        for y in xrange(h - 1):
            draw_dithered_color(t, x0 + x, y0 + y, palette, x, w - 1)


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


def draw_text(t, x0, y0, string, fg=termbox.DEFAULT, bg=termbox.BLACK):
    for i, c in enumerate(string):
        t.change_cell(x0 + i, y0, ord(c), fg, bg)
