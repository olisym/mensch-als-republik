# Prompt: Punkt-7-Ausnahme für `core/*` und zwei Vektoren (D263, D264)

## Branch und Basis

Branch `lauf/00ae-c11`. Basis ist der Commit, der diese Datei einführt — der Kopf des Branches
beim Start. Am Ende **ein** Commit auf diesem Branch, kein Merge, kein Push nach `main`.

## Normative Grundlage

- **D264**: auf `core/*` findet die Feld-Konsistenz `t < t_exp` nicht statt. `01 §6` Punkt 7 und
  `01 §5.3` tragen die Ausnahme bereits im Text; die Referenzimplementierung noch nicht.
- **D263**: `J.tag != claim-ref` auf `core/*` ist `MALFORMED_CBOR`. Das ist bereits das Verhalten
  von `structural_check`; es fehlt der Vektor.
- **D250**: ein Anhang wird **angehängt, nicht eingeschoben**. C.11 kommt hinter C.10.
- **D257**: ein Vektor trägt genau einen Mangel.

## Auftrag

### 1. `mensch_als_republik/verifier.py`

Schritt 7 in `structural_check` entfällt für `core/*`-Prädikate. Die Bedingung ist dieselbe, die
`_is_temporally_valid` schon benutzt. Kein anderer Schritt wird angefasst, keine Signatur
geändert, keine Fehlerklasse ergänzt.

### 2. `tests/vectors/gen.py` — zwei neue Vektoren

Die Felder liegen fest. Nichts daran ist frei zu wählen, auch nicht die Zeitstempel:

**TV6** — positiv, `core/revoke@1` mit `t >= t_exp`:

```
version  = 1
I        = ALICE
J        = [2, TV1.claim_id]
p        = "core/revoke@1"
v        = abwesend
N        = abwesend
t        = 1700000410
t_exp    = 1700000405
h_prev   = TV5.claim_id
signiert = ALICE
```

**NV12** — negativ, `core/revoke@1` mit falschem `J.tag`:

```
version  = 1
I        = ALICE
J        = [1, ALICE]
p        = "core/revoke@1"
v        = abwesend
N        = abwesend
t        = 1700000409
t_exp    = abwesend
h_prev   = id_genesis_anchor(ALICE)
signiert = ALICE
erwartet = Reject: MALFORMED_CBOR
```

TV5 ist im Generator bisher an keine Variable für seine `claim_id` gebunden; TV6 braucht sie.
Beide Vektoren werden hinten an die Rückgabeliste angehängt, TV6 vor NV12. `TV6` bekommt kein
`expect_reject`.

### 3. `tests/vectors/vectors_01.json`

Neu erzeugen über den Generator, nicht von Hand ergänzen.

### 4. `tests/test_vectors_01.py`

Die beiden Namen in `GOLDEN` aufnehmen. Die Werte werden **aus der Generatorausgabe gelesen**,
nicht getippt und nicht geschätzt.

### 5. Zwei Tests

TV6 wird angenommen: `read_claim` über die signierten Bytes liefert einen `Claim`, keinen
Fehlercode. NV12 wird mit `MALFORMED_CBOR` abgelehnt. Beide Tests ziehen ihre Bytes aus der
Vektorquelle, nicht aus getippten Hex-Zeichenketten.

### 6. `01-claim-atom.md` — neuer Abschnitt C.11

Hinter C.10 und **vor** `## Änderungshistorie`. Form wie C.9 und C.10: eine Überschrift der
Ebene 3, je ein `core = { … }` in der Kurzschreibweise des Bestands, dann `bytes`, `claim_id`
und `σ` als umbrochene Hex-Blöcke mit eingerückten Fortsetzungszeilen, bei NV12 zusätzlich die
Zeile `erwartet = Reject: MALFORMED_CBOR`. Dazu je zwei bis drei Sätze: bei TV6, dass `t_exp`
auf `core/*` ohne Wirkung bleibt und deshalb auch `t >= t_exp` kein Reject ist (`01 §5.3`); bei
NV12, dass der Tag die Form verletzt, die `01 §6` Punkt 4 für `core/*` verlangt, und dass
`FOREIGN_LIFECYCLE` ohne bekannten Ziel-Claim nichts behaupten kann.

Alle Zahlen kommen aus dem Generator. Keine Zeile über 100 Zeichen; keine Escapes; Bytes als
Hex ohne Präfix, wie im Bestand.

### 7. Rücknahmeprobe

Vor der Probe die Trägermenge zählen: welche Tests hängen an der Änderung aus Schritt 1. Dann die
Änderung zurücknehmen, `.venv/bin/python -m pytest -q` laufen lassen, die Zahl **und die Namen**
der roten Tests melden, die Änderung wiederherstellen und einen sauberen Baum bestätigen. Wird
kein Test rot, ist der neue Test keiner — das ist zu melden, nicht zu reparieren.

## Nicht-Ziele

- Keine Änderung an `_check_foreign_lifecycle`, kein Store, kein neuer Fehlercode.
- Keine Umsortierung der Prüfschritte in `structural_check`, keine Umbenennung der
  Kommentarmarken.
- NV11 bleibt unberührt, ebenso jeder bestehende Vektor und jeder bestehende Test.
- Kein weiterer Abschnitt in `01-claim-atom.md`, kein Eintrag in `07-decisions.md`.
- Kein Merge, kein Push nach `main`, kein Löschen des Branches.
- Was hier nicht steht, wird gemeldet und nicht gebaut.

## Abnahmekriterien

1. `make check` ist grün. Die Testzahl steigt um genau die neu geschriebenen Tests; keine
   bestehende wird rot.
2. `python3 tools/check_specs.py` meldet `01-claim-atom.md` ohne Befund.
3. `vectors_01.json` trägt TV6 und NV12.
4. `claim_id`, `bytes` und `σ` im gedruckten C.11 sind zeichengleich mit der Generatorausgabe.
5. Die Rücknahmeprobe meldet mindestens einen roten Test mit Namen.
6. Ein Commit. Der Bericht enthält den vollständigen `git diff` gegen den Branchpunkt, nicht nur
   `--numstat`.
