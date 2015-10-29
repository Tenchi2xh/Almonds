# -*- encoding: utf-8 -*-

from __future__ import division

from time import sleep

import termbox

from .drawing import *


class SplashPopup(object):
    def __init__(self, t, message, box=False):
        self.t = t

        self.message = message.splitlines()
        self.box = box

        self.width = 0
        self.height = 0
        self.x0 = 0
        self.y0 = 0

    def show(self):
        self.draw_popup()
        sleep(2)
        return

    def draw_popup(self):
        self.update_dimensions()

        # Clear
        fill(self.t, self.x0 + 1, self.y0 + 1, self.width - 2, self.height - 2, 32)

        if self.box:
            draw_box(self.t, self.x0, self.y0, self.width, self.height)

        for y, line in enumerate(self.message):
            draw_text(self.t, self.x0 + 1, self.y0 + 1 + y, line)

        self.t.present()

    def update_dimensions(self):
        self.width = len(self.message[0]) + 2
        self.height = len(self.message) + 2

        # Center the popup
        self.x0 = (self.t.width() - self.width) // 2
        self.y0 = (self.t.height() - self.height) // 2
