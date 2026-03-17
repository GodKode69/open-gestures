import subprocess

def volume_up():
    try:
        # try pamixer or amixer
        subprocess.run(["pamixer", "--increase", "5"], check=True)
    except Exception:
        try:
            subprocess.run(["amixer", "-q", "sset", "Master", "5%+"], check=True)
        except Exception:
            print("volume up")

def volume_down():
    try:
        subprocess.run(["pamixer", "--decrease", "5"], check=True)
    except Exception:
        try:
            subprocess.run(["amixer", "-q", "sset", "Master", "5%-"], check=True)
        except Exception:
            print("volume down")