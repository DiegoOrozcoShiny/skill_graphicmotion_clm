"""Rellena marcadores en video/compositions/*.html (idempotente).
/*FONTS*/      -> @font-face de assets/fonts/fonts.css
/*MOUTH*/[...] -> envolvente de boca (assets/mouth.json)
<!--MAP-->, <!--GRID-->, <!--BALL--> -> celdas SVG generadas
Uso: python -I inject.py <carpeta video>"""
import sys, os, re, json

vd = sys.argv[1]
comp = os.path.join(vd, "compositions")
fonts = open(os.path.join(vd, "assets", "fonts", "fonts.css"), encoding="utf-8").read().strip()
mouth = json.load(open(os.path.join(vd, "assets", "mouth.json")))

MEX = [  # México en cuadrados (24 x 14)
    "#.#########.............",
    "#..##########...........",
    ".#..###########.........",
    ".#...###########........",
    "..#...##########........",
    "..#....#########........",
    "...#....########........",
    "...#.....#######........",
    ".........########.......",
    "..........#########.###.",
    "...........##########.##",
    "............#########...",
    "..............######....",
    "................###.....",
]
RED = [(4, 0), (5, 0), (5, 1), (9, 1), (10, 2), (13, 3), (14, 3), (8, 5), (11, 6), (12, 8), (13, 8), (15, 10), (16, 11), (22, 10)]

def map_svg():
    out = []
    for r, row in enumerate(MEX):
        for c, ch in enumerate(row):
            if ch == "#":
                cls = "s3-c s3-r" if (c, r) in RED else "s3-c"
                out.append(f'<rect class="{cls}" x="{c*40+3}" y="{r*40+3}" width="34" height="34" rx="7"/>')
    return "\n      ".join(out)

def grid_svg():
    on = {3, 9, 14, 20, 27, 33, 38}
    out = []
    for i in range(40):
        r, c = divmod(i, 8)
        cls = "s2-u on" if i in on else "s2-u"
        out.append(f'<use class="{cls}" href="#s2-st" x="{c*100}" y="{r*100}"/>')
    return "\n      ".join(out)

def ball_svg():
    rows = ["..###..", ".#####.", "#######", "#######", "#######", ".#####.", "..###.."]
    on = {(2, 1), (4, 2), (1, 3), (3, 3), (5, 4), (2, 5), (4, 0)}
    out = []
    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch == "#":
                cls = "s8-c on" if (c, r) in on else "s8-c"
                out.append(f'<rect class="{cls}" x="{c*62+8}" y="{r*62+8}" width="52" height="52" rx="10"/>')
    return "\n        ".join(out)

def block(text, tag, content, open_, close_):
    pat = re.compile(re.escape(open_) + r".*?" + re.escape(close_), re.S)
    new = open_ + "\n" + content + "\n" + close_
    if pat.search(text):
        return pat.sub(lambda m: new, text)
    return text.replace(tag, new)

for fn in sorted(os.listdir(comp)):
    if not fn.endswith(".html"):
        continue
    p = os.path.join(comp, fn)
    t = open(p, encoding="utf-8").read()
    o = t
    t = block(t, "/*FONTS*/", fonts, "/*FONTS*/", "/*/FONTS*/")
    t = re.sub(r"/\*MOUTH\*/\[[^\]]*\]", "/*MOUTH*/" + json.dumps(mouth, separators=(",", ":")), t)
    t = block(t, "<!--MAP-->", map_svg(), "<!--MAP-->", "<!--/MAP-->")
    t = block(t, "<!--GRID-->", grid_svg(), "<!--GRID-->", "<!--/GRID-->")
    t = block(t, "<!--BALL-->", ball_svg(), "<!--BALL-->", "<!--/BALL-->")
    if t != o:
        open(p, "w", encoding="utf-8").write(t)
        print("updated", fn)
