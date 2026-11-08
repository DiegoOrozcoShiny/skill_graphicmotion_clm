"""Fase de audio completa, en Mac y Windows: proyecto HyperFrames + voz editada + verificación + boca.

Uso:
    python3 fase_audio.py "<audio del usuario>" "<tema-corto>"        (Mac)
    python  fase_audio.py "<audio del usuario>" "<tema-corto>"        (Windows)

Crea la carpeta del video en:
    Mac:     ~/Movies/HIPA Reels/AAAA-MM-DD-<tema>/
    Windows: %USERPROFILE%/Videos/HIPA Reels/AAAA-MM-DD-<tema>/
e imprime al final la ruta del proyecto (línea "PROYECTO=...").
"""
import sys, os, subprocess, shutil, datetime, re, json

audio = os.path.abspath(sys.argv[1])
tema = re.sub(r"[^a-z0-9-]+", "-", (sys.argv[2] if len(sys.argv) > 2 else "reel").lower()).strip("-") or "reel"
skill = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
scripts = os.path.join(skill, "scripts")
py = sys.executable
win = os.name == "nt"

# En Windows sin permisos, las herramientas portables viven en %USERPROFILE%\tools
if win:
    t = os.path.join(os.path.expanduser("~"), "tools")
    extra = [os.path.join(t, p) for p in ("git\\cmd", "node", "python", "python\\Scripts", "ffmpeg\\bin")]
    os.environ["PATH"] = os.pathsep.join([p for p in extra if os.path.isdir(p)] + [os.environ.get("PATH", "")])

base = os.path.join(os.path.expanduser("~"), "Videos" if win else "Movies", "HIPA Reels")
proj = os.path.join(base, f"{datetime.date.today():%Y-%m-%d}-{tema}")
n = 2
while os.path.exists(proj):
    proj = os.path.join(base, f"{datetime.date.today():%Y-%m-%d}-{tema}-{n}"); n += 1
os.makedirs(proj)

def run(cmd, **kw):
    print(">", " ".join(cmd) if isinstance(cmd, list) else cmd, flush=True)
    subprocess.run(cmd, check=True, **kw)

for tool in ("ffmpeg", "node", "npx"):
    if not shutil.which(tool):
        sys.exit(f"FALTA {tool}: revisa references/entorno.md")

v = os.path.join(proj, "video")
run(f'npx hyperframes init "{v}" --skip-skills --skill=hyperframes', shell=True, stdout=subprocess.DEVNULL)
run([py, os.path.join(scripts, "setup_project.py"), skill, proj, audio])
A = lambda f: os.path.join(proj, "audio", f)
run([py, os.path.join(scripts, "transcribe.py"), A("voz_original.wav"), A("transcripcion.json")])
run([py, os.path.join(scripts, "cut_silence.py"), A("voz_original.wav"), A("voz_editada.wav"),
     A("transcripcion.json"), A("transcripcion_editada.json"), "-38"])
run([py, os.path.join(scripts, "transcribe.py"), A("voz_editada.wav"), A("verificacion.json")])
shutil.copy(A("voz_editada.wav"), os.path.join(v, "assets", "audio", "voz.wav"))
run([py, os.path.join(scripts, "mouth.py"), os.path.join(v, "assets", "audio", "voz.wav"), os.path.join(v, "assets", "mouth.json")])

# Resumen para el agente
words = lambda f: [w["w"].strip() for s in json.load(open(A(f), encoding="utf-8")) for w in s["words"]]
o, e = words("transcripcion.json"), words("verificacion.json")
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                            A("voz_editada.wav")], capture_output=True, text=True).stdout.strip())
print(f"\nPROYECTO={proj}")
print(f"VOZ_EDITADA={dur:.2f}s  DURACION_VIDEO={dur + 3.5:.2f}s")
print(f"PALABRAS original={len(o)} verificacion={len(e)} (si difieren en más de 2, revisa el recorte)")
print("Lee audio/transcripcion.txt (texto y palabras dudosas) antes del storyboard.")
