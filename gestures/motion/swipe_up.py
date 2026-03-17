# placeholder (not used per your list)
from detectors.motion import MotionDetector
det = MotionDetector()

class SwipeUp:
    name = "swipe_up"
    mode = "trigger"
    def detect(self, landmarks):
        return False