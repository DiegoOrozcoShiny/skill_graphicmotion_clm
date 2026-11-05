# El celular en clase · Reel animado Academia HIPA

Reel vertical (1080×1920, 60 s) 100 % animado en motion graphics 2D. Lleva la voz en off original, un avatar del maestro Edgar que explica como en clase, subtítulos palabra por palabra y efectos de sonido. Está hecho con [HyperFrames](https://hyperframes.heygen.com), que convierte HTML + GSAP en MP4.

> No incluye la grabación de voz, las transcripciones, la foto de referencia ni el MP4 final (ver `.gitignore`). Para volver a renderizar hay que poner la voz editada en `video/assets/audio/voz.wav`.

## Estructura

| Ruta | Qué es |
|---|---|
| `STORYBOARD.md` | Storyboard aprobado: 14 escenas con tiempos sincronizados con la voz |
| `video/` | Proyecto HyperFrames: `index.html` (raíz) y `compositions/` (fondo, 11 escenas, transiciones, subtítulos, maestro) |
| `video/assets/` | Tipografías (Barlow, Figtree, Space Grotesk), efectos de sonido, logo HIPA y envolvente de la boca |
| `build/` | Scripts del flujo: recorte de silencios, transcripción, subtítulos, inyección de fuentes/boca |
| `skill/hipa-reel-animado/` | Skill para Claude Code que repite este flujo con cualquier audio |
| `assets/` | Logos oficiales HIPA |

## Requisitos
Node 22+, Python 3 (`faster-whisper pymupdf pypdf numpy`), ffmpeg y git.

## Volver a renderizar

```bash
cd video
npx hyperframes check
npx hyperframes render . -o ../render/celular-en-clase.mp4 --quality looks
```

## Instalar el skill en Claude Code (Mac)

```bash
git clone <URL de este repositorio> hipa-reel
mkdir -p ~/.claude/skills && cp -R hipa-reel/skill/hipa-reel-animado ~/.claude/skills/
npx hyperframes skills
python3 -m pip install --user faster-whisper numpy
```

Abre Claude Code y escribe `/hipa-reel-animado`. Te pedirá el audio y, antes de producir, te mandará un storyboard con imágenes para que lo apruebes. Al final entrega el MP4.

## Flujo (por fases, con aprobación en cada una)
1. Entorno → 2. Análisis (video de referencia, manual de marca, audio) → 3. Edición de voz (silencios ≤ 0,25 s, sin acelerar) → 4. Storyboard + avatar → 5. Animación, revisión de fotogramas y render.
