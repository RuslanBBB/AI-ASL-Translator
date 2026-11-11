from pathlib import Path
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (15, 5)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "landmarks.csv"

# fixed_df = pd.read_csv(DATA_PATH) кол-во букв в датасете

# print(fixed_df.shape)
# print(fixed_df["label"].value_counts())


df = pd.read_csv(DATA_PATH)

# обучение

# print(df.head()) первые 5 строк
# print(df.shape) тут табличка наша разделенная удобно

# print(df.columns)

# print(df.dtypes) типы данных

# print(df.info) проверка на пустые значения в столбцах






train_df = df[df["session_id"] == "session_01"]

feature_columns = []

for i in range(21):
    feature_columns.append(f"x{i}")
    feature_columns.append(f"y{i}")

X_train = train_df[feature_columns]
y_train = train_df["label"]

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

KNeighborsClassifier(
    n_neighbors=5,
    weights="uniform",
)

validation_df = df[df["session_id"] == "session_02"]

feature_columns_1 = []

for i in range(21):
    feature_columns_1.append(f"x{i}")
    feature_columns_1.append(f"y{i}")


X_validation = validation_df[feature_columns_1]
y_validation = validation_df['label']

y_pred = model.predict(X_validation)

# print("Предсказания:", y_pred)
# print("Правильные ответы:", y_validation.to_numpy())

print("Accuracy:", accuracy_score(y_validation, y_pred))

print(classification_report(y_validation, y_pred))

print("Порядок классов:", model.classes_)
print(confusion_matrix(
    y_validation,
    y_pred,
    labels=model.classes_,
))