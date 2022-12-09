import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tslearn.clustering import TimeSeriesKMeans, silhouette_score
from tslearn.neighbors import KNeighborsTimeSeries
from tslearn.utils import to_time_series_dataset

df = pd.read_csv(
    "/home/clem/Documents/source/reinforcement-learning-pluralsight/reinforcement_learning_pluralsight/eCO2mix_RTE_Annuel-Definitif_2020.xls",
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

n_neighbors = 6
k_values = int(len(df) / 12)

df_nrj = df[nrj_sources]

df_nrj_scaled = (df_nrj - df_nrj.mean()) / df_nrj.std()
df_nrj_scaled = (df_nrj - df_nrj.min()) / (df_nrj.max() - df_nrj.min())
df_nrj_scaled = df_nrj / df_nrj.abs().max()

X_train = to_time_series_dataset(df_nrj_scaled[:k_values].T)

knn = KNeighborsTimeSeries(n_neighbors=n_neighbors)
knn.fit(X_train)

query_txt = "Ech. comm. Angleterre"

ts_query = to_time_series_dataset(df_nrj_scaled[query_txt][:k_values])
ind = knn.kneighbors(ts_query, return_distance=False)

n_queries = 1

plt.figure()
for idx_ts in range(n_queries):
    plt.subplot(n_neighbors + 1, n_queries, idx_ts + 1)
    plt.plot(ts_query.ravel(), "k-")
    plt.title(query_txt, fontsize=10, pad="2.0")
    plt.xticks([])
    for rank_nn in range(n_neighbors):
        plt.subplot(
            n_neighbors + 1, n_queries, idx_ts + (n_queries * (rank_nn + 1)) + 1
        )
        plt.plot(X_train[ind[idx_ts, rank_nn]].ravel(), "r-")
        plt.title(nrj_sources[ind[idx_ts, rank_nn]], fontsize=10, pad="2.0")
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
