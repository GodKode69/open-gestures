from detectors.orientation import OrientationDetector
det = OrientationDetector()

class ThumbDown:
    name = "thumb_down"
    mode = "trigger"
    def detect(self, landmarks):
        return det.thumb_down(landmarks)