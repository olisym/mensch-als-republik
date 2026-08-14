# Korrektur-Prompt — Layer 04b

Sehr eng. Ausgangsstand `impl/04a-korrektur`, Commit `e576663`. Zwei Änderungen aus D112, sonst
nichts. Erst `git pull`, dann `04-governance.md §3.5` und `§4.1` lesen.

## 1. `proposal.scope` prüfen

`Proposal` behauptet mit drei Feldern eine Zugehörigkeit; bisher werden zwei geprüft.

In `decide()` als **allererste** Bedingung, vor der Paarprüfung, und in `verify_ratification()`
zusammen mit der bestehenden `epoch_id`/`proposal_hash`-Prüfung:

```
proposal.scope != epoch.scope   ->   ValueError
```

Kein Vermerk, kein `UNEVALUABLE`. Begründung wie D109: ein fehlzugeordnetes Objekt ist ein
Aufruferfehler.

## 2. Schwellenvalidierung vor der Umwandlung

`threshold_for()` coerciert heute mit `int(old_th[0])`, bevor `_is_ratio` läuft. Bei
`thresholds[klasse] = ["a","b"]` wirft `int("a")` einen `ValueError`, der in der `except`-Liste
von `decide()` nicht steht — der Aufruf reißt ab, statt `MALFORMED_THRESHOLD` zu liefern.

Reihenfolge umdrehen: `_is_ratio` läuft auf den **Rohwerten** beider Verfassungen, bevor
`threshold_for` sie anfasst. `threshold_for` coerciert danach nicht mehr; sie bekommt geprüfte
Integer-Paare. Die Klassenbestimmung darf vorher laufen — sie braucht die Schwelle nicht.

## 3. Tests

- `GV-46`: `proposal.scope` eines anderen Nukleus bei passendem `predecessor`. `ValueError` in
  **beiden** Funktionen, zwei Tests.
- `GV-47`: `thresholds[klasse] = ["3","4"]` und `["a","b"]`. Beide Male `MALFORMED_THRESHOLD` und
  Zustand `UNEVALUABLE`; kein `ValueError`, kein Abbruch.

Erwartete Testzahl: **über 384**.

## 4. Nichts sonst

Keine weiteren Änderungen. Drei Beobachtungen aus der Abnahme bleiben ausdrücklich **offen** und
werden in diesem Schritt nicht angefasst:

- `dedupe_sort` existiert in drei Modulen dreimal.
- Ein Ja-Vote mit `J[0] != 3` landet im `UNKNOWN_PROPOSAL`-Zweig, obwohl es auf gar keinen
  Vorschlag zeigt.
- `membership()` unterscheidet „nicht gelistet" nicht von „Liste unlesbar" — so gewollt.

## 5. Abnahme

Branch `impl/04b-korrektur`. `make check` grün in drei Blöcken, committen **vor** dem Melden,
`git add` mit expliziten Pfaden.
