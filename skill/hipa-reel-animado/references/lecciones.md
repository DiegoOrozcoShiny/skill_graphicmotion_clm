# Lecciones (errores reales y su arreglo)

- **El audio puede no tratar del tema pedido.** Transcribe primero y compáralo; avisa antes de hacer storyboard.
- **Recorte de silencios:** con umbral −38 dB y 0,125 s de margen se comía finales suaves ("hacer-te", "utiliza-rlo"). Arreglo: umbral −38 dB pero dejar **0,20 s después** de cada palabra y 0,05 s antes de la siguiente; verificar re-transcribiendo.
- **faster-whisper + PyAV:** `decode_audio` falla (`metadata_errors`). Pasa el audio como array numpy de un WAV 16 kHz mono.
- **Whisper en español** confunde nombres ("SEP" → "CEP") y muletillas ("sí" → "Oscar"); corrige en `subtitulos.config.json`, no en el audio.
- **Python con `-I`** ignora `PYTHONIOENCODING`: escribe a archivo con `encoding="utf-8"`, no a la consola.
- **Transiciones que tapan lo importante:** un sello que aterriza 0,3 s antes del wipe no se ve. Mueve el corte unas décimas después de la frase o adelanta la acción.
- **Brazo del maestro:** con rotación > ~45° la mano queda detrás de la cabeza. Dedo arriba = 35°, pensativo = 30°, señalar abajo = −38°.
- **Objetos que entran desde abajo** (`y: 700`) se asoman antes de tiempo detrás del maestro: añade `opacity: 0` en el estado inicial.
- **Estado inicial con `tl.set(..., 0)`** no se pinta en el frame 0: usa CSS (`opacity: 0`) o `fromTo` (immediateRender).
- **CSS `transform` + GSAP** en el mismo elemento rompe el lint: pon el estado inicial dentro del tween.
- **`z-index: -1`** para un resaltado detrás del texto: el contenedor necesita `isolation: isolate`.
- **El tablero HTML del storyboard** se abre como snapshot estático: incrusta imágenes en base64 si deben verse.
- **Sin permisos de instalación:** usa binarios portables (ver `entorno.md`); las shells del agente no heredan el PATH de usuario, antepónlo en cada comando.
