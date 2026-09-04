# Befund: Rücknahmeproben für die vierzehn markierten Pflichten

Vierzehn Neutralisierungen, je ein Lauf `.venv/bin/python -m pytest -q`. Dazwischen
`git diff --quiet`. Grundlinie 597 Tests. Kein Produktivcode bleibt geändert.

## Geteilte Stellen

N04 und N05 sind dieselbe Vergleichsstelle in `resolve_scope`: `claim.N != expected`.
Eine Neutralisierung, die nur N04 träfe, gibt es nicht. Die Messung gilt für beide;
sie steht unter N04 und wird unter N05 nicht wiederholt.

N11 hat parallele Stellen in `credit.py`, `verdict.py`, `membership.py` und
`tally.py`. Die Probe sitzt an der zuerst genannten Paarung, `receipt` gegen
`obligation` in `settlement`. Die übrigen Stellen sind unangetastet.

N14 wirft in `resolve_epoch`. Dieselbe Abweichung wirft `resolve_policy` mit
derselben Meldung, bevor ein Test die Kette unterscheiden könnte. Die Stelle
ist da; der Lauf blieb grün.

## Die vierzehn

### N01 — `akt.N` ist gesetzt und passt zum aufgelösten Scope

Stelle: `mensch_als_republik/verifier.py`, `structural_check`. Der Aufruf von
`check_scope_binding` für `nuc:`-Claims.

rot: 1

```
tests/test_verifier.py::test_bad_scope_binding_structural
```

Klasse: **geprüft**

Die Stelle ist nicht akt-spezifisch. Sie durchsetzt die Bindungsregel für jedes
`nuc:`-Prädikat am Einlesepfad (`00 §7` zitiert `01 §2.2`). Ein eigener Träger
nur für Nukleus-Akte fehlt. `resolve_scope` selbst bleibt auf diesem Pfad
unangetastet; N03 und N04 haben dort eigene Proben.

### N02 — ein Alias trifft das kanonische Muster nicht

Stelle: `mensch_als_republik/predicates.py`, die Lookaheads in `_ALIAS_SCOPE`
und `_NUC_PREDICATE`.

rot: 0. Der Lauf blieb grün.

Klasse: **ungeprüft**

`_CANONICAL_SCOPE` wird zuerst geprüft; 64-Hex läuft als kanonisch, nicht als
Alias. Der Lookahead trägt keine eigene Prüfung. Der Test
`test_alias_matching_64_hex_rejected` hängt an N04, nicht an diesem Lookahead.

### N03 — Bindungsregel: `N` ist gesetzt

Stelle: `mensch_als_republik/predicates.py`, `resolve_scope`. Die beiden
Prüfungen `claim.N is None`.

rot: 1

```
tests/test_predicates.py::test_bad_scope_binding_missing_n_on_nuc
```

Klasse: **geprüft**

Im kanonischen Zweig ist `N is None` redundant zu `N != expected` (N04). Die
Probe trifft nur den Alias-Zweig, der keine Byte-Gleichheit hat.

### N04 — `N` entspricht dem aufgelösten Scope

Stelle: `mensch_als_republik/predicates.py`, `resolve_scope`. Der Vergleich
`claim.N != expected` im kanonischen Zweig.

rot: 2

```
tests/test_predicates.py::test_bad_scope_binding_wrong_n
tests/test_predicates.py::test_alias_matching_64_hex_rejected
```

Klasse: **geprüft**

Dieselbe Stelle trägt N05.

### N05 — bei kanonischer Kodierung gilt Byte-Gleichheit

Stelle: dieselbe wie N04, `resolve_scope`, `claim.N != expected`.

rot: 2

```
tests/test_predicates.py::test_bad_scope_binding_wrong_n
tests/test_predicates.py::test_alias_matching_64_hex_rejected
```

Klasse: **geprüft**

Keine Neutralisierung, die N05 aufhöbe und N04 stünde. Gemeldet, nicht
zusammengefasst.

### N06 — der Verifizierer serialisiert neu und vergleicht byte-genau

Stelle: `mensch_als_republik/verifier.py`, `structural_check`. Der Zweig
`if not canonical: raise NonCanonicalEncoding()`.

rot: 4

```
tests/test_verifier.py::test_nv2_non_canonical_encoding
tests/test_verifier.py::test_nv2_non_canonical_encoding_read_claim
tests/test_verifier.py::test_bv_structural_check[BV3-NonCanonicalEncoding]
```

Klasse: **geprüft**

Der vierte rote Test ist
`tests/test_verifier.py::test_read_claim_reject_vectors[BV3]`.

### N07 — der Verifizierer ignoriert `t_exp` auf einem `core/*`-Claim

Stelle: `mensch_als_republik/verifier.py`, `_is_temporally_valid`. Der frühe
Rückgabewert `True` für `core/*`.

rot: 0. Der Lauf blieb grün.

Klasse: **ungeprüft**

`test_core_revoke_ignores_t_exp` klassifiziert TV3; TV3 trägt kein `t_exp`.
Ohne gesetztes `t_exp` bleibt der Default-Zweig wahr, auch wenn der
Ignore-Zweig fehlt.

### N08 — VR-02.1: die Aggregation rechnet simultan

Stelle: `mensch_als_republik/trust/flow.py`, `trust`. Ein Multi-Sink-Lauf über
`targets` statt der Summe der Einzelläufe.

rot: 21

```
tests/trust/test_anchors.py::test_individual_and_simultaneous[A]
tests/trust/test_anchors.py::test_A_prime_simultaneous_is_16_not_48
tests/trust/test_invariants.py::test_INV1_differs_for_A_simultaneous_only
```

Klasse: **geprüft**

Varianten B und E0 blieben grün: dort ist simultan gleich der Summe.

### N09 — ein Vouch trägt `t_exp`, wo die Budgetregel gilt

Stelle: `mensch_als_republik/trust/groups.py`, `build_groups`. Der Vermerk
`VOUCH_WITHOUT_TEXP`.

rot: 3

```
tests/trust/test_vouch_without_texp.py::test_vouch_without_texp_finding_fires
tests/trust/test_vouch_without_texp.py::test_vouch_without_texp_is_inert
tests/trust/test_vouch_without_texp.py::test_vouch_without_texp_fires_on_flagged_author
```

Klasse: **geprüft**

Der Vermerk ist ohne Wirkung auf den Fluss (D119). Die Probe färbt die
Behauptung des Vermerks, nicht eine Ausschlussregel.

### N10 — ein vorhandenes `v` trägt den deklarierten Typ

Stelle: `mensch_als_republik/profiles/credit.py`, `_obligation_v_findings`.
`INVALID_V_TYPE` für Key 0 und Key 1.

rot: 1

```
tests/profiles/test_payload.py::test_TV_T1
```

Klasse: **geprüft**

Nur Key 0 der Obligation ist geprüft. Key 1 und die Quittung haben keine
eigenen roten Tests. `verdict.py` prüft den Typ von `v` nicht.

### N11 — dieses `N` ist der ausgewertete Scope

Stelle: `mensch_als_republik/profiles/credit.py`, `settlement`. Die Prüfung
`c.N != scope` an der Quittung, Vermerk `SCOPE_MISMATCH`.

rot: 1

```
tests/profiles/test_credit.py::test_SE_5
```

Klasse: **geprüft**

Parallele Stellen in `verdict.py`, `membership.py` und `tally.py` sind nicht
neutralisiert. Die Argumentprüfung `obligation.N != scope` (ValueError) ist ein
zweiter Träger derselben Pflicht in derselben Funktion; sie blieb stehen.

### N12 — `irrevocable_predicates` enthält `vote@1` und `ratify@1`

Stelle: `mensch_als_republik/governance/tally.py`, `constitution_governable`.

rot: 4

```
tests/governance/test_regierbarkeit.py::test_target_with_revocable_vote
tests/governance/test_regierbarkeit.py::test_target_with_revocable_ratify
tests/governance/test_vectors.py::test_GV_27
```

Klasse: **geprüft**

Der vierte rote Test ist `tests/governance/test_vectors.py::test_GV_31`.

### N13 — `decide` rechnet die Genesis-Bindung vor jedem Feldzugriff nach

Stelle: `mensch_als_republik/governance/tally.py`, `decide`. Der Vergleich des
Genesis-Hash gegen `epoch.scope`, vor dem Zugriff auf `genesis_obj[5]` und
`genesis_obj[6]`.

rot: 1

```
tests/governance/test_genesis_bindung.py::test_D145_unbound_ordinary_genesis_does_not_pass_amendment
```

Klasse: **geprüft**

### N14 — es wird geworfen, nicht vermerkt

Stelle: `mensch_als_republik/governance/chain.py`, `resolve_epoch`. Der
Vergleich von `scope` gegen den Hash des Genesis.

rot: 0. Der Lauf blieb grün.

Klasse: **ungeprüft**

`resolve_policy` wirft dieselbe `ValueError` mit derselben Meldung, sobald die
Kette weiterläuft. Die Prüfung in `resolve_epoch` ist damit für die bestehenden
Tests unsichtbar. Das ist der Fall aus den Rückfragen: die Stelle lässt sich
nicht allein rot färben.

## Zählung

| Klasse | Pflichten |
| --- | --- |
| geprüft | N01, N03, N04, N05, N06, N08, N09, N10, N11, N12, N13 |
| ungeprüft | N02, N07, N14 |
| ohne Träger | keine |

Elf geprüft, drei ungeprüft, keiner ohne Träger. N01 hat keinen akt-spezifischen
Träger, aber einen allgemeinen. Deshalb nicht ohne Träger.

## Nachlauf: N11 und N14 mit geschlossener Trägermenge

Nach D245. Zwei Proben, je alle Träger zugleich. Dazwischen `git diff --quiet`.
Grundlinie 597 Tests. Kein Produktivcode bleibt geändert.

### N14 — es wird geworfen, nicht vermerkt

Träger, die den Genesis-Hash gegen `scope` vergleichen und bei Abweichung
werfen. Die Meldung ist überall `genesis_obj does not match scope`:

1. `mensch_als_republik/governance/chain.py`, `resolve_epoch`
2. `mensch_als_republik/profiles/policy.py`, `resolve_policy`
3. `mensch_als_republik/keys.py`, `resolve_authorized_keys`
4. `mensch_als_republik/trust/params.py`, `resolve_trust_params`

rot: 6

```
tests/governance/test_chain.py::test_chain_wrong_scope_raises
tests/nucleus/test_anchor.py::test_j_scope_mismatch_raises
tests/profiles/test_invariants.py::test_PR_INV_4
```

Die übrigen drei sind `test_P_F`,
`test_resolve_state_wrong_scope_raises_like_resolve_epoch` und
`test_genesis_does_not_match_scope`.

Klasse: **geprüft**

Abweichung vom bisherigen Befund: dort nur `resolve_epoch`, mit
`resolve_policy` als unsichtbarem Schatten. Die geschlossene Menge hat vier
Träger. D245 nannte dieselben vier; das ist bestätigt, nicht übernommen.

`decide` in `tally.py` wirft gegen `epoch.scope` mit der anderen Meldung
`genesis_obj does not match epoch scope`. Das ist N13, nicht N14.

### N11 — dieses `N` ist der ausgewertete Scope

Träger, die ein `N` gegen den ausgewerteten Scope prüfen:

1. `mensch_als_republik/profiles/credit.py`, `settlement`: `obligation.N`,
   ValueError
2. `mensch_als_republik/profiles/credit.py`, `settlement`: Quittung `c.N`,
   Vermerk `SCOPE_MISMATCH`
3. `mensch_als_republik/profiles/verdict.py`, `verdict_status`: `verdict.N`,
   ValueError
4. `mensch_als_republik/profiles/verdict.py`, `_active_submission`: `c.N`,
   Vermerk `SCOPE_MISMATCH`
5. `mensch_als_republik/profiles/verdict.py`, `verdict_status`: `accusation.N`,
   Vermerk `SCOPE_MISMATCH`
6. `mensch_als_republik/profiles/membership.py`, `membership`: `accept-rules`,
   `c.N`
7. `mensch_als_republik/profiles/membership.py`, `membership`:
   `grant-membership`, `c.N`
8. `mensch_als_republik/governance/tally.py`, `decide`: `vote.N` gegen
   `epoch.scope`

rot: 8

```
tests/governance/test_vectors.py::test_GV_20
tests/profiles/test_credit.py::test_SE_5
tests/profiles/test_invariants.py::test_PR_INV_9
```

Die übrigen fünf sind `test_PR_INV_13`, `test_MB_9`, `test_VS_7`, `test_VS_12`
und `test_VS_13`.

Klasse: **geprüft**

Abweichung: der bisherige Befund nannte vier Module und eine Argumentprüfung
in `settlement`. Die geschlossene Menge hat acht Stellen in denselben vier
Modulen. Die Argumentprüfung in `verdict_status` war ungenannt.

Die Argumentprüfung `obligation.N` in `settlement` ist Träger. Der einzige
Test, der sie trifft, wirft danach noch über `policy.scope`. Unter
geschlossener Neutralisierung der N-Stellen blieb dieser eine Aufruf grün.
Die Klasse hängt nicht an ihm.

`test_PR_INV_9` wurde rot, weil die Vermerke `SCOPE_MISMATCH` fehlten, nicht
weil eine andere Pflicht brach.
