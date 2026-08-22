# 00k — Die Auszählung sagt, was fehlt, und die Ratifizierung gibt es weiter

## Branch und Basis

Branch `impl/00k-vermerkweitergabe`, abgezweigt von `main` bei `32c55c9`
(`register: D192–D195, Prüfregel 30`). Ein Commit am Ende, kein Merge, kein Push.

## Normative Grundlage

- `04-governance.md §4.1` — die beiden Vermerke der Ratifizierung und ihre Begründung: im einen
  Fall weiß der Beobachter, welche `claim_id` er holen muss, im anderen weiß er, dass Holen nichts
  nützt.
- D194 — die Entscheidung, die hier gebaut wird: die Vermerke der Auszählung werden zusätzlich
  weitergegeben, der grobe Vermerk bleibt unverändert stehen.
- D195 — die Prüfwelt für den neuen Test, Feld für Feld gemessen.
- D193 — die Berichtigung der Vorbedingung im Kettenbauer.

## Auftrag

### 1. Weitergabe in `verify_ratification`

In `mensch_als_republik/governance/epoch.py`, im Zweig `if tally.state is
TallyState.UNEVALUABLE:`, werden die Vermerke der Auszählung zusätzlich in das Ergebnis
aufgenommen. Aus der bisherigen Liste mit dem einen Eintrag
`Finding(kind=GovernanceFinding.TALLY_UNEVALUABLE, subject=claim_id(ratify))` wird dieselbe Liste,
gefolgt von `*tally.findings`. `dedupe_sort` bleibt wie es ist und ordnet.

Unverändert bleiben: der Vermerk `TALLY_UNEVALUABLE` selbst, `next_epoch=None`, der darunter
folgende Zweig `if tally.participants is None:` und jede andere Stelle der Datei.

### 2. `tests/governance/test_chain.py` nachziehen

Zwei Tests vergleichen exakt und bekommen je einen Vermerk mehr. Der Zusatz wird **abgeleitet**,
nicht getippt — beide Hashes stehen bereits als Feld der jeweiligen Vorschlagsfixture zur
Verfügung:

- `test_chain_missing_c3_stops_at_epoch_2`: zusätzlich
  `Finding(GovernanceFinding.PROPOSAL_CONSTITUTION_UNAVAILABLE, PROPOSAL_2.constitution_hash)`
- `test_chain_miskeyed_c3_stops_at_epoch_1`: zusätzlich
  `Finding(GovernanceFinding.PROPOSAL_CONSTITUTION_UNAVAILABLE, PROPOSAL_1.constitution_hash)`

Beide Einträge kommen in die Liste, die an `dedupe_sort` übergeben wird. Die Reihenfolge wird
nicht von Hand gesetzt; das ist die Aufgabe von `dedupe_sort`.

### 3. `tests/test_resolve.py` nachziehen

In `test_resolve_state_missing_c1_keeps_findings_separate` behauptet die letzte Zusicherung eine
**Position** in einer sortierten Folge:

    assert state.epoch_findings != ()
    assert (
        state.epoch_findings[0].kind
        == governance_findings.GovernanceFinding.TALLY_UNEVALUABLE
    )

Beide Zeilenblöcke werden ersetzt durch eine Zusicherung über die Menge der Vermerkarten:

    assert {f.kind for f in state.epoch_findings} == {
        governance_findings.GovernanceFinding.TALLY_UNEVALUABLE,
        governance_findings.GovernanceFinding.CONSTITUTION_UNAVAILABLE,
    }

Die Zeile `assert state.epoch_findings != ()` entfällt dabei: eine Menge mit zwei Elementen kann
nicht leer sein, die Zusicherung ist enthalten. Die übrigen Zusicherungen des Tests bleiben
unangetastet, insbesondere die beiden über `policy_findings` und `key_findings` — sie sind der
eigentliche Gegenstand des Tests.

### 4. Docstring von `kettenwelt()` berichtigen

In `tests/kettenwelt.py` steht im Docstring von `kettenwelt()` die Zusage:

    ``identitaeten[0]`` signiert jedes ``propose`` und jedes ``ratify`` und muss unter
    der jeweils geltenden Epoche autorisiert sein; sonst rückt die Kette nicht vor.

Sie ist gemessen falsch (D193). Ersetzen durch:

    ``identitaeten[0]`` signiert jedes ``propose`` und jedes ``ratify`` und muss
    Teilnehmer der jeweils geltenden Verfassung sein, also in ``participants`` stehen;
    sonst rückt die Kette nicht vor. Autorisiert im Sinne von ``authorized_keys`` muss
    der Autor nicht sein (D193).

### 5. Neuer Test in `tests/test_kettenwelt.py`

Neben `_welt()` — nicht an dessen Stelle — entsteht ein Helfer `_welt3()`, der dieselbe Form mit
drei Verfassungen baut. Die Welt ist Feld für Feld die gemessene:

    def _welt3() -> tuple[Kettenwelt, Identity, Identity, Identity]:
        a = Identity("A")
        b = Identity("B")
        c = Identity("C")
        people = sorted([a.pub, b.pub, c.pub])
        schwellen = {
            "ordinary": [1, 2],
            "membership": [1, 2],
            "amendment": [1, 2],
        }
        basis = {
            "irrevocable_predicates": ["obligation@1", "ratify@1", "vote@1"],
            "thresholds": schwellen,
            "arbitration": {"arbitrators": people},
            "participants": people,
        }
        erste = dict(basis)
        zweite = dict(basis)
        zweite["nucleus_keys"] = [b.pub]
        dritte = dict(basis)
        dritte["nucleus_keys"] = [c.pub]
        welt = kettenwelt(
            identitaeten=(a, b, c),
            root_keys=(a.pub,),
            verfassungen=(erste, zweite, dritte),
        )
        return welt, a, b, c

Der Test heißt `test_kettenwelt_missing_middle_constitution_blocks_chain`. Er entfernt aus einer
Kopie von `welt.known_constitutions` genau den Eintrag zu `welt.verfassungs_hashes[1]` und ruft
`resolve_state` mit dieser Kopie auf; `known_proposals`, `genesis_obj`, `scope` und `now` kommen
unverändert aus der Welt.

Zugesichert wird, alles gemessen:

- `state.epoch == welt.epochen[0]`
- `state.constitution_obj == welt.verfassungen[0]`
- `state.authorized_keys == frozenset(welt.genesis_obj[1])`
- `state.policy_findings == ()`
- `state.key_findings == ()`
- `state.epoch_findings` gleicht `dedupe_sort` über genau zwei Einträge:
  `Finding(GovernanceFinding.PROPOSAL_CONSTITUTION_UNAVAILABLE, welt.verfassungs_hashes[1])`
  und `Finding(GovernanceFinding.TALLY_UNEVALUABLE, claim_id(erster_ratify))`

`erster_ratify` wird **aus dem Speicher abgeleitet**, nicht getippt: der Claim aus
`welt.store.all_claims()`, für den `is_nuc_name(claim, "ratify")` gilt und dessen `J` gleich
`(3, welt.vorschlaege[0].proposal_hash)` ist. Ein getippter Hash wäre hier ein Defekt.

## Ausdrückliche Nicht-Ziele

- **Kein Eingriff in `decide`**, `resolve_epoch`, `resolve_state` oder die Kettenauflösung. Der
  Lauf ändert, welche Vermerke entstehen, und nicht, welche Epoche sich auflöst.
- **Keine Weitergabe im Zweig `tally.participants is None`.** Er ist über `decide` nicht
  erreichbar und rein defensiv; er bleibt wie er ist.
- **Keine Weitergabe im auswertbaren Fall.** Scheitert eine Ratifizierung bei Zustand `PASSED`,
  `FAILED` oder `PENDING`, bleibt es bei den heutigen Vermerken. D194 hält diese Frage
  ausdrücklich offen; sie wird hier nicht mitgenommen.
- **`_welt()` wird nicht umgebaut** und nicht verallgemeinert. `_welt3()` steht daneben.
- **`kettenwelt()` bekommt keinen Ratifizierer-Knopf.** Der Bauer bleibt in seiner Signatur, wie
  er ist; nur der Docstring wird berichtigt.
- **Keine neuen Vermerkarten**, keine Änderung an den vier `Finding`-Klassen und ihren
  `dedupe_sort` (D183).
- **Keine Änderung an `04-governance.md`** oder einer anderen Spec-Datei in diesem Lauf.

## Rücknahmeproben

Beide Proben werden gefahren, ihr Ergebnis wird gemeldet, und der Zustand wird danach
wiederhergestellt. Eine Probe, die nicht rot wird, ist ein Befund und kein Grund, den Test zu
ändern.

**Probe A — die Weitergabe.** Aufgabe 1 zurücknehmen, also `*tally.findings` wieder entfernen,
und die volle Testreihe fahren. Erwartet werden **genau vier** rote Tests, und zwar:

- `tests/test_kettenwelt.py::test_kettenwelt_missing_middle_constitution_blocks_chain`
- `tests/governance/test_chain.py::test_chain_missing_c3_stops_at_epoch_2`
- `tests/governance/test_chain.py::test_chain_miskeyed_c3_stops_at_epoch_1`
- `tests/test_resolve.py::test_resolve_state_missing_c1_keeps_findings_separate`

Wird ein fünfter Test rot oder bleibt einer der vier grün, ist das zu melden und nicht zu
beheben.

**Probe B — die Welt des neuen Tests.** Im neuen Test die Zeile weglassen, die den Eintrag zu
`welt.verfassungs_hashes[1]` aus der Kopie entfernt, sodass alle drei Verfassungen bekannt sind.
Erwartet wird **genau ein** roter Test, nämlich der neue. Diese Probe zeigt, dass der Test die
Abwesenheit der Verfassung sieht und nicht eine Aussage, die in jeder Welt gilt.

## Abnahmekriterien

- `make check` ist grün.
- Die Testzahl steigt von **571** auf **572**. Gemessen mit `.venv/bin/python -m pytest -q`, die
  letzte Zeile wird gemeldet.
- `git diff --numstat` gegen `32c55c9` nennt **genau fünf** Dateien:
  `mensch_als_republik/governance/epoch.py`, `tests/governance/test_chain.py`,
  `tests/test_resolve.py`, `tests/kettenwelt.py`, `tests/test_kettenwelt.py`.
- Beide Proben sind gefahren und ihr Ergebnis ist im Bericht genannt, mit den Namen der roten
  Tests.

## Abschluss

Ein Commit auf `impl/00k-vermerkweitergabe`. Kein Merge, kein Push. Gemeldet werden: der
Commit-Hash, die letzte Zeile des Testlaufs, die Ausgabe von `git diff --numstat` gegen `32c55c9`
und das Ergebnis beider Proben.

Widerspricht eine Messung diesem Prompt, wird sie **gemeldet, nicht angepasst**. Erwartete Werte
werden nicht nachgezogen, um einen Test grün zu bekommen.
