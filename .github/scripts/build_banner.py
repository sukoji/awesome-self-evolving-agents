# -*- coding: utf-8 -*-
"""Banner: the field as depth. Each ring is a layer of itself that an agent
learned to rewrite, outermost first; the innermost is the improver itself."""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SERIF = "Georgia,'Times New Roman',serif"
SANS = "-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

# sequential single hue, outer (light) -> inner (dark); inner accent separate
T = {
    "light": dict(bg="#ffffff", ink="#1f2328", sub="#59636e",
                  ramp=["#dbe9fa", "#bcd6f5", "#94bdef", "#6da7ec", "#4a8fe0", "#2a78d6"], core="#1a7f64"),
    "dark": dict(bg="#0d1117", ink="#e6edf3", sub="#9198a1",
                 ramp=["#1b2c44", "#1d3a60", "#21497d", "#28599a", "#326cb8", "#3987e5"], core="#2fbf88"),
}
LAYERS = [  # label, year, example
    ("its prompts", "2023", "Reflexion · Promptbreeder"),
    ("its memory", "2023", "MemGPT · ExpeL"),
    ("its workflow", "2024", "ADAS · AFlow"),
    ("its own code", "2025", "Darwin Gödel Machine"),
    ("its harness", "2026", "Self-Harness · RRSI"),
    ("its training", "2026", "A-Evolve-Training · AIDE²"),
]
CORE = ("the process that improves it", "2026", "Hyperagents")
W, H = 1200, 400


def arc(cx, cy, r, a0, a1):
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    return f"M{x0:.1f} {y0:.1f} A{r} {r} 0 0 1 {x1:.1f} {y1:.1f}"


def banner(t):
    c = T[t]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Awesome Self-Evolving Agents. Concentric layers an agent has learned to rewrite, outermost first: its prompts (2023), '
         f'its memory (2023), its workflow (2024), its own code (2025), its harness (2026), its training (2026), and at the centre the process that improves it (2026).">\n',
         f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>\n',
         f'<text x="56" y="100" font-family="{MONO}" font-size="13" letter-spacing="3" fill="{c["sub"]}">AWESOME LIST · 240+ PAPERS · SEPTEMBER 2026</text>\n',
         f'<text x="52" y="176" font-family="{SERIF}" font-size="66" font-style="italic" fill="{c["ink"]}">Self-Evolving</text>\n',
         f'<text x="52" y="244" font-family="{SERIF}" font-size="66" fill="{c["ink"]}">Agents</text>\n',
         f'<rect x="56" y="270" width="56" height="3" fill="{c["core"]}"/>\n',
         f'<text x="56" y="306" font-family="{SANS}" font-size="20" fill="{c["sub"]}">Agents that rewrite themselves —</text>\n',
         f'<text x="56" y="334" font-family="{SANS}" font-size="20" fill="{c["sub"]}">each year, one layer deeper.</text>\n']
    X0, Y0, X1, Y1 = 560, 28, 1168, 382
    dx, dy = 40, 42
    levels = LAYERS + [CORE]
    for k, (label, year, ex) in enumerate(levels):
        x, y = X0 + k * dx, Y0 + k * dy
        w, h = X1 - x - k * 3, Y1 - y - k * 3
        core = k == len(LAYERS)
        fill = c["core"] if core else c["ramp"][k]
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{fill}"/>\n')
        light_text = (not core and k >= 4) or (core and t == "light")
        col = "#ffffff" if light_text else ("#0d1117" if core else c["ink"])
        subc = col if (light_text or core) else c["sub"]
        s.append(f'<text x="{x+16}" y="{y+27}" font-family="{SANS}" font-size="16" font-weight="600" fill="{col}">{label}'
                 f'<tspan font-family="{MONO}" font-weight="400" font-size="13.5" dx="10" fill="{subc}">{year}</tspan></text>\n')
        if core:
            s.append(f'<text x="{x+16}" y="{y+52}" font-family="{MONO}" font-size="13" fill="{subc}">{ex}</text>\n')
        else:
            s.append(f'<text x="{x+w-16}" y="{y+27}" text-anchor="end" font-family="{MONO}" font-size="13" fill="{subc}">{ex}</text>\n')
    s.append("</svg>\n")
    return "".join(s)


for t in T:
    (ROOT / "assets" / f"banner-{t}.svg").write_text(banner(t), encoding="utf-8")
print("ok")
