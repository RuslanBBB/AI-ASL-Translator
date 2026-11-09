from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (15, 5)

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "landmarks.csv"

fixed_df = pd.read_csv(DATA_PATH)

print(fixed_df.shape)
print(fixed_df["label"].value_counts())