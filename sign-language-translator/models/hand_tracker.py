
import cv2
import mediapipe as mp
import time

from pathlib import Path

print("Рабочая директория:", Path.cwd())
print("Файл существует:", Path("models/hand_landmarker.task").is_file())

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path="models/hand_landmarker.task"
    ),
    running_mode=RunningMode.VIDEO,
    num_hands=1
)

cap = cv2.VideoCapture(1)

with HandLandmarker.create_from_options(options) as landmarker:
    try:
        while cap.isOpened():
            success, frame = cap.read()

            if not success:
                break

            rgb_frame = cv2.cvtColor(
                frame, cv2.COLOR_BGR2RGB
            )

            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB,
                data=rgb_frame
            )

            timestamp_ms = int(time.monotonic() * 1000)

            result = landmarker.detect_for_video(
                mp_image, timestamp_ms
            )

            height, width = frame.shape[:2]

            for hand in result.hand_landmarks:
                for point in hand:
                    x = int(point.x * width)
                    y = int(point.y * height)

                    cv2.circle(
                        frame, (x, y), 5,
                        (0, 255, 0), -1
                    )

            cv2.imshow("Hand Tracker", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
