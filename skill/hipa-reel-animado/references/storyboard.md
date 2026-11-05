# Storyboard con imágenes

El usuario valida **imágenes reales del video**, no bocetos. Por eso, en esta fase las escenas se maquetan ya en HyperFrames con su composición final (la animación fina y los efectos vienen después del OK).

## 1. Guion visual (`$P/STORYBOARD.md`)
- Divide la voz editada en **escenas de 3–7 s** (una idea por escena; 8–12 escenas en 60 s). Corta en pausas o fin de frase.
- Arco: **gancho** (frame 0 ya con titular grande y un objeto) → contexto → pregunta o giro → desarrollo → conclusión → cierre fijo HIPA.
- Marca 1 o 2 momentos **serios** (pregunta clave, predicción o advertencia): fondo negro y acercamiento al maestro.
- Por escena: título (≤ 2 líneas, palabra clave en verde), objeto visual **inventado para el tema** (`escenas.md` → "Del audio a la escena"), en qué palabra aparece cada cosa, transición de entrada (wipe modular, corte a negro o corte seco) y lo que dice la voz.
- Formato: el de `hyperframes/references/storyboard-format.md` (`## Frame N — Título`, `- duration`, `- voiceover`, `- reads`, `- sound`).

## 2. Maquetar
- `video/index.html`: crea los hosts de escena contiguos con sus `data-start`/`data-duration` y sustituye `DURACION`, `VOZ` y `VOZ_MAS_04`.
- Una escena por archivo `compositions/sNN-nombre.html`. Toma de `templates/ejemplos/` solo la estructura del código (mismo CSS base: `.tag`, `.ttl`, `.stamp`…); los objetos son los del tema. Usa los tiempos absolutos de las palabras con `a(t)`.
- Genera subtítulos, maestro (`DURACION`, `CIERRE`), transiciones (`WIPES`) e inyecta fuentes y boca, como en la producción. Ejecuta `npx hyperframes check` y corrige los errores.

## 3. Lámina de imágenes
```bash
cd "$P/video"
npx hyperframes snapshot --at <un segundo por escena, cuando todo ya aterrizó (≈ 80 % de la escena)>,<VOZ+2.5>
```
- El comando devuelve `contact-sheet-*.jpg`. Cópialos a `$P/storyboard/` y ábrelos con `open "$P/storyboard/"`.
- Mira tú las imágenes antes de mandarlas. Si algo se tapa, se sale o queda sobre el maestro, corrígelo primero.

## 4. Mensaje al usuario
- Las imágenes (rutas y `open`).
- Una tabla: escena | tiempo | lo que dice la voz | qué se ve.
- Lo que se recortó del audio y las palabras dudosas.
- "¿Te gusta así o cambio algo? Cuando me digas que estás de acuerdo, produzco el video."
