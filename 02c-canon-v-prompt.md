# `02c-canon-v` — Kanonizität des `v`-Payloads

Auftrag an den Implementierer. Normative Quelle: `02-trust-flow.md §3.1`, Absatz
„Nicht-kanonisches `v` ist unlesbar"; `01-claim-atom.md §3`, `§6` Regel 2; Register D37, D77.

Der Umfang ist klein und die Grenze scharf: **ein Enum-Eintrag, drei Zeilen in einer privaten
Funktion, sieben Vektoren.** Alle 235 bestehenden Tests müssen unverändert grün bleiben — kein
bestehender Golden Anchor, kein bestehender Vektor und keine bestehende Findings-Liste ändert
sich. Ein roter Bestandstest ist kein Nachjustieren wert, sondern der Beweis, dass die Prüfung
an der falschen Stelle sitzt.

---

## 1. Warum es das gibt

D37 verlangt kanonisches CBOR für `v`. Durchgesetzt war es nirgends: `cbor_canon.is_canonical`
läuft ausschließlich im Verifizierer auf den **Core**-Bytes. `v` ist darin eine `bstr`, deren
Inhalt uninterpretiert bleibt, und `trust/groups.py` liest sie per nacktem `decode`.

Der Fall, auf den es ankommt, ist der doppelte Schlüssel: `v = h'a2001864001865'` dekodiert zu
`{0: 101}` — ein Eintrag geht verloren, und welcher gewinnt, steht in cbor2, nicht in der Spec.
Damit hängt `n` an einer undokumentierten Bibliotheksentscheidung.

---

## 2. Änderung an `mensch_als_republik/trust/findings.py`

Ein Eintrag, sonst nichts:

```python
class TrustFinding(str, Enum):
    OVERCOMMITTED_AUTHOR = "OVERCOMMITTED_AUTHOR"
    SUBGRANULAR_VOUCH = "SUBGRANULAR_VOUCH"
    INVALID_VOUCH_WEIGHT = "INVALID_VOUCH_WEIGHT"
    UNPARSABLE_VOUCH_PAYLOAD = "UNPARSABLE_VOUCH_PAYLOAD"
    NON_CANONICAL_V = "NON_CANONICAL_V"
```

Die Zeichenkette ist normativ und wird in Layer 03 wörtlich wiederverwendet (eigener Enum, D69 —
geteilt wird der Name, nicht das Symbol).

---

## 3. Änderung an `mensch_als_republik/trust/groups.py`

Ausschließlich in `_decode_weight`. Die Platzierung **ist** die Aufgabe:

```python
def _decode_weight(v: bytes | None, D: int) -> tuple[int | None, TrustFinding | None]:
    if v is None:
        return D, None
    try:
        obj = cbor_canon.decode(v)
    except Exception:
        return None, TrustFinding.UNPARSABLE_VOUCH_PAYLOAD
    if not cbor_canon.is_canonical(v):
        return None, TrustFinding.NON_CANONICAL_V
    if not isinstance(obj, dict) or 0 not in obj:
        ...unverändert...
```

### 3.1 Drei Randbedingungen, jede mit einem Vektor dahinter

**Nach dem `decode`, nicht davor.** `is_canonical(v)` ruft intern `decode` auf und **wirft** bei
undekodierbarer Eingabe, statt `False` zu liefern — `h'a1'` → `CBORDecodeEOF`, `h'ff'` →
`CBOREncodeError` beim Re-Enkodieren. Ein Wächter vor dem `try` verwandelt
`UNPARSABLE_VOUCH_PAYLOAD` in eine durchschlagende Exception. `V-CANON-6` fängt das.

**Vor der Wertprüfung.** Kanonizität ist eine Eigenschaft der Bytes und geht der Interpretation
voraus. Trägt ein nicht-kanonisches `v` zugleich ein `n` außerhalb `[1, D]`, lautet der Vermerk
`NON_CANONICAL_V`, nicht `INVALID_VOUCH_WEIGHT`. `V-CANON-4` fängt das.

**Nicht wie ein abwesendes `v`.** Rückgabe ist `(None, NON_CANONICAL_V)` — kein Beitrag —, nie
`(D, …)`. Der Abwesend-Default `n = D` auf einen defekten Payload angewandt erzeugt maximales
Vertrauen aus einem Fehler; das ist Über-Vertrauen und damit die eine gefährliche Richtung
(`02 §7`).

### 3.2 Ausdrücklich verboten

`cbor_canon.encode(obj) != v` statt `cbor_canon.is_canonical(v)`. Es ist rechnerisch identisch
und spart den zweiten Dekodierdurchlauf — und es schreibt die Definition von „kanonisch" ein
zweites Mal auf. Zwei Definitionen driften. Der Payload ist vier Bytes groß; die Ersparnis ist
keine.

---

## 4. Ausdrücklich nicht in diesem Schritt

- **Layer 01 bleibt eingefroren.** Kein zwölfter Reject-Code, keine Änderung an `atom.py`,
  `cbor_canon.py`, `verifier.py`, `policy.py`, `errors.py`. Eine Kanonizitätsprüfung von `v` im
  Atom hieße, das Atom liest `v` — Bruch der Bedeutungsblindheit.
- **`cbor_canon.decode` bleibt, wie es ist.** Ein Decoder, der zusätzlich validiert, hat zwei
  Aufgaben. Die Trennung `decode` / `is_canonical` ist richtig und wird nicht angefasst.
- **Kein Eingriff in `rank()`.** Beide Sichten teilen `derive()` und damit `build_groups`; ein
  zweiter Aufrufpfad existiert nicht. Falls die Suche einen findet: Rückfrage, nicht Reparatur.
- **Layer 03** bekommt seinen eigenen Vermerk in einem eigenen Durchgang. Hier wird nichts für
  `profiles/` vorbereitet.
- **Keine Änderung an `Group`, `build_groups`, `graph.py`, `flow.py`, `relax.py`.** Der Vermerk
  fließt über den bestehenden Pfad `findings.append(Finding(kind=…, subject=cid)); continue`.

---

## 5. Tests

### 5.1 Einheitsvektoren auf `_decode_weight` (`tests/trust/test_payload.py`)

Alle mit `D = 100`. Die `v`-Werte sind **rohe Bytes**, nicht über `cbor_canon.encode` erzeugt —
das ist der Punkt der Übung.

| ID | `v` (hex) | dekodiert zu | erwartete Rückgabe |
|---|---|---|---|
| `V-CANON-1` | `a100190064` | `{0: 100}` | `(None, NON_CANONICAL_V)` |
| `V-CANON-2` | `bf001864ff` | `{0: 100}` | `(None, NON_CANONICAL_V)` |
| `V-CANON-3` | `a20901001864` | `{9: 1, 0: 100}` | `(None, NON_CANONICAL_V)` |
| `V-CANON-4` | `a2001864001865` | `{0: 101}` | `(None, NON_CANONICAL_V)` |
| `V-CANON-5` | `a1001864` | `{0: 100}` | `(100, None)` |
| `V-CANON-6` | `a1` | — | `(None, UNPARSABLE_VOUCH_PAYLOAD)` |

`V-CANON-1` bis `V-CANON-3` decken die drei harmlosen Verstoßklassen ab: nicht-minimale
Ganzzahl, indefinite-length Map, unsortierte Schlüssel. `V-CANON-3` zeigt zusätzlich, dass
Zusatzkeys die Ordnung nicht entschuldigen — `{9: 1, 0: 100}` ist inhaltlich zulässig (D37:
„weitere Keys sind unschädlich"), aber falsch kodiert; kanonisch wäre `a20018640901`.

**`V-CANON-4` ist der Vorrangvektor.** Er ist der einzige, der die richtige von der plausiblen
Reihenfolge trennt: `n = 101 > D` würde ohne die Kanonizitätsprüfung `INVALID_VOUCH_WEIGHT`
liefern. Die Wirkung ist in beiden Fällen dieselbe, der Vermerk nicht.

**`V-CANON-6` ist der eigentliche Abnahmevektor.** Er prüft nicht die neue Regel, sondern dass
die neue Regel die alte nicht zertrampelt hat. Er muss einen Vermerk liefern, keine Exception.

### 5.2 Ein End-zu-End-Vektor

`V-CANON-E2E`: derselbe Vouch wie in einem bestehenden Zwei-Knoten-Anker, aber mit
`v = h'a100190064'` statt `h'a1001864'`. Erwartet:

- `trust()` auf den Gebürgten liefert **0** (die Kante existiert nicht),
- `TrustResult.findings` enthält `Finding(NON_CANONICAL_V, claim_id(vouch))`,
- der Autor erhält **keinen** `OVERCOMMITTED_AUTHOR`-Vermerk aus diesem Vouch (kein
  Budget-Beitrag).

Der Vektor trägt, was die Einheitstests nicht können: dass der Vermerk durch `build_groups`,
`derive()` und die Sortierung/Deduplizierung bis ins Ergebnisobjekt durchkommt und die Kante
tatsächlich aus dem Graphen verschwindet.

### 5.3 Hilfsmittel

`tests/helpers.py` erzeugt `v` heute ausschließlich über `cbor_canon.encode(payload)`. Für
`V-CANON-E2E` wird ein Weg gebraucht, **rohe** `v`-Bytes anzuhängen — z. B. ein optionaler
Parameter `v_raw: bytes | None = None`, der `payload` vorgeht. Bestehende Aufrufe bleiben
unverändert.

Das ist bewusst so formuliert und nicht ausgeführt: wenn sich beim Bauen zeigt, dass der
Helfer anders geschnitten ist als hier vermutet, ist das eine **Rückfrage**, keine Umdeutung
des Vektors.

---

## 6. Abnahme

1. `make check` grün in allen drei Blöcken.
2. **242 Tests** (235 + 6 + 1). Keiner der 235 bestehenden ist geändert, übersprungen oder
   angepasst worden.
3. `git diff --stat` zeigt **genau vier** Dateien: `trust/findings.py`, `trust/groups.py`,
   `tests/trust/test_payload.py`, `tests/helpers.py`. Jede weitere Datei ist zu begründen,
   bevor gemergt wird.
4. `git status` ohne unversionierte Quelldateien — `tools/check_tree.py` bricht sonst ohnehin ab.
5. Ein frischer Clone des Branches ist grün.

---

## 7. Rückfragen

Jede Frage, die beim Bauen aufkommt und in `02 §3.1` keine Antwort hat, ist eine **Spec-Lücke**
und geht zurück ins Spec-Gespräch — nicht im Implementierungsfenster entscheiden. Das gilt
besonders für: weitere Aufrufstellen von `cbor_canon.decode`, die `v` lesen; Verhalten bei
`v = b""`; und jede Stelle, an der die drei Randbedingungen aus `§3.1` einander zu
widersprechen scheinen.
