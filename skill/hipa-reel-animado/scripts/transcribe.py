"""Transcripción en español con tiempos por palabra (faster-whisper).
Uso: python3 transcribe.py <audio> <salida.json> [modelo=medium]
Escribe <salida.json> y <salida.txt> (segmentos legibles + palabras dudosas)."""
import sys, json, os, subprocess, tempfile, wave
import numpy as np
from faster_whisper import WhisperModel

src, out = sys.argv[1], sys.argv[2]
size = sys.argv[3] if len(sys.argv) > 3 else "medium"

# Se decodifica con ffmpeg a 16 kHz mono (evita el decode_audio de PyAV, que falla en algunas versiones)
tmp = os.path.join(tempfile.gettempdir(), "hipa_reel_16k.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", tmp], check=True)
with wave.open(tmp) as wf:
    audio = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0

m = WhisperModel(size, device="cpu", compute_type="int8")
segs, info = m.transcribe(audio, language="es", word_timestamps=True, vad_filter=False, beam_size=5)
res = []
for s in segs:
    res.append({"start": s.start, "end": s.end, "text": s.text.strip(),
                "words": [{"w": w.word, "s": round(w.start, 2), "e": round(w.end, 2), "p": round(w.probability, 2)} for w in s.words]})
json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
with open(os.path.splitext(out)[0] + ".txt", "w", encoding="utf-8") as f:
    for s in res:
        f.write(f"[{s['start']:6.2f}-{s['end']:6.2f}] {s['text']}\n")
    low = [f"{w['w'].strip()}@{w['s']}" for s in res for w in s["words"] if w["p"] < 0.6]
    f.write("\nPalabras dudosas (confianza < 0.6): " + ", ".join(low) + "\n")
print("ok", len(res), "segmentos")
