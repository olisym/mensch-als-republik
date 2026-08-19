# Werkzeug-Prompt: Charakterisierungstest Distanzkauf (D141)

## Branch und Basis

- Branch: `impl/distanzkauf`, abgezweigt von `71a8720` auf `main`.
- Ein Commit am Ende. **Kein Merge**, kein Push nach `main`, kein Rebase.

## Normative Grundlage

- `07-decisions.md`, **D141** — der Distanzkauf entfernt eine Decke, er trägt keinen Fluss.
- `07-decisions.md`, **D139** — der Befund selbst, in den Zahlen durch D141 ersetzt.
- `02-trust-flow.md §4`, Warnblock „Distanz ist kaufbar".
- `02-trust-flow.md §2.7` / Anker K8 — `E⁺` ist die Menge der Kanten mit `cap ≥ 1`.

## Auftrag

Eine neue Testdatei `tests/trust/test_distanzkauf.py` mit dem Charakterisierungstest zu D141.
Der Test **repariert nichts**. Er hält fest, dass eine Kante minimaler Kapazität von einem
seed-nahen Knoten die Knotendecke eines seed-fernen Grenzknotens hebt und damit bereits
vorhandenen ehrlichen Fluss freigibt.

### Parameter und Topologie

```
PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=16)
now    = 1000
```

Ein Scope aus `scope_id`, alle Vouches mit `t=1, t_exp=5000`. Identitäten aus `tests.helpers`:

- `A` — Anker.
- vier Ketten `A → a_i → b_i → x_i → h` mit `i = 0..3`.
- `h → S`, wobei `S` das Ziel ist.
- `p` — der verwirrte seed-nahe Knoten, über `A → p`.

Budgets, damit `Σ n ≤ D` je Autor eingehalten ist:

| Kante | `n` |
|---|---|
| `A → p` | 4 |
| `A → a_i` (viermal) | 3 |
| `a_i → b_i`, `b_i → x_i`, `x_i → h`, `h → S` | 16 |
| `p → h` (nur im Angriffsfall) | Fallabhängig, siehe unten |

`A` liegt damit bei `4 + 4·3 = 16`, alle übrigen Autoren bei genau einer Kante mit `n = 16`.

### Drei Fälle

1. **Ohne Angriff** — die Kante `p → h` fehlt.
2. **Angriff auf der Schwelle** — `p → h` mit `n = 2`.
3. **Angriff unter der Schwelle** — `p → h` mit `n = 1`.

### Behauptungen

Gemessen wird über `trust(...)` und `derive(...)` aus `mensch_als_republik.trust`.

**Alle erwarteten Kapazitäten und Distanzen werden abgeleitet, nicht getippt.** Die Quelle ist
`mensch_als_republik.trust.graph.capacity(PARAMS, d)`; die Schwelle für `n` wird aus
`PARAMS.D` und der Kapazität von `p` gerechnet, nicht als Literal geschrieben. Eine getippte
Zahl in diesem Test ist ein Abnahmefehler.

Fall 1:
- `d(h) == 4`
- `C(h) == capacity(PARAMS, 4)`
- `trust(...).value == capacity(PARAMS, 4)` — der Fluss wird von der Knotendecke bestimmt, nicht
  vom Zufluss.
- Der Zufluss zu `h` über `derive(...).bfs.edges` ist **echt größer** als `C(h)`. Das ist die
  eigentliche Aussage des Falls: ehrlicher Fluss liegt an und wird abgeschnitten.
- keine `SUBGRANULAR_VOUCH`-Findings.

Fall 2:
- `d(h) == 2`
- `C(h) == capacity(PARAMS, 2)`
- `trust(...).value == capacity(PARAMS, 2)`
- Die Summe der Kantenkapazitäten von `p` nach `h` ist genau `1`, ebenfalls abgeleitet als
  `(n · C(p)) // D` mit `C(p) = capacity(PARAMS, 1)`.
- Der Zuwachs an Fluss gegenüber Fall 1 ist **echt größer** als der Beitrag von `p`. Diese
  Behauptung trägt D141 und ist die wichtigste der Datei.
- keine `SUBGRANULAR_VOUCH`-Findings.

Fall 3:
- `d(h) == 4` und `trust(...).value == capacity(PARAMS, 4)`, also identisch zu Fall 1.
- Die Findings enthalten genau ein `SUBGRANULAR_VOUCH`, dessen `subject` die `kante_claim_id`
  der Gruppe `(p, h)` ist.
- Es existiert keine Kante mit `author == p.pub` in `derive(...).bfs.edges`.

Fall 3 ist die Isolierung: eine Einheit unter der Schwelle ist wirkungslos, genau auf der
Schwelle vervierfacht dieselbe Kante den Fluss. Ohne diesen Fall könnte der Test auch von etwas
anderem als dem `E⁺`-Filter grün gehalten werden.

### Rücknahmeproben

Zwei Änderungen, also zwei Proben. Beide werden **durchgeführt und im Bericht dokumentiert**,
keine bleibt im Code zurück:

1. In `bfs_capacities` den Filter `if cap == 0: continue` versuchsweise entfernen, sodass auch
   Kanten mit `cap == 0` in `E⁺` landen. Erwartung: Fall 3 wird rot. Wird er es nicht, misst
   Fall 3 nicht den Filter.
2. In `capacity` versuchsweise `d` durch eine Konstante ersetzen, sodass die Kapazität nicht
   mehr von der Distanz abhängt. Erwartung: Fall 1 **und** Fall 2 werden rot. Bleibt einer grün,
   hängt er nicht an der Distanz.

Nach beiden Proben wird der ursprüngliche Zustand wiederhergestellt und `make check-all` läuft
kalt grün.

### Docstring

Das Modul zitiert `D141` und `02 §4`. Nach Prüfregel 17 macht dieses Zitat die Stelle prüfbar —
der Verweis muss auf existierenden Text zeigen.

## Ausdrückliche Nicht-Ziele

- **Keine Änderung an `mensch_als_republik/`.** Kein Modul unter dem Paket wird angefasst, auch
  nicht „nur ein Kommentar". Der Distanzkauf wird **nicht** repariert, nicht abgemildert und
  nicht erkannt.
- Keine neuen Golden Anchors, keine Änderung an `02-golden-anchors.md` oder
  `02b-golden-anchors.md`.
- Keine Änderung an bestehenden Testdateien.
- Keine Änderung an `02-trust-flow.md` oder `07-decisions.md`.
- Kein Eigenschaftstest, kein `hypothesis`. Der Test ist ein fester Vektor.
- Keine Skalierungsmessung über mehrere Grenzknoten. Wie der Effekt mit `p`s Budget wächst, ist
  in D141 ausdrücklich als ungemessen bezeichnet und bleibt es in diesem Lauf.
- Keine Verallgemeinerung der Topologie, keine Parametrisierung über mehrere `γ` oder `C₀`.

Fällt bei der Arbeit etwas auf, das über diesen Zuschnitt hinausgeht: **melden, nicht bauen.**
Das gilt besonders für Abweichungen zwischen gemessenen und in D141 genannten Werten — solche
Abweichungen werden berichtet, nicht durch Anpassung der Erwartung geglättet.

## Abnahmekriterien

1. `tests/trust/test_distanzkauf.py` existiert, alle drei Fälle sind abgedeckt.
2. Keine getippte Kapazitäts- oder Distanzzahl in den Behauptungen; alle aus `capacity(...)` und
   `PARAMS` abgeleitet.
3. `git diff --stat` gegen `71a8720` zeigt **genau eine** geänderte Datei.
4. `make check-all` läuft kalt grün. Vor dem Lauf werden `__pycache__` und `.hypothesis`
   entfernt (Prüfregel 19).
5. Die Testzahl steigt um die Anzahl der neuen Testfunktionen; die alte Zahl ist `493`.
6. Beide Rücknahmeproben sind durchgeführt und ihr Ergebnis ist im Bericht genannt.

## Abschluss

Ein Commit auf `impl/distanzkauf`. Bericht zurück: `git log --oneline -1`, `git diff --stat`
gegen die Basis, die beiden Endzeilen von `make check-all`, das Ergebnis beider Rücknahmeproben
und jede Rückfrage, die während der Arbeit entstanden ist. Rückfragen werden nicht selbst
entschieden.
