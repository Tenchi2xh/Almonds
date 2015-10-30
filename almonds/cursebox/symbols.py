# -*- encoding: utf-8 -*-

import os
import sys

from ..utils import is_native_windows

UTF8_SYMBOLS = {
    "BOX_TOP_LEFT"    : u"┌",
    "BOX_TOP_RIGHT"   : u"┐",
    "BOX_BOTTOM_LEFT" : u"└",
    "BOX_BOTTOM_RIGHT": u"┘",
    "BOX_HORIZONTAL"  : u"─",
    "BOX_VERTICAL"    : u"│",
    "BOX_X_LEFT"      : u"├",
    "BOX_X_RIGHT"     : u"┤",
    "BOX_X_TOP"       : u"┬",
    "BOX_X_BOTTOM"    : u"┴",
    "BOX_X_MIDDLE"    : u"┼",
    "DITHER_1"        : u"█▓▒░ ",
    "DITHER_2"        : u"#&X$x=+;:,. ",
    "ARROW_UP"        : u"↑",
    "ARROW_DOWN"      : u"↓",
    "ARROW_LEFT"      : u"←",
    "ARROW_RIGHT"     : u"→"
}

CP437_SYMBOLS = {
    "BOX_TOP_LEFT"    : chr(218),
    "BOX_TOP_RIGHT"   : chr(191),
    "BOX_BOTTOM_LEFT" : chr(192),
    "BOX_BOTTOM_RIGHT": chr(217),
    "BOX_HORIZONTAL"  : chr(196),
    "BOX_VERTICAL"    : chr(179),
    "BOX_X_LEFT"      : chr(195),
    "BOX_X_RIGHT"     : chr(180),
    "BOX_X_TOP"       : chr(194),
    "BOX_X_BOTTOM"    : chr(193),
    "BOX_X_MIDDLE"    : chr(197),
    "DITHER_1"        : chr(219) + chr(178) + chr(177) + chr(176) + chr(32),
    "DITHER_2"        : "#&X$x=+;:,. ",
    "ARROW_UP"        : chr(24),
    "ARROW_DOWN"      : chr(25),
    "ARROW_LEFT"      : chr(27),
    "ARROW_RIGHT"     : chr(26)
}


class Symbols(object):
    def __init__(self):
        if is_native_windows():
            self.symbols = CP437_SYMBOLS
            self.encoding = "cp437"
        else:
            self.symbols = UTF8_SYMBOLS
            self.encoding = "utf-8"
        self.symbols["DITHER_1"] = list(self.symbols["DITHER_1"])

    def __getitem__(self, key):
        return self.symbols[key]

    @property
    def dither1(self):
        return self.symbols["DITHER_1"]

    @property
    def dither2(self):
        return self.symbols["DITHER_2"]

    def encode(self, string):
        if self.encoding == "cp437":
            return string
        return string.encode(self.encoding)

symbols = Symbols()
