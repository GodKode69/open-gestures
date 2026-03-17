from detectors.states import StateDetector
det = StateDetector()

class ThreeFinger:
    name = "three_finger"
    mode = "trigger"
    def detect(self, landmarks):
        return det.three_finger(landmarks)