import pandas
from readers import data_reader
from sklearn.linear_model import LinearRegression
import numpy
import seaborn
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from scipy import stats
import numpy
from scipy import stats
import pandas as pd
from scipy import stats
from linearmodels import PooledOLS
import statsmodels.api as sm

import pandas
import requests

import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt

from sklearn.manifold import TSNE
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, silhouette_samples
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import LinearSVC

df = data_reader.read_all_indicators()
df_industry = df[["Company", "Sector"]].drop_duplicates().reset_index(drop=True)

X_orig = df[df["Year"] == 2021]
X_orig = X_orig.set_index("Company")
X_orig = X_orig[["CR", "DA", "FL", "OPM", "RT", "TAT"]]

scaler = StandardScaler()
X_orig = scaler.fit_transform(X_orig)
print(X_orig.shape)

results = []

for perplexity in range(5, 15):
    tsne = TSNE(
        init="pca",
        n_components=2,
        perplexity=perplexity,
        learning_rate="auto",
        random_state=0,
    )
    X = tsne.fit_transform(X_orig)

    for n_clusters in range(5, 15):
        model = KMeans(n_clusters=n_clusters, random_state=0)
        labels = model.fit_predict(X)
        silhouette_score_val = silhouette_score(X, labels)
        results.append([perplexity, n_clusters, silhouette_score_val])

df_results = pandas.DataFrame(results, columns=["perplexity", "n_clusters", "silhouette_score_val"])
df_results.to_excel("results.xlsx")

perplexity = 6
n_clusters = 10

tsne = TSNE(
    init="pca",
    n_components=2,
    perplexity=perplexity,
    learning_rate="auto",
    random_state=0,
)
# X = tsne.fit_transform(X_orig)
X = X_orig

model = KMeans(n_clusters=n_clusters, random_state=0)
labels = model.fit_predict(X)
plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap="Set1")
centers = model.cluster_centers_
print(centers)
plt.scatter(centers[:, 0], centers[:, 1], c="black", s=200, alpha=0.5)
plt.show()
silhouette_score_val = silhouette_score(X, labels)
print(silhouette_score_val)

df = df[df["Year"] == 2021]
df["Labels"] = labels
df.to_excel("df.xlsx")

df_pivot = pandas.pivot_table(data=df, index="Sector", columns="Labels", values="Company", aggfunc=len)
print(df_pivot)
df_pivot.to_excel("pivot.xlsx")

# inversed = scaler.inverse_transform(X)
# print(inversed)
# print(scaler.inverse_transform(centers))
