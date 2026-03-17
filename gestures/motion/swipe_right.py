from detectors.motion import MotionDetector
det = MotionDetector()

class SwipeRight:
    name = "swipe_right"
    mode = "trigger"
    def detect(self, landmarks):
        return det.swipe_right(landmarks)