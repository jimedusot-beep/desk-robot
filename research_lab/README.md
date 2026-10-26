# Rocky V1 × H.E.R.B.I.E. Software Laboratory

**SIMULATION ONLY — no physical movement, GPIO, servo driver, hardware wiring or Wi-Fi connection.**

This branch is derived from the original [cgro00/desk-robot V1](https://github.com/cgro00/desk-robot/releases/tag/v1.0) and remains in the owner's separate Rocky fork. Original upstream code is licensed under MIT; retain the upstream LICENSE. This research lab contains new isolated Python code, not a copy of Rocky's firmware.

## Three experiments

1. **Face state:** send `{"seq":1,"type":"face","emotion":"happy"}`. The virtual state changes. The original Rocky OLED rendering is not used or driven.
2. **Virtual pan/tilt:** send `{"seq":2,"type":"move","axis":"pan","degrees":20}`. Only Python numbers change. Demo envelope (-60..60 pan, -60..0 tilt) comes from Rocky V1 and **is not an approved H.E.R.B.I.E. mechanical limit**.
3. **Host/controller messages:** send dictionaries to `RobotLab.command`. Receive simulated ACK/state; reject stale sequences, validate payloads, latch STOP and disconnect, and reset to DISARMED. This is an experiment, **not** Rocky's WebSocket protocol or a hardware-safety implementation.

## Run without dependencies

```bash
python -m unittest discover -s research_lab -p 'test_*.py' -v
python -c "from research_lab.simulator import RobotLab; r=RobotLab(); print(r.command({'seq':1,'type':'face','emotion':'happy'})); print(r.command({'seq':2,'type':'move','axis':'pan','degrees':20})); print(r.command({'type':'STOP'}))"
```

No API keys or electronics are required. The lab does not import or call Rocky firmware or brain server. The original project files are unchanged.

## Safety / scope

The simulation does **not** establish a physical emergency stop, watchdog, mechanical clearance, electrical safety or suitability of any controller. A simulated `reset` is not permission to arm hardware. Do not flash or wire anything based on this experiment.

Do not merge this lab into H.E.R.B.I.E. or Cyborg without separate technical and licensing review. Cyborg PR #16 remains unmerged.
