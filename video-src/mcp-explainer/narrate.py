# Builds narration.wav (68s) from the cues below using kokoro-onnx.
# usage: python narrate.py <kokoro.onnx> <voices.bin> <out.wav>
import sys, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
model, voices, out = sys.argv[1:4]
k = Kokoro(model, voices)
SR, TOTAL = 24000, 68
# (start, window_end, spoken text) — windows match the on-screen captions in index.html
CUES = [
 (0.3, 5.7, "Claude, ChatGPT and other AI agents are really smart."),
 (5.7, 8.0, "But they can't reach your files or apps."),
 (8.0, 15.0, "Wiring every AI to every tool means custom glue code. Every. Single. Time."),
 (15.0, 19.5, "M C P is one open standard for that connection."),
 (19.5, 24.0, "Think USB C for AI. Build each side once, and everything plugs in."),
 (24.0, 29.0, "The host app runs an M C P client for each server."),
 (29.0, 34.0, "Each server wraps a tool or data source, offering tools, resources and prompts."),
 (34.0, 37.0, "You ask: summarise my open pull requests."),
 (37.0, 40.5, "One: the client asks the server what it can do."),
 (40.5, 43.5, "Two: the model picks the tool it needs."),
 (43.5, 47.0, "Three: the client sends the call, after you approve."),
 (47.0, 50.5, "Four: the server asks GitHub, and returns the result."),
 (50.5, 54.0, "Five: the model writes a clear answer."),
 (54.0, 61.0, "Same standard, same server. It works with Claude, ChatGPT, and any M C P capable assistant."),
 (61.0, 67.5, "Recap: host and client, servers, and one shared protocol. Learn more at A I Command Desk."),
]
buf = np.zeros(SR * TOTAL, dtype=np.float32)
for a, b, s in CUES:
    spd = 1.0
    while True:
        y, sr = k.create(s, voice="af_heart", speed=spd, lang="en-us")
        if len(y) / sr <= (b - a) - 0.25 or spd >= 1.2: break
        spd += 0.05
    i = int((a + 0.15) * SR); buf[i:i + len(y)] += y[:len(buf) - i]
    print(f"{a:5.1f} dur={len(y)/sr:4.1f}/{b-a:4.1f} speed={spd:.2f}")
sf.write(out, buf, SR)
