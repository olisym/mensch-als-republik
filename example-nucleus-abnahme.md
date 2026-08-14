# Beispielnukleus — Abnahme

Gegenstand: `impl/example-nucleus`, Commits `8d2a8f5`, `8b1364d`, `fbd69a1`, gemergt als
`f3750ed`. 399 Tests, `make check` grün in drei Blöcken, Register D1–D116.

**Abgenommen.**

## 1. Was geprüft wurde

`tools/example_nucleus.py` und `tests/test_example_nucleus.py` gegen `example-nucleus.md`.

Die Leitfrage war nicht „ist der Code richtig", sondern **„ist der Nachweis tragfähig"**. Das
Werkzeug soll belegen, dass Dokument und Implementierung dasselbe meinen; dieser Beleg hält nur,
wenn jede Zahl aus dem Paket kommt und die dokumentierten Werte ausschließlich als Zusicherung
danebenstehen.

**Er hält.** Alles Rechnende stammt aus `mensch_als_republik`: `cbor_canon`,
`policy.constitution_hash`, `governance.Epoch`/`Proposal`/`decide`/`verify_ratification`,
`profiles.membership`, `trust.derive`, `trust.graph.capacity`. Keine zweite Kodierung, keine
zweite Kapazitätsformel. Die `DOC_*`-Konstanten sind Erwartungen, gegen die `_eq` **nach** der
Rechnung vergleicht; `probe_stock_anchors()` reproduziert vor allem anderen die Bestandsanker aus
`00 §3.1`.

`_Author` führt echte Autorenketten ab `SHA-256(DOM_ID_GEN ‖ I)` und signiert wirklich — kein
Attrappen-Store.

Der Test importiert ausschließlich aus dem Werkzeug: 56 Zeilen, zwölf Tests, keine doppelte Logik.

## 2. Befunde

Zwei, beide **fehlende Vektoren** — keine falsche Zeile.

**E-1 — Der Overcommit-Fall fehlte.** Die vier Kanten mit `n = 100` waren nicht geprüft, und damit
die zweite Betriebswarnung aus `example-nucleus.md §8.1` unbelegt: dass ein Vouch zu viel **alle**
Kanten desselben Autors entwertet, nicht die letzte und nicht anteilig. Behoben in `fbd69a1`;
`check_overcommit` prüft alle drei Aussagen — Vermerk für beide Autoren, Kantenmenge leer, CHRIS
weder in `distance` noch in `node_capacity`.

**E-2 — Die Weitergaberechnung fehlte.** Geprüft war die Kantenkapazität **von** einem Anker
(`50`), nicht die **von CHRIS weiter** (`25`). Erst dort zeigt sich die doppelte Rundung, vor der
`02 §8` ausdrücklich warnt. Behoben; `check_edge_capacity` liest `cap` aus der Ableitung, statt
sie nachzurechnen — sonst hätte die Prüfung die eigene Formel gegen die eigene Formel gehalten.

Die Zusatzkante CHRIS→DORA liegt nur in der Prüffunktion, nicht in `claim_set()`. Wäre sie
gewandert, hätten sich die dokumentierten Erwartungen verschoben, und der Nachtrag wäre ein Befund
gewesen.

## 3. Ein Befund gegen das Dokument, vor dem Lauf

`example-nucleus.md §7` verlangte vier Vouches mit `n = D = 100`. Bei `D = 100` überzeichnen ANNA
und BRUNO damit beide um das Doppelte — **das Beispiel verletzte die Budgetregel, die es
illustriert.** Gefunden hat es das Werkzeug, das die Belegung nicht raten wollte und zurückfragte.

Korrigiert auf `n = 50` je Kante, `Σ n = 100 = D`. Dazu war die Out-Degree-Tabelle in `§4.3`
schief: `min(D, C(I))` begrenzt die **Zahl** der Kanten und wird nur bei `n = 1` je Kante erreicht;
die eigentliche Schranke ist `Σ n ≤ D`.

Kein Registereintrag — kein Fork, ein Fehler in einem nicht-normativen Dokument.

## 4. Bilanz

Zum ersten Mal in dieser Sitzung hatte eine Abnahme nichts zu **korrigieren**, sondern nur etwas
zu **ergänzen**. Der Grund ist benennbar: das Dokument war vorher gerechnet und nicht beschrieben.
Wo die Zahlen aus einer Rechnung kamen, stimmten sie. Der eine Fehler — die Budgetverletzung —
stand genau an der Stelle, an der ich eine Belegung hingeschrieben hatte, weil sie sich richtig
anhörte.

Dieselbe Bauform wie die zunächst falsche Schranke in D108: behauptet statt hergeleitet, und die
eigene Prüfung bestätigte nur die eigene Annahme.

**Konsequenz — vor dem Schreiben rechnen:** Jede Zahl in einem Dokument, die aus einer Regel
folgt, wird gerechnet, bevor sie geschrieben wird — nicht danach geprüft. Das gilt für Schwellen,
Belegungen, Kapazitäten und Grenzen gleichermaßen. Der Aufwand ist eine Zeile; der Preis für das
Gegenteil war in dieser Sitzung dreimal eine Runde.

## 5. Stand

`01` bis `04` vollständig, abgenommen, gemergt. `08-scope.md` als Zweckbestimmung. 116
Registereinträge. Ein Beispielnukleus, der nicht beschrieben, sondern gerechnet ist: zwei Scopes,
vier Identitäten, echte Signaturen, zwei Epochen, ein Trust-Graph — und ein Werkzeug, das ihn bei
jedem `make test` neu erzeugt und gegen das Dokument prüft.

Der nächste Schritt ist keiner, der geschrieben wird.
