# Werkzeug-Prompt: Nachlauf Deckenelastizität

## Branch und Basis

- Weiter auf `mess/deckenelastizitaet`, Basis unverändert `8ca6c46`. **Kein Rebase**, auch
  nicht auf den Commit, der diese Datei bringt.
- `tests/trust/test_deckenelastizitaet.py` bleibt unversioniert bis zum Abschluss. Ein Commit
  am Ende, kein Merge, kein Push nach `main`.

## Anlass

Die Meldung war richtig und der Prompt war falsch. Die gerechnete Erwartung für Fall B hat
`cap(p → h)` als Beitrag geführt. Das ist eine Schranke, kein Ertrag: `p` empfängt über
`A → p` mit `n = 4` nur `cap = 4` und kann nicht mehr weiterreichen, als bei ihm ankommt.
Gemessen `1 → 5` ist richtig, getippt `1 → 8` war falsch.

Korrigiert wird die Erwartung, **nicht** die Topologie und **nicht** ein Golden Anchor.

## Auftrag

Drei Änderungen an `tests/trust/test_deckenelastizitaet.py`. Fall A und Fall C werden **nicht**
angefasst — sie treffen die Tafel.

### 1. Beitrag von `p` einheitlich definieren

In Fall A und Fall B hat `p` genau eine Eingangs- und eine Ausgangskante. Der Beitrag ist
deshalb der **tatsächlich zugeführte Fluss**

```
min( cap(A -> p), cap(p -> h) )
```

und wird als solcher abgeleitet, beide Kantenkapazitäten aus `(n * capacity(PARAMS, d)) // D`.
Die bisherige Gleichsetzung von `cap(p -> h)` mit dem Beitrag entfällt in beiden Fällen. In
Fall A ändert das den Wert nicht (`min(4, 1) = 1`), in Fall B von `8` auf `4`.

Wo eine Testfunktion diesen Wert braucht, wird er aus derselben Hilfsfunktion bezogen, damit
die Definition nicht an zwei Stellen auseinanderlaufen kann.

### 2. Fall B: Erwartungen nachziehen

Topologie unverändert (`A → h` mit `n = 1`, `A → p` mit `n = 4`, `p → h` mit `n = 16`,
`h → S` mit `n = 16`). Neu behauptet wird:

- `d(h) == 1` vorher wie nachher — unverändert, bereits grün.
- `Σ C(h) == capacity(PARAMS, 1)` vorher wie nachher — unverändert, bereits grün.
- `value` steigt von `(1 * capacity(PARAMS, 0)) // D` auf diesen Wert **plus** den Beitrag von
  `p` nach Punkt 1.
- **Die Schranke bleibt vorher wie nachher schlaff**: `value` ist in beiden Zuständen echt
  kleiner als `Σ C(h)`. Das ersetzt die frühere Behauptung, sie werde nachher scharf.
- **Der Hebel ist genau eins**: der Zuwachs an `value` ist gleich dem Beitrag von `p`. Das
  ersetzt die frühere Behauptung, der Beitrag sei echt größer als der Zuwachs.

### 3. Fall B2 ergänzen: die gesättigte Spende

Neue Testfunktion, gleiche Form wie Fall B, nur die Anbindung von `p` ist breiter.

| Kante | `n` |
|---|---|
| `A → h` | 1 |
| `A → p` | 15 |
| `h → S` | 16 |
| `p → h` (nur im Angriffsfall) | 16 |

`A` liegt damit bei `Σ n = 16`, also genau auf `D`. Grenzmenge `{h}`, Ziel `{S}`.

Behauptet wird:

- `d(h) == 1` vorher wie nachher.
- `Σ C(h) == capacity(PARAMS, 1)` vorher wie nachher.
- Der Beitrag von `p` nach Punkt 1 ist hier durch `C(p)` und nicht durch `cap(A → p)`
  begrenzt; die Behauptung leitet ihn zusätzlich über `capacity(PARAMS, 1)` ab und prüft, dass
  beide Wege denselben Wert ergeben.
- **Die Schranke wird nachher scharf**: `value == Σ C(h)`, während sie vorher schlaff ist.
- **Der Hebel ist echt kleiner als eins**: der Zuwachs an `value` ist echt kleiner als der
  Beitrag von `p`. Eine Einheit des Zuflusses verfällt an `C(h)`.
- Keine `OVER_COMMITTED`- oder `SUBGRANULAR_VOUCH`-Findings.

Fall B und Fall B2 zusammen tragen die Aussage: eine Spende, die `d` nicht bewegt, addiert
höchstens den Fluss, den sie trägt. Fall B zeigt den Gleichstand, Fall B2 den Verfall.

## Gerechnete Erwartung (zur Abweichungsmeldung, nicht zum Abschreiben)

| Fall | `Σ C(h)` ohne → mit | `value` ohne → mit | Beitrag `p` | Hebel |
|---|---|---|---|---|
| A | 1 → 4 | 1 → 4 | 1 | 3 |
| B | 8 → 8 | 1 → 5 | 4 | 1 |
| B2 | 8 → 8 | 1 → 8 | 8 | 7/8 |
| C, k=1 | 1 → 4 | 1 → 4 | 1 | 3 |
| C, k=2 | 2 → 8 | 2 → 8 | 2 | 3 |
| C, k=3 | 3 → 12 | 3 → 12 | 3 | 3 |

Weicht eine Messung hiervon ab: **melden, nicht anpassen.** Das gilt nach dem ersten Fehlschlag
verschärft — eine zweite falsche Tafel wäre kein Grund, dem Code zu misstrauen.

## Rücknahmeprobe

Eine zusätzliche Probe, durchgeführt und im Bericht dokumentiert, nicht im Code zurückgelassen:

3. In Fall B `A → p` versuchsweise von `n = 4` auf `n = 15` heben, also auf die Belegung von
   Fall B2. Erwartung: **Fall B wird rot**, Fall B2 bleibt grün. Bleibt Fall B grün, hängt
   seine Aussage nicht an der Sättigung und der Unterschied zu B2 ist nicht gemessen.

Die Proben 1 und 2 aus dem ersten Prompt werden **erneut durchgeführt**, weil sich die
Erwartungen in Fall B geändert haben. Probe 1 lautet für Fall B jetzt: `p → h` mit `n = 2`
statt `n = 16` — Erwartung weiterhin rot.

Nach allen Proben wird der ursprüngliche Zustand wiederhergestellt und `make check-all` läuft
kalt grün. Vor dem Lauf werden `__pycache__` und `.hypothesis` entfernt.

## Ausdrückliche Nicht-Ziele

- **Keine Änderung an `mensch_als_republik/`.**
- Keine Änderung an Fall A und Fall C.
- Keine Änderung an `tests/trust/test_distanzkauf.py`. Die gemeldete Doppelung der
  D141-Topologie bleibt bewusst stehen; es wird **kein** geteilter Topologie-Baumeister
  ausgelagert.
- Keine Änderung an `02-trust-flow.md`, den Golden-Anchor-Dateien oder `07-decisions.md`.
- Kein weiterer Fall über B2 hinaus. Kein `k = 4`.
- Kein `hypothesis`.

## Abnahmekriterien

1. Fall B trifft die korrigierte Tafel; Fall B2 existiert und trifft sie.
2. Der Beitrag von `p` wird an genau einer Stelle definiert und in Fall A, B und B2 von dort
   bezogen.
3. Keine getippte Kapazitäts-, Distanz-, Kantenkapazitäts- oder Flusszahl in den Behauptungen.
4. `git diff --stat` gegen `8ca6c46` zeigt **genau eine** geänderte Datei.
5. `make check-all` läuft kalt grün. Die alte Testzahl ist `496`; die neue steigt um die Anzahl
   der Testfunktionen in der neuen Datei.
6. Alle drei Rücknahmeproben sind durchgeführt und ihr Ergebnis ist im Bericht genannt.

## Abschluss

Ein Commit auf `mess/deckenelastizitaet`. Bericht zurück: `git log --oneline -1`,
`git diff --stat` gegen `8ca6c46`, die beiden Endzeilen von `make check-all`, die neue
Testzahl, das Ergebnis aller drei Rücknahmeproben, die vollständig gemessene Tafel über alle
sechs Zustände, und jede Rückfrage. Rückfragen werden nicht selbst entschieden.
