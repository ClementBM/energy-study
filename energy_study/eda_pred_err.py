from datetime import datetime

import pandas as pd
import seaborn as sns
import statsmodels.api as sm
import statsmodels.tsa.api as smt
from pandas.plotting import autocorrelation_plot
from scipy.stats import norm, uniform, t
from energy_study.ts_toolbox import (
    plot_nrj,
    descriptive_metrics,
    plot_seasonality,
    tsplot,
)

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
