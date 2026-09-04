# Prompt 00y — Tranche C: Bereichsform prüfen und die Produktivstellen qualifizieren

**Branch:** `tranche-c` — vom Basis-Commit anlegen.
**Basis-Commit:** der Commit, der diese Datei einführt.

## Normative Grundlage

`07-decisions.md` D227 (`96c70cc`): bare Paragraphenverweise in `.py` sind unzulässig; der Befund
für bare Verweise entsteht im **letzten** Lauf, nicht in diesem.

`07-decisions.md` D228 (`f29f86a`): die Form `NAME §A–§B` ist zulässig und bindet **beide**
Nummern an denselben Namen. Halbgeviertstrich und Bindestrich sind beide zulässige Trennzeichen.

Tranche A (`d853b1b`) und Tranche B (`b84d0eb`) sind erledigt. Dieser Lauf hat **zwei**
Änderungen und deshalb **zwei** Rücknahmeproben, je eine pro Änderung.

## Änderung 1 — `tools/check_specs.py` löst die Bereichsform auf

`SECTION_REF` erfasst heute genau eine Abschnittsnummer hinter einem Namen. Künftig erfasst der
Verweis eine **optional folgende zweite** Nummer, eingeleitet durch einen Trennstrich und ein
weiteres Paragraphenzeichen. Beide Nummern werden gegen dieselbe Zieldatei aufgelöst und geprüft,
beide zählen einzeln in `n_resolved`.

**Die Falle, die es zu vermeiden gilt:** eine zusätzliche, zweite Regex neben `SECTION_REF`
lässt den ersten Teil des Bereichs doppelt zählen, weil `SECTION_REF` ihn weiterhin selbst
matcht. Die Erfassung gehört in **eine** Regex mit einer optionalen Gruppe; die Auswertung muss
dann über die Matches laufen, nicht über `findall`-Paare.

Das Verhalten für alle übrigen Verweise bleibt unverändert: Kurzform über `LAYER_FILES`,
Dateiname über den Stamm einer Wurzel-`.md`, sonst übergangen; ein Kurzform-Name ohne
Tabelleneintrag bleibt ein Befund.

**Kein Befund für bare Verweise.** Der kommt im letzten Lauf, D227.

## Änderung 2 — vier bare Verweise qualifizieren

| Datei | Zeile | heute | künftig |
|---|---:|---|---|
| `mensch_als_republik/governance/findings.py` | 1 | `04-governance.md §3.5, §4.1` | `04 §3.5, 04 §4.1` |
| `mensch_als_republik/governance/objects.py` | 1 | `04-governance.md §1.1, §2.4` | `04 §1.1, 04 §2.4` |
| `mensch_als_republik/profiles/credit.py` | 38 | `03-profiles.md §1.3, §3.3.1` | `03 §1.3, 03 §3.3.1` |
| `tools/example_nucleus.py` | 694 | `example-nucleus.md §4.3, §7` | `example-nucleus.md §4.3, example-nucleus.md §7` |

**Warum der Nachbar in den ersten drei Zeilen mitgeändert wird**, obwohl er heute schon
qualifiziert ist: zwei verschiedene Namensformen für dieselbe Datei in einer Klammer lesen sich,
als wären zwei Ziele gemeint. Tranche A hat denselben Fall in `domains.py` so aufgelöst; das ist
der Präzedenzfall. In der vierten Zeile geht das nicht — `example-nucleus.md` hat keine Kurzform,
also wird der Name wiederholt.

**Die beiden Bereichsstellen in `tools/example_nucleus.py` (Zeilen 174 und 199) bleiben
unverändert.** `example-nucleus.md §2–§5` ist nach D228 bereits vollständig qualifiziert; die
zweite Nummer wird durch Änderung 1 geprüft, nicht durch eine Textänderung.

## Nicht-Ziele

- **Keine Datei in `tests/`.** Die restlichen 18 baren Verweise sind Tranche D.
- **Keine weitere Überarbeitung.** Keine Umformulierung, keine Ergänzung, keine Korrektur von
  Tippfehlern, die dabei auffallen — melden statt beheben.
- **Keine Vereinheitlichung der Trennstriche.** D228 lässt beide zu, ausdrücklich.
- **Keine Verhaltensänderung außerhalb von `check_specs.py`.** Kein Test wird angefasst.

## Abnahmekriterien

Abgeleitet, nicht getippt:

1. `make check` grün. **597** Tests, unverändert.
2. Die Python-Zeile von `check_specs.py` meldet **121 Dateien, 242 Verweise**. Heute sind es 230.
   Die Rechnung: vier neu qualifizierte Stellen, plus acht zweite Bereichsnummern, die durch
   Änderung 1 in den Prüfkreis treten — zwei davon in `tools/example_nucleus.py`, sechs in
   `tests/`, ohne dass eine Testdatei angefasst wird.
3. Der Diff berührt **genau fünf** Dateien: `tools/check_specs.py`, `findings.py`, `objects.py`,
   `credit.py`, `tools/example_nucleus.py`.
4. Keine Spec-Datei wird rot. Alle Bereichsverweise sind beidseitig gedeckt; wird eine Datei rot,
   ist die Regex zu weit gefasst und greift auf etwas, das kein Bereich ist.

## Rücknahmeproben

Zwei Proben, eine je Änderung. Beide müssen **unabhängig** rot ausfallen.

**Probe 1, für Änderung 1.** In `tools/example_nucleus.py` Zeile 174 wird im Bereich die zweite
Nummer von 5 auf 99 geändert. `.venv/bin/python tools/check_specs.py` muss einen Befund melden,
der `example-nucleus.md` und die Nummer 99 nennt. Fällt die Probe nicht rot aus, wird die zweite
Bereichsnummer nicht geprüft und Änderung 1 ist wirkungslos.

**Probe 2, für Änderung 2.** In `mensch_als_republik/profiles/credit.py` wird die Kurzform der
neu qualifizierten Stelle von `03` auf `05` geändert. `check_specs.py` muss einen Befund melden,
der die Kurzform 05 und die Nummer 3.3.1 nennt — `05-enforcement.md` führt keinen solchen
Abschnitt.

Beide Ausgaben **wörtlich** in den Bericht. Nach jeder Probe zurücknehmen und bestätigen, dass
`check_specs.py` wieder grün läuft.

Fällt eine Probe nicht rot aus, ist das ein Befund und kein Grund, das Kriterium anzupassen.

## Abschluss

Ein Commit auf `tranche-c`, kein Merge, kein Push. Der Bericht enthält den **vollständigen**
`git diff` gegen den Branchpunkt, die Python-Zeile von `check_specs.py` und die wörtliche
Ausgabe beider Rücknahmeproben.

Widerspricht eine Messung diesem Prompt, wird sie gemeldet, nicht angepasst.
