# placeholder (not used per your list)
from detectors.motion import MotionDetector
det = MotionDetector()

class SwipeDown:
    name = "swipe_down"
    mode = "trigger"
    def detect(self, landmarks):
        return False