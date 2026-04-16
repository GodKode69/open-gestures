from __future__ import annotations
from core.swipe_tracker import tracker

GESTURE_NAME = "swipe_down_2"

def matches(result) -> bool:
    if not result or not result.hand_landmarks:
        return False
    if len(result.hand_landmarks) != 2:
        return False
    return tracker.check("up", 2)