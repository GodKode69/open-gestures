import cv2
import mediapipe as mp
from pathlib import Path
from core.landmarks import Landmarks

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode


class HandTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        model_path = Path(__file__).parent / "hand_landmarker.task"

        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(model_path)),
            running_mode=VisionRunningMode.IMAGE,
            num_hands=1
        )

        self.landmarker = HandLandmarker.create_from_options(options)

        self.frame = None
        self.last_result = None

    def get_landmarks(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        frame = cv2.flip(frame, 1)
        self.frame = frame

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame
        )

        result = self.landmarker.detect(mp_image)
        self.last_result = result

        if not result.hand_landmarks:
            return None

        return Landmarks(result.hand_landmarks[0])

    def draw(self, gesture_name=None):
        if self.frame is None:
            return

        frame = self.frame.copy()

        if self.last_result and self.last_result.hand_landmarks:
            h, w, _ = frame.shape

            for hand_landmarks in self.last_result.hand_landmarks:
                for lm in hand_landmarks:
                    x = int(lm.x * w)
                    y = int(lm.y * h)
                    cv2.circle(frame, (x, y), 4, (0, 255, 0), -1)

        if gesture_name:
            cv2.putText(
                frame,
                f"Gesture: {gesture_name}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        cv2.imshow("Open Gestures Debug", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            self.cap.release()
            cv2.destroyAllWindows()
            raise SystemExit