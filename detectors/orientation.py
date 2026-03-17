class OrientationDetector:
    def point_up(self, landmarks):
        # index tip (8) above pip (6)
        return landmarks.finger_extended(8, 6)

    def point_down(self, landmarks):
        # index tip below pip
        return not landmarks.finger_extended(8, 6)

    def thumb_up(self, landmarks):
        # thumb: tip(4) is left of ip(3) in mirrored camera? use y relative to mcp
        # simpler: check if thumb tip y < thumb mcp y (higher)
        tip_y = landmarks.lm[4].y
        mcp_y = landmarks.lm[2].y
        return tip_y < mcp_y

    def thumb_down(self, landmarks):
        tip_y = landmarks.lm[4].y
        mcp_y = landmarks.lm[2].y
        return tip_y > mcp_y