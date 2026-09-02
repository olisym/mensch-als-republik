# Die Versionsausnahme an das Gitter binden (00al)

## Branch und Basis

Branch `00al-versionstest`, Basis-Commit `e27181d`. Ein Commit auf diesem Branch. Kein Merge,
kein Push.

## Normative Grundlage

D308 mit Beschluss und Nachtrag. Der Absatz in `01 §B.2` unter der Überschrift zur Feldtabelle je
Version trägt seit diesem Lauf beide Sätze: dass unter einer nicht unterstützten Version kein
Code gilt, dessen Aussage eine Feldbedeutung aus `01 §2` voraussetzt, und dass die Ausnahme eine
als uint lesbare `version` verlangt.

## Auftrag

**Ein Test in `tests/test_gitter.py`.** Er läuft über `mutant_lines()` und teilt jede Zeile, deren
Feld 0 nicht den Wert 1 trägt, in zwei Gruppen:

- **Lesbar fremde Version.** Feld 0 ist ein uint ungleich 1. Erwartet ist genau
  `UNSUPPORTED_VERSION`.
- **Keine lesbare Version.** Feld 0 fehlt, ist negativ oder trägt einen anderen Typ. Erwartet ist
  genau `MALFORMED_CBOR`.

Beide Gruppen sind nichtleer; das gehört in den Test, sonst trägt er nichts (Prüfregel 62).

**Der uint-Begriff.** Ein Wert ist genau dann ein uint, wenn `type(wert) is int` gilt und er nicht
negativ ist. `isinstance` ist hier falsch, weil `bool` eine Unterklasse von `int` ist und ein
`True` im Versionsfeld sonst als Version 1 durchginge (D272).

## Nicht-Ziele

- **Keine Änderung am Verifizierer, am Kodierer, an `tools/gitter.py`, `tools/paare.py`,
  `tools/korpus.py`, `tools/verdikt.py` oder an einer Spec-Datei.** Der Test beschreibt Verhalten,
  das bereits vorliegt; schlägt er an, ist das zu melden und nicht zu reparieren.
- **Kein Lauf über die Paarmenge.** Die Aussage gilt dort ebenso, aber der Test würde teuer, und
  die Gittermenge trägt sie schon.
- Keine neuen Vektoren und kein neuer Abschnitt in Anhang C.

## Abnahmekriterien

- `make check` läuft grün, ein Test mehr als im Basis-Commit.
- Der Bericht nennt die Zeilenzahl beider Gruppen. Die Zahlen werden gemessen; sie stehen
  absichtlich nicht in diesem Prompt.

## Rücknahmeprobe

Zwei Proben, je mit dem Namen des roten Tests und seiner Meldung (Prüfregel 60). Beide greifen am
Verifizierer an und lassen die Menge unberührt, über die der Test quantifiziert (Prüfregel 62):

1. Die Versionsprüfung im Verifizierer aussetzen, so dass eine fremde Version nicht mehr zu
   `UNSUPPORTED_VERSION` führt. Erwartet rot: der neue Test, in seiner ersten Gruppe.
2. Den uint-Test für das Versionsfeld aufweichen, so dass auch ein nicht-uint als fremde Version
   durchgeht. Erwartet rot: der neue Test, in seiner zweiten Gruppe.

Ein zusätzlich roter Test ist zu melden, nicht wegzunehmen. Beide Proben werden zurückgenommen,
bevor committet wird.

## Abschluss

Ein Commit auf `00al-versionstest`. Der Bericht enthält den vollständigen `git diff` gegen
`e27181d`, die Ausgabe von `make check`, die beiden Gruppengrössen und beide Rücknahmeproben mit
Testnamen.
