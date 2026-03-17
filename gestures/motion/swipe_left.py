from detectors.motion import MotionDetector
det = MotionDetector()

class SwipeLeft:
    name = "swipe_left"
    mode = "trigger"
    def detect(self, landmarks):
        return det.swipe_left(landmarks)