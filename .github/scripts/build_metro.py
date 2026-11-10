#!/usr/bin/env python3
"""Draw the field as a metro map: assets/metro-light.svg and assets/metro-dark.svg.

Six lines are six threads through the list. A station is a paper that is in
the README, placed in the order it was posted to arXiv (read from its
identifier). An interchange is a paper that belongs to two threads. A dashed
marker notes an outside event that the research timeline should be read
against.

The station list is curated below; everything else is computed, including
where each label goes: every label tries a few positions and takes the first
that collides with no other label, station, or line. The script refuses to
draw a station whose arXiv identifier is not in the README, so the map cannot
drift away from the list.

Run from the repository root:  python .github/scripts/build_metro.py
"""

import html
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Validated categorical slots 1-6 (see the dataviz palette), light and dark.
PALETTE = {
    "light": ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#8a63d2"],
    "dark": ["#3987e5", "#d95926", "#199e70", "#c98500", "#d55181", "#9a7be0"],
}
SURFACE = {
    "light": dict(bg="#ffffff", ink="#1f2328", sub="#59636e", faint="#d8dee4", ring="#1f2328", core="#1a7f64"),
    "dark": dict(bg="#0d1117", ink="#e6edf3", sub="#9198a1", faint="#30363d", ring="#e6edf3", core="#2fbf88"),
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
        ("2603.19461", "Hyperagents"), ("2606.20657", "A-Evolve-Training"), ("2607.07663", "RSI survey"),
        ("2609.24972", "RRSI"), ("2609.26457", "AIDE²"), ("2610.11794", "Memento 3"),
        ("2611.03698", "RSI-Dojo"), ("2611.04035", "Recursa"),
    ]),
    ("Design → harness", 0, [
        ("2402.16823", "GPTSwarm"), ("2408.08435", "ADAS"), ("2410.10762", "AFlow"), ("2502.04180", "MaAS"),
        ("2505.22954", "Darwin Gödel Machine"), ("2603.22791", "ABSTRAL"), ("2606.09498", "Self-Harness"),
        ("2608.07545", "DarwinX"), ("2609.00069", "Harness tampering"), ("2609.24972", "RRSI"),
        ("2610.13025", "Evo²"), ("2611.05139", "Meta²"), ("2611.07624", "Beneath the Surface"),
    ]),
    ("Failure & safety", 4, [
        ("2503.13657", "MAST"), ("2509.26354", "Misevolution"), ("2602.03224", "TAME"), ("2606.08106", "PACE"),
        ("2608.12851", "Skill misevolution"), ("2609.00069", "Harness tampering"), ("2610.27735", "RSI Control"),
        ("2610.38392", "Masked Erosion"), ("2610.39122", "Appreciation Teaches…"), ("2611.07624", "Beneath the Surface"),
    ]),
    ("Memory & skills", 1, [
        ("2303.11366", "Reflexion"), ("2304.03442", "Generative Agents"), ("2305.16291", "Voyager"),
        ("2308.10144", "ExpeL"), ("2310.08560", "MemGPT"), ("2511.20857", "Evo-Memory"), ("2603.01145", "AutoSkill"),
        ("2605.06614", "SkillOS"), ("2606.04536", "TMEM"), ("2608.12851", "Skill misevolution"),
        ("2610.11373", "Repertoires"), ("2611.00544", "Skill++"),
    ]),
    ("Evaluation & audit", 5, [
        ("2502.14499", "MLGym"), ("2505.11942", "LifelongAgentBench"), ("2508.19005", "StuLife"),
        ("2511.20857", "Evo-Memory"), ("2608.20318", "AI4AI-Bench"), ("2609.04280", "EvoHarnessBench"),
        ("2610.10310", "RSIGym"), ("2610.27610", "Auditing the Product"), ("2611.01736", "RSI-Env"),
        ("2611.02797", "SelfImprove-Bench"),
    ]),
]
# (arXiv month YYMM the event falls in, short text, source) — outside events, not papers.
EVENTS = [
    ("2504", "Apr 2025 · AI 2027 scenario forecasts a superhuman coder by 2027",
     "https://ai-2027.com/"),
    ("2611", "Nov 2026 · Anthropic S-1/A: RSI threshold may be near",
     "https://techcrunch.com/2026/11/02/anthropic-warns-that-its-very-close-to-rsi-capability-aka-self-building-ai/"),
]
# A thread that grew out of another branches off it just before its first paper.
PARENT = {
    "Design → harness": "Gödel machines & RSI",
    "Failure & safety": "Design → harness",
    "Evaluation & audit": "Memory & skills",
}
# The question each thread asks, shown under its name.
PURPOSE = {
    "Self-play & zero data": "learn with no human data",
    "Gödel machines & RSI": "the improver improves itself",
    "Design → harness": "search the agent's own design",
    "Failure & safety": "what breaks as agents evolve",
    "Memory & skills": "learn from experience",
    "Evaluation & audit": "did it really improve?",
}
# What agents learned to change in each period, shown under its year.
W, H = 1200, 1060
TOP, ROW = 200, 132
X0, X1 = 292, 1085  # first and last station
FONT = 12.5


def when(arxiv_id):
    return int(arxiv_id[:2]), int(arxiv_id[2:4]), int(arxiv_id.split(".")[1])


def layout():
    """Metro maps are ordered, not to scale: every distinct paper gets its own
    column, in the order the papers appeared on arXiv."""
    ids = sorted({aid for _, _, st in LINES for aid, _ in st}, key=when)
    lines_of = {aid: {n for n, _, st in LINES if aid in dict(st)} for aid in ids}
    # Labels share a slant, so a station needs a full unit of room only from the
    # previous station on its own line(s); papers on other lines can sit close.
    # Interchanges are wide, so they keep more room from every neighbour.
    pos, last, prev, prev_inter = {}, {}, None, False
    for aid in ids:
        inter = len(lines_of[aid]) > 1
        x = 0.0 if prev is None else pos[prev] + (0.7 if inter or prev_inter else 0.25)
        for line in lines_of[aid]:
            if line in last:
                x = max(x, last[line] + 1.0)
        pos[aid], prev, prev_inter = x, aid, inter
        for line in lines_of[aid]:
            last[line] = x
    scale = (X1 - X0) / pos[ids[-1]]
    return {aid: X0 + p * scale for aid, p in pos.items()}, ids


# --- label placement: rotated rectangles, separating-axis collision test ---

def text_width(label, bold):
    return len(label) * FONT * (0.6 if bold else 0.55)


def label_box(x, y, angle, side, label, bold):
    """Corners of a label's box and its anchor. side "r": the text starts at the
    station; side "l": it ends there, so the label sits on the far side."""
    a = math.radians(angle)
    ux, uy = math.cos(a), math.sin(a)          # along the text
    nx, ny = -uy, ux                           # across it, towards the baseline
    w, h = text_width(label, bold), FONT * 1.05
    if angle == 0:
        ax, ay = (x + 15, y + 4) if side == "r" else (x - 15, y + 4)
        sx, sy = (ax, ay) if side == "r" else (ax - w, ay)
    elif side == "r":
        ax, ay = (x + 6, y - 12) if angle < 0 else (x + 9, y + 9)
        sx, sy = ax, ay
    else:
        ax, ay = (x - 9, y + 16) if angle < 0 else (x - 6, y - 12)
        sx, sy = ax - ux * w, ay - uy * w
    p0 = (sx - nx * (h + 2), sy - ny * (h + 2))   # above the text at its start, with halo
    t = h + 6
    corners = [p0, (p0[0] + ux * w, p0[1] + uy * w),
               (p0[0] + ux * w + nx * t, p0[1] + uy * w + ny * t), (p0[0] + nx * t, p0[1] + ny * t)]
    return corners, (ax, ay)


def rect(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]


def collide(p, q):
    for poly in (p, q):
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
            ax, ay = y1 - y2, x2 - x1
            pa = [ax * x + ay * y for x, y in p]
            qa = [ax * x + ay * y for x, y in q]
            if max(pa) <= min(qa) or max(qa) <= min(pa):
                return False
    return True


def place(obstacles, x, ys, label, bold):
    """First position with no collision, else the one with fewest."""
    best = None
    cands = [(ys[0], -55, "r"), (ys[-1], 55, "r")]
    if len(ys) > 1:  # an interchange may also sit level, beside its connector
        mid = (ys[0] + ys[-1]) / 2
        cands += [(mid, 0, "r"), (mid, 0, "l")]
    cands += [(ys[0], -72, "r"), (ys[-1], 72, "r")]
    for yy, angle, side in cands:
        box, anchor = label_box(x, yy, angle, side, label, bold)
        if (min(px for px, _ in box) < 4 or max(px for px, _ in box) > W - 4
                or min(py for _, py in box) < TOP - 125 or max(py for _, py in box) > H - 70):
            continue
        hits = sum(collide(box, o) for o in obstacles)
        if best is None or hits < best[0]:
            best = (hits, box, anchor, angle, side)
        if hits == 0:
            return best
    return best


def draw(mode, readme_ids):
    c, pal = SURFACE[mode], PALETTE[mode]
    sans = "-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="Evolution map: six threads of self-evolving agent research drawn as metro lines, stations ordered by arXiv date, through November 2026">\n',
           f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>\n<g font-family="{sans}">\n']
    xs, order = layout()
    def edge(k):  # boundary just before column k
        return xs[order[0]] - 10 if k == 0 else (xs[order[k - 1]] + xs[order[k]]) / 2
    def end(k):
        return xs[order[-1]] + 10 if k == len(order) - 1 else edge(k + 1)
    ys = {name: TOP + i * ROW for i, (name, _, _) in enumerate(LINES)}
    ybot = ys[LINES[-1][0]] + 125
    yband = TOP - 128

    # year bands, computed from the columns each year's papers occupy; labels on top
    years = {}
    for aid in order:
        yr = 2000 + when(aid)[0]
        years.setdefault("2022–23" if yr < 2024 else str(yr), []).append(order.index(aid))
    for k, (label, col) in enumerate(years.items()):
        xa, xb = edge(min(col)), end(max(col))
        if k:
            out.append(f'<path d="M{xa:.1f} {yband-62} V{ybot}" stroke="{c["faint"]}" stroke-width="1"/>\n')
        xm = (xa + xb) / 2
        out.append(f'<text x="{xm:.1f}" y="{yband-40}" font-size="14" font-weight="700" text-anchor="middle" fill="{c["ink"]}">{label}</text>\n')

    at = {}  # id -> list of (line, x, y, label)
    for name, slot, stations in LINES:
        for aid, label in stations:
            if aid not in readme_ids:
                raise SystemExit(f"{aid} ({label}) is on the map but not in README.md")
            at.setdefault(aid, []).append((name, xs[aid], ys[name], label))

    # outside events: a dashed rule where that month's papers begin
    for k, (month, text, _) in enumerate(EVENTS):
        first = [i for i, a in enumerate(order) if a >= month]
        if not first:
            continue
        xe = edge(first[0])
        out.append(f'<path d="M{xe:.1f} {yband} V{ybot}" stroke="{c["sub"]}" stroke-width="1.2" stroke-dasharray="5 4"/>\n')
        out.append(f'<text x="{xe-6:.1f}" y="{ybot+4}" font-size="12" text-anchor="end" fill="{c["sub"]}">{html.escape(text)}</text>\n')

    obstacles = []
    # lines run from their first station to their last; a branch curves out of its parent
    for name, slot, stations in LINES:
        y = ys[name]
        xa = min(xs[a] for a, _ in stations) - 22
        xb = max(xs[a] for a, _ in stations) + 22
        d = f"M{xa:.1f} {y} H{xb:.1f}"
        if name in PARENT:
            parent = next(st for n, _, st in LINES if n == PARENT[name])
            first = min(xs[a] for a, _ in stations)
            yp = ys[PARENT[name]]
            x0 = max(first - 80, min(xs[a] for a, _ in parent))  # leave the parent where it already runs
            xa = first - 8
            k = (xa - x0) * 0.6
            d = f"M{x0:.1f} {yp} C{x0+k:.1f} {yp} {xa-k:.1f} {y} {xa:.1f} {y} H{xb:.1f}"
            for i in range(9):  # the curve, as small boxes, so labels avoid it
                t = i / 8
                px = (1-t)**3*x0 + 3*(1-t)**2*t*(x0+k) + 3*(1-t)*t*t*(xa-k) + t**3*xa
                py = (1-t)**3*yp + 3*(1-t)**2*t*yp + 3*(1-t)*t*t*y + t**3*y
                obstacles.append(rect(px - 6, py - 6, px + 6, py + 6))
        out.append(f'<path d="{d}" fill="none" stroke="{pal[slot]}" stroke-width="7" stroke-linecap="round"/>\n')
        out.append(f'<path d="M43 {y-6} H57" stroke="{pal[slot]}" stroke-width="7" stroke-linecap="round"/>\n')
        out.append(f'<text x="68" y="{y-1}" font-size="14.5" font-weight="600" fill="{c["ink"]}">{html.escape(name)}</text>\n')
        out.append(f'<text x="68" y="{y+16}" font-size="12.5" fill="{c["sub"]}">{html.escape(PURPOSE[name])}</text>\n')
        obstacles.append(rect(xa, y - 6, xb, y + 6))
        obstacles.append(rect(40, y - 18, 66 + max(text_width(name, True), text_width(PURPOSE[name], False)), y + 20))

    # interchange connectors, drawn under the station dots
    for aid, spots in at.items():
        if len(spots) > 1:
            x = spots[0][1]
            y1, y2 = min(s[2] for s in spots), max(s[2] for s in spots)
            out.append(f'<rect x="{x-9:.1f}" y="{y1-9}" width="18" height="{y2-y1+18}" rx="9" fill="{c["bg"]}" stroke="{c["ring"]}" stroke-width="2.5"/>\n')
            obstacles.append(rect(x - 10, y1 - 10, x + 10, y2 + 10))
    for aid, spots in at.items():
        for _, x, y, _ in spots:
            obstacles.append(rect(x - 8, y - 8, x + 8, y + 8))

    # stations, then labels in column order so crowded runs alternate sides
    labels = []
    for name, slot, stations in LINES:
        y = ys[name]
        for aid, label in stations:
            x = xs[aid]
            inter = len(at[aid]) > 1
            title = html.escape(f"{label} · arXiv:{aid}")
            out.append(f'<circle cx="{x:.1f}" cy="{y}" r="5" fill="{c["bg"]}" stroke="{c["ring"] if inter else pal[slot]}" '
                       f'stroke-width="{2.5 if inter else 3}"><title>{title}</title></circle>\n')
            if inter and at[aid][0][0] != name:
                continue  # an interchange is labelled once
            labels.append((x, aid, label, inter))
    for x, aid, label, inter in sorted(labels):
        spots = at[aid]
        title = html.escape(f"{label} · arXiv:{aid}")
        hits, box, (lx, ly), ang, side = place(obstacles, x, sorted(s[2] for s in spots), label, inter)
        obstacles.append(box)
        weight = ' font-weight="700"' if inter else ""
        anchor = ' text-anchor="end"' if side == "l" else ""
        out.append(f'<text x="{lx:.1f}" y="{ly:.1f}" transform="rotate({ang} {lx:.1f} {ly:.1f})" font-size="{FONT}" fill="{c["ink"]}" '
                   f'stroke="{c["bg"]}" stroke-width="4" stroke-linejoin="round" paint-order="stroke"{weight}{anchor}>{html.escape(label)}<title>{title}</title></text>\n')
        if hits:
            print(f"  warning: {label} overlaps {hits} item(s)")

    # key
    yk = H - 20
    out.append(f'<circle cx="46" cy="{yk-4}" r="5" fill="{c["bg"]}" stroke="{c["sub"]}" stroke-width="3"/>'
               f'<text x="60" y="{yk}" font-size="12" fill="{c["sub"]}">paper</text>\n')
    out.append(f'<rect x="120" y="{yk-17}" width="16" height="26" rx="8" fill="{c["bg"]}" stroke="{c["ring"]}" stroke-width="2.5"/>'
               f'<text x="144" y="{yk}" font-size="12" fill="{c["sub"]}">interchange: one paper on two threads</text>\n')
    out.append(f'<path d="M400 {yk-16} V{yk+8}" stroke="{c["sub"]}" stroke-width="1.2" stroke-dasharray="5 4"/>'
               f'<text x="410" y="{yk}" font-size="12" fill="{c["sub"]}">outside event</text>\n')
    out.append("</g>\n</svg>\n")
    return "".join(out)


def main():
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    ids = set(re.findall(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", readme))
    for mode in SURFACE:
        (ROOT / "assets" / f"metro-{mode}.svg").write_text(draw(mode, ids), encoding="utf-8", newline="\n")
    print("drew", sum(len(s) for _, _, s in LINES), "stations on", len(LINES), "lines")


if __name__ == "__main__":
    main()
