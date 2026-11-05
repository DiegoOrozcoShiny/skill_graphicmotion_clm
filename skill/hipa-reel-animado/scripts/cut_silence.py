"""Trim every pause longer than MAXGAP down to MAXGAP. Never time-stretches speech.
Args: in.wav out.wav words.json out_words.json
"""
import sys, json, wave, numpy as np

src, dst, wj, wout = sys.argv[1:5]
MAXGAP, THR_DB, FRAME, HEAD, TAIL, FADE = 0.25, float(sys.argv[5]) if len(sys.argv) > 5 else -45.0, 0.01, 0.08, 0.30, 0.012

with wave.open(src) as wf:
    sr = wf.getframerate()
    x = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
n = int(sr * FRAME)
frames = len(x) // n
rms = np.sqrt(np.mean(x[: frames * n].reshape(frames, n) ** 2, axis=1) + 1e-12)
db = 20 * np.log10(rms)
voiced = db > THR_DB

# silent runs (in seconds)
runs, i = [], 0
while i < frames:
    if not voiced[i]:
        j = i
        while j < frames and not voiced[j]:
            j += 1
        runs.append((i * FRAME, j * FRAME))
        i = j
    else:
        i += 1

dur = len(x) / sr
remove = []  # (start, end) intervals to delete
for a, b in runs:
    if a == 0:
        if b > HEAD: remove.append((0, b - HEAD))
    elif b >= dur - FRAME:
        if b - a > TAIL: remove.append((a + TAIL, dur))
    elif b - a > MAXGAP:
        keep_l = 0.20  # more room after speech (soft word endings), less before next onset
        remove.append((a + keep_l, b - (MAXGAP - keep_l)))

# build kept pieces with short fades at each joint
keep, t = [], 0.0
for a, b in remove:
    if a > t: keep.append((t, a))
    t = b
if t < dur: keep.append((t, dur))
fl = int(sr * FADE)
out = []
for k, (a, b) in enumerate(keep):
    seg = x[int(a * sr): int(b * sr)].copy()
    if k > 0 and len(seg) > fl: seg[:fl] *= np.linspace(0, 1, fl)
    if k < len(keep) - 1 and len(seg) > fl: seg[-fl:] *= np.linspace(1, 0, fl)
    out.append(seg)
y = np.concatenate(out)
with wave.open(dst, "wb") as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr)
    wf.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes())

def remap(tt):
    shift = 0.0
    for a, b in remove:
        if tt >= b: shift += b - a
        elif tt > a: return a - shift
    return tt - shift

segs = json.load(open(wj, encoding="utf-8"))
for s in segs:
    for w in s["words"]:
        w["s"], w["e"] = round(remap(w["s"]), 3), round(remap(w["e"]), 3)
    s["start"], s["end"] = s["words"][0]["s"], s["words"][-1]["e"]
json.dump(segs, open(wout, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open(wout.replace(".json", ".txt"), "w", encoding="utf-8") as f:
    for s in segs:
        f.write(f"[{s['start']:6.2f}-{s['end']:6.2f}] {s['text']}\n")
    f.write("\nCORTES (tiempos del original):\n")
    for a, b in remove:
        f.write(f"  {a:6.2f} -> {b:6.2f}  ({b-a:.2f}s)\n")
print(f"orig {dur:.2f}s -> edit {len(y)/sr:.2f}s, cuts {len(remove)}, removed {sum(b-a for a,b in remove):.2f}s")
