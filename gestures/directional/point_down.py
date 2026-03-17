from detectors.orientation import OrientationDetector
det = OrientationDetector()

class PointDown:
    name = "point_down"
    mode = "continuous"
    def detect(self, landmarks):
        return det.point_down(landmarks)