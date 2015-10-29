#! /bin/sh

pip install pyinstaller
pyinstaller -c -F almonds.py
ALMONDS_VERSION=`python -c "from almonds import __version__; print __version__"`
cd "dist/"
zip "almonds-${ALMONDS_VERSION}-osx.zip" almonds
cd ..
