import subprocess
from actions.base import BaseAction
from actions.system import system

class Screenshot(BaseAction):
    name = "Screenshot"
    description = "Take a screenshot"
    id = "record_screen"

    def execute(self) -> None:
        sys = system()
        if sys == "linux":
            try:
                subprocess.Popen(["scrot"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as exc:
                print(f"[{self.id}] {exc}")
        elif sys == "win":
            print("hi")
        elif sys == "mac":
            try:
                subprocess.Popen(["osascript", "-e", "tell application \"System Events\" to keystroke \"4\" using {command down, shift down}"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as exc:
                print(f"[{self.id}] {exc}")
