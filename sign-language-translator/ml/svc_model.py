from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from pathlib import Path
import pandas as pd


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "landmarks_xyz.csv"

df = pd.read_csv(DATA_PATH)


train_df = df[df["session_id"] == "session_01"]
feature_columns = []

for i in range(21):
    feature_columns.append(f"x{i}")
    feature_columns.append(f"y{i}")
    feature_columns.append(f"z{i}")

X_train = train_df[feature_columns]
y_train = train_df["label"]

validation_df = df[df["session_id"] == "session_02"]

feature_columns_1 = []

for i in range(21):
    feature_columns_1.append(f"x{i}")
    feature_columns_1.append(f"y{i}")
    feature_columns_1.append(f"z{i}")

X_validation = validation_df[feature_columns_1]
y_validation = validation_df['label']


model = make_pipeline(
    StandardScaler(),
    SVC(C=1, karnel="rbf",gamma='scale')
)



model.fit(X_train,y_train)
y_pred = model.predict(X_validation)

