from detectors.states import StateDetector
det = StateDetector()

class Fist:
    name = "fist"
    mode = "trigger"
    def detect(self, landmarks):
        return det.fist(landmarks)