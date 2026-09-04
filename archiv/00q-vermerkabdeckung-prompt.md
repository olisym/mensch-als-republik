# 00q — Abdeckung der zwei Vermerkslagen aus D207

## 1. Branch und Basis

Branch `00q` von `cc29a2d`. Ein Commit, kein Merge.

## 2. Normative Grundlage

`04-governance.md §4.1`, Tabelle unter „Zwei Vermerke, weil die Diagnose verschieden ist": die
Zeile „ein zitierter Eintrag ist überhaupt keine `claim_id`" liefert `UNSUPPORTED_RATIFICATION`.
Der Absatz darunter hält fest, dass das Subjekt die `claim_id` des `ratify@1` ist, weil die
Zeugenliste ein Feld ist und keine eigene Adresse hat.

`03-profiles.md §2.4.4`, Tabelle unter „Fünf Lagen, drei Vermerke": die Zeile
„`accusation.J.tag` ist weder `identity` noch `claim-ref`" liefert `UNRESOLVED_ACCUSED`. Der Absatz
darunter hält fest, dass das Subjekt die `claim_id` der Anklage ist.

`07-decisions.md` D207. Beide Zeilen wurden dort aus einer Messung eingetragen: die Lagen treten im
Produktivcode auf und standen in keiner Tabelle.

## 3. Auftrag

Zwei Prüffälle. **Kein Produktivcode wird angefasst.** Beide Lagen verhalten sich heute richtig;
was fehlt, ist Abdeckung.

### PF-1 — `tests/governance/test_vermerk_subjekte.py`

Die Welt, Feld für Feld gemessen:

- `alice, bob, _c, _d = fresh_p1()`
- `ja = vote(alice, PROPOSAL_1, choice=1, t=1)`
- `nein = vote(bob, PROPOSAL_1, choice=0, t=1)`
- `store = store_with(ja, nein)`, dann `tally = _tally(store)`
- `ratify = ratify_claim(alice, PROPOSAL_1, witnesses=[claim_id(nein), 42], t=10)`, danach
  `store.add(ratify)`
- `verify_ratification(store, ratify=ratify, epoch=EPOCH_1, proposal=PROPOSAL_1, tally=tally,
  target_constitution_obj=C2, now=NOW, policy=policy_of(C1))`

Gemessen an dieser Welt: `tally.state` ist `TallyState.PENDING`, `tally.findings` ist leer, und
`claim_id(nein)` steht nicht in `tally.yes`. Der Eintrag `42` ist Absicht — er ist die Lage aus der
neuen Tabellenzeile.

Der Test sichert seine eigene Voraussetzung ab: `assert tally.findings == ()`, damit die
Vermerkserwartung nicht stillschweigend von einer leeren Auszählung abhängt.

Erwartet: `next_epoch` ist `None`, und die Vermerke sind **zwei** `UNSUPPORTED_RATIFICATION`, eines
mit `claim_id(nein)` und eines mit `claim_id(ratify)`. Die Erwartung wird über `dedupe_sort` aus
diesen beiden Findings **abgeleitet**, nicht in Reihenfolge getippt; die Sortierung hängt an den
Hashes und darf nicht als Konstante im Test stehen.

Damit deckt PF-1 zugleich den Fall ab, dass beide Adressgenauigkeiten desselben Vermerks in einer
Menge liegen — der zitierte Claim und der Träger, dessen Feld defekt ist.

### PF-2 — `tests/profiles/test_vermerk_subjekte.py` (neue Datei)

Die Datei entsteht neu, parallel benannt zur bestehenden unter `tests/governance/`. Die
Anker-Datei `tests/profiles/test_verdict.py` wird nicht angefasst; PF-2 ist kein `VS`-Anker.

Die Welt, Feld für Feld gemessen:

- `alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()`
- `acc = alice.claim(p=nuc(N_B, "accusation"), J=(3, bytes(32)), t=1, N=N_B)`
- `sub_a = alice.claim(p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=2, N=N_B)`
- `sub_b = bob.claim(p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=3, N=N_B)`
- `verdict = carol.claim(p=nuc(N_B, "verdict"), J=(2, claim_id(acc)), t=4, N=N_B)`
- `verdict_status(store_with(acc, sub_a, sub_b, verdict), verdict=verdict, scope=N_B,
  arbitrators=ARBITRATORS, now=NOW)` mit `ARBITRATORS = frozenset({ALICE.pub, BOB.pub})`

Der Tag `3` in `acc.J` ist die Lage aus der neuen Tabellenzeile: weder `identity` noch `claim-ref`.

Erwartet: Status `ATTRIBUTED_OPINION` und **genau ein** Vermerk, `UNRESOLVED_ACCUSED` mit
`claim_id(acc)`.

## 4. Ausdrücklich nicht in diesem Schritt

- **Kein Produktivcode.** Weder in `mensch_als_republik/governance/epoch.py` noch in
  `mensch_als_republik/profiles/verdict.py` noch sonstwo.
- **Keine neuen `kind`-Werte, kein optionales `subject`, kein Rollenfeld.** D207 hat alle drei
  Varianten gebaut, gemessen und verworfen. Wer sie hier wieder vorschlägt, meldet es, statt sie zu
  bauen.
- **`dedupe_sort` wird nicht angefasst.** Der offene Punkt aus D183 bleibt geschlossen.
- **Die Annotation `witnesses: list[bytes]` in `tests/governance/fixtures.py` bleibt.** Der
  Nicht-Bytes-Eintrag in PF-1 ist der Prüfgegenstand. Sie wird nicht auf `list[object]` erweitert
  und der Aufruf nicht per `cast` geglättet.
- **Kein neuer `VS`-Anker** in `03-golden-anchors.md §9`, keine Änderung an bestehenden Ankern.
- Keine weiteren Vermerkspfade, auch wenn beim Bauen auffällt, dass es sie gibt. Melden.

## 5. Abnahmekriterien

- Testzahl steigt von **587** auf **589**. Keine bestehende Erwartung ändert sich.
- `make check` grün: `check_tree`, `check_specs`, `ruff check` ohne Fund, volle Reihe.
- `git diff --numstat` zeigt genau zwei Dateien: `tests/governance/test_vermerk_subjekte.py`
  (Zuwachs) und `tests/profiles/test_vermerk_subjekte.py` (neu). Neue Datei vor `make check` mit
  explizitem Pfad adden, nie `-A`.

## 6. Zwei Rücknahmeproben

Zwei Prüffälle, zwei Proben. Jede wird einzeln gefahren und danach zurückgenommen.

**Probe A.** In `verify_ratification` den Zweig für den Nicht-Bytes-Eintrag auf ein blosses
`continue` reduzieren, also den Vermerk nicht mehr anlegen. Erwartet: **PF-1 rot, alle übrigen
grün.** Gemessen wurde bereits, dass diese Umstellung ohne PF-1 folgenlos bleibt — die Reihe lief
mit ihr durch, 587 grün. Genau das ist der Grund für diesen Lauf.

**Probe B.** In `verdict_status` im `else`-Zweig `subject=claim_id(accusation)` auf `bytes(32)`
setzen. Erwartet: **PF-2 rot, alle übrigen grün.** Auch diese Umstellung lief ohne PF-2 folgenlos
durch, 587 grün.

Beide Proben belegen Abdeckung, nicht den Ort einer Prüfung; Prüfregel 34 ist hier nicht berührt,
weil kein Ort behauptet wird.

Wird eine Probe **nicht** rot, ist das ein Befund und wird gemeldet, nicht durch Nachziehen des
Tests geheilt.

## 7. Abschluss

Ein Commit auf `00q`, kein Merge, kein Push. Zurück kommen: der Commit-Hash, `git diff --numstat`,
die Testzahl und je Probe die Rotmenge. Weicht eine Messung von diesem Prompt ab, wird die
Abweichung gemeldet und nicht angeglichen.

## 8. Rückfragen

Jede Frage, deren Antwort nicht in `04-governance.md §4.1`, `03-profiles.md §2.4.4` oder D207
steht, ist ein Kandidat für eine Spec-Lücke und geht zurück ins Spec-Gespräch.
