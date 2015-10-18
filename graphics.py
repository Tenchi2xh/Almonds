# -*- encoding: utf-8 -*-

import math
import termbox

from colors import colors

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
DITHER_TYPES = [("8 colors ANSI", DITHER_1),
                ("8 colors ASCII", DITHER_2),
                ["256 colors"]]

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
    c1 = palette[int(math.floor(i))]()
    c2 = palette[int(math.ceil(i))]()
    value = i - int(math.floor(i))

    symbol = dither_symbol(value, dither)
    t.change_cell(x, y, symbol, c1, c2)


# FIXME: Consider dither type 2 (256 colors)
def draw_gradient(t, x0, y0, w, h, palette, dither):
    """
    Test function that draws a gradient in the given rect.
    :type t: termbox.Termbox
    """
    for x in xrange(w - 1):
        for y in xrange(h - 1):
            draw_dithered_color(t, x0 + x, y0 + y, palette, dither, x, w - 1)


def draw_box(t, x0, y0, w, h, fg=colors.default_fg, bg=colors.default_bg, h_seps=[], v_seps=[]):
    """
    Draws a box in the given terminal.
    :type t: termbox.Termbox
    """
    w -= 1
    h -= 1
    corners = [(x0, y0), (x0 + w, y0), (x0, y0 + h), (x0 + w, y0 + h)]

    fg = fg()
    bg = bg()

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


def draw_progress_bar(t, message, value, max_value):
    """
    :type t: termbox.Termbox
    """
    m_x = t.width() / 2
    m_y = t.height() / 2
    w = len(message) + 4
    h = 3
    draw_box(t, m_x - w / 2, m_y - 1, w, h)
    message = " %s " % message
    i = int((float(value) / max_value) * (len(message) + 2))
    message = "$" + message[:i] + "$" + message[i:]
    draw_text(t, m_x - w / 2 + 1, m_y, message)


def draw_scroll_bar(t, x0, y0, h, n_visible, n_items, position, fg=colors.default_fg, bg=colors.default_bg):
    knob_height = int(h * 1.0 * n_visible / n_items)
    knob_position = int((h - knob_height) * 1.0 * position / n_items)
    knob_end = knob_position + knob_height

    for y in xrange(h):
        symbol = ord(u"█") if knob_position <= y <= knob_end else ord(u"░")
        t.change_cell(x0, y0 + y, symbol, fg(), bg())


def draw_text(t, x0, y0, string, fg=colors.default_fg, bg=colors.default_bg):
    markup_compensation = 0
    fg = fg()
    bg = bg()
    for i, c in enumerate(string):
        if c == "$":
            fg, bg = bg, fg
            markup_compensation += 1
            continue
        t.change_cell(x0 + i - markup_compensation, y0, ord(c), fg, bg)


def fill(t, x0, y0, w, h, symbol, fg=colors.default_fg, bg=colors.default_bg):
    for x in xrange(w):
        for y in xrange(h):
            t.change_cell(x0 + x, y0 + y, symbol, fg(), bg())


def interpolate(c1, c2, factor):
    return (int(c1[0] * (1 - factor) + c2[0] * factor),
            int(c1[1] * (1 - factor) + c2[1] * factor),
            int(c1[2] * (1 - factor) + c2[2] * factor))


def get_color(count, max_iterations, palette):
    i = count * (len(palette) - 1.0) / max_iterations
    c1 = COLORS[palette[int(math.floor(i))]]
    c2 = COLORS[palette[int(math.ceil(i))]]
    return interpolate(c1, c2, i - int(math.floor(i)))


class OptionMenu:
    def __init__(self, t, options, title=""):
        self.t = t

        self.title = title
        self.options = options
        self.selected = 0
        self.open = True

    def show(self):
        self.draw_menu()

        while self.open:
            event = self.t.poll_event()
            while event:
                (kind, ch, key, mod, w, h, x, y) = event
                if kind == termbox.EVENT_KEY and key == termbox.KEY_ESC:
                    self.selected = -1
                    self.open = False
                if kind == termbox.EVENT_KEY:
                    if key == termbox.KEY_ARROW_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif key == termbox.KEY_ARROW_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif key == termbox.KEY_ENTER:
                        self.open = False
                event = self.t.peek_event()

            if self.open:
                self.draw_menu()

        return self.selected

    def draw_menu(self):
        self.update_dimensions()

        # Clear
        fill(self.t, self.x0 + 1, self.y0 + 1, self.width - 2, self.height - 2, 32)

        offset_y = 0  # Vertical offset if a title is present
        offset_x = 0  # Horizontal negative offset if a scroll bar is present

        # If there's a title, add a separator in the box
        h_seps = []
        if self.title != "":
            offset_y = 2
            h_seps.append(2)
        # Draw box, with eventual separator
        draw_box(self.t, self.x0, self.y0, self.width, self.height, h_seps=h_seps)

        # Centered title
        # FIXME: Account for title in widget width
        draw_text(self.t, self.x0 + 1, self.y0 + 1, " " * ((self.width - 2 - len(self.title)) / 2) + self.title)

        # Figure out if we need to limit the view due to too many options
        view = self.options
        max_items = self.height - offset_y - 2
        offset_selected = 0
        # If too many options..
        if len(view) > max_items:
            # If selected option is further than the first half of first visible part the list,
            if self.selected > max_items / 2:
                # Start offsetting the view
                offset_selected = self.selected - (max_items / 2)
            # If we reach the end of the list,
            if self.selected > len(view) - (max_items / 2):
                # Keep a fixed offset
                offset_selected = len(view) - max_items

            view = view[offset_selected:max_items + offset_selected]
            offset_x = 1

        # Draw all options
        for y, item in enumerate(view):
            text = " " + item                                           # Prepend a space for visual prettiness
            if len(text) < self.width - 2 - offset_x:                   # If option too short,
                text += " " * (self.width - 2 - len(text) - offset_x)   # add spaces for highlight when selected
            elif len(text) > self.width - 3 - offset_x:                 # If too long,
                text = text[:self.width - 6 - offset_x] + "... "        # truncate
            if y == self.selected - offset_selected:                    # If it's the selected option,
                text = "$" + text                                       # highlight using custom markup

            draw_text(self.t, self.x0 + 1, self.y0 + offset_y + y + 1, text)

        # Draw scrollbar if present
        if offset_x != 0:
            draw_scroll_bar(self.t, self.x0 + self.width - 2, self.y0 + 1 + offset_y, self.height - 2 - offset_y,
                            max_items, len(self.options), self.selected)

        self.t.present()

    def update_dimensions(self):
        # Prevent menu from taking the whole screen
        max_width = 2 * self.t.width() / 5
        max_height = 2 * self.t.height() / 3

        longest = len(max(self.options, key=len))
        # Fit menu to option lengths if small enough, else use proportions
        self.width = (max_width if longest >= max_width else longest) + 4
        self.height = (max_height if len(self.options) >= max_height else len(self.options)) + 2

        # If a title is displayed, add more height
        if self.title != "":
            self.height += 2
        # If a scroll bar will be displayed, add more width
        if len(self.options) > self.height - (4 if self.title == "" else 2):
            self.width += 1

        # Center the menu
        self.x0 = (self.t.width() - self.width) / 2
        self.y0 = (self.t.height() - self.height) / 2
