# 00l — Untaugliche Zwischenverfassung und die Adresse eines Vermerks

## Branch und Basis

Branch `impl/00l-vermerksubjekte`, abgezweigt von `main` bei dem Commit, auf dem **dieser Prompt**
liegt. Vor der ersten Änderung festhalten, etwa `set BASIS (git rev-parse HEAD)`; `$BASIS` ist der
Vergleichspunkt für das Abnahmekriterium unten (Prüfregel 31). Ein Commit am Ende, kein Merge,
kein Push.

## Normative Grundlage

- `04-governance.md §3.5` — die Regel, dass das Subjekt das zurückgewiesene Objekt benennt, samt
  den beiden ausgeschriebenen Fällen. Sie steht bereits in der Spec; dieser Lauf zieht den Code
  nach.
- D198 — die Entscheidung dazu, mit den drei betroffenen Stellen.
- D197 — der Prüffall der untauglichen Zwischenverfassung, Feld für Feld gemessen.

## Auftrag

### 1. Drei Subjekte in `decide` nachziehen

In `mensch_als_republik/governance/tally.py`, in `decide`:

**a) Die Schwellenschleife führt den Hash des geprüften Objekts mit.** Aus

    for obj in (constitution_obj, target_constitution_obj):

wird eine Schleife über Paare aus Objekt und zugehörigem Hash:

    for obj, obj_hash in (
        (constitution_obj, epoch.constitution_hash),
        (target_constitution_obj, proposal.constitution_hash),
    ):

Beide `_unevaluable`-Ausgänge im Rumpf dieser Schleife — der für die fehlende Klasse und der für
die formwidrige Schwelle — übergeben statt `epoch.constitution_hash` nun `obj_hash`.

**b) `UNSUPPORTED_WEIGHT_MODE` adressiert den Scope.** Der Ausgang bei `genesis_obj.get(6) != 0`
übergibt `epoch.scope` statt `epoch.constitution_hash`.

**c) Das `MALFORMED_THRESHOLD` aus `genesis[5]` adressiert den Scope.** Der Ausgang bei
`type(idx) is not int or idx not in _CLASS_BY_INDEX` übergibt `epoch.scope` statt
`epoch.constitution_hash`.

Die übrigen neun Ausgänge von `_unevaluable` bleiben unverändert. Keine Änderung an
Prüfreihenfolge, Zuständen oder Vermerkarten — `04 §3.5` nennt die Reihenfolge ausdrücklich
normativ.

### 2. Neue Datei `tests/governance/test_vermerk_subjekte.py`

Drei Tests, die je genau ein Subjekt festhalten. Alle drei Welten sind gemessen. Ein lokaler
Helfer baut ein zusammengehöriges Paar aus Epoche und Vorschlag:

    def _paar(cons, ziel, *, scope=N_D, index=2):
        epoch = Epoch(
            scope=scope, index=index, constitution_hash=constitution_hash(cons)
        )
        proposal = Proposal(
            scope=scope,
            predecessor=epoch.epoch_id,
            constitution_hash=constitution_hash(ziel),
        )
        return epoch, proposal

**a) Formwidrige Schwelle in der Zielverfassung.** Die Zielverfassung ist `C2` mit einer eigenen
`thresholds`-Kopie, deren `amendment` auf `[3, 2]` steht — die geltende Verfassung ist `C2`
selbst, deren Schwelle einwandfrei ist. Der Aufruf geht über `_tally` aus
`tests/governance/fixtures.py` mit `constitution=C2`, dem Zielobjekt als `target`, dem Paar aus
`_paar` und `known={proposal.proposal_hash: proposal}`.

Zugesichert: `result.state is TallyState.UNEVALUABLE`, genau ein Vermerk, seine Art ist
`MALFORMED_THRESHOLD`, sein Subjekt ist `proposal.constitution_hash` — und ausdrücklich **nicht**
`epoch.constitution_hash`. Beide Zusicherungen werden geschrieben; die zweite ist der eigentliche
Gegenstand des Tests und war vor diesem Lauf falsch.

**b) `genesis[6] = 1`.** Eine Kopie von `GENESIS_D` mit `6: 1`, der Scope daraus neu gerechnet als
`sha256(DOM_NUC_GEN + cbor(genesis))`, Epoche und Vorschlag über `_paar` auf diesem Scope,
`constitution=C2`, `target=C3`, `genesis` die Kopie.

Zugesichert: `UNEVALUABLE`, genau ein Vermerk der Art `UNSUPPORTED_WEIGHT_MODE`, Subjekt
`epoch.scope`.

**c) `genesis[5] = 3`.** Wie b), nur mit `5: 3`. Zugesichert: `UNEVALUABLE`, genau ein Vermerk der
Art `MALFORMED_THRESHOLD`, Subjekt `epoch.scope`.

Der Scope wird in b) und c) **gerechnet**, nicht getippt. Kein Hash in dieser Datei steht als
Literal.

### 3. Neuer Test in `tests/test_kettenwelt.py`

`_welt3()` bekommt einen Schlüsselwortparameter `c2_ohne_participants: bool = False`. Ist er
gesetzt, wird aus der zweiten Verfassung der Eintrag `participants` entfernt, und sonst nichts.
Der bestehende Aufruf `_welt3()` bleibt unverändert. Die Variantenwelt entsteht damit aus
demselben Bauer wie die Referenzwelt, wie es Prüfregel 30 verlangt.

Neuer Test `test_kettenwelt_unusable_middle_constitution_governs`. Er baut
`_welt3(c2_ohne_participants=True)` und ruft `resolve_state` mit den unveränderten Feldern der
Welt auf — `known_constitutions` wird hier **nicht** beschnitten, alle drei Verfassungen sind
bekannt.

Zugesichert, alles gemessen:

- `state.epoch == welt.epochen[1]`
- `state.constitution_obj == welt.verfassungen[1]`
- `state.authorized_keys == frozenset(welt.verfassungen[1]["nucleus_keys"])`
- `state.policy_findings == ()`
- `state.key_findings == ()`
- `state.epoch_findings` gleicht `dedupe_sort` über genau zwei Einträge:
  `Finding(GovernanceFinding.PARTICIPANTS_UNDECLARED, welt.verfassungs_hashes[1])`
  und `Finding(GovernanceFinding.TALLY_UNEVALUABLE, claim_id(zweiter_ratify))`

`zweiter_ratify` wird aus dem Speicher abgeleitet: der Claim, für den `is_nuc_name(claim,
"ratify")` gilt und dessen `J` gleich `(3, welt.vorschlaege[1].proposal_hash)` ist. Beachte den
Index **1** — es ist der zweite Übergang, nicht der erste.

Der Docstring nennt D197 und hält fest, was der Test zeigt: die Kette rückt in die untaugliche
Verfassung ein, und diese regiert.

## Ausdrückliche Nicht-Ziele

- **`decide` prüft die Zielverfassung nicht auf Inhalt.** Dass eine Verfassung ohne
  `participants` ein zulässiges Übergangsziel ist, wird in diesem Lauf **nicht** geändert. D197
  hält diese Frage als benannten Fork offen; der neue Test hält den heutigen Zustand fest.
- **Keine Änderung an den bestehenden Vektortests.** `test_GV_24`, `test_GV_29` und `test_GV_47`
  prüfen die Art des Vermerks und spiegeln damit `04-golden-anchors.md`. Sie bekommen **keine**
  Subjektzusicherung; die Anker nennen kein Subjekt, und ein Test soll seinen Anker nicht
  überholen.
- **Keine Änderung an Prüfreihenfolge, Zuständen oder Vermerkarten** in `decide`.
- **Keine Änderung an den neun übrigen `_unevaluable`-Ausgängen.**
- **`_welt()` und der bestehende Test aus `_welt3()` werden nicht angefasst.**
- **Keine Änderung an einer Spec-Datei.** `04 §3.5` trägt die Regel bereits.
- **Kein neuer Helfer in `tests/governance/fixtures.py`.** `_paar` steht lokal in der neuen
  Testdatei.

## Rücknahmeproben

Drei Proben, alle drei gefahren, alle drei gemeldet. Der Zustand wird danach wiederhergestellt.

**Probe A — die Schwellenschleife.** Aufgabe 1a zurücknehmen, also wieder
`epoch.constitution_hash` in beiden Ausgängen der Schleife. Erwartet wird **genau ein** roter
Test: der aus 2a.

**Probe B — die beiden Genesis-Subjekte.** Aufgaben 1b und 1c zurücknehmen. Erwartet werden
**genau zwei** rote Tests: die aus 2b und 2c.

**Probe C — die Welt des Kettentests.** Im neuen Test aus Aufgabe 3 statt
`_welt3(c2_ohne_participants=True)` schlicht `_welt3()` bauen. Erwartet wird **genau ein** roter
Test, nämlich dieser.

Dass die Proben A und B jeweils nur die neuen Tests treffen und keinen der bestehenden, ist kein
Nebenbefund, sondern der Zweck: er zeigt, dass die Subjekte vor diesem Lauf von nichts gehalten
wurden. Trifft eine Probe zusätzlich einen bestehenden Test, ist das zu melden und nicht zu
beheben.

## Abnahmekriterien

- `make check` ist grün. Die neue Testdatei wird **vor** `make check` mit `git add` erfasst, sonst
  meldet `check_tree.py` eine unversionierte Quelldatei.
- Die Testzahl steigt von **572** auf **576**. Gemessen mit `.venv/bin/python -m pytest -q`, die
  letzte Zeile wird gemeldet.
- `git diff --numstat $BASIS` nennt **genau drei** Dateien:
  `mensch_als_republik/governance/tally.py`, `tests/governance/test_vermerk_subjekte.py`,
  `tests/test_kettenwelt.py`.
- Alle drei Proben sind gefahren und ihr Ergebnis ist mit den Namen der roten Tests genannt.

## Abschluss

Ein Commit auf `impl/00l-vermerksubjekte`. Kein Merge, kein Push. Gemeldet werden: der
Commit-Hash, die letzte Zeile des Testlaufs, `git diff --numstat $BASIS` und das Ergebnis der drei
Proben.

Widerspricht eine Messung diesem Prompt, wird sie **gemeldet, nicht angepasst**. Erwartete Werte
werden nicht nachgezogen, um einen Test grün zu bekommen.
