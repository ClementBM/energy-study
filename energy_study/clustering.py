from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tslearn.clustering import TimeSeriesKMeans, silhouette_score
from tslearn.neighbors import KNeighborsTimeSeries
from tslearn.utils import to_time_series_dataset
import seaborn as sns
from energy_study.common import (
    FOSSIL_SOURCES,
    NRJ_DETAILED_SOURCES,
    NRJ_SOURCES,
    RENEWABLE_SOURCES,
    BASE_DIR,
)

from random import seed, random
from random import randrange


seed(1)

# iid Noise
series = [randrange(10) for i in range(1000)]
plt.plot(series)

# Random walk
random_walk = list()
random_walk.append(-1 if random() < 0.5 else 1)
for i in range(1, 1000):
    movement = -1 if random() < 0.5 else 1
    value = random_walk[i - 1] + movement
    random_walk.append(value)
plt.plot(random_walk)


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


k_values = 12 * int(len(df) / 12)

selected_columns = NRJ_SOURCES + ["Prevision_Error", "fossil_sum"]
df_nrj = df[selected_columns]

# Consommation - Prévision J
# df ...
# Comparer avec les pics de prod nrj fossil

df_nrj_scaled = (df_nrj - df_nrj.mean()) / df_nrj.std()
df_nrj_scaled = (df_nrj - df_nrj.min()) / (df_nrj.max() - df_nrj.min())
df_nrj_scaled = df_nrj / df_nrj.abs().max()

X_train = to_time_series_dataset(df_nrj_scaled[:k_values].T)

n_neighbors = 10
knn = KNeighborsTimeSeries(n_neighbors=n_neighbors)
knn.fit(X_train)

query_txt = "Prevision_Error"

ts_query = to_time_series_dataset(df_nrj_scaled[query_txt][:k_values])
distances, ind = knn.kneighbors(ts_query, return_distance=True)

plt.figure(figsize=(18, 12))
plt.subplot(n_neighbors + 1, 1, 1)
plt.plot(ts_query.ravel(), "k-")
plt.title(query_txt, fontsize=10, pad="2.0")
plt.xticks([])
for rank_nn in range(n_neighbors):
    plt.subplot(n_neighbors + 1, 1, rank_nn + 2)
    plt.plot(X_train[ind[0, rank_nn]].ravel(), "r-")
    plt.title(
        selected_columns[ind[0, rank_nn]] + f" {distances[0, rank_nn]}",
        fontsize=10,
        pad="2.0",
    )
    plt.xticks([])


plt.suptitle("Queries (in black) and their nearest neighbors (red)")
plt.show()

for cluster_count in range(3, 7):
    km = TimeSeriesKMeans(n_clusters=5, metric="dtw", n_jobs=4, n_init=5)
    labels = km.fit_predict(X_train)
    score = silhouette_score(X_train, labels, metric="dtw", n_jobs=4)
    print(f"{cluster_count}: {score}")


km = TimeSeriesKMeans(n_clusters=5, metric="dtw", n_jobs=4, n_init=5)
labels = km.fit_predict(X_train)

score = silhouette_score(X_train, labels, metric="dtw", n_jobs=4)
print(f"{cluster_count}: {score}")

for yi in range(5):
    plt.subplot(5, 1, yi + 1)
    for xx in X_train[labels == yi]:
        plt.plot(xx.ravel(), "k-", alpha=0.2)
    plt.plot(km.cluster_centers_[yi].ravel(), "r-")
    plt.xlim(0, 1000)
    plt.ylim(-4, 4)
    plt.text(0.55, 0.85, "Cluster %d" % (yi + 1), transform=plt.gca().transAxes)


np.array(selected_columns)[labels == 4]
