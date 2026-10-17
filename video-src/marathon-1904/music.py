# Synthesises a period-style ragtime backing track + a few sound effects (no external assets).
# usage: python music.py <timings.json> <out_music.wav> <out_sfx.wav>
import sys, json, numpy as np, soundfile as sf
tj, out_m, out_s = sys.argv[1:4]
T = json.load(open(tj)); SR = 24000; total = T["total"]; N = int(SR * total)
rng = np.random.default_rng(4)
def note(f, dur, vel=1.0):
    t = np.arange(int(SR * dur)) / SR
    y = sum(a * np.sin(2 * np.pi * f * k * t) * np.exp(-t * (3 + k * 2.2)) for k, a in [(1, 1), (2, .5), (3, .28), (4, .14), (5, .08)])
    y += .25 * np.sin(2 * np.pi * f * 1.004 * t) * np.exp(-t * 4)
    y *= np.minimum(1, t * 400)
    return (y * vel).astype(np.float32)
mid = lambda m: 440 * 2 ** ((m - 69) / 12)
bpm = 92; beat = 60 / bpm
prog = [(45, [57, 60, 64]), (41, [57, 60, 65]), (48, [55, 60, 64]), (40, [56, 59, 64])]  # Am F C E
melody = [[76, 74, 72, 74], [77, 76, 74, 72], [79, 76, 72, 76], [76, 74, 71, 68]]
m = np.zeros(N, dtype=np.float32)
def put(y, s):
    i = int(s * SR)
    if i < N: m[i:i + len(y)] += y[:N - i]
bar = 0; t = 0.0
while t < total:
    bass, chord = prog[bar % 4]
    for b in range(4):
        tb = t + b * beat
        if b in (0, 2): put(note(mid(bass if b == 0 else bass + 7), beat * 1.6, .55), tb)
        else:
            for n in chord: put(note(mid(n), beat * .9, .16), tb)
        put(note(mid(melody[bar % 4][b]), beat * 1.4, .2), tb + (0.03 if b % 2 else 0))
    t += 4 * beat; bar += 1
env = np.minimum(1, np.arange(N) / (SR * 2)) * np.minimum(1, (N - np.arange(N)) / (SR * 3))
m *= env.astype(np.float32); m /= max(1e-6, np.abs(m).max()); m *= .5
sf.write(out_m, m, SR)
# --- sfx ---
SC = [0] + [l["start"] - .3 for l in T["lines"][1:]] + [total]
s = np.zeros(N, dtype=np.float32)
def sput(y, at):
    i = int(at * SR)
    if 0 <= i < N: s[i:i + len(y)] += y[:N - i]
def gun():
    n = int(SR * .5); t = np.arange(n) / SR
    return (rng.standard_normal(n) * np.exp(-t * 14) * .9 + np.sin(2 * np.pi * 70 * t) * np.exp(-t * 9) * .8).astype(np.float32)
def snip():
    n = int(SR * .06); t = np.arange(n) / SR
    return (rng.standard_normal(n) * np.exp(-t * 90) * .6 * np.sin(2 * np.pi * 3500 * t)).astype(np.float32)
def crunch():
    out = np.zeros(int(SR * .5), dtype=np.float32)
    for k in range(4):
        n = int(SR * .08); t = np.arange(n) / SR
        c = (rng.standard_normal(n) * np.exp(-t * 40) * .5).astype(np.float32); out[int(k * SR * .11):int(k * SR * .11) + n] += c
    return out
def thud():
    n = int(SR * .3); t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 90 * t) * np.exp(-t * 12) * .7).astype(np.float32)
d4 = SC[5] - SC[4]
sput(snip(), SC[4] + .55 * d4 - .08); sput(snip(), SC[4] + .55 * d4 + .02)
sput(gun(), SC[5] + .6)
d6 = SC[7] - SC[6]
for k in (.3, .38, .46): sput(crunch(), SC[6] + k * d6)
sput(thud(), SC[8] + (SC[9] - SC[8]) * .55 + .0)
sf.write(out_s, np.clip(s, -1, 1), SR)
print("ok", total)
