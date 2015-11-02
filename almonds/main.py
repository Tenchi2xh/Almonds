# -*- encoding: utf-8 -*-

from __future__ import print_function
from __future__ import division

import os
import sys
import multiprocessing
import argparse

from almonds import splash
from almonds import __version__
from almonds import main


def wrap_prolog(func, prolog):
    def wrapped(*args, **kwargs):
        print(prolog)
        func(*args, **kwargs)
    return wrapped


def launch():
    if os.name == "nt" and sys.platform != "cygwin":
        __name__ = "__main__"

    parser = argparse.ArgumentParser(description="version " + __version__, prog="almonds",
                                     formatter_class=lambda prog:
                                     argparse.RawTextHelpFormatter(prog, max_help_position=45))

    parser.add_argument("save", nargs="?", type=str, default=None,
                        help="path of a save to load")
    parser.add_argument("-p", "--processes", type=int, metavar="N",
                        default=multiprocessing.cpu_count(),
                        help="number of concurrent processes")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--char-ratio", type=float,
                       default=0.428, metavar="RATIO",
                       help="width to height ratio of the terminal characters")
    group.add_argument("-d", "--dimensions", type=int, nargs=2,
                       metavar=("W", "H"), help="width and height of the terminal characters")

    parser.add_argument("-z", "--qwertz", action="store_true", default=False,
                        help='swap the "z" and "y" keys')

    parser.print_help = wrap_prolog(parser.print_help, "\n".join(splash))
    parser.print_usage = wrap_prolog(parser.print_usage, "")

    args = parser.parse_args()

    ratio = args.char_ratio
    if args.dimensions is not None:
        ratio = args.dimensions[0] / args.dimensions[1]

    pool = multiprocessing.Pool(args.processes)
    main(pool, ratio, args.qwertz, args.save)


if __name__ == "__main__":
    launch()
