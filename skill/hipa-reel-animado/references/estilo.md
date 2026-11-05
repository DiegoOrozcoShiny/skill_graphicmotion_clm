# Estilo, composición y tiempos

## Marca (Academia HIPA)
- Fondo **Pure Blue #002aff** con cuadrícula de cuadrados modulares (líneas blancas al 7 %, deriva lenta). Escenas "serias" (pregunta, predicción): fondo **negro**.
- Acento **Pure Green #64dd00** en la palabra clave de cada título y subtítulo. **Pure Red #ff0000** solo para "prohibido"/alertas (sellos). Blanco y negro para tarjetas. Nunca degradados; nunca rojo semitransparente sobre azul (se ve violeta).
- Tipos: Barlow 900 (títulos, mayúsculas), Figtree 800 (subtítulos), Space Grotesk 500 (etiqueta `// 03 · la pregunta`).
- Logo: siempre los PNG oficiales de `assets/logos/`, nunca redibujado. Los cuadrados del logo sirven como recurso: transiciones, "?", bola de cristal, la "h" que se arma.

## Layout 1080x1920 (zona segura de la app: texto entre 168 y 1330 px)
| Elemento | Posición |
|---|---|
| Etiqueta tipo código | left 72, top 196, 32 px |
| Subtítulos palabra por palabra | left/right 72, top 262, 56 px, máx. 2 líneas, 3–5 palabras por grupo |
| Título | left/right 72, top 430, 128 px (110–112 si la palabra tiene ≥ 13 letras), 1–2 líneas |
| Escenario (objetos) | 690–1300 px de alto, x 60–1000 |
| Maestro | abajo a la derecha; su cabeza ocupa x ≈ 760–1030, y ≥ 1250. Nada de contenido ahí |

## Ritmo
- Algo cambia cada 1–2 s. Cada objeto aparece **en la palabra que lo nombra** (tiempo de la transcripción).
- Entradas: título por palabra con blur 10→0 en 0,22 s `expo.out`; pops `back.out(1.8–2.4)`; sellos que caen `scale 2.4→1` en 0,24 s `power4.in` + golpe de sonido.
- Transición "wipe modular": 66 cuadrados redondeados (6x11) que cubren en 0,3 s y descubren en 0,3 s; cambia de escena en el instante de cobertura total. 3–5 tipos de transición por video: wipe, corte a negro, corte seco, blur swap.
- Lo que haya que leer necesita ≥ 0,5 s + 0,3 s por palabra antes de que lo tape una transición; el texto final ≥ 2,8 s.
- Cierre fijo (`templates/cierre.html`, 3,5 s, empieza al terminar la voz): "MÁNDASELO a quien lo necesite" + icono de compartir + "Síguenos" + logo + @academia.hipa, con el maestro señalando el texto. No se cambia.
- Duración total = voz editada + 3,5 s. Se usa todo el audio; no se recorta contenido para ajustar el tiempo.

## Sonido
- Efectos de la librería incluida en `media-use/audio/assets/sfx` (pop, whoosh, whoosh-short, impact-bass-1/2, click, click-soft, notification, riser, glitch-1). Las búsquedas en Openverse pueden devolver grabaciones de voz diciendo el nombre del efecto: no las uses sin revisar.
- Cada efecto tiene una causa en pantalla; alterna tomas (whoosh / whoosh-short, impact 1 / 2). Volumen 0,3–0,45 bajo la voz a 1,0.
- Riser: su tramo audible es 0,9–4,5 s del archivo (usa `data-media-start≈2.95`, 1,6 s, terminando en el corte).
- **Sin música**: solo la voz y los efectos.
- Los efectos los copia `setup_project.py` desde el skill `media-use` de HyperFrames.
