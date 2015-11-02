<p align="center"><img width="720" alt="logo" src="misc/logo/logo.png"></p>
<p align="right">
  <a href="https://www.codacy.com/app/Tenchi2xh/Almonds">
    <img height=27 alt="Codacy" src="https://img.shields.io/codacy/3b8d442e099546ec838aa44a2f9a5d23.svg">
  </a>
  <a href="https://travis-ci.org/Tenchi2xh/Almonds">
    <img height=27 alt="Travis-CI" src="https://img.shields.io/travis/Tenchi2xh/Almonds.svg">
  </a>
  <a href="https://github.com/Tenchi2xh/Almonds/releases/tag/1.22b">
    <img height=27 alt="Version" src="https://img.shields.io/badge/version-1.22b-blue.svg">
  </a>
</p>

---

- [Features](#features)
- [Running](#running)
- [Controls](#controls)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Renders](#renders)

---

### Features

- Fully fledged Mandelbrot viewer, in your terminal
- *Now compatible with the native Windows console!*
- Julia sets
- Homemade terminal UI
- 8 color ANSI mode with dithering
- 256 color mode
- Parallelized using `multiprocessing`
- Multiple palettes, adaptive mode
- Save and load capabilities
- Available in standalone, source compatible with Python 2 & 3
- Infinite fun from the comfort of your terminal

### Running

On OS X, Linux and Cygwin:

```
$ pip install Pillow
$ python main.py
```

(For Cygwin, [`mintty`](https://mintty.github.io/) or [`babun`](http://babun.github.io/) are recommended)

On Windows, download the `curses` module from the [Unofficial Windows Binaries for Python Extension Packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses) (a `curses` implementation for Windows based on [PDCurses](http://pdcurses.sourceforge.net/)), then run:

```
> pip install curses‑2.2‑cp27‑none‑win32.whl
> pip install Pillow
> python main.py
```

The font [Envy Code R](https://damieng.com/blog/2008/05/26/envy-code-r-preview-7-coding-font-released) is *highly* recommended. If your terminal emulator supports it, try to reduce the line spacing so that the box drawing characters touch. When using another font, the appearance of the fractal may seem squashed because the width to height ratio of the character are different; try to adjust it using the argument `--ratio` (see [Usage](#usage)).

Using PyPy will make the hi-res captures faster, but the terminal navigation slower.

### Usage

<pre>
                                                                             
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

</pre>

### Controls

Keys | Action
:---:|:------
<kbd>↑</kbd>, <kbd>↓</kbd>, <kbd>←</kbd>, <kbd>→</kbd> | Move around
<kbd>C</kbd>, <kbd>V</kbd> | Adjust move speed
<kbd>⏎</kbd> | Input manual coordinates
<kbd>Y</kbd>, <kbd>U</kbd> | Zoom / Un-zoom
<kbd>I</kbd>, <kbd>O</kbd> | Increase / Decrase number of iterations
<kbd>J</kbd> | Enter / Leave Julia set 
<kbd>P</kbd> | Next palette
<kbd>D</kbd> | Color mode (256 colors / 8 colors ANSI / 8 colors ASCII)
<kbd>R</kbd> | Reverse palette order
<kbd>A</kbd> | Palette mode (Normal / Adaptive)
<kbd>Z</kbd> | Launch palette cycling animation
<kbd>H</kbd> | Capture current view in a high-resolution PNG file
<kbd>X</kbd> | Show / Hide crosshairs
<kbd>T</kbd> | Toggle UI theme (Dark / Light)
<kbd>S</kbd> | Save all current settings and view
<kbd>L</kbd> | Load a previous save
<kbd>ESC</kbd>, <kbd>CTRL</kbd>+<kbd>C</kbd> | Exit

### Screenshots

<img width="1053" alt="screen shot 2015-10-28 at 21 51 50" src="https://cloud.githubusercontent.com/assets/4116708/10803277/adec2722-7dc1-11e5-9599-a5e90bead5d8.png">
<p align="center"><i>Mandelbrot in your terminal, now in 256 colors!</i></p>
<br/><br/>

<img width="1053" alt="screen shot 2015-10-28 at 21 56 13" src="https://cloud.githubusercontent.com/assets/4116708/10803276/ade76bce-7dc1-11e5-9b98-649215f1c56b.png">
<p align="center"><i>Rendering a capture with the editor's light theme and 8-color dithered ANSI mode.</i></p>
<br/><br/>

<img width="1053" alt="screen shot 2015-10-28 at 22 06 42" src="https://cloud.githubusercontent.com/assets/4116708/10803279/aded968e-7dc1-11e5-8aed-cf61473a8d66.png">
<p align="center"><i>Almonds in Julia mode. The load menu sports a very sophisticated scrollbar.</i></p>
<br/><br/>

<img width="1053" alt="screen shot 2015-10-28 at 22 02 26" src="https://cloud.githubusercontent.com/assets/4116708/10803278/adec2556-7dc1-11e5-8f0d-50975b6ac718.png">
<p align="center"><i>Discovering a mini-brot. At this level of deep zoom, the adaptive palette mode is very handy.</i></p>
<br/>

<br/>
<img width="971" alt="screen shot 2015-10-30 at 13 18 45" src="https://cloud.githubusercontent.com/assets/4116708/10845542/f0f0cc2e-7f08-11e5-8b1e-a1cda696c1cb.png">
<br/><p align="center"><i>Now running in native Windows terminals!</i> (Notice the stretching because the default terminal font for windows is 8 by 12 pixels, try running with `-d 8 12` for a perfect display)</p> 
<br/>


### Renders

![almonds_2015-10-18_02-11-52](https://cloud.githubusercontent.com/assets/4116708/10803285/b5b03b9c-7dc1-11e5-81a0-2e16503322f6.png)

![almonds_2015-10-17_16-47-52](https://cloud.githubusercontent.com/assets/4116708/10803283/b58b99fe-7dc1-11e5-83c3-ef991ba7d0dc.png)

![almonds_2015-10-28_22-08-20](https://cloud.githubusercontent.com/assets/4116708/10803284/b5a21fee-7dc1-11e5-93ee-f36621fa8544.png)

![almonds_2015-10-28_19-49-27](https://cloud.githubusercontent.com/assets/4116708/10803286/b5b24aae-7dc1-11e5-88df-ed751518dcd0.png)

![almonds_2015-10-18_01-51-37](https://cloud.githubusercontent.com/assets/4116708/10803287/b5b50f1e-7dc1-11e5-8c8b-76953178efcc.png)

### TODO

- Finish documenting
- Separate options in two tabs ?
- Press <kbd>SPACE</kbd> to hide log
- New project idea: full-fledged python module for making `cursebox` UI applications
- PyPI package
