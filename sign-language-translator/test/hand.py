from pathlib import Path
from urllib.request import urlretrieve
import time
import sys

PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

from backend.preprocessing import normalize_landmarks
from backend.collector import save_sample

import cv2
import mediapipe as mp

PROJECT_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_DIR / "models"
MODEL_PATH = MODELS_DIR / "hand_landmarker.task"

MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "hand_landmarker/hand_landmarker/float16/1/"
    "hand_landmarker.task"
)

MODELS_DIR.mkdir(parents=True, exist_ok=True)

if not MODEL_PATH.is_file():
    print("Скачиваем модель MediaPipe...")
    urlretrieve(MODEL_URL, MODEL_PATH)
    print("Модель скачана:", MODEL_PATH)


BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=str(MODEL_PATH)
    ),
    running_mode=RunningMode.VIDEO,
    num_hands=2
)


CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17)
]


cap = cv2.VideoCapture(1)

session_id = "session_01"

if not cap.isOpened():
    raise RuntimeError("Не удалось открыть камеру")

start_time = time.monotonic()
last_timestamp = -1

try:
    with HandLandmarker.create_from_options(options) as landmarker:

        while True:
            success, frame = cap.read()

            if not success:
                break

            frame = cv2.flip(frame, 1)

            rgb_frame = cv2.cvtColor(
                frame, cv2.COLOR_BGR2RGB
            )

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_frame
            )

            timestamp = int(
                (time.monotonic() - start_time) * 1000
            )
            timestamp = max(timestamp, last_timestamp + 1)
            last_timestamp = timestamp

            result = landmarker.detect_for_video(
                mp_image, timestamp
            )

            height, width = frame.shape[:2]

            for hand_index, hand in enumerate(
                result.hand_landmarks
            ):
                points = []

                for point in hand:
                    x = int(point.x * width)
                    y = int(point.y * height)
                    points.append((x, y))

                for start, end in CONNECTIONS:
                    cv2.line(
                        frame,
                        points[start],
                        points[end],
                        (255, 255, 255),
                        2
                    )

                for index, (x, y) in enumerate(points):
                    cv2.circle(
                        frame,
                        (x, y),
                        5,
                        (0, 255, 0),
                        -1
                    )

                    cv2.putText(
                        frame,
                        str(index),
                        (x + 7, y - 7),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.4,
                        (0, 255, 255),
                        1
                    )
# кисть
                features = normalize_landmarks(hand)

                if features is None:
                    continue

                print(f"Рука {hand_index + 1}")

                for index in [4, 8, 12, 16, 20]:
                    x = features[index * 2]
                    y = features[index * 2 + 1]

                    print(f"Точка {index}: x={x:.3f}, y={y:.3f}")

            cv2.imshow("Hand Tracking", frame)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            if key == ord("a"):
                if len(result.hand_landmarks) == 1:
                    features = normalize_landmarks(result.hand_landmarks[0])

                    if features is not None:
                        save_sample("C", features, session_id)
                        print("Сохранён пример буквы C")

finally:
    cap.release()
    cv2.destroyAllWindows()