# Prompt: Einlesepfad Lauf A — Paketschicht (D130, D131)

Branch: `impl/einlesen` von `spec/d130-d132` (`8406ef4`).

Normative Grundlage: `07-decisions.md` D130 und D131, `01-claim-atom.md` §6, Anhang B.2,
Anhang C.8. Bei Widerspruch zwischen diesem Prompt und der Spec gilt die Spec — und der
Widerspruch ist zu melden, nicht aufzulösen.

**Rückfragen gehen an den Supervisor, nicht ins eigene Fenster.** Jede offene Frage ist ein
Kandidat für eine Registerlücke.

## 1. Was gebaut wird

Zwei Dinge in `mensch_als_republik/verifier.py`, sonst nichts.

### 1.1 D130 — der Rundlauf steht im `try`

`structural_check` ruft heute in Schritt 2c:

```python
    # 2c: kanonische Kodierung (§3)
    if not cbor_canon.is_canonical(data):
        raise NonCanonicalEncoding()
```

`is_canonical` ruft `reserialize` und damit `encode`. Für `h'a100ff'` (BV1) wirft `encode` einen
`CBOREncodeError`, der `structural_check` als Nicht-`VerifierError` verläßt.

Zu bauen:

```python
    # 2c: kanonische Kodierung (§3, D130)
    try:
        canonical = cbor_canon.is_canonical(data)
    except Exception as exc:
        raise MalformedCbor() from exc
    if not canonical:
        raise NonCanonicalEncoding()
```

**Der `try` bleibt an dieser Stelle.** Er wandert nicht zum Dekodier-`try` in 2a. Der Grund steht
in D130 und wird von BV2 geprüft: vorgezogen kippte die Diagnose für Bytes, die zugleich
nicht-kanonisch und strukturell ungültig sind, auf `NON_CANONICAL_ENCODING`. Die Reihenfolge
§6 2a → 2b → 2c → 2d bleibt unverändert.

`except Exception` ist hier richtig, weil im `try` ein **fremder** Aufruf steht, dessen
Ausnahmemenge weder aufzählbar noch versionsstabil ist — dieselbe Form wie in
`trust/groups.py:41` und `profiles/payload.py:18`. Das ist die Ausnahme von 1.2, nicht deren
Widerlegung.

### 1.2 D131 — `read_claim`

Neu in `verifier.py`, direkt nach `structural_check`, und in `__all__`:

```python
def read_claim(data: bytes, store: ClaimStore | None = None) -> Claim | ErrorCode:
    """Einlesepfad: liefert einen Claim oder einen Reject-Code, wirft nie (D131)."""
    try:
        return structural_check(data, store)
    except VerifierError as exc:
        return exc.code
```

**Nur `VerifierError`.** Nicht `Exception`. Ein Programmierfehler in `structural_check` muß
durchschlagen; fienge ihn `read_claim`, würde jeder Claim zu `MALFORMED_CBOR` und das Netz sähe
aus, als bestünde es aus kaputten Bytes, während die Ursache lokal ist.

Die Zusicherung „wirft nie" wird durch den Eigenschaftstest aus 2.4 getragen, nicht durch eine
breite `except`-Klausel.

## 2. Tests

### 2.1 Die Byte-Vektoren in `gen.py`

BV1–BV3 aus `01 Anhang C.8` gehen in `tests/vectors/gen.py` als Hex-Konstanten und erscheinen in
`vectors_01.json` als Einträge der bestehenden Vektorliste. Sie tragen **kein** `signed_bytes` —
sie sind nicht signiert. Feldname: `wire_bytes`.

```
BV1  a100ff                      expect_reject MALFORMED_CBOR
BV2  bf616100ff                  expect_reject MALFORMED_CBOR
BV3  bf0001…01ff (310 Byte)      expect_reject NON_CANONICAL_ENCODING
```

BV3 wird **nicht** von Hand eingetragen, sondern in `gen.py` aus TV1 gerechnet: äußere Map in
indefinite-length-Form, Schlüssel aufsteigend, Werte kanonisch kodiert —
`h'bf'` ‖ Σ(`encode(k)` ‖ `encode(m[k])`) ‖ `h'ff'`. Stimmt das Ergebnis nicht Byte für Byte mit
dem Hex in `Anhang C.8` überein, ist das ein Befund und keine Anpassung des Generators.

`gen.py` läuft als Modul (`python -m tests.vectors.gen`); die erzeugte JSON wird committet.

**Der Grund für den Umweg über `gen.py`:** `test_verifier.py` liest Vektoren ausschließlich aus
der JSON. Eine zweite Bezugsquelle für Vektoren wäre genau die Asymmetrie, die D132 an anderer
Stelle verbietet.

### 2.2 Vektortests

In `tests/test_verifier.py`:

- Je Vektor BV1–BV3 ein Test gegen `structural_check`, der die passende Ausnahmeklasse erwartet.
- Eine **abgeleitete** Parametrisierung für `read_claim`: über alle Vektoren, die
  `expect_reject` **und** verwertbare Draht-Bytes tragen — `wire_bytes`, ersatzweise
  `signed_bytes`. Erwartung: `read_claim(bytes) == ErrorCode[v["expect_reject"]]`.
  Die Liste der Codes wird **nicht** getippt, sie fällt aus der Vektordatei.
- NV2 trägt weder `wire_bytes` noch `signed_bytes` und fällt aus der Parametrisierung. Damit
  wäre `NON_CANONICAL_ENCODING` auf dem neuen Weg ungeprüft — also bekommt
  `test_nv2_non_canonical_encoding` einen Zwilling, der dieselben zusammengebauten Bytes durch
  `read_claim` schickt und den Code erwartet.
- Ein Test, der für einen gültigen Vektor (TV1) zeigt, daß `read_claim` einen `Claim` mit
  derselben `claim_id` liefert wie `structural_check`.

### 2.3 Testpunkt an der Hilfsschicht

In `tests/test_cbor_canon.py`: ein Test, der zeigt, daß `is_canonical` auf BV1-Bytes **wirft**.
Drei Produktivaufrufer verlassen sich auf diese Eigenschaft; sie hat bisher keine Zusicherung.
Auf eine bestimmte Ausnahmeklasse wird nicht geprüft — die gehört `cbor2`.

### 2.4 Eigenschaftstest

Neue Datei `tests/property/test_read_claim.py`, zwei Aussagen im selben Testsatz. **Beide sind
nötig**; jede allein ist erfüllbar, ohne daß `read_claim` richtig ist.

1. **Totalität.** Über `st.binary(min_size=0, max_size=512)`: `read_claim` gibt einen `Claim`
   oder einen `ErrorCode` zurück und wirft nicht. Allein erfüllt eine Funktion, die konstant
   `MALFORMED_CBOR` liefert.
2. **Kopplung.** Über `welten()` aus `tests/property/welten.py`: für jeden erzeugten Claim `c`
   stimmt `read_claim(signed_bytes(c))` mit `structural_check(signed_bytes(c))` überein — entweder
   derselbe `Claim` (gleiche `claim_id`), oder derselbe Code wie die geworfene
   `VerifierError.code`. Allein erfüllt sie eine Funktion, die nur dekodiert und nichts prüft:
   die lieferte einen `Claim`, wo `structural_check` wirft.

Die Kopplungsaussage macht **keine** Annahme über die Gültigkeit der erzeugten Claims. Das ist
Absicht: `welten()` erzeugt in der Lage `"vergangen"` ein `t_exp` ohne Rücksicht auf `t` und
damit Claims, die `INCOHERENT_EXPIRY` sind. Dieser Befund wird in diesem Lauf **nicht repariert**
und **nicht weggefiltert** — kein `assume`, kein Filter, keine Änderung an `welten.py`. Er wird
gemeldet (siehe §5).

Nichtleere trägt der TV1-Test aus §2.2: dort kommt nachweislich ein `Claim` zurück. Ohne ihn
wäre die Kopplung von einer Funktion erfüllbar, die immer denselben Code liefert wie eine gleich
kaputte `structural_check`.

Profilsteuerung wie im Bestand (`conftest.py`, `MAR_HYPOTHESIS`). Keine neuen Strategien in
`welten.py`.

## 3. Ausdrücklich nicht in diesem Lauf

- **`atom.claim_from_bytes` wird nicht angefaßt** — weder umbenannt noch privat gemacht. Das ist
  D132 und gehört nach Lauf B.
- **`tools/sim/welt.py` wird nicht angefaßt.** `store_laden` bleibt, wie es ist.
- **Die Bestandsaufrufer von `structural_check`** in `index.py` und `verifier.py` bleiben bei
  `try/except VerifierError`. Sie reichen eigene Bytes herein; ein Umbau auf `read_claim` wäre
  Geschmack, nicht Reparatur.
- **Kein Bündelformat.** Das ist Lauf B.
- **B-4** (Zwillingsbuchführung in `welten()`) bleibt offen. Mitzunehmen hieße, bei einer
  Abweichung nicht zu wissen, welche Änderung sie bewegt hat.
- **`welten.py` wird nicht angefaßt**, auch nicht für das `t_exp`-Problem aus §2.4. Ein Lauf, der
  den Erzeuger repariert und zugleich den Einlesepfad baut, kann bei einer Abweichung nicht
  sagen, welche der beiden Änderungen sie bewegt hat.

## 4. Abnahmekriterien

Abgeleitet, nicht aufgezählt:

1. `make check-all` grün, zwei pytest-Endzeilen. Testzahl steigt von 474.
2. `MAR_HYPOTHESIS=voll` grün; der neue Eigenschaftstest erscheint dort.
3. `grep -n 'is_canonical' mensch_als_republik/verifier.py` zeigt den Aufruf innerhalb eines
   `try` in Schritt 2c — nicht in 2a.
4. `grep -c 'except Exception' mensch_als_republik/verifier.py` ergibt **2** — Schritt 2a
   (Bestand) und Schritt 2c (dieser Lauf), beide um einen fremden Aufruf. `grep -n 'except'`
   zeigt darüber hinaus in `read_claim` ausschließlich `except VerifierError`.
5. Der Vektortest zu BV1 schlägt fehl, wenn 1.1 zurückgenommen wird — bitte einmal prüfen und im
   Commit-Text bestätigen. Ein Regressionstest, der die Regression nicht sieht, ist keiner.
6. `python -m tests.vectors.gen` erzeugt `vectors_01.json` reproduzierbar; `git diff` danach
   leer.
7. `python -m tools.check_specs` sauber.

## 5. Abschluß

Ein Commit auf `impl/einlesen`. Kein Merge. Die Abnahme führt der Supervisor.

Was im Commit-Text stehen soll: die Testzahl vorher/nachher, das Ergebnis von Kriterium 5, und
jede Stelle, an der die Spec eine Frage offen gelassen hat.

Dazu **eine Messung**, die kein Test ist und nichts grün oder rot macht: über einen Lauf von
`welten()` unter `MAR_HYPOTHESIS=voll` die Verteilung der Ergebnisse von
`read_claim(signed_bytes(c))` — wie viele `Claim`, und je Reject-Code wie viele. Die Zahlen
gehören in den Commit-Text. Sie sagen, wie groß der `welten()`-Befund ist, und sie sind der
billigste Weg dorthin, weil der Einlesepfad ohnehin gebaut wird.
