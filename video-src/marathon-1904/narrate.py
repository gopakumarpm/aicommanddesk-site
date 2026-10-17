# Builds narration.wav + timings.json (line start/end times) for the 1904 marathon story using kokoro-onnx.
# usage: python narrate.py <kokoro.onnx> <voices.bin> <out_dir>
import sys, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro
model, voices, out = sys.argv[1:4]
k = Kokoro(model, voices)
SR = 24000
LINES = [
 "St. Louis, August nineteen oh four. The Olympic marathon is about to begin, and it will become the strangest race in history.",
 "It was ninety degrees. The roads were dust. And there was only one water stop on the whole course.",
 "Among the runners was Felix Carvajal, a Cuban mailman, with no money, no coach, and no running shoes.",
 "To reach America, he ran laps around Havana while the crowd tossed him coins. Then he lost it all gambling, and had to hitchhike.",
 "He arrived in street clothes. So another athlete grabbed a pair of scissors, and cut his trousers into shorts.",
 "The gun went off, and Felix ran. And then he stopped, to chat with the spectators.",
 "Then he spotted an orchard, and ate some apples. They were rotten.",
 "So he lay down, for a nap.",
 "Meanwhile, up front, it was chaos. Fred Lorz rode in a car for eleven miles, then jogged into the stadium, to cheers.",
 "He was found out. The real winner, Thomas Hicks, was kept going by his trainers with brandy and strychnine, and was practically carried over the line.",
 "Len Tau, a Tswana runner, was reportedly chased a mile off course by wild dogs, and still finished ninth.",
 "And Felix? He woke up, and ran on, all the way to fourth place.",
 "No money. No coach. No shoes. And he came fourth in an Olympic marathon. Never underestimate someone who simply shows up.",
]
GAP = 0.55
chunks, timings, t = [], [], 0.6
for i, s in enumerate(LINES):
    y, sr = k.create(s, voice="bm_george", speed=0.96, lang="en-us")
    timings.append({"start": round(t, 3), "end": round(t + len(y) / sr, 3), "text": s})
    chunks.append((t, y))
    t += len(y) / sr + GAP
total = round(t + 2.0, 2)
buf = np.zeros(int(SR * total), dtype=np.float32)
for st, y in chunks:
    i = int(st * SR); buf[i:i + len(y)] += y
sf.write(f"{out}/narration.wav", buf, SR)
json.dump({"total": total, "lines": timings}, open(f"{out}/timings.json", "w"), indent=1)
print(total, [(round(l['start'], 1), round(l['end'], 1)) for l in timings])
