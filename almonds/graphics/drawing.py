# -*- encoding: utf-8 -*-

from __future__ import division

import math
import os
import sys

from ..cursebox import colors
from ..cursebox import symbols
from ..utils import *

# Box drawing symbols

BOX_CORNERS      = [symbols["BOX_TOP_LEFT"], symbols["BOX_TOP_RIGHT"],
                    symbols["BOX_BOTTOM_LEFT"], symbols["BOX_BOTTOM_RIGHT"]]

# Block drawing symbols

DITHER_TYPES = [("8 colors ANSI", symbols.dither1),
                ("8 colors ASCII", symbols.dither2),
                ["256 colors"]]

if is_native_windows():
    DITHER_TYPES.pop()

# Palettes

PALETTE_1 = [colors.black, colors.blue, colors.cyan, colors.white]
PALETTE_2 = [colors.black, colors.red, colors.yellow, colors.black]
PALETTE_3 = [colors.black, colors.green, colors.cyan, colors.yellow, colors.white]
PALETTE_4 = [colors.white, colors.black, colors.white]
PALETTE_5 = [colors.black, colors.blue, colors.yellow, colors.white]
PALETTE_6 = [colors.white, colors.magenta, colors.black, colors.black, colors.white]
PALETTE_7 = [colors.black, colors.red, colors.yellow, colors.green,
             colors.cyan, colors.blue, colors.magenta, colors.black]
PALETTE_8 = [colors.black, colors.red, colors.yellow]
PALETTES = [("Moonlight", PALETTE_1),
            ("Magma", PALETTE_2),
            ("Radioactive", PALETTE_3),
            ("Monochrome", PALETTE_4),
            ("Neon", PALETTE_5),
            ("Hello Kitty", PALETTE_6),
            ("Rainbow", PALETTE_7),
            ("Fire", PALETTE_8)]

# Colors

COLORS = {colors.black:   (  0,   0,   0),
          colors.red:     (255,   0,   0),
          colors.green:   (  0, 255,   0),
          colors.blue:    (  0,   0, 255),
          colors.yellow:  (255, 255,   0),
          colors.magenta: (255,   0, 255),
          colors.cyan:    (0,   255, 255),
          colors.white:   (255, 255, 255)}


def sort_palette(palette):
    def intensity(color):
        return sum(COLORS[color]) / 3

    return sorted(list(set(palette)), key=intensity)


def dither_symbol(value, dither):
    """
    Returns the appropriate block drawing symbol for the given intensity.
    :param value: intensity of the color, in the range [0.0, 1.0]
    :return: dithered symbol representing that intensity
    """
    dither = DITHER_TYPES[dither][1]
    return dither[int(round(value * (len(dither) - 1)))]


def draw_dithered_color(cb, x, y, palette, dither, n, n_max, crosshairs_coord=None):
    """
    Draws a dithered color block on the terminal, given a palette.
    :type cb: cursebox.CurseBox
    """
    i = n * (len(palette) - 1) / n_max
    c1 = palette[int(math.floor(i))]
    c2 = palette[int(math.ceil(i))]
    value = i - int(math.floor(i))

    symbol = dither_symbol(value, dither)

    if crosshairs_coord is not None:
        old_symbol = symbol
        symbol, crosshairs = get_crosshairs_symbol(x, y, old_symbol, crosshairs_coord)
        if crosshairs:
            sorted_palette = sort_palette(palette)
            if old_symbol == DITHER_TYPES[dither][1][0]:
                c2 = c1
            sorted_index = sorted_palette.index(c2)
            if sorted_index > len(sorted_palette) // 2:
                c1 = sorted_palette[0]
            else:
                c1 = sorted_palette[-1]

    cb.put(x, y, symbol, c1(), c2())


def draw_color(cb, x, y, value, max_iterations, palette, crosshairs_coord=None):
    bg = get_color(value, max_iterations, palette)
    symbol = " "
    fg = colors.black()
    if crosshairs_coord is not None:
        symbol, crosshairs = get_crosshairs_symbol(x, y, symbol, crosshairs_coord)
        if crosshairs:
            fg = colors.to_xterm((255 - bg[0], 255 - bg[1], 255 - bg[2]))

    cb.put(x, y, symbol, fg, colors.to_xterm(bg))


def get_crosshairs_symbol(x, y, symbol, crosshairs_coord):

    crosshairs = False
    if x == crosshairs_coord[0]:
        crosshairs = True
        if y == crosshairs_coord[1]:
            symbol = symbols["BOX_X_MIDDLE"]
        else:
            symbol = symbols["BOX_VERTICAL"]
    elif y == crosshairs_coord[1]:
        crosshairs = True
        symbol = symbols["BOX_HORIZONTAL"]

    return symbol, crosshairs


def draw_box(cb, x0, y0, w, h, fg=colors.default_fg, bg=colors.default_bg, h_seps=[], v_seps=[]):
    """
    Draws a box in the given terminal.
    :type cb: cursebox.CurseBox
    """
    w -= 1
    h -= 1
    corners = [(x0, y0), (x0 + w, y0), (x0, y0 + h), (x0 + w, y0 + h)]

    fg = fg()
    bg = bg()

    for i, c in enumerate(corners):
        cb.put(c[0], c[1], BOX_CORNERS[i], fg, bg)

    for s in h_seps + [0, h]:
        cb.put(x0 + 1, y0 + s, symbols["BOX_HORIZONTAL"] * (w - 1), fg, bg)

    for y in range(1, h):
        for s in v_seps + [0, w]:
            cb.put(x0 + s, y0 + y, symbols["BOX_VERTICAL"], fg, bg)

    for s in h_seps:
        cb.put(x0,     y0 + s, symbols["BOX_X_LEFT"],  fg, bg)
        cb.put(x0 + w, y0 + s, symbols["BOX_X_RIGHT"], fg, bg)

    for s in v_seps:
        cb.put(x0 + s, y0,     symbols["BOX_X_TOP"],    fg, bg)
        cb.put(x0 + s, y0 + h, symbols["BOX_X_BOTTOM"], fg, bg)


def draw_progress_bar(cb, message, value, max_value):
    """
    :type cb: cursebox.Cursebox
    """
    m_x = cb.width // 2
    m_y = cb.height // 2
    w = len(message) + 4
    h = 3
    draw_box(cb, m_x - w // 2, m_y - 1, w, h)
    message = " %s " % message
    i = int((value / max_value) * (len(message) + 2))
    message = "$" + message[:i] + "$" + message[i:]
    draw_text(cb, m_x - w // 2 + 1, m_y, message)


def draw_scroll_bar(cb, x0, y0, h, n_visible, n_items, position, fg=colors.default_fg, bg=colors.default_bg):
    knob_height = int(h * n_visible / n_items)
    knob_position = int((h - knob_height) * position / n_items)
    knob_end = knob_position + knob_height

    for y in range(h):
        symbol = u"█" if knob_position <= y <= knob_end else u"░"
        cb.put(x0, y0 + y, symbol, fg(), bg())


def draw_text(cb, x0, y0, string, fg=colors.default_fg, bg=colors.default_bg):
    markup_compensation = 0
    fg = fg()
    bg = bg()
    for i, c in enumerate(string):
        if c == "$":
            fg, bg = bg, fg
            markup_compensation += 1
            continue
        cb.put(x0 + i - markup_compensation, y0, c, fg, bg)


def fill(cb, x0, y0, w, h, symbol, fg=colors.default_fg, bg=colors.default_bg):
    for y in range(h):
        cb.put(x0, y0 + y, symbol * (w - 1), fg(), bg())


def interpolate(c1, c2, factor):
    return (int(c1[0] * (1 - factor) + c2[0] * factor),
            int(c1[1] * (1 - factor) + c2[1] * factor),
            int(c1[2] * (1 - factor) + c2[2] * factor))


def get_color(count, max_iterations, palette):
    i = count * (len(palette) - 1.0) / max_iterations
    c1 = COLORS[palette[int(math.floor(i))]]
    c2 = COLORS[palette[int(math.ceil(i))]]
    return interpolate(c1, c2, i - int(math.floor(i)))
