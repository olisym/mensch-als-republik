# Prompt 00y — Tranche D: die Tests qualifizieren und die Grammatik schließen

**Branch:** `tranche-d` — vom Basis-Commit anlegen.
**Basis-Commit:** der Commit, der diese Datei einführt.

## Normative Grundlage

`07-decisions.md` D227 (`96c70cc`): bare Paragraphenverweise in `.py` sind unzulässig. Der Befund
entsteht **im letzten Lauf**, zusammen mit der letzten Tranche. Dies ist der letzte Lauf.

`07-decisions.md` D228 (`f29f86a`): die Bereichsform bindet beide Nummern an denselben Namen.

Tranche A (`d853b1b`), B (`b84d0eb`) und C (`b51b56c`) sind erledigt. Dieser Lauf hat **zwei**
Änderungen und **drei** Proben — zwei Rücknahmeproben, je eine pro Änderung, und eine dritte, die
eine Behauptung dieses Prompts belegt.

## Änderung 1 — die letzten 18 baren Verweise qualifizieren

Alle in `tests/`. Die Zielnamen sind einzeln gegen die Zieldatei geprüft und **nicht**
abzuleiten. Sie verteilen sich auf sieben verschiedene Dateien; dieselbe Nummer meint an
verschiedenen Stellen verschiedene Ziele.

| Datei | Zeile | heute | künftig |
|---|---:|---|---|
| `governance/test_chain.py` | 127 | `§4.1` | `04 §4.1` |
| `governance/test_vermerkweitergabe.py` | 1 | `§4.5` | `04 §4.5` |
| `governance/test_vermerkweitergabe.py` | 111 | `§4.1` | `04 §4.1` |
| `governance/test_vermerkweitergabe.py` | 144 | `§4.5` | `04 §4.5` |
| `helpers.py` | 55 | `§2.3` | `02a §2.3` |
| `nucleus/test_anchor.py` | 1 | `§6.4` | `00 §6.4` |
| `test_verifier.py` | 236 | `§5.3` | `01 §5.3` |
| `trust/test_anchors.py` | 216 | `§4` | `02 §4` |
| `trust/test_bootstrap.py` | 92 | `§5` | `02a §5` |
| `trust/test_bootstrap.py` | 94 | `§5` | `02a §5` |
| `trust/test_invariants.py` | 115 | `§4` | `02 §4` |
| `trust/test_pagerank_invariants.py` | 21 | `§9` | `02b §9` |
| `trust/test_pagerank_invariants.py` | 114 | `§5` | `02 §5` |
| `trust/test_pagerank_invariants.py` | 114 | `§4` | `02 §4` |
| `trust/test_pagerank_invariants.py` | 210 | `§4` | `02 §4` |
| `trust/test_pagerank_invariants.py` | 210 | `§7` (1.) | `02 §7` |
| `trust/test_pagerank_invariants.py` | 210 | `§7` (2.) | `02 §7` |
| `trust/test_pagerank_invariants.py` | 232 | `§11` | `02b §11` |

Alle Pfade relativ zu `tests/`.

**Eine Stelle mit gemischter Namensform.** In `test_vermerkweitergabe.py` Zeile 1 steht der
Nachbar als Dateiname. Er wird auf die Kurzform gebracht, wie in Tranche A und C — zwei
Namensformen für dieselbe Datei in einer Klammer lesen sich, als wären zwei Ziele gemeint.

**Zeilennummern sind Fundhilfen, kein Anker.** Identifiziere die Stellen über den Text.

## Änderung 2 — `tools/check_specs.py` meldet bare Verweise in Python

Ein **barer** Verweis ist ein Paragraphenzeichen, dem unmittelbar eine Ziffer folgt und dem
**kein** auflösbarer Zitiername unmittelbar vorangeht. Auflösbar heißt: Kurzform aus
`LAYER_FILES` oder Stamm einer Wurzel-`.md`-Datei — dieselbe Prüfung, die `check_section_refs`
schon anwendet. Ein solcher Verweis ist ein Befund; die Datei und die Zahl der Fundstellen
gehören in die Meldung.

Drei Abgrenzungen, jede gemessen:

- **Nur `.py`.** D227 spricht ausschließlich von Python. Die Wurzel-`.md` führen bare Verweise
  in großer Zahl und bleiben unberührt.
- **Nur Ziffern.** Die Anhangsform mit Buchstaben ist nach D227 ausdrücklich offen. In `.py`
  gibt es davon ohnehin keinen Fall.
- **Regex-Literale sind keine Verweise.** In `tools/check_specs.py` und
  `tools/register_index.py` steht das Paragraphenzeichen sechsmal in Mustern und
  Format-Strings; dort folgt ihm eine öffnende Klammer, eine geschweifte Klammer oder ein
  Leerzeichen. Die Ziffernbedingung schließt sie aus, ohne dass eine Ausnahmeliste nötig wäre.
  Entsteht doch eine Ausnahmeliste, ist das ein Befund und zu melden.

**Kein separater Test für die Bereichsauflösung aus D228.** Für `tools/` gibt es heute keine
Tests; die Werkzeuge werden durch `make check` an den echten Spec-Dateien ausgeführt. Der neue
Befund deckt die Bereichsregel mit ab: bricht die optionale Gruppe in `SECTION_REF`, werden die
acht zweiten Bereichsnummern bar und der Befund feuert. Probe 3 belegt genau das.

## Nicht-Ziele

- **Keine weitere Überarbeitung.** Keine Umformulierung, keine Ergänzung, keine Korrektur von
  Tippfehlern, die dabei auffallen — melden statt beheben.
- **Keine Verhaltensänderung an geprüftem Code.** Nur Docstrings und Kommentare in `tests/`,
  plus die neue Prüfung in `check_specs.py`. Keine Testlogik wird angefasst.
- **Keine Ausnahmeliste für einzelne Dateien** in der neuen Prüfung.
- **Keine neue Testdatei.**

## Abnahmekriterien

Abgeleitet, nicht getippt:

1. `make check` grün. **597** Tests, unverändert.
2. Die Python-Zeile meldet **121 Dateien, 260 Verweise**. Heute sind es 242, dazu die 18.
3. Die neue Prüfung meldet **null** bare Verweise. Findet sie welche, ist das ein Befund und zu
   melden — nicht durch eine Ausnahme zu beheben.
4. Der Diff berührt **genau acht** Dateien: `tools/check_specs.py` und die sieben Testdateien.
5. Keine Spec-Datei wird rot.

## Proben

**Probe 1, Rücknahme für Änderung 1.** In `trust/test_pagerank_invariants.py` Zeile 232 wird die
Kurzform von `02b` auf `02` geändert. `check_specs.py` muss einen Befund melden, der die Kurzform
02 und die Nummer 11 nennt — `02-trust-flow.md` endet bei Abschnitt 10.

**Probe 2, Rücknahme für Änderung 2.** In `test_verifier.py` wird an der neu qualifizierten
Stelle die Kurzform samt Leerzeichen entfernt, sodass der Verweis wieder bar dasteht.
`check_specs.py` muss genau **einen** baren Verweis melden, in genau dieser Datei.

**Probe 3, Kopplung von Änderung 2 an D228.** In `SECTION_REF` wird die optionale Bereichsgruppe
entfernt. `check_specs.py` muss dann **acht** bare Verweise melden, verteilt auf
`tools/example_nucleus.py` und fünf Testdateien. Das belegt, dass die Bereichsregel ohne eigenen
Test regressionssicher ist.

Alle drei Ausgaben **wörtlich** in den Bericht. Nach jeder Probe zurücknehmen und bestätigen,
dass `check_specs.py` wieder grün läuft.

Fällt eine Probe nicht rot aus oder weicht Probe 3 von acht ab, ist das ein Befund und kein
Grund, das Kriterium anzupassen.

## Abschluss

Ein Commit auf `tranche-d`, kein Merge, kein Push. Der Bericht enthält den **vollständigen**
`git diff` gegen den Branchpunkt, die Python-Zeile von `check_specs.py` und die wörtliche
Ausgabe aller drei Proben.

Widerspricht eine Messung diesem Prompt, wird sie gemeldet, nicht angepasst.
