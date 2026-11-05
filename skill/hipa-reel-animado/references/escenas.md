# Catálogo de escenas (patrones probados)

Todos los ejemplos están en `templates/ejemplos/` (video "El celular en clase"). Copia el patrón y cambia el contenido.

| Patrón | Ejemplo | Úsalo para |
|---|---|---|
| Titular + objeto + sello rojo "PROHIBIDO" | `s01-gancho.html` | Gancho con una prohibición o problema |
| Bocadillo del maestro (cita) | `s01-gancho.html` | El maestro "dice" una frase entre comillas |
| Objeto que entra a una caja + sello "GUARDADO" | `s01-gancho.html` | Acción concreta que termina algo |
| Cuadrícula de personas que se llena + chip | `s02-miles.html` | Cantidades ("miles de…"), grupos |
| Mapa pixelado de México con celdas rojas | `s03-restricciones.html` | Lugares, alcance geográfico (sin datos inventados) |
| Documento oficial + resaltado + firma | `s03-restricciones.html` | Normas, reglas, instituciones |
| "?" armado con cuadrados (fondo negro) | `s04-pregunta.html` | La pregunta central |
| Dos tarjetas A **o** B, gana una | `s05-dilema.html` | Dilema o comparación |
| Celular con notificaciones + sello | `s06-distrae.html` | Un problema que se acumula |
| Celular que cambia de pantalla + checklist numerada | `s07-giro.html` | Enumeraciones (3–5 cosas) |
| Iconos que vuelan dentro de un objeto + barra 0→100 % | `s07-giro.html` | Síntesis, progreso, "herramienta" |
| Bola de cristal de cuadrados + sello verde | `s08-prediccion.html` | Predicción, futuro, hipótesis |
| Reloj que avanza + sello que se agrieta + texto a mano | `s09-replantear.html` | Cambio de opinión, "hay que replantear" |
| Línea de tiempo + piezas que encajan en un bloque | `s10-futuro.html` | Evolución, conclusión, "parte de…" |

## Plantilla mínima de escena
- `<template>` → `<style>` con `/*FONTS*/` y el CSS base (`#root`, `.tag`, `.ttl`, `.ln`, `.g`, `.stamp`) idéntico al de los ejemplos.
- `#root` con `data-composition-id="sNN-nombre"` (igual al id del host en `index.html`).
- Etiqueta `// NN · capítulo` y título; ids con prefijo único (`sN-…`).
- Script: `const S = <data-start de la escena>, a = t => +(t - S).toFixed(3);`. Usa `fromTo` (nunca `from`). Termina con `tl.set({}, {}, <duración>)` y `window.__timelines["sNN-nombre"] = tl;`.
