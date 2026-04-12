"""
gestures/static/iloveyou_1.py
──────────────────────────────
Single-hand 🤟  ILoveYou
Action: Mute / Unmute System Audio (toggle via pactl)

Cycles the default sink mute state — works on PulseAudio and PipeWire.
No display server connection needed.
"""
from __future__ import annotations

GESTURE_LABEL = "ILoveYou"
GESTURE_NAME  = "iloveyou_1"


def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70


def action() -> None:
    try:
        import subprocess
        subprocess.Popen(
            ["pactl", "set-sink-mute", "@DEFAULT_SINK@", "1"], #1 = mute
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")