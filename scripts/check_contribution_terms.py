#!/usr/bin/env python3
"""Verify provenance and CLA acceptance trailers for a Git revision range."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys


SIGNOFF_RE = re.compile(r"(?mi)^Signed-off-by:\s+.+\s+<[^<>\s]+@[^<>\s]+>\s*$")
CLA_RE = re.compile(r"(?mi)^Flyto2-CLA:\s+accepted\s*$")


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", required=True, help="exclusive base revision")
    parser.add_argument("--head", default="HEAD", help="inclusive head revision")
    args = parser.parse_args()

    commits = _git("rev-list", "--reverse", f"{args.base}..{args.head}").splitlines()
    failures = []
    for commit in commits:
        message = _git("show", "-s", "--format=%B", commit)
        missing = []
        if not SIGNOFF_RE.search(message):
            missing.append("Signed-off-by")
        if not CLA_RE.search(message):
            missing.append("Flyto2-CLA: accepted")
        if missing:
            subject = _git("show", "-s", "--format=%s", commit)
            failures.append(f"{commit[:12]} {subject}: {', '.join(missing)}")

    if failures:
        print("contribution terms check failed:", file=sys.stderr)
        for failure in failures:
            print(f"  {failure}", file=sys.stderr)
        return 1

    print(f"contribution terms passed for {len(commits)} commit(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
