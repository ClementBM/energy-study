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
from rpy2.robjects.packages import importr
from rpy2.robjects import FloatVector, r

# Import R functions
# TSA => McLeod.Li.test
importr("TSA")
# spgs => turningpoint.test(n)
importr("spgs")

df = prepare_data("eCO2mix_RTE_Annuel-Definitif_2020.xls")

column_mappings = DataColumnSpec.mappings()
prevision_error_col = DataColumnSpec.PREVISION_ERROR.__name__
renewable_cols = [
    column_mappings[col_name] for col_name in DataColumnSpec.RENEWABLE_SOURCES
]
energy_cols = [column_mappings[col_name] for col_name in DataColumnSpec.ENERGY_SOURCES]

x = df[prevision_error_col]

model = ARIMA(
    df[prevision_error_col],
    order=(2, 0, 3),
    seasonal_order=(1, 0, 0, 48),
)
model_fit = model.fit()
## summary of fit model
print(model_fit.summary())

x = pd.DataFrame(model_fit.resid)

# Statistical tests
x.describe()
descriptive_metrics(x, prevision_error_col)
x.plot()

ax = x.plot(kind="kde")
x_norm = np.linspace(-10, 10, 200)
plt.plot(x_norm, norm.pdf(x_norm, x.mean(), x.std()))
ax.set_xlim(-7, 7)

## Ljung Box Portmanteau test
sm.stats.acorr_ljungbox(x, lags=[48 * 2, 48 * 3], return_df=True)

## McLeod Li Portmanteau teast
x_for_r = FloatVector(x.ravel())  # converted R float vector
mcleod_li_result = r["McLeod.Li.test"](y=x_for_r)

list(dict(zip(mcleod_li_result.names, list(mcleod_li_result)))["p.values"])

## Turning point test
turning_point_result = r["turningpoint.test"](x_for_r)
list(dict(zip(turning_point_result.names, list(turning_point_result)))["p.value"])

## Rank test
rank_test_result = r["rank.test"](x_for_r)
list(dict(zip(rank_test_result.names, list(rank_test_result)))["p.value"])

## Yule-Walker
model = ARIMA(
    x,
    order=([0, 1, 2, 3, 4, 5], 0, 0),
)
model_fit = model.fit(method="yule_walker")
print(model_fit.summary())

## Jarque Bera

# density plot of residuals
x.plot(kind="kde")

sm.qqplot(
    x.to_numpy().ravel(),
    norm,
    loc=x.mean(),
    scale=x.std(),
    fit=False,
    line="45",
)


# Rolling statistics
x.rolling(window=48).mean().plot(
    title="Forecast error rolling mean", ylabel="GW", xlabel="Time"
)
x.rolling(window=48).std().plot(
    title="Forecast error rolling standard deviation", ylabel="GW", xlabel="Time"
)


# Correlogram
tsplot(x, lags=48 * 2)
tsplot(x, lags=48 * 3)


# Stationarity test
## Up to 3 day lag

stationarity_test = StationarityTests(significance=0.05, max_lag=48 * 3)
stationarity_test.kpss(x)
stationarity_test.adf(x)
