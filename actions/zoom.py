import subprocess

def zoom_in():
    try:
        subprocess.run(["xdotool", "key", "ctrl+plus"], check=True)
    except Exception:
        print("zoom in")

def zoom_out():
    try:
        subprocess.run(["xdotool", "key", "ctrl+minus"], check=True)
    except Exception:
        print("zoom out")