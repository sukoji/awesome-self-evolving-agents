#!/usr/bin/env python3
"""Render paper entries in README.md as tables.

Contributors keep writing the plain format from CONTRIBUTING.md:

    - **Title** — Venue. [arXiv:ID](url) · [code](github url). One sentence.

This script turns every run of such lines, together with any table rows next to
them, into one two-column table:

    | **Title**<br><sub>Venue</sub> [![arXiv](badge)](url) [![code](badge)](github url) | One sentence. |

Rows already in that form are kept as they are, so it can run on every pass.
``--new ID,ID,...`` tags those entries with a "new" badge and removes the tag
from every other entry.

Run from the repository root:  python .github/scripts/format_entries.py [--new IDS]
"""

import argparse
import re
from pathlib import Path

README = Path(__file__).resolve().parents[2] / "README.md"
S = "style=flat-square"
BADGE = {
    "arxiv": f"https://img.shields.io/badge/arXiv-b31b1b?{S}&logo=arxiv&logoColor=white",
    "paper": f"https://img.shields.io/badge/paper-59636e?{S}",
    "code": f"https://img.shields.io/badge/code-1f2328?{S}&logo=github&logoColor=white",
    "new": f"https://img.shields.io/badge/new-1a7f64?{S}",
}
# The run of no-break spaces sets the Paper column's minimum width, so titles
# wrap onto two lines instead of four; GitHub strips column-width attributes.
HEADER = ["| Paper" + "&nbsp;" * 50 + " | What it does |", "|:---|:---|"]
HEAD = re.compile(r"^\| Paper(?:&nbsp;)* \| What it does \|$|^\|:---\|:---\|$")
PLAIN = re.compile(
    r"^- \*\*(?P<title>[^*]+)\*\* — (?P<venue>.+?)\. "
    r"\[(?P<label>[^\]]+)\]\((?P<url>https?://[^\s)]+)\)"
    r"(?: · \[code\]\((?P<code>https://github\.com/[^\s)]+)\))?\."
    r"(?: (?P<desc>.+))?$")
ROW = re.compile(r"^\| \*\*[^*]+\*\*<br><sub>.*\|$")
NEW_TAG = f" [![new]({BADGE['new']})](#updates)"


def row(m):
    kind = "arxiv" if "arxiv.org/abs/" in m["url"] else "paper"
    links = f"[![{'arXiv' if kind == 'arxiv' else 'paper'}]({BADGE[kind]})]({m['url']})"
    if m["code"]:
        links += f" [![code]({BADGE['code']})]({m['code']})"
    desc = (m["desc"] or "").replace("|", "\\|")
    return f"| **{m['title']}**<br><sub>{m['venue']}</sub> {links} | {desc} |"


def in_table(line):
    return bool(PLAIN.match(line) or ROW.match(line) or HEAD.match(line))


def tag(line, new):
    line = line.replace(NEW_TAG, "")
    aid = re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", line)
    if aid and aid.group(1) in new:
        head, rest = line.split(" | ", 1)
        line = f"{head}{NEW_TAG} | {rest}"
    return line


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", default=None, help="comma-separated arXiv ids to tag as new")
    new = ap.parse_args().new
    new = set(new.split(",")) if new else None
    lines = README.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    end = next(i for i, l in enumerate(lines) if l.startswith("## Updates"))
    out, i, converted = [], 0, 0
    while i < len(lines):
        if i < end and in_table(lines[i]):
            rows = []
            while i < end and in_table(lines[i]):
                m = PLAIN.match(lines[i])
                if m:
                    rows.append(row(m))
                    converted += 1
                elif ROW.match(lines[i]):
                    rows.append(lines[i])
                i += 1
            if new is not None:
                rows = [tag(r, new) for r in rows]
            out += HEADER + rows
            continue
        out.append(lines[i])
        i += 1
    README.write_text("\n".join(out), encoding="utf-8", newline="\n")
    print("converted %d plain entries" % converted)


if __name__ == "__main__":
    main()
