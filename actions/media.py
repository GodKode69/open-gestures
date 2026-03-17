import subprocess
import json

def play():
    try:
        subprocess.run(["playerctl", "play"], check=True)
    except Exception:
        print("play")

def pause():
    try:
        subprocess.run(["playerctl", "pause"], check=True)
    except Exception:
        print("pause")

def workspace_next():
    # try sway first (Wayland)
    try:
        subprocess.run(["swaymsg", "workspace", "next"], check=True)
        return
    except Exception:
        pass

    # fallback: try i3
    try:
        subprocess.run(["i3-msg", "workspace", "next"], check=True)
    except Exception:
        print("workspace next")

def workspace_prev():
    try:
        subprocess.run(["swaymsg", "workspace", "prev"], check=True)
        return
    except Exception:
        pass

    try:
        subprocess.run(["i3-msg", "workspace", "prev"], check=True)
    except Exception:
        print("workspace prev")