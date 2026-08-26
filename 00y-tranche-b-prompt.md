# Prompt 00y — Tranche B: bare Paragraphenverweise im Trust-Paket qualifizieren

**Branch:** `tranche-b` — vom Basis-Commit anlegen.
**Basis-Commit:** der Commit, der diese Datei einführt.

## Normative Grundlage

`07-decisions.md` D227: bare Paragraphenverweise in `.py` sind unzulässig; jeder Verweis trägt
einen Namen aus D221. Qualifiziert wird in Tranchen nach Verzeichnis, der Befund in
`tools/check_specs.py` entsteht im **letzten** Lauf. Dieser Lauf ist der zweite von mehreren und
baut keine Prüfung.

Tranche A hat `mensch_als_republik/*.py` in der Paketwurzel erledigt (Commit `d853b1b`).

## Auftrag

Genau 17 bare Verweise in `mensch_als_republik/trust/*.py` bekommen ihren Zitiernamen, in der
Kurzform.

**Die Zielnamen sind nicht abzuleiten und nicht zu raten.** Sie sind einzeln gegen die Zieldatei
geprüft worden. Anders als in Tranche A zeigen sie **nicht** alle auf dieselbe Datei: elf gehen
an `02a-maxflow-prompt.md`, sechs an `02-trust-flow.md`. Zwei Nummern kommen in beiden Rollen
vor — `§4` meint in `graph.py` den Solver aus `02a`, in `derive.py` und `relax.py` den Fluss aus
`02`; `§3` meint in `graph.py` die API-Beschreibung aus `02a`, in `relax.py` das Kapazitätsmodell
aus `02`. Wer hier nach Verzeichnis oder nach Nachbarzeile geht, bindet falsch.

| Datei | Zeile | heute | künftig |
|---|---:|---|---|
| `derive.py` | 1 | `§4` | `02 §4` |
| `derive.py` | 1 | `§5` | `02 §5` |
| `derive.py` | 6 | `§5` | `02 §5` |
| `flow.py` | 1 | `§2.10` | `02a §2.10` |
| `graph.py` | 1 | `§2.8` | `02a §2.8` |
| `graph.py` | 24 | `§2.2` | `02a §2.2` |
| `graph.py` | 52 | `§2.7` | `02a §2.7` |
| `graph.py` | 107 | `§2.8` | `02a §2.8` |
| `graph.py` | 111 | `§2.7` | `02a §2.7` |
| `graph.py` | 129 | `§4` | `02a §4` |
| `graph.py` | 160 | `§3` | `02a §3` |
| `groups.py` | 89 | `§2.10` | `02a §2.10` |
| `params.py` | 14 | `§2.2` | `02a §2.2` |
| `relax.py` | 4 | `§9` | `02 §9` |
| `relax.py` | 32 | `§4` | `02 §4` |
| `relax.py` | 76 | `§5` | `02 §5` |
| `relax.py` | 91 | `§3` | `02 §3` |

**Stellen mit einem Nachbarn in derselben Klammer.** In `flow.py` Zeile 1 steht `(02a §3,
§2.10)`, in `graph.py` Zeile 1 steht `(02a §2.7, §2.8)`. Der zweite Verweis bekommt seinen
eigenen Namen; der erste bleibt unverändert. In `derive.py` Zeile 1 stehen beide Nummern vor dem
Klammerzusatz `(02b §2, D49)` — dieser Zusatz bleibt unangetastet, er zeigt auf eine dritte
Datei.

**Stellen am Docstring-Anfang.** In `graph.py` Zeile 52 beginnt der Docstring mit der Nummer;
daraus wird die Kurzform gefolgt von der Nummer, die übrige Formulierung bleibt.

**Zeilennummern sind Fundhilfen, kein Anker.** Identifiziere die Stellen über den Text.

## Nicht-Ziele

- **Keine Datei außerhalb von `mensch_als_republik/trust/*.py`.** `governance/`, `profiles/`,
  `tests/` und `tools/` sind spätere Tranchen.
- **Kein Befund für bare Verweise in `tools/check_specs.py`.** Der kommt im letzten Lauf, D227.
- **Keine Verhaltensänderung.** Nur Docstrings und Kommentare. Kein Test wird angefasst.
- **Keine weitere Überarbeitung.** Keine Umformulierung, keine Ergänzung, keine Korrektur von
  Tippfehlern, die dabei auffallen — melden statt beheben.
- **Kein bestehender Zitiername wird geändert**, auch nicht zur Vereinheitlichung.

## Abnahmekriterien

Abgeleitet, nicht getippt:

1. `make check` grün. **597** Tests, unverändert — dieser Lauf ändert kein Verhalten.
2. Die Python-Zeile von `check_specs.py` meldet **121 Dateien, 230 Verweise**. Nach Tranche A
   sind es 213; die 17 qualifizierten Stellen treten neu in den Prüfkreis.
3. Der Diff berührt **genau sechs** Dateien: `derive.py`, `flow.py`, `graph.py`, `groups.py`,
   `params.py`, `relax.py`.
4. `git diff --numstat` zeigt reine Zeilenersetzungen, gleich viele Einfügungen wie Löschungen.

## Rücknahmeprobe

Eine Probe, für die eine Änderung dieses Laufs.

Nach dem Commit: in `graph.py` Zeile 24 wird die Kurzform `02a` durch `02` ersetzt, sodass der
Verweis auf Abschnitt 2.2 von `02-trust-flow.md` zeigt. Dann
`.venv/bin/python tools/check_specs.py` laufen lassen. Erwartet ist ein Befund der Form
*verweist auf unbekannten Abschnitt*, der die Kurzform 02 und die Nummer 2.2 nennt —
`02-trust-flow.md` führt keinen Abschnitt 2.2, die Kapazitätsformel steht in
`02a-maxflow-prompt.md`. Die Ausgabe **wörtlich** in den Bericht. Danach zurücknehmen und
bestätigen, dass `check_specs.py` wieder grün läuft.

Fällt die Probe nicht rot aus, ist das ein Befund und kein Grund, das Kriterium anzupassen.

**Eine benannte Grenze dieser Probe, die nicht zu beheben ist.** Sie fängt nur Fehlbindungen auf
eine Nummer, die es im falschen Ziel nicht gibt. Die Verwechslung von `02a §4` mit `02 §4` bliebe
unentdeckt, weil beide Dateien einen Abschnitt 4 führen. Die Prüfung sichert die Existenz des
Ziels, nicht seine Richtigkeit. Deshalb ist der Diff hier die Abnahme und nicht die grüne Zeile.

## Abschluss

Ein Commit auf `tranche-b`, kein Merge, kein Push. Der Bericht enthält den **vollständigen**
`git diff` gegen den Branchpunkt, die Python-Zeile von `check_specs.py` und die wörtliche
Ausgabe der Rücknahmeprobe.

Widerspricht eine Messung diesem Prompt, wird sie gemeldet, nicht angepasst.
