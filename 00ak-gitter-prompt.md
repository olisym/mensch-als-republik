# 00ak — Das Mutationsgitter, Stufe 1

## Branch und Basis

Branch `00ak-gitter`, Basis ist der Register-Commit auf diesem Branch (D297). Ein Commit am Ende,
kein Merge.

## Normative Grundlage

- **D289** — Bauform der Kampagne: vollständiges Gitter statt Suchverfahren, Saat sind die gültigen
  Vektoren aus Anhang C, mutiert wird die dekodierte Map, danach kanonisch neu kodiert. Beschluss 2
  verlangt die Neusignierung über den mutierten Core, Beschluss 3 eine unsignierte dritte Familie,
  Beschluss 5 den Ausgang „angenommen" samt `claim_id` im Ausgabetupel.
- **D297** — die Typklasse wird aufgefächert; drei Operatoren kommen hinzu; signiert wird mit dem
  Schlüssel der Saat.
- **D293** — der Korpusbauer liegt im Repo, der Vergleich mit einer zweiten Fassung außerhalb.
- `01 §2` — die zehn Felder. `01 §B.2` — die zwölf Reject-Codes.

## Auftrag

### 1. `tools/gitter.py`, neu

Ein Modul, das die Mutantenmenge deterministisch erzeugt.

**Saat.** Die Vektoren mit den Namen TV1 bis TV6 aus `tests/vectors/vectors_01.json`, über
`tools/korpus.py` gelesen und mit `cbor_canon.decode` in ihre signierte Map zerlegt.

**Typklassen.** Zehn Muster, je eines für uint, negative Ganzzahl, Bytefolge, Zeichenfolge, Array,
Map, Wahrheitswert, Null, Gleitkomma und Tag. Die Klasse eines Wertes wird bestimmt, bevor eine
Typmutation angewandt wird; ein Muster der eigenen Klasse wird übersprungen. Die Bestimmung prüft
den Wahrheitswert **vor** der Ganzzahl, weil ein Wahrheitswert in Python eine Ganzzahl ist (D272).

**Operatoren, je Feld ausser Schlüssel neun.**

- *Typ tauschen*: das Feld bekommt jedes der zehn Muster, dessen Klasse nicht die eigene ist.
- *Wert innerhalb der Klasse*: uint bekommt null, eins, den eigenen Wert plus eins, den eigenen
  Wert minus eins, zwei hoch zweiunddreissig und zwei hoch vierundsechzig minus eins; negative
  Ganzzahlen minus eins sowie den eigenen Wert plus und minus eins; eine Bytefolge die Nullfolge
  und die Einsfolge gleicher Länge, sich selbst rückwärts, sich selbst um ein Byte kürzer und um
  ein Nullbyte länger; eine Zeichenfolge ihre Gross- und ihre Kleinschreibung, sich selbst mit
  einem Zeichen vorn und mit einem Zeichen hinten sowie um ein Zeichen kürzer; ein Wahrheitswert
  sein Gegenteil; ein Array sich selbst ohne das letzte Element, mit einem angehängten Element und
  in umgekehrter Reihenfolge. Varianten, die dem Ausgangswert gleichen, entfallen; bei uint
  entfallen negative Ergebnisse.
- *Rekursion*: ist das Feld ein Array, werden auf jedes seiner Elemente die Typmuster und die
  Wertvarianten angewandt.
- *Key entfernen*: das Feld wird gelöscht.
- *Fremdwert*: das Feld bekommt den Wert desselben Feldes aus einer anderen Saat, sofern dort
  vorhanden und verschieden.
- *Feldkopie*: der Wert eines Feldes wird auf ein anderes Feld derselben Saat gelegt, sofern beide
  verschieden sind.

**Je Saat zusätzlich**: ein Schlüssel ausserhalb der Tabelle, drei Stück, mit dem Wert eins.

**Familie A.** Jeder Mutant wird über seinen eigenen Core — die Schlüssel ausser neun — mit dem
Schlüssel des Autors der **Saat** signiert, nicht mit einem aus dem mutierten Feld abgeleiteten.
Die Signatur steht dann auf Schlüssel neun, und die ganze Map wird kanonisch kodiert.

**Familie B.** Dieselben Mutanten ohne Neusignierung, also mit der Signatur der Saat. Dazu die
Mutationen auf Schlüssel neun selbst: Typmuster ausser dem der eigenen Klasse, die Wertvarianten
und das Entfernen.

**Entdopplung.** Eine Drahtfolge, die schon vorkommt, wird verworfen; ebenso jede, die einer Saat
gleicht. Familie B enthält nichts, was schon in Familie A steht. Bei einer Kollision gewinnt der
zuerst erzeugte Mutant sein Etikett.

**Ausgabe.** Eine Funktion liefert Paare aus Etikett und Drahtbytes in Hex, in stabiler
Reihenfolge. Das Etikett benennt Familie, Saat, Feld, Operator und Detail und ist eindeutig. Dazu
ein `main` in der Form von `tools/korpus.py`: ohne Argument die Hexzeilen, mit `--manifest` die
Etiketten.

### 2. `tests/test_gitter.py`, neu

- Die Etiketten sind paarweise verschieden, und Etiketten- und Hexausgabe haben gleich viele
  Zeilen.
- Keine Drahtfolge des Gitters gleicht einer Saat, und keine kommt zweimal vor.
- Zwei Aufrufe liefern dasselbe Ergebnis.
- Für Familie A: die Signatur auf Schlüssel neun ist die Signatur des Autors der Saat über den Core
  des Mutanten. Nachgerechnet, nicht geglaubt.
- Die Menge der Reject-Codes, die das Gitter über `tools.verdikt` erzeugt, ist die Menge aller
  zwölf Codes ohne `NON_CANONICAL_ENCODING` und ohne `FOREIGN_LIFECYCLE`. Die erwartete Menge wird
  aus der Aufzählung der Fehlerklassen **abgeleitet**, die beiden Ausnahmen werden benannt.
- Mindestens ein Mutant wird angenommen, und jeder angenommene trägt eine `claim_id` aus
  vierundsechzig Hexziffern.

## Nicht-Ziele

- **Keine Stufe 2.** Kombinationen aus zwei und drei Mängeln sind nicht Gegenstand dieses Laufs.
- **Kein Aufruf der Go-Fassung**, kein Verweis auf sie in einer Datei des Repos.
- Keine Änderung an `tools/verdikt.py`, `tools/korpus.py`, `tests/vectors/gen.py`,
  `tests/vectors/vectors_01.json` oder an einer Datei unter `mensch_als_republik`.
- Keine Änderung an einer Spec- oder Prompt-Datei.
- Keine getippte Mutantenzahl in Code oder Test. Zahlen werden gemessen und gemeldet, nicht
  festgeschrieben.
- Keine neue Abhängigkeit ausser `cbor2`, das bereits Abhängigkeit ist.

## Abnahmekriterien

1. `make check` grün.
2. Gemeldet werden: die Zahl der Rohmutanten, die Zahl in Familie A, die Zahl in Familie B, die
   Summe der verschiedenen Drahtfolgen, die Zahl der angenommenen Mutanten und die Verteilung der
   Verdikte über die Codes, je Familie.
3. Drei Rücknahmeproben am Gitter, jede einzeln und jede danach zurückgenommen: der Wertoperator
   abgeschaltet, die Rekursion abgeschaltet, die Feldkopie abgeschaltet. Gemeldet wird je Probe,
   **welche** Codes dadurch unerreichbar werden und **welcher Test namentlich** rot wird
   (Prüfregel 60). Eine Probe, die keinen Test rot macht, wird als solche gemeldet und nicht
   nachgebessert.
4. Widerspricht eine Messung diesem Prompt, wird sie **gemeldet, nicht angepasst**.

## Abschluss

Ein Commit auf `00ak-gitter`. Danach der **vollständige** `git diff` gegen den Branchpunkt,
zusammen mit den Zahlen aus Punkt 2 und den drei Probenergebnissen aus Punkt 3.
