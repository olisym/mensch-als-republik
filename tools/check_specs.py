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


def check_line_length(text: str) -> list[str]:
    """Prosa höchstens 100 Zeichen; Tabellenzeilen und Codeblöcke ausgenommen (D222).

    Gezählt wird mit ``len()`` über den dekodierten Text, nicht in Bytes.
    Führende Leerzeichen und Blockzitat-Zeichen samt folgenden Leerzeichen
    werden nur für die Klassifikation abgezogen.
    """
    problems: list[str] = []
    in_code = False
    for line_no, line in enumerate(text.splitlines(), 1):
        body = line.lstrip(" \t")
        while body.startswith(">"):
            body = body[1:].lstrip(" \t")
        if body.startswith("```"):
            in_code = not in_code
            continue
        if in_code or body.startswith("|"):
            continue
        n = len(line)
        if n > 100:
            problems.append(f"Zeile {line_no} zu lang: {n} Zeichen")
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
# bezeichnen je vier Dateien (D209). Die gleichnamigen Abnahme-Dateien sind
# nicht die Ziele, weil sie keine nummerierten Überschriften führen und damit
# unter der geltenden Konvention kein Zitierziel sein können (D219).
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
    "01a": "01a-policy-prompt.md",
    "02a": "02a-maxflow-prompt.md",
    "02b": "02b-golden-anchors.md",
    "04a": "04a-korrektur-prompt.md",
}

HEADING_NUM = re.compile(r"^#{2,4} (\d+(?:\.\d+)*)", re.M)
SECTION_REF = re.compile(
    r"(?<![A-Za-z0-9.-])([A-Za-z0-9-]+(?:\.md)?) §(\d+(?:\.\d+)*)"
    r"(?:[–-]§(\d+(?:\.\d+)*))?"
)
SHORT_NAME = re.compile(r"0[0-8][a-z]?$")


def layer_headings() -> dict[str, frozenset[str]]:
    """Überschriftennummern der Ebene 2–4 je Layer-Datei und je Wurzel-Stamm (D209, D221)."""
    result: dict[str, frozenset[str]] = {}
    for name in SPECS:
        text = read(ROOT / name)
        nums = frozenset() if text is None else frozenset(HEADING_NUM.findall(text))
        result[name.removesuffix(".md")] = nums
    for prefix, name in LAYER_FILES.items():
        result[prefix] = result[name.removesuffix(".md")]
    return result


def heading_covers(wanted: str, headings: frozenset[str]) -> bool:
    """Getroffen bei genauer Nummer oder bei Nummer plus Punkt (D209)."""
    if wanted in headings:
        return True
    prefix = wanted + "."
    return any(heading.startswith(prefix) for heading in headings)


def check_section_refs(
    text: str, headings: dict[str, frozenset[str]]
) -> tuple[int, list[str]]:
    """Verweise mit Kurzform oder Dateiname gegen die Zieldatei (D209, D219, D221, D228).

    Drei Klassen (D221): Kurzform über ``LAYER_FILES``, Dateiname über den
    Stamm einer Wurzel-``.md``-Datei, sonst übergangen. Ein Kurzform-Name
    ohne Tabelleneintrag ist ein Befund (D219). Ein fehlender Dateistamm
    ist keiner. Ein Bereich ``NAME §A–§B`` bindet beide Nummern an denselben
    Namen (D228). Rückgabe: Zahl der aufgelösten Verweise, Befunde.
    """
    unknown_names: dict[str, int] = {}
    counts: dict[str, int] = {}
    n_resolved = 0
    for match in SECTION_REF.finditer(text):
        name = match.group(1)
        sections = [match.group(2)]
        if match.group(3) is not None:
            sections.append(match.group(3))
        if SHORT_NAME.fullmatch(name):
            if name not in headings:
                unknown_names[name] = unknown_names.get(name, 0) + len(sections)
                n_resolved += len(sections)
                continue
        else:
            stem = name.removesuffix(".md")
            if f"{stem}.md" not in SPECS:
                continue
        for section in sections:
            n_resolved += 1
            ref = f"{name} §{section}"
            counts[ref] = counts.get(ref, 0) + 1
    problems: list[str] = []
    for name in sorted(unknown_names):
        problems.append(
            f"unbekannter Zitiername: {name} ({unknown_names[name]}x)"
        )
    for ref in sorted(counts):
        prefix, section = ref.split(" §", 1)
        key = prefix.removesuffix(".md")
        if not heading_covers(section, headings[key]):
            problems.append(
                f"verweist auf unbekannten Abschnitt: {ref} ({counts[ref]}x)"
            )
    return n_resolved, problems


def python_sources() -> list[Path]:
    """``.py`` unter der Wurzel, ohne ``.venv``, stabil sortiert (D215)."""
    return sorted(p for p in ROOT.rglob("*.py") if ".venv" not in p.parts)


def check_python_section_refs(
    headings: dict[str, frozenset[str]],
) -> tuple[int, int, list[tuple[str, list[str]]]]:
    """``check_section_refs`` über alle Python-Dateien (D215, D221).

    Rückgabe: Dateizahl, Zahl der aufgelösten Verweise, Befunde je Relativpfad.
    """
    files = python_sources()
    n_refs = 0
    findings: list[tuple[str, list[str]]] = []
    for path in files:
        text = read(path)
        if text is None:
            findings.append((str(path.relative_to(ROOT)), ["UTF-8 defekt"]))
            continue
        n_resolved, problems = check_section_refs(text, headings)
        n_refs += n_resolved
        if problems:
            findings.append((str(path.relative_to(ROOT)), problems))
    return len(files), n_refs, findings


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
        problems += check_line_length(text)
        if name == "07-decisions.md":
            problems += check_decisions(text)
        if known:
            problems += check_references(text, known)
        excepted = name == "07-decisions.md" or name.startswith("sitzungsstart-")
        if not excepted:
            _, section_problems = check_section_refs(text, headings)
            problems += section_problems

        if problems:
            print(f"FEHLER {name}")
            for problem in problems:
                print(f"  {problem}")
            failures += 1
        else:
            lines = text.count("\n") + 1
            print(f"  ok  {name:36} {lines:>5} Zeilen")

    n_py, n_py_refs, py_findings = check_python_section_refs(headings)
    if py_findings:
        for rel, problems in py_findings:
            print(f"FEHLER {rel}")
            for problem in problems:
                print(f"  {problem}")
            failures += 1
    else:
        print(f"  ok  {'Python-Dateien':36} {n_py:>5} Dateien, {n_py_refs} Verweise")

    if failures:
        print(f"\n{failures} Datei(en) mit Befund.")
        return 1

    print(f"\nAlle Spec-Dateien sauber. Register: D1–D{max(known)}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
