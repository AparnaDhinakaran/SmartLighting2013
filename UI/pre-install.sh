#!/bin/bash

# Install python modules (tkinter, numpy, scipy, matplotlib, pandas, sqlite3, pip, setuptools
sudo apt-get install python python-tk idle python-pmw python-imaging python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose python-pip python-setuptools sqlite3 python-imaging-tk

# Install patsy
sudo pip install --upgrade patsy

# Install pandas version 0.7.1
sudo easy_install pandas==0.7.1

# Install statsmodels
sudo easy_install -U statsmodels
