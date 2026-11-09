#!/usr/bin/env python3
"""Render paper entries in README.md as tables.

Contributors keep writing the plain format from CONTRIBUTING.md:

    - **Title** — Venue. [arXiv:ID](url) · [code](github url). One sentence.

This script turns every run of such lines into an HTML table with one row per
paper — title on top, then a row of badges (venue, arXiv, code), the
description beside it — and folds plain lines placed after an existing table
into that table. HTML rather than Markdown because only HTML lets the Paper
column keep a fixed share of the width and both cells align to the top.

Rows already rendered are kept as they are, so it can run on every pass.
``--new ID,ID,...`` tags those entries with a "new" badge and removes the tag
from every other entry.

Run from the repository root:  python .github/scripts/format_entries.py [--new IDS]
"""

import argparse
import html
import re
from pathlib import Path
from urllib.parse import quote

README = Path(__file__).resolve().parents[2] / "README.md"
S = "style=flat-square"
BADGE = {
    "arxiv": f"https://img.shields.io/badge/arXiv-b31b1b?{S}&logo=arxiv&logoColor=white",
    "paper": f"https://img.shields.io/badge/paper-59636e?{S}",
    "code": f"https://img.shields.io/badge/code-1f2328?{S}&logo=github&logoColor=white",
    "new": f"https://img.shields.io/badge/new-1a7f64?{S}",
}
OPEN, CLOSE = "<table>", "</table>"
HEAD = '<tr><th width="38%" align="left">Paper</th><th align="left">What it does</th></tr>'
PLAIN = re.compile(
    r"^- \*\*(?P<title>[^*]+)\*\* — (?P<venue>.+?)\. "
    r"\[(?P<label>[^\]]+)\]\((?P<url>https?://[^\s)]+)\)"
    r"(?: · \[code\]\((?P<code>https://github\.com/[^\s)]+)\))?\."
    r"(?: (?P<desc>.+))?$")
ROW = re.compile(r'^<tr><td valign="top"><b>.*</td></tr>$')
NEW_TAG = f' <a href="#updates"><img src="{BADGE["new"]}" alt="new"></a>'


def inline(text):
    """The Markdown that occurs in titles and descriptions, as HTML."""
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<i>\1</i>", text)
    return text


def venue_badge(venue):
    """Grey for a preprint year, blue for a named venue."""
    color = "59636e" if venue[:1].isdigit() else "2a78d6"
    text = quote(venue.replace("-", "--").replace("_", "__"), safe="")
    return f'<img src="https://img.shields.io/badge/{text}-{color}?{S}" alt="{html.escape(venue)}">'


def row(m):
    kind = "arxiv" if "arxiv.org/abs/" in m["url"] else "paper"
    alt = "arXiv" if kind == "arxiv" else "paper"
    badges = [venue_badge(m["venue"]), f'<a href="{m["url"]}"><img src="{BADGE[kind]}" alt="{alt}"></a>']
    if m["code"]:
        badges.append(f'<a href="{m["code"]}"><img src="{BADGE["code"]}" alt="code"></a>')
    return (f'<tr><td valign="top"><b>{inline(m["title"])}</b><br>{" ".join(badges)}</td>'
            f'<td valign="top">{inline(m["desc"] or "")}</td></tr>')


def tag(line, new):
    line = line.replace(NEW_TAG, "")
    aid = re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", line)
    if aid and aid.group(1) in new:
        head, rest = line.split("</td>", 1)
        line = f"{head}{NEW_TAG}</td>{rest}"
    return line


def part(line):
    return bool(PLAIN.match(line) or ROW.match(line) or line in (OPEN, CLOSE, HEAD))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--new", default=None, help="comma-separated arXiv ids to tag as new")
    new = ap.parse_args().new
    new = set(new.split(",")) if new else None
    lines = README.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    end = next(i for i, l in enumerate(lines) if l.startswith("## Updates"))
    out, i, converted = [], 0, 0
    while i < len(lines):
        if not (i < end and part(lines[i])):
            out.append(lines[i])
            i += 1
            continue
        rows = []
        while i < end:
            if part(lines[i]):
                m = PLAIN.match(lines[i])
                if m:
                    rows.append(row(m))
                    converted += 1
                elif ROW.match(lines[i]):
                    rows.append(lines[i])
                i += 1
                continue
            # plain entries a contributor added after the table, past a blank line
            j = i
            while j < end and not lines[j].strip():
                j += 1
            if j < end and PLAIN.match(lines[j]):
                i = j
                continue
            break
        if new is not None:
            rows = [tag(r, new) for r in rows]
        out += [OPEN, HEAD] + rows + [CLOSE]
    README.write_text("\n".join(out), encoding="utf-8", newline="\n")
    print("converted %d plain entries" % converted)


if __name__ == "__main__":
    main()
