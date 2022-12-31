import numpy as np
from random import random, choices
from energy_study.ts_toolbox import (
    plot_nrj,
    descriptive_metrics,
    plot_seasonality,
    tsplot,
)
import pandas as pd


def simple_symmetric_random_walk(n_sample):
    y = choices([-1, 1], k=n_sample + 1)
    random_walk = np.cumsum(y)
    return pd.DataFrame(random_walk)


def normal_random_walk(n_sample):
    y = np.random.normal(0, 1, n_sample + 1)
    random_walk = np.cumsum(y)
    return pd.DataFrame(random_walk)


rw = simple_symmetric_random_walk(1000)
tsplot(rw, lags=100)
tsplot(rw.diff().dropna(), lags=100)


rw = normal_random_walk(1000)
tsplot(rw, lags=100)
tsplot(rw.diff().dropna(), lags=100)
