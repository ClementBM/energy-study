from datetime import datetime
from random import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.tsa.api as smt
from matplotlib import pyplot
from pandas.plotting import autocorrelation_plot
from scipy.stats import norm, uniform, t

from energy_study.common import (
    BASE_DIR,
    FOSSIL_SOURCES,
    NRJ_DETAILED_SOURCES,
    NRJ_SOURCES,
    RENEWABLE_SOURCES,
)
from energy_study.ts_toolbox import descriptive_metrics, normality

sns.set(rc={"figure.figsize": (14, 10)})

df = pd.read_csv(
    BASE_DIR / "eCO2mix_RTE_Annuel-Definitif_2020.xls",
    delimiter="\t",
    index_col=False,
)


df = df[df["Consommation"].notna()]
df["DateTime"] = [
    datetime.strptime(f"{date} {hour}", "%Y-%m-%d %H:%M")
    for date, hour in zip(df["Date"], df["Heures"])
]

df = df.set_index("DateTime")

df["Year"] = df.index.year
df["Month"] = df.index.month_name()
df["Day"] = df.index.day_name()


df["Prevision_Error"] = df["Prévision J-1"] - df["Consommation"]
df["fossil_sum"] = df[FOSSIL_SOURCES].sum(axis=1)


def plot_nrj(nrj_names):
    plt.figure(figsize=(18, 12))
    for i, nrj_name in enumerate(nrj_names):
        plt.subplot(len(nrj_names) + 1, 1, i + 1)
        plt.plot(df[nrj_name].ravel(), "r-")
        plt.title(nrj_name, fontsize=10, pad="2.0")
        plt.xticks([])

    plt.subplot(len(nrj_names) + 1, 1, len(nrj_names) + 1)
    plt.plot(df.index, df[nrj_names].sum(axis=1).ravel(), "r-")
    plt.title("Somme", fontsize=10, pad="2.0")


def plot_seasonality(df, columns, seasonality="Month"):
    """
    Heures
    """
    fig, axes = plt.subplots(len(columns), 1, figsize=(11, 10), sharex=True)
    for name, ax in zip(columns, axes):
        sns.boxplot(data=df, x=seasonality, y=name, ax=ax)
        ax.set_ylabel("MW")
        ax.set_title(name)
        # Remove the automatic x-axis label from all but the bottom subplot
        if ax != axes[-1]:
            ax.set_xlabel("")
        else:
            ax.tick_params(axis="x", rotation=45)


def tsplot(y, lags=None, title="", figsize=(14, 8)):
    """Examine the patterns of ACF and PACF, along with the time series plot and histogram.

    Original source: https://tomaugspurger.github.io/modern-7-timeseries.html
    """
    fig = plt.figure(figsize=figsize)
    layout = (2, 2)
    ts_ax = plt.subplot2grid(layout, (0, 0))
    hist_ax = plt.subplot2grid(layout, (0, 1))
    acf_ax = plt.subplot2grid(layout, (1, 0))
    pacf_ax = plt.subplot2grid(layout, (1, 1))

    y.plot(ax=ts_ax)
    ts_ax.set_title(title)
    y.plot(ax=hist_ax, kind="hist", bins=25)
    hist_ax.set_title("Histogram")
    smt.graphics.plot_acf(y, lags=lags, ax=acf_ax)
    smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax)
    [ax.set_xlim(0) for ax in [acf_ax, pacf_ax]]
    sns.despine()
    plt.tight_layout()
    return ts_ax, acf_ax, pacf_ax


plot_nrj(NRJ_SOURCES)
plot_nrj(RENEWABLE_SOURCES)

plot_seasonality(df, columns=RENEWABLE_SOURCES, seasonality="Heures")
plot_seasonality(df, columns=RENEWABLE_SOURCES, seasonality="Month")
plot_seasonality(df, columns=RENEWABLE_SOURCES, seasonality="Day")


plot_seasonality(
    df,
    columns=["Prevision_Error", "Consommation"],
    seasonality="Heures",
)
plot_seasonality(
    df,
    columns=["Prevision_Error", "Consommation"],
    seasonality="Month",
)
plot_seasonality(
    df,
    columns=["Prevision_Error", "Consommation"],
    seasonality="Day",
)

sns.lineplot(
    x=df.index,
    y="Prevision_Error",
    hue="Day",
    style="Day",
    data=df,
)

df.groupby(by="Month")["Prevision_Error"].plot(figsize=(14, 10), marker="o")

df.groupby(by="Heures")["Prevision_Error"].plot(figsize=(14, 10), kind="density")
df.groupby(by="Day")["Prevision_Error"].plot(figsize=(14, 10), kind="density")
df.groupby(by="Month")["Prevision_Error"].plot(figsize=(14, 10), kind="density")

descriptive_metrics(df, "Prevision_Error")

df.groupby(by="Heures")["Prevision_Error"].agg(["mean", "count"])
df.groupby(by="Day")["Prevision_Error"].agg(["mean", "count"])
df.groupby(by="Month")["Prevision_Error"].agg(["mean", "count"])


df["Prevision_Error"].hist(by=df["Heures"], bins=30, figsize=(14, 10))
df["Prevision_Error"].hist(by=df["Day"], bins=30, figsize=(14, 10))
df["Prevision_Error"].hist(by=df["Month"], bins=30, figsize=(14, 10))
df["Prevision_Error"].hist(bins=40, figsize=(14, 10))


smt.graphics.plot_acf(df["Prevision_Error"], lags=48)

smt.graphics.plot_pacf(df["Prevision_Error"], lags=48)
smt.graphics.plot_pacf(df["Prevision_Error"].diff().dropna(), lags=48)


tsplot(df["Prevision_Error"], lags=48)
tsplot(df["Prevision_Error"], lags=48 * 2)
tsplot(df["Prevision_Error"], lags=48 * 3)
tsplot(df["Prevision_Error"].pow(2), lags=48 * 3)
tsplot(df["Prevision_Error"].abs(), lags=48 * 3)
tsplot(df["Prevision_Error"].diff().dropna(), lags=48)

autocorrelation_plot(df["Prevision_Error"].diff().dropna())
autocorrelation_plot(df["Prevision_Error"])

# Random walk differenciation
random_walk = list()
random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = random_walk[i - 1] + movement
    random_walk.append(value)

# line plot
autocorrelation_plot(random_walk)
pyplot.show()

tsplot(pd.DataFrame(random_walk), 250)


normality(df, "Prevision_Error").T


sm.qqplot(df["Prevision_Error"], line="s")


sm.qqplot(df["Prevision_Error"], norm, fit=True, line="45")
sm.qqplot(df["Prevision_Error"], t, fit=True, line="45")

df_normalized = (df["Prevision_Error"] - df["Prevision_Error"].mean()) / df[
    "Prevision_Error"
].std()

# standardized and studentized residuals typically rescale
# the residuals so that values of more than 1.96 from 0 equate
# to a p-value of 0.05. Different software packages use terminology inconsistently.
