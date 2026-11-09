# -*- coding: utf-8 -*-
""""Start here" cards under the banner: assets/card-{read,see,run}-{light,dark}.svg.

Same palette as the banner, so the header reads as one piece. Text only
describes what is already in the repository.

Run from the repository root:  python .github/scripts/build_cards.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SANS = "-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
T = {
    "light": dict(bg="#ffffff", edge="#d0d7de", ink="#1f2328", sub="#59636e",
                  ramp=["#bcd6f5", "#6da7ec", "#2a78d6"], core="#1a7f64"),
    "dark": dict(bg="#0d1117", edge="#30363d", ink="#e6edf3", sub="#9198a1",
                 ramp=["#1d3a60", "#28599a", "#3987e5"], core="#2fbf88"),
}
CARDS = [  # name, kicker, title, two lines, footer
    ("read", "01 · READ", "The primer", "Builds the ideas from the ground up,",
     "from one agent loop to misevolution.", "docs/primer.md"),
    ("see", "02 · SEE", "Evolution map", "Five threads through the field,",
     "drawn as metro lines by arXiv date.", "#evolution-map"),
    ("run", "03 · RUN", "Reference code", "Design-as-search and safety-gated",
     "evolution, two short Python demos.", "code/"),
]
W, H = 300, 150


def icon(name, c):
    r = c["ramp"]
    if name == "read":  # nested layers, as in the banner
        return "".join(f'<rect x="{24+k*6}" y="{24+k*6}" width="{40-k*12}" height="{40-k*12}" rx="5" fill="{col}"/>'
                       for k, col in enumerate([r[0], r[1], c["core"]]))
    if name == "see":  # a metro line with three stations
        s = f'<path d="M22 44 H66" stroke="{r[2]}" stroke-width="6" stroke-linecap="round"/>'
        return s + "".join(f'<circle cx="{x}" cy="44" r="6" fill="{c["bg"]}" stroke="{col}" stroke-width="3"/>'
                           for x, col in [(26, r[1]), (44, r[2]), (62, c["core"])])
    return (f'<rect x="22" y="26" width="44" height="36" rx="6" fill="{r[2]}"/>'  # a terminal
            f'<path d="M30 38 l7 6 l-7 6" stroke="#ffffff" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="M41 52 h12" stroke="#ffffff" stroke-width="3" stroke-linecap="round"/>')


def card(spec, t):
    name, kicker, title, l1, l2, foot = spec
    c = T[t]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="{title}: {l1} {l2}">\n'
            f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{c["bg"]}" stroke="{c["edge"]}" stroke-width="1.5"/>\n'
            f'{icon(name, c)}\n'
            f'<text x="84" y="38" font-family="{MONO}" font-size="11.5" letter-spacing="2" fill="{c["sub"]}">{kicker}</text>\n'
            f'<text x="84" y="62" font-family="{SANS}" font-size="20" font-weight="700" fill="{c["ink"]}">{title}</text>\n'
            f'<text x="22" y="98" font-family="{SANS}" font-size="13.5" fill="{c["sub"]}">{l1}</text>\n'
            f'<text x="22" y="117" font-family="{SANS}" font-size="13.5" fill="{c["sub"]}">{l2}</text>\n'
            f'<text x="{W-22}" y="{H-14}" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="{c["core"]}">{foot} →</text>\n'
            f'</svg>\n')


for spec in CARDS:
    for t in T:
        (ROOT / "assets" / f"card-{spec[0]}-{t}.svg").write_text(card(spec, t), encoding="utf-8", newline="\n")
print("ok")
