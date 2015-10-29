# -*- encoding: utf-8 -*-

import curses

from cursebox import CurseBox

with CurseBox() as cb:
    cb.hide_cursor()

    try:
        for i in range(20):
            cb.change_cell(i, i // 3, ord("X"), i, 255 - i)
    except curses.ERR:
        # End of screen reached
        pass

    cb.screen.getch()
