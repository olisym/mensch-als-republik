# 00a-rotate-key — Implementierungs-Prompt

## Branch und Basis

Branch `impl/00a-rotate-key`, Basis ist der Commit, der diese Datei einführt. Ein Commit am
Ende, kein Merge, kein Push.

## Normative Grundlage

`00 §5.2`, `§6.1`, `§6.3`, `§6.4`; Register D62, D63 (Musterfall), D125, D149, D151, D152, D153,
D154, D155. Bei Widerspruch zwischen dieser Datei und dem Register gilt das Register — melden,
nicht auflösen.

Layer 00 hat bisher keinen Produktivcode. `resolve_current_key` ist die erste Funktion, die eine
Aussage aus `00` trägt.

## Auftrag 1 — Protokoll-Default der irrevocablen Prädikate erweitern (D153)

In `mensch_als_republik/policy.py` nimmt `PROTOCOL_IRREVOCABLE` zusätzlich `rotate-key@1` und
`rotate-ack@1` auf. Der Kommentar nennt neben D70 und `00 §5.2` auch D153.

Ein Test in der bestehenden Policy-Testdatei belegt, dass ein `core/revoke@1` auf ein
`nuc:N/rotate-key@1` desselben Autors den Rotate **nicht** in `REVOKED` bringt.

**Rücknahmeprobe (Prüfregel 23):** die Erweiterung testweise zurücknehmen und bestätigen, dass
genau dieser Test rot wird. Die geschützte Seite ist `obligation@1` — ein Test, der über
`obligation@1` läuft, sieht die Regression nicht. Das Ergebnis der Probe gehört in den Bericht,
mit dem Namen des Tests, der rot wurde.

## Auftrag 2 — `mensch_als_republik/keys.py`

Neues Modul, flach neben `policy.py` und `predicates.py`. Ein einzelnes Modul rechtfertigt kein
Paket.

```
def resolve_current_key(
    store: ClaimStore,
    *,
    scope: bytes,
    anchor_keys: frozenset[bytes],
    now: int,
) -> frozenset[bytes]
```

`anchor_keys` ist der Anker (D151); das Herleiten aus Genesis oder Verfassung ist **nicht**
Gegenstand dieses Laufs. Der Rückgabetyp ist deckungsgleich mit `authorized_keys` in
`profiles/membership.py`, damit das Ergebnis dort ohne Umformung eingesetzt werden kann.

**Semantik, aus `§6.4` Schritt 2 bis 4:**

Für jeden Schlüssel `k` aus `anchor_keys` wird ein Kopf bestimmt. Die Vereinigung aller Köpfe ist
das Ergebnis; Wurzeln ohne Kopf tragen nichts bei.

Kopfbestimmung ab `k`, iterativ mit `k_cur = k` und einer Menge besuchter Schlüssel:

1. Ist `k_cur` bereits besucht, liefert die Wurzel **keinen Kopf** (D155 d).
2. Existiert im Store ein `rotate-key@1` mit `I == k_cur` und Klassifikation
   `EQUIVOCATION_FLAGGED`, liefert die Wurzel **keinen Kopf** — unabhängig davon, ob dieser
   Rotate gegengezeichnet ist (D155, letzter Absatz; `§6.4` Schritt 3).
3. Alle **vollständigen** Rotationen mit `I == k_cur` sammeln. Vollständig heißt: der Rotate
   erfüllt die Belegung unten und es existiert eine passende Ack.
   - keine: Kopf ist `k_cur`, fertig.
   - genau eine: `k_cur` wird der von ihr benannte Nachfolger, weiter bei 1.
   - mehrere: die früheste in der eigenen Kette von `k_cur` bindet (D154). Früher heißt: sie
     liegt auf dem `h_prev`-Pfad der anderen, rückwärts über `store.get(h_prev)`. Ist keine auf
     dem Pfad aller übrigen, liefert die Wurzel **keinen Kopf** (D155 a).

**Belegung des Rotate (`00 §6.1`):**

```
R.p          == nuc:<scope>/rotate-key@1
R.J          == (1, K_n)          ; identity
R.N          == scope
R.I          == k_cur
Zustand      ∈ {ACTIVE, EXPIRED}
```

**Belegung der Ack (D152):**

```
ack.p        == nuc:<scope>/rotate-ack@1
ack.J        == (2, claim_id(R))  ; claim-ref
ack.I        == R.J[1]
ack.N        == R.N
Zustand      ∈ {ACTIVE, EXPIRED}
```

Alle vier Bedingungen der Ack sind zu prüfen. `ack.N == R.N` ist nicht redundant (D152, D63).

`EXPIRED` zählt wie `ACTIVE`, weil die Auflösung sonst an `now` hinge (D155 c). `now` bleibt
trotzdem Parameter, weil die Klassifikation ihn braucht.

**Zu benutzen:** `classify_all(store, now)` für die Zustände, `claim_id`, `parse_predicate` bzw.
die vorhandene Prädikatprüfung aus `profiles/membership.py` als Muster, `store.get` für den
Rückwärtslauf. Kein neues Store-Primitiv, keine Änderung an `verifier.py`, `index.py`, `atom.py`.

## Auftrag 3 — Tests

Neue Datei `tests/nucleus/test_rotate_key.py` (mit `__init__.py`, falls das Testverzeichnis
Pakete führt — an den bestehenden Testverzeichnissen ablesen, nicht raten). Alle Schlüssel und
Claims im Test konstruiert; keine Erwartungswerte tippen, die sich aus einer Konstruktion ableiten
lassen.

Mindestens diese Lagen, jede mit dem Registerbezug im Docstring:

1. Kein Rotate im Store: Ergebnis ist `anchor_keys`.
2. Eine vollständige Rotation: Ergebnis ist der Nachfolger, nicht die Wurzel.
3. Rotate ohne Ack: Ergebnis bleibt die Wurzel (D125).
4. Ack vom Vorgängerschlüssel statt vom Nachfolger: unvollständig (D152).
5. Ack mit fremdem `N`: unvollständig (D152, vierte Bedingung).
6. Ack als `core/revoke@1` statt `rotate-ack@1`: unvollständig (D152, der Fall, wegen dem das
   Prädikat eigens existiert).
7. Rotate mit `J.tag == claim-ref` statt `identity`: kein gültiger Rotate (D152).
8. Zwei Wurzeln in `anchor_keys`, eine davon rotiert: Ergebnis enthält beide Köpfe (D149).
9. Equivocation an einem Kettenpunkt: diese Wurzel liefert nichts, die andere weiter (D155).
10. Zwei vollständige Rotationen desselben Autors mit verschiedener `h_prev`, Zwischenglied
    vorhanden: die frühere bindet (D154).
11. Dieselbe Lage ohne Zwischenglied im Store: kein Kopf aus dieser Wurzel (D155 a).
12. Rücksprung unter Wissenszuwachs (D154): erst nur die Ack der späteren Rotation im Store,
    Kopf ist deren Nachfolger; nach Hinzufügen der Ack der früheren Rotation ist der Kopf ein
    anderer. Der Test hält beide Ergebnisse fest, nicht nur das zweite.
13. Zyklus `K_1 → K_2 → K_1`: kein Kopf, Lauf terminiert (D155 d).
14. Rotate mit gesetztem `t_exp`, `now` darüber hinaus: zählt weiter (D155 c).

## Nicht-Ziele

Was hier nicht steht, wird gemeldet, nicht gebaut.

- **Kein `nucleus_keys`, keine Epochenkette, kein Zugriff auf Layer 04** (D151, gehört nach `00b`).
- **Keine Herleitung des Ankers aus dem Genesis.** `anchor_keys` bleibt Parameter.
- **Kein FROST** (`00 §6.5`).
- **Keine Änderung an `profiles/membership.py`** oder sonst an Layer 03; `authorized_keys` bleibt
  dort Parameter.
- **Keine Findings, kein Rückgabe-Objekt, kein zwölfter Reject-Code.** Eine unaufgelöste Wurzel
  ist am Fehlen ihres Kopfes erkennbar; mehr ist nicht entschieden.
- **Keine Änderung an Layer 01** und keine an den Golden Anchors irgendeiner Schicht.
- Kein `float`, kein `fractions`, keine neue Abhängigkeit. `now` bleibt Parameter.

## Abnahmekriterien

- `make check-all` grün, mit der Testzahl vor und nach dem Lauf im Bericht.
- Die Rücknahmeprobe aus Auftrag 1 ist gelaufen, mit dem Namen des rot gewordenen Tests.
- Lage 13 terminiert; falls nicht, ist das ein Befund und keine Anpassung des Tests.
- Widerspricht eine Messung diesem Prompt, wird sie **gemeldet**. Erwartungswerte werden nicht
  nachgezogen.

## Abschluss

Ein Commit auf `impl/00a-rotate-key`. Kein Merge, kein Push. Der Bericht nennt den Commit, das
Ergebnis von `make check-all`, die Rücknahmeprobe und jede Stelle, an der der Prompt unterbestimmt
war.
