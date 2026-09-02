# Generates assets/neofetch.svg — ASCII portrait + neofetch-style info panel.
#
#   pip install pillow
#   python tools/gen_neofetch.py
#
# Edit the INFO table below to change the right-hand panel; edit CROP / build()
# args in ascii3.py to retune the portrait.
import html
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from ascii3 import build

OUT = Path(__file__).resolve().parent.parent / "assets" / "neofetch.svg"

art = build(width=56, local=1.15, contrast=1.45, aspect=0.5)

# ── info panel ────────────────────────────────────────────────────────────────
# ("kind", label, value)  kind: h=section header, r=row, s=spacer, l=rule
INFO = [
    ("t", "shamila", "@github"),
    ("l", "", ""),
    ("r", "Name",        "Shamila Hasaranga"),
    ("r", "Role",        "Full-Stack Developer"),
    ("r", "Host",        "Sri Lanka"),
    ("r", "Shell",       "bash - powershell"),
    ("r", "Editor",      "VS Code"),
    ("s", "", ""),
    ("h", "Languages", ""),
    ("r", "  Programming", "TypeScript, JavaScript, Python"),
    ("r", "  Markup",      "HTML, CSS, EJS, JSON, YAML"),
    ("r", "  Spoken",      "Sinhala, English"),
    ("s", "", ""),
    ("h", "Stack", ""),
    ("r", "  Frontend",  "React, Next.js, TailwindCSS"),
    ("r", "  Backend",   "Node.js, Express"),
    ("r", "  Database",  "MongoDB, PostgreSQL"),
    ("r", "  AI",        "LLMs, RAG, Knowledge Graphs"),
    ("s", "", ""),
    ("h", "Currently", ""),
    ("r", "  Building",  "trading tools, finance + habit apps"),
    ("r", "  Learning",  "LLM engineering, agents, retrieval"),
    ("s", "", ""),
    ("h", "Contact", ""),
    ("r", "  Email",     "shamilawasalagedara16@gmail.com"),
    ("r", "  Website",   "shamila.netlify.app"),
    ("r", "  LinkedIn",  "/in/YOUR-HANDLE"),
    ("s", "", ""),
    ("r", "GitHub",      "43 public repositories"),
]

# ── geometry ──────────────────────────────────────────────────────────────────
PAD_X, TOP = 30, 64
ART_FS, ART_LH = 9.5, 11.4
INF_FS, INF_LH = 13, 17.6
ART_X = PAD_X + 6
INF_X = 372
VAL_X = INF_X + 132

art_h = len(art) * ART_LH
inf_h = len(INFO) * INF_LH
BODY = max(art_h, inf_h)
W, H = 1000, int(TOP + BODY + 34)

e = html.escape
parts = []
add = parts.append

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'fill="none" xml:space="preserve" '
    f'font-family="ui-monospace, \'SF Mono\', \'Cascadia Code\', \'DejaVu Sans Mono\', Menlo, Consolas, monospace">')
add('''
  <defs>
    <linearGradient id="skin" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0"   stop-color="#39FF14"/>
      <stop offset="0.55" stop-color="#2BE0C8"/>
      <stop offset="1"   stop-color="#58A6FF"/>
    </linearGradient>
    <style>
      .lbl  { fill: #58A6FF; }
      .val  { fill: #C9D1D9; }
      .sec  { fill: #39FF14; font-weight: 700; }
      .dim  { fill: #6E7681; }
      .cur  { fill: #39FF14; animation: blink 1.05s step-end infinite; }
      @keyframes blink { 50% { opacity: 0; } }
    </style>
  </defs>''')

# window chrome
add(f'  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="#0D1117" stroke="#39FF14" stroke-opacity="0.42"/>')
add(f'  <path d="M1 13 A12 12 0 0 1 13 1 H{W-13} A12 12 0 0 1 {W-1} 13 V40 H1 Z" fill="#161B22"/>')
add('  <circle cx="25" cy="20.5" r="6" fill="#FF5F56"/>')
add('  <circle cx="47" cy="20.5" r="6" fill="#FFBD2E"/>')
add('  <circle cx="69" cy="20.5" r="6" fill="#27C93F"/>')
add(f'  <text x="{W/2}" y="25.5" text-anchor="middle" class="dim" font-size="13">shamila@github: ~ — neofetch</text>')

# ascii portrait
# NB: SVG collapses runs of plain spaces, so emit U+00A0 — same advance width
# in a monospace face, but never collapsed.
art_dy = (BODY - art_h) / 2
add(f'  <g font-size="{ART_FS}" fill="url(#skin)" style="white-space:pre">')
for i, line in enumerate(art):
    if not line.strip():
        continue
    y = TOP + art_dy + (i + 1) * ART_LH
    add(f'    <text x="{ART_X}" y="{y:.1f}">{e(line).replace(" ", " ")}</text>')
add('  </g>')

# info panel
add(f'  <g font-size="{INF_FS}">')
for i, (kind, label, value) in enumerate(INFO):
    y = TOP + (i + 1) * INF_LH
    if kind == "s":
        continue
    if kind == "t":
        add(f'    <text x="{INF_X}" y="{y:.1f}" font-size="15" font-weight="700">'
            f'<tspan class="sec">{e(label)}</tspan><tspan class="lbl">{e(value)}</tspan></text>')
    elif kind == "l":
        add(f'    <text x="{INF_X}" y="{y:.1f}" class="dim">{"─" * 46}</text>')
    elif kind == "h":
        add(f'    <text x="{INF_X}" y="{y:.1f}" class="sec">{e(label)}</text>')
    else:
        add(f'    <text x="{INF_X}" y="{y:.1f}" class="lbl">{e(label)}</text>')
        add(f'    <text x="{VAL_X}" y="{y:.1f}" class="val">{e(value)}</text>')
add('  </g>')

# prompt + cursor
py = TOP + BODY + 20
add(f'  <text x="{ART_X}" y="{py:.1f}" font-size="{INF_FS}">'
    f'<tspan class="sec">$</tspan>'
    f'<tspan class="cur" dx="9">\u2588</tspan></text>')

add('</svg>')

svg = "\n".join(parts) + "\n"
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {OUT}  ({W}x{H}, {len(art)} art lines, {len(INFO)} info lines)")
