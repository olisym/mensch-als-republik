# Lauf 00m — Bedingung 6: die Zielverfassung muss regieren können

## Branch und Basis

```
git switch -c impl/00m-regierbarkeit
set BASIS (git rev-parse HEAD)
echo $BASIS
```

`$BASIS` ist der Vergleichspunkt für alle Zahlen in der Abnahme. Der Wert wird im Bericht
genannt.

## Normative Grundlage

- `04-governance.md §4.1`, **Bedingung 6** und der Prosablock dazu. Der Text ist im Basis-Commit
  vorhanden; er ist die Wahrheit, nicht dieser Prompt.
- `04-governance.md §3.5`, Abschnitt „Dann der Inhalt" — dieselben vier Lagen, dort an der
  Verfassung der Epoche gemessen.
- `07-decisions.md`, **D200**. Insbesondere die Absätze „Ein Helfer, nicht zwei Fassungen" und
  „Nebenbefund, mit erledigt".
- **D198** für die Subjektregel: das Subjekt benennt das zurückgewiesene Objekt.

## Auftrag

### 1. Helfer `constitution_governable`

Neu in `mensch_als_republik/governance/tally.py`, oberhalb von `decide`:

```
def constitution_governable(obj: dict) -> GovernanceFinding | None
```

Gibt die Vermerksart zurück, wenn `obj` keine Auszählung tragen kann, sonst `None`. Die
Prüfreihenfolge ist **normativ** und steht in `04 §3.5`:

1. `participants` nicht deklariert  ->  `PARTICIPANTS_UNDECLARED`
2. `participants` formwidrig — kein Array, leer, Eintrag nicht 32 Byte, Duplikat, unsortiert
   ->  `MALFORMED_PARTICIPANTS`
3. `irrevocable_predicates` fehlt, ist kein Array oder führt `vote@1` nicht  ->  `VOTE_REVOCABLE`
4. `irrevocable_predicates` führt `ratify@1` nicht  ->  `RATIFY_REVOCABLE`

Die Prüfungen sind die, die heute in `decide` inline stehen. Sie werden **verschoben**, nicht neu
erfunden; das Verhalten von `decide` darf sich nicht ändern.

### 2. `decide` benutzt den Helfer

Der Inline-Block in `decide`, der `participants` und `irrevocable_predicates` der
**Epochenverfassung** prüft, wird durch einen Aufruf des Helfers ersetzt. Subjekt bleibt
`epoch.constitution_hash`. Die spätere Zeile `participants = frozenset(ordered)` wird auf
`constitution_obj["participants"]` umgestellt, weil `ordered` mit dem Block entfällt.

Keine weitere Änderung an `decide`. Reihenfolge, Vermerksarten und Subjekte bleiben, wie sie sind.

### 3. Bedingung 6 in `verify_ratification`

In `mensch_als_republik/governance/epoch.py`:

- Neuer **erforderlicher** keyword-Parameter `target_constitution_obj: dict | None`, eingefügt
  zwischen `tally` und `now`. Kein Vorgabewert — ein Aufrufer, der das Objekt nicht reichen kann,
  kann über den Übergang nicht entscheiden.
- Unmittelbar **vor** der Konstruktion der Folgeepoche, also nach allen Bedingungen 1 bis 5, in
  dieser Reihenfolge:
  1. Ist `target_constitution_obj` `None` oder weicht `constitution_hash(...)` von
     `proposal.constitution_hash` ab: **`ValueError`**. Ein fehlzugeordnetes Objekt ist ein
     Aufruferfehler, wie in Bedingung 0.
  2. Liefert `constitution_governable(target_constitution_obj)` eine Art: Rückgabe
     `RatificationResult(next_epoch=None, findings=dedupe_sort([Finding(kind=..., subject=
     proposal.constitution_hash)]))`.

Kein neuer Eintrag in `GovernanceFinding`. Die vier Arten sind vorhanden.

### 4. Aufrufer reichen durch

Fünf Dateien rufen `verify_ratification` auf und bekommen das Zielobjekt gereicht:

- `mensch_als_republik/governance/chain.py` — in `resolve_epoch` ist es die lokale Variable
  `target`.
- `tests/governance/test_vectors.py`
- `tests/governance/test_invariants.py`
- `tools/example_nucleus.py` — `ex.constitution_2`
- `tools/sim/szenario.py` — `ctx.ex.constitution_2`

In den beiden Testdateien wird das Zielobjekt aus dem gereichten `proposal` abgeleitet, nicht
geraten: es ist dasjenige Verfassungsobjekt aus `tests/governance/fixtures.py`, dessen
`constitution_hash` gleich `proposal.constitution_hash` ist. Sollte eine Aufrufstelle sich so
nicht auflösen lassen, **melden statt raten**.

### 5. Prüffälle

**Neue Datei `tests/governance/test_regierbarkeit.py`**, fünf Fälle. Die Welt ist in allen fünf
dieselbe und wird lokal gebaut:

- ein `Proposal` mit `scope = EPOCH_1.scope`, `predecessor = EPOCH_1.epoch_id`,
  `constitution_hash = constitution_hash(ziel)`,
- **alle vier** Mitglieder aus `P1` stimmen mit `choice=1` — mit dreien bleibt die Auszählung in
  den beiden `irrevocable_predicates`-Fällen `PENDING`, weil dort die Klasse `amendment` gilt,
- die Auszählung über `_tally(store, proposal=..., constitution=C1, target=ziel)`,
- ein `ratify_claim` von `alice` mit allen vier Stimmen als Zeugen.

Jeder der ersten vier Fälle prüft:

```
tally.state is TallyState.PASSED
result.next_epoch is None
len(result.findings) == 1
result.findings[0].kind == <erwartete Art>
result.findings[0].subject == proposal.constitution_hash
result.findings[0].subject != EPOCH_1.constitution_hash
```

Die vier Ziele, jeweils aus `C2` abgeleitet:

- `test_target_without_participants` — Ziel ist `C2` ohne `participants`.
  Erwartet `PARTICIPANTS_UNDECLARED`.
- `test_target_with_malformed_participants` — Ziel ist `C2` mit absteigend sortierten
  `participants`. Erwartet `MALFORMED_PARTICIPANTS`.
- `test_target_with_revocable_vote` — Ziel ist `C2` ohne `vote@1` in `irrevocable_predicates`.
  Erwartet `VOTE_REVOCABLE`.
- `test_target_with_revocable_ratify` — Ziel ist `C2` ohne `ratify@1` in
  `irrevocable_predicates`. Erwartet `RATIFY_REVOCABLE`.

Fünfter Fall `test_mismatched_target_object_raises`: dieselbe Welt mit `ziel = C2`, Auszählung
`PASSED`, und `verify_ratification` mit `target_constitution_obj=C1` wirft `ValueError`.

**In `tests/governance/test_vermerk_subjekte.py`** ein Fall
`test_participants_undeclared_addresses_epoch_constitution`: Epochenverfassung ist `C2` ohne
`participants`, Ziel ist `C3`. Erwartet `UNEVALUABLE`, genau ein Vermerk,
`PARTICIPANTS_UNDECLARED`, Subjekt `epoch.constitution_hash` und **nicht**
`proposal.constitution_hash`. Dieser Fall schließt die Lücke aus dem Nebenbefund in D200.

**In `tests/test_kettenwelt.py`** wird `test_kettenwelt_unusable_middle_constitution_governs`
umbenannt in `test_kettenwelt_unusable_middle_constitution_blocks_chain` und umgeschrieben. Die
Kette hält jetzt bei Epoche 1:

```
state.epoch == welt.epochen[0]
state.constitution_obj == welt.verfassungen[0]
state.authorized_keys == frozenset(welt.genesis_obj[1])
state.policy_findings == ()
state.key_findings == ()
state.epoch_findings == dedupe_sort([Finding(PARTICIPANTS_UNDECLARED, welt.verfassungs_hashes[1])])
```

Der Vermerk `TALLY_UNEVALUABLE` entfällt — die Auszählung war auswertbar. Die lokale Variable für
den zweiten `ratify` wird nicht mehr gebraucht und fällt weg.

## Nicht-Ziele

Was hier nicht steht, wird **gemeldet, nicht gebaut**.

- **Keine Prüfung der `thresholds` der Zielverfassung** über das hinaus, was `§3.5` heute tut. Die
  vollständige Regierbarkeit inklusive beider erreichbarer Schwellenklassen ist in D200
  ausdrücklich offen gelassen.
- **Keine Signaturprüfung der Zielverfassung.** In D200 benannt und aus benanntem Grund abgelehnt.
- **Kein neuer Eintrag** in `GovernanceFinding`.
- **Keine Änderung an `resolve_state` oder `NucleusState`.**
- **Keine Zusammenführung der vier `Finding`-Klassen** oder der vier `dedupe_sort` (D183).
- **Keine Änderung an `pyproject.toml`**, kein Zuschalten weiterer `ruff`-Gruppen (D182).
- **Keine Änderung an Spec-Dateien.** `04-governance.md`, `07-decisions.md` und `pruefregeln.md`
  liegen im Basis-Commit fertig vor.

## Abnahmekriterien

1. `make check` grün.
2. Testzahl **582**, gemessen mit `.venv/bin/python -m pytest -q`. Basis sind 576.
3. `git diff --numstat $BASIS` nennt **genau zehn** Dateien:
   `mensch_als_republik/governance/tally.py`, `mensch_als_republik/governance/epoch.py`,
   `mensch_als_republik/governance/chain.py`, `tests/governance/test_vectors.py`,
   `tests/governance/test_invariants.py`, `tests/governance/test_vermerk_subjekte.py`,
   `tests/governance/test_regierbarkeit.py`, `tests/test_kettenwelt.py`,
   `tools/example_nucleus.py`, `tools/sim/szenario.py`.
4. Vier Rücknahmeproben, jede einzeln gefahren und danach zurückgenommen. Die Rotmengen sind
   **vorher** festgelegt; eine Abweichung wird gemeldet, nicht angepasst.

**Probe A** — den Regierbarkeitsblock in `verify_ratification` entfernen, den
ValueError-Wächter stehen lassen. Erwartet rot, **fünf**: die vier `test_target_*` aus
`test_regierbarkeit.py` und `test_kettenwelt_unusable_middle_constitution_blocks_chain`.
`test_mismatched_target_object_raises` bleibt grün.

**Probe B** — nur den ValueError-Wächter entfernen. Erwartet rot, **einer**:
`test_mismatched_target_object_raises`.

**Probe C** — das Subjekt in `verify_ratification` auf `epoch.constitution_hash` umstellen.
Erwartet rot, **fünf**: dieselben wie in Probe A.

**Probe D** — das Subjekt in `decide` auf `proposal.constitution_hash` umstellen. Erwartet rot,
**einer**: `test_participants_undeclared_addresses_epoch_constitution`.

Probe D ist die wichtigste: sie führt am Artefakt vor, dass diese Adresse vor dem Lauf von nichts
gehalten wurde.

## Abschluss

**Ein** Commit auf `impl/00m-regierbarkeit`. **Kein** Merge, **kein** Push.

Der Bericht nennt: `$BASIS`, den Commit-Hash, die Ausgabe von `git diff --numstat $BASIS`, die
Testzahl und für jede der vier Proben die tatsächlich rote Menge.

Widerspricht eine Messung diesem Prompt, wird sie **gemeldet**. Kein Wert wird nachgezogen, damit
ein Kriterium aufgeht.
