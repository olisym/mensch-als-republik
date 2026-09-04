# Prompt `00v-grammatik` — Die Dateinamensform prüfen (D221)

## 0. Rahmen

Branch `impl/00v`, abgezweigt von `main`. Basis ist der **Branchpunkt** — der Commit, der D221 und
diese Datei trägt; `git merge-base main HEAD` nennt ihn. Ein Commit am Ende, **kein Merge, kein
Push**.

Geändert werden fünf Dateien: `tools/check_specs.py` und vier Dateien mit je einem toten Zeiger.
Keine weitere.

## 1. Normative Grundlage

- **D209** hat `LAYER_FILES` und die Abschnittsprüfung angelegt.
- **D215** hat sie auf Python ausgedehnt.
- **D219** hat die Kurzform mit Buchstaben gebunden und den unbekannten Zitiernamen zum Befund
  gemacht.
- **D221** entscheidet die Grammatik: **zwei** Namensformen, ein fehlender Dateistamm ist **kein**
  Befund, die Anhangs-Zielform wird **nicht** gebaut. D221 ist die Grundlage dieses Laufs. Bei
  einem Widerspruch zwischen diesem Prompt und D221 gilt D221, und der Widerspruch wird gemeldet.

Heute erfasst `SECTION_REF` nur die Kurzform. Verweise, die die Datei beim Namen nennen — 321
Stück über `.md` und `.py` — fallen still durch.

## 2. Auftrag

### (a) Drei Klassen bei der Auflösung eines Namens

Ein Paragraphenverweis besteht aus einem Namen und einer Abschnittsnummer. Der Name wird in
dieser Reihenfolge geprüft:

1. **Kurzform** — der Name passt auf `0[0-8]` mit optionalem Kleinbuchstaben. Dann entscheidet
   `LAYER_FILES`. Fehlt der Eintrag, bleibt es beim Befund über den unbekannten Zitiernamen
   (D219, unverändert im Wortlaut).
2. **Dateiname** — der Name ist, mit oder ohne angehängtes `.md`, der Stamm einer `.md`-Datei im
   Wurzelverzeichnis. Dann ist diese Datei das Ziel. Beide Schreibweisen sind zulässig; im Baum
   kommen beide vor.
3. **Sonst** — der Verweis wird **übergangen**. Das ist der bare Verweis, dem ein beliebiges Wort
   vorangeht, und er ist Frage 2 und nicht Gegenstand. **Kein Befund**, kein `KeyError`.

Ein fehlender Dateistamm fällt damit in Klasse 3 und erzeugt keinen Befund. Das ist ausdrücklich
so entschieden (D221): die Verweise auf die gelöschten Prompt-Dateien stehen in Umzugstabellen,
die den Namen erwähnen statt ihn zu benutzen, und syntaktisch sind die Fälle nicht zu trennen.

Die Regex darf nicht am Wortanfang zerbrechen: einem Namen darf kein Buchstabe, keine Ziffer, kein
Punkt und kein Bindestrich unmittelbar vorangehen. Sonst greift sie mitten in einen zusammen-
gesetzten Dateinamen hinein.

### (b) Überschriften aller Wurzel-Dateien indexieren

`layer_headings` liefert heute die Überschriftennummern der dreizehn Tabelleneinträge. Es muss
zusätzlich jeden Stamm der `.md`-Dateien im Wurzelverzeichnis führen. Einmal aufbauen, nicht je
Datei neu lesen. `HEADING_NUM` bleibt **unverändert** — die Anhangs-Zielform wird nicht gebaut.

### (c) Die Zählung wandert mit

`check_python_section_refs` zählt heute `len(SECTION_REF.findall(text))`. Gezählt werden künftig
die **aufgelösten** Verweise, also Klasse 1 und Klasse 2 zusammen. Klasse 3 zählt nicht. Die
Zählung muss aus derselben Auflösung stammen wie die Prüfung, nicht aus einer zweiten Regex
daneben — zwei Regexe, die auseinanderlaufen, sind genau der Defekt, den diese Prüfung fangen
soll.

### (d) Vier tote Zeiger

Je eine Zeile, ohne Umbau des Umfelds:

1. **`distanzkauf-prompt.md`**, Zeile 13: der Verweis nennt Abschnitt 2.7 und die Datei
   `02-trust-flow.md`. Die Nummer stimmt, die Datei nicht — der Abschnitt steht in
   `02a-maxflow-prompt.md`. Die Datei im Verweis austauschen, die Nummer und den Rest der Zeile
   lassen.
2. **`02b-abnahme.md`**, Zeile 115: der Verweis nennt Abschnitt 10.1 von `02b-golden-anchors.md`.
   Den gibt es nicht; gemeint ist Punkt 1 der Liste in Abschnitt 10. Auf Abschnitt 10 ändern.
   **Den umgebenden Satz nicht anfassen** — er beschreibt einen vergangenen Stand der Datei und
   ist als solcher richtig.
3. **`welten-prompt.md`**, Zeile 22: der Verweis nennt Abschnitt 6.7 von `01-claim-atom.md`. Den
   gibt es nicht; die Aussage über `INCOHERENT_EXPIRY` steht in Anhang B.2 derselben Datei. Da
   die Zielgrammatik Anhänge nicht trägt, wird der Verweis **in Prosaform** gesetzt: die Datei in
   Backticks, dann Anhang B.2 als Wort, **ohne Paragraphenzeichen**. Der Rest der Zeile bleibt.
4. **`01-claim-atom.md`**, Zeile 649: die Tabellenzelle definiert `INCOHERENT_EXPIRY` und trägt
   dahinter in Klammern einen baren Verweis auf einen Abschnitt 6.7, den die Datei nicht führt.
   Die Klammer samt Inhalt **streichen**. Die Zelle sagt die Bedingung vollständig; der Zeiger
   trägt nichts, was sie nicht schon sagt. Sonst nichts an der Tabelle ändern.

Die Zeilennummern sind auf dem Branchpunkt gemessen. Weicht eine ab: **melden, nicht suchen und
still anpassen.**

## 3. Ausdrückliche Nicht-Ziele

- **`HEADING_NUM` bleibt.** Keine Anhangs-Zielform, kein `§B.2`. D221 hat das verworfen, weil die
  Erweiterung heute null Wirkung hätte.
- **Die baren Verweise bleiben unangetastet.** 73 in `.py`. Keine Modulkontext-Heuristik, keine
  Zuordnung Verzeichnis auf Schicht, keine vorbereitende Struktur dafür.
- **`LAYER_FILES` wächst nicht.** Dreizehn Einträge, geschlossen (D221). Wer einen vierzehnten
  brauchte, hat die Dateinamensform übersehen.
- **Kein Befund für fehlende Dateistämme.** Auch nicht als Warnung, auch nicht hinter einem
  Schalter.
- **Keine Ausnahmeliste** für einzelne Dateien. Die bestehende Ausnahme für `07-decisions.md` und
  `sitzungsstart-*.md` bleibt, wie sie ist.
- **Keine Tests unter `tests/`.** Für `tools/` gibt es keine; ob das so bleibt, ist offen und wird
  hier nicht beantwortet.
- **Keine Änderung** an `check_escapes`, `check_control_chars`, `check_decisions`,
  `check_references`, `heading_covers`, `python_sources` oder an `tools/check_tree.py`.
- **Das Ausgabeformat bleibt.** Keine neue Befundart, keine neue Zeile.

## 4. Abnahmekriterien

Alle Zahlen sind auf dem Branchpunkt gemessen. Widerspricht eine Messung diesem Prompt:
**melden, nicht anpassen.**

1. `make check-specs` grün. Die Python-Zeile lautet danach
   `ok  Python-Dateien   ...   120 Dateien, 187 Verweise`. Vorher steht dort `75 Verweise`. Die
   Dateizahl bleibt 120.
2. `make check` grün, **597** Tests, `ruff` grün.
3. Die vier Korrekturen ändern je **eine** Zeile. `git diff --numstat` weist für jede der vier
   Dateien `1  1` aus. Mehr ist ein Umbau des Umfelds und ein Defekt.
4. Die Zahl der Verweise mit Kurzform bleibt **31** über `.md` und `.py`. Sie wird **abgeleitet**,
   per Grep, nicht aus diesem Prompt abgeschrieben. Ändert sie sich, ist an einer Kurzform
   gedreht worden.

## 5. Rücknahmeproben

Drei Eingriffe, zwei Proben.

**P1 — trägt (a), (b) und (d) zusammen.** Die drei Korrekturen aus (d).1 bis (d).3 zurücknehmen,
sonst nichts, `make check-specs` laufen lassen. Erwartung: **rot**, mit **genau drei** Befunden in
genau `distanzkauf-prompt.md`, `02b-abnahme.md` und `welten-prompt.md`, je einmal, je über einen
unbekannten Abschnitt. Danach die Korrekturen wieder einsetzen und die Rückkehr nach grün zeigen.
Diese Probe deckt (a) und (b) mit ab: ohne die Dateinamensform bliebe die Rücknahme wirkungslos
und der Lauf grün.

**P2 — trägt die Grammatik in beide Richtungen.** In `distanzkauf-prompt.md` vorübergehend **zwei**
Zeilen anfügen: einen Verweis auf Abschnitt 99 der Datei `werkzeuge.md`, und daneben einen Verweis
auf Abschnitt 1 einer Datei, die es nicht gibt — etwa `gibt-es-nicht.md`. `make check-specs` laufen
lassen. Erwartung: **rot** mit **genau einem** Befund in dieser Datei, nämlich über den
unbekannten Abschnitt von `werkzeuge.md`. Der zweite Verweis darf **keinen** Befund erzeugen.
Danach beide Zeilen entfernen und mit `git diff --quiet distanzkauf-prompt.md` gegen den Stand
nach (d).1 belegen, dass nichts zurückbleibt.

Beide Proben werden mit ihrer **wörtlichen Ausgabe** berichtet.

**Ohne eigene Probe bleibt:** die Streichung in `01-claim-atom.md` aus (d).4. Sie betrifft einen
**baren** Verweis, den die Prüfung nach diesem Lauf gar nicht sieht; eine rote Probe dafür wäre
erfunden. Ebenso probenlos ist die Zählung aus (c) — sie ist Abnahmekriterium 1 und wird dort
direkt abgelesen.

## 6. Abschluss

Ein Commit auf `impl/00v`. Kein Merge, kein Push, kein Rebase.

Zurückgemeldet werden: der Commit-Hash, `git diff --numstat` gegen den Branchpunkt, die letzten
drei Zeilen von `make check-specs`, die Testzahl, die abgeleitete Kurzform-Zählung und die
wörtlichen Ausgaben beider Proben.

## 7. Rückfragen

Rückfragen gehen an den Supervisor, nicht in den Code. Was hier nicht steht, wird gemeldet und
nicht gebaut.
