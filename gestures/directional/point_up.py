from detectors.orientation import OrientationDetector
det = OrientationDetector()

class PointUp:
    name = "point_up"
    mode = "continuous"
    def detect(self, landmarks):
        return det.point_up(landmarks)