# Prompt 00am — die drei Rückstände aus der Kampagne

## Branch und Basis

Branch `00am-rueckstaende`, abgezweigt vom Kopf von `main` — das ist der Commit, der diesen
Prompt und D309 einführt. Lies ihn zu Beginn mit einem Aufruf ab und nenne ihn im Bericht;
tippe ihn nicht aus dieser Zeile ab. Ein Commit am Ende, kein Merge.

## Normative Grundlage

`07-decisions.md`, Eintrag **D309** — er trägt alle vier Aufträge und ihre Begründung. Dazu D304
Beschluss zum Operator, D305 und D306 für den Zuschnitt der Stufe 2, D307 für die beiden
Rückstände. `01 §2` für die Feldtabelle, `01 §B.2` für die Codewahl.

Lies D309 vor Beginn. Widerspricht eine Messung diesem Prompt oder dem Register: **melden, nicht
anpassen.** Der Stopp mit drei gemeldeten Widersprüchen war im letzten Lauf der wertvollste Zug.

## Auftrag 1 — die fünf Namen in `tools/gitter.py` öffnen

`_SEED_NAMES`, `_SIG_KEY`, `_author_sk`, `_clone` und `_sign_a` verlieren den führenden
Unterstrich. Alle Verwendungsstellen in `tools/gitter.py` und der Importblock in `tools/paare.py`
ziehen mit. Kein Alias, keine Verdopplung: der alte Name verschwindet.

Nach diesem Auftrag darf keine Datei unter `tools/` einen Namen mit führendem Unterstrich aus einem
anderen Modul importieren.

## Auftrag 2 — der Kopfverbreiterer erhält den Schritt 26 auf 27

Die Hilfsfunktion in `tools/gitter.py`, die einen CBOR-Kopf eine Stufe breiter schreibt, behandelt
heute drei Fälle: Additional Information kleiner als 24 wird 24, 24 wird 25, 25 wird 26. Alles
Übrige liefert nichts zurück, ebenso Major sieben.

Ergänze den vierten Fall: Additional Information 26 wird 27. Das vierbytige Argument wird als
achtbytiges geschrieben, der Rest des Items bleibt unverändert. Bei 27 und bei Major sieben bleibt
es beim Nichts.

Damit greift der Operator `feldkopf_breiter` auch auf `t` und `t_exp`. Die Zahl der neuen Zeilen
steht in D309; sie ist bei der Abnahme zu **melden**, nicht in einen Test zu tippen.

## Auftrag 3 — ein Träger für die neuen Zeilen

Neuer Test in `tests/test_gitter.py`. Er leitet die erwartete Menge der
`feldkopf_breiter`-Etiketten aus den Saatbytes ab und vergleicht sie mit der tatsächlichen Menge:

- Für jede Saat aus `tools/korpus.py`, die zur Saatmenge des Gitters gehört, wird die oberste Map
  dekodiert.
- Für jeden Schlüssel wird der Wert kanonisch kodiert; das erste Byte ist der Kopf des Wertes, weil
  die Saat kanonisch ist.
- Erwartet wird ein Etikett für diesen Schlüssel genau dann, wenn der Major des Kopfes ungleich
  sieben und die Additional Information kleiner als 27 ist.
- Die beiden Mengen müssen gleich sein — nicht Teilmenge, nicht gleich groß, sondern gleich.

Der Test benutzt `cbor_canon` und `tools.korpus`, **nicht** die Kopfhilfe aus `tools/gitter.py`.
Ein Test, der den Prüfling zur Berechnung seiner eigenen Erwartung heranzieht, prüft nichts.

## Auftrag 4 — der Klassentest in `tests/test_paare.py`

Neuer Test. Für jede Zeile, deren Etikett mit `P1`, `P2` oder `P3` beginnt:

- Die beiden Einzeletiketten werden aus dem Paaretikett zurückgeführt. Die Hilfe dafür ist bereits
  vorhanden und wird von `test_vorrangprobe_verdict_is_derived_from_the_two_singles` benutzt.
- Die beiden Einzelverdikte kommen aus `tools/verdikt.py`, angewendet auf die Drahtbytes derselben
  Etiketten in der Ausgabe von `tools/gitter.py`.
- Erwartet wird `P1`, wenn beide Einzelverdikte annehmen; `P2`, wenn genau eines annimmt; `P3`,
  wenn keines annimmt.
- Zusätzlich: **kein** Einzelverdikt einer Klassenzeile lautet auf `MALFORMED_CBOR`. Das ist die
  Aussage, die den Schnitt aus D306 trägt, und sie steht bisher in keinem Test.

Die Klassenfunktion aus `tools/paare.py` wird **nicht** importiert. Die Regel wird im Test aus D305
und D306 neu formuliert. Dass die Verdikte aus der Referenz stammen, ist beabsichtigt: geprüft wird
die Zuordnung, nicht das Verdikt.

Die Ausgabe des Gitters ist teuer; berechne sie einmal je Test und halte sie in einer lokalen
Abbildung, statt sie je Zeile neu zu erzeugen.

## Nicht-Ziele

- Keine Änderung an `mensch_als_republik/`, `tools/korpus.py`, `tools/verdikt.py`.
- Keine Änderung an Anhang C in `01-claim-atom.md` und keine an `vectors_01.json`.
- Keine weiteren Operatoren, keine weiteren Familien, kein neuer Zuschnitt der Stufe 2.
- Die gleichnamigen lokalen Kopien in `tests/test_gitter.py` und `tests/test_paare.py` bleiben
  unverändert und werden **nicht** durch Importe ersetzt. Siehe D309.
- Keine getippte Zeilenzahl, Codeverteilung oder Mengengröße in irgendeinem Test.
- Keine Änderung an `07-decisions.md`, `pruefregeln.md` oder einer Layer-Datei.
- Kein Merge, kein Push nach `main`.

## Rücknahmeproben

Beide Proben werden gefahren, das Ergebnis gemeldet, und der Zustand danach zurückgesetzt.

**Probe 1 — zu den Aufträgen 2 und 3.** Nimm den Schritt 26 auf 27 zurück, sodass die Kopfhilfe
dort wieder nichts liefert. Erwartet: der Test aus Auftrag 3 wird rot, der bestehende
Operatorentest bleibt grün. Prüfe dabei ausdrücklich, dass die Menge, über die der rote Test
urteilt, nicht leer wird — sonst wäre die Probe nach Prüfregel 62 stumm.

**Probe 2 — zu Auftrag 4.** Vertausche in `tools/paare.py` die Klassennummern eins und zwei.
Erwartet: der Test aus Auftrag 4 wird rot. Prüfe auch hier, dass beide Klassen nichtleer sind.

**Zu Auftrag 1 gibt es keine Probe.** Ein Bruch der Namenskopplung erzeugt einen `ImportError` und
ist damit laut, nicht still; das ist der Grund, aus dem D307 die Kopplung überhaupt angenommen hat.

## Abnahmekriterien

1. `make check` ist grün. Die Testzahl wird gemeldet, nicht behauptet.
2. Gemeldet werden, jeweils aus einem Aufruf abgelesen und nicht geschätzt:
   - die Gesamtzahl der Zeilen des Gitters und die Zahl der Zeilen mit Präfix `C/`,
   - die Zahl der `feldkopf_breiter`-Etiketten und ihre Verteilung über Saat und Schlüssel,
   - die Gesamtzahl der Zeilen der Stufe 2 und die Verteilung über `PV`, `P1`, `P2` und `P3`.
3. Kein Import eines Namens mit führendem Unterstrich zwischen zwei Dateien unter `tools/`.
4. Die Ergebnisse beider Rücknahmeproben, jeweils mit dem Namen des Tests, der rot wurde.

## Abschluss

Ein Commit auf `00am-rueckstaende`. `git add` mit expliziten Pfaden, nie mit `-A`. Kein Merge.

Melde am Ende den **vollständigen** `git diff` gegen den Branchpunkt, nicht nur die Statistik.
