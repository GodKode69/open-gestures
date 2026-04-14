import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import subprocess
from actions.base import BaseAction
from actions.system import system

class PlayMedia(BaseAction):
    name = "Play Media"
    description = "Play system media"
    id = "play_media"

    def execute(self) -> None:
        sys = system()
        
        if sys=="linux":
            try:
                subprocess.Popen(
                    ["playerctl", "play"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except Exception as exc:
                print(f"[{self.id}] {exc}")
        elif sys=="win":
            #code here
            print("hi")
        elif sys=="mac":
            try:
                subprocess.Popen(
                    ["osascript", "-e", "tell application \"System Events\" to key code 16"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                )
            except Exception as exc:
                print(f"[{self.id}] {exc}")
 
          
