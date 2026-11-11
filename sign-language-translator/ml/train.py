from pathlib import Path
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (15, 5)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "landmarks.csv"

# fixed_df = pd.read_csv(DATA_PATH) кол-во букв в датасете

# print(fixed_df.shape)
# print(fixed_df["label"].value_counts())


df = pd.read_csv(DATA_PATH)

# обучение

# print(df.head()) тут табличка наша разделенная удобно
# print(df.shape) первые 5 строк

# print(df.columns)

# print(df.dtypes) типы данных

print(df.info)


model = KNeighborsClassifier(n_neighbors=5)

# X = df( colomns = ['session_1',])

# model.fit(X_train, y_train)
# predictions = model.predict(X_check)

# KNeighborsClassifier(
#     n_neighbors=5,
#     weights="uniform",
# )