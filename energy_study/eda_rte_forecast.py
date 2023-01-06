import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.tsa.api as smt
from pandas.plotting import autocorrelation_plot
from scipy.stats import norm, t, uniform, jarque_bera
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
from energy_study.ts_iid import IidTests
from energy_study.ts_autocorrelation import AutocorrelationTests


df = prepare_data("eCO2mix_RTE_Annuel-Definitif_2020.xls")

column_mappings = DataColumnSpec.mappings()
prevision_error_col = DataColumnSpec.FORECAST_ERROR.__name__
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

# sns.residplot

## summary of fit model
print(model_fit.summary().to_markdown())

x = pd.DataFrame(model_fit.resid)

# Basic informations
print(descriptive_metrics(x, 0).T.to_markdown())
x.plot()

# Rolling statistics
pd.DataFrame(
    {
        "Forecast error rolling mean": x.rolling(window=48).mean().to_numpy().ravel(),
        "Forecast error rolling standard deviation": x.rolling(window=48)
        .std()
        .to_numpy()
        .ravel(),
    },
    index=x.index,
).plot(ylabel="GW", xlabel="Time")

# Correlogram
tsplot(x, lags=48 * 2)
tsplot(x, lags=48 * 3)

## Autocorrelation tests
autocorrelation_tests = AutocorrelationTests(lags=[48 * 2, 48 * 3])
print(autocorrelation_tests.ljung_box(x))
autocorrelation_tests.mcleod_li(x)

## Turning point test
independence_tests = IidTests()
print(independence_tests.turning_point(x).to_markdown())

## Rank test
print(independence_tests.rank(x).to_markdown())


# Stationarity test
## Up to 3 day lag

stationarity_test = StationarityTests(significance=0.05, max_lag=48 * 3)
print(stationarity_test.kpss(x, return_df=True).T.to_markdown())
print(stationarity_test.adf(x).T.to_markdown())


## Yule-Walker
model = ARIMA(
    x,
    order=([1, 2, 3, 4, 5, 6, 7, 8, 9], 0, 0),
)
model.fit(method="yule_walker").summary()

model_AR0 = ARIMA(
    x,
    order=(0, 0, 0),
)
model_AR0.fit(method="yule_walker").summary()

## Jarque Bera
jarque_bera(x)

# density plot of residuals
ax = x.plot(kind="kde")
x_norm = np.linspace(-10, 10, 200)
plt.plot(x_norm, norm.pdf(x_norm, x.mean(), x.std()))
ax.set_xlim(-7, 7)


sm.qqplot(
    x.to_numpy().ravel(),
    norm,
    loc=float(x.mean()),
    scale=float(x.std()),
    fit=False,
    line="45",
)
