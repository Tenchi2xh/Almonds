# -*- encoding: utf-8 -*-

import pytest

from ..utils import range
from ..plane import Plane


def test_empty():
    plane = Plane()

    assert plane[0, 0] is None
    assert plane[-42, -42] is None


def test_filler():
    filler = "Empty"
    plane = Plane(filler=filler)

    assert plane[0, 0] == filler
    assert plane[1337, 1337] == filler


def test_add():
    plane = Plane()

    assert plane[13, 37] is None
    plane[13, 37] = "foo"
    assert plane[13, 37] == "foo"


def test_reset():
    plane = Plane()

    plane[13, 37] = "foo"
    assert plane[13, 37] == "foo"
    plane.reset()
    assert plane[13, 37] is None


def test_extrema():
    plane = Plane()

    i = -1337
    for x in range(-100, 100):
        for y in range(-100, 100):
            plane[x, y] = i
            i += 3

    minimum, maximum = plane.extrema(-100, -100, 200, 200)

    assert minimum == -1337
    assert maximum == i - 3


def test_index_type():
    plane = Plane()

    with pytest.raises(AssertionError) as excinfo:
        plane["1", 2] = "foo"

    with pytest.raises(AssertionError) as excinfo:
        _ = plane["1", 2]
