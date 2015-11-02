.. image:: https://github.com/Tenchi2xh/Almonds/raw/master/misc/logo/logo.png
   :align: center

.. image:: https://img.shields.io/pypi/v/almonds.svg
   :align: right
   :target: https://pypi.python.org/pypi?:action=display&name=almond

.. image:: https://img.shields.io/codacy/3b8d442e099546ec838aa44a2f9a5d23.svg
   :align: right
   :target: https://www.codacy.com/app/Tenchi2xh/Almonds

.. image:: https://img.shields.io/travis/Tenchi2xh/Almonds.svg
   :align: right
   :target: https://travis-ci.org/Tenchi2xh/Almonds

.. image:: https://img.shields.io/badge/tag-1.25b-blue.svg
   :align: right
   :target: https://github.com/Tenchi2xh/Almonds/releases/tag/1.25b

Features
========

-  Fully fledged Mandelbrot viewer, in your terminal
-  *Now compatible with the native Windows console!*
-  Julia sets
-  Homemade terminal UI
-  8 color ANSI mode with dithering
-  256 color mode
-  Parallelized using ``multiprocessing``
-  Multiple palettes, adaptive mode
-  Save and load capabilities
-  Available in standalone, source compatible with Python 2 & 3
-  Infinite fun from the comfort of your terminal

Running
=======

Using PIP
---------

Just run:

::

    $ pip install almonds
    $ almonds

On non-Cygwin Windows, you will still have to install the unofficial
``curses`` module (see "From source" below)

From source
-----------

Clone the repo:

::

    $ git clone https://github.com/Tenchi2xh/Almonds.git
    $ cd Almonds

On OS X, Linux and Cygwin:

::

    $ pip install Pillow
    $ python -m almonds.main

(For Cygwin, `mintty <https://mintty.github.io/>`__ or
`babun <http://babun.github.io/>`__ are recommended)

On Windows, download the ``curses`` module from the `Unofficial Windows
Binaries for Python Extension
Packages <http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses>`__ (a
``curses`` implementation for Windows based on
`PDCurses <http://pdcurses.sourceforge.net/>`__), then run:

::

    > pip install curses‑2.2‑cp27‑none‑win32.whl
    > pip install Pillow
    > python -m almonds.main

The font `Envy Code
R <https://damieng.com/blog/2008/05/26/envy-code-r-preview-7-coding-font-released>`__
is *highly* recommended. If your terminal emulator supports it, try to
reduce the line spacing so that the box drawing characters touch. When
using another font, the appearance of the fractal may seem squashed
because the width to height ratio of the character are different; try to
adjust it using the argument ``--ratio`` (see "Usage" below).

Using PyPy will make the hi-res captures faster, but the terminal
navigation slower.

Usage
=====

::
                                                                                
                   ██                                                           
             ██  ██████  ██   .d8b.  db                              db         
               ██████████    d8' `8b 88 .88b  d88. .d88b. .888b  .d8888 .d8888  
         ██  ██████████████  88ooo88 88 88  88  88 8P  Y8 88  88 88  88 `8bo.   
     ████████████████████    88   88 88 88  88  88 8b  d8 88  88 88  8D   `Y8b  
         ██  ██████████████  YP   YP YP YP  YP  YP `Y88P' VP  VP Y888D' `8888Y  
               ██████████                                                       
             ██  ██████  ██    T e r m i n a l   f r a c t a l   v i e w e r    
                   ██                                                           
                                                                                
   usage: almonds [-h] [-p N] [-r RATIO | -d W H] [-z] [save]

   version 1.20b

   positional arguments:
     save                          path of a save to load

   optional arguments:
     -h, --help                    show this help message and exit
     -p N, --processes N           number of concurrent processes
     -r RATIO, --char-ratio RATIO  width to height ratio of the terminal characters
     -d W H, --dimensions W H      width and height of the terminal characters
     -z, --qwertz                  swap the "z" and "y" keys


Controls
========

+----------------------------+------------------------------------------------------------+
| Keys                       | Action                                                     |
+============================+============================================================+
| ``↑``, ``↓``, ``←``, ``→`` | Move around                                                |
+----------------------------+------------------------------------------------------------+
| ``C``, ``V``               | Adjust move speed                                          |
+----------------------------+------------------------------------------------------------+
| ``⏎``                      | Input manual coordinates                                   |
+----------------------------+------------------------------------------------------------+
| ``Y``, ``U``               | Zoom / Un-zoom                                             |
+----------------------------+------------------------------------------------------------+
| ``I``, ``O``               | Increase / Decrase number of iterations                    |
+----------------------------+------------------------------------------------------------+
| ``J``                      | Enter / Leave Julia set                                    |
+----------------------------+------------------------------------------------------------+
| ``P``                      | Next palette                                               |
+----------------------------+------------------------------------------------------------+
| ``D``                      | Color mode (256 colors / 8 colors ANSI / 8 colors ASCII)   |
+----------------------------+------------------------------------------------------------+
| ``R``                      | Reverse palette order                                      |
+----------------------------+------------------------------------------------------------+
| ``A``                      | Palette mode (Normal / Adaptive)                           |
+----------------------------+------------------------------------------------------------+
| ``Z``                      | Launch palette cycling animation                           |
+----------------------------+------------------------------------------------------------+
| ``H``                      | Capture current view in a high-resolution PNG file         |
+----------------------------+------------------------------------------------------------+
| ``X``                      | Show / Hide crosshairs                                     |
+----------------------------+------------------------------------------------------------+
| ``T``                      | Toggle UI theme (Dark / Light)                             |
+----------------------------+------------------------------------------------------------+
| ``S``                      | Save all current settings and view                         |
+----------------------------+------------------------------------------------------------+
| ``L``                      | Load a previous save                                       |
+----------------------------+------------------------------------------------------------+
| ``ESC``, ``CTRL``+``C``    | Exit                                                       |
+----------------------------+------------------------------------------------------------+

Screenshots & Renders
=====================

See on the `GitHub Project Page <https://github.com/Tenchi2xh/Almonds#screenshots>`__
