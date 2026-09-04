#!/usr/bin/env python3
"""Prüft die nummerierten Posten in offen.md (D316, D209, D229).

Sichert, dass eine genannte Nummer existiert, nicht dass der Posten die
Nennung trägt. Dieselbe Grenze wie bei den Abschnittsverweisen (D229).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OFFEN = ROOT / "offen.md"
REGISTER = ROOT / "07-decisions.md"

HEADING = re.compile(r"^### O(\d+)", re.M)
MENTION = re.compile(r"O(\d+)")


def post_numbers(text: str) -> list[int]:
    """Kopfzeilen ``### O`` plus Ziffernfolge, in Dateireihenfolge (D316)."""
    return [int(n) for n in HEADING.findall(text)]


def mentioned_numbers(text: str) -> set[int]:
    """Nennungen: Grossbuchstabe O unmittelbar gefolgt von einer Ziffernfolge."""
    return {int(n) for n in MENTION.findall(text)}


def findings(numbers: list[int], mentioned: set[int]) -> list[str]:
    """Lücken, Dubletten, Nennungen ohne Posten (D316).

    Sichert, dass eine genannte Nummer existiert, nicht dass der Posten
    die Nennung trägt. Dieselbe Grenze wie bei den Abschnittsverweisen (D229).
    Ein Posten ohne Nennung ist kein Befund.
    """
    problems: list[str] = []
    if not numbers:
        return ["keine Posten gefunden"]

    seen: set[int] = set()
    for num in numbers:
        if num in seen:
            problems.append(f"O{num} doppelt")
        seen.add(num)

    missing = sorted(set(range(1, max(numbers) + 1)) - seen)
    if missing:
        problems.append("fehlend: " + ", ".join(f"O{n}" for n in missing))

    unknown = sorted(mentioned - seen)
    if unknown:
        problems.append(
            "nennt unbekannte Nummer: " + ", ".join(f"O{n}" for n in unknown)
        )
    return problems


def main() -> int:
    posts_text = OFFEN.read_text(encoding="utf-8")
    register_text = REGISTER.read_text(encoding="utf-8")
    numbers = post_numbers(posts_text)
    mentioned = mentioned_numbers(posts_text) | mentioned_numbers(register_text)
    problems = findings(numbers, mentioned)
    if problems:
        for problem in problems:
            print(problem)
        return 1
    print(len(numbers))
    return 0


if __name__ == "__main__":
    sys.exit(main())
