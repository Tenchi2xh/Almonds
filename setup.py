# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

from almonds import __version__

setup(
    name="almonds",
    packages=find_packages(),
    version=__version__,
    description="Terminal fractal viewer",
    author="Tenchi",
    author_email="tenkage@gmail.com",
    url="https://github.com/Tenchi2xh/Almonds",
    download_url="https://github.com/Tenchi2xh/Almonds/tarball/" + __version__,
    keywords=["fractal", "mandelbrot", "terminal", "termbox", "curses"],
    classifiers=[
        "Development Status :: 4 - Beta",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    install_requires=["Pillow"],
    extras_require={
        "test": ["pytest"]
    },
    entry_points={
        "console_scripts": [
            "almonds = almonds.main:launch"
        ]
    }
)
