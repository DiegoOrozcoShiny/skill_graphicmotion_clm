"""Download latin woff2 fonts, build mouth envelope from the voice. Args: video_dir voice_wav"""
import sys, os, re, json, urllib.request, wave
import numpy as np

vd, wav = sys.argv[1], sys.argv[2]
fd = os.path.join(vd, "assets", "fonts"); os.makedirs(fd, exist_ok=True)
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
url = "https://fonts.googleapis.com/css2?family=Barlow:wght@700;800;900&family=Figtree:wght@500;700;800&family=Space+Grotesk:wght@500;700&display=swap"
css = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA})).read().decode()
faces = []
for block in re.findall(r"/\* (\S+) \*/\s*@font-face \{(.*?)\}", css, re.S):
    subset, body = block
    if subset != "latin":
        continue
    fam = re.search(r"font-family: '([^']+)'", body).group(1)
    wt = re.search(r"font-weight: (\d+)", body).group(1)
    src = re.search(r"url\((https://[^)]+\.woff2)\)", body).group(1)
    fn = f"{fam.replace(' ', '')}-{wt}.woff2"
    urllib.request.urlretrieve(src, os.path.join(fd, fn))
    faces.append(f"@font-face{{font-family:'{fam}';font-weight:{wt};font-display:block;src:url('assets/fonts/{fn}') format('woff2');}}")
open(os.path.join(fd, "fonts.css"), "w", encoding="utf-8").write("\n".join(faces) + "\n")
print("fonts:", len(faces))

# mouth envelope at 30 fps, 0..1
with wave.open(wav) as wf:
    sr = wf.getframerate()
    x = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
hop = sr // 30
n = len(x) // hop
rms = np.sqrt(np.mean(x[: n * hop].reshape(n, hop) ** 2, axis=1))
db = 20 * np.log10(rms + 1e-9)
v = np.clip((db + 42) / 26, 0, 1)          # -42 dB closed .. -16 dB wide open
v = np.convolve(v, [0.25, 0.5, 0.25], mode="same")
env = [round(float(a), 2) for a in v]
open(os.path.join(vd, "assets", "mouth.json"), "w").write(json.dumps(env))
print("mouth frames:", len(env), "secs", len(env) / 30)
