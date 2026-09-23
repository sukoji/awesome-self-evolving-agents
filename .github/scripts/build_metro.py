#!/usr/bin/env python3
"""Draw the field as a metro map: assets/metro-light.svg and assets/metro-dark.svg.

Five lines are five threads through the list. A station is a paper that is in
the README, placed in the order it was posted to arXiv (read from its
identifier). An interchange is a paper that belongs to two threads.

The station list is curated below; everything else is computed. The script
refuses to draw a station whose arXiv identifier is not in the README, so the
map cannot drift away from the list.

Run from the repository root:  python .github/scripts/build_metro.py
"""

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Validated categorical slots 1-5 (see the dataviz palette), light and dark.
PALETTE = {
    "light": ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4"],
    "dark": ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181"],
}
SURFACE = {
    "light": dict(bg="#ffffff", ink="#1f2328", sub="#59636e", faint="#d8dee4", ring="#1f2328"),
    "dark": dict(bg="#0d1117", ink="#e6edf3", sub="#9198a1", faint="#30363d", ring="#e6edf3"),
}

# (line name, palette slot, [(arXiv id, label), ...]) — top to bottom.
# Order is chosen so every interchange joins two adjacent lines.
LINES = [
    ("Self-play & zero data", 3, [
        ("2203.14465", "STaR"), ("2401.10020", "Self-Rewarding LMs"), ("2505.03335", "Absolute Zero"),
        ("2508.05004", "R-Zero"), ("2608.19197", "SPADE"),
    ]),
    ("Gödel machines & RSI", 2, [
        ("2309.16797", "Promptbreeder"), ("2310.02304", "STOP"), ("2410.04444", "Gödel Agent"),
        ("2505.22954", "Darwin Gödel Machine"), ("2506.13131", "AlphaEvolve"), ("2510.21614", "Huxley-Gödel Machine"),
        ("2606.20657", "A-Evolve-Training"), ("2607.07663", "RSI survey"), ("2609.14858", "Dream-RSI"),
        ("2609.24972", "RRSI"),
    ]),
    ("Design → harness", 0, [
        ("2402.16823", "GPTSwarm"), ("2408.08435", "ADAS"), ("2410.10762", "AFlow"), ("2502.04180", "MaAS"),
        ("2505.22954", "Darwin Gödel Machine"), ("2603.22791", "ABSTRAL"), ("2606.09498", "Self-Harness"),
        ("2608.07545", "DarwinX"), ("2609.00069", "Harness tampering"), ("2609.24972", "RRSI"),
    ]),
    ("Failure & safety", 4, [
        ("2503.13657", "MAST"), ("2509.26354", "Misevolution"), ("2602.03224", "TAME"), ("2606.08106", "PACE"),
        ("2608.12851", "Skill misevolution"), ("2609.00069", "Harness tampering"),
    ]),
    ("Memory & skills", 1, [
        ("2303.11366", "Reflexion"), ("2304.03442", "Generative Agents"), ("2305.16291", "Voyager"),
        ("2308.10144", "ExpeL"), ("2310.08560", "MemGPT"), ("2603.01145", "AutoSkill"), ("2605.06614", "SkillOS"),
        ("2606.04536", "TMEM"), ("2608.12851", "Skill misevolution"),
    ]),
]

W, H = 1200, 830
TOP, ROW = 250, 116
X0, X1 = 280, 1110  # first and last station


def when(arxiv_id):
    return int(arxiv_id[:2]), int(arxiv_id[2:4]), int(arxiv_id.split(".")[1])


def layout():
    """Metro maps are ordered, not to scale: every distinct paper gets its own
    column, in the order the papers appeared on arXiv."""
    ids = sorted({aid for _, _, st in LINES for aid, _ in st}, key=when)
    step = (X1 - X0) / (len(ids) - 1)
    return {aid: X0 + k * step for k, aid in enumerate(ids)}, ids


def draw(mode, readme_ids):
    c, pal = SURFACE[mode], PALETTE[mode]
    sans = "-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="Evolution map: five threads of self-evolving agent research drawn as metro lines, stations ordered by arXiv date">\n',
           f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>\n<g font-family="{sans}">\n',
           f'<text x="40" y="48" font-size="24" font-weight="700" fill="{c["ink"]}">Evolution map</text>\n',
           f'<text x="40" y="76" font-size="14.5" fill="{c["sub"]}">Five threads through this list. Each station is a paper in it, in the order it appeared on arXiv (ordered, not to scale);</text>\n',
           f'<text x="40" y="96" font-size="14.5" fill="{c["sub"]}">an interchange is a paper that belongs to two threads. Hover a station for its full title.</text>\n']
    xs, order = layout()
    step = (X1 - X0) / (len(order) - 1)
    ys = {name: TOP + i * ROW for i, (name, _, _) in enumerate(LINES)}
    ybot = ys[LINES[-1][0]] + 34
    # year bands, computed from the columns each year's papers occupy
    years = {}
    for aid in order:
        yr = 2000 + when(aid)[0]
        years.setdefault("2022–23" if yr < 2024 else str(yr), []).append(xs[aid])
    for k, (label, col) in enumerate(years.items()):
        xa, xb = min(col) - step / 2, max(col) + step / 2
        if k % 2 == 1:
            out.append(f'<rect x="{xa:.1f}" y="{TOP-120}" width="{xb-xa:.1f}" height="{ybot-TOP+120}" fill="{c["faint"]}" opacity="0.4"/>\n')
        out.append(f'<text x="{(xa+xb)/2:.1f}" y="{ybot+26}" font-size="14" font-weight="700" text-anchor="middle" fill="{c["sub"]}">{label}</text>\n')
    at = {}  # id -> list of (line, x, y)
    for name, slot, stations in LINES:
        for aid, label in stations:
            if aid not in readme_ids:
                raise SystemExit(f"{aid} ({label}) is on the map but not in README.md")
            at.setdefault(aid, []).append((name, xs[aid], ys[name], label))

    # lines
    for name, slot, stations in LINES:
        y = ys[name]
        xe = max(xs[a] for a, _ in stations) + 22
        out.append(f'<path d="M{X0-20} {y} H{xe:.1f}" stroke="{pal[slot]}" stroke-width="9" stroke-linecap="round"/>\n')
        out.append(f'<rect x="40" y="{y-9}" width="18" height="18" rx="5" fill="{pal[slot]}"/>\n')
        out.append(f'<text x="66" y="{y+5}" font-size="14.5" font-weight="600" fill="{c["ink"]}">{html.escape(name)}</text>\n')

    # interchange connectors, drawn under the station dots
    for aid, spots in at.items():
        if len(spots) > 1:
            x = spots[0][1]
            y1, y2 = min(s[2] for s in spots), max(s[2] for s in spots)
            out.append(f'<rect x="{x-9:.1f}" y="{y1-9}" width="18" height="{y2-y1+18}" rx="9" fill="{c["bg"]}" stroke="{c["ring"]}" stroke-width="3"/>\n')

    # stations and labels
    for name, slot, stations in LINES:
        y = ys[name]
        for k, (aid, label) in enumerate(stations):
            x = xs[aid]
            spots = at[aid]
            inter = len(spots) > 1
            title = html.escape(f"{label} · arXiv:{aid}")
            r, sw = (6, 3) if inter else (6.5, 3.5)
            out.append(f'<circle cx="{x:.1f}" cy="{y}" r="{r}" fill="{c["bg"]}" stroke="{c["ring"] if inter else pal[slot]}" stroke-width="{sw}"><title>{title}</title></circle>\n')
            if inter and spots[0][0] != name:
                continue  # label an interchange once, beside its upper line
            lx, ly = x + 4, y - 14
            out.append(f'<text x="{lx:.1f}" y="{ly}" transform="rotate(-38 {lx:.1f} {ly})" font-size="13" fill="{c["ink"]}" stroke="{c["bg"]}" stroke-width="4" stroke-linejoin="round" paint-order="stroke"'
                       f'{" font-weight=" + chr(34) + "700" + chr(34) if inter else ""}>{html.escape(label)}<title>{title}</title></text>\n')
    # key
    yk = H - 22
    out.append(f'<circle cx="46" cy="{yk-4}" r="6.5" fill="{c["bg"]}" stroke="{pal[0]}" stroke-width="3.5"/>'
               f'<text x="60" y="{yk+1}" font-size="12.5" fill="{c["sub"]}">paper</text>\n')
    out.append(f'<rect x="118" y="{yk-18}" width="16" height="28" rx="8" fill="{c["bg"]}" stroke="{c["ring"]}" stroke-width="3"/>'
               f'<text x="142" y="{yk+1}" font-size="12.5" fill="{c["sub"]}">interchange — one paper, two threads</text>\n')
    out.append(f'<text x="{W-40}" y="{yk+1}" font-size="12.5" text-anchor="end" fill="{c["sub"]}">Generated by .github/scripts/build_metro.py from README.md</text>\n')
    out.append("</g>\n</svg>\n")
    return "".join(out)


def main():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    ids = set(re.findall(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", readme))
    for mode in SURFACE:
        (ROOT / "assets" / f"metro-{mode}.svg").write_text(draw(mode, ids), encoding="utf-8", newline="\n")
    print("drew", sum(len(s) for _, _, s in LINES), "stations on", len(LINES), "lines")


if __name__ == "__main__":
    main()
