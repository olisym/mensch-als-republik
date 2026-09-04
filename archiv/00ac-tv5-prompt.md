# Lauf 00ac-A — TV5: `t_exp` auf `core/*` sichtbar machen

## Branch und Basis

Branch `lauf/00ac-tv5`, abgezweigt vom Commit, der diese Datei einführt. Dieser Commit ist der
Vergleichspunkt des Laufs (Prüfregel 37), nicht der Stand davor.

## Normative Grundlage

- `01 §5.3` — Lifecycle-Claims SOLLEN kein `t_exp` setzen; ein Verifizierer MUSS ein `t_exp` auf
  einem `core/*`-Claim ignorieren. Der Absatz nennt seit dem Basis-Commit TV5 als Vektor.
- `01 §B.3` — `t_exp` auf `core/*` ist ausdrücklich kein Reject-Grund.
- `01 §C.9` — TV5 mit gerechneten Bytes, `claim_id` und Signatur. Diese Werte sind Vorgabe.
- D247 (der Befund), D250 (Vektor statt Sondierwelt, C.9 statt Einschub), D253 (die Probe zu N02).

## Der Befund, den dieser Lauf schließt

`tests/test_verifier.py::test_core_revoke_ignores_t_exp` behauptet im Docstring, ein `core/*`-Claim
werde auch mit gesetztem `t_exp` als `active` klassifiziert. Der Test klassifiziert TV3, und TV3
trägt kein `t_exp`. Wird der `core/*`-Zweig aus `_is_temporally_valid` entfernt, bleibt der Lauf
grün: die nächste Zeile liefert für einen Claim ohne `t_exp` dasselbe Ergebnis. Der Test kann nicht
sehen, was er zu sehen behauptet.

## Auftrag

**1. TV5 in `tests/vectors/gen.py`.** Ein `core/revoke@1` von Alice auf TV1, verkettet auf TV3:
`I` ist `ALICE_PUB`, `J` ist `(2, tv1_cid)`, `p` ist `P_REVOKE`, `t` ist `1_700_000_300`, `t_exp`
ist `1_700_000_400`, `h_prev` ist die `claim_id` von TV3. Kein `N`, kein `v`. Signiert mit
`alice_sk` über `_finalize`. Als **letzter** Eintrag der `vectors`-Liste über `_vec("TV5", tv5)`,
ohne `expect_reject`.

**2. `tests/vectors/vectors_01.json` neu erzeugen** aus `gen.py`. Die Datei wird nicht von Hand
bearbeitet.

**3. Golden-Werte eintragen.** In `tests/test_vectors_01.py` ein `GOLDEN`-Eintrag für TV5, in
`tests/test_atom.py` ein `GOLDEN_CLAIM_IDS`-Eintrag für TV5 und TV5 in der Parametrisierung von
`test_claim_id_from_vectors`. Beide Tabellen tragen dieselbe `claim_id`; eine von beiden
auszulassen hieße, sie auseinanderlaufen zu lassen.

**4. `tests/test_verifier.py`.**

- `test_structural_check_valid_vectors` um TV5 erweitern.
- `test_core_revoke_ignores_t_exp` umbenennen in `test_core_revoke_without_t_exp_stays_active` und
  den Docstring auf das korrigieren, was der Test misst: ein `core/*`-Claim **ohne** `t_exp` bleibt
  jenseits jedes `now` aktiv. Der Testkörper bleibt unverändert.
- Ein neuer Test `test_core_revoke_with_expired_t_exp_stays_active`: Store mit TV1, TV2, TV3, dann
  TV5 hinzufügen, `classify` mit `now = 1_800_000_000` aufrufen und `State.ACTIVE` erwarten. Der
  Vorgänger von TV5 ist TV3; ohne die drei ist TV5 `pending` und der Test misst etwas anderes.

**5. Rücknahmeprobe A.** In `mensch_als_republik/verifier.py` in `_is_temporally_valid` den Zweig
entfernen, der für `core/*`-Prädikate früh `True` liefert. Testlauf. Erwartet wird genau ein roter
Test, `test_core_revoke_with_expired_t_exp_stays_active`, mit `State.EXPIRED` statt `ACTIVE`. Die
Trägermenge ist geschlossen: die Funktion steht einmal in `verifier.py`, `index.py` importiert sie
(Prüfregel 49). Danach zurücknehmen.

**6. Probe B — drei Läufe zu N02.** Alle drei werden nach der Messung zurückgenommen; am Ende ist
`mensch_als_republik/predicates.py` unverändert.

- **B1:** Im Alias-Scope-Muster den vorangestellten negativen Lookahead entfernen, die
  Zeichenklasse und beide Anker unverändert lassen. Sonst nichts ändern. Erwartet: kein roter Test.
- **B2:** Nur die Reihenfolge der beiden Muster-Abfragen in `parse_predicate` tauschen, so dass das
  Alias-Muster vor dem kanonischen Muster geprüft wird. Das Lookahead bleibt. Erwartet: kein roter
  Test.
- **B3:** Beides zugleich. Erwartet: genau ein roter Test,
  `tests/test_predicates.py::test_alias_matching_64_hex_rejected`.

Gemeldet wird je Probe die Liste der roten Tests, nicht nur die Anzahl.

## Nicht-Ziele

- **Keine Löschung in `predicates.py`.** D251 hat den Löschungsbeschluss aus D248 zurückgenommen:
  beide Lookaheads spiegeln die gedruckten Regexe aus Anhang A von `01-claim-atom.md`, und die
  redundante Bedingung in `resolve_scope` spiegelt die zwei MUSS aus `01 §2.2` Regel 3. Probe B
  misst, sie repariert nicht.
- **Keine Änderung an Anhang A.** Der Befund dazu ist D252 und ausdrücklich offen.
- **Keine Umnummerierung von Anhang C.** TV5 ist C.9 und bleibt es.
- **Keine Änderung an TV1 bis TV4, NV1 bis NV3, BV1 bis BV3** und an keinem bestehenden
  Golden-Wert. Weicht ein bestehender Wert nach der Neuerzeugung ab, ist das ein Befund: melden,
  nicht nachziehen.
- **Kein zweiter Vektor, keine Sondierwelt.**
- **`07-decisions.md`, `pruefregeln.md` und `01-claim-atom.md` werden nicht angefasst.** Der
  Spec-Teil liegt im Basis-Commit.

## Abnahmekriterien

1. `vectors_01.json` trägt elf Einträge; der letzte heißt TV5 und hat kein `expect_reject`.
2. TV5 trägt `claim_id` `8b19196274b2a8ac08e9a34337de5f445e6efd19fb75155eb187b069f5fd8022`. Die
   Bytes und die Signatur stimmen mit `01 §C.9` überein.
3. `make check-all` ist grün mit **601** Tests plus 14 Eigenschaftstests. Die vier neuen kommen aus
   je einem Parametrisierungsfall in `test_structural_check_valid_vectors`,
   `test_claim_id_matches_golden` und `test_claim_id_from_vectors` sowie dem neuen
   Verifizierer-Test.
4. Probe A färbt genau `test_core_revoke_with_expired_t_exp_stays_active` rot.
5. Probe B1 und B2 färben keinen Test rot, B3 färbt genau `test_alias_matching_64_hex_rejected` rot.
6. `git diff` gegen den Branchpunkt zeigt Änderungen ausschließlich in `tests/vectors/gen.py`,
   `tests/vectors/vectors_01.json`, `tests/test_vectors_01.py`, `tests/test_atom.py` und
   `tests/test_verifier.py`.

## Abschluss

Ein Commit auf `lauf/00ac-tv5`, kein Merge. Zurück kommen der vollständige `git diff` gegen den
Branchpunkt, die Ausgabe von `make check-all` und die fünf Probenergebnisse aus 5 und 6.

Widerspricht eine Messung diesem Prompt, wird sie gemeldet und nicht angepasst. Was hier nicht
steht, wird nicht gebaut.
