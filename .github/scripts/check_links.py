#!/usr/bin/env python3
"""Enforce the list's own link policy.

Two checks, both against live sources:

1. Every ``arxiv.org/abs/<id>`` link resolves through the arXiv API, and the
   returned title is recognisably the entry's own title. Entries listed under a
   short project name (``APE``, ``StuLife``) are matched by containment instead
   of similarity, so a short name inside a long official title still passes.
2. Every other http(s) link answers without a client or server error.

Exits non-zero and prints one line per problem.
"""

import argparse
import difflib
import html
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

FILES = ["README.md", "COMMUNITY.md", "CONTRIBUTING.md", "docs/primer.md",
         "docs/contributing-guide.md", "code/README.md"]
ARXIV_API = "https://export.arxiv.org/api/query?id_list=%s&max_results=%d"
UA = {"User-Agent": "awesome-self-evolving-agents link check"}
BATCH = 40
SIMILARITY = 0.55

# Entries deliberately listed under a short project or benchmark name rather
# than the paper's full title. The link is still checked; only the title
# comparison is waived.
SHORT_NAMES = {
    "2211.01910": "Automatic Prompt Engineer (APE)",
    "2508.19005": "StuLife",
    "2511.20857": "Evo-Memory",
    "2604.17308": "SkillFlow",
    "2505.11942": "LifelongAgentBench",
}

# Placeholder URLs that appear inside documentation examples.
PLACEHOLDERS = ("github.com/org/repo", "OWNER/REPO")


def normalise(text):
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()


def get(url, timeout=40):
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=timeout)


def skippable(url):
    """Links a bot cannot meaningfully verify, or that verify nothing."""
    if "img.shields.io" in url or "arxiv.org" in url:
        return True   # badge images; arXiv is checked through the API instead
    if any(token in url for token in PLACEHOLDERS):
        return True   # documentation examples, not real destinations
    if re.match(r"https?://github\.com/[^/]+/[^/]+/"
                r"(stargazers|forks|watchers|commits|graphs|issues/new|network)", url):
        return True   # navigation sub-pages of a repo, rate-limited for bots
    if url.startswith("https://doi.org/"):
        return True   # publishers routinely answer 403 to unauthenticated requests
    return False


def collect(root):
    """-> {arxiv_id: [entry titles]}, [(source file, url)]"""
    papers, urls = {}, []
    for name in FILES:
        path = root / name
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").split("\n"):
            for url in re.findall(r"https?://[^\s)\"'<>\]]+", line):
                url = url.rstrip(".,;")
                match = re.search(r"arxiv\.org/abs/(\d{4}\.\d{4,5})", url)
                if match:
                    title = line.split("**")[1] if line.count("**") >= 2 else line[:60]
                    papers.setdefault(match.group(1), []).append(title)
                elif skippable(url):
                    continue
                else:
                    urls.append((name, url))
    return papers, urls


def check_arxiv(papers):
    problems = []
    ids = sorted(papers)
    for start in range(0, len(ids), BATCH):
        chunk = ids[start:start + BATCH]
        try:
            body = get(ARXIV_API % (",".join(chunk), BATCH)).read().decode()
        except (urllib.error.URLError, OSError) as exc:
            problems.append("arXiv API unreachable for %s: %s" % (chunk[0], exc))
            continue
        found = {}
        for entry in re.findall(r"<entry>(.*?)</entry>", body, re.S):
            match = re.search(r"abs/(\d{4}\.\d{4,5})", entry)
            title = re.search(r"<title>(.*?)</title>", entry, re.S)
            if match and title:
                found[match.group(1)] = html.unescape(
                    re.sub(r"\s+", " ", title.group(1))).strip()
        for arxiv_id in chunk:
            if arxiv_id not in found:
                problems.append("arXiv:%s does not resolve (listed as %r)"
                                % (arxiv_id, papers[arxiv_id][0]))
                continue
            official = normalise(found[arxiv_id])
            if arxiv_id in SHORT_NAMES:
                continue
            for listed in papers[arxiv_id]:
                ours = normalise(listed)
                if ours in official or official in ours:
                    continue
                ratio = difflib.SequenceMatcher(None, ours, official).ratio()
                if ratio < SIMILARITY:
                    problems.append(
                        "arXiv:%s title mismatch (%.2f): listed %r, arXiv says %r"
                        % (arxiv_id, ratio, listed, found[arxiv_id]))
        time.sleep(3.2)  # arXiv asks for one request every three seconds
    return problems


def check_urls(urls):
    problems, seen = [], set()
    for source, url in urls:
        if url in seen:
            continue
        seen.add(url)
        try:
            code = get(url, timeout=25).getcode()
        except urllib.error.HTTPError as exc:
            code = exc.code
        except (urllib.error.URLError, OSError) as exc:
            problems.append("%s: %s unreachable (%s)" % (source, url, exc))
            continue
        if code == 429:
            continue   # rate limited, not broken
        if code >= 400:
            problems.append("%s: %s returned HTTP %d" % (source, url, code))
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[2],
        help="directory holding the Markdown to check (default: this checkout). "
             "Lets a workflow run this trusted copy of the script against a "
             "pull request's files without executing the pull request's own.")
    root = parser.parse_args().root
    papers, urls = collect(root)
    print("checking %d arXiv identifiers and %d other links"
          % (len(papers), len({u for _, u in urls})))
    problems = check_arxiv(papers) + check_urls(urls)
    for problem in problems:
        print("FAIL " + problem)
    print("%d problem(s)" % len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
