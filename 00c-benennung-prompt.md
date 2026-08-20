# Lauf `00c-benennung` — die Benennungsregel prüfbar machen

## Rahmen

- **Branch:** `00c-benennung`, abzuzweigen von `main`.
- **Branchpunkt:** `git merge-base main 00c-benennung` — beim Schreiben dieses Prompts
  `e6b9c69`. Alle Zeilennummern unten beziehen sich auf diesen Stand.
- **Abschluss:** genau ein Commit auf dem Branch. **Kein** Merge, **kein** Push nach `main`.
- Ausgangslage: 542 Tests grün, zusätzlich 14 Eigenschaftstests unter `MAR_HYPOTHESIS=voll`.

## Normative Grundlage

`01-claim-atom.md §4.1` (neu, seit `e6b9c69`) trennt zwei Fälle:

- **Benennen.** Muss eine Ableitung aus mehreren Claims, die eine Regel gleich erfüllen, einen
  benennen, so ist es der mit der **kleinsten `claim_id`**, ausgewählt nach der inhaltlichen
  Filterung. Zulässig ist das genau dann, wenn die **Vertauschungsprobe** hält: ersetzt man den
  benannten Claim durch einen beliebigen anderen der Kandidatenmenge, ist das Ergebnis der
  Ableitung byte-gleich — das benannte Feld ausgenommen.
- **Entscheiden.** Hält die Probe nicht, darf keine abgeleitete Ordnung wählen.

`02-trust-flow.md §3.1` wendet das auf `kante_claim_id` an: die kleinste `claim_id` unter den
Gruppenmitgliedern mit `n = n_kante`; `cap`, Budget, BFS-Distanzen und Fluss lesen das Feld
nicht. Register: `D172`, Beifang aus `D171`.

Heute ist beides von **nichts** geprüft. `mensch_als_republik/trust/groups.py:117-118` bricht den
Gleichstand über `sorted(...)[0]`; `tests/trust/test_groups.py` und
`tests/trust/test_pagerank_groups.py` bauen zwar zwei aktive Vouches derselben Gruppe mit
gleichem `n`, behaupten über die Auswahl aber nichts.

## Auftrag A — Vektor auf den Wert

In `tests/trust/test_groups.py` ein Test, der einen Gleichstand baut (zwei aktive
`nuc:N/vouch@1` desselben Autors auf dasselbe Subjekt im selben Scope, gleiches `n`, beide
`ACTIVE`, keiner supersediert) und über `derive()` behauptet:

1. Die Kante dieser Gruppe trägt als `claim_id` das **Minimum** der Kandidatenmenge.
2. Die Kandidatenmenge wird im Test **aus dem Store abgeleitet**, nicht getippt: sie ist die
   Menge der `claim_id` der beiden gebauten Vouches. Keine Hex-Literale im Test.

Trägt die Sondierwelt zusätzlich eine Gruppe mit `cap == 0`, ist auch zu behaupten, dass das
`subject` des zugehörigen `SUBGRANULAR_VOUCH` denselben Wert trägt wie die Kante ihrer Gruppe.
Ist eine solche Gruppe nicht ohne Umbau zu bekommen, entfällt dieser Punkt — melden, nicht
erzwingen.

## Auftrag B — Vertauschungsprobe

Neue Datei `tests/trust/test_benennung.py`. Zwei Welten, die sich **ausschließlich** darin
unterscheiden, welcher der beiden gleichständigen Vouches die kleinere `claim_id` trägt:

- Identitäten, Scope, Parameter, Topologie, `n`, `t_exp` und `now` sind in beiden Welten
  gleich.
- Der erste Vouch `v1` ist in beiden Welten **byte-gleich**.
- Der zweite Vouch `v2` unterscheidet sich allein im deklarierten `t`. `t` ist hier inert: beide
  Vouches sind `ACTIVE`, `t_exp` liegt weit hinter `now`, kein Lebenszyklus-Akt bezieht sich auf
  sie. `v2` ist der **letzte** Claim seiner Autorenkette, damit die Änderung keinen weiteren
  Claim verschiebt.
- Das `t` von `v2` wird über einen begrenzten, im Test sichtbaren Bereich gesucht, bis eine Welt
  mit `claim_id(v1) < claim_id(v2)` und eine mit `claim_id(v2) < claim_id(v1)` vorliegt.

Behauptet wird die **Norm**, nicht der Wert:

1. Der benannte Claim ist in beiden Welten Element der Kandidatenmenge.
2. Die beiden Welten benennen **verschiedene** Claims.
3. Alles übrige ist gleich: `bfs.distance`, `bfs.node_capacity`, je Kante
   `(author, subject, cap, n_kante)`, und aus `trust()` der Wert, `disjoint_paths` und der
   Schnitt. Vermerke werden nach `kind` **und** `subject` verglichen; ausgenommen sind
   ausschließlich `Edge.claim_id` und das `subject` von `SUBGRANULAR_VOUCH`.

**Punkt 3 ist strikt zu lesen.** Erscheint ein weiterer Vermerk, dessen `subject` sich zwischen
den Welten unterscheidet, ist die Welt falsch gebaut oder `t` doch nicht inert — dann melden,
nicht die Ausnahmeliste erweitern.

Findet die Suche keinen Umschlag, ist das ein Befund: melden, keine Welt erfinden, die ihn
herbeiführt.

## Auftrag C — drei Docstring-Zeiger (`D171`)

1. `mensch_als_republik/profiles/payload.py:10` — `read_v` zitiert `03-prompt.md §3.1`. Richtig
   ist `03-profiles.md §1.3`.
2. `mensch_als_republik/governance/findings.py:41` — `dedupe_sort` zitiert `04-prompt.md §2`.
   Richtig ist `04-golden-anchors.md §8`.
3. `mensch_als_republik/findings.py:23` — `dedupe_sort` trägt **keine** Zitatzeile. Sie bekommt
   dieselbe wie die Schwester in `governance/findings.py`.

Nur die Docstrings. Keine Signatur, kein Verhalten, keine weiteren Zeiger.

## Ausdrückliche Nicht-Ziele

- **Kein Eingriff in `groups.py` oder `graph.py`.** Die Implementierung ist richtig; geprüft
  wird sie, nicht geändert.
- Keine Änderung an `tests/trust/test_pagerank_groups.py`.
- Keine neuen Vermerke, keine neuen Felder, keine Änderung an `Group` oder `Edge`.
- Kein Eigenschaftstest unter `tests/property/`. Auftrag B ist ein Vektorpaar, keine
  `hypothesis`-Strategie.
- Kein Nachziehen von `example-nucleus.md` oder dokumentierten Hashes.
- Was hier nicht steht, wird **gemeldet, nicht gebaut**.

## Rücknahmeproben (beide sind zu fahren und zu berichten)

| Eingriff | A | B |
|---|---|---|
| `groups.py`: `tied[0]` → `tied[-1]` | **rot** | **grün** |
| `graph.py`: `edges.sort(key=lambda e: e.claim_id)` statt `(e.author, e.subject)` | grün | **rot** |

Die erste Probe verletzt den Wert, nicht die Norm: bei zwei Kandidaten ist `tied[-1]` immer noch
eine Auswahl aus der Kandidatenmenge, und sie schlägt in beiden Welten um. Bleibt B dabei rot,
prüft B den Wert statt der Aussage und ist wertlos — dann melden.

Die zweite Probe macht den Namen zur Eingabe in die Kantenreihenfolge. Bleibt B dabei grün,
trägt die Sondierwelt zu wenige Kanten, als dass die Umsortierung sichtbar würde. Auch das ist
zu melden, **nicht** durch Aufblähen der Welt zu reparieren.

Beide Eingriffe werden nach der Messung vollständig zurückgenommen. Der Commit enthält sie
nicht.

## Abnahmekriterien

- `make check` grün, Testzahl **544** (542 plus die beiden neuen).
- `make check-all` grün, weiterhin 14 Eigenschaftstests.
- `git diff --numstat` gegen den Branchpunkt zeigt Änderungen **ausschließlich** in
  `tests/trust/test_groups.py`, `tests/trust/test_benennung.py`,
  `mensch_als_republik/profiles/payload.py`, `mensch_als_republik/governance/findings.py`,
  `mensch_als_republik/findings.py` und dieser Prompt-Datei.
- Beide Rücknahmeproben gefahren, Ergebnis je Zelle der Tabelle berichtet.
- Zeilen ≤ 100 Zeichen. Keine Backslash-Escapes in `.md`-Dateien.

## Bericht

Zurück kommen: der Commit-Hash, die Testzahl, die vier Ergebnisse der Rücknahmeproben, die
gefundenen `t`-Werte aus Auftrag B, und jede Stelle, an der der Prompt nicht aufging. Der
Bericht ist nicht die Abnahme; geprüft wird der Diff.
