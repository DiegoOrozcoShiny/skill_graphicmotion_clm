# Entorno sin permisos de instalación (Windows)

Binarios portables en `%USERPROFILE%\tools` (descargar de fuentes oficiales, sin admin):

| Herramienta | Fuente | Carpeta |
|---|---|---|
| Node LTS (zip) | nodejs.org/dist | `tools\node` |
| Python 3.12 (paquete NuGet `python`) | api.nuget.org | `tools\python` (+ `python -m ensurepip`) |
| ffmpeg essentials | gyan.dev | `tools\ffmpeg\bin` |
| MinGit 64-bit | github.com/git-for-windows | `tools\git\cmd` |

Paquetes Python: `faster-whisper pymupdf pypdf numpy`.

Cada comando de PowerShell del agente empieza con:

```powershell
$t="$env:USERPROFILE\tools"; $env:Path="$t\git\cmd;$t\node;$t\python;$t\python\Scripts;$t\ffmpeg\bin;$env:Path"
```

`hyperframes doctor` marcará Docker y whisper-cpp como ausentes: son opcionales.
