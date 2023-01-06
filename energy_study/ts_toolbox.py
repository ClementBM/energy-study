import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.tsa.api as smt
import seaborn as sns


def descriptive_metrics(df, column_name):

    metrics = pd.DataFrame(
        data=[
            column_name,
            df[column_name].count(),
            df[column_name].mean(),
            df[column_name].std(),
            df[column_name].var(),
            df[column_name].skew(),
            df[column_name].kurt(),
            df[column_name].min(),
            df[column_name].quantile(q=0.25),
            df[column_name].quantile(q=0.5),
            df[column_name].quantile(q=0.75),
            df[column_name].max(),
        ],
        index=[
            "column",
            "count",
            "mean",
            "std",
            "variance",
            "skewness",
            "kurtosis",
            "min",
            "25%",
            "median",
            "75%",
            "max",
        ],
    )

    return metrics


def normality(df, column_name):
    sw = stats.shapiro(df[column_name])
    ks_norm = stats.kstest(rvs=df[column_name], cdf="norm")

    ks_uniform = stats.kstest(rvs=df[column_name], cdf="uniform")

    error_metric = pd.DataFrame(
        data={
            "column": column_name,
            "count": len(df[column_name]),
            "shapiro-wilk statistic": sw.statistic,
            "shapiro-wilk p-value": sw.pvalue,
            "ks-n-test statistic": ks_norm.statistic,
            "ks-n-test p-value": ks_norm.pvalue,
            "ks-u-test statistic": ks_uniform.statistic,
            "ks-u-test p-value": ks_uniform.pvalue,
        },
        index=[0],
    )

    return error_metric


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
    ts_ax.set_xlabel("Time steps")
    y.plot(ax=hist_ax, kind="hist", bins=25)
    hist_ax.set_xlabel("Values")
    smt.graphics.plot_acf(y, lags=lags, ax=acf_ax)
    acf_ax.set_xlabel("Lags (h)")

    smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax)
    pacf_ax.set_xlabel("Lags (h)")

    [ax.set_xlim(0) for ax in [acf_ax, pacf_ax]]
    sns.despine()
    plt.tight_layout()
    return ts_ax, acf_ax, pacf_ax


def plot_nrj(df, nrj_names, unit, zoom=slice(0, -1), show_sum=True):
    plt.figure(figsize=(18, 12))
    for i, nrj_name in enumerate(nrj_names):
        ax = plt.subplot(len(nrj_names) + 1, 1, i + 1)
        ax.set_ylabel(unit)
        if i == len(nrj_names) - 1 and show_sum == False:
            plt.plot(df.index[zoom], df[nrj_name].ravel()[zoom], "r-")
            plt.title(nrj_name, fontsize=10, pad="2.0")
            continue
        plt.plot(df[nrj_name].ravel()[zoom], "r-")
        plt.title(nrj_name, fontsize=10, pad="2.0")
        plt.xticks([])

    if show_sum:
        plt.subplot(len(nrj_names) + 1, 1, len(nrj_names) + 1)
        plt.plot(df.index[zoom], df[nrj_names].sum(axis=1).ravel()[zoom], "r-")
        plt.title("SUM", fontsize=10, pad="2.0")


def plot_seasonality(df, columns, unit, seasonality="Month"):
    """
    Heures
    """
    fig, axes = plt.subplots(len(columns), 1, figsize=(11, 10), sharex=True)
    for name, ax in zip(columns, axes):
        sns.boxplot(data=df, x=seasonality, y=name, ax=ax)
        ax.set_ylabel(unit)
        ax.set_title(name)
        # Remove the automatic x-axis label from all but the bottom subplot
        if ax != axes[-1]:
            ax.set_xlabel("")
        else:
            ax.tick_params(axis="x", rotation=45)
