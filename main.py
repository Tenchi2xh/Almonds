# -*- encoding: utf-8 -*-

import multiprocessing

from almonds import main

if __name__ == "__main__":
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    main(p)
