# -*- encoding: utf-8 -*-

from textwrap import dedent

from ..graphics.drawing import *
from .fake_terminal import CurseBox


def test_sort_palette():
    palette = [colors.white, colors.black, colors.blue, colors.cyan]
    sorted_palette = sort_palette(palette)

    assert sorted_palette == [colors.black, colors.blue, colors.cyan, colors.white]


def test_dither_symbol():
    values = [0.00, 0.25, 0.50, 0.75, 1.00]
    chars = [dither_symbol(value, 0) for value in values]

    for i, char in enumerate(chars):
        assert char == symbols.dither1[i]


def test_draw_box():
    cb = CurseBox(15, 5)
    draw_box(cb, 0, 0, cb.width, cb.height, v_seps=[7])
    expected = dedent(u"""
        ┌──────┬──────┐
        │      │      │
        │      │      │
        │      │      │
        └──────┴──────┘
        """)[1:]

    assert expected == cb.get_screen()[0]


def test_draw_text():
    cb = CurseBox(13, 1)
    draw_text(cb, 0, 0, "Hello, $World$!")
    expected_chars = "Hello, World!\n"

    cn = (colors.default_fg(), colors.default_bg())
    ci = cn[::-1]
    expected_colors = [[cn] * 7 + [ci] * 5 + [cn]]
    result_chars, result_colors = cb.get_screen()

    assert expected_chars == result_chars
    assert expected_colors == result_colors


def test_fill():
    cb = CurseBox(10, 5)
    draw_box(cb, 0, 0, 10, 5)
    fill(cb, 1, 1, 9, 3, "#")
    expected = dedent(u"""
        ┌────────┐
        │########│
        │########│
        │########│
        └────────┘
        """)[1:]
    assert expected == cb.get_screen()[0]


def test_interpolate():
    c1 = (255, 0, 0)
    c2 = (0, 0, 255)
    c3 = interpolate(c1, c2, 0.5)
    assert c3 == (127, 0, 127)
