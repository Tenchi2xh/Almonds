# -*- encoding: utf-8 -*-

from ..utils import *


def test_clamp():
    assert clamp(   0,   42, 1337) == 42    # n < lower
    assert clamp( 386,   42, 1337) == 386   # lower < n < upper
    assert clamp(9000,   42, 1337) == 1337  # upper < n
    assert clamp(9000, 1337,   42) == 1337  # lower > upper
