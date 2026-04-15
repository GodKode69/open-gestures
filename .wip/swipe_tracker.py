"""
core/swipe_tracker.py
─────────────────────
Quadrant + time-window swipe detection.

Coordinate system (normalized, matches MediaPipe):
    (0,0) = top-left corner of frame
    (1,1) = bottom-right corner of frame

Zones (used to decide whether a swipe occurred):
    LEFT  zone : x < 0.35
    RIGHT zone : x > 0.65
    UP    zone : y < 0.35   (y=0 is top in MediaPipe)
    DOWN  zone : y > 0.65

A swipe fires when the wrist enters the OPPOSITE zone from where it
started within WINDOW_SECONDS. The center band (0.35–0.65) acts as a
dead zone, ensuring the hand must travel a meaningful distance.

Usage (from a gesture module):
    from core.swipe_tracker import tracker
    fired = tracker.check("left", num_hands)   # returns True once per swipe
"""
from __future__ import annotations

import time
from collections import deque
from typing import Optional

# ── Tunable constants ──────────────────────────────────────────────────────

WINDOW_SECONDS   = 0.4   # how long a swipe attempt can last
COOLDOWN_SECONDS = 0.6   # minimum gap between two swipe triggers
STALE_SECONDS    = 0.3   # drop history if hand disappears for this long

# Zone boundaries
_LEFT_MAX  = 0.35
_RIGHT_MIN = 0.65
_UP_MAX    = 0.35
_DOWN_MIN  = 0.65

# Opposite zone pairs that constitute a valid swipe
_OPPOSITES = {
    "left":  "right",   # start in right zone → end in left zone
    "right": "left",
    "up":    "down",
    "down":  "up",
}

# ── Helpers ────────────────────────────────────────────────────────────────

def _zone_of(x: float, y: float) -> Optional[str]:
    """Return the zone name for a normalised wrist position, or None (centre)."""
    if x < _LEFT_MAX:
        return "left"
    if x > _RIGHT_MIN:
        return "right"
    if y < _UP_MAX:
        return "up"
    if y > _DOWN_MIN:
        return "down"
    return None   # centre dead zone


# ── Per-hand history ───────────────────────────────────────────────────────

class _HandHistory:
    """Stores (timestamp, x, y) samples within the rolling time window."""

    def __init__(self) -> None:
        # Each entry: (timestamp_float, x_float, y_float)
        self._buf: deque[tuple[float, float, float]] = deque()
        self.last_update: float = 0.0

    def push(self, x: float, y: float) -> None:
        now = time.monotonic()
        self._buf.append((now, x, y))
        self.last_update = now
        self._prune(now)

    def _prune(self, now: float) -> None:
        """Drop samples older than WINDOW_SECONDS."""
        cutoff = now - WINDOW_SECONDS
        while self._buf and self._buf[0][0] < cutoff:
            self._buf.popleft()

    def clear(self) -> None:
        self._buf.clear()

    def check_swipe(self, direction: str, debug: bool = False) -> bool:
        """
        Return True if samples within the window show a swipe in `direction`.

        Logic:
          - The oldest sample in the window must be in the *start* zone for
            `direction` (i.e. the zone you leave to swipe that way).
          - The newest sample must be in the *destination* zone (opposite).
          - At least one intermediate sample must have passed through centre
            (ensuring the hand crossed the dead zone, not just noise).
        """
        if len(self._buf) < 2:
            if debug:
                print(f"  [tracker] check_swipe({direction}): FAIL — only {len(self._buf)} sample(s) in window")
            return False

        start_zone = _OPPOSITES[direction]   # where the hand starts
        end_zone   = direction               # where the hand must end up

        oldest = self._buf[0]
        newest = self._buf[-1]

        oldest_zone = _zone_of(oldest[1], oldest[2])
        newest_zone = _zone_of(newest[1], newest[2])

        if debug:
            zone_trail = [_zone_of(e[1], e[2]) or "centre" for e in self._buf]
            # Condense consecutive duplicates for readability
            condensed = [zone_trail[0]]
            for z in zone_trail[1:]:
                if z != condensed[-1]:
                    condensed.append(z)
            print(
                f"  [tracker] check_swipe({direction}): "
                f"{len(self._buf)} samples | "
                f"oldest=({oldest[1]:.2f},{oldest[2]:.2f}) zone={oldest_zone or 'centre'} | "
                f"newest=({newest[1]:.2f},{newest[2]:.2f}) zone={newest_zone or 'centre'} | "
                f"trail={' → '.join(condensed)}"
            )

        if oldest_zone != start_zone:
            if debug:
                print(f"  [tracker]   ✗ start zone wrong — need '{start_zone}', got '{oldest_zone or 'centre'}'")
            return False

        if newest_zone != end_zone:
            if debug:
                print(f"  [tracker]   ✗ end zone wrong — need '{end_zone}', got '{newest_zone or 'centre'}'")
            return False

        # Verify at least one frame passed through the centre dead zone
        crossed_centre = any(
            _zone_of(entry[1], entry[2]) is None
            for entry in self._buf
        )

        if debug:
            if crossed_centre:
                print(f"  [tracker]   ✓ crossed centre — SWIPE {direction.upper()} VALID")
            else:
                print(f"  [tracker]   ✗ never crossed centre dead zone — swipe rejected")

        return crossed_centre


# ── Shared singleton tracker ───────────────────────────────────────────────

class SwipeTracker:
    """
    Singleton shared across all swipe gesture modules.

    main.py feeds wrist positions every frame via `feed()`.
    Gesture modules call `check(direction, num_hands)` which returns True
    exactly once per detected swipe (then resets history + cooldown).
    """

    def __init__(self) -> None:
        # Two slots — hand 0 and hand 1
        self._histories: list[_HandHistory] = [_HandHistory(), _HandHistory()]
        self._last_trigger: float = 0.0
        self._feed_count: int = 0   # counts feed() calls for periodic logging

    # ── Called by main.py each frame ───────────────────────────────────────

    def feed(self, hand_landmarks_list: list) -> None:
        """
        Accept a list of hand landmark objects from the GestureRecognizer
        result (result.hand_landmarks). Each element is a list of landmarks;
        landmark[0] is the wrist (WRIST = 0).

        Stale histories (hand lost for > STALE_SECONDS) are cleared here.
        """
        now = time.monotonic()
        self._feed_count += 1

        active_indices = set(range(len(hand_landmarks_list)))

        for i, hist in enumerate(self._histories):
            if i in active_indices:
                wrist = hand_landmarks_list[i][0]
                hist.push(wrist.x, wrist.y)
                # Log wrist position every 30 feeds so you can see live coords
                if self._feed_count % 30 == 0:
                    zone = _zone_of(wrist.x, wrist.y) or "centre"
                    buf_len = len(hist._buf)
                    print(
                        f"[tracker] hand{i} wrist=({wrist.x:.2f}, {wrist.y:.2f}) "
                        f"zone={zone:6s}  buf={buf_len} samples"
                    )
            else:
                # Clear only if the hand has been gone long enough
                if hist.last_update and (now - hist.last_update) > STALE_SECONDS:
                    hist.clear()

    # ── Called by gesture modules ──────────────────────────────────────────

    def check(self, direction: str, num_hands: int) -> bool:
        """
        Returns True if a swipe in `direction` is detected with `num_hands`
        hands visible. Fires at most once per COOLDOWN_SECONDS.

        `direction` must be one of: "left", "right", "up", "down"
        `num_hands` is 1 or 2 (matches the _1 / _2 gesture name suffix).

        For single-hand swipes, verbose debug is printed on every check so
        you can see exactly which condition fails.
        """
        debug = (num_hands == 1)   # only log for _1 gestures to avoid spam
        now = time.monotonic()

        cooldown_remaining = COOLDOWN_SECONDS - (now - self._last_trigger)
        if cooldown_remaining > 0:
            if debug:
                print(f"[tracker] check({direction}, {num_hands}): on cooldown ({cooldown_remaining:.2f}s left)")
            return False

        # For a two-hand swipe both hands must agree; for one-hand only hand 0
        hands_to_check = self._histories[:num_hands]
        if debug:
            print(f"[tracker] check({direction}, {num_hands}): evaluating hand0 history ({len(hands_to_check[0]._buf)} samples in window)")

        if not all(h.check_swipe(direction, debug=debug) for h in hands_to_check):
            return False

        # Trigger — reset histories and record cooldown
        print(f"\n[tracker] ✅ SWIPE {direction.upper()}_{num_hands} FIRED\n")
        self._last_trigger = now
        for h in self._histories:
            h.clear()

        return True

    # kept for compatibility with main.py calling swiper.close()
    def close(self) -> None:
        pass


# Module-level singleton — imported by every gesture module
tracker = SwipeTracker()