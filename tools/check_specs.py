#!/usr/bin/env python3
"""Prüft die Spec-Dateien auf Defekte, die beim Editieren entstehen.

Fängt genau die Klasse von Fehlern, die in der Rev-2-Sitzung aufgetreten ist:
Markdown-Autoformatierung escaped Bezeichner, Heredocs zerhacken Multibyte-Zeichen,
Registereinträge verschwinden beim Zurückkopieren.

Aufruf: make check-specs
Rückgabe: 0 sauber, 1 Befund.
"""

from __future__ import annotations

import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SPECS = sorted(
    (q.name for q in ROOT.glob("*.md")),
    key=lambda n: (not n[0].isdigit(), n),
)

# Escapes, die legitim vorkommen: als Fußnotenmarker und in grep-/Regex-Ausdrücken
# sowie in Markdown-Tabellenzellen. Alles andere ist Editor-Schaden.
ALLOWED_ESCAPES = set("*|.b")

# Bezeichner, die als `\_` verstümmelt in der Spec auftauchen können. Ein escapter
# Unterstrich in Backticks rendert mit sichtbarem Backslash und ist damit falsch.
NEVER_ESCAPED = set("_{}[]<>#")


def read(path: Path) -> str | None:
    """Liest UTF-8 und meldet die Byte-Position bei Defekt."""
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        ctx = raw[max(0, exc.start - 40) : exc.start + 40]
        print(f"  UTF-8 defekt bei Byte {exc.start}: {exc.reason}")
        print(f"    Kontext: {ctx!r}")
        return None


def check_escapes(text: str) -> list[str]:
    """Backslash-Escapes, die kein Markdown-Autor absichtlich setzt."""
    found: dict[str, int] = {}
    for match in re.finditer(r"\\(.)", text, re.S):
        char = match.group(1)
        if char in ALLOWED_ESCAPES:
            continue
        found[char] = found.get(char, 0) + 1

    problems = []
    for char, count in sorted(found.items()):
        marker = "  ← Editor-Autoformatierung" if char in NEVER_ESCAPED else ""
        problems.append(f"escapte Zeichen: \\{char} ({count}x){marker}")
    return problems


def check_control_chars(text: str) -> list[str]:
    """Ersetzungszeichen und unsichtbare Steuerzeichen aus fehlgeschlagenen Kopien."""
    problems = []
    if "\ufffd" in text:
        problems.append(f"Ersetzungszeichen U+FFFD ({text.count(chr(0xFFFD))}x)")
    for line_no, line in enumerate(text.splitlines(), 1):
        for char in line:
            if unicodedata.category(char) == "Cc" and char != "\t":
                problems.append(f"Steuerzeichen U+{ord(char):04X} in Zeile {line_no}")
                break
    if "\r" in text:
        problems.append("CRLF-Zeilenenden")
    return problems


# Überschriften: "### D28 — ..." und kombiniert "### D16 / D22 — ..."
HEADING = re.compile(r"^### (D\d+(?:\s*/\s*D\d+)*)\s+—", re.M)


def decision_numbers(text: str) -> list[int]:
    """Alle im Register definierten D-Nummern, auch aus kombinierten Überschriften."""
    numbers = []
    for heading in HEADING.findall(text):
        numbers += [int(n) for n in re.findall(r"D(\d+)", heading)]
    return numbers


def check_decisions(text: str) -> list[str]:
    """Register: D-Einträge lückenlos und ohne Dubletten.

    Die Reihenfolge wird NICHT geprüft — das Register ist thematisch nach
    Abschnitten geordnet, nicht numerisch. Das ist Absicht.
    """
    numbers = decision_numbers(text)
    problems = []

    if not numbers:
        return ["keine D-Einträge gefunden"]

    seen: set[int] = set()
    for num in numbers:
        if num in seen:
            problems.append(f"D{num} doppelt")
        seen.add(num)

    missing = sorted(set(range(1, max(numbers) + 1)) - seen)
    if missing:
        problems.append("fehlend: " + ", ".join(f"D{n}" for n in missing))

    return problems


def check_references(text: str, known: set[int]) -> list[str]:
    """Verweise auf D-Nummern, die es im Register nicht gibt."""
    referenced = {int(n) for n in re.findall(r"\bD(\d+)\b", text)}
    unknown = sorted(referenced - known)
    if unknown:
        return ["verweist auf unbekannte Entscheidung: "
                + ", ".join(f"D{n}" for n in unknown)]
    return []


# Zuordnung Präfix → Layer-Datei. Explizite Tabelle, kein Glob: 03 und 04
# bezeichnen je vier Dateien (D209).
LAYER_FILES = {
    "00": "00-nucleus-genesis-constitution.md",
    "01": "01-claim-atom.md",
    "02": "02-trust-flow.md",
    "03": "03-profiles.md",
    "04": "04-governance.md",
    "05": "05-enforcement.md",
    "06": "06-services.md",
    "07": "07-decisions.md",
    "08": "08-scope.md",
}

HEADING_NUM = re.compile(r"^#{2,4} (\d+(?:\.\d+)*)", re.M)
SECTION_REF = re.compile(r"(?<![A-Za-z0-9])(0[0-8]) §(\d+(?:\.\d+)*)")


def layer_headings() -> dict[str, frozenset[str]]:
    """Überschriftennummern der Ebene 2–4 je Layer-Datei (D209)."""
    result: dict[str, frozenset[str]] = {}
    for prefix, name in LAYER_FILES.items():
        text = read(ROOT / name)
        if text is None:
            result[prefix] = frozenset()
            continue
        result[prefix] = frozenset(HEADING_NUM.findall(text))
    return result


def heading_covers(wanted: str, headings: frozenset[str]) -> bool:
    """Getroffen bei genauer Nummer oder bei Nummer plus Punkt (D209)."""
    if wanted in headings:
        return True
    prefix = wanted + "."
    return any(heading.startswith(prefix) for heading in headings)


def check_section_refs(
    text: str, headings: dict[str, frozenset[str]]
) -> list[str]:
    """Verweise ``NN §X.Y`` mit Ziffernpräfix 00–08 gegen die Layer-Datei (D209)."""
    counts: dict[str, int] = {}
    for prefix, section in SECTION_REF.findall(text):
        ref = f"{prefix} §{section}"
        counts[ref] = counts.get(ref, 0) + 1
    problems: list[str] = []
    for ref in sorted(counts):
        prefix, section = ref.split(" §", 1)
        if not heading_covers(section, headings[prefix]):
            problems.append(
                f"verweist auf unbekannten Abschnitt: {ref} ({counts[ref]}x)"
            )
    return problems


def main() -> int:
    register = ROOT / "07-decisions.md"
    known: set[int] = set()
    if register.exists():
        text = read(register)
        if text:
            known = set(decision_numbers(text))

    headings = layer_headings()
    failures = 0
    for name in SPECS:
        path = ROOT / name
        if not path.exists():
            continue

        problems: list[str] = []
        text = read(path)
        if text is None:
            print(f"FEHLER {name}")
            failures += 1
            continue

        problems += check_escapes(text)
        problems += check_control_chars(text)
        if name == "07-decisions.md":
            problems += check_decisions(text)
        if known:
            problems += check_references(text, known)
        excepted = name == "07-decisions.md" or name.startswith("sitzungsstart-")
        if not excepted:
            problems += check_section_refs(text, headings)

        if problems:
            print(f"FEHLER {name}")
            for problem in problems:
                print(f"  {problem}")
            failures += 1
        else:
            lines = text.count("\n") + 1
            print(f"  ok  {name:36} {lines:>5} Zeilen")

    if failures:
        print(f"\n{failures} Datei(en) mit Befund.")
        return 1

    print(f"\nAlle Spec-Dateien sauber. Register: D1–D{max(known)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
