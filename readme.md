# Almonds

Terminal Mandelbrot fractal viewer, using [`termbox`](https://github.com/nsf/termbox) for easy `ncurses` like terminal graphics.

---

### Requisites

You will need to install `termbox`, `PIL` (or `Pillow`), then run:

```
$ python almonds.py
```

On Windows, Almonds only works using [`mintty`](https://mintty.github.io/) ([`babun`](http://babun.github.io/) is recommended)

### Screenshots

<img width="969" alt="screen shot 2015-10-15 at 11 45 05" src="https://cloud.githubusercontent.com/assets/4116708/10510459/742ef26e-7333-11e5-95a0-39eda364be65.png">
<img width="1221" alt="screen shot 2015-10-15 at 11 48 43" src="https://cloud.githubusercontent.com/assets/4116708/10510460/743c1908-7333-11e5-8392-646f3c9b516f.png">

### TODO

- Add progress bar for capture
- Fix capture zoom
- Open menu, displays saved .params files
- GitHub releases (bbfreeze, Py2App)
- Adaptive palette stretching
- Julia mode
- Update screenshots