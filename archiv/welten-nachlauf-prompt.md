# Nachlauf `impl/welten` — das Budget der Existenzbehauptungen

## Branch und Basis

Branch: `impl/welten`, weiter auf demselben Branch. Basis ist der Commit, der diese Datei
einführt; er wird abgeleitet, nicht getippt:

    git log --format=%H -1 -- welten-nachlauf-prompt.md

Der Lauf `4da3304` ist abgenommen und wird nicht angefasst. Dies ist ein zweiter Commit daneben.

## Normative Grundlage

`07-decisions.md` D137 — `find` läuft mit festem Budget und festem Seed, unabhängig vom Profil.
`werkzeuge.md §4.2` — die sechs Eigenschaften; ein Lauf, der keine Verletzung findet, ist der
Befund.

## Auftrag

An genau drei Stellen wird `settings=settings()` ersetzt durch
`settings=settings(max_examples=200, derandomize=True, deadline=None)`:

- `tests/property/test_p3.py::test_p3a_finds_overcommit_violation`
- `tests/property/test_p3.py::test_p3b_finds_equivocation_passed_to_pending`
- `tests/property/test_t_exp.py::test_finds_budget_exit_via_clock`

Die drei sind die vollständige Menge der `find`-Aufrufe im Repo. Findet sich ein vierter, wird er
gemeldet und nicht mitbehandelt — er wäre eine Lücke in D137, keine Fleißaufgabe.

Die Werte stehen bewusst am Aufrufort und nicht als viertes Profil in `conftest.py`. Ein Profil
wird über `MAR_HYPOTHESIS` umgeschaltet und wäre damit wieder von außen beeinflussbar; genau das
soll hier nicht sein.

## Ausdrückliche Nicht-Ziele

- `tests/property/conftest.py` wird nicht angefasst. `schnell` und `voll` bleiben, wie sie sind.
- Kein `@given`-Test bekommt ein eigenes Budget. Nur `find`.
- Keine gefundene Welt wird als fester Vektor eingefroren. D137 begründet, warum: die Suche
  behauptet, dass der Erzeuger die Gegend erreicht, ein Vektor behauptet das nicht.
- `.hypothesis/` bleibt ungetrackt.
- `welten.py` und `test_d134.py` werden nicht angefasst.

## Abnahmekriterien

1. Kalt, mit gelöschtem `.hypothesis/`, unter `schnell`: alle drei grün. Das ist die eigentliche
   Behauptung des Laufs — vorher waren zwei davon kalt rot.

2. Kalt und unter `voll` ebenfalls grün.

3. `make check` grün, 491 Tests. Laufzeit vorher und nachher melden; vorher waren es 10,09 s.
   Steigt sie um mehr als das Doppelte, ist das ein Befund und wird gemeldet — nicht durch
   Senken des Budgets behoben.

4. Die Zahl der `find`-Aufrufe wird gegriffen, nicht geschätzt:

       grep -rn "find(" tests | grep -v "\.pyc"

   Erwartung drei, alle drei geändert.

5. `python tools/check_specs.py` sauber.

## Abschluss

Ein Commit auf `impl/welten`. Kein Merge, kein Push.

Widerspricht eine Messung dem Prompt: melden, nicht anpassen. Rückfragen gehen an den Supervisor.
