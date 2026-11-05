import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
w = [x for s in d for x in s["words"]]
print("first", w[0]["s"], "last", w[-1]["e"], "words", len(w))
tot = 0
for a, b in zip(w, w[1:]):
    g = b["s"] - a["e"]
    if g > 0.25:
        tot += g - 0.25
        print(f"gap {g:.2f}s at {a['e']:.2f}: '{a['w'].strip()}' -> '{b['w'].strip()}'")
print("removable", round(tot, 2), "est final", round(w[-1]["e"] - w[0]["s"] - tot, 2))
low = [f"{x['w'].strip()}({x['p']}@{x['s']})" for x in w if x["p"] < 0.6]
print("low conf:", ", ".join(low))
