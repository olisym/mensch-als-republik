#!/usr/bin/env python3
"""Registerindex: welche Entscheidungen einen Abschnitt nennen (D209, Prüfregel 38)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTER = ROOT / "07-decisions.md"

ENTRY = re.compile(r"^### (D\d+[a-z]?)", re.M)
REF = re.compile(
    r"(?<![A-Za-z0-9])(\d+[a-z]*|VISION) §(\d+(?:\.\d+)*|[A-Z]\.\d+(?:\.\d+)*)"
)


def entries(text: str) -> list[tuple[str, str]]:
    """Zerlegt das Register an Zeilen ``### D<zahl>`` (D209)."""
    matches = list(ENTRY.finditer(text))
    result: list[tuple[str, str]] = []
    for i, match in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        result.append((match.group(1), text[match.start() : end]))
    return result


def refs_in(body: str) -> list[str]:
    """Verweise ``<praefix> §<abschnitt>``, je Eintrag einmal, in Registerreihenfolge."""
    seen: set[str] = set()
    ordered: list[str] = []
    for prefix, section in REF.findall(body):
        key = f"{prefix} §{section}"
        if key not in seen:
            seen.add(key)
            ordered.append(key)
    return ordered


def build_index(text: str) -> dict[str, list[str]]:
    """Abschnitt → D-Nummern in Registerreihenfolge (D209)."""
    index: dict[str, list[str]] = {}
    for did, body in entries(text):
        for ref in refs_in(body):
            index.setdefault(ref, []).append(did)
    return index


def emit_query(query: str, index: dict[str, list[str]]) -> None:
    ids = index.get(query, [])
    print(f"{query}   {' '.join(ids)}")


def emit_overview(index: dict[str, list[str]]) -> None:
    rows = sorted(index.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    for section, ids in rows:
        print(f"{section}   {len(ids)}")


def main(argv: list[str]) -> int:
    text = REGISTER.read_text(encoding="utf-8")
    index = build_index(text)
    if len(argv) > 1:
        emit_query(argv[1], index)
    else:
        emit_overview(index)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
