# 00ak — Anhangsverweise im Registerindex

## Branch und Basis

Branch `00ak-index`, Basis ist der Register-Commit auf diesem Branch (D300, D301). Ein Commit am
Ende, kein Merge.

## Normative Grundlage

- **D300** — die Verweiserkennung nimmt neben der Ziffernform auch die Anhangsform an.
- **D230** — die Anhangsnummer ist ein Großbuchstabe mit Punkt vor der Ziffernfolge.
- **D209** — Zerlegung des Registers und Zweck des Index.
- **Prüfregel 38** — der Index vor der Position.

## Auftrag

### 1. `tools/register_index.py`

Die Verweiserkennung erkennt bisher nach dem Paragraphenzeichen nur eine Ziffernfolge, die weitere
punktgetrennte Ziffern tragen darf. Sie soll zusätzlich die Anhangsform erkennen: **ein
Großbuchstabe, ein Punkt, dann eine Ziffernfolge**, die ihrerseits weitere punktgetrennte Ziffern
tragen darf. Der Teil vor dem Paragraphenzeichen bleibt unverändert, ebenso die Ziffernform selbst
und alles übrige an der Datei.

Ein Verweis ohne Ziffer nach dem Großbuchstaben ist **kein** Verweis und wird nicht erkannt.

### 2. `tests/test_register_index.py`, neu

Der Index hat bisher keinen Test. Der neue prüft:

- Die Ziffernform wird weiterhin erkannt. Der Test wählt dafür einen Abschnitt, den der Index schon
  vor dieser Änderung geführt hat, und verlangt eine nichtleere Liste.
- Die Anhangsform wird erkannt. Der Test verlangt für `01 §B.1`, `01 §B.2`, `01 §B.3`, `01 §C.10`,
  `01 §C.13` und `01 §C.15` je eine nichtleere Liste.
- Für `01 §B.2` enthält die Liste die Einträge, die den Abschnitt tatsächlich nennen. Die erwartete
  Menge wird **nicht getippt**, sondern im Test aus dem Registertext abgeleitet: die D-Nummern
  aller Einträge, deren Text die Zeichenfolge `01 §B.2` enthält.
- Ein Großbuchstabe ohne Ziffer dahinter erzeugt keinen Schlüssel im Index.
- Die Reihenfolge der Liste ist die Registerreihenfolge, und keine D-Nummer kommt doppelt vor.

## Nicht-Ziele

- Keine Änderung an der Ausgabeform, weder bei der Abfrage noch bei der Übersicht.
- Keine Änderung an `tools/check_specs.py` oder an einer anderen Datei unter `tools`.
- Keine Änderung an einer Spec-, Register- oder Prompt-Datei.
- Keine Prüfung, **ob** ein Verweis richtig ist. Der Index sagt, wer einen Abschnitt nennt; die
  Richtigkeit bleibt Prüfregel 27 und ist mit D229 ausdrücklich nicht Sache eines Werkzeugs.
- Keine neue Abhängigkeit.

## Abnahmekriterien

1. `make check` grün.
2. Gemeldet werden: die Zahl der geführten Abschnitte vor und nach der Änderung, die Zahl der
   hinzugekommenen Abschnitte, und die vollständige Liste zu `01 §B.2`.
3. Gemeldet wird, dass kein vorher geführter Abschnitt seine Liste ändert. Das wird gemessen, nicht
   behauptet: die Übersicht vor der Änderung wird in eine Datei geschrieben, die Übersicht nach der
   Änderung ebenfalls, und die alte muss Zeile für Zeile in der neuen enthalten sein.
4. Eine Rücknahmeprobe: die Anhangsform wieder entfernen und melden, **welcher Test namentlich**
   rot wird (Prüfregel 60). Danach zurücknehmen.
5. Widerspricht eine Messung diesem Prompt, wird sie gemeldet, nicht angepasst.

## Abschluss

Ein Commit auf `00ak-index`. Danach der **vollständige** `git diff` gegen den Branchpunkt, zusammen
mit den Zahlen aus Punkt 2 und 3 und dem Probenergebnis aus Punkt 4.
