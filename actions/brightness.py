import subprocess

def brightness_up(step="10%"):
    try:
        subprocess.run(["brightnessctl", "set", f"+{step}"], check=True)
    except Exception:
        # fallback
        print("brightness up (fallback)")

def brightness_down(step="10%"):
    try:
        subprocess.run(["brightnessctl", "set", f"-{step}"], check=True)
    except Exception:
        print("brightness down (fallback)")