"""Deterministic software-only face, pan/tilt and controller-message experiments.

Does not import firmware, networking, GPIO, servos or hardware drivers.
"""
from dataclasses import dataclass, field

EMOTIONS = {"neutral", "happy", "sad", "surprised", "sleepy", "thinking"}
LIMITS = {"pan": (-60.0, 60.0), "tilt": (-60.0, 0.0)}  # V1 demo envelope ONLY, not H.E.R.B.I.E. limits


@dataclass
class RobotLab:
    state: str = "DISARMED"
    emotion: str = "neutral"
    pan: float = 0.0
    tilt: float = 0.0
    last_seq: int = -1
    events: list = field(default_factory=list)

    def command(self, msg):
        """Return a simulated ACK; STOP takes precedence over sequencing."""
        if not isinstance(msg, dict):
            return self._ack(False, "invalid-message")
        kind = msg.get("type")
        if kind == "STOP":
            self.state = "STOPPED"
            self.events.append("stop")
            return self._ack(True)
        seq = msg.get("seq")
        if type(seq) is not int or seq < 0:
            return self._ack(False, "invalid-sequence")
        if seq <= self.last_seq:
            return self._ack(False, "stale-sequence")
        if kind not in {"face", "move", "status", "reset", "disconnect"}:
            return self._ack(False, "unknown-command")
        self.last_seq = seq
        if kind == "disconnect":
            self.state = "STOPPED"
            self.events.append("disconnect")
        elif kind == "reset":
            if self.state != "STOPPED":
                return self._ack(False, "not-stopped")
            self.state = "DISARMED"
        elif kind == "face":
            name = msg.get("emotion")
            if name not in EMOTIONS:
                return self._ack(False, "invalid-emotion")
            self.emotion = name
            self.events.append("face:" + name)
        elif kind == "move":
            axis = msg.get("axis")
            value = msg.get("degrees")
            if axis not in LIMITS or type(value) not in (int, float):
                return self._ack(False, "invalid-motion")
            low, high = LIMITS[axis]
            if not low <= value <= high:
                return self._ack(False, "out-of-demo-range")
            if self.state == "STOPPED":
                return self._ack(False, "stopped")
            setattr(self, axis, float(value))
            self.events.append("virtual-" + axis)
        return self._ack(True)

    def _ack(self, ok, reason=None):
        result = {"ok": ok, "simulated": True, "state": self.state,
                  "pan": self.pan, "tilt": self.tilt, "emotion": self.emotion}
        if reason:
            result["reason"] = reason
        return result
