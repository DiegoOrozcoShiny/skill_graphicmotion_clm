# Entorno (Mac)

Comprueba en silencio:

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
| faster-whisper | `python3 -m pip install --user faster-whisper numpy`. Si pip responde "externally-managed-environment", crea un entorno: `python3 -m venv ~/.hipa-reel-venv && ~/.hipa-reel-venv/bin/pip install faster-whisper numpy` y usa `~/.hipa-reel-venv/bin/python` en lugar de `python3` para los scripts |
| Skills de HyperFrames | `npx hyperframes skills` y luego `npx hyperframes doctor` (Docker y whisper-cpp son opcionales) |

La primera transcripción descarga el modelo `medium` de Whisper (~1,5 GB, una sola vez). En Apple Silicon tarda 1–3 min por minuto de audio.
