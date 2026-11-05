"""Prepara un proyecto de reel HIPA a partir del audio del usuario.

Uso (ejecutar DESPUÉS de `npx hyperframes init <proyecto>/video --skip-skills --skill=hyperframes`):
    python3 setup_project.py <skill_dir> <proyecto> <audio_del_usuario>

Crea audio/voz_original.wav (48 kHz mono), copia tipografías, logos, efectos y plantillas
(fondo, transiciones, maestro, index) al proyecto HyperFrames y la config de subtítulos.
"""
import sys, os, shutil, subprocess, glob

skill, proj, audio = (os.path.abspath(a) for a in sys.argv[1:4])
v = os.path.join(proj, "video")
if not os.path.exists(os.path.join(v, "hyperframes.json")):
    sys.exit(f"Falta el proyecto HyperFrames en {v}: ejecuta primero `npx hyperframes init {v} --skip-skills --skill=hyperframes`")

for d in ["audio", "build", "render", "storyboard", "video/compositions", "video/assets/fonts",
          "video/assets/img", "video/assets/audio/sfx"]:
    os.makedirs(os.path.join(proj, d), exist_ok=True)

# 1. voz original normalizada a WAV 48 kHz mono
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", audio, "-vn", "-ac", "1", "-ar", "48000",
                "-c:a", "pcm_s16le", os.path.join(proj, "audio", "voz_original.wav")], check=True)

# 2. tipografías y logos de marca
for f in glob.glob(os.path.join(skill, "assets", "fonts", "*")):
    shutil.copy(f, os.path.join(v, "assets", "fonts"))
for f in glob.glob(os.path.join(skill, "assets", "logos", "*.png")):
    shutil.copy(f, os.path.join(v, "assets", "img"))

# 3. efectos de sonido de la librería incluida en el skill media-use de HyperFrames
home = os.path.expanduser("~")
cands = [os.path.join(home, ".claude", "skills", "media-use", "audio", "assets", "sfx"),
         os.path.join(home, ".agents", "skills", "media-use", "audio", "assets", "sfx")]
sfx = next((c for c in cands if os.path.isdir(c)), None)
if sfx:
    for n in ["pop", "whoosh", "whoosh-short", "impact-bass-1", "impact-bass-2", "click", "click-soft",
              "notification", "riser", "glitch-1"]:
        src = os.path.join(sfx, n + ".mp3")
        if os.path.exists(src):
            shutil.copy(src, os.path.join(v, "assets", "audio", "sfx"))
else:
    print("AVISO: no encontré la librería de efectos (ejecuta `npx hyperframes skills`).")

# 4. plantillas fijas
for n in ["fondo.html", "transiciones.html", "maestro.html", "cierre.html"]:
    shutil.copy(os.path.join(skill, "templates", n), os.path.join(v, "compositions", n))
shutil.copy(os.path.join(skill, "templates", "index.html"), os.path.join(v, "index.html"))
cfg = os.path.join(proj, "build", "subtitulos.config.json")
if not os.path.exists(cfg):
    shutil.copy(os.path.join(skill, "scripts", "subtitulos.config.json"), cfg)

print("Proyecto listo en", proj)
print("Siguiente: transcribe.py → cut_silence.py → transcribe.py (verificación) → mouth.py")
