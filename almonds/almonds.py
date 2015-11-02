#!/usr/bin/python
# -*- encoding: utf-8 -*-

from __future__ import print_function
from __future__ import division

import os
import sys
import textwrap
import multiprocessing
import subprocess

from PIL import Image

from .cursebox import *
from .plane import Plane
from .splash import splash
from .graphics.option_menu import *
from .graphics.input_menu import *
from .graphics.splash_popup import *
from .mandelbrot import *
from .logger import *
from .params import *
from .utils import *

__version__ = "1.24b"

MENU_WIDTH = 40


def compute(args):
    x, y, params = args
    """Callable function for the multiprocessing pool."""
    return x, y, mandelbrot(x, y, params)


def compute_capture(args):
    x, y, w, h, params = args
    """Callable function for the multiprocessing pool."""
    return x, y, mandelbrot_capture(x, y, w, h, params)


def draw_panel(cb, pool, params, plane):
    """
    Draws the application's main panel, displaying the current Mandelbrot view.

    :param cb: Cursebox instance.
    :type cb: cursebox.Cursebox
    :param params: Current application parameters.
    :type params: params.Params
    :param plane: Plane containing the current Mandelbrot values.
    :type plane: plane.Plane
    """
    w = cb.width - MENU_WIDTH - 1
    h = cb.height - 1

    params.plane_w = w
    params.plane_h = h
    params.resize(w, h)

    palette = PALETTES[params.palette][1]
    if params.reverse_palette:
        palette = palette[::-1]

    # draw_gradient(t, 1, 1, w, h, palette, params.dither_type)

    generated = 0
    missing_coords = []

    # Check for coordinates that have no value in current plane
    xs = range(params.plane_x0, params.plane_x0 + params.plane_w - 1)
    ys = range(params.plane_y0, params.plane_y0 + params.plane_h - 1)
    for x in xs:
        for y in ys:
            if plane[x, y] is None:
                missing_coords.append((x, y, params))
                generated += 1

    # Compute all missing values via multiprocessing
    n_processes = 0
    if len(missing_coords) > 0:
        n_cores = pool._processes
        n_processes = len(missing_coords) // 256
        if n_processes > n_cores:
            n_processes = n_cores

        start = time.time()
        for i, result in enumerate(pool.imap_unordered(compute, missing_coords, chunksize=256)):
            plane[result[0], result[1]] = result[2]
            if time.time() - start > 2:
                if i % 200 == 0:
                    draw_progress_bar(cb, "Render is taking a longer time...", i, len(missing_coords))
                    cb.refresh()

    if generated > 0:
        params.log("Added %d missing cells" % generated)
        if n_processes > 1:
            params.log("(Used %d processes)" % n_processes)

    min_value = 0.0
    max_value = params.max_iterations
    max_iterations = params.max_iterations

    if params.adaptive_palette:
        min_value, max_value = plane.extrema(params.plane_x0, params.plane_y0,
                                             params.plane_w, params.plane_h)

    crosshairs_coord = None
    if params.crosshairs:
        crosshairs_coord = params.crosshairs_coord

    # Draw all values in cursebox
    for x in xs:
        for y in ys:
            value = (plane[x, y] + params.palette_offset) % (params.max_iterations + 1)
            if params.adaptive_palette:
                # Remap values from (min_value, max_value) to (0, max_iterations)
                if max_value - min_value > 0:
                    value = ((value - min_value) / (max_value - min_value)) * max_iterations
                else:
                    value = max_iterations

            # Dithered mode
            if params.dither_type < 2:
                draw_dithered_color(cb, x - params.plane_x0 + 1,
                                           y - params.plane_y0 + 1,
                                           palette, params.dither_type,
                                           value, max_iterations,
                                           crosshairs_coord=crosshairs_coord)
            # 256 colors mode
            else:
                draw_color(cb, x - params.plane_x0 + 1,
                              y - params.plane_y0 + 1,
                              value, max_iterations, palette,
                              crosshairs_coord=crosshairs_coord)

    # Draw bounding box
    draw_box(cb, 0, 0, w + 1, h + 1)


def draw_menu(cb, params, qwertz):
    """
    Draws the application's side menu and options.

    :param cb: Cursebox instance.
    :type cb: cursebox.Cursebox
    :param params: Current application parameters.
    :type params: params.Params
    """
    w = cb.width
    h = cb.height

    x0 = w - MENU_WIDTH + 1

    # Clear buffer inside the box
    fill(cb, x0, 1, MENU_WIDTH, h - 2, " ")

    def draw_option(key, value, shortcuts):
        """
        Helper function to draw options. Self-increments own counter.

        :param key: Name of the option.
        :param value: Value of the option.
        :param shortcuts: Keyboard shortcut keys.
        :return:
        """
        draw_text(cb, x0 + 1, 2 + draw_option.counter,
                  "%s %s %s" % (key, str(value).rjust(MENU_WIDTH - 14 - len(key)), shortcuts))
        draw_option.counter += 1
    draw_option.counter = 1

    z = "Z"
    y = "Y"
    if qwertz:
        z, y = y, z

    h_seps = [2]
    # Draw title
    draw_text(cb, x0, 1, ("Almonds %s" % __version__).center(MENU_WIDTH - 2))
    # Write options (and stats)
    # Mandelbrot position
    draw_option("Real", "{0:.13g}".format(params.mb_cx),
                "$[" + symbols["ARROW_LEFT"] + "]$, $[" + symbols["ARROW_RIGHT"] + "]$")
    draw_option("Imaginary", "{0:.13g}".format(params.mb_cy),
                "$[" + symbols["ARROW_UP"] + "]$, $[" + symbols["ARROW_DOWN"] + "]$")
    # FIXME: try to find a way to avoid this hack
    if is_native_windows():
        cb.put_arrow(x0 + 30, 3, "up", colors.default_bg(), colors.default_fg())
        cb.put_arrow(x0 + 35, 3, "down", colors.default_bg(), colors.default_fg())
        cb.put_arrow(x0 + 30, 4, "left", colors.default_bg(), colors.default_fg())
        cb.put_arrow(x0 + 35, 4, "right", colors.default_bg(), colors.default_fg())
    draw_option("Input coordinates...", "", "$[Enter]$")
    draw_option.counter += 1
    h_seps.append(draw_option.counter + 1)
    # Mandelbrot options
    draw_option("Move speed", params.move_speed, "$[C]$, $[V]$")
    draw_option("Zoom", "{0:.13g}".format(params.zoom), "$[" + y + "]$, $[U]$")
    draw_option("Iterations", params.max_iterations, "$[I]$, $[O]$")
    draw_option("Julia mode", "On" if params.julia else "Off", "$[J]$")
    draw_option.counter += 1
    h_seps.append(draw_option.counter + 1)
    # Palette options
    draw_option("Palette", PALETTES[params.palette][0], "$[P]$")
    draw_option("Color mode", DITHER_TYPES[params.dither_type][0], "$[D]$")
    draw_option("Order", "Reversed" if params.reverse_palette else "Normal", "$[R]$")
    draw_option("Mode", "Adaptive" if params.adaptive_palette else "Linear", "$[A]$")
    draw_option("Cycle!", "", "$[" + z + "]$")
    draw_option.counter += 1
    h_seps.append(draw_option.counter + 1)
    # Misc.
    draw_option("Hi-res capture", "", "$[H]$")
    draw_option("Crosshairs", "On" if params.crosshairs else "Off", "$[X]$")
    draw_option("Theme", "Dark" if colors.dark else "Light", "$[T]$")
    draw_option("Save", "", "$[S]$")
    draw_option("Load...", "", "$[L]$")
    draw_option("Exit", "", "$[ESC]$")

    # Draw box with separators
    middle = 3 + draw_option.counter
    draw_box(cb, w - MENU_WIDTH, 0, MENU_WIDTH, h, h_seps=h_seps + [middle - 1, middle + 1])

    # Draw log
    draw_text(cb, x0, middle, "Event log".center(MENU_WIDTH - 2))
    latest_logs = params.log.get_latest(h - middle)
    latest_logs = [textwrap.wrap(l, MENU_WIDTH - 4)[::-1] for l in latest_logs]  # Wrap all messages
    latest_logs = [l for ls in latest_logs for l in ls]                          # Flatten [[str]] -> [str]
    i = h - 2
    for l in latest_logs:
        draw_text(cb, x0 + 1, i, l)
        i -= 1
        if i == middle + 1:
            break


def update_display(cb, pool, params, plane, qwertz):
    """
    Draws everything.

    :param cb: Cursebox instance.
    :type cb: cursebox.Cursebox
    :param params: Current application parameters.
    :type params: params.Params
    :param plane: Plane containing the current Mandelbrot values.
    :type plane: plane.Plane
    :return:
    """
    cb.clear()
    draw_panel(cb, pool, params, plane)
    update_position(params)  # Update Mandelbrot-space coordinates before drawing them
    draw_menu(cb, params, qwertz)
    cb.refresh()


def save(params):
    """
    Saves the current parameters to a file.

    :param params: Current application parameters.
    :return:
    """
    if is_python3():
        import pickle
        cPickle = pickle
    else:
        import cPickle
    ts = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d_%H-%M-%S")
    if not os.path.exists("saves/"):
        os.makedirs("saves/")
    with open("saves/almonds_%s.params" % ts, "wb") as f:
        cPickle.dump(params, f)
        params.log("Current scene saved!")


def capture(cb, pool, params):
    """
    Renders and saves a screen-sized picture of the current position.

    :param cb: Cursebox instance.
    :type cb: cursebox.Cursebox
    :param params: Current application parameters.
    :type params: params.Params
    """
    w, h = screen_resolution()

    # Re-adapt dimensions to match current plane ratio
    old_ratio = w / h
    new_ratio = params.plane_ratio
    if old_ratio > new_ratio:
        w = int(h * new_ratio)
    else:
        h = int(w / new_ratio)

    image = Image.new("RGB", (w, h), "white")
    pixels = image.load()

    # FIXME: refactor common code to get_palette(params)
    palette = PALETTES[params.palette][1]
    if params.reverse_palette:
        palette = palette[::-1]

    # All coordinates to be computed as single arguments for processes
    coords = [(x, y, w, h, params) for x in range(w) for y in range(h)]

    results = []
    # Dispatch work to pool and draw results as they come in
    for i, result in enumerate(pool.imap_unordered(compute_capture, coords, chunksize=256)):
        results.append(result)
        if i % 2000 == 0:
            draw_progress_bar(cb, "Capturing current scene...", i, w * h)
            cb.refresh()

    min_value = 0.0
    max_value = params.max_iterations
    max_iterations = params.max_iterations

    if params.adaptive_palette:
        from operator import itemgetter
        min_value = min(results, key=itemgetter(2))[2]
        max_value = max(results, key=itemgetter(2))[2]

    # Draw pixels
    for result in results:
        value = result[2]
        if params.adaptive_palette:
            # Remap values from (min_value, max_value) to (0, max_iterations)
            if max_value - min_value > 0:
                value = ((value - min_value) / (max_value - min_value)) * max_iterations
            else:
                value = max_iterations
        pixels[result[0], result[1]] = get_color(value, params.max_iterations, palette)

    if not os.path.exists("captures/"):
        os.makedirs("captures/")

    ts = datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d_%H-%M-%S")
    filename = "captures/almonds_%s.png" % ts
    image.save(filename, "PNG")
    params.log("Current scene captured!")
    params.log("(Used %d processes)" % pool._processes)

    open_file(filename)


def cycle(cb, pool, params, plane):
    """
    Fun function to do a palette cycling animation.

    :param cb: Cursebox instance.
    :type cb: cursebox.Cursebox
    :param params: Current application parameters.
    :type params: params.Params
    :param plane: Plane containing the current Mandelbrot values.
    :type plane: plane.Plane
    :return:
    """
    step = params.max_iterations // 20
    if step == 0:
        step = 1
    for i in range(0, params.max_iterations, step):
        params.palette_offset = i
        draw_panel(cb, pool, params, plane)
        cb.refresh()
    params.palette_offset = 0


def init_coords(cb, params):
    """
    Initializes coordinates and zoom for first use.

    Loads coordinates from Mandelbrot-space.

    :param cb: Cursebox instance.
    :type cb: cursebox.Cursebox
    :param params: Current application parameters.
    :type params: params.Params
    :return:
    """
    w = cb.width - MENU_WIDTH - 1
    h = cb.height - 1

    params.plane_w = w
    params.plane_h = h
    params.resize(w, h)

    zoom(params, 1)


def main(pool, ratio, qwertz, savefile):
    begin = time.time()
    with Cursebox() as cb:

        log = Logger()
        log("Welcome to Almonds %s" % __version__)
        log("Exit with $[ESC]$")
        log("or $[CTRL]$ + $[C]$")

        params = Params(log, ratio)
        plane = Plane()

        def load(path):
            if is_python3():
                import pickle
                cPickle = pickle
            else:
                import cPickle

            with open(path, "rb") as f:
                params = cPickle.load(f)
                params.log = log
                log("Save loaded!")
                return params

        if savefile is not None:
            params = load(savefile)

        popup = SplashPopup(cb, "\n".join(splash), box=True)
        popup.show()

        init_coords(cb, params)
        update_display(cb, pool, params, plane, qwertz)

        running = True
        while running:
            event = cb.poll_event().upper()

            if event == EVENT_RESIZE:
                plane.reset()
            elif event in (EVENT_ESC, EVENT_CTRL_C):
                running = False
            # Navigation
            elif event == EVENT_UP:
                params.plane_y0 -= 1 * params.move_speed
            elif event == EVENT_DOWN:
                params.plane_y0 += 1 * params.move_speed
            elif event == EVENT_LEFT:
                params.plane_x0 -= int(2 * params.move_speed)
            elif event == EVENT_RIGHT:
                params.plane_x0 += int(2 * params.move_speed)
            # Move speed
            elif event == "C":
                params.move_speed += 1
            elif event == "V":
                params.move_speed -= 1
                if params.move_speed == 0:
                    params.move_speed = 1
            # Manual input
            elif event == EVENT_ENTER:
                menu = InputMenu(cb, ["* Real (X)", "* Imaginary (Y)", "  Zoom", "  Iterations"],
                                 "Input manual coordinates")
                r, values = menu.show()
                if r >= 0:
                    try:
                        new_mb_cx = float(values[0])
                        new_mb_cy = float(values[1])
                        new_zoom = params.zoom
                        new_iterations = params.max_iterations
                        try:
                            new_zoom = float(values[2])
                            new_iterations = int(values[3])
                        except ValueError:
                            pass
                        params.mb_cx = new_mb_cx
                        params.mb_cy = new_mb_cy
                        params.zoom = new_zoom
                        params.max_iterations = new_iterations
                        init_coords(cb, params)
                        plane.reset()
                    except ValueError:
                        params.log("Given coordinates are not floating numbers")
                else:
                    params.log("Manual input canceled")
            # Zoom / un-zoom
            elif (qwertz and event == "Z") or (not qwertz and event == "Y"):
                zoom(params, 1.3)
                plane.reset()
            elif event == "U":
                zoom(params, 1 / 1.3)
                plane.reset()
            # Iterations control
            elif event == "I":
                params.max_iterations += 10
                plane.reset()
            elif event == "O":
                params.max_iterations -= 10
                if params.max_iterations <= 0:
                    params.max_iterations = 10
                else:
                    plane.reset()
            # Palette swap
            elif event == "P":
                params.palette = (params.palette + 1) % len(PALETTES)
            elif event == "D":
                params.dither_type = (params.dither_type + 1) % len(DITHER_TYPES)
            elif event == "R":
                params.reverse_palette = not params.reverse_palette
            # Misc
            elif event == "S":
                save(params)
            elif event == "L":
                if not os.path.exists("saves/"):
                    log("No saved states present")
                else:
                    options = os.listdir("saves/")
                    menu = OptionMenu(cb, options, "Load save")
                    n = menu.show()
                    if n >= 0:
                        params = load("saves/" + options[n])
                        init_coords(cb, params)
                        plane.reset()
                    else:
                        log("Load canceled")
            elif event == "H":
                capture(cb, pool, params)
            elif (qwertz and event == "Y") or (not qwertz and event == "Z"):
                cycle(cb, pool, params, plane)
            elif event == "T":
                colors.toggle_dark()
            elif event == "A":
                params.adaptive_palette = not params.adaptive_palette
            elif event == "J":
                params.toggle_julia()
                init_coords(cb, params)
                plane.reset()
            elif event == "X":
                params.crosshairs = not params.crosshairs

            if running:
                update_display(cb, pool, params, plane, qwertz)

    spent = (time.time() - begin) // 60
    spaces = " " * 26
    if not(is_native_windows()):
        print("\n".join(splash))
    else:
        spaces = ""
        print()
    print("%s%d minute%s exploring fractals, see you soon :)\n" % (spaces, spent, "s" if spent > 1 else ""))
    print("%s- Almonds %s by Tenchi <tenchi@team2xh.net>" % (spaces, __version__))
