"""
core/swipe_tracker.py
─────────────────────
Fixed Deep Debug Edition: Added __len__ and flicker-resistant history.
"""
from __future__ import annotations

import threading
import time
from collections import deque
from pathlib import Path
from typing import Optional

import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision
from mediapipe.tasks.python.vision.core.vision_task_running_mode import VisionTaskRunningMode

from core.config import get

LANDMARK_MODEL_PATH = Path(__file__).parent.parent / "models" / "hand_landmarker.task"
_WRIST = 0

class _HandHistory:
    def __init__(self, maxlen: int) -> None:
        self._positions: deque[tuple[float, float]] = deque(maxlen=maxlen)
        self.last_update = 0

    def push(self, x: float, y: float) -> None:
        self._positions.append((x, y))
        self.last_update = time.time()

    def clear(self) -> None:
        self._positions.clear()

    def __len__(self) -> int:
        return len(self._positions)

    def get_sampled_displacement(self) -> tuple[float, float, bool]:
        if len(self._positions) < 20:
            return 0.0, 0.0, False
            
        p0 = self._positions[0]
        p5 = self._positions[5]
        p10 = self._positions[10]
        p15 = self._positions[15]
        p_end = self._positions[-1]
        
        dx = p_end[0] - p0[0]
        dy = p_end[1] - p0[1]

        # Check for consistent movement direction
        segs = [
            (p5[0]-p0[0], p5[1]-p0[1]), 
            (p10[0]-p5[0], p10[1]-p5[1]), 
            (p15[0]-p10[0], p15[1]-p10[1]), 
            (p_end[0]-p15[0], p_end[1]-p15[1])
        ]
        
        x_con = sum(1 for s in segs if (s[0] > 0) == (dx > 0)) >= 3 if abs(dx) > 0.04 else True
        y_con = sum(1 for s in segs if (s[1] > 0) == (dy > 0)) >= 3 if abs(dy) > 0.04 else True

        return dx, dy, (x_con and y_con)

class _LandmarkSlot:
    def __init__(self) -> None:
        self._lock   = threading.Lock()
        self._result = None

    def put(self, result) -> None:
        with self._lock: self._result = result

    def get(self):
        with self._lock: return self._result

class SwipeTracker:
    def __init__(self) -> None:
        print("[SwipeTracker] Initializing Deep Debug Mode...")
        if not LANDMARK_MODEL_PATH.exists():
            raise FileNotFoundError(f"CRITICAL: Model file missing at {LANDMARK_MODEL_PATH}")

        self._slot = _LandmarkSlot()
        self._landmarker = self._build_landmarker()
        self._histories = [_HandHistory(20), _HandHistory(20)]
        self._last_trigger = 0
        self._frame_counter = 0

    def _build_landmarker(self) -> mp_vision.HandLandmarker:
        def _on_result(result, _image, _ts) -> None:
            self._slot.put(result)

        options = mp_vision.HandLandmarkerOptions(
            base_options=mp_python.BaseOptions(model_asset_path=str(LANDMARK_MODEL_PATH)),
            running_mode=VisionTaskRunningMode.LIVE_STREAM,
            num_hands=2,
            min_hand_detection_confidence=0.4, 
            min_hand_presence_confidence=0.4,
            min_tracking_confidence=0.4,
            result_callback=_on_result,
        )
        return mp_vision.HandLandmarker.create_from_options(options)

    def feed(self, mp_image: mp.Image, timestamp_ms: int) -> None:
        self._frame_counter += 1
        # Low-frequency log to prove main loop is alive
        if self._frame_counter % 60 == 0:
            print(f"[SwipeTracker] Frame {self._frame_counter} passed to AI...")
        
        self._landmarker.detect_async(mp_image, timestamp_ms)

    def detect(self) -> Optional[str]:
        result = self._slot.get()
        now = time.time()
        
        if result is None:
            return None

        # Flicker resistance: Don't clear immediately if hand is lost
        if not result.hand_landmarks:
            for h in self._histories:
                if h._positions and (now - h.last_update > 0.3):
                    h.clear()
            return None

        # We have landmarks! 
        threshold = get("swipe", "displacement_threshold", default=0.10)
        
        for i, landmarks in enumerate(result.hand_landmarks):
            if i < len(self._histories):
                self._histories[i].push(landmarks[_WRIST].x, landmarks[_WRIST].y)
                
                h_len = len(self._histories[i])
                if h_len % 5 == 0:
                    print(f"Tracking Hand {i}: {h_len}/20 samples")

                if h_len >= 20:
                    dx, dy, con = self._histories[i].get_sampled_displacement()
                    # Only log significant motion to avoid spam
                    if abs(dx) > 0.02 or abs(dy) > 0.02:
                        print(f"Hand {i} Move -> dx:{dx:.2f} dy:{dy:.2f} | Thr:{threshold} | Con:{con}")

        if now - self._last_trigger < 0.5:
            return None

        gesture = None
        if len(result.hand_landmarks) >= 1:
            dx, dy, con = self._histories[0].get_sampled_displacement()
            if con:
                direction = _classify_swipe(dx, dy, threshold)
                if direction:
                    gesture = f"swipe_{direction}_{len(result.hand_landmarks)}"

        if gesture:
            print(f"\n🔥🔥🔥 GESTURE TRIGGERED: {gesture} 🔥🔥🔥\n")
            self._last_trigger = now
            for h in self._histories: h.clear()
            return gesture

        return None

    def close(self) -> None:
        self._landmarker.close()

def _classify_swipe(dx: float, dy: float, threshold: float) -> Optional[str]:
    abs_dx, abs_dy = abs(dx), abs(dy)
    if max(abs_dx, abs_dy) < threshold: return None
    # Use a 1.5x ratio to determine horizontal vs vertical
    if abs_dx > abs_dy * 1.5: return "right" if dx > 0 else "left"
    if abs_dy > abs_dx * 1.5: return "down" if dy > 0 else "up"
    return None