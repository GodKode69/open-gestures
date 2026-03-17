from detectors.motion import MotionDetector
det = MotionDetector()

class PinchIn:
    name = "pinch_in"
    mode = "trigger"
    def detect(self, landmarks):
        return det.pinch_in(landmarks)