# Prompt 00y — Tranche A: bare Paragraphenverweise in der Paketwurzel qualifizieren

**Branch:** `tranche-a` — vom Basis-Commit anlegen.
**Basis-Commit:** der Commit, der diese Datei einführt.

## Normative Grundlage

`07-decisions.md` D227 entscheidet: bare Paragraphenverweise in `.py` sind unzulässig. Jeder
Verweis trägt einen der beiden Namen aus D221 — den Dateinamen oder die Kurzform `NN`/`NNx`.

D227 legt die Reihenfolge fest: qualifiziert wird in Tranchen nach Verzeichnis, der Befund in
`tools/check_specs.py` entsteht **im letzten Lauf**. Dieser Lauf ist der erste. Er baut keine
Prüfung.

## Auftrag

Genau 26 bare Verweise in `mensch_als_republik/*.py` (nur die Paketwurzel, keine
Unterverzeichnisse) bekommen ihren Zitiernamen. Gewählt wird die **Kurzform**, weil sie in
`atom.py` bereits in Gebrauch ist.

Die Zielnamen sind unten benannt und **nicht** abzuleiten. Sie sind einzeln gegen die Zieldatei
geprüft worden. Zeile 10 von `domains.py` zeigt auf `04`, nicht auf `01` — der Verweis steht
neben `04-governance.md §1.1`, und `04 §2.4` ist das Vorschlagsobjekt.

| Datei | Zeile | heute | künftig |
|---|---:|---|---|
| `atom.py` | 1 | `§2` | `01 §2` |
| `atom.py` | 1 | `§4` | `01 §4` |
| `atom.py` | 22 | `§2` | `01 §2` |
| `atom.py` | 49 | `§3` | `01 §3` |
| `atom.py` | 86 | `§4` | `01 §4` |
| `atom.py` | 96 | `§4` | `01 §4` |
| `atom.py` | 111 | `§4` | `01 §4` |
| `atom.py` | 140 | `§4` | `01 §4` |
| `atom.py` | 147 | `§4` | `01 §4` |
| `atom.py` | 161 | `§4` | `01 §4` |
| `cbor_canon.py` | 1 | `§3` | `01 §3` |
| `domains.py` | 1 | `§4` | `01 §4` |
| `domains.py` | 10 | `§2.4` | `04 §2.4` |
| `policy.py` | 1 | `§5.4` | `01 §5.4` |
| `policy.py` | 109 | `§5.4.2` | `01 §5.4.2` |
| `predicates.py` | 1 | `§2.2` | `01 §2.2` |
| `predicates.py` | 79 | `§2.2` | `01 §2.2` |
| `predicates.py` | 110 | `§2.2` | `01 §2.2` |
| `predicates.py` | 123 | `§2.2` | `01 §2.2` |
| `verifier.py` | 1 | `§6` | `01 §6` |
| `verifier.py` | 98 | `§2` | `01 §2` |
| `verifier.py` | 139 | `§6` | `01 §6` |
| `verifier.py` | 157 | `§3` | `01 §3` |
| `verifier.py` | 223 | `§5.3` | `01 §5.3` |
| `verifier.py` | 308 | `§5.4` | `01 §5.4` |
| `verifier.py` | 312 | `§5.4` | `01 §5.4` |

**Zwei Stellen brauchen eine Formulierungsentscheidung.** In `atom.py` Zeile 1 steht `(§2, §4)`,
in Zeile 111 steht `(D122, 01 §2/§4)`. Jede Nummer bekommt einen eigenen Namen — aus `(§2, §4)`
wird `(01 §2, 01 §4)`, aus `01 §2/§4` wird `01 §2/01 §4`. Wenn die zweite Form unlesbar wirkt,
ist auch `01 §2 und 01 §4` zulässig; der Docstring darf an dieser einen Stelle umformuliert
werden, solange die Aussage dieselbe bleibt. Jede andere Stelle wird nur um das Präfix ergänzt.

**Zeilennummern sind Fundhilfen, kein Anker.** Wird eine Zeile durch das Präfix zu lang und
umgebrochen, verschieben sich die folgenden Nummern. Identifiziere die Stellen über den Text.

## Nicht-Ziele

- **Keine Datei außerhalb von `mensch_als_republik/*.py` in der Paketwurzel.** Die Verweise in
  `trust/`, `governance/`, `profiles/`, `tests/` und `tools/` sind spätere Tranchen.
- **Kein Befund für bare Verweise in `tools/check_specs.py`.** Der kommt im letzten Lauf, D227.
- **Keine Verhaltensänderung.** Nur Docstrings und Kommentare. Kein Test wird angefasst.
- **Keine weitere Überarbeitung der Docstrings.** Keine Umformulierung, keine Ergänzung, keine
  Korrektur von Tippfehlern, die dabei auffallen — melden statt beheben.
- **Kein zweiter Zitiername je Stelle.** Wo heute schon ein Name steht, bleibt er unverändert.

## Abnahmekriterien

Abgeleitet, nicht getippt:

1. `make check` grün. **597** Tests, unverändert — dieser Lauf ändert kein Verhalten.
2. Die Python-Zeile von `check_specs.py` meldet **121 Dateien, 213 Verweise**. Heute sind es 187;
   die 26 qualifizierten Stellen treten neu in den Prüfkreis. Weicht die Zahl ab, ist entweder
   eine Stelle übersehen oder eine zusätzliche angefasst worden.
3. Der Diff berührt **genau sechs** Dateien: `atom.py`, `cbor_canon.py`, `domains.py`,
   `policy.py`, `predicates.py`, `verifier.py`.
4. `git diff --numstat` zeigt keine Datei mit mehr gelöschten als geänderten Zeilen; erwartet
   sind reine Zeilenersetzungen.

## Rücknahmeprobe

Eine Probe, für die eine Änderung dieses Laufs. Sie belegt, dass die neu qualifizierten Stellen
tatsächlich geprüft werden und nicht bloß anders formatierter Text sind.

Nach dem Commit: in `verifier.py` Zeile 308 wird die Kurzform `01` durch `05` ersetzt, sodass
der Verweis auf Abschnitt 5.4 von `05-enforcement.md` zeigt. Dann
`.venv/bin/python tools/check_specs.py` laufen lassen. Erwartet ist ein Befund der Form
*verweist auf unbekannten Abschnitt*, der die Kurzform 05 und die Nummer 5.4 nennt —
`05-enforcement.md` führt keinen Abschnitt 5.4.
Die Ausgabe **wörtlich** in den Bericht. Danach die Probe zurücknehmen und bestätigen, dass
`check_specs.py` wieder grün läuft.

Fällt die Probe nicht rot aus, ist das ein Befund und kein Grund, das Kriterium anzupassen.

## Abschluss

Ein Commit auf `tranche-a`, kein Merge, kein Push. Der Bericht enthält den **vollständigen**
`git diff` gegen den Branchpunkt — nicht `--numstat`, nicht eine Zusammenfassung — sowie die
Python-Zeile von `check_specs.py` und die wörtliche Ausgabe der Rücknahmeprobe.

Widerspricht eine Messung diesem Prompt, wird sie gemeldet, nicht angepasst.
