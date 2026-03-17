class MotionDetector:
    def __init__(self):
        self.prev_x = None
        self.prev_y = None
        self.prev_pinch = None

    def update_prev(self, landmarks):
        cx, cy = landmarks.palm_center()
        self.prev_x = cx if self.prev_x is None else self.prev_x
        self.prev_y = cy if self.prev_y is None else self.prev_y
        self.prev_pinch = landmarks.thumb_index_distance() if self.prev_pinch is None else self.prev_pinch

    def swipe_left(self, landmarks, threshold=0.06):
        cx, _ = landmarks.palm_center()
        if self.prev_x is None:
            self.prev_x = cx
            return False
        dx = cx - self.prev_x
        self.prev_x = cx
        return dx < -threshold

    def swipe_right(self, landmarks, threshold=0.06):
        cx, _ = landmarks.palm_center()
        if self.prev_x is None:
            self.prev_x = cx
            return False
        dx = cx - self.prev_x
        self.prev_x = cx
        return dx > threshold

    def pinch_in(self, landmarks, threshold=0.02):
        d = landmarks.thumb_index_distance()
        if self.prev_pinch is None:
            self.prev_pinch = d
            return False
        dd = d - self.prev_pinch
        self.prev_pinch = d
        return dd < -threshold  # distance reducing => pinch in

    def pinch_out(self, landmarks, threshold=0.02):
        d = landmarks.thumb_index_distance()
        if self.prev_pinch is None:
            self.prev_pinch = d
            return False
        dd = d - self.prev_pinch
        self.prev_pinch = d
        return dd > threshold  # distance increasing => pinch out