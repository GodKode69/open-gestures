import math

class Landmarks:
    def __init__(self, lm):
        self.lm = lm

    def point(self, i):
        p = self.lm[i]
        return (p.x, p.y, p.z)

    def distance(self, a, b):
        ax, ay, _ = self.point(a)
        bx, by, _ = self.point(b)
        return math.hypot(ax - bx, ay - by)

    def finger_extended(self, tip_idx, pip_idx):
        tip_y = self.lm[tip_idx].y
        pip_y = self.lm[pip_idx].y
        return tip_y < pip_y

    def palm_center(self):
        pts = [0, 5, 17]
        xs = [self.lm[i].x for i in pts]
        ys = [self.lm[i].y for i in pts]
        return (sum(xs) / len(xs), sum(ys) / len(ys))

    def thumb_index_distance(self):
        return self.distance(4, 8)

    def is_fist(self):
        fingers = [
            self.finger_extended(8, 6),
            self.finger_extended(12, 10),
            self.finger_extended(16, 14),
            self.finger_extended(20, 18),
        ]
        return not any(fingers)

    def is_open(self):
        fingers = [
            self.finger_extended(8, 6),
            self.finger_extended(12, 10),
            self.finger_extended(16, 14),
            self.finger_extended(20, 18),
        ]
        return all(fingers)