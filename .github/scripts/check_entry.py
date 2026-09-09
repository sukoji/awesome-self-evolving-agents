#!/usr/bin/env python3
"""Decide whether a pull request is a routine list addition.

A pull request qualifies when it does nothing but add entries to the list:
Markdown files only, additions only, a handful of lines, each one shaped like
an entry, each link live, and nothing already in the list. Anything else — a
reworded section, a new workflow, a code change — is a human's call and this
script says so.

Reads a unified diff on stdin (``gh pr diff --patch``) and takes the base
checkout as its second source of truth for duplicate detection. It never
executes anything from the pull request.
"""

import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ALLOWED_FILES = {"README.md", "COMMUNITY.md"}
MAX_ADDED_LINES = 3
MAX_REASONS = 8   # a comment listing every line of a large diff helps nobody

# - **Title** — Venue'Year. [label](url). One sentence.
ENTRY = re.compile(
    r"^- \*\*[^*]{4,200}\*\* — [^.]{2,60}\. "
    r"\[[^\]]{4,120}\]\((https?://[^\s)]+)\)\. "
    r"[A-Z][^\n]{15,400}$")
# | [**name**](url) | author | pathway | focus |
ROW = re.compile(
    r"^\| \[\*\*[^*]{2,80}\*\*\]\((https?://[^\s)]+)\) \| [^|]{1,60}"
    r"\| [^|]{1,40}\| [^|]{10,200}\|$")
UA = {"User-Agent": "awesome-self-evolving-agents entry guard"}


def fail(message):
    print("BLOCK " + message)


def report(problems):
    for problem in problems[:MAX_REASONS]:
        fail(problem)
    if len(problems) > MAX_REASONS:
        fail("and %d further reason(s), not listed"
             % (len(problems) - MAX_REASONS))
    print("%d reason(s) this needs a human" % len(problems))
    return 1


def parse(diff):
    """-> (files touched, [(file, added line)]), removed line count"""
    files, added, removed, current = set(), [], 0, None
    for line in diff.split("\n"):
        if line.startswith("+++ b/"):
            current = line[6:].strip()
            files.add(current)
        elif line.startswith("--- a/"):
            files.add(line[6:].strip())
        elif line.startswith("+") and not line.startswith("+++"):
            added.append((current, line[1:]))
        elif line.startswith("-") and not line.startswith("---"):
            if line[1:].strip():
                removed += 1
    return files, added, removed


def link_ok(url):
    try:
        return urllib.request.urlopen(
            urllib.request.Request(url, headers=UA), timeout=25).getcode() < 400
    except urllib.error.HTTPError as exc:
        return exc.code in (403, 429)   # bot-blocked or throttled, not broken
    except (urllib.error.URLError, OSError):
        return False


def main():
    diff = sys.stdin.read()
    if not diff.strip():
        fail("empty diff")
        return 1

    files, added, removed = parse(diff)
    problems = []

    outside = sorted(f for f in files if f not in ALLOWED_FILES)
    if outside:
        # Once the diff reaches outside the list, checking its lines one by one
        # says nothing useful — this is a human's pull request either way.
        return report(["touches %s; only %s may be auto-merged"
                       % (", ".join(outside), " and ".join(sorted(ALLOWED_FILES)))])
    if removed:
        problems.append("removes or rewrites %d line(s); additions only" % removed)

    body = [(f, l) for f, l in added if l.strip()]
    if not body:
        problems.append("adds nothing")
    elif len(body) > MAX_ADDED_LINES:
        problems.append("adds %d lines; the limit for an automatic merge is %d"
                        % (len(body), MAX_ADDED_LINES))

    root = Path(__file__).resolve().parents[2]
    existing = "".join((root / name).read_text(encoding="utf-8")
                       for name in ALLOWED_FILES if (root / name).exists())

    for name, line in body:
        stripped = line.strip()
        match = ENTRY.match(stripped) or ROW.match(stripped)
        if not match:
            problems.append("line does not match the entry format: %.90s" % stripped)
            continue
        url = match.group(1)
        if not link_ok(url):
            problems.append("link does not resolve: %s" % url)
        title = stripped.split("**")[1]
        if title in existing:
            problems.append("%r is already in the list" % title)

    if problems:
        return report(problems)
    print("OK routine list addition: %d line(s), links live, no duplicates"
          % len(body))
    return 0


if __name__ == "__main__":
    sys.exit(main())
