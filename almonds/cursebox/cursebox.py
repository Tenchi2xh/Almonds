# -*- encoding: utf-8 -*-

import curses
import os
import locale

from .constants import *
from .symbols import symbols
from .pairs import Pairs


class Cursebox(object):
    """
    A wrapper for curses which provides simple API calls.

    Instances should be created using the with statement,
    which will take care of initializing the curses environment
    and disposing of it when the context is lost:

    >>> with Cursebox() as cb:
    >>>    cb.put(42, 13, "Hello from curses!", colors.black, colors.white)
    >>>    cb.refresh()

    Cursebox also handles keyboard strokes and events:

    >>> event = cb.poll_event()
    >>> if event == EVENT_CTRL_C:
    >>>     exit()
    """

    def hide_cursor(self):
        """
        Hides the cursor.
        """
        curses.curs_set(0)

    def set_cursor(self, x, y):
        """
        Sets the cursor to the desired position.

        :param x: X position
        :param y: Y position
        """
        curses.curs_set(1)
        self.screen.move(y, x)

    def refresh(self):
        """
        Refreshes the screen.
        """
        self.screen.refresh()

    def put(self, x, y, text, fg, bg):
        """
        Puts a string at the desired coordinates using the provided colors.

        :param x:    X position
        :param y:    Y position
        :param text: Text to write
        :param fg:   Foreground color number
        :param bg:   Background color number
        """
        if x < self.width and y < self.height:
            try:
                self.screen.addstr(y, x, symbols.encode(text), self.pairs[fg, bg])
            except curses.error:
                # Ignore out of bounds error
                pass

    def put_arrow(self, x, y, direction, fg, bg):
        ch = getattr(curses, "ACS_UARROW")
        if direction == "down":
            ch = getattr(curses, "ACS_DARROW")
        if direction == "left":
            ch = getattr(curses, "ACS_LARROW")
        if direction == "right":
            ch = getattr(curses, "ACS_RARROW")

        if x < self.width and y < self.height:
            try:
                self.screen.addch(y, x, ch, self.pairs[fg, bg])
            except curses.error:
                # Ignore out of bounds error
                pass


    @property
    def width(self):
        """
        The width of the current terminal.
        """
        return self.screen.getmaxyx()[1]

    @property
    def height(self):
        """
        The height of the current terminal.
        """
        return self.screen.getmaxyx()[0]

    def clear(self):
        """
        Clears the terminal.
        """
        self.screen.clear()

    def poll_event(self):
        """
        Waits for an event to happen and returns a string related to the event.

        If the event is a normal (letter) key press, the letter is returned (case sensitive)

        :return: Event type
        """
        # Flush all inputs before this one that were done since last poll
        curses.flushinp()

        ch = self.screen.getch()

        if ch == 27:
            return EVENT_ESC
        elif ch == -1 or ch == curses.KEY_RESIZE:
            return EVENT_RESIZE
        elif ch == 10 or ch == curses.KEY_ENTER:
            return EVENT_ENTER
        elif ch == 127 or ch == curses.KEY_BACKSPACE:
            return EVENT_BACKSPACE
        elif ch == curses.KEY_UP:
            return EVENT_UP
        elif ch == curses.KEY_DOWN:
            return EVENT_DOWN
        elif ch == curses.KEY_LEFT:
            return EVENT_LEFT
        elif ch == curses.KEY_RIGHT:
            return EVENT_RIGHT
        elif ch == 3:
            return EVENT_CTRL_C
        elif 0 <= ch < 256:
            return chr(ch)
        else:
            return EVENT_UNHANDLED

    def __enter__(self):
        os.environ["ESCDELAY"] = "25"        # Default delay when pressing ESC is 1000ms
        self.pairs = Pairs()                 # Initialize our pairs dictionary
        locale.setlocale(locale.LC_ALL, "")  # Make curses use unicode

        self.screen = curses.initscr()       # Initialize curses and get a screen handle

        curses.noecho()                      # Pressed keys will not print their value on the screen
        curses.raw()                         # Using raw instead of cbreak() gives us access to CTRL+C and others
        self.screen.keypad(True)             # Convert special keys escape sequences to curses magic numbers
        curses.start_color()                 # We want colors
        curses.use_default_colors()          # Allow use of standard color numbers
        self.hide_cursor()                   # We don't want the cursor

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        curses.noraw()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
