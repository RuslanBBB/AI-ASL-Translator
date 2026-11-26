from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from pathlib import Path
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report
import numpy as np


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "landmarks_xyz.csv"

df = pd.read_csv(DATA_PATH)


df["index_middle_distance"] = np.sqrt(
    (df["x8"] - df["x12"]) ** 2
    + (df["y8"] - df["y12"]) ** 2
    + (df["z8"] - df["z12"]) ** 2
)

df["tip_dx"] = df["x8"] - df["x12"]
df["middle_dx"] = df["x7"] - df["x11"]

df["fingers_crossed"] = (
    df["tip_dx"] * df["middle_dx"] < 0
).astype(int)

def landmark_distance(df, point_a, point_b):
    return np.sqrt(
        (df[f"x{point_a}"] - df[f"x{point_b}"]) ** 2
        + (df[f"y{point_a}"] - df[f"y{point_b}"]) ** 2
        + (df[f"z{point_a}"] - df[f"z{point_b}"]) ** 2
    )


def finger_straightness(df, mcp, pip, dip, tip):
    direct_distance = landmark_distance(df, mcp, tip)

    finger_length = (
        landmark_distance(df, mcp, pip)
        + landmark_distance(df, pip, dip)
        + landmark_distance(df, dip, tip)
    )

    return direct_distance / (finger_length + 1e-8)

df["index_straightness"] = finger_straightness(
    df, 5, 6, 7, 8
)

df["middle_straightness"] = finger_straightness(
    df, 9, 10, 11, 12
)

df["pinky_straightness"] = finger_straightness(
    df, 17, 18, 19, 20
)

train_df = df[df["session_id"] == "session_01"]
feature_columns = []

for i in range(21):
    feature_columns.append(f"x{i}")
    feature_columns.append(f"y{i}")
    feature_columns.append(f"z{i}")

feature_columns.extend([
    "index_middle_distance",
    "tip_dx",
    "middle_dx",
    "fingers_crossed",
    "index_straightness",
    "middle_straightness",
    "pinky_straightness",
])

X_train = train_df[feature_columns]
y_train = train_df["label"]

validation_df = df[df["session_id"] == "session_02"]

X_validation = validation_df[feature_columns]

model = make_pipeline(
    StandardScaler(),
    SVC(C=100, kernel="rbf",gamma='scale')
)


model.fit(X_train,y_train)
y_validation = validation_df["label"]
y_pred = model.predict(X_validation)

print("Accuracy:", accuracy_score(y_validation, y_pred))
print(classification_report(y_validation, y_pred, zero_division=0))
