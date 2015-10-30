# -*- encoding: utf-8 -*-

from __future__ import division

from time import sleep

from .drawing import *


class SplashPopup(object):
    def __init__(self, cb, message, box=False):
        self.cb = cb

        self.message = message.splitlines()
        self.box = box

        self.width = 0
        self.height = 0
        self.x0 = 0
        self.y0 = 0

    def show(self):
        self.draw_popup()
        sleep(1)
        return

    def draw_popup(self):
        self.update_dimensions()

        # Clear
        fill(self.cb, 0, 0, self.cb.width, self.cb.height, " ",
             colors.black, lambda: 16)

        if self.box:
            draw_box(self.cb, self.x0, self.y0, self.width, self.height)

        for y, line in enumerate(self.message):
            draw_text(self.cb, self.x0 + 1, self.y0 + 1 + y, line)

        self.cb.refresh()

    def update_dimensions(self):
        self.width = len(self.message[0]) + 2
        self.height = len(self.message) + 2

        # Center the popup
        self.x0 = (self.cb.width - self.width) // 2
        self.y0 = (self.cb.height - self.height) // 2
