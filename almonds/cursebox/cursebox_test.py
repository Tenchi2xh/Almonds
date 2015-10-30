# -*- encoding: utf-8 -*-

import curses

from .cursebox import Cursebox


with Cursebox() as cb:
    cb.hide_cursor()

    try:
        for i in range(255):
            cb.change_cell(i % cb.width, i % cb.height, str(i), i, -1)
    except curses.ERR:
        # End of screen reached
        pass

    cb.screen.getch()
