# -*- encoding: utf-8 -*-
import termbox

import string

from drawing import *


class InputMenu(object):

    INPUT_WIDTH = 20

    def __init__(self, t, fields, title=""):
        self.t = t

        self.fields = fields
        self.values = ["" for _ in fields]
        self.title = title
        self.line = 0
        self.column = 0
        self.status = 0
        self.longest = 0

        self.width = 0
        self.height = 0
        self.x0 = 0
        self.y0 = 0

        self.open = True

    def show(self):
        self.draw_inputs()

        while self.open:
            event = self.t.poll_event()
            while event:
                (kind, ch, key, mod, w, h, x, y) = event
                if kind == termbox.EVENT_KEY and key == termbox.KEY_ESC:
                    self.status = -1
                    self.open = False

                if kind == termbox.EVENT_KEY:
                    if key in (termbox.KEY_ARROW_UP, termbox.KEY_ARROW_DOWN):
                        if key == termbox.KEY_ARROW_UP:
                            self.line = (self.line - 1) % len(self.fields)
                        elif key == termbox.KEY_ARROW_DOWN:
                            self.line = (self.line + 1) % len(self.fields)
                        self.column = len(self.values[self.line])
                    elif key == termbox.KEY_ENTER:
                        self.open = False
                    elif key == termbox.KEY_BACKSPACE2:
                        if self.column > 0:
                            self.column -= 1
                            self.values[self.line] = self.values[self.line][:-1]
                    elif self.column < self.INPUT_WIDTH:
                        if ch is not None and ch in string.printable:
                            self.column += 1
                            self.values[self.line] += ch
                        elif key == termbox.KEY_SPACE:
                            self.column += 1
                            self.values[self.line] += " "
                event = self.t.peek_event()

            if self.open:
                self.draw_inputs()

        self.t.hide_cursor()

        return self.status, self.values

    def draw_inputs(self):
        self.update_dimensions()

        # Clear
        fill(self.t, self.x0 + 1, self.y0 + 1, self.width - 2, self.height - 2, 32)

        offset_y = 0  # Vertical offset if a title is present

        # If there's a title, add a separator in the box
        h_seps = []
        if self.title != "":
            offset_y = 2
            h_seps.append(2)
        # Draw box, with eventual separator
        draw_box(self.t, self.x0, self.y0, self.width, self.height, h_seps=h_seps)

        # Centered title
        draw_text(self.t, self.x0 + 1, self.y0 + 1, " " * ((self.width - 2 - len(self.title)) / 2) + self.title)

        for y, field in enumerate(self.fields):
            text = " " + field + ": " + " " * (self.longest - len(field))
            if self.line == y:
                text += "$"
            text += self.values[y] + " " * (self.INPUT_WIDTH - len(self.values[y]))

            draw_text(self.t, self.x0 + 1, self.y0 + offset_y + y + 1, text)

        self.t.set_cursor(self.x0 + self.longest + 4 + self.column, self.y0 + offset_y + self.line + 1)

        self.t.present()

    def update_dimensions(self):
        # Prevent menu from taking the whole screen
        max_width = 2 * self.t.width() / 5

        longest = len(max(self.fields, key=len))
        self.longest = longest
        # Fit menu to option lengths if small enough, else use proportions
        # Also add space for borders, spaces, fields, ": "...
        self.width = (max_width if longest >= max_width else longest) + 4 + self.INPUT_WIDTH + 2
        self.height = len(self.fields) + 2

        # If a title is displayed, add more height
        if self.title != "":
            self.height += 2

        # Center the window
        self.x0 = (self.t.width() - self.width) / 2
        self.y0 = (self.t.height() - self.height) / 2
