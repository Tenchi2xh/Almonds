#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import sys
import textwrap
import time
import datetime
import multiprocessing
import subprocess

import termbox
from PIL import Image

from graphics import *
from mandelbrot import *
from logger import *
from params import *
from utils import *


__version__ = "1.8b"

MENU_WIDTH = 40


def draw_panel(t, params):
    """
    Draws the application's main panel
    :type t: termbox.Termbox
    """
    w = t.width() - MENU_WIDTH - 1
    h = t.height() - 1

    params.plane_w = w
    params.plane_h = h
    params.resize(w, h)

    palette = PALETTES[params.palette][1]
    if params.reverse_palette:
        palette = palette[::-1]

    draw_box(t, 0, 0, w + 1, h + 1)
    # draw_gradient(t, 1, 1, w, h, palette, params.dither_type)

    generated = 0
    missing_coords = []

    xs = xrange(params.plane_x0, params.plane_x0 + params.plane_w - 1)
    ys = xrange(params.plane_y0, params.plane_y0 + params.plane_h - 1)
    for x in xs:
        for y in ys:
            if params.plane[x, y] is None:
                missing_coords.append((x, y))
                generated += 1

    n_threads = 0
    if len(missing_coords) > 0:
        threads = []

        chunks = []
        chunk_size = (w * h) / (2 * multiprocessing.cpu_count())
        for i in xrange(0, len(missing_coords), chunk_size):
            chunks.append(missing_coords[i:i + chunk_size])

        n_threads = len(chunks)
        for i in xrange(n_threads):
            threads.append(MBWorker(chunks[i], params))
        for i in xrange(n_threads):
            threads[i].start()
        for i in xrange(n_threads):
            threads[i].join()
        for i in xrange(n_threads):
            for j in xrange(len(threads[i].coords)):
                c = threads[i].coords[j]
                params.plane[c[0], c[1]] = threads[i].results[j]

    if generated > 0:
        params.log("Added %d missing cells" % generated)
        if n_threads > 1:
            params.log("(Used %d threads)" % n_threads)

    if params.dither_type < 2:
        for x in xs:
            for y in ys:
                draw_dithered_color(t, x - params.plane_x0 + 1,
                                       y - params.plane_y0 + 1,
                                       palette, params.dither_type,
                                       (params.plane[x, y] + params.palette_offset) % (params.max_iterations + 1),
                                       params.max_iterations)
    else:
        for x in xs:
            for y in ys:
                c = get_color((params.plane[x, y] + params.palette_offset) % (params.max_iterations + 1),
                               params.max_iterations, palette)
                t.change_cell(x - params.plane_x0 + 1,
                              y - params.plane_y0 + 1,
                              32, colors.black(), colors.to_xterm(c))


def draw_menu(t, params):
    """
    Draws the application's side menu
    :type t: termbox.Termbox
    """
    w = t.width()
    h = t.height()

    x0 = w - MENU_WIDTH + 1

    fill(t, x0, 1, MENU_WIDTH, h - 2, 32)

    def stats(k, v, shortcuts):
        draw_text(t, x0 + 1, 2 + stats.counter,
                  "%s %s %s" % (k, str(v).rjust(MENU_WIDTH - 14 - len(k)), shortcuts))
        stats.counter += 1
    stats.counter = 1
    draw_text(t, x0, 1, ("Almonds v.%s" % __version__).center(MENU_WIDTH - 2))
    # Write stats
    stats("Real", params.mb_cx, u"$[←]$, $[→]$")
    stats("Imaginary", params.mb_cy, u"$[↑]$, $[↓]$")
    stats("Move speed", params.move_speed, "$[C]$, $[V]$")
    stats.counter += 1
    stats("Zoom", params.zoom, "$[Z]$, $[U]$")
    stats("Iterations", params.max_iterations, "$[I]$, $[O]$")
    stats.counter += 1
    stats("Palette", PALETTES[params.palette][0], "$[P]$")
    stats("Color mode", DITHER_TYPES[params.dither_type][0], "$[D]$")
    stats("Order", "Reversed" if params.reverse_palette else "Normal", "$[R]$")
    stats("Mode", "Adaptive" if params.adaptive_palette else "Linear", "$[A]$")
    stats("Cycle!", "", "$[X]$")
    stats.counter += 1
    stats("Hi-res capture", "", "$[H]$")
    stats("Save", "", "$[S]$")
    stats("Load", "", "$[L]$")
    stats("Exit", "", "$[ESC]$")

    middle = 3 + stats.counter
    draw_box(t, w - MENU_WIDTH, 0, MENU_WIDTH, h, h_seps=[2, 6, 9, 15, middle - 1, middle + 1])

    # Write log
    draw_text(t, x0, middle, "Event log".center(MENU_WIDTH - 2))
    latest_logs = params.log.get_latest(h - middle)
    latest_logs = map(lambda l: textwrap.wrap(l, MENU_WIDTH - 4)[::-1], latest_logs)  # Wrap all messages
    latest_logs = [l for ls in latest_logs for l in ls]                               # Flatten
    i = h - 2
    for l in latest_logs:
        draw_text(t, x0 + 1, i, l)
        i -= 1
        if i == middle + 1:
            break


def update_display(t, params):

    t.clear()
    draw_panel(t, params)
    update_position(params)
    draw_menu(t, params)
    t.present()


def save(params):
    import cPickle
    ts = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d_%H-%M-%S")
    if not os.path.exists("saves/"):
        os.makedirs("saves/")
    cPickle.dump(params, open("saves/almonds_%s.params" % ts, "wb"))
    params.log("Current scene saved!")


def capture(t, params):

    w, h = screen_resolution()

    # Re-adapt dimensions to match current ratio
    old_ratio = 1.0 * w / h
    new_ratio = params.plane_ratio
    if old_ratio > new_ratio:
        w = int(h * new_ratio)
    else:
        h = int(w / new_ratio)

    image = Image.new("RGB", (w, h), "white")
    pixels = image.load()

    palette = PALETTES[params.palette][1]
    if params.reverse_palette:
        palette = palette[::-1]

    coords = [(x, y) for x in xrange(w) for y in xrange(h)]
    threads = []
    chunks = []
    chunk_size = (w * h) / (2 * multiprocessing.cpu_count())
    for i in xrange(0, len(coords), chunk_size):
        chunks.append(coords[i:i + chunk_size])

    n_threads = len(chunks)
    lock = threading.Lock()
    for i in xrange(n_threads):
        threads.append(MBWorker(chunks[i], params, (w, h), t, lock))
    for i in xrange(n_threads):
        threads[i].start()
    for i in xrange(n_threads):
        threads[i].join()
    for i in xrange(n_threads):
        for j in xrange(len(threads[i].coords)):
            c = threads[i].coords[j]
            n = threads[i].results[j]
            pixels[c[0], c[1]] = get_color(n, params.max_iterations, palette)

    params.progress = 0

    if not os.path.exists("captures/"):
        os.makedirs("captures/")

    ts = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d_%H-%M-%S")
    filename = "captures/almonds_%s.png" % ts
    image.save(filename, "PNG")
    params.log("Current scene captured!")
    if n_threads > 1:
        params.log("(Used %d threads)" % n_threads)

    try:
        subprocess.call(["open", filename])
    except OSError:
        pass


def cycle(t, params):
    step = params.max_iterations / 20
    if step == 0:
        step = 1
    for i in xrange(0, params.max_iterations, step):
        params.palette_offset = i
        draw_panel(t, params)
        t.present()
    params.palette_offset = 0


def init_coords(t, params):
    w = t.width() - MENU_WIDTH - 1
    h = t.height() - 1

    params.plane_w = w
    params.plane_h = h
    params.resize(w, h)

    zoom(params, 1)


def main():
    begin = time.time()
    with termbox.Termbox() as t:

        # t.select_output_mode(termbox.OUTPUT_256)

        log = Logger()
        log("$Welcome to Almonds v.%s$" % __version__)

        params = Params(log)

        def load(path):
            import cPickle
            params = cPickle.load(open(path, "rb"))
            params.reload(log)
            if params.dither_type == 2:
                colors.select_output_mode(termbox.OUTPUT_256)
                t.select_output_mode(termbox.OUTPUT_256)
                colors.toggle_bright()
            log("Save loaded!")
            return params

        if len(sys.argv) == 2:
            params = load(sys.argv[1])

        init_coords(t, params)
        update_display(t, params)

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
                        params.plane_y0 -= 1 * params.move_speed
                    elif key == termbox.KEY_ARROW_DOWN:
                        params.plane_y0 += 1 * params.move_speed
                    elif key == termbox.KEY_ARROW_LEFT:
                        params.plane_x0 -= 2 * params.move_speed
                    elif key == termbox.KEY_ARROW_RIGHT:
                        params.plane_x0 += 2 * params.move_speed
                    # Move speed
                    if ch == "c":
                        params.move_speed += 1
                    elif ch == "v":
                        params.move_speed -= 1
                        if params.move_speed == 0:
                            params.move_speed = 1
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
                    elif ch == "d":
                        params.dither_type = (params.dither_type + 1) % len(DITHER_TYPES)
                        if params.dither_type == 2:
                            colors.select_output_mode(termbox.OUTPUT_256)
                            t.select_output_mode(termbox.OUTPUT_256)
                            colors.toggle_bright()
                        else:
                            colors.select_output_mode(termbox.OUTPUT_NORMAL)
                            t.select_output_mode(termbox.OUTPUT_NORMAL)
                    elif ch == "r":
                        params.reverse_palette = not params.reverse_palette
                    # Misc
                    elif ch == "s":
                        save(params)
                    elif ch == "l":
                        if not os.path.exists("saves/"):
                            log("No saved states present")
                        else:
                            options = os.listdir("saves/")
                            menu = OptionMenu(t, options, "Load save")
                            n = menu.show()
                            if n >= 0:
                                params = load("saves/" + options[n])
                            else:
                                log("Load canceled")
                    elif ch == "h":
                        capture(t, params)
                    elif ch == "x":
                        cycle(t, params)

                event = t.peek_event()
            if running:
                update_display(t, params)

    spent = (time.time() - begin) / 60
    print "\nSpent %d minutes exploring fractals, see you soon :)\n" % spent
    print "- Almonds v.%s by Tenchi <tenchi@team2xh.net>\n" % __version__

if __name__ == "__main__":
    main()
