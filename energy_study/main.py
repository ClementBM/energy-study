import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tslearn.clustering import TimeSeriesKMeans, silhouette_score
from tslearn.neighbors import KNeighborsTimeSeries
from tslearn.utils import to_time_series_dataset
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

df = pd.read_csv(
    BASE_DIR / "eCO2mix_RTE_Annuel-Definitif_2020.xls",
    delimiter="\t",
    index_col=False,
)

df = df[df["Consommation"].notna()]

nrj_sources = [
    "Fioul",
    "Charbon",
    "Gaz",
    "Nucléaire",
    "Eolien",
    "Solaire",
    "Hydraulique",
    "Pompage",
    "Bioénergies",
    "Ech. physiques",
    "Taux de Co2",
]


def plot_nrj(nrj_names):
    plt.figure(figsize=(18, 12))
    for i, nrj_name in enumerate(nrj_names):
        plt.subplot(len(nrj_names) + 1, 1, i + 1)
        plt.plot(df[nrj_name].ravel(), "r-")
        plt.title(nrj_name, fontsize=10, pad="2.0")
        plt.xticks([])

    plt.subplot(len(nrj_names) + 1, 1, len(nrj_names) + 1)
    plt.plot(df[nrj_names].sum(axis=1).ravel(), "r-")
    plt.title("Somme", fontsize=10, pad="2.0")
    plt.xticks([])


plot_nrj(nrj_sources)

nrj_detailed_sources = [
    "Ech. comm. Angleterre",
    "Ech. comm. Espagne",
    "Ech. comm. Italie",
    "Ech. comm. Suisse",
    "Ech. comm. Allemagne-Belgique",
    "Fioul - TAC",
    "Fioul - Cogén.",
    "Fioul - Autres",
    "Gaz - TAC",
    "Gaz - Cogén.",
    "Gaz - CCG",
    "Gaz - Autres",
    "Hydraulique - Fil de l?eau + éclusée",
    "Hydraulique - Lacs",
    "Hydraulique - STEP turbinage",
    "Bioénergies - Déchets",
    "Bioénergies - Biomasse",
    "Bioénergies - Biogaz",
]

renewable_sources = [
    "Eolien",
    "Solaire",
    "Hydraulique",
]


plot_nrj(renewable_sources)


fossil_sources = [
    "Fioul",
    "Charbon",
    "Gaz",
]

k_values = int(len(df) / 12)

df_nrj = df[nrj_sources]
df_nrj["fossil_sum"] = df_nrj[fossil_sources].sum(axis=1)
nrj_sources.append("fossil_sum")

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

query_txt = "Taux de Co2"

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
        nrj_sources[ind[0, rank_nn]] + f" {distances[0, rank_nn]}",
        fontsize=10,
        pad="2.0",
    )
    plt.xticks([])


plt.suptitle("Queries (in black) and their nearest neighbors (red)")
plt.show()

for cluster_count in range(3, 12):
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


np.array(nrj_sources)[labels == 4]
