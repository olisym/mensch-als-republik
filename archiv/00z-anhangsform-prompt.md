# Prompt `00z-anhangsform` — Anhangsnummer und Backtick-Form (D230, D231)

## 0. Rahmen

Branch `impl/00z`, abgezweigt von `main`. Basis ist der **Branchpunkt** — der Commit, der D231 und
diese Datei trägt; `git merge-base main HEAD` nennt ihn. Ein Commit am Ende, **kein Merge, kein
Push**.

Geändert werden drei Dateien: `tools/check_specs.py`, `00-nucleus-genesis-constitution.md` und
`02b-abnahme.md`. Keine weitere.

## 1. Normative Grundlage

- **D209**, **D215**, **D219**, **D221**: die Verweisprüfung, ihre Ausdehnung auf Python, die
  Kurzform mit Buchstaben, die zwei Namensformen.
- **D227**: bare Verweise sind in `.py` ein Befund. In `.md` sind sie zulässig und bleiben es.
- **D228**: die Bereichsform bindet beide Nummern an denselben Namen.
- **D230** (Commit `2919e76`): die Anhangsnummer wird auf die Form Großbuchstabe, Punkt, Zahl
  beschränkt und geprüft. Dazu vier Textkorrekturen.
- **D231** (Commit `45731f5`): `SECTION_REF` toleriert einen schließenden Backtick zwischen Namen
  und Paragraphenzeichen. Enthält die Berichtigung zu D230.

Bei einem Widerspruch zwischen diesem Prompt und dem Register gilt das Register, und der
Widerspruch wird gemeldet.

## 2. Auftrag

### (a) Die Anhangsnummer als Überschriftennummer

`HEADING_NUM` erfasst heute Überschriften der Ebenen 2 bis 4, deren erstes Wort eine Ziffernfolge
ist, optional durch Punkte gegliedert. Künftig darf dieser Nummer **ein einzelner Großbuchstabe
mit unmittelbar folgendem Punkt** vorangehen. Der Ebenenbereich, die Ziffernfolge und die
Punktgliederung bleiben unverändert.

Gemessen auf `45731f5`, Zuwachs an erfassten Überschriften:

| Datei | vorher | nachher |
|---|---:|---:|
| `01-claim-atom.md` | 23 | 35 |
| `02a-abnahme.md` | 0 | 12 |
| `02b-abnahme.md` | 0 | 10 |
| `02-spec-nachzug.md` | 0 | 9 |

Insgesamt 43 zusätzliche Überschriften, alle mit Buchstabennummer, keine andere Datei betroffen.
Weicht die Messung ab: **melden, nicht anpassen.**

### (b) Die Anhangsnummer als Abschnittsnummer

In `SECTION_REF` bekommen **beide** Nummerngruppen dieselbe optionale Erweiterung: die Nummer
hinter dem Paragraphenzeichen und die zweite Nummer der Bereichsform aus D228. Sonst bleibt die
Regex, wie sie ist.

### (c) Der schließende Backtick

`SECTION_REF` verlangt heute zwischen dem Namen und dem Paragraphenzeichen genau ein Leerzeichen.
Künftig darf dort **ein einzelner Backtick** stehen, unmittelbar hinter dem Namen und vor dem
Leerzeichen. Der Name selbst, die Endung `.md` und der negative Vorlauf bleiben unverändert.

Gemessen sind elf Stellen in sieben Dateien. Alle elf lösen nach der Änderung **grün** auf; keine
davon wird angefasst:

| Datei | Zeilen | Ziel und Nummer |
|---|---|---|
| `00b-prompt.md` | 11, 13, 13 | Nukleusdatei 5.4, Profile 4, Governance 5 |
| `03b-prompt.md` | 11, 12, 13 | Profile 1.2, Anker 03 mit 4, Nukleusdatei 4 |
| `02b-golden-anchors.md` | 437 | `02b-abnahme.md`, Nummer C.1 |
| `03-prompt.md` | 397 | Anker 03, Nummer 4 |
| `einlesen-a-prompt.md` | 6 | `01-claim-atom.md`, Nummer 6 |
| `einlesen-a-nachlauf-prompt.md` | 6 | `einlesen-a-abnahme.md`, Nummer 2 |
| `07-decisions.md` | 5857 | von der Verweisprüfung ausgenommen |

### (d) Der Kommentar über `LAYER_FILES` wird falsch

Der Kommentarblock über der Tabelle begründet heute, die gleichnamigen Abnahme-Dateien seien keine
Zitierziele, weil sie keine nummerierten Überschriften führten. Nach (a) führen zwei von ihnen
welche, und über den Dateinamen sind sie zitierbar. Der Satz wird berichtigt: die Abnahme-Dateien
sind nicht die Ziele der **Kurzform**; die Tabelle bindet die Kurzform, und der Dateiname bindet
sich selbst. D219 und D230 nennen.

Nur dieser eine Satz. Der Rest des Kommentars bleibt.

### (e) Vier Textstellen

Je eine Zeile, ohne Umbau des Umfelds. Die Zeilennummern sind auf `45731f5` gemessen; weicht eine
ab, **melden statt suchen**.

1. **`00-nucleus-genesis-constitution.md`, Zeile 76.** Der Verweis nennt Anhang C von
   `01-claim-atom.md` mit einem Paragraphenzeichen vor dem Wort Anhang. Diese Wortform wird nicht
   geprüft und bekommt keine Regex. Der Verweis wird zu Prosa: Anhang C als Wort, dann die Datei
   in Backticks, **ohne Paragraphenzeichen**. Der Rest der Zeile bleibt.
2. **Dieselbe Datei, Zeile 371.** Der Verweis lautet auf Atom-Spec und dahinter das
   Paragraphenzeichen mit A3. Es gibt keinen solchen Abschnitt: A3 ist das dritte Axiom im
   Abschnitt 1 von `01-claim-atom.md`. Neu ist ein qualifizierter Verweis auf `01 §1` und
   dahinter das Wort Axiom mit der Kennung A3, ohne zweites Paragraphenzeichen.
3. **Dieselbe Datei, Zeile 418.** Wortgleich derselbe Fall, innerhalb eines eingerückten
   Listenpunkts. Die Einrückung bleibt unangetastet.
4. **`02b-abnahme.md`, Zeile 30.** Der Verweis nennt die Nummer A.1 für die Schnittstellenform von
   `derive()`. Die Datei führt keine solche Überschrift; gemeint ist B.4, deren Überschrift die
   Schnittstelle der geteilten Ableitung nachzieht. Nur die Nummer ändern. **Den umgebenden Satz
   nicht anfassen** — er beschreibt einen vergangenen Stand und ist als solcher richtig.

Der Verweis aus Nummer 4 bleibt bar und damit ungeprüft; das ist so entschieden. In `.md` ist der
Selbstverweis der Normalfall, und er wird nicht mit dem eigenen Dateinamen qualifiziert.

## 3. Ausdrückliche Nicht-Ziele

- **`check_bare_refs` bleibt unverändert.** In `.py` gibt es null Fälle beider Formen. Eine
  Erweiterung auf Buchstaben machte als erstes den Docstring von `check_specs.py` rot.
- **Keine zweite Überschriftenquelle.** Die Ebene-2-Wortform mit dem Wort Anhang statt einer
  Nummer wird nicht erfasst. Deshalb Korrektur 1 in Prosa.
- **Keine Migration der elf Backtick-Stellen.** Sie bleiben, wie sie sind; die Regex kommt zu
  ihnen, nicht sie zur Regex.
- **`LAYER_FILES` wächst nicht.** Dreizehn Einträge, geschlossen seit D221.
- **Kein Test für `tools/`.** Mit D229 ausdrücklich verworfen.
- **Keine Umbenennung, kein Refactoring**, keine Änderung an der Ausgabeform, keine zusätzliche
  Zählung. Was nicht hier steht, wird gemeldet, nicht gebaut.

## 4. Abnahmekriterien

Abgeleitet, nicht getippt — jede Zahl stammt aus einer Messung auf `45731f5`.

1. `make check-specs` läuft grün und schließt mit dem Registerstand D1 bis D231.
2. Die Python-Zeile lautet unverändert 121 Dateien und 260 Verweise. Kein `.py` trägt eine der
   beiden Formen; ändert sich diese Zahl, ist etwas anderes passiert als beauftragt.
3. `make check` grün, 597 Tests. Der Lauf berührt keinen Produktivcode.
4. Keine Zeile über 100 Zeichen in den geänderten `.md`; `check-specs` prüft das mit.
5. Der Diff berührt genau drei Dateien.

## 5. Zwei Rücknahmeproben

Je eine pro Änderung. Beide Male die Ausgabe **wörtlich** berichten und danach zurücksetzen.

**Probe 1 — die Anhangsnummer.** Das Großbuchstaben-Präfix allein in `HEADING_NUM` zurücknehmen,
alles andere in Kraft lassen. `make check-specs` muss **genau einen** Befund melden: in
`02b-golden-anchors.md`, ein Verweis auf einen unbekannten Abschnitt mit der Nummer C.1. Kein
weiterer Befund.

**Probe 2 — der Backtick.** Beide Änderungen in Kraft. In `03-prompt.md`, Zeile 397, die
Abschnittsnummer 4 vorübergehend auf 99 setzen. `make check-specs` muss **genau einen** Befund
melden. Ohne die Toleranz aus (c) würde die Stelle gar nicht gelesen und bliebe still; dass der
Befund feuert, ist der Nachweis.

Keine der beiden Proben darf den Produktivcode formen (Prüfregel 45). Wird eine Probe rot, wo sie
grün sein soll, oder grün, wo sie rot sein soll: **melden, nichts nachziehen.**

## 6. Abschluss

Ein Commit auf `impl/00z`. Kein Merge, kein Push. Zurück kommen:

- der **vollständige** `git diff` gegen den Branchpunkt, nicht nur `git diff --numstat`,
- die Ausgabe von `make check-specs` und `make check`,
- beide Probenausgaben wörtlich,
- jede Abweichung von den Zahlen oben, als Meldung und nicht als Anpassung.
