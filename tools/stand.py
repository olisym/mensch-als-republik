#!/usr/bin/env python3
"""Kaltzahlen einer Sitzung als eine Zeile, Kopftext der Projektkopie (D224, D316, D318)."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTER = ROOT / "07-decisions.md"
RULES = ROOT / "pruefregeln.md"
OFFEN = ROOT / "offen.md"

PASSED = re.compile(r"(\d+) passed")
RULE_HEAD = re.compile(r"^\*\*[0-9]+\.")


def test_count(text: str) -> int | None:
    """Die Zahl unmittelbar vor dem Wort ``passed``, oder None."""
    matches = PASSED.findall(text)
    if not matches:
        return None
    return int(matches[-1])


def commit_hash() -> str | None:
    """Kurzhash von HEAD, oder None wenn git fehlschlägt."""
    try:
        out = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    if out.returncode != 0:
        return None
    hash_ = out.stdout.strip()
    if not hash_:
        return None
    return hash_


def branch_count() -> int | None:
    """Zahl der Zeilen von ``git branch -a``, oder None wenn git fehlschlägt."""
    try:
        out = subprocess.run(
            ["git", "branch", "-a"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return None
    if out.returncode != 0:
        return None
    return len(out.stdout.splitlines())


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        return 1
    path = Path(argv[1])
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return 1
    tests = test_count(text)
    if tests is None:
        return 1
    hash_ = commit_hash()
    if hash_ is None:
        return 1
    branches = branch_count()
    if branches is None:
        return 1
    register = sum(
        1 for line in REGISTER.read_text(encoding="utf-8").splitlines() if line.startswith("### D")
    )
    rules = sum(
        1 for line in RULES.read_text(encoding="utf-8").splitlines() if RULE_HEAD.match(line)
    )
    posts = sum(
        1 for line in OFFEN.read_text(encoding="utf-8").splitlines() if line.startswith("### O")
    )
    print(
        f"{hash_} {tests} Tests, {register} Registerköpfe, "
        f"{rules} Prüfregeln, {posts} Posten, {branches} Branches"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
