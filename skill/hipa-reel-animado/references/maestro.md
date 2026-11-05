# Rig del maestro (`templates/maestro.html`)

Un SVG (viewBox `0 30 370 490`) dentro de `#m-wrap` (600x795, abajo a la derecha, origen de escala `85% 100%`).

| Parte | id | Animación |
|---|---|---|
| Brazo que señala | `#m-arm` | `rotation` con `svgOrigin: "150 345"` (hombro). 0 = señala arriba-izquierda; 35 = dedo arriba; 30 = pensativo; −38 = señala abajo-izquierda |
| Cabeza | `#m-head` | `y` y leve `rotation` con la voz (por cuadro) |
| Boca | `#m-mouth` | `scaleY 0.22 + 0.95·env` con `svgOrigin: "230 246"`, un `tl.set` por cuadro desde `/*MOUTH*/[...]` |
| Bigote | `#m-stache` | sube `−4·env` px |
| Ojos | `#m-eyes` | parpadeo `scaleY 0.1` en tiempos fijos |
| Cejas | `#m-brows` | `y: −6` en momentos de énfasis |
| Cuerpo | `#m-body` | respiración `scaleY 1.012` cada 3,2 s |
| Envoltura | `#m-wrap` | punch-in `scale 1.32, x −120, y −60` en escenas serias |

Personalizar a otra persona: cambia colores de piel (`#d9a27a`), cabello, camisa y la forma del bigote/cabello en el SVG. Diseña primero en el tablero del storyboard, con la foto al lado, y pide OK.

Poses: edita las llamadas `arm(t, ángulo, duración)` y los punch-ins al final del script según los momentos del storyboard.
