# -*- coding: utf-8 -*-

"""MAPE scorer for sklearn.

"""

# Author: Mo Frank Hu (mofrankhu@gmail.com)
# Dependency: Python 3, scikit-learn

from sklearn.metrics.scorer import make_scorer
import math

def MAPE_scorer(y, y_pred):
    error = 0
    num = len(y)
    for i in range(0, num):
        if y[i] > 0:
            error += math.fabs(y_pred[i] - y[i]) / y[i]
    # print(error, num)
    if num > 0:
        return error / num
    else:
        return 0

my_scorer = make_scorer(MAPE_scorer)
