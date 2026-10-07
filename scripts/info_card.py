"""Builds data/info-card.svg, a neofetch-style card. Edit ROWS to change the content."""
import os
from html import escape

STATIC = os.environ.get("STATIC") == "1"
TITLE = "manoj@github"
ROWS = [
    ("Role", "Azure Data Engineer"),
    ("Prev", "Senior Analyst, Teleperformance (2022-2026)"),
    ("Location", "Hyderabad, India"),
    ("Stack", "ADF · ADLS Gen2 · Databricks · PySpark · Delta Lake · SQL"),
    ("Streaming", "Event Hubs · Kafka · Structured Streaming"),
    ("Projects", "Logistics Data Platform · Uber-style Streaming Platform"),
    ("Education", "B.Tech Mechanical Engineering, JNTUK"),
]
W, LH, TOP = 490, 22, 56
H = TOP + len(ROWS) * LH + 24

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Consolas, Menlo, monospace" font-size="11">',
       f'<rect width="{W}" height="{H}" rx="10" fill="#0d1117" stroke="#30363d"/>',
       '<circle cx="18" cy="16" r="5" fill="#ff5f56"/><circle cx="36" cy="16" r="5" fill="#ffbd2e"/><circle cx="54" cy="16" r="5" fill="#27c93f"/>',
       f'<text x="{W // 2}" y="20" text-anchor="middle" fill="#8b949e">neofetch</text>']

def line(i, inner):
    a = "" if STATIC else (
        f'<animate attributeName="opacity" from="0" to="1" begin="{0.3 + i * 0.25:.2f}s" dur="0.4s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="-8 0" to="0 0" begin="{0.3 + i * 0.25:.2f}s" dur="0.4s" fill="freeze"/>')
    return f'<g opacity="{1 if STATIC else 0}">{inner}{a}</g>'

out.append(line(0, f'<text x="18" y="{TOP - 14}" fill="#39d353" font-weight="bold">{escape(TITLE)}</text>'))
out.append(f'<line x1="18" y1="{TOP - 8}" x2="{18 + len(TITLE) * 7}" y2="{TOP - 8}" stroke="#30363d"/>')
for i, (k, v) in enumerate(ROWS, start=1):
    y = TOP + (i - 1) * LH + 12
    out.append(line(i, f'<text x="18" y="{y}" fill="#58a6ff" font-weight="bold">{escape(k)}</text>'
                       f'<text x="104" y="{y}" fill="#c9d1d9">{escape(v)}</text>'))
out.append("</svg>")
os.makedirs("data", exist_ok=True)
open("data/info-card.svg", "w", encoding="utf-8").write("".join(out))
print("info-card.svg written")
