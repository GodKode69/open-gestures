import subprocess
from actions.base import BaseAction
from actions.system import system

class OpenFiles(BaseAction):
    name = "Open Files"
    description = "Open Finder"
    id = "open_files"

    def execute(self) -> None:
        sys = system()
        if sys == "linux":
            try:
                subprocess.Popen(["xdg-open", "."], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as exc:
                print(f"[{self.id}] {exc}")
        elif sys == "win":
            print("hi")
        elif sys == "mac":
            try:
                subprocess.Popen(["open", "-a", "Finder"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as exc:
                print(f"[{self.id}] {exc}")
