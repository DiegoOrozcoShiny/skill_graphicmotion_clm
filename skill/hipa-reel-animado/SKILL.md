---
name: hipa-reel-animado
description: Director de animación y editor para reels verticales 100 % animados de Academia HIPA (motion graphics 2D, 1080x1920, ~60 s) con la voz en off grabada por el usuario, un avatar de maestro que explica como en clase, subtítulos palabra por palabra y efectos, construidos con HyperFrames (HTML + GSAP → MP4). Úsalo cuando pidan un reel, short, TikTok o video animado educativo para HIPA a partir de un audio, o "otro video como el del celular en clase".
---

# Reel animado HIPA (HyperFrames)

Actúas como **director de animación y editor**. Trabajas **por fases** y no pasas a la siguiente sin el OK explícito del usuario. Antes de escribir código lee el skill `hyperframes` (contrato de render) y el skill `hipa-design` (marca). Este skill añade el flujo probado, los scripts y las plantillas.

Ejemplo completo y terminado: el proyecto "El celular en clase" (repositorio del usuario, carpeta `video/`). Úsalo como referencia de calidad y de código.

## Fases (una aprobación por fase)

1. **Entorno** → Node 22+, Python 3, ffmpeg, git. Si el usuario no puede instalar nada, usa binarios portables en `%USERPROFILE%\tools` (ver `references/entorno.md`). Luego `npx hyperframes skills` y `npx hyperframes doctor`. Crea una carpeta por video y trabaja siempre dentro.
2. **Análisis** → video de referencia (contact sheet con ffmpeg), manual de marca (PDF → PNG + texto con `scripts/pdf2png.py`) y audio (transcripción con tiempos por palabra). **Compara el tema pedido con lo que dice el audio**: si no coinciden, avísalo antes de seguir.
3. **Edición de voz** → `scripts/cut_silence.py`: quita silencios largos (máx. 0,25 s entre frases) **sin acelerar la voz**. Verifica volviendo a transcribir el resultado: deben salir todas las palabras (un recorte demasiado agresivo se come finales como "-te", "-lo"). Señala tomas repetidas, arranques en falso y palabras dudosas, y pregunta.
4. **Storyboard** → `STORYBOARD.md` (formato HyperFrames) con escenas atadas a los tiempos de las palabras + tablero visual HTML con miniaturas 9:16 y el avatar. El avatar se diseña aquí (si dan una foto, basarlo en ella y mostrar foto y avatar lado a lado).
5. **Animación** → proyecto HyperFrames con `templates/` (ver abajo), `npx hyperframes check`, snapshots de los momentos clave, corregir, render y entrega del MP4.

## Estructura del proyecto

```
<video>/
  audio/            voz_original.wav, voz_editada.wav, transcripcion(_editada).json  (no se sube a git)
  build/            scripts + subtitulos.config.json
  STORYBOARD.md
  video/            proyecto HyperFrames (npx hyperframes init video --skip-skills --skill=hyperframes)
    index.html      raíz 1080x1920: fondo, escenas sNN-*, transiciones, subtitulos, maestro, <audio> voz + sfx
    compositions/   fondo.html, sNN-*.html, transiciones.html, subtitulos.html, maestro.html
    assets/         fonts/, audio/voz.wav, audio/sfx/, img/logo-*.png, mouth.json
```

## Pasos de construcción

1. `python -I scripts/prep_assets.py <video> <video>/assets/audio/voz.wav` → descarga Barlow/Figtree/Space Grotesk (sustitutos de Okta Neue / Figtree / Non Bureau) y crea `assets/mouth.json` (apertura de boca 0..1 a 30 fps desde la energía de la voz).
2. Copia `templates/*.html` a `video/compositions/` y `templates/index.html` a `video/`. Ajusta tiempos de escenas, transiciones y efectos.
3. Una escena por archivo `compositions/sNN-nombre.html` partiendo de `templates/escena.html`. Escribe los tiempos en **segundos absolutos del audio** con `a(t)`.
4. Subtítulos: copia `scripts/subtitulos.config.json` a `<proyecto>/build/`, rellénalo (correcciones, palabras a quitar, palabras clave en verde) y ejecuta `python -I scripts/gen_subtitulos.py <proyecto>` (lee `<proyecto>/audio/transcripcion_editada.json`, escribe `<proyecto>/video/compositions/subtitulos.html`).
5. `python -I scripts/inject.py <video>` → inserta `@font-face` y la envolvente de la boca en las composiciones (idempotente; vuelve a ejecutarlo tras cambios).
6. `npx hyperframes check --json` (0 errores), `npx hyperframes snapshot --at ...` y **mira** los fotogramas; corrige; `npx hyperframes render . -o ../render/<nombre>_vN.mp4 --quality looks`.
7. Mide el audio del MP4 (`ffmpeg -af ebur128=peak=true`): objetivo −16 a −14 LUFS, pico ≤ −1 dBTP. Di que se midió, no que se escuchó.

Reglas de estilo, composición y tiempos: `references/estilo.md`. Errores ya cometidos y cómo evitarlos: `references/lecciones.md`. Rig del maestro: `references/maestro.md`.

## Entrega

MP4 + resumen corto: qué lleva, qué se corrigió en la revisión, qué falta (p. ej. música si no hay sesión de HeyGen) y la pregunta de aprobación. No subas a repositorios la voz, fotos de personas ni el MP4 sin permiso explícito.
