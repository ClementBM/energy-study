from tslearn.clustering import TimeSeriesKMeans, silhouette_score
from energy_study.common import (
    BASE_DIR,
    DataColumnSpec,
)
import pandas as pd
from datetime import datetime
from tslearn.utils import to_time_series_dataset

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
df["fossil_sum"] = df[DataColumnSpec.FOSSIL_SOURCES].sum(axis=1)

df_nrj = df[DataColumnSpec.ENERGY_SOURCES + ["Prevision_Error", "fossil_sum"]]

df_nrj = df_nrj.resample("1H").mean()

df_nrj_scaled = (df_nrj - df_nrj.mean()) / df_nrj.std()
df_nrj_scaled = (df_nrj - df_nrj.min()) / (df_nrj.max() - df_nrj.min())
df_nrj_scaled = df_nrj / df_nrj.abs().max()

X_train = to_time_series_dataset(df_nrj_scaled.T)

for cluster_count in range(3, 7):
    km = TimeSeriesKMeans(n_clusters=5, metric="dtw", n_jobs=2, n_init=5)
    labels = km.fit_predict(X_train)
    score = silhouette_score(X_train, labels, metric="dtw", n_jobs=4)
    print(f"{cluster_count}: {score}")
