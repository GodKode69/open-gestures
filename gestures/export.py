from gestures.static.fist import Fist
from gestures.static.open import Open
#from gestures.static.two_finger import TwoFinger
#from gestures.static.three_finger import ThreeFinger

from gestures.motion.swipe_left import SwipeLeft
from gestures.motion.swipe_right import SwipeRight
from gestures.motion.swipe_up import SwipeUp
from gestures.motion.swipe_down import SwipeDown

from gestures.directional.point_up import PointUp
from gestures.directional.point_down import PointDown
from gestures.directional.thumb_up import ThumbUp
from gestures.directional.thumb_down import ThumbDown


class Gestures:
    def __init__(self):
        self.gestures = [
            Fist(),
            Open(),
            #TwoFinger(),
            #ThreeFinger(),
            SwipeLeft(),
            SwipeRight(),
            SwipeUp(),
            SwipeDown(),
            PointUp(),
            PointDown(),
            ThumbUp(),
            ThumbDown(),
        ]

    def get_all(self):
        return self.gestures