"""Builds data/portrait.svg (ASCII portrait). Uses scripts/photo-prepped.png, else scripts/photo.jpg."""
import os
from html import escape

from PIL import Image, ImageOps

STATIC = os.environ.get("STATIC") == "1"
WIDTH = 100  # characters per line
RAMP = " .`:-=+*cs#%@"  # dark/background (blank) -> bright (dense)

path = "scripts/photo-prepped.png" if os.path.exists("scripts/photo-prepped.png") else "scripts/photo.jpg"
img = ImageOps.autocontrast(Image.open(path).convert("L"))
height = max(1, int(img.height / img.width * WIDTH * 0.5))
img = img.resize((WIDTH, height))
px = img.load()
rows = ["".join(RAMP[px[x, y] * (len(RAMP) - 1) // 255] for x in range(WIDTH)).rstrip() for y in range(height)]

LH, CW = 7.0, 4.2
W, H = int(WIDTH * CW) + 20, len(rows) * int(LH) + 20
text = []
for i, row in enumerate(rows):
    anim = "" if STATIC else (
        f'<animate attributeName="opacity" from="0" to="1" begin="{i * 0.05:.2f}s" dur="0.25s" fill="freeze"/>')
    text.append(f'<text x="10" y="{14 + i * LH}" xml:space="preserve" opacity="{1 if STATIC else 0}">{escape(row)}{anim}</text>')
os.makedirs("data", exist_ok=True)
open("data/portrait.svg", "w", encoding="utf-8").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
    f'<rect width="100%" height="100%" fill="#0d1117" rx="8"/>'
    f'<g font-family="Consolas, Menlo, monospace" font-size="6.6" fill="#c9d1d9">{"".join(text)}</g></svg>')
print(f"portrait.svg: {len(rows)} rows")
