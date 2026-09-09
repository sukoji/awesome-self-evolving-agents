# Security policy

This repository is a curated reading list. It ships no runtime dependencies and
nothing here is meant to be deployed. Two things are still worth reporting.

## The automation

`.github/workflows/` runs on every pull request, and `entry-guard.yml` holds a
write token. If you find a way to make it merge something a maintainer did not
intend — a diff shape that slips past `.github/scripts/check_entry.py`, a path
that reaches the write-token job with code from a fork, a way to make the guard
comment or merge on a pull request it should have left alone — please report it
privately rather than opening a demonstration pull request.

**How:** use [private vulnerability reporting](https://github.com/sukoji/awesome-self-evolving-agents/security/advisories/new).
Expect an acknowledgement within a week.

## The links

Every link in the list is machine-checked for *resolvability*, not for what is
on the other side. If a linked repository, dataset, or page has been taken over
or now serves something harmful, that is worth reporting the same way — or, if
it is not sensitive, as a
[correction issue](https://github.com/sukoji/awesome-self-evolving-agents/issues/new?template=correction.yml).

## Out of scope

- The two demos under `code/`. They are deterministic, dependency-light, and
  meant to be read; they are not a library and take no untrusted input.
- Findings from automated scanners with no described impact on this repository.
