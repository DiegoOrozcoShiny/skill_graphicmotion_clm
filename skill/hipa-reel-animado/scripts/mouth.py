"""Envolvente de apertura de boca (0..1, 30 fps) a partir de la voz editada.
Uso: python3 mouth.py <proyecto>/video/assets/audio/voz.wav <proyecto>/video/assets/mouth.json"""
import sys, json, wave
import numpy as np

wav, out = sys.argv[1], sys.argv[2]
with wave.open(wav) as wf:
    sr, ch = wf.getframerate(), wf.getnchannels()
    x = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
if ch > 1:
    x = x.reshape(-1, ch).mean(axis=1)
hop = sr // 30
n = len(x) // hop
rms = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1))
db = 20 * np.log10(rms + 1e-9)
v = np.clip((db + 42) / 26, 0, 1)          # -42 dB boca cerrada .. -16 dB abierta
v = np.convolve(v, [0.25, 0.5, 0.25], mode="same")
json.dump([round(float(a), 2) for a in v], open(out, "w"))
print(f"mouth: {n} cuadros ({n / 30:.2f} s)")
