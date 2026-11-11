from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier


PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "data" / "landmarks.csv"
PLOT_PATH = PROJECT_DIR / "data" / "pca_clusters.png"

df = pd.read_csv(DATA_PATH)

# Одинаковый порядок 42 признаков для обучения и проверки.
feature_columns = []
for i in range(21):
    feature_columns.append(f"x{i}")
    feature_columns.append(f"y{i}")

train_df = df[df["session_id"] == "session_01"]
validation_df = df[df["session_id"] == "session_02"]

X_train = train_df[feature_columns]
y_train = train_df["label"]
X_validation = validation_df[feature_columns]
y_validation = validation_df["label"]

# KNN использует все 42 признака. PCA нужен только для графика.
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)
y_pred = model.predict(X_validation)

print("Train:", X_train.shape)
print("Validation:", X_validation.shape)
print("Accuracy:", accuracy_score(y_validation, y_pred))
print(classification_report(y_validation, y_pred))
print("Порядок классов:", model.classes_)
print(confusion_matrix(y_validation, y_pred, labels=model.classes_))

# PCA обучается только на train; validation использует те же оси.
pca = PCA(n_components=2)
train_2d = pca.fit_transform(X_train)
validation_2d = pca.transform(X_validation)
variance = pca.explained_variance_ratio_

fig, ax = plt.subplots(figsize=(10, 7))
colors = plt.get_cmap("tab10")

for i, label in enumerate(sorted(df["label"].unique())):
    train_mask = (y_train == label).to_numpy()
    validation_mask = (y_validation == label).to_numpy()

    ax.scatter(
        train_2d[train_mask, 0], train_2d[train_mask, 1],
        color=colors(i), marker="o", alpha=0.5,
        label=f"{label} — train",
    )
    ax.scatter(
        validation_2d[validation_mask, 0], validation_2d[validation_mask, 1],
        color=colors(i), marker="x", s=70,
        label=f"{label} — validation",
    )

ax.set_xlabel(f"PC1 — {variance[0]:.1%} дисперсии")
ax.set_ylabel(f"PC2 — {variance[1]:.1%} дисперсии")
ax.set_title("Примеры жестов: PCA с 42 признаков на 2 оси")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(PLOT_PATH, dpi=180)

print("PCA сохраняет долю дисперсии:", f"{variance.sum():.1%}")
print("Это доля разброса данных, а не точность классификации.")
print("График сохранён:", PLOT_PATH)
plt.show()
