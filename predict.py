# -*- coding: utf-8 -*-

"""Predict output script.

"""

# Author: Mo Frank Hu (mofrankhu@gmail.com)
# Dependency: Python 3, pandas
import pandas as pd

def main():
    from subprocess import call
    for dist in range (1, 67):
        call(['python', 'split-sets.py', str(dist)])
main()

