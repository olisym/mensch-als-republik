# Implementierungs-Prompt — `tools/example_nucleus.py`

Kein Layer, kein neues Modul im Paket. Ein Werkzeug plus ein Test, die belegen, dass
`example-nucleus.md` und die Implementierung dasselbe meinen.

Normative Quelle: `example-nucleus.md`. Weicht das Skript von einer dort dokumentierten Zahl ab,
ist das ein **Befund** und geht ins Spec-Gespräch zurück — das Dokument wird nicht angepasst,
damit das Skript grün wird.

---

## 1. Was es tut

`tools/example_nucleus.py` baut den Beispielnukleus aus Seeds auf, rechnet alle Objekte, erzeugt
das Claim-Set, lässt die Governance-Funktionen darüber laufen und prüft jedes Ergebnis gegen
`example-nucleus.md`.

Nichts wird als Konstante eingetragen. Jede Zahl entsteht aus der Rechnung und wird **danach**
gegen den dokumentierten Hexwert verglichen. Ein Skript, das die Werte als Literale trägt, prüft
sie gegen sich selbst.

## 2. Selbstprobe zuerst

Vor allem anderen: die Bestandsanker aus `00 §3.1` über denselben Kodierungsweg reproduzieren.

```
constitution_hash = 890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e6585c352dcf19ccad5ea7e
N                 = 65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557
```

Bricht diese Probe, ist die Kodierung falsch und nicht der Beispielnukleus. Das Skript bricht dann
ab, bevor es irgendetwas anderes rechnet.

## 3. Identitäten und Objekte

Ed25519 aus den Seeds `0x11×32` bis `0x14×32` — ANNA, BRUNO, CHRIS, DORA.

Zu prüfen sind alle Werte aus `example-nucleus.md §2` bis `§5`: beide `constitution_hash`, beide
`N`, `epoch_id_1`, `constitution_hash_2`, `proposal_hash`, `epoch_id_2`, und beide
`cbor(genesis)`-Hexstrings byteweise.

Ebenso die **Sortierung**: `participants` byteweise aufsteigend. DORA sortiert zwischen BRUNO und
CHRIS ein. Ein eigener Test hängt sie stattdessen an und erwartet `MALFORMED_PARTICIPANTS`.

## 4. Das Claim-Set

Neun Claims im Governance-Scope nach `example-nucleus.md §7`, vier `vouch@1` im
Ressourcen-Scope. Alle über die vorhandenen Bausteine des Pakets erzeugt und signiert — `atom`,
`cbor_canon`, `domains`.

**Die `v`-Kodierung von `vouch@1` wird aus `02-trust-flow.md` gelesen, nicht erfunden.** Findet
sich dort keine eindeutige Festlegung, ist das ein Befund und keine Ermessensfrage; der
Ressourcen-Teil wird dann zurückgestellt und der Governance-Teil allein geliefert.

## 5. Was geprüft wird

**Mitgliedschaft, Epoche 1.** Nach den drei `accept-rules`: alle drei `MEMBER`. Mit
`constitution_obj` gereicht (D111), `participants` nicht separat.

**Auszählung.** `decide()` gegen `proposal_hash` in Epoche 1, Klasse `membership`, Schwelle
`[1,2]`, `n = 3`. Drei Läufe entsprechend der Tabelle in `§5`:

| Stimmen | erwartet |
|---|---|
| ANNA ja, BRUNO nein | `PENDING` |
| ANNA ja, BRUNO nein, CHRIS ja | `PASSED` |
| ANNA ja, BRUNO nein, CHRIS nein | `FAILED` |

**Ratifizierung.** `verify_ratification()` mit der Zeugenmenge aus den beiden Ja-Stimmen liefert
`next_epoch` mit `epoch_id_2`. Ein zweites `ratify@1` von CHRIS mit **anderer** Zeugenmenge liefert
denselben `epoch_id_2` (D99).

**Mitgliedschaft, Epoche 2 — der wichtigste Test.** Gegen `constitution_hash_2` sind ANNA, BRUNO
und CHRIS `GRANT_ONLY`, weil ihre `accept-rules` auf den vorigen Hash zeigen. DORA ist
`GRANT_ONLY` vor ihrer Annahme und `MEMBER` danach. Das ist D116 und die Betriebswarnung aus
`example-nucleus.md §8.1`.

**Trust-Flow.** Im Ressourcen-Scope mit `C₀ = 100`, `γ = 1/2`, `D = 100`: CHRIS in Distanz 1 zum
Ankerset, `C(CHRIS) = 50`. Dazu die Reichweitentabelle aus `§4.3` als Rechnung, nicht als Literal:
`⌊100·(1/2)^d⌋` für `d = 0…7` ergibt `100, 50, 25, 12, 6, 3, 1, 0`.

**Scope-Trennung.** Kein Claim des einen Scopes wirkt im anderen: `membership(scope=N_res, …)`
liefert für alle vier `NONE`, und `decide()` auf `N_res` liefert `UNEVALUABLE` mit
`PARTICIPANTS_UNDECLARED`.

## 6. Form

- `tools/example_nucleus.py`, ausführbar, gibt bei Erfolg die Objekttabelle aus.
- `tests/test_example_nucleus.py` ruft dieselben Funktionen und prüft dieselben Werte, damit
  `make test` es abdeckt. Keine Logik doppelt: der Test importiert aus dem Werkzeug.
- Kein Eintrag in `Makefile` nötig — `make test` findet es über `testpaths`.
- Nur `cbor2`-freie Bausteine des Pakets, `cryptography` für Ed25519. Keine neuen Abhängigkeiten.

Erwartete Testzahl: **über 387.**

## 7. Rückfragen

Wie immer: jede Frage ohne Antwort in `example-nucleus.md` oder in den Spec-Dateien ist eine
Lücke und geht zurück. Besonders erwartbar ist die `v`-Kodierung aus `§4` und die Frage, mit
welchem `t` und `h_prev` die Claims gebaut werden — `now` ist Parameter, nie Systemuhr, und die
Kette jedes Autors beginnt bei `SHA-256(DOM_ID_GEN ‖ I)`.

## 8. Abnahme

Branch `impl/example-nucleus`. `make check` grün in drei Blöcken, committen **vor** dem Melden,
`git add` mit expliziten Pfaden.
