from __future__ import annotations
import pythoncom
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

GESTURE_LABEL = "Thumb_Up"
GESTURE_NAME  = "thumb_up_1"

def matches(result) -> bool:
    if not result.gestures or len(result.gestures) != 1:
        return False
    top = result.gestures[0][0]
    return top.category_name == GESTURE_LABEL and top.score >= 0.70

def action() -> None:
    try:
        pythoncom.CoInitialize()
        # GetSpeakers() returns an AudioDevice wrapper — access raw COM device via ._dev
        devices = AudioUtilities.GetSpeakers()
        interface = devices._dev.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current_vol = volume.GetMasterVolumeLevelScalar()
        volume.SetMasterVolumeLevelScalar(min(1.0, current_vol + 0.05), None)
    except Exception as exc:
        print(f"[{GESTURE_NAME}] {exc}")
    finally:
        pythoncom.CoUninitialize()