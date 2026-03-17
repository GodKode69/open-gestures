class StateDetector:
    def fist(self, landmarks):
        return landmarks.is_fist()

    def open(self, landmarks):
        return landmarks.is_open()

    def two_finger(self, landmarks):
        # two_finger = index + middle extended, others folded
        idx = landmarks.finger_extended(8, 6)
        mid = landmarks.finger_extended(12, 10)
        ring = landmarks.finger_extended(16, 14)
        pinky = landmarks.finger_extended(20, 18)
        return idx and mid and (not ring) and (not pinky)

    def three_finger(self, landmarks):
        # index, middle, ring extended
        idx = landmarks.finger_extended(8, 6)
        mid = landmarks.finger_extended(12, 10)
        ring = landmarks.finger_extended(16, 14)
        pinky = landmarks.finger_extended(20, 18)
        return idx and mid and ring and (not pinky)