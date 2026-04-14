import subprocess
from actions.base import BaseAction
from actions.system import system

class VolumeDown(BaseAction):
    name = "Volume Down"
    description = "Decrease system volume"
    id = "volume_down"

    def execute(self) -> None:
        sys = system()
        if sys == "linux":
            try:
                subprocess.Popen(["pactl", "set-sink-volume", "@DEFAULT_SINK@", "-10%"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as exc:
                print(f"[{self.id}] {exc}")
        elif sys == "win":
            print("hi")
        elif sys == "mac":
            try:
                subprocess.Popen(["osascript", "-e", "set volume output volume (output volume of (get volume settings) - 10)"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as exc:
                print(f"[{self.id}] {exc}")
