# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

def get_version(relpath):
  """Read version info from a file without importing it"""
  from os.path import dirname, join
  root = dirname(__file__)
  for line in open(join(root, relpath), "rb"):
    # encoding is not passed to open() parameter, because
    # it is incompatible with Python 2
    line = line.decode("utf-8")
    if "__version__" in line:
      if '"' in line:
        return line.split('"')[1]
VERSION = get_version("almonds/almonds.py")

readme_file = open("readme_pypi.rst", "r")
README = readme_file.read()
readme_file.close()

setup(
    name="almonds",
    packages=find_packages(),
    version=VERSION,
    description="Terminal fractal viewer",
    long_description=README,
    author="Tenchi",
    author_email="tenkage@gmail.com",
    url="https://github.com/Tenchi2xh/Almonds",
    download_url="https://github.com/Tenchi2xh/Almonds/tarball/" + VERSION,
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
