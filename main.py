from core.tracker import HandTracker
from logic.cooldown import Cooldown
from logic.confidence import Confidence
from logic.manager import GestureManager
from logic.controller import Controller
from gestures.export import Gestures

from actions.brightness import brightness_up, brightness_down
from actions.volume import volume_up, volume_down
from actions.media import play, pause, workspace_next, workspace_prev
from actions.zoom import zoom_in, zoom_out

def main():
    tracker = HandTracker()
    cooldown = Cooldown()
    confidence = Confidence(threshold=3)
    manager = GestureManager(cooldown, confidence)
    controller = Controller(manager)

    gest_class = Gestures()
    gestures = gest_class.get_all()

    manager.register("point_up", brightness_up)
    manager.register("point_down", brightness_down)
    manager.register("thumb_up", volume_up)
    manager.register("thumb_down", volume_down)
    manager.register("fist", pause)
    manager.register("open", play)
    manager.register("swipe_left", workspace_prev)
    manager.register("swipe_right", workspace_next)
    manager.register("pinch_in", zoom_in)
    manager.register("pinch_out", zoom_out)


    last_gesture = None

    while True:
        landmarks = tracker.get_landmarks()

        if landmarks:
            for gesture in gestures:
                if gesture.detect(landmarks):
                    last_gesture = gesture.name
                    controller.process(gesture)

        tracker.draw(last_gesture)

if __name__ == "__main__":
    main()