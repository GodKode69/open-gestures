class GestureManager:
    def __init__(self, cooldown, confidence):
        self.cooldown = cooldown
        self.confidence = confidence
        self.actions = {}

    def register(self, gesture_name, action):
        self.actions[gesture_name] = action

    def handle(self, gesture_obj):
        name = gesture_obj.name
        mode = getattr(gesture_obj, "mode", "trigger")

        # update confidence using the gesture name
        self.confidence.update(name)
        if not self.confidence.confirmed():
            return

        action = self.actions.get(name)
        if not action:
            # no action registered
            if mode == "trigger":
                self.confidence.reset()
            return

        if mode == "trigger":
            if not self.cooldown.can_trigger(name):
                return
            action()
            self.cooldown.record_trigger(name)
            self.confidence.reset()
        else:  # continuous
            # continuous actions are executed every confirmed frame
            action()