# Lauf 00n — Weitergabe der Auszählungsvermerke ohne Folgeepoche

## Branch und Basis

```
git switch -c impl/00n-vermerkweitergabe
set BASIS (git rev-parse HEAD)
echo $BASIS
```

## Normative Grundlage

- `04-governance.md §4.1`, Absätze „Entsteht keine Epoche, trägt das Ergebnis die Vermerke der
  Auszählung mit" und „Entsteht eine Epoche, werden sie nicht weitergegeben".
- `04-governance.md §4.5`, Absatz „Vermerke", in der Fassung seit D203.
- `07-decisions.md`, **D203**, besonders die Absätze „Die Grenze wird von zwei Schichten gehalten"
  und „Benannt und nicht gebaut".
- **D194** für die Form der Weitergabe: additiv, der eigene Vermerk bleibt stehen.

## Auftrag

### 1. Weitergabe auf allen Pfaden ohne Folgeepoche

In `mensch_als_republik/governance/epoch.py` hängt jedes `RatificationResult` mit
`next_epoch=None` die Vermerke der Auszählung an, additiv, vor dem `dedupe_sort`. Betroffen sind
alle fünf Rückgaben:

- `TALLY_UNEVALUABLE` bei `tally.state is UNEVALUABLE` — hat die Weitergabe bereits (D194),
  bleibt unverändert.
- `TALLY_UNEVALUABLE` bei `tally.participants is None`.
- `UNSUPPORTED_RATIFICATION` über den Helfer `_unsupported`.
- `RATIFY_WITH_EXPIRY`.
- die Zeugenvermerke (`witness_findings`).
- Bedingung 6, der Regierbarkeitsblock aus D200.

Der Helfer `_unsupported` braucht die Auszählung dafür; er bekommt sie als zweiten Parameter.

**Die tragende Rückgabe bleibt unberührt.** Etabliert der Claim eine Epoche, ist `findings` weiter
leer. Das ist die Grenze aus `§4.5` und ausdrücklich Teil des Auftrags, nicht sein Rand.

`resolve_epoch` in `chain.py` wird **nicht** angefasst.

### 2. Ein bestehender Prüffall bekommt seine Erwartung erweitert

`tests/governance/test_chain.py::test_chain_missing_proposal_2` erwartet heute einen
`EPOCH_PROPOSAL_UNAVAILABLE` und drei `UNSUPPORTED_RATIFICATION`. Dazu kommen die
`UNKNOWN_PROPOSAL`-Vermerke der Auszählung.

Die Erwartung wird **abgeleitet, nicht getippt**: es sind die `claim_id` derjenigen Claims im
Speicher der Welt, die `vote@1` sind, deren `J` auf `PROPOSAL_2.proposal_hash` zeigt und deren
Autor in `C1["participants"]` steht. Gemessen sind das vier; die fünfte Stimme auf `PROPOSAL_2`
stammt von EVE, die in `C1` nicht Teilnehmerin ist. Wird die Zahl nicht vier, **melden**.

Kein anderer bestehender Prüffall ändert sich.

### 3. Neue Prüffälle

Neue Datei `tests/governance/test_vermerkweitergabe.py`, vier Fälle. Die Welten entstehen aus
`tests/governance/fixtures.py`, die fremde Stimme aus einer Identität, die in `C1["participants"]`
nicht vorkommt.

**`test_pending_tally_findings_reach_unsupported_ratification`** — zwei gültige Ja von
Teilnehmern, ein Ja von der fremden Identität, alle auf `PROPOSAL_1`. Erwartet: die Auszählung
steht auf `PENDING`; der `ratify@1` zitiert die beiden gültigen und trägt nicht; das Ergebnis führt
genau zwei Vermerke, `UNSUPPORTED_RATIFICATION` mit der `claim_id` des `ratify@1` und
`NON_MEMBER_VOTE` mit der `claim_id` der fremden Stimme.

**`test_governability_block_carries_tally_findings`** — alle vier Teilnehmer stimmen mit Ja, dazu
die fremde Stimme; Zielverfassung ist `C2` ohne `participants`. Erwartet: die Auszählung steht auf
`PASSED`; das Ergebnis führt genau zwei Vermerke, `PARTICIPANTS_UNDECLARED` mit
`proposal.constitution_hash` und `NON_MEMBER_VOTE` mit der `claim_id` der fremden Stimme.

**`test_carried_ratification_drops_tally_findings`** — alle vier Teilnehmer stimmen mit Ja, dazu
die fremde Stimme, Zielverfassung ist `C2`. Erwartet: die Auszählung steht auf `PASSED` und führt
genau den einen `NON_MEMBER_VOTE`; der `ratify@1` zitiert die vier gültigen, etabliert eine Epoche,
und `result.findings` ist **leer**. Das ist der Wächter der `§4.1`-Seite der Grenze.

**`test_carried_transition_drops_tally_findings`** — die Kettenwelt aus `tests/test_kettenwelt.py`
mit zwei Verfassungen, dazu eine Stimme der fremden Identität auf dem ersten Vorschlag, gebaut mit
dem Scope der Kettenwelt. Erwartet: `resolve_state` erreicht die zweite Epoche und
`epoch_findings` ist **leer**. Das ist der Wächter der `§4.5`-Seite derselben Grenze.

Die letzten beiden Fälle sehen ähnlich aus und sind es nicht: der eine hält `§4.1`, der andere
`§4.5`, und keiner hält den anderen (D203, Prüfregel 35). Beide sind zu bauen.

## Nicht-Ziele

Was hier nicht steht, wird **gemeldet, nicht gebaut**.

- **Keine Änderung an `mensch_als_republik/governance/chain.py`.** Weder die Vermerkliste aus der
  Schleife heben noch auf dem tragenden Pfad füllen.
- **Keine Änderung an `decide`** oder an `constitution_governable`.
- **Kein neuer Eintrag** in `GovernanceFinding`.
- **Keine Prüffälle für `RATIFY_WITH_EXPIRY` und den Zeugenpfad.** Dass diese beiden die Regel
  ungeprüft tragen, ist in D203 benannt und bewusst so.
- **Keine Änderung an Spec-Dateien**; sie liegen im Basis-Commit fertig vor.
- **Keine Umbenennung** bestehender Prüffälle.

## Abnahmekriterien

1. `make check` grün.
2. Testzahl **587**, gemessen mit `.venv/bin/python -m pytest -q`. Basis sind 583.
3. `git diff --numstat $BASIS` nennt **genau drei** Dateien:
   `mensch_als_republik/governance/epoch.py`, `tests/governance/test_chain.py`,
   `tests/governance/test_vermerkweitergabe.py`.
4. Vier Rücknahmeproben, jede einzeln gefahren und danach zurückgenommen.

**Probe G** — die Weitergabe aus `_unsupported` entfernen. Erwartet rot, **genau einer**:
`test_pending_tally_findings_reach_unsupported_ratification`.

**Probe I** — die Weitergabe aus dem Regierbarkeitsblock entfernen. Erwartet rot, **genau einer**:
`test_governability_block_carries_tally_findings`.

**Probe H1** — die Weitergabe zusätzlich auf die **tragende** Rückgabe legen, also `findings=()`
durch die Vermerke der Auszählung ersetzen. Erwartet rot, **genau einer**:
`test_carried_ratification_drops_tally_findings`. Der Kettentest bleibt grün — genau das ist der
Punkt von Prüfregel 35 und darf nicht als Abweichung gemeldet werden.

**Probe H2** — die verworfene Bauform in `chain.py`: die Vermerkliste vor die `while`-Schleife
heben und auf dem tragenden Pfad mit den Vermerken der Auszählung füllen. Erwartet rot, **genau
zwei**: `test_carried_transition_drops_tally_findings` und der bestehende
`test_chain_stale_epoch_findings_absent`.

## Abschluss

**Ein** Commit auf `impl/00n-vermerkweitergabe`. **Kein** Merge, **kein** Push.

Der Bericht nennt `$BASIS`, den Commit-Hash, `git diff --numstat $BASIS`, die Testzahl und für
jede der vier Proben die tatsächlich rote Menge.

Widerspricht eine Messung diesem Prompt, wird sie **gemeldet**. Kein Wert wird nachgezogen.
