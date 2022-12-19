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

df = pd.read_json(BASE_DIR / "donnees-synop-essentielles-omm.json")

df = pd.read_csv(
    BASE_DIR / "donnees-synop-essentielles-omm-2020.csv",
    delimiter=";",
    index_col=False,
    parse_dates=["Date"],
    infer_datetime_format=True,
)

df = df.set_index("Date")

df.sort_index()

df["Date"] = [datetime.fromisoformat(date) for date in df["Date"]]

"2020-04-24T23:00:00+02:00"

pd.to_datetime(df["Date"]).dt.normalize()
