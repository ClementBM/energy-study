import numpy as np
from random import random, choices
from energy_study.ts_toolbox import (
    plot_nrj,
    descriptive_metrics,
    plot_seasonality,
    tsplot,
)
import pandas as pd


def gaussian_white_noise(n_sample):
    z = np.random.normal(0, 1, n_sample)
    return pd.DataFrame(z, columns=["Gaussian White Noise"])


def symmetric_random_walk(n_sample):
    z = choices([-1, 1], k=n_sample + 1)
    random_walk = np.cumsum(z)
    return pd.DataFrame(random_walk)


def normal_random_walk(n_sample):
    z = np.random.normal(0, 1, n_sample + 1)
    random_walk = np.cumsum(z)
    return pd.DataFrame(random_walk, columns=["Gaussian Random Walk"])


def auto_regressive_1(n_sample, phi_1, sigma=1):
    epsilons = np.random.normal(0, sigma, n_sample)

    z = [sigma * epsilons[0]]

    for i in range(n_sample - 1):
        z.append(phi_1 * z[-1] + sigma * epsilons[i + 1])

    return pd.DataFrame(z, columns=[f"1st Order Autoregressive $\phi_1$ = {phi_1}"])


def moving_average_1(n_sample, theta_1, sigma=1):
    epsilons = np.random.normal(0, sigma, n_sample)

    z = [epsilons[0]]

    for i in range(n_sample - 1):
        z.append(theta_1 * epsilons[i] + epsilons[i + 1])

    return pd.DataFrame(
        z, columns=[f"1st Order Moving Average $\\theta_1$ = {theta_1}"]
    )


N = 2000
LAGS = 40


z = gaussian_white_noise(N)
tsplot(z, lags=LAGS)

z = symmetric_random_walk(N)
tsplot(z, lags=LAGS)

z = normal_random_walk(N)
tsplot(z, lags=LAGS)

z = auto_regressive_1(N, 0.9)
tsplot(z, lags=LAGS)

z = moving_average_1(N, 0.9)
tsplot(z, lags=LAGS)

z.rolling(100).apply(lambda x: x.autocorr(lag=1), raw=False).plot()
z.rolling(100).apply(lambda x: x.autocorr(lag=10), raw=False).plot()
z.rolling(10).apply(lambda x: x.autocorr(lag=1), raw=False).plot()
z.rolling(50).apply(lambda x: x.autocorr(lag=1), raw=False).rolling(50).mean().plot()
z.rolling(50).apply(lambda x: x.autocorr(lag=2), raw=False).rolling(50).mean().plot()

tsplot(z.diff().dropna(), lags=LAGS)
