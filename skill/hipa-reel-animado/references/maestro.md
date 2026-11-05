# El maestro Edgar (`templates/maestro.html`)

Es el avatar fijo de todos los videos y está basado en el maestro Edgar real: cabello negro corto, lentes rectangulares, bigote recortado, sonrisa amplia y camisa blanca con botones. **No cambies su diseño, colores ni posición.** Va abajo a la derecha en todo el video, también durante el cierre.

## Qué se configura por video
Al final del script, en el bloque `CONFIGURACIÓN POR VIDEO`:

| Variable | Qué es |
|---|---|
| `DURACION` | Duración total (voz editada + 3,5) |
| `POSES` | `[segundo, ángulo]`. 0 = señala hacia el contenido (reposo); 18 o 28 = gesticula; 30 = pensativo; 35 = dedo arriba; −10 = señala con energía. Después de cada gesto, vuelve a 0 unos 0,3–0,6 s después |
| `ACERCAMIENTOS` | `[inicio, fin]` de las escenas serias de fondo negro: acercamiento, dedo arriba y cejas levantadas |
| `CIERRE` | Segundo en el que termina la voz: señala el texto del cierre |

La boca (`/*MOUTH*/[...]`) la rellena `inject.py` desde `assets/mouth.json`: se abre con la energía de la voz cuadro a cuadro. El parpadeo y la respiración son automáticos.

## Dónde no poner contenido
Su cabeza ocupa x ≈ 760–1030 e y ≥ 1250. En los acercamientos crece hasta x ≈ 240–1080 e y ≥ 890: en las escenas serias, pon el contenido a la izquierda (x < 500).

## Límites del brazo
Con más de ~45° la mano queda detrás de la cabeza y no se ve. Usa 35° como máximo hacia arriba.
