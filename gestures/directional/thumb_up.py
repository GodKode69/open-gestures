from detectors.orientation import OrientationDetector
det = OrientationDetector()

class ThumbUp:
    name = "thumb_up"
    mode = "trigger"
    def detect(self, landmarks):
        return det.thumb_up(landmarks)