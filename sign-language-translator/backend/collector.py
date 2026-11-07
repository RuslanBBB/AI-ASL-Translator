
import csv
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "landmarks.csv"


def save_sample(label, features, session_id):
    if len(features) != 42:
        raise ValueError("Ожидалось 42 признака")

    need_header = (
        not DATA_PATH.exists()
        or DATA_PATH.stat().st_size == 0
    )

    with open(DATA_PATH, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if need_header:
            header = ["label", "session_id"]

            for i in range(21):
                header.append(f"x{i}")
                header.append(f"y{i}")

            writer.writerow(header)

        writer.writerow([label, session_id] + features)

    print("Путь к CSV:", DATA_PATH.resolve())
    print("Размер файла:", DATA_PATH.stat().st_size, "байт")