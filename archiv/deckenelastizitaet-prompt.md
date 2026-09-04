# Werkzeug-Prompt: Messlauf Deckenelastizität

## Branch und Basis

- Branch: `mess/deckenelastizitaet`, abgezweigt vom Commit, der **diese Datei** nach `main`
  bringt. Nicht von `c97dc9d` — der Vergleichspunkt ist der Prompt-Commit.
- Ein Commit am Ende. **Kein Merge**, kein Push nach `main`, kein Rebase.

## Normative Grundlage

- `02-trust-flow.md §4`, Satz (simultaner Fluss): `maxflow(s → S) ≤ Σ_{h ∈ Grenze} C(h)`.
- `02-trust-flow.md §4`, Warnblock „Distanz ist kaufbar" (D139/D141) — insbesondere der Satz
  „Der Min-Cut-Satz bleibt davon unberührt".
- `02-trust-flow.md §4`, **VR-02.1** — Aggregation über mehrere Identitäten MUSS den
  Multi-Sink-Fluss rechnen.
- `07-decisions.md`, **D141** — der Distanzkauf entfernt eine Decke, er trägt keinen Fluss.

## Die Frage, die der Lauf beantwortet

`§4` sagt zu Recht, dass der Min-Cut-Satz vom Distanzkauf unberührt bleibt — er ist ein Satz
über den Graphen, wie er vorliegt. Ungemessen ist, was mit der **Schranke selbst** geschieht:

> Ist `Σ_{h ∈ Grenze} C(h)` gegen den Zug des Angreifers invariant, oder wandert sie mit?

Der Lauf misst das an drei Topologien und stellt keine normative Behauptung auf. Er repariert
nichts, er mildert nichts ab, er erkennt nichts.

## Auftrag

Eine neue Testdatei `tests/trust/test_deckenelastizitaet.py`.

### Gemeinsame Parameter

```
PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=16)
now    = 1000
```

Ein Scope aus `scope_id`, alle Vouches mit `t=1, t_exp=5000`, Identitäten aus `tests.helpers`.
`A` ist stets der Anker, `p` der verwirrte seed-nahe Knoten, angebunden über `A → p` mit
`n = 4`.

Gemessen wird über `trust(...)` aus `mensch_als_republik.trust` und `derive(...)` aus
`mensch_als_republik.trust.derive` — die Funktion ist aus dem Paket **nicht** re-exportiert.
Das ist ein bekannter offener Punkt und in diesem Lauf **nicht** zu beheben.

**Die Grenzmenge steht in jeder Topologie fest, weil die Topologie sie festlegt.** Sie wird als
Konstante der jeweiligen Testfunktion geführt, und `Σ_{h ∈ Grenze} C(h)` wird als Summe über
`derive(...).bfs.node_capacity` gebildet — nicht neu gerechnet.

**Alle erwarteten Kapazitäten, Distanzen und Kantenkapazitäten werden abgeleitet.** Quelle ist
`mensch_als_republik.trust.graph.capacity(PARAMS, d)` und `PARAMS.D`. Eine getippte Kapazitäts-,
Distanz- oder Flusszahl in den Behauptungen ist ein Abnahmefehler.

### Fall A — Distanzkauf, die Topologie aus D141

Vier Ketten `A → a_i → b_i → x_i → h` mit `i = 0..3`, dazu `h → S`.

| Kante | `n` |
|---|---|
| `A → p` | 4 |
| `A → a_i` (viermal) | 3 |
| `a_i → b_i`, `b_i → x_i`, `x_i → h`, `h → S` | 16 |
| `p → h` (nur im Angriffsfall) | 2 |

Grenzmenge `{h}`, Ziel `{S}`.

Behauptet wird, jeweils ohne und mit der Kante `p → h`:

- `d(h)` fällt von `4` auf `2`, also `Σ C(h)` von `capacity(PARAMS, 4)` auf `capacity(PARAMS, 2)`.
- `trust(...).value` steigt im selben Verhältnis, von `capacity(PARAMS, 4)` auf
  `capacity(PARAMS, 2)`.
- **Die Schranke ist in beiden Zuständen scharf**: `trust(...).value == Σ C(h)`, vorher wie
  nachher.
- Der Beitrag von `p` ist eine Kapazitätseinheit, abgeleitet als `(2 * capacity(PARAMS, 1)) // D`.
- Der Zuwachs an Fluss ist echt größer als der Beitrag von `p`.

### Fall B — Kapazitätsspende, die Decke bleibt stehen

Der Kontrollfall. Keine Kette, `h` sitzt von Anfang an seed-nah, aber ausgehungert.

| Kante | `n` |
|---|---|
| `A → h` | 1 |
| `A → p` | 4 |
| `h → S` | 16 |
| `p → h` (nur im Angriffsfall) | 16 |

Grenzmenge `{h}`, Ziel `{S}`.

Behauptet wird:

- `d(h) == 1` **vorher wie nachher** — der Zug bewegt die Distanz nicht.
- `Σ C(h) == capacity(PARAMS, 1)` vorher wie nachher, also unverändert.
- `trust(...).value` steigt von `(1 * capacity(PARAMS, 0)) // D` auf `capacity(PARAMS, 1)`.
- **Die Schranke ist vorher schlaff und nachher scharf**: vorher echt kleiner als `Σ C(h)`,
  nachher gleich.
- Der Beitrag von `p` ist `(16 * capacity(PARAMS, 1)) // D` und damit echt **größer** als der
  Zuwachs an Fluss.

Fall B trägt den Kontrast. Ohne ihn könnte Fall A auch von etwas anderem als der
Distanzbewegung grün gehalten werden.

### Fall C — Skalierung über das Budget von `p`

Parametrisiert über `k = 1, 2, 3`. Je `h_j` mit `j = 0..k-1` zwei Ketten
`A → a_{j,i} → b_{j,i} → x_{j,i} → h_j` mit `i = 0..1`, dazu `h_j → S_j`.

| Kante | `n` |
|---|---|
| `A → p` | 4 |
| `A → a_{j,i}` (`2k`-mal) | 2 |
| `a → b`, `b → x`, `x → h_j`, `h_j → S_j` | 16 |
| `p → h_j` (nur im Angriffsfall, `k`-mal) | 2 |

Grenzmenge `{h_0 .. h_{k-1}}`, Ziel `{S_0 .. S_{k-1}}` — **eine echte Multi-Sink-Abfrage**,
eine einzelne `trust(...)`-Auswertung über der gesamten Zielmenge. Die Summe von
`k` Einzelabfragen ist nach VR-02.1 keine gültige Näherung und wird **nicht** gebildet.

Behauptet wird für jedes `k`:

- `Σ C(h)` steigt von `k * capacity(PARAMS, 4)` auf `k * capacity(PARAMS, 2)`.
- `trust(...).value` steigt von `k * capacity(PARAMS, 4)` auf `k * capacity(PARAMS, 2)`.
- Der Beitrag von `p` ist `k * ((2 * capacity(PARAMS, 1)) // D)`.
- Das Verhältnis von Flusszuwachs zu Beitrag ist über alle `k` **gleich** und gleich dem aus
  Fall A. Diese Behauptung ist die eigentliche Aussage des Falls.
- Die Budgetregel `Σ n ≤ D` ist für **jeden** Autor eingehalten, insbesondere für `A` und `p`.
  Für `A` gilt `4 + 4k ≤ D`; bei `k = 3` mit Gleichheit. Das wird als eigene Behauptung
  geprüft, aus `PARAMS.D` abgeleitet.
- Keine `OVER_COMMITTED`- oder `SUBGRANULAR_VOUCH`-Findings in irgendeinem `k`.

`k = 4` wird **nicht** gebaut. Dass `A`s Budget vor `p`s Budget bindet, ist der Befund; ihn
durch einen über-committeten Anker zu umgehen wäre eine andere Messung.

## Gerechnete Erwartung (zur Abweichungsmeldung, nicht zum Abschreiben)

`capacity(PARAMS, d)` ergibt `16, 8, 4, 2, 1, 0` für `d = 0..5`.

| Fall | `Σ C(h)` ohne → mit | `value` ohne → mit | Beitrag `p` |
|---|---|---|---|
| A | `1 → 4` | `1 → 4` | `1` |
| B | `8 → 8` | `1 → 8` | `8` |
| C, `k=1` | `1 → 4` | `1 → 4` | `1` |
| C, `k=2` | `2 → 8` | `2 → 8` | `2` |
| C, `k=3` | `3 → 12` | `3 → 12` | `3` |

Weicht eine Messung hiervon ab: **melden, nicht anpassen.** Weder die Erwartung im Code noch
die Topologie wird nachgezogen, um eine Zahl zu treffen. Eine Abweichung ist der wertvollste
mögliche Ausgang dieses Laufs.

## Rücknahmeproben

Zwei Proben, beide durchgeführt und im Bericht dokumentiert, keine bleibt im Code zurück:

1. **Züge tauschen.** In Fall A `p → h` versuchsweise mit `n = 16` statt `n = 2` belegen, in
   Fall B mit `n = 2` statt `n = 16`. Erwartung: **beide** Fälle werden rot. Bleibt einer
   grün, unterscheidet die Datei die beiden Mechanismen nicht, sondern misst nur, dass sich
   irgendeine Zahl bewegt.
2. **Substanz entziehen.** In Fall C bei `k = 3` eine der beiden Ketten zu `h_0` entfernen.
   Erwartung: Fall C wird rot. Bleibt er grün, hängt die Messung nicht am ehrlichen Zufluss,
   und die Aussage über den Hebel trägt nicht.

Nach beiden Proben wird der ursprüngliche Zustand wiederhergestellt und `make check-all` läuft
kalt grün. Vor dem Lauf werden `__pycache__` und `.hypothesis` entfernt (Prüfregel 19).

## Docstring

Das Modul zitiert `D141` und `02 §4`. Nach Prüfregel 17 macht das Zitat die Stelle prüfbar; der
Verweis muss auf existierenden Text zeigen.

## Ausdrückliche Nicht-Ziele

- **Keine Änderung an `mensch_als_republik/`.** Kein Modul unter dem Paket wird angefasst, auch
  nicht „nur ein Kommentar". Insbesondere wird das fehlende Re-Export von `derive` **nicht**
  nachgetragen.
- Keine Änderung an `tests/trust/test_distanzkauf.py` oder einer anderen bestehenden Testdatei.
  Entsteht dabei Doppelung der Topologie aus D141: **melden, nicht refaktorieren.**
- Keine Änderung an `02-trust-flow.md`, `02-golden-anchors.md`, `02b-golden-anchors.md` oder
  `07-decisions.md`. Der Befund wird gemessen, nicht eingetragen.
- Kein Eigenschaftstest, kein `hypothesis`. Alle drei Fälle sind feste Vektoren.
- Keine Variation über `γ` oder `C₀`. Ein Parametersatz.
- Keine Summe von Einzelabfragen in Fall C.
- Kein `k = 4`, kein über-committeter Anker.

Fällt bei der Arbeit etwas auf, das über diesen Zuschnitt hinausgeht: **melden, nicht bauen.**

## Abnahmekriterien

1. `tests/trust/test_deckenelastizitaet.py` existiert; Fall A, Fall B und Fall C mit
   `k = 1, 2, 3` sind abgedeckt.
2. Keine getippte Kapazitäts-, Distanz-, Kantenkapazitäts- oder Flusszahl in den Behauptungen;
   alle aus `capacity(...)` und `PARAMS.D` abgeleitet.
3. `Σ C(h)` wird aus `derive(...).bfs.node_capacity` gebildet, nicht nachgerechnet.
4. Fall C führt genau eine `trust(...)`-Auswertung je Zustand über der gesamten Zielmenge.
5. `git diff --stat` gegen den Prompt-Commit zeigt **genau eine** geänderte Datei.
6. `make check-all` läuft kalt grün.
7. Die alte Testzahl wird vor dem Lauf mit `python -m pytest -q --collect-only` festgestellt und
   im Bericht genannt; die neue Zahl steigt um die Anzahl der neuen Testfunktionen.
8. Beide Rücknahmeproben sind durchgeführt und ihr Ergebnis ist im Bericht genannt.

## Abschluss

Ein Commit auf `mess/deckenelastizitaet`. Bericht zurück: `git log --oneline -1`,
`git diff --stat` gegen den Prompt-Commit, die beiden Endzeilen von `make check-all`, die alte
und die neue Testzahl, das Ergebnis beider Rücknahmeproben, **die gemessene Tabelle aus
`Σ C(h)`, `value` und Beitrag für alle fünf Zustände**, und jede Rückfrage, die während der
Arbeit entstanden ist. Rückfragen werden nicht selbst entschieden.
