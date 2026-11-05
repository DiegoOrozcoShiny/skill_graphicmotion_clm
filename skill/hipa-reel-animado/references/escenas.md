# Cómo diseñar las escenas

**Cada video tiene escenas nuevas, inventadas a partir de lo que dice su audio.** Lo fijo es el *estilo*: fondo HIPA, maestro, tipografías, etiqueta `// NN · capítulo`, título con palabra verde, subtítulos, transiciones y cierre. Lo que se ve en el escenario cambia siempre con el tema.

Los archivos de `templates/ejemplos/` son de otro video ("El celular en clase"). Úsalos **solo** para copiar la estructura del código (CSS base, `a(t)`, `fromTo`, sellos, pops) y el nivel de calidad. **No copies sus objetos ni su contenido** (celular, mapa de México, documento de la SEP…) salvo que el audio hable exactamente de eso.

## Del audio a la escena
1. Por cada escena, toma la idea central de la frase y su **palabra clave** (sustantivo o verbo con más peso).
2. Elige una **imagen concreta** que la explique a un estudiante de secundaria en 2 segundos:
   - **Un objeto del tema** dibujado simple en SVG/HTML: matraz, balanza, moneda, cerebro, reloj, libro abierto, gráfica, planeta, mochila…
   - **Una acción:** algo entra, se llena, se rompe, se ordena, se compara o crece.
   - **Un dato:** contador que sube, barra que se llena, cuadrícula de personas, línea de tiempo.
   - **Una estructura:** lista con checks, dos opciones A/B, pasos numerados, antes/después.
3. Construye esa imagen con el lenguaje HIPA: formas planas con contorno negro, cuadrados modulares redondeados y colores de la paleta. Las ideas se arman **pieza por pieza**.
4. Haz que aparezca **en la palabra** que la nombra y que tenga una pequeña acción (no solo aparecer).
5. Si el audio da cifras, nombres o lugares, muéstralos tal cual. **Nunca inventes datos** que el audio no dice.

## Recursos de movimiento que funcionan (aplícalos a objetos del tema)
| Recurso | Para qué sirve |
|---|---|
| Sello que cae (rojo = alerta/prohibido; verde o negro = conclusión) | Remarcar un veredicto |
| Objeto que cambia de estado (pantalla que cambia, vaso que se llena, pieza que encaja) | Mostrar una transformación |
| Lista numerada que se va marcando con checks verdes | Enumeraciones de 3–5 cosas |
| Dos tarjetas A **o** B, una gana | Dilemas y comparaciones |
| Cuadrícula de elementos que se llena en cascada | Cantidades, "muchos", porcentajes |
| Contador o barra 0 → N | Datos, progreso |
| Signo o figura armada con cuadrados (fondo negro) | La pregunta central o el momento serio |
| Línea de tiempo con piezas | Evolución, pasado → futuro |
| Bocadillo del maestro | Cuando la voz cita a alguien |
| Texto escrito a mano en verde que se revela | Replantear o corregir una idea |

Varía los recursos: no repitas el mismo en escenas seguidas y usa al menos 5 distintos por video.

## Plantilla técnica de una escena
- `<template>` → `<style>` con `/*FONTS*/` y el CSS base (`#root`, `.tag`, `.ttl`, `.ln`, `.g`, `.stamp`), igual al de los ejemplos.
- `#root` con `data-composition-id="sNN-nombre"`, el mismo id del host en `index.html`.
- Etiqueta `// NN · capítulo` y título; ids con prefijo único (`sN-…`).
- Script: `const S = <data-start de la escena>, a = t => +(t - S).toFixed(3);`. Usa `fromTo` (nunca `from`). Termina con `tl.set({}, {}, <duración>)` y `window.__timelines["sNN-nombre"] = tl;`.
- Objetos en la zona 690–1300 px de alto, sin invadir la cabeza del maestro (x > 760, y > 1250).
