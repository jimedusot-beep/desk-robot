"""Run: python -m unittest discover -s research_lab -p 'test_*.py' -v"""
import unittest
from research_lab.simulator import RobotLab


class LabTests(unittest.TestCase):
    def test_disarmed_startup(self):
        self.assertEqual(RobotLab().state, "DISARMED")

    def test_face_changes(self):
        lab = RobotLab()
        self.assertEqual(lab.command({"seq": 1, "type": "face", "emotion": "happy"})["emotion"], "happy")

    def test_rejects_unknown_face(self):
        self.assertEqual(RobotLab().command({"seq": 1, "type": "face", "emotion": "angry"})["reason"], "invalid-emotion")

    def test_virtual_pan_tilt(self):
        lab = RobotLab()
        self.assertEqual(lab.command({"seq": 1, "type": "move", "axis": "pan", "degrees": 20})["pan"], 20)
        self.assertEqual(lab.command({"seq": 2, "type": "move", "axis": "tilt", "degrees": -10})["tilt"], -10)

    def test_limits_and_nan(self):
        lab = RobotLab()
        self.assertEqual(lab.command({"seq": 1, "type": "move", "axis": "tilt", "degrees": 30})["reason"], "out-of-demo-range")
        self.assertEqual(lab.command({"seq": 2, "type": "move", "axis": "pan", "degrees": float("nan")})["reason"], "out-of-demo-range")

    def test_stop_blocks_motion(self):
        lab = RobotLab()
        lab.command({"seq": 8, "type": "STOP"})
        self.assertEqual(lab.command({"seq": 9, "type": "move", "axis": "pan", "degrees": 15})["reason"], "stopped")

    def test_stale_stop_always_accepted(self):
        lab = RobotLab()
        lab.command({"seq": 100, "type": "status"})
        self.assertEqual(lab.command({"seq": 1, "type": "STOP"})["state"], "STOPPED")

    def test_replay_rejected(self):
        lab = RobotLab()
        lab.command({"seq": 4, "type": "status"})
        self.assertEqual(lab.command({"seq": 4, "type": "status"})["reason"], "stale-sequence")

    def test_disconnect_and_reset(self):
        lab = RobotLab()
        self.assertEqual(lab.command({"seq": 1, "type": "disconnect"})["state"], "STOPPED")
        self.assertEqual(lab.command({"seq": 2, "type": "reset"})["state"], "DISARMED")

    def test_bad_message(self):
        self.assertEqual(RobotLab().command(None)["reason"], "invalid-message")


if __name__ == "__main__":
    unittest.main()
