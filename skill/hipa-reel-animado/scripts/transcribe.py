import sys, json
from faster_whisper import WhisperModel
src, out, size = sys.argv[1], sys.argv[2], sys.argv[3]
m = WhisperModel(size, device="cpu", compute_type="int8")
import wave, numpy as np
with wave.open(src) as wf:
    audio = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
segs, info = m.transcribe(audio, language="es", word_timestamps=True, vad_filter=False, beam_size=5)
res = []
for s in segs:
    res.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                "words": [{"w": w.word, "s": round(w.start, 2), "e": round(w.end, 2), "p": round(w.probability, 2)} for w in s.words]})
json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open(out.replace(".json", ".txt"), "w", encoding="utf-8") as f:
    for s in res:
        f.write(f"[{s['start']:6.2f}-{s['end']:6.2f}] {s['text']}\n")
print("ok", len(res))
