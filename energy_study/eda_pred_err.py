import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.tsa.api as smt
from pandas.plotting import autocorrelation_plot
from scipy.stats import norm, t, uniform
from statsmodels.tsa.arima.model import ARIMA

from energy_study.common import DataColumnSpec
from energy_study.data_preprocessing import prepare_data
from energy_study.ts_stationarity import StationarityTests
from energy_study.ts_toolbox import (
    descriptive_metrics,
    normality,
    plot_nrj,
    plot_seasonality,
    tsplot,
)
import math


df = prepare_data("eCO2mix_RTE_Annuel-Definitif_2020.xls")

column_mappings = DataColumnSpec.mappings()
prevision_error_col = DataColumnSpec.PREVISION_ERROR.__name__
renewable_cols = [
    column_mappings[col_name] for col_name in DataColumnSpec.RENEWABLE_SOURCES
]
energy_cols = [column_mappings[col_name] for col_name in DataColumnSpec.ENERGY_SOURCES]

# Data integrity, none ? constant time step ?

# General visualization
covid_1 = slice(7 * 48 * 10, 7 * 48 * 12)
covid_2 = slice(7 * 48 * 42, 7 * 48 * 43)
christmas_2 = slice(7 * 48 * 51, 7 * 48 * 54)

plot_nrj(
    df,
    [
        column_mappings[DataColumnSpec.FORECAST],
        column_mappings[DataColumnSpec.CONSUMPTION],
        prevision_error_col,
    ],
    unit="GW",
    zoom=covid_1,
    show_sum=False,
)

plot_nrj(df, energy_cols, unit="GW", zoom=covid_1)
plot_nrj(df, renewable_cols, unit="GW")


# Error superior than 5 GW
df["IS_EXTREME"] = df[prevision_error_col].abs() > 5

sns.scatterplot(
    x=df.index,
    y=prevision_error_col,
    hue="IS_EXTREME",
    style="IS_EXTREME",
    data=df,
)


autocorr_1 = (
    df[prevision_error_col]
    .rolling(48 * 7)
    .apply(lambda x: x.autocorr(lag=1), raw=False)
)
autocorr_1.plot()

autocorr_2 = (
    df[prevision_error_col]
    .rolling(48 * 7)
    .apply(lambda x: x.autocorr(lag=2), raw=False)
)
autocorr_2.plot()


autocorr_6 = (
    df[prevision_error_col]
    .rolling(48 * 7)
    .apply(lambda x: x.autocorr(lag=6), raw=False)
)
autocorr_6.plot()

autocorr_12 = (
    df[prevision_error_col]
    .rolling(48 * 7)
    .apply(lambda x: x.autocorr(lag=12), raw=False)
)
autocorr_12.plot()

np.corrcoef(
    [
        autocorr_1.dropna().to_numpy(),
        autocorr_2.dropna().to_numpy(),
        autocorr_6.dropna().to_numpy(),
        autocorr_12.dropna().to_numpy(),
    ]
)


## Box plot seasonality

plot_seasonality(df, columns=renewable_cols, unit="GW", seasonality="Hour")
plot_seasonality(df, columns=renewable_cols, unit="GW", seasonality="Month")
plot_seasonality(df, columns=renewable_cols, unit="GW", seasonality="Day")


plot_seasonality(
    df,
    columns=[
        prevision_error_col,
        column_mappings[DataColumnSpec.CONSUMPTION],
    ],
    unit="GW",
    seasonality="Hour",
)

df[df[prevision_error_col].abs() < 5]
plot_seasonality(
    df,
    columns=[
        prevision_error_col,
        column_mappings[DataColumnSpec.CONSUMPTION],
    ],
    unit="GW",
    seasonality="Month",
)
plot_seasonality(
    df,
    columns=[
        prevision_error_col,
        column_mappings[DataColumnSpec.CONSUMPTION],
    ],
    unit="GW",
    seasonality="Day",
)

sns.lineplot(
    x=df.index,
    y=prevision_error_col,
    hue="Day",
    style="Day",
    data=df,
)

df.groupby(by="Month")[prevision_error_col].plot(figsize=(14, 10), marker="o")

df.groupby(by="Hour")[prevision_error_col].plot(figsize=(14, 10), kind="density")
df.groupby(by="Day")[prevision_error_col].plot(figsize=(14, 10), kind="density")
df.groupby(by="Month")[prevision_error_col].plot(figsize=(14, 10), kind="density")


df.groupby(by="Hour")[prevision_error_col].agg(["mean", "std", "count"])
df.groupby(by="Day")[prevision_error_col].agg(["mean", "std", "count"])
df.groupby(by="Month")[prevision_error_col].agg(["mean", "std", "count"])


df[prevision_error_col].hist(by=df["Hour"], bins=30, figsize=(14, 10))
df[prevision_error_col].hist(by=df["Day"], bins=30, figsize=(14, 10))
df[prevision_error_col].hist(by=df["Month"], bins=30, figsize=(14, 10))
df[prevision_error_col].hist(bins=40, figsize=(14, 10))


smt.graphics.plot_acf(df[prevision_error_col], lags=50)
smt.graphics.plot_acf(df[prevision_error_col].diff().dropna(), lags=48 * 3)

smt.graphics.plot_pacf(df[prevision_error_col], lags=50)
smt.graphics.plot_pacf(df[prevision_error_col].diff().dropna(), lags=48 * 3)


tsplot(df[prevision_error_col], lags=48)
tsplot(df[prevision_error_col], lags=48 * 2)
tsplot(df[prevision_error_col], lags=48 * 3)
tsplot(df[prevision_error_col].pow(2), lags=48 * 3)
tsplot(df[prevision_error_col].abs(), lags=48 * 3)
tsplot(df[prevision_error_col].diff().dropna(), lags=48)

autocorrelation_plot(df[prevision_error_col].diff().dropna())
autocorrelation_plot(df[prevision_error_col])


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
