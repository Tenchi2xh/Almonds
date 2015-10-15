#!/usr/bin/python
# -*- encoding: utf-8 -*-

import sys
import textwrap
import time
import datetime

import termbox

from graphics import *
from mandelbrot import *
from logger import *

__version__ = "1.0"

MENU_WIDTH = 40

"""
TODO:
  - Multi-threading
  - Hi-res capture (use resolution)
  - Open menu, looks for .params files
  - Git + releases
  - Adaptive palette
  - Alternative dithering strings
  - Julia ?
"""

def draw_panel(t, params, log):
    """
    Draws the application's main panel
    :type t: termbox.Termbox
    """
    w = t.width() - MENU_WIDTH - 1
    h = t.height() - 1

    params.plane_w = w
    params.plane_h = h
    params.resize(w, h)

    draw_box(t, 0, 0, w + 1, h + 1)
    # draw_gradient(t, 1, 1, w, h, PALETTE_1)

    generated = 0
    palette = PALETTES[params.palette][1]
    if params.reverse_palette:
        palette = palette[::-1]

    xs = xrange(params.plane_cx, params.plane_cx + params.plane_w - 1)
    ys = xrange(params.plane_cy, params.plane_cy + params.plane_h - 1)
    for x in xs:
        for y in ys:
            if params.plane[x, y] is None:
                params.plane[x, y] = mandelbrot(x, y, params)
                generated += 1
            draw_dithered_color(t, x - params.plane_cx + 1,
                                   y - params.plane_cy + 1,
                                   palette,
                                   params.plane[x, y],
                                   params.max_iterations)

    if generated > 0:
        log("Added %d missing cells" % generated)


def draw_menu(t, params, log):
    """
    Draws the application's side menu
    :type t: termbox.Termbox
    """
    w = t.width()
    h = t.height()

    x0 = w - MENU_WIDTH + 1

    def stats(k, v, shortcuts):
        draw_text(t, x0 + 1, 2 + stats.counter,
                  "%s %s %s" % (k, str(v).rjust(MENU_WIDTH - 14 - len(k)), shortcuts))
        stats.counter += 1
    stats.counter = 1
    draw_text(t, x0, 1, ("Almonds v.%s" % __version__).center(MENU_WIDTH - 2))
    # Write stats
    stats("Real", params.mb_cx, u"[←], [→]")
    stats("Imaginary", params.mb_cy, u"[↑], [↓]")
    stats.counter += 1
    stats("Zoom", params.zoom, "[Z], [U]")
    stats("Iterations", params.max_iterations, "[I], [O]")
    stats.counter += 1
    stats("Palette", PALETTES[params.palette][0], "[P]")
    stats("Palette order", "Reversed" if params.reverse_palette else "Normal", "[R]")
    stats("Palette mode", "Adaptive" if params.adaptive_palette else "Linear", "[A]")
    stats.counter += 1
    stats("Hi-res capture", "", "[C]")
    stats("Save", "", "[S]")
    stats("Exit", "", "[ESC]")

    middle = 3 + stats.counter
    draw_box(t, w - MENU_WIDTH, 0, MENU_WIDTH, h, h_seps=[2, 5, 8, 12, middle - 1, middle + 1])

    # Write log
    draw_text(t, x0, middle, "Event log".center(MENU_WIDTH - 2))
    latest_logs = log.get_latest(h - middle)
    latest_logs = map(lambda l: textwrap.wrap(l, MENU_WIDTH - 4)[::-1], latest_logs)  # Wrap all messages
    latest_logs = [l for ls in latest_logs for l in ls]                               # Flatten
    i = h - 2
    for l in latest_logs:
        draw_text(t, x0 + 1, i, l)
        i -= 1
        if i == middle + 1:
            break


def update_display(t, params, log):

    t.clear()
    draw_panel(t, params, log)
    update_position(params)
    draw_menu(t, params, log)
    t.present()


def save(params, log):
    import cPickle
    ts = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d_%H-%M-%S")
    cPickle.dump(params, open("almonds_%s.params" % ts, "wb"))
    log("Current scene saved!")


def main():
    begin = time.time()
    with termbox.Termbox() as t:

        log = Logger()
        log("Welcome to Almonds v.%s" % __version__)

        params = Params(1.0, 40, log)
        if len(sys.argv) == 2:
            import cPickle
            params = cPickle.load(open(sys.argv[1], "rb"))
            params.reload(log)

        update_display(t, params, log)

        running = True
        while running:
            event = t.poll_event()
            while event:
                (kind, ch, key, mod, w, h, x, y) = event
                if kind == termbox.EVENT_KEY and key in (termbox.KEY_ESC, termbox.KEY_CTRL_C):
                    running = False
                if kind == termbox.EVENT_KEY:
                    # Navigation
                    if key == termbox.KEY_ARROW_UP:
                        params.plane_cy -= 1
                    elif key == termbox.KEY_ARROW_DOWN:
                        params.plane_cy += 1
                    elif key == termbox.KEY_ARROW_LEFT:
                        params.plane_cx -= 2
                    elif key == termbox.KEY_ARROW_RIGHT:
                        params.plane_cx += 2
                    # Zoom / un-zoom
                    elif ch == "z":
                        zoom(params, 1.3)
                    elif ch == "u":
                        zoom(params, 1 / 1.3)
                    # Iterations control
                    elif ch == "i":
                        params.max_iterations += 10
                        params.plane.reset()
                    elif ch == "o":
                        params.max_iterations -= 10
                        if params.max_iterations <= 0:
                            params.max_iterations = 10
                        else:
                            params.plane.reset()
                    # Palette swap
                    elif ch == "p":
                        params.palette = (params.palette + 1) % len(PALETTES)
                    elif ch == "r":
                        params.reverse_palette = not params.reverse_palette
                    # Misc
                    elif ch == "s":
                        save(params, log)

                event = t.peek_event()
            if running:
                update_display(t, params, log)

    spent = (time.time() - begin) / 60
    print "\nSpent %d minutes exploring fractals, see you soon :)\n" % spent
    print "- Almonds v.%s by Tenchi <tenchi@team2xh.net>\n" % __version__

if __name__ == "__main__":
    main()
