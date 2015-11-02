# -*- encoding: utf-8 -*-

import pytest

from ..logger import *
from ..utils import range


def test_empty():
    log = Logger()
    with pytest.raises(IndexError) as excinfo:
        _ = log[0]


def test_log():
    log = Logger()
    for i in range(100):
        log(i)
        assert log[i].split(" ")[1] == str(i)


def test_get_latest():
    log = Logger()
    for i in range(100):
        log(i)

    assert len(log.get_latest(10)) == 10
    assert log.get_latest(10)[0].split(" ")[1] == str(99)
