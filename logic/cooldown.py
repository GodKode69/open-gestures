import time

class Cooldown(object):
    def __init__(self):
        self.static = {
            "fist": 0.25,
            "open": 0.25,
            "two_finger": 2, #screenshot
            "three_finger": 2, #selfie
        }
        self.motion = {
            "swipe_left": 0.5,
            "swipe_right": 0.5,
            "swipe_up": 0.5,
            "swipe_down": 0.5,
        }
        self.directional = {
            "point_up": 0.1,
            "point_down": 0.1,
            "thumb_down": 0.1,
            "thumb_up": 0.1
        }
        self.last_trigger = {}
    
    def record_trigger(self, gesture):
        now = time.monotonic()
        self.last_trigger[gesture] = now    

    def can_trigger(self, gesture):
        now = time.monotonic()

        if gesture in self.static:
            cooldown = self.static[gesture]
        elif gesture in self.motion:
            cooldown = self.motion[gesture]
        elif gesture in self.directional:
            cooldown = self.directional[gesture]
        else:
            return False

        if gesture not in self.last_trigger:
            return True

        elapsed = now - self.last_trigger[gesture]

        return elapsed >= cooldown