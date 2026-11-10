#!/usr/bin/env python3
"""Figures for the README, drawn plainly, like figures in a paper: no titles
inside the image (the README caption carries them), sans-serif text, boxes and
arrows for diagrams, axes and legends for charts. Each is written twice, for
GitHub's light and dark themes, as assets/<name>-light.svg and -dark.svg.

- misevolution-loop  the primer: (a) the feedback loop, (b) the curves the
                     simulation produces, (c) papers that saw the loop in real agents
- growth             papers in this list per arXiv quarter (read from README.md)
- sim-timeseries     safety and utility over time, median and 10-90% band over seeds
- sim-pareto         the utility-safety frontier, points labelled by re-anchor strength

The last two and the primer's curves come from code/safety_gated_evolution.py.
Needs numpy and matplotlib. Run from the repository root:
    python .github/scripts/build_figures.py
"""

import html
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
SANS = "Helvetica,Arial,sans-serif"
THEME = {
    "light": dict(bg="#ffffff", ink="#1f2328", sub="#59636e", faint="#d8dee4", line="#57606a",
                  box="#f6f8fa", blue="#2a78d6", blue_bg="#ddeafb", warm="#bf8700", warm_bg="#fbefc9",
                  bad="#cf222e", bad_bg="#ffe3e1", series=["#cf222e", "#bf8700", "#1a7f64", "#2a78d6"],
                  bars="#6da7ec"),
    "dark": dict(bg="#0d1117", ink="#e6edf3", sub="#9198a1", faint="#30363d", line="#8b949e",
                 box="#161b22", blue="#3987e5", blue_bg="#122540", warm="#d29922", warm_bg="#2e2410",
                 bad="#ff7b72", bad_bg="#3a1618", series=["#ff7b72", "#d29922", "#2fbf88", "#3987e5"],
                 bars="#3987e5"),
}
CONDITIONS = [  # label, reg, write_gate, line style
    ("no defense", 0.0, 0.0, "-"),
    ("write-gate", 0.0, 0.8, (0, (4, 3))),
    ("re-anchor", 0.06, 0.0, "-"),
    ("both", 0.06, 0.8, "-"),
]
REGS = [0.30, 0.20, 0.14, 0.10, 0.075, 0.055, 0.04, 0.028, 0.018, 0.010]


def text(x, y, s, size, fill, weight=None, anchor=None):
    a = [f'x="{x:.1f}"', f'y="{y:.1f}"', f'font-size="{size}"', f'fill="{fill}"']
    if weight:
        a.append(f'font-weight="{weight}"')
    if anchor:
        a.append(f'text-anchor="{anchor}"')
    return f'<text {" ".join(a)}>{html.escape(s)}</text>\n'


def box(x, y, w, h, lines, fill, stroke, ink):
    o = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>\n']
    y0 = y + h / 2 - (len(lines) - 1) * 8 + 5
    for i, s in enumerate(lines):
        o.append(text(x + w / 2, y0 + i * 16, s, 13.5, ink, anchor="middle"))
    return "".join(o)


def arrow(x1, y1, x2, y2, color, mark):
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="1.6" marker-end="url(#{mark})"/>\n'


# --- the primer: three panels, as in a paper figure ---

def loop_svg(t, curve):
    c = THEME[t]
    W, H = 1040, 345
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="(a) The misevolution loop: the agent approves a refund, the customer rates it five stars, the agent learns that approving is good, its approval bias rises, and the loop repeats until bad requests are approved too. (b) In a simulation with no defense, utility stays near 1 while safety falls to 0 within about 500 interactions. (c) Three 2025-26 papers observed the loop in real agents.">\n',
         f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>\n<g font-family="{SANS}">\n']
    for name, col in (("ar", c["line"]), ("br", c["bad"])):
        o.append(f'<defs><marker id="{name}-{t}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" '
                 f'orient="auto-start-reverse"><path d="M1 1L9 5L1 9z" fill="{col}"/></marker></defs>\n')
    ar, br = f"ar-{t}", f"br-{t}"

    # (a) the loop, four boxes in a cycle and the way out
    bw, bh = 150, 52
    A, B, C, D = (30, 30), (220, 30), (220, 150), (30, 150)
    o.append(box(*A, bw, bh, ["Agent approves", "a refund"], c["blue_bg"], c["blue"], c["ink"]))
    o.append(box(*B, bw, bh, ["Customer rates", "it 5 stars"], c["blue_bg"], c["blue"], c["ink"]))
    o.append(box(*C, bw, bh, ["Agent learns", "“approving is good”"], c["warm_bg"], c["warm"], c["ink"]))
    o.append(box(*D, bw, bh, ["Approval bias", "rises"], c["warm_bg"], c["warm"], c["ink"]))
    o.append(arrow(A[0] + bw + 2, A[1] + bh / 2, B[0] - 4, B[1] + bh / 2, c["line"], ar))
    o.append(arrow(B[0] + bw / 2, B[1] + bh + 2, C[0] + bw / 2, C[1] - 4, c["line"], ar))
    o.append(arrow(C[0] - 2, C[1] + bh / 2, D[0] + bw + 4, D[1] + bh / 2, c["line"], ar))
    o.append(arrow(D[0] + bw / 2, D[1] - 2, A[0] + bw / 2, A[1] + bh + 4, c["line"], ar))
    o.append(text(D[0] + bw / 2 + 8, (A[1] + bh + D[1]) / 2 + 4, "repeat", 12, c["sub"]))
    E = (30, 250)
    o.append(arrow(D[0] + bw / 2, D[1] + bh + 2, E[0] + bw / 2, E[1] - 4, c["bad"], br))
    o.append(box(*E, bw, bh, ["Bad requests", "approved too"], c["bad_bg"], c["bad"], c["ink"]))

    # (b) the simulated curves, with axes and a legend
    X0, Y0, PW, PH = 470, 40, 230, 220
    o.append(f'<path d="M{X0} {Y0} V{Y0+PH} H{X0+PW}" fill="none" stroke="{c["line"]}" stroke-width="1"/>\n')
    for v in (0, 0.5, 1.0):
        y = Y0 + PH - v * PH * 0.92
        o.append(f'<path d="M{X0-4} {y:.1f} H{X0}" stroke="{c["line"]}"/>\n')
        o.append(text(X0 - 8, y + 4, f"{v:g}", 11.5, c["sub"], anchor="end"))
    steps, util, safe = curve
    xmax = steps[-1]
    for v in (0, 1000, 2000):
        x = X0 + v / xmax * PW
        o.append(f'<path d="M{x:.1f} {Y0+PH} V{Y0+PH+4}" stroke="{c["line"]}"/>\n')
        o.append(text(x, Y0 + PH + 18, f"{v:,}", 11.5, c["sub"], anchor="middle"))
    o.append(text(X0 + PW / 2, Y0 + PH + 36, "interactions", 12, c["sub"], anchor="middle"))
    o.append(f'<text x="{X0-34}" y="{Y0+PH/2}" font-size="12" fill="{c["sub"]}" text-anchor="middle" '
             f'transform="rotate(-90 {X0-34} {Y0+PH/2})">rate</text>\n')

    def path(vals):
        return " ".join(f"{'M' if i == 0 else 'L'}{X0 + s / xmax * PW:.1f} {Y0 + PH - v * PH * 0.92:.1f}"
                        for i, (s, v) in enumerate(zip(steps, vals)))
    o.append(f'<path d="{path(util)}" fill="none" stroke="{c["blue"]}" stroke-width="2.2"/>\n')
    o.append(f'<path d="{path(safe)}" fill="none" stroke="{c["bad"]}" stroke-width="2.2"/>\n')
    lx, ly = X0 + 70, Y0 + PH * 0.42
    o.append(f'<rect x="{lx-10}" y="{ly-16}" width="160" height="48" fill="{c["bg"]}" stroke="{c["faint"]}"/>\n')
    for k, (col, s) in enumerate(((c["blue"], "utility"), (c["bad"], "safety"))):
        y = ly + k * 20
        o.append(f'<path d="M{lx} {y-4} H{lx+22}" stroke="{col}" stroke-width="2.2"/>\n')
        o.append(text(lx + 30, y, s, 12, c["ink"]))

    # (c) the same loop in real agents
    X2 = 770
    seen = [(["Your Agent May Misevolve"], ["Refusal rates drop", "after self-training"]),
            (["Appreciation Teaches", "Unauthorized Execution"], ["Learning from user feedback", "raises hidden-injection success"]),
            (["Masked Erosion"], ["Redundant safeguards erode,", "unseen by the acceptance gate"])]
    y = 34
    for head, body in seen:
        h = 14 + 17 * (len(head) + len(body))
        o.append(f'<rect x="{X2}" y="{y}" width="245" height="{h}" rx="6" fill="{c["box"]}" stroke="{c["faint"]}" stroke-width="1.5"/>\n')
        yy = y + 22
        for s in head:
            o.append(text(X2 + 12, yy, s, 13, c["ink"], weight="700"))
            yy += 17
        for s in body:
            o.append(text(X2 + 12, yy, s, 12.5, c["sub"]))
            yy += 17
        y += h + 10

    # panel captions
    for x, s in ((180, "(a) The feedback loop"), (X0 + PW / 2, "(b) Simulated agent, no defense"), (X2 + 122, "(c) Observed in real agents")):
        o.append(text(x, H - 14, s, 13.5, c["ink"], anchor="middle"))
    o.append("</g>\n</svg>\n")
    return "".join(o)


# --- matplotlib charts ---

def style(t):
    c = THEME[t]
    plt.rcParams.update({
        "svg.fonttype": "none", "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"], "font.size": 11,
        "figure.facecolor": c["bg"], "axes.facecolor": c["bg"], "savefig.facecolor": c["bg"],
        "axes.edgecolor": c["line"], "axes.labelcolor": c["ink"], "xtick.color": c["sub"],
        "ytick.color": c["sub"], "text.color": c["ink"], "grid.color": c["faint"], "grid.linewidth": 0.7,
        "axes.spines.top": False, "axes.spines.right": False,
        "legend.edgecolor": c["faint"], "legend.facecolor": c["bg"], "legend.framealpha": 1,
    })
    return c


def save(fig, name, t):
    fig.savefig(ROOT / "assets" / f"{name}-{t}.svg", metadata={"Date": None}, bbox_inches="tight", pad_inches=0.15)
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


def growth(t):
    c = style(t)
    keys, n = quarters()
    fig, ax = plt.subplots(figsize=(9.6, 3.2))
    bars = ax.bar(range(len(keys)), n, color=c["bars"], width=0.72)
    bars[-1].set_hatch("////")
    bars[-1].set_facecolor(c["bg"])
    bars[-1].set_edgecolor(c["bars"])
    for i, v in enumerate(n):
        if v:
            ax.text(i, v + max(n) * 0.015, str(v), ha="center", va="bottom", fontsize=9, color=c["sub"])
    starts = [i for i, (_, q) in enumerate(keys) if q == 1]
    ax.set_xticks([i - 0.5 for i in starts])
    ax.set_xticklabels([str(keys[i][0]) for i in starts], ha="left")
    ax.set_xlim(-0.6, len(keys) - 0.4)
    ax.set_ylabel("papers per quarter")
    ax.grid(axis="y")
    ax.set_axisbelow(True)
    ax.legend([bars[0], bars[-1]], ["arXiv quarter", "quarter in progress"], loc="upper left", fontsize=9.5)
    save(fig, "growth", t)


def timeseries(t, data):
    c = style(t)
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.9))
    for ax, col, ylabel, tag in ((axes[0], 2, "safety (bad requests refused)", "(a)"),
                                 (axes[1], 1, "utility (good requests approved)", "(b)")):
        for (label, reg, gate, ls), color in zip(CONDITIONS, c["series"]):
            r = data[label]
            x = r[0, :, 0]
            lo, mid, hi = np.percentile(r[:, :, col], [10, 50, 90], axis=0)
            ax.fill_between(x, lo, hi, color=color, alpha=0.15, linewidth=0)
            ax.plot(x, mid, color=color, linestyle=ls, linewidth=1.8, label=label)
        ax.set_ylim(-0.03, 1.05)
        ax.set_xlabel("interactions")
        ax.set_ylabel(ylabel)
        ax.grid(alpha=0.8)
        ax.set_title(tag, loc="left", fontsize=11.5)
    axes[0].legend(loc="upper right", fontsize=9.5)
    fig.tight_layout(w_pad=3)
    save(fig, "sim-timeseries", t)


def pareto(t, sweep):
    c = style(t)
    fig, ax = plt.subplots(figsize=(6.4, 4.6))
    for (label, gate, marker), color in zip([("re-anchor only", 0.0, "o"), ("re-anchor + write-gate", 0.8, "s")],
                                            (c["series"][2], c["series"][1])):
        u, s = zip(*sweep[gate])
        ax.plot(u, s, marker=marker, color=color, linewidth=1.5, markersize=5, label=label)
        if gate == 0.0:
            for reg, x, y in zip(REGS, u, s):
                if reg in (0.30, 0.10, 0.04):
                    ax.annotate(f"reg = {reg:g}", (x, y), xytext=(8, 6), textcoords="offset points", fontsize=9, color=c["sub"])
    ax.scatter([1.0], [0.0], marker="x", s=60, color=c["series"][0], zorder=5, label="no defense")
    ax.set_xlabel("utility (good requests approved)")
    ax.set_ylabel("safety (bad requests refused)")
    ax.grid(alpha=0.8)
    ax.legend(loc="upper right", fontsize=9.5)
    save(fig, "sim-pareto", t)


def runs(reg, gate):
    out = []
    for s in SEEDS:
        agent = sim.Agent(random.Random(s), reg=reg, write_gate=gate)
        out.append(np.array(sim.rollout(agent, seed=s)))  # columns: step, utility, safety, bias
    return np.stack(out)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
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
        growth(t)
        timeseries(t, data)
        pareto(t, sweep)
    print("wrote misevolution-loop, growth, sim-timeseries, sim-pareto (light and dark)")


if __name__ == "__main__":
    main()
