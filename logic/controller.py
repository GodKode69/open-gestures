class Controller:
    def __init__(self, manager):
        self.manager = manager

    def process(self, gesture_obj):
        self.manager.handle(gesture_obj)