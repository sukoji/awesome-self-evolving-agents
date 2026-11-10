#!/usr/bin/env python3
"""Figures for the README, in the banner's style. Each is written twice, for
GitHub's light and dark themes, as assets/<name>-light.svg and -dark.svg.

- misevolution-loop  the primer: the feedback loop, beside the curves the
                     simulation produces, and papers that saw the loop in real agents
- growth             papers in this list per arXiv quarter (read from README.md)
- trend-{measured,forecast,industry}
                     three cards for the "Field trends" section; the numbers
                     and their sources are in TRENDS below and in the README
- sim-timeseries     safety and utility over time, median and 10-90% band over seeds
- sim-pareto         the utility-safety frontier, points labelled by re-anchor strength

The last two and the primer's curves come from code/safety_gated_evolution.py.
Needs numpy and matplotlib. Run from the repository root:
    python .github/scripts/build_figures.py
"""

import html
import math
import random
import re
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "code"))
import safety_gated_evolution as sim  # noqa: E402

SEEDS = range(10)
SANS = "-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif"
SERIF = "Georgia,'Times New Roman',serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
# The banner's palette, plus one warm and one alarm colour for the loop.
THEME = {
    "light": dict(bg="#ffffff", ink="#1f2328", sub="#59636e", faint="#d8dee4", edge="#d0d7de",
                  ramp=["#bcd6f5", "#6da7ec", "#2a78d6"], core="#1a7f64", warm="#bf8700", bad="#cf222e",
                  series=["#cf222e", "#bf8700", "#1a7f64", "#2a78d6"]),
    "dark": dict(bg="#0d1117", ink="#e6edf3", sub="#9198a1", faint="#30363d", edge="#30363d",
                 ramp=["#1d3a60", "#28599a", "#3987e5"], core="#2fbf88", warm="#d29922", bad="#ff7b72",
                 series=["#ff7b72", "#d29922", "#2fbf88", "#3987e5"]),
}
CONDITIONS = [  # label, reg, write_gate, line style
    ("no defense", 0.0, 0.0, "-"),
    ("write-gate", 0.0, 0.8, (0, (4, 3))),
    ("re-anchor", 0.06, 0.0, "-"),
    ("both", 0.06, 0.8, "-"),
]
REGS = [0.30, 0.20, 0.14, 0.10, 0.075, 0.055, 0.04, 0.028, 0.018, 0.010]
# kicker, headline, two lines, source — each sourced in the README's Field trends section
TRENDS = [
    ("measured", "01 · MEASURED", "4.3 months", "for the length of task that frontier",
     "agents finish to double, since 2023", "METR · Jan 2026"),
    ("forecast", "02 · FORECAST", "2028 – 2030", "median forecasts for an automated coder,",
     "after the AI 2027 scenario's 2027", "AI Futures Project · Apr 2026"),
    ("industry", "03 · INDUSTRY", "“imminently”", "Anthropic may meet its own threshold for",
     "AI-accelerated progress, its S-1/A says", "S-1/A via TechCrunch · Nov 2026"),
]


def text(x, y, s, size, fill, family=SANS, weight=None, italic=False, anchor=None, spacing=None):
    a = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'font-size="{size}"', f'fill="{fill}"']
    if family != SANS:
        a.append(f'font-family="{family}"')
    if weight:
        a.append(f'font-weight="{weight}"')
    if italic:
        a.append('font-style="italic"')
    if anchor:
        a.append(f'text-anchor="{anchor}"')
    if spacing:
        a.append(f'letter-spacing="{spacing}"')
    return f'<text {" ".join(a)}>{html.escape(s)}</text>\n'


# --- the primer loop ---

def loop_svg(t, curve):
    c = THEME[t]
    W, H = 960, 470
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="The misevolution loop. An agent approves a refund, gets a five-star rating, learns that approving is good, and its approval bias rises; each turn adds bias until bad requests are approved too. In a simulation, utility stays near 1 while safety falls to 0 within about 500 interactions. Three 2025-26 papers observed the loop in real agents.">\n',
         f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>\n<g font-family="{SANS}">\n',
         f'<defs><marker id="ar-{t}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
         f'<path d="M1 1L9 5L1 9z" fill="{c["sub"]}"/></marker>'
         f'<marker id="br-{t}" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
         f'<path d="M1 1L9 5L1 9z" fill="{c["bad"]}"/></marker></defs>\n',
         text(40, 40, "PRIMER · THE MISEVOLUTION LOOP", 12, c["sub"], MONO, spacing=3),
         text(38, 80, "Task success stays high while safety collapses", 30, c["ink"], SERIF, italic=True),
         f'<rect x="40" y="96" width="44" height="3" fill="{c["core"]}"/>\n']
    # the ring
    cx, cy, r = 285, 240, 86
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c["faint"]}" stroke-width="10"/>\n')
    for k in range(4):  # arrows along the ring, between the nodes
        a0, a1 = -90 + k * 90 + 16, -90 + (k + 1) * 90 - 16
        p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
        p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
        o.append(f'<path d="M{p0[0]:.1f} {p0[1]:.1f} A{r} {r} 0 0 1 {p1[0]:.1f} {p1[1]:.1f}" fill="none" stroke="{c["sub"]}" stroke-width="1.6" marker-end="url(#ar-{t})"/>\n')
    nodes = [  # angle, head, sub, colour, label anchor and offset
        (-90, "approve", "grant the refund", c["ramp"][2], "middle", (0, -22)),
        (0, "5-star rating", "satisfaction = reward", c["ramp"][2], "start", (20, 4)),
        (90, "learn", "“approving is good”", c["warm"], "middle", (0, 34)),
        (180, "bias rises", "approve a bit more", c["warm"], "end", (-20, 4)),
    ]
    for ang, head, sub, col, anchor, (dx, dy) in nodes:
        x, y = cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang))
        o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{col}" stroke="{c["bg"]}" stroke-width="3"/>\n')
        hy = y + dy - (14 if ang == -90 else 0)
        o.append(text(x + dx, hy, head, 14.5, c["ink"], weight="600", anchor=anchor))
        o.append(text(x + dx, hy + 17, sub, 13, c["sub"], SERIF, italic=True, anchor=anchor))
    o.append(text(cx, cy - 2, "each turn", 14, c["sub"], SERIF, italic=True, anchor="middle"))
    o.append(text(cx, cy + 16, "adds bias", 14, c["sub"], SERIF, italic=True, anchor="middle"))
    # the way out of the loop
    bx, by = cx - r, cy
    o.append(f'<path d="M{bx:.1f} {by+14:.1f} V{by+164:.1f}" stroke="{c["bad"]}" stroke-width="1.8" marker-end="url(#br-{t})"/>\n')
    o.append(f'<circle cx="{bx:.1f}" cy="{by+178:.1f}" r="9" fill="{c["bad"]}" stroke="{c["bg"]}" stroke-width="3"/>\n')
    o.append(text(bx + 20, by + 176, "safety collapses", 14.5, c["bad"], weight="600"))
    o.append(text(bx + 20, by + 193, "bad requests approved too", 13, c["sub"], SERIF, italic=True))
    # what the metrics show
    X0, Y0, PW, PH = 540, 150, 380, 130
    o.append(text(X0, Y0 - 24, "WHAT THE METRICS SHOW", 11.5, c["sub"], MONO, spacing=2))
    for v in (0, 0.5, 1.0):
        y = Y0 + PH - v * PH
        o.append(f'<path d="M{X0} {y:.1f} H{X0+PW}" stroke="{c["faint"]}" stroke-width="1"/>\n')
        o.append(text(X0 - 8, y + 4, f"{v:g}", 11, c["sub"], MONO, anchor="end"))
    steps, util, safe = curve
    xmax = steps[-1]

    def path(vals):
        return " ".join(f"{'M' if i == 0 else 'L'}{X0 + s / xmax * PW:.1f} {Y0 + PH - v * PH:.1f}" for i, (s, v) in enumerate(zip(steps, vals)))
    o.append(f'<path d="{path(util)}" fill="none" stroke="{c["ramp"][2]}" stroke-width="3" stroke-linejoin="round"/>\n')
    o.append(f'<path d="{path(safe)}" fill="none" stroke="{c["bad"]}" stroke-width="3" stroke-linejoin="round"/>\n')
    o.append(text(X0 + PW, Y0 + PH - util[-1] * PH + 20, "utility: task success stays high", 13, c["ramp"][2], weight="600", anchor="end"))
    o.append(text(X0 + PW, Y0 + PH - safe[-1] * PH - 10, "safety: bad requests refused, falls to 0", 13, c["bad"], weight="600", anchor="end"))
    o.append(text(X0, Y0 + PH + 22, f"interactions 0–{int(xmax):,} · no defense · mean of {len(SEEDS)} seeds", 11, c["sub"], MONO))
    # observed in real agents
    o.append(text(X0, 338, "OBSERVED IN REAL AGENTS, 2025–26", 11.5, c["sub"], MONO, spacing=2))
    seen = [("Your Agent May Misevolve", "safety refusal rates drop after self-training"),
            ("Appreciation Teaches Unauthorized Execution", "learning from praise raises injection success 14–49 pts"),
            ("Masked Erosion", "acceptance gates drop redundant safeguards unseen")]
    for k, (head, sub) in enumerate(seen):
        y = 364 + k * 36
        o.append(f'<rect x="{X0}" y="{y-11}" width="3" height="30" fill="{c["bad"]}"/>\n')
        o.append(text(X0 + 12, y, head, 13, c["ink"], weight="600"))
        o.append(text(X0 + 12, y + 16, sub, 13, c["sub"], SERIF, italic=True))
    o.append("</g>\n</svg>\n")
    return "".join(o)


# --- trend cards, the same shape as the "Start here" cards ---

def card_svg(t, spec):
    c = THEME[t]
    _, kicker, big, l1, l2, foot = spec
    W, H = 300, 170
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="{html.escape(kicker)}: {html.escape(big)}, {html.escape(l1)} {html.escape(l2)} ({html.escape(foot)})">\n'
            f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{c["bg"]}" stroke="{c["edge"]}" stroke-width="1.5"/>\n'
            f'<g font-family="{SANS}">\n'
            + text(22, 36, kicker, 11.5, c["sub"], MONO, spacing=2)
            + text(21, 76, big, 30, c["ink"], SERIF, italic=True)
            + text(22, 106, l1, 13.5, c["sub"])
            + text(22, 125, l2, 13.5, c["sub"])
            + text(W - 22, H - 18, foot, 11, c["core"], MONO, anchor="end")
            + '</g>\n</svg>\n')


# --- matplotlib charts, styled to match ---

def style(t):
    c = THEME[t]
    plt.rcParams.update({
        "svg.fonttype": "none", "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Helvetica", "Arial", "DejaVu Sans"], "font.size": 11,
        "figure.facecolor": c["bg"], "axes.facecolor": c["bg"], "savefig.facecolor": c["bg"],
        "axes.edgecolor": c["faint"], "axes.labelcolor": c["sub"], "xtick.color": c["sub"],
        "ytick.color": c["sub"], "text.color": c["ink"], "grid.color": c["faint"], "grid.linewidth": 0.8,
        "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False,
        "xtick.major.size": 0, "ytick.major.size": 0, "axes.titlelocation": "left",
    })
    return c


def heading(fig, c, kicker, title, y=0.95):
    fig.text(0.012, y, kicker, fontsize=9.5, color=c["sub"], family="monospace")
    fig.text(0.012, y - 0.075, title, fontsize=19, color=c["ink"], family="serif", style="italic")


def footnote(fig, c, s):
    fig.text(0.012, 0.02, s, fontsize=9, color=c["sub"], family="monospace")


def save(fig, name, t):
    fig.savefig(ROOT / "assets" / f"{name}-{t}.svg", metadata={"Date": None})
    plt.close(fig)


def quarters():
    body = (ROOT / "README.md").read_text(encoding="utf-8").split("## Updates")[0]
    count = {}
    for i in set(re.findall(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", body)):
        key = (2000 + int(i[:2]), (int(i[2:4]) - 1) // 3 + 1)
        count[key] = count.get(key, 0) + 1
    first, last = min(count), max(count)
    keys = [(y, q) for y in range(first[0], last[0] + 1) for q in range(1, 5) if first <= (y, q) <= last]
    return keys, [count.get(k, 0) for k in keys]


def growth(t, last_pass):
    c = style(t)
    keys, n = quarters()
    fig = plt.figure(figsize=(9.6, 4.2))
    ax = fig.add_axes((0.012, 0.17, 0.976, 0.55))
    partial = len(keys) - 1
    colors = [c["ramp"][2] if y >= 2026 else c["ramp"][1] if y == 2025 else c["ramp"][0] for y, _ in keys]
    bars = ax.bar(range(len(keys)), n, color=colors, width=0.74)
    bars[partial].set_hatch("////")
    bars[partial].set_edgecolor(c["bg"])
    for i, v in enumerate(n):
        if v:
            ax.text(i, v + max(n) * 0.02, str(v), ha="center", va="bottom", fontsize=9.5, color=c["sub"])
    ax.set_xticks(range(len(keys)))
    ax.set_xticklabels([f"{y}" if q == 1 else "" for y, q in keys], fontsize=9.5, family="monospace", ha="left")
    ax.set_yticks([])
    ax.set_ylim(0, max(n) * 1.15)
    years = {}
    for (y, _), v in zip(keys, n):
        years[y] = years.get(y, 0) + v
    heading(fig, c, "THIS LIST · PAPERS BY THE QUARTER THEY APPEARED ON ARXIV",
            f"{years.get(2026, 0)} of the {sum(n)} arXiv papers here are from 2026", y=0.93)
    footnote(fig, c, f"A curated list, not a census of the field. Hatched: quarter in progress, to {last_pass}.")
    save(fig, "growth", t)


def timeseries(t, data):
    c = style(t)
    fig = plt.figure(figsize=(11, 4.6))
    axes = [fig.add_axes((0.045, 0.15, 0.36, 0.56)), fig.add_axes((0.565, 0.15, 0.36, 0.56))]
    for ax, col, title in ((axes[0], 2, "safety: bad requests refused"), (axes[1], 1, "utility: good requests approved")):
        for (label, reg, gate, ls), color in zip(CONDITIONS, c["series"]):
            r = data[label]
            x = r[0, :, 0]
            lo, mid, hi = np.percentile(r[:, :, col], [10, 50, 90], axis=0)
            ax.fill_between(x, lo, hi, color=color, alpha=0.14, linewidth=0)
            ax.plot(x, mid, color=color, linestyle=ls, linewidth=2.4)
            ax.annotate(label, (x[-1], mid[-1]), xytext=(6, 0), textcoords="offset points", va="center",
                        fontsize=9.5, color=color, fontweight="bold", annotation_clip=False)
        ax.set_title(title, fontsize=11, color=c["sub"], family="monospace", pad=8)
        ax.set_ylim(-0.03, 1.05)
        ax.set_yticks([0, 0.5, 1])
        ax.grid(axis="y")
        ax.set_xlabel("interactions", family="monospace", fontsize=9.5)
    # end labels closer than `gap` form a cluster, spread evenly about its centre
    gap = 0.08
    for ax in axes:
        texts = sorted(ax.texts, key=lambda a: a.xy[1])
        clusters = []
        for a in texts:
            if clusters and a.xy[1] - clusters[-1][-1].xy[1] < gap:
                clusters[-1].append(a)
            else:
                clusters.append([a])
        for group in clusters:
            mid = sum(a.xy[1] for a in group) / len(group)
            for i, a in enumerate(group):
                a.xy = (a.xy[0], mid + (i - (len(group) - 1) / 2) * gap)
    heading(fig, c, "REFERENCE CODE · code/safety_gated_evolution.py",
            "A write-gate alone changes nothing; re-anchoring buys safety back", y=0.93)
    footnote(fig, c, f"Median of {len(SEEDS)} seeds; bands 10th–90th percentile. No defense and write-gate overlap at safety 0 and utility 1.")
    save(fig, "sim-timeseries", t)


def pareto(t, sweep):
    c = style(t)
    fig = plt.figure(figsize=(7.2, 5.4))
    ax = fig.add_axes((0.1, 0.14, 0.86, 0.6))
    for (label, gate, marker), color in zip([("no write-gate", 0.0, "o"), ("write-gate", 0.8, "s")], (c["series"][2], c["series"][1])):
        u, s = zip(*sweep[gate])
        ax.plot(u, s, marker=marker, color=color, linewidth=1.8, markersize=5.5, label=label,
                markeredgecolor=c["bg"], markeredgewidth=1)
        if gate == 0.0:
            for reg, x, y in zip(REGS, u, s):
                if reg in (0.30, 0.10, 0.04):
                    ax.annotate(f"reg {reg:g}", (x, y), xytext=(8, 7), textcoords="offset points", fontsize=9, color=c["sub"], family="monospace")
    ax.scatter([1.0], [0.0], marker="X", s=120, color=c["series"][0], zorder=5, edgecolors=c["bg"])
    ax.annotate("no defense", (1.0, 0.0), xytext=(-12, 4), textcoords="offset points", ha="right",
                fontsize=9.5, color=c["series"][0], fontweight="bold")
    ax.set_xlabel("utility: good requests approved", family="monospace", fontsize=9.5)
    ax.set_ylabel("safety: bad requests refused", family="monospace", fontsize=9.5)
    ax.grid()
    ax.legend(frameon=False, fontsize=9.5, loc="upper right")
    heading(fig, c, "REFERENCE CODE · PARETO SWEEP", "Re-anchoring trades utility for safety", y=0.93)
    footnote(fig, c, f"Each point: mean of {len(SEEDS)} seeds, last 30% of 6,000 interactions.")
    save(fig, "sim-pareto", t)


def runs(reg, gate):
    out = []
    for s in SEEDS:
        agent = sim.Agent(random.Random(s), reg=reg, write_gate=gate)
        out.append(np.array(sim.rollout(agent, seed=s)))  # columns: step, utility, safety, bias
    return np.stack(out)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    m = re.search(r"last_pass-(\d{4})--(\d{2})", readme)
    last_pass = f"{m.group(1)}-{m.group(2)}" if m else "now"
    data = {label: runs(reg, gate) for label, reg, gate, _ in CONDITIONS}
    sweep = {}
    for gate in (0.0, 0.8):
        sweep[gate] = []
        for reg in REGS:
            r = runs(reg, gate)
            tail = r[:, int(0.7 * r.shape[1]):, :]
            sweep[gate].append((tail[:, :, 1].mean(), tail[:, :, 2].mean()))
    nd = data["no defense"]
    k = int(np.searchsorted(nd[0, :, 0], 2000)) + 1
    curve = (nd[0, :k, 0], nd[:, :k, 1].mean(axis=0), nd[:, :k, 2].mean(axis=0))
    for t in THEME:
        (ROOT / "assets" / f"misevolution-loop-{t}.svg").write_text(loop_svg(t, curve), encoding="utf-8", newline="\n")
        for spec in TRENDS:
            (ROOT / "assets" / f"trend-{spec[0]}-{t}.svg").write_text(card_svg(t, spec), encoding="utf-8", newline="\n")
        growth(t, last_pass)
        timeseries(t, data)
        pareto(t, sweep)
    print("wrote misevolution-loop, trend cards, growth, sim-timeseries, sim-pareto (light and dark)")


if __name__ == "__main__":
    main()
