from detectors.states import StateDetector
det = StateDetector()

class TwoFinger:
    name = "two_finger"
    mode = "trigger"
    def detect(self, landmarks):
        return det.two_finger(landmarks)