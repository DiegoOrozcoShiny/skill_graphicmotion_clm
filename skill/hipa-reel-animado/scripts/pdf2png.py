import sys, os, pymupdf
src, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
doc = pymupdf.open(src)
with open(os.path.join(out, "text.txt"), "w", encoding="utf-8") as f:
    f.write(f"pages: {doc.page_count}\n")
    for i, p in enumerate(doc):
        p.get_pixmap(dpi=50).save(os.path.join(out, f"p{i+1:02d}.png"))
        t = p.get_text().strip().replace("\n", " | ")
        f.write(f"--- p{i+1}: {t[:600]}\n")
print("done", doc.page_count)
