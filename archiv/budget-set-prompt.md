# Prompt: Budget-Set (D135)

Branch: `impl/budget-set` von `spec/d133-d134` (`354506f`).

Normative Grundlage: `07-decisions.md` D135, `02 §3.1`, `02 §8`, `02a §2.6`.

Rückfragen gehen an den Supervisor, nicht ins eigene Fenster.

## 1. Produktivcode — drei Zeilen

`mensch_als_republik/trust/groups.py`:

```python
BUDGET_STATES = frozenset(
    {State.ACTIVE, State.REVOKED, State.SUPERSEDED, State.PENDING}
)
```

wird um `State.EQUIVOCATION_FLAGGED` erweitert.

**Der Docstring von `_in_budget_set` wird mitgezogen.** Er zählt die vier Zustände heute im Text
auf und zitiert `02a §2.6`. Bleibt er stehen, steht der reparierte Code neben seiner eigenen
Widerlegung — genau die Lage, die D135 überhaupt erst erzeugt hat. Der neue Text nennt fünf
Zustände und den Grund: Equivocation ist kein Lebenszyklus-Akt, und der
Über-Commitment-Beweis beruht auf Signaturen, nicht auf Aktivität.

Sonst nichts. `derive.py` bleibt unangetastet — Schritt 4 rechnet bereits richtig, sobald die
Gruppen da sind.

## 2. Die umgedrehte Erwartung

`tests/trust/test_vouch_without_texp.py::test_no_vouch_without_texp_on_flagged_author` behauptet,
ein geflaggter Vouch ohne `t_exp` erzeuge kein `VOUCH_WITHOUT_TEXP`. Das folgt aus der alten
Whitelist und aus nichts sonst.

Unter D135 bindet dieser Vouch Budget dauerhaft — genau die Lage, vor der das Finding warnt. Die
Erwartung dreht sich um: **beide** Claims des Paars stehen im Budget-Set, beide haben kein
`t_exp`, also fallen **zwei** Findings.

Die erwarteten Subjekte werden aus `claim_id(v1)` und `claim_id(v2)` gebildet, nicht getippt.

**Der Testname wird mitgeändert.** `test_no_vouch_without_texp_on_flagged_author` behauptet nach
der Umdrehung das Gegenteil dessen, was der Test prüft. Neuer Name sinngemäß
`test_vouch_without_texp_fires_on_flagged_author`. Ein Name, der die alte Regel weiterträgt, ist
eine Fußangel für den nächsten Leser — dieselbe Sorte Defekt wie in der `impl/authoring`-Abnahme.

Prüfen, ob im Testkopf ein Docstring oder Kommentar die alte Regel wiederholt; wenn ja, mit
ändern.

## 3. Der Regressionstest — der Budget-Reset als Szenario

Neue Datei `tests/trust/test_budget_equivocation.py`.

Szenario, gebaut mit dem Idiom aus der Nachbardatei — kein `Autor`, kein `gabeln`:

```
a1 = Identity("budget-reset-A")
a2 = Identity("budget-reset-A")      # gleicher Seed, gleiches I, gleiche Genesis-Spitze
bob, carol = Identity("budget-reset-B"), Identity("budget-reset-C")

v1 = a1.vouch(bob,   n=PARAMS.D, scope=scope, t=1, t_exp=T_EXP)
v2 = a2.vouch(carol, n=PARAMS.D, scope=scope, t=1, t_exp=T_EXP)
```

`t_exp=T_EXP` ist wesentlich: ohne es fiele zusätzlich `VOUCH_WITHOUT_TEXP` und die Behauptung
des Tests wäre nicht mehr scharf.

Beide Claims sind die **ersten** ihrer Kette, teilen `(I, h_prev)` und bilden ein
Equivocation-Paar. Der Test hält das ausdrücklich fest, bevor er weiterrechnet — sonst prüft er
bei einer späteren Änderung an `Identity` unbemerkt etwas anderes.

**Zwei Behauptungen, ein Szenario:**

1. **Die Summe.** `build_groups(...)` liefert zwei Gruppen, `Σ n_budget == 2 * PARAMS.D`.
2. **Die Wirkung.** `trust(..., include_flagged=True)` liefert genau ein Finding:
   `Finding(kind=TrustFinding.OVERCOMMITTED_AUTHOR, subject=a1.pub)`.

Beide sind nötig. Die Summe allein ließe eine spätere Änderung durch, die richtig summiert und das
Finding verliert; das Finding allein ließe eine durch, die aus anderem Grund feuert.

Erwartete Nebenwirkungen: keine. Beide Claims sind `EQUIVOCATION_FLAGGED`, also nicht `ACTIVE`,
also `n_kante == 0` und kein Kantensatz — `SUBGRANULAR_VOUCH` kann nicht fallen. Fällt es doch,
ist das ein Befund und wird gemeldet, nicht weggeprüft.

## 4. Ausdrücklich nicht

- **`welten.py`** bleibt unangetastet. D133 und D134 sind ein eigener Lauf und hängen von diesem
  ab, nicht umgekehrt.
- **`derive.py`**, **`flow.py`**, **`graph.py`** bleiben unangetastet.
- **Keine Golden Anchors anfassen.** Die Messung vor D135 hat gezeigt, dass sie sich nicht bewegen
  — Variante A bleibt trotz geflaggter CAROL innerhalb `D`. Wird ein Ankertest rot, ist die
  Messung falsch gewesen: **melden, nicht anpassen.**
- Kein Umbau von `test_include_flagged.py`. Die dortige `_TABLE` hält Flusswerte fest, nicht
  Budget; sie war in der Messung grün.

## 5. Abnahmekriterien

1. `make check-all` grün, zwei pytest-Endzeilen. 489 → **490**; die Eigenschaftstests bleiben
   bei 13.
2. `python -m tools.check_specs` sauber.
3. `git diff --stat` gegen den Branchpunkt zeigt genau drei Dateien: `trust/groups.py`,
   `tests/trust/test_vouch_without_texp.py`, `tests/trust/test_budget_equivocation.py`.
4. **Rücknahmeprobe.** Wird `State.EQUIVOCATION_FLAGGED` aus `BUDGET_STATES` wieder entfernt,
   müssen **beide** neuen Behauptungen aus §3 fehlschlagen — die Summe fiele auf 0, das Finding
   bliebe aus. Einmal prüfen und im Commit-Text bestätigen. Ein Regressionstest, der die
   Regression nicht sieht, ist keiner.
5. `grep -n 'ACTIVE, State.REVOKED' mensch_als_republik/trust/groups.py` und der Docstring
   darunter nennen dieselbe Menge. Code und Kommentar dürfen nicht auseinanderlaufen.

## 6. Abschluss

Ein Commit auf `impl/budget-set`. Kein Merge. Die Abnahme führt der Supervisor.

Im Commit-Text: Testzahl vorher/nachher, Ergebnis von Kriterium 4, und jede Stelle, an der die
Spec eine Frage offen gelassen hat.
