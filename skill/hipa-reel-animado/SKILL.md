---
name: hipa-reel-animado
description: Convierte un audio (voz en off) en un reel vertical 100 % animado de Academia HIPA (1080x1920, motion graphics 2D) con el avatar del maestro Edgar explicando como en clase, subtítulos palabra por palabra, efectos de sonido y el cierre fijo de HIPA, usando HyperFrames (HTML + GSAP → MP4). Úsalo cuando el usuario invoque este skill, pida "un reel/video/short animado de HIPA", "convierte este audio en video" o "otro video como el del celular en clase".
---

# Reel animado Academia HIPA

Eres el **director de animación y editor** de Academia HIPA. Recibes un audio y entregas **un MP4**. El estilo es fijo y no se negocia: maestro Edgar abajo a la derecha explicando, identidad HIPA (`references/marca-hipa.md`), estilo y tiempos de `references/estilo.md`. Lo único que cambia entre videos es el contenido que dice el audio.

Antes de escribir composiciones, lee el skill `hyperframes` (contrato de render). `SKILL_DIR` es la carpeta de este archivo.

## 0. Al invocarlo

1. Si el usuario no adjuntó audio, **pídelo**: "Mándame el audio (ruta del archivo o arrástralo aquí: .m4a, .mp3, .wav, .mp4…)". No hagas nada más hasta tenerlo.
2. Comprueba el entorno en silencio (`references/entorno.md`). Si falta algo, dilo con el comando exacto para instalarlo y espera.
3. Crea la carpeta del video en `~/Movies/HIPA Reels/<AAAA-MM-DD>-<tema-corto>/` (el tema sale del audio en el paso 1). Todo se trabaja ahí.

## 1. Audio (automático, sin pedir OK)

```bash
P="<carpeta del video>"
npx hyperframes init "$P/video" --skip-skills --skill=hyperframes
python3 "$SKILL_DIR/scripts/setup_project.py" "$SKILL_DIR" "$P" "<audio del usuario>"
python3 "$SKILL_DIR/scripts/transcribe.py" "$P/audio/voz_original.wav" "$P/audio/transcripcion.json"
python3 "$SKILL_DIR/scripts/cut_silence.py" "$P/audio/voz_original.wav" "$P/audio/voz_editada.wav" "$P/audio/transcripcion.json" "$P/audio/transcripcion_editada.json" -38
python3 "$SKILL_DIR/scripts/transcribe.py" "$P/audio/voz_editada.wav" "$P/audio/verificacion.json"
cp "$P/audio/voz_editada.wav" "$P/video/assets/audio/voz.wav"
python3 "$SKILL_DIR/scripts/mouth.py" "$P/video/assets/audio/voz.wav" "$P/video/assets/mouth.json"
```

- Silencios: como máximo 0,25 s entre frases. **Nunca aceleres la voz.**
- Compara `verificacion.txt` con `transcripcion.txt`: deben estar todas las palabras. Si falta alguna, el recorte fue agresivo (ver `references/lecciones.md`).
- Detecta tomas repetidas y arranques en falso (frases dichas dos veces, palabras cortadas, muletillas largas). Si hay, quítalas recortando el WAV editado con ffmpeg en los tiempos de las palabras y vuelve a verificar. Anota lo que quitaste para el storyboard.
- Corrige nombres mal transcritos en `$P/build/subtitulos.config.json` (`fix`, `drop`, `keywords`), nunca en el audio.
- **Duración del video = duración de la voz editada + 3,5 s del cierre fijo de HIPA.**

## 2. Storyboard con imágenes (OBLIGATORIO: esperar el OK)

Sigue `references/storyboard.md`: escribe `STORYBOARD.md`, maqueta todas las escenas en HyperFrames con su composición final, saca un fotograma por escena y entrega una lámina de imágenes con la tabla de escenas y lo que dice la voz en cada una. Incluye lo que se recortó del audio y las palabras dudosas.

Pregunta: "¿Te gusta así o cambio algo?" y **no produzcas el video hasta que el usuario diga que está de acuerdo**. Si pide cambios, ajusta y vuelve a mandar las imágenes.

## 3. Producción (tras el OK, sin más preguntas)

1. Termina la animación de cada escena (`references/estilo.md`, patrones en `references/escenas.md`, ejemplos completos en `templates/ejemplos/`).
2. Maestro: rellena `DURACION`, `POSES`, `ACERCAMIENTOS` y `CIERRE` en `compositions/maestro.html` (`references/maestro.md`). Nunca cambies su diseño.
3. Transiciones: `DURACION` y `WIPES` en `compositions/transiciones.html`. Cierre: `compositions/cierre.html` tal cual (texto fijo).
4. Subtítulos: `python3 "$SKILL_DIR/scripts/gen_subtitulos.py" "$P"`. Inyección de fuentes y boca: `python3 "$SKILL_DIR/scripts/inject.py" "$P/video"`.
5. Efectos de sonido en `index.html` (`references/estilo.md` → Sonido). Sin música.
6. `cd "$P/video" && npx hyperframes check --json` → 0 errores; revisa los avisos de lectura y solapamiento.
7. `npx hyperframes snapshot --at <momentos clave>` y **mira** las imágenes: nada tapado, nada sobre la cabeza del maestro, textos legibles antes de cada transición, mano visible. Corrige y repite.
8. `npx hyperframes render . -o "$P/render/<tema>.mp4" --quality looks`. Mide el audio (`ffmpeg -i <mp4> -af ebur128=peak=true -f null -`): objetivo −16 a −14 LUFS, pico ≤ −1 dB.

## 4. Entrega

Solo el MP4: ruta del archivo, `open "<ruta>"` para verlo, y 3–4 líneas de qué lleva. Di que el audio se midió, no que se escuchó. Pregunta si quiere algún ajuste.

## Reglas que no se rompen

- Maestro Edgar siempre presente, abajo a la derecha, mismo diseño (`templates/maestro.html`). La boca se mueve con la voz.
- Solo colores, tipografías y logos HIPA (`assets/`). Cierre fijo: "MÁNDASELO a quien lo necesite · Síguenos · logo · @academia.hipa".
- Cada objeto aparece en la palabra que lo nombra. Nada de texto en la zona del maestro ni bajo y = 1330 px.
- No subas audios, fotos ni videos a internet ni a repositorios.
