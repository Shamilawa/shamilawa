# Generates assets/neofetch.svg — ASCII wordmark + neofetch-style info panel.
#
#   python tools/gen_neofetch.py
#
# Edit INFO to change the right-hand panel, WORDMARK/SUBTITLE for the left.
import html
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "neofetch.svg"

# ── left column ───────────────────────────────────────────────────────────────
# ANSI-Shadow block letters. Every row is exactly 54 cells wide; keep it that
# way if you edit them, or the vertical strokes will shear.
WORDMARK = [
    "███████╗██╗  ██╗ █████╗ ███╗   ███╗██╗██╗      █████╗ ",
    "██╔════╝██║  ██║██╔══██╗████╗ ████║██║██║     ██╔══██╗",
    "███████╗███████║███████║██╔████╔██║██║██║     ███████║",
    "╚════██║██╔══██║██╔══██║██║╚██╔╝██║██║██║     ██╔══██║",
    "███████║██║  ██║██║  ██║██║ ╚═╝ ██║██║███████╗██║  ██║",
    "╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚══════╝╚═╝  ╚═╝",
]
WM_COLS = 54

SUBTITLE = [
    ("gap",  14, ""),
    ("sec",  13, "H  A  S  A  R  A  N  G  A"),
    ("gap",  16, ""),
    ("rule", 12, "─" * 40),
    ("gap",  14, ""),
    ("val",  13, "full-stack developer"),
    ("dim",  13, "sri lanka"),
]

# ── right column ──────────────────────────────────────────────────────────────
# kind: t=title  l=rule  h=section header  r=row  s=spacer
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
PAD_X, TOP = 34, 64
WM_FS = 12.0                 # block letters
WM_LH = WM_FS * 0.90         # <1em so the block rows overlap and seams close
INF_FS, INF_LH = 13, 17.6
CH = WM_FS * 0.6             # monospace advance width
WM_W = WM_COLS * CH
ART_X = PAD_X + 6
WM_MID = ART_X + WM_W / 2
INF_X = 452
VAL_X = INF_X + 138

left_h = len(WORDMARK) * WM_LH + sum(dy for _, dy, _ in SUBTITLE)
inf_h = len(INFO) * INF_LH
BODY = max(left_h, inf_h)
W, H = 1000, int(TOP + BODY + 34)

e = html.escape
# SVG collapses runs of plain spaces; U+00A0 has the same advance in a
# monospace face but is never collapsed.
nb = lambda s: e(s).replace(" ", " ")

out = []
add = out.append

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'fill="none" xml:space="preserve" '
    f'font-family="ui-monospace, \'SF Mono\', \'Cascadia Code\', \'DejaVu Sans Mono\', Menlo, Consolas, monospace">')
add('''
  <defs>
    <linearGradient id="skin" x1="0" y1="0" x2="0.35" y2="1">
      <stop offset="0"    stop-color="#39FF14"/>
      <stop offset="0.55" stop-color="#2BE0C8"/>
      <stop offset="1"    stop-color="#58A6FF"/>
    </linearGradient>
    <style>
      .lbl  { fill: #58A6FF; }
      .val  { fill: #C9D1D9; }
      .sec  { fill: #39FF14; font-weight: 700; }
      .dim  { fill: #6E7681; }
      .rule { fill: #30363D; }
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

# left column, vertically centred against the taller info panel
y = TOP + (BODY - left_h) / 2
add(f'  <g fill="url(#skin)" font-size="{WM_FS}" style="white-space:pre">')
for row in WORDMARK:
    y += WM_LH
    add(f'    <text x="{ART_X}" y="{y:.1f}">{nb(row)}</text>')
add('  </g>')

add(f'  <g text-anchor="middle">')
for cls, dy, text in SUBTITLE:
    y += dy
    if cls == "gap":
        continue
    fs = 13 if cls != "rule" else 12
    ls = ' letter-spacing="1.5"' if cls == "sec" else ""
    add(f'    <text x="{WM_MID:.1f}" y="{y:.1f}" class="{cls}" font-size="{fs}"{ls}>{nb(text)}</text>')
add('  </g>')

# right column
add(f'  <g font-size="{INF_FS}">')
for i, (kind, label, value) in enumerate(INFO):
    iy = TOP + (i + 1) * INF_LH
    if kind == "s":
        continue
    if kind == "t":
        add(f'    <text x="{INF_X}" y="{iy:.1f}" font-size="15" font-weight="700">'
            f'<tspan class="sec">{e(label)}</tspan><tspan class="lbl">{e(value)}</tspan></text>')
    elif kind == "l":
        add(f'    <text x="{INF_X}" y="{iy:.1f}" class="rule">{"─" * 42}</text>')
    elif kind == "h":
        add(f'    <text x="{INF_X}" y="{iy:.1f}" class="sec">{e(label)}</text>')
    else:
        add(f'    <text x="{INF_X}" y="{iy:.1f}" class="lbl">{nb(label)}</text>')
        add(f'    <text x="{VAL_X}" y="{iy:.1f}" class="val">{e(value)}</text>')
add('  </g>')

# prompt + blinking cursor
py = TOP + BODY + 20
add(f'  <text x="{ART_X}" y="{py:.1f}" font-size="{INF_FS}">'
    f'<tspan class="sec">$</tspan><tspan class="cur" dx="9">█</tspan></text>')
add('</svg>')

OUT.write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"wrote {OUT}  ({W}x{H}, wordmark {WM_COLS} cols, {len(INFO)} info lines)")
