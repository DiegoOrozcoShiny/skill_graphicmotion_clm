# Entorno

Detecta el sistema: en Windows `$env:OS` es `Windows_NT`; en Mac `uname` devuelve `Darwin`.

## Mac

Comprueba sin avisar:

```bash
node -v        # 22 o superior
python3 --version
ffmpeg -version | head -1
git --version
python3 -c "import faster_whisper, numpy" 2>/dev/null && echo whisper-ok
ls ~/.claude/skills/hyperframes/SKILL.md ~/.claude/skills/media-use 2>/dev/null
```

Si falta algo:

| Falta | Comando |
|---|---|
| Node 22+, ffmpeg, git | `brew install node ffmpeg git` (Homebrew: https://brew.sh) |
| faster-whisper | `python3 -m pip install --user faster-whisper numpy`. Si pip responde "externally-managed-environment": `python3 -m venv ~/.hipa-reel-venv && ~/.hipa-reel-venv/bin/pip install faster-whisper numpy`, y usa `~/.hipa-reel-venv/bin/python` como `PY` |
| Skills de HyperFrames | `npx hyperframes skills` y después `npx hyperframes doctor` (Docker y whisper-cpp son opcionales) |

## Windows

Si el usuario no puede instalar programas, las herramientas van portables en `%USERPROFILE%\tools`. Cada comando de PowerShell empieza así:

```powershell
$t="$env:USERPROFILE\tools"; $env:Path="$t\git\cmd;$t\node;$t\python;$t\python\Scripts;$t\ffmpeg\bin;$env:Path"
```

Comprueba: `node -v`, `python --version`, `ffmpeg -version`, `git --version`, `python -c "import faster_whisper, numpy"`.

Si falta algo:
- **Con permisos:** `winget install OpenJS.NodeJS.LTS Python.Python.3.12 Gyan.FFmpeg Git.Git`.
- **Sin permisos:** descarga versiones portables de fuentes oficiales a `%USERPROFILE%\tools`, pidiendo permiso antes de descargar:

| Herramienta | Fuente | Carpeta |
|---|---|---|
| Node LTS (zip) | nodejs.org/dist | `tools\node` |
| Python 3.12 (paquete NuGet `python`) | api.nuget.org | `tools\python` (+ `python -m ensurepip`) |
| ffmpeg essentials | gyan.dev | `tools\ffmpeg\bin` |
| MinGit 64-bit | github.com/git-for-windows | `tools\git\cmd` |

Después: `python -m pip install faster-whisper numpy` y `npx hyperframes skills`.

## Ambos
La primera transcripción descarga el modelo `medium` de Whisper (~1,5 GB, una sola vez) y tarda 1–3 min por minuto de audio.
