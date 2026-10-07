"""Builds data/contributions.json and data/heatmap.svg from the public contributions calendar.
No token needed. Set STATIC=1 to emit a frozen frame (handy for previews)."""
import json
import os
import re
from datetime import date, timedelta

import requests

USER = "manojchoragudi"
STATIC = os.environ.get("STATIC") == "1"
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
CELL, GAP, PAD, TOP = 11, 3, 10, 30
MUTED = "#8b949e"

html = requests.get(
    f"https://github.com/users/{USER}/contributions",
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=30,
).text
cells = re.findall(r'data-date="(\d{4}-\d{2}-\d{2})"[^>]*?id="([^"]+)"[^>]*?data-level="(\d)"', html)
counts = {
    i: (0 if n == "No" else int(n.replace(",", "")))
    for i, n in re.findall(r'for="(contribution-day-component-[^"]+)"[^>]*>\s*(No|\d[\d,]*) contribution', html)
}
if not cells:
    raise SystemExit("No contribution cells found - GitHub's HTML may have changed.")

days = sorted((d, int(lv), counts.get(cid, 0)) for d, cid, lv in cells)

# ---- stats ----
total = sum(c for _, _, c in days)
best = max(days, key=lambda x: x[2])
longest = run = 0
for _, _, c in days:
    run = run + 1 if c > 0 else 0
    longest = max(longest, run)
current, idx = 0, len(days) - 1
if days[idx][2] == 0:  # today may not have a contribution yet
    idx -= 1
while idx >= 0 and days[idx][2] > 0:
    current += 1
    idx -= 1

os.makedirs("data", exist_ok=True)
json.dump(
    {"days": [{"date": d, "level": lv, "count": c} for d, lv, c in days],
     "total": total, "current_streak": current, "longest_streak": longest,
     "best_day": {"date": best[0], "count": best[2]}},
    open("data/contributions.json", "w"),
)

# ---- render ----
offset = (date.fromisoformat(days[0][0]).weekday() + 1) % 7  # Sunday = row 0
cols = (len(days) + offset + 6) // 7
grid_w, grid_h = cols * (CELL + GAP), 7 * (CELL + GAP)
W, H = grid_w + PAD * 2, TOP + grid_h + 44

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Consolas, Menlo, monospace">',
       f'<text x="{PAD}" y="18" font-size="12" fill="{MUTED}">{total:,} contributions in the last year</text>']
for i, (d, lv, c) in enumerate(days):
    col, row = divmod(i + offset, 7)
    x, y = PAD + col * (CELL + GAP), TOP + row * (CELL + GAP)
    delay = round((col + row) * 0.02, 2)
    anim = "" if STATIC else (
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay}s" dur="0.35s" fill="freeze"/>')
    out.append(
        f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{PALETTE[lv]}" '
        f'opacity="{1 if STATIC else 0}"><title>{c} on {d}</title>{anim}</rect>')

fy = TOP + grid_h + 22
out.append(f'<text x="{PAD}" y="{fy}" font-size="11" fill="{MUTED}">'
           f'current streak {current}d · longest streak {longest}d · best day {best[2]} ({best[0]})</text>')
lx = W - PAD - 5 * (CELL + 3) - 70
out.append(f'<text x="{lx}" y="{fy}" font-size="11" fill="{MUTED}">Less</text>')
for k, colr in enumerate(PALETTE):
    out.append(f'<rect x="{lx + 32 + k * (CELL + 3)}" y="{fy - 10}" width="{CELL}" height="{CELL}" rx="2" fill="{colr}"/>')
out.append(f'<text x="{lx + 36 + 5 * (CELL + 3)}" y="{fy}" font-size="11" fill="{MUTED}">More</text></svg>')
open("data/heatmap.svg", "w", encoding="utf-8").write("".join(out))
print(f"heatmap: {len(days)} days, {total} contributions")
