#!/bin/bash

rmvirtualenv --no-site-packages landbank
mkvirtualenv --no-site-packages landbank
workon landbank
pip install numpy
pip install scipy
pip install matplotlib
pip install --no-install gdal
cd $WORKON_HOME/landbank/build/gdal
python setup.py build_ext --include-dirs=/usr/include/gdal
pip install --no-download gdal
cd -
pip install ipython
pip install scikit-learn
pip install pandas

