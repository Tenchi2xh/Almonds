# -*- encoding: utf-8 -*-

from .cursebox import symbols

b = lambda n: tuple([symbols.dither1[0] * 2] * n)
splash = ["                                                                             ",
          "                %s                                                           " % b(1),
          "          %s  %s%s%s  %s   .d8b.  db                              db         " % b(5),
          "            %s%s%s%s%s    d8' `8b 88 .88b  d88. .d88b. .888b  .d8888 .d8888  " % b(5),
          "      %s  %s%s%s%s%s%s%s  88ooo88 88 88  88  88 8P  Y8 88  88 88  88 `8bo.   " % b(8),
          "  %s%s%s%s%s%s%s%s%s%s    88   88 88 88  88  88 8b  d8 88  88 88  8D   `Y8b  " % b(10),
          "      %s  %s%s%s%s%s%s%s  YP   YP YP YP  YP  YP `Y88P' VP  VP Y888D' `8888Y  " % b(8),
          "            %s%s%s%s%s                                                       " % b(5),
          "          %s  %s%s%s  %s    T e r m i n a l   f r a c t a l   v i e w e r    " % b(5),
          "                %s                                                           " % b(1),
          "                                                                             "]
