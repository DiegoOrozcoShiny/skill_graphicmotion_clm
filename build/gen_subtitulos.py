"""Genera video/compositions/subtitulos.html desde audio/transcripcion_editada.json.
Uso: python -I gen_subtitulos.py <proyecto>"""
import sys, os, json, re, html

root = sys.argv[1]
words = [w for s in json.load(open(os.path.join(root, "audio", "transcripcion_editada.json"), encoding="utf-8")) for w in s["words"]]
fonts = open(os.path.join(root, "video", "assets", "fonts", "fonts.css"), encoding="utf-8").read()

# Correcciones por video en build/subtitulos.config.json:
# {"fix": {"CEP": "SEP"}, "drop": ["Oscar"], "keywords": ["celular", ...]}
cfg_path = os.path.join(root, "build", "subtitulos.config.json")
cfg = json.load(open(cfg_path, encoding="utf-8")) if os.path.exists(cfg_path) else {}
FIX = cfg.get("fix", {})
DROP = set(cfg.get("drop", []))
KEY = {k.lower() for k in cfg.get("keywords", [])}

ws = []
for w in words:
    raw = w["w"].strip()
    core = re.sub(r"[¿?¡!,.]", "", raw)
    if core in DROP:
        continue
    if core in FIX:
        raw = raw.replace(core, FIX[core])
    ws.append({"t": raw, "s": w["s"], "e": w["e"], "k": re.sub(r"[¿?¡!,.]", "", raw).lower() in KEY})

groups, cur = [], []
for i, w in enumerate(ws):
    cur.append(w)
    nxt = ws[i + 1] if i + 1 < len(ws) else None
    brk = (re.search(r"[,.?!]$", w["t"]) is not None) or len(cur) >= 5 or nxt is None or (nxt["s"] - w["e"] >= 0.15 and len(cur) >= 2)
    if brk:
        groups.append(cur); cur = []

out_groups, js = [], []
for gi, g in enumerate(groups):
    start = max(0.1, g[0]["s"] - 0.06)
    nxt = groups[gi + 1][0]["s"] - 0.06 if gi + 1 < len(groups) else g[-1]["e"] + 0.8
    end = min(nxt, g[-1]["e"] + 0.8)
    spans = "".join(f'<span id="sw{gi}_{wi}" class="w{" k" if w["k"] else ""}">{html.escape(w["t"])}</span> ' for wi, w in enumerate(g))
    out_groups.append(f'    <div id="sg{gi}" class="grp">{spans.strip()}</div>')
    js.append(f'  tl.set("#sg{gi}", {{opacity: 1, visibility: "visible"}}, {start:.3f});')
    for wi, w in enumerate(g):
        js.append(f'  tl.fromTo("#sw{gi}_{wi}", {{opacity: 0.32}}, {{opacity: 1, duration: 0.08, ease: "none"}}, {max(start, w["s"]):.3f});')
    js.append(f'  tl.to("#sg{gi}", {{opacity: 0, duration: 0.1, ease: "power2.in"}}, {end - 0.1:.3f});')
    js.append(f'  tl.set("#sg{gi}", {{opacity: 0, visibility: "hidden"}}, {end:.3f});')

doc = f"""<template>
  <style>
{fonts}
    #root {{ position: absolute; inset: 0; pointer-events: none; }}
    .grp {{ position: absolute; left: 72px; right: 72px; top: 262px; font-family: 'Figtree'; font-weight: 800;
           font-size: 56px; line-height: 1.18; color: #fff; text-align: left; opacity: 0; visibility: hidden; }}
    .w.k {{ color: #64dd00; }}
  </style>
  <div id="root" data-composition-id="subtitulos" data-width="1080" data-height="1920">
{chr(10).join(out_groups)}
  </div>
  <script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
  window.__timelines["subtitulos"] = tl;
  </script>
</template>
"""
open(os.path.join(root, "video", "compositions", "subtitulos.html"), "w", encoding="utf-8").write(doc)
print("groups", len(groups), "words", len(ws))
for g in groups:
    print(f"{g[0]['s']:6.2f}  " + " ".join(w["t"] for w in g))
