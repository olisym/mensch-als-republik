# Werkzeug-Prompt: Genesis-Bindung in Layer 04 (D145)

## Branch und Basis

Branch `impl/genesis-bindung`, Basis ist der Commit, der diese Datei einführt. Ein Commit am
Ende, kein Merge.

## Normative Grundlage

- `07-decisions.md` D145 — der Beschluss und seine Begründung.
- `04-governance.md §3` — der neue Absatz „Zuerst die Bindung des Genesis an den Scope".
- `03-profiles.md §1.2` — die Präzedenz: `resolve_policy` rechnet dieselbe Bindung nach, und die
  Asymmetrie zwischen falscher Zuordnung und Teilwissen ist dort begründet.
- `04-golden-anchors.md` — die geänderten Eingangslagen von `GV-24` und `GV-29`.

## Auftrag

**1. Die Prüfung in `decide()`.** In `mensch_als_republik/governance/tally.py` prüft `decide`
unmittelbar nach `proposal.scope != epoch.scope`, dass
`SHA-256(DOM_NUC_GEN ‖ cbor_canon.encode(genesis_obj)) == epoch.scope`. Bei Abweichung
`ValueError`. Kein Vermerk, kein neuer `GovernanceFinding`, kein Eintrag in einer Befundtabelle.

Die Prüfung steht **vor** jedem Zugriff auf ein Feld des Genesis. Heute sind das
`genesis_obj.get(6)`, `genesis_obj.get(5)` und der Aufruf von `threshold_class`; die Reihenfolge
dieser drei untereinander bleibt unverändert (D112).

**2. Die zwei Golden-Anchor-Vektoren.** `tests/governance/test_vectors.py` baut für `GV-24` und
`GV-29` heute `dict(GENESIS_D)`, mutiert Key 6 bzw. Key 5 und übergibt das Ergebnis an eine
Epoche mit `N_D`. Das mutierte Genesis hat einen anderen Hash und ist nach D145 keine zulässige
Eingabe mehr.

Beide Vektoren werden so umgebaut, dass das Genesis zum Scope der Epoche gehört: eigenes
Genesis-Objekt, sein Hash über `DOM_NUC_GEN` als Scope, Epoche und Vorschlag auf diesem Scope,
Stimmen mit diesem `N`. `STOCK_GENESIS`/`STOCK_N` in `tests/governance/fixtures.py` ist diese
Bauform bereits und trägt `[6] = 1`; ob es unmittelbar verwendbar ist oder ein zweites Fixture
nötig wird, entscheidet der Aufbau der beiden Vektoren.

**Die Erwartungswerte bleiben unverändert:** `GV-24` ergibt `UNSUPPORTED_WEIGHT_MODE` und
`UNEVALUABLE`, `GV-29` ergibt `MALFORMED_THRESHOLD` und `UNEVALUABLE`. Ändert sich einer dieser
Werte, ist das kein Nachziehen, sondern ein Abbruchgrund: melden, nicht anpassen.

**3. Ein Regressionstest mit Rücknahmeprobe.** Neuer Test in `tests/governance/`, der zeigt,
was die Prüfung verhindert — nicht bloß, dass eine Ausnahme fliegt.

Aufbau: ein Genesis, das sich von `GENESIS_D` **nur** in Key 5 unterscheidet (Wert `0`,
`ordinary`, statt `2`, `amendment`), übergeben an `EPOCH_1` mit `scope = N_D` und einem Vorschlag,
der eine Verfassungsänderung jenseits von `participants` trägt — `PROPOSAL_AMEND_E1` ist einer.
Dazu so viele aktive Ja-Stimmen, dass die `ordinary`-Schwelle überschritten und die
`amendment`-Schwelle verfehlt ist.

**Die Stimmenzahl wird abgeleitet, nicht getippt:** aus `len(P1)`, aus `_thresholds()` und aus
`passed()` in `tally.py`. Steht sie als Literal im Test, veraltet sie still, sobald jemand eine
Schwelle im Fixture ändert.

Erwartung des Tests: `ValueError`.

**Rücknahmeprobe.** Die Prüfung aus Auftrag 1 versuchsweise entfernen, den Test laufen lassen und
festhalten, welches Ergebnis stattdessen entsteht. Erwartet wird **nicht** nur ein roter Test,
sondern ein `TallyResult`, in dem der Vorschlag durchgeht. Entsteht stattdessen ein Vermerk, ein
`UNEVALUABLE` oder ein durchgefallener Vorschlag, trägt die Konstruktion des Vektors nicht — dann
melden und die Prüfung wieder einsetzen, nicht die Erwartung anpassen. Die Prüfung ist danach in
jedem Fall wieder an Ort und Stelle.

**4. Die Vorbedingung von `threshold_class`.** Ihr Docstring hält fest, dass sie `genesis_obj[5]`
ungeprüft liest und einen Aufrufer voraussetzt, der Bindung und Index bereits validiert hat —
so wie `decide` es tut. Nur der Docstring. Siehe Nicht-Ziele.

## Nicht-Ziele

- **Kein neuer Befundcode.** Die Zahl der `GovernanceFinding`-Werte bleibt unverändert.
- **Keine Prüfung in `threshold_class`.** Sie brächte die zweite Implementierung derselben Regel
  zurück, die D111 beseitigt hat. Nur der Docstring aus Auftrag 4.
- **`trust_params` bleibt unberührt.** Der Abgleich zwischen `trust/params.py` und `genesis[9]`
  ist ein eigener Fork und nicht Teil dieses Laufs.
- **`resolve_policy` bleibt unberührt.** Sie prüft bereits richtig.
- **Kein Umbau weiterer Vektoren.** Andere Tests als `GV-24`, `GV-29` und der neue werden nicht
  angefasst — es sei denn, sie werden rot; dann siehe unten.
- **Keine Änderung an Erwartungswerten**, in keinem Test.

## Abnahmekriterien

- `make check` grün. Die Testzahl steigt um die Zahl der neu hinzugefügten Testfunktionen und um
  nichts sonst; die Zahl vorher wird vor dem ersten Lauf festgehalten und im Bericht genannt.
- `make check-all` grün.
- `python tools/check_specs.py` grün.
- Die Rücknahmeprobe ist durchgeführt und ihr Ergebnis im Bericht wörtlich genannt: welcher
  Zustand und welches Ergebnis bei entfernter Prüfung entstanden sind.
- Gegrept und im Bericht genannt: alle Aufrufer von `decide` außerhalb der Tests
  (`tools/sim/szenario.py`, `tools/example_nucleus.py`, `tests/property/welten.py`) und ob ihr
  `genesis_obj` zum jeweiligen `epoch.scope` gehört. Falls einer nicht passt, ist das ein Befund
  und **kein** Anlass, die Prüfung abzuschwächen.

## Wenn etwas nicht aufgeht

Weitere rote Tests durch die neue Prüfung sind ein erwartbares Ergebnis, kein Fehler. Jeder wird
im Bericht **einzeln** genannt, mit der Frage, ob sein Genesis zum Scope gehört. Repariert wird
nur, was durch Anpassung der Konstruktion grün wird, ohne dass sich eine Erwartung ändert. Alles
andere wird gemeldet.

Widerspricht eine Messung diesem Prompt, gilt die Messung. Melden, nicht anpassen.
