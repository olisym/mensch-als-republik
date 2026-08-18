"""Tabellenausgabe für Szenarioschritte (werkzeuge.md §3.1)."""

from __future__ import annotations


def tabelle(
    titel: str,
    spalten: list[str],
    zeilen: list[tuple[str, ...]],
) -> str:
    """Einfache Texttabelle: erste Spalte Bezeichner, Rest je Beobachter."""
    if not zeilen:
        return titel
    widths = [len(spalten[0])]
    for i in range(1, len(spalten)):
        widths.append(max(len(spalten[i]), *(len(row[i]) for row in zeilen)))
    header = "  ".join(spalten[i].ljust(widths[i]) for i in range(len(spalten)))
    lines = [titel, header]
    for row in zeilen:
        lines.append("  ".join(row[i].ljust(widths[i]) for i in range(len(row))))
    return "\n".join(lines)
