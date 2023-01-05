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
)
from energy_study.ts_toolbox import descriptive_metrics, normality

sns.set(rc={"figure.figsize": (14, 10)})

df = pd.read_csv(
    BASE_DIR / "donnees-synop-essentielles-omm-2020.csv",
    delimiter=";",
    index_col=False,
    parse_dates=["Date"],
    infer_datetime_format=True,
)

df["Date"] = pd.to_datetime(df["Date"], utc=True, errors="coerce")
df = df.dropna(subset=["Nebulosité totale"])

df = df.set_index("Date")
df = df.sort_index()
df["Year"] = df.index.year
df["Month"] = df.index.month_name()
df["Day"] = df.index.day_name()

selected_column = [
    "Nebulosité totale",
    "Direction du vent moyen 10 mn",
    "Vitesse du vent moyen 10 mn",
    "Temps présent",
    "Temps présent.1",
    "Température (°C)",
    "Précipitations dans les 24 dernières heures",
    "Coordonnees",
    "Nom",
    "communes (name)",
    "department (name)",
    "region (name)",
    "mois_de_l_annee",
    "Year",
    "Month",
    "Day",
]

df = df[selected_column]
