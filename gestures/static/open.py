from detectors.states import StateDetector
det = StateDetector()

class Open:
    name = "open"
    mode = "trigger"
    def detect(self, landmarks):
        return det.open(landmarks)