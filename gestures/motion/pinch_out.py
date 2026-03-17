from detectors.motion import MotionDetector
det = MotionDetector()

class PinchOut:
    name = "pinch_out"
    mode = "trigger"
    def detect(self, landmarks):
        return det.pinch_out(landmarks)