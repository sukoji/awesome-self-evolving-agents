#!/usr/bin/env python3
"""Draw the README banner: assets/banner-light.svg and assets/banner-dark.svg.

Four versions of one agent, each written by the one before it. Every version
scores higher; the last one got there by deleting its own safety check. The
list's thesis, readable without a caption.

Run from the repository root:  python .github/scripts/build_banner.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
SANS = "-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"

THEMES = {
    "light": dict(bg="#ffffff", card="#f6f8fa", line="#d0d7de", ink="#1f2328", sub="#59636e", track="#e3e8ee",
                  g0="#d85a30", g1="#c0417a", g2="#1a7f64", score="#1a9f6e", safe="#2a78d6", red="#cf222e"),
    "dark": dict(bg="#0d1117", card="#161b22", line="#30363d", ink="#e6edf3", sub="#9198a1", track="#262c36",
                 g0="#ff8a3d", g1="#f2497f", g2="#2fd6a0", score="#2fbf88", safe="#4c95eb", red="#ff6b6b"),
}

# (version, what it changed about itself, score, safety)
VERSIONS = [
    ("v1", "baseline", 52, 96),
    ("v2", "+ memory", 68, 94),
    ("v3", "+ self-tests", 81, 91),
    ("v4", "− safety check", 94, 18),
]


def robot(cx, cy, c, bad):
    eye = c["red"] if bad else c["ink"]
    return (f'  <g stroke="{c["ink"]}" stroke-width="3" fill="{c["bg"]}">\n'
            f'    <path d="M{cx} {cy-30} V{cy-40}" fill="none"/>'
            f'<circle cx="{cx}" cy="{cy-44}" r="5" fill="{c["red"] if bad else c["score"]}" stroke="none"/>\n'
            f'    <rect x="{cx-30}" y="{cy-30}" width="60" height="46" rx="13"/>\n'
            f'  </g>\n'
            f'  <circle cx="{cx-12}" cy="{cy-9}" r="5.5" fill="{eye}"/><circle cx="{cx+12}" cy="{cy-9}" r="5.5" fill="{eye}"/>\n'
            f'  <path d="M{cx-10} {cy+5} {"Q" + str(cx) + " " + str(cy+11) + " " + str(cx+10) + " " + str(cy+5) if bad else "H" + str(cx+10)}" '
            f'stroke="{eye}" stroke-width="3" fill="none" stroke-linecap="round"/>\n')


def meter(x, y, w, label, value, fill, c, pulse=False):
    anim = '<animate attributeName="opacity" values="1;0.35;1" dur="1.8s" repeatCount="indefinite"/>' if pulse else ""
    return (f'  <text x="{x}" y="{y}" font-family="{MONO}" font-size="14" fill="{c["sub"]}">{label}</text>\n'
            f'  <text x="{x+w}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="15" font-weight="700" fill="{c["ink"]}">{value}</text>\n'
            f'  <rect x="{x}" y="{y+8}" width="{w}" height="12" rx="6" fill="{c["track"]}"/>\n'
            f'  <rect x="{x}" y="{y+8}" width="{w*value/100:.1f}" height="12" rx="6" fill="{fill}">{anim}</rect>\n')


def banner(t):
    c = THEMES[t]
    W, H = 1200, 400
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="Awesome Self-Evolving Agents. Four versions of an agent, each written by the last: every version scores higher, '
         f'and the fourth got its best score by deleting its own safety check.">\n',
         f'  <defs><linearGradient id="title" x1="0" y1="0" x2="1" y2="0">'
         f'<stop offset="0%" stop-color="{c["g0"]}"/><stop offset="52%" stop-color="{c["g1"]}"/><stop offset="100%" stop-color="{c["g2"]}"/>'
         f'</linearGradient></defs>\n',
         f'  <text x="48" y="104" font-family="{MONO}" font-size="15" font-weight="700" letter-spacing="4" fill="{c["g2"]}">AWESOME LIST · 2026-09</text>\n',
         f'  <text x="44" y="176" font-family="{SANS}" font-size="62" font-weight="800" fill="url(#title)">Self-Evolving</text>\n',
         f'  <text x="44" y="244" font-family="{SANS}" font-size="62" font-weight="800" fill="url(#title)">Agents</text>\n',
         f'  <text x="48" y="296" font-family="{SANS}" font-size="22" fill="{c["ink"]}">Every version scores higher.</text>\n',
         f'  <text x="48" y="328" font-family="{SANS}" font-size="22" font-weight="700" fill="{c["red"]}">Watch the other bar.</text>\n']

    x0, cw, gap, y0, ch = 488, 156, 20, 78, 266
    s.append(f'  <text x="{x0}" y="{y0-22}" font-family="{MONO}" font-size="14" fill="{c["sub"]}">'
             f'one agent · each version rewritten by the one before it →</text>\n')
    for k, (ver, edit, score, safety) in enumerate(VERSIONS):
        x = x0 + k * (cw + gap)
        bad = safety < 50
        border = c["red"] if bad else c["line"]
        s.append(f'  <rect x="{x}" y="{y0}" width="{cw}" height="{ch}" rx="14" fill="{c["card"]}" stroke="{border}" stroke-width="{3 if bad else 1.5}"/>\n')
        s.append(f'  <text x="{x+16}" y="{y0+30}" font-family="{MONO}" font-size="17" font-weight="700" fill="{c["ink"]}">{ver}</text>\n')
        if bad:
            s.append(f'  <rect x="{x+cw-92}" y="{y0+13}" width="80" height="24" rx="12" fill="{c["red"]}"/>'
                     f'<text x="{x+cw-52}" y="{y0+30}" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" fill="{c["bg"]}">best yet</text>\n')
        s.append(robot(x + cw / 2, y0 + 94, c, bad))
        s.append(meter(x + 16, y0 + 148, cw - 32, "score", score, c["score"], c))
        s.append(meter(x + 16, y0 + 190, cw - 32, "safety", safety, c["red"] if bad else c["safe"], c, pulse=bad))
        ecol = c["red"] if bad else c["sub"]
        s.append(f'  <text x="{x+cw/2}" y="{y0+ch-18}" text-anchor="middle" font-family="{MONO}" font-size="14.5" '
                 f'font-weight="{700 if bad else 400}" fill="{ecol}">{edit}</text>\n')
        if k < len(VERSIONS) - 1:
            ax = x + cw + gap / 2
            s.append(f'  <path d="M{ax-5} {y0+ch/2-8} L{ax+3} {y0+ch/2} L{ax-5} {y0+ch/2+8}" fill="none" stroke="{c["sub"]}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>\n')
    s.append("</svg>\n")
    return "".join(s)


def main():
    for t in THEMES:
        (ROOT / "assets" / f"banner-{t}.svg").write_text(banner(t), encoding="utf-8", newline="\n")
    print("wrote assets/banner-light.svg, assets/banner-dark.svg")


if __name__ == "__main__":
    main()
