# -*- encoding: utf-8 -*-

from __future__ import division

from ..cursebox import *
from .drawing import *


class InputMenu(object):

    INPUT_WIDTH = 20

    def __init__(self, cb, fields, title=""):
        self.cb = cb

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
            event = self.cb.poll_event()

            if event == EVENT_ESC:
                self.status = -1
                self.open = False

            if event in (EVENT_UP, EVENT_DOWN):
                if event == EVENT_UP:
                    self.line = (self.line - 1) % len(self.fields)
                elif event == EVENT_DOWN:
                    self.line = (self.line + 1) % len(self.fields)
                self.column = len(self.values[self.line])
            elif event == EVENT_ENTER:
                self.open = False
            elif event == EVENT_BACKSPACE:
                if self.column > 0:
                    self.column -= 1
                    self.values[self.line] = self.values[self.line][:-1]
            elif self.column < self.INPUT_WIDTH:
                if len(event) == 1:
                    self.column += 1
                    self.values[self.line] += event

            if self.open:
                self.draw_inputs()

        self.cb.hide_cursor()

        return self.status, self.values

    def draw_inputs(self):
        self.update_dimensions()

        # Clear
        fill(self.cb, self.x0 + 1, self.y0 + 1, self.width - 2, self.height - 2, " ")

        offset_y = 0  # Vertical offset if a title is present

        # If there's a title, add a separator in the box
        h_seps = []
        if self.title != "":
            offset_y = 2
            h_seps.append(2)
        # Draw box, with eventual separator
        draw_box(self.cb, self.x0, self.y0, self.width, self.height, h_seps=h_seps)

        # Centered title
        draw_text(self.cb, self.x0 + 1, self.y0 + 1, " " * ((self.width - 2 - len(self.title)) // 2) + self.title)

        for y, field in enumerate(self.fields):
            text = " " + field + ": " + " " * (self.longest - len(field))
            if self.line == y:
                text += "$"
            text += self.values[y] + " " * (self.INPUT_WIDTH - len(self.values[y]))

            draw_text(self.cb, self.x0 + 1, self.y0 + offset_y + y + 1, text)

        self.cb.set_cursor(self.x0 + self.longest + 4 + self.column, self.y0 + offset_y + self.line + 1)

        self.cb.refresh()

    def update_dimensions(self):
        # Prevent menu from taking the whole screen
        max_width = 2 * self.cb.width // 5

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
        self.x0 = (self.cb.width - self.width) // 2
        self.y0 = (self.cb.height - self.height) // 2
