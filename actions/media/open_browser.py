import subprocess
from actions.base import BaseAction
from actions.system import system

class OpenBrowser(BaseAction):
    name = "Open Browser"
    description = "Open the default web browser"
    id = "open_browser"

    def execute(self) -> None:
        sys = system()
        if sys == "linux":
            try:
                subprocess.Popen(["xdg-open", "https://"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as exc:
                print(f"[{self.id}] {exc}")
        elif sys == "win":
            print("hi")
        elif sys == "mac":
            try:
                subprocess.Popen(["open", "-a", "Safari"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as exc:
                print(f"[{self.id}] {exc}")
