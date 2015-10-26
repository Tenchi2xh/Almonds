# Almonds

Terminal Mandelbrot fractal viewer, using [`termbox`](https://github.com/nsf/termbox) for easy `ncurses` like terminal graphics.

---

### Requisites

You will need to install `termbox`, `PIL` (or `Pillow`), then run:

```
$ python almonds.py
```

On Windows, Almonds only works using [`mintty`](https://mintty.github.io/) ([`babun`](http://babun.github.io/) is recommended)

The font [Envy Code R](https://damieng.com/blog/2008/05/26/envy-code-r-preview-7-coding-font-released) is *highly* recommended. If your terminal emulator supports it, try to reduce the line spacing so that the box drawing characters touch. When using another font, if the appearance of the fractal seems squashed, try to adjust the constant `CHAR_RATIO` in `params.py`.

Using PyPy will make the hi-res captures faster, but the terminal navigation slower.

### Screenshots

<img width="1032" alt="screen shot 2015-10-15 at 21 12 23" src="https://cloud.githubusercontent.com/assets/4116708/10524783/9a51d0a8-7381-11e5-9847-d53ca0e74f6d.png">
<img width="1550" alt="screen shot 2015-10-15 at 21 03 37" src="https://cloud.githubusercontent.com/assets/4116708/10524786/9d8526b2-7381-11e5-9d20-a376b3e7343c.png">
![almonds_2015-10-15_21-03-40](https://cloud.githubusercontent.com/assets/4116708/10524793/a68abb82-7381-11e5-9bae-bd9768582c27.png)
<img width="1004" alt="screen shot 2015-10-15 at 21 11 35" src="https://cloud.githubusercontent.com/assets/4116708/10524803/adc880e6-7381-11e5-9ef8-f6af71f67f0e.png">
![almonds_2015-10-15_21-11-44](https://cloud.githubusercontent.com/assets/4116708/10524807/b2928018-7381-11e5-9120-d6af6efb839e.png)

### TODO

- GitHub releases (bbfreeze, Py2App)
- Julia mode
- Document everything (graphics package missing)
- Two tabs for stats/options
- Project idea: full-fledged module for `termbox` UI elements
- Space to hide log
- Margins ? (with rounding, notches will look uneven)
