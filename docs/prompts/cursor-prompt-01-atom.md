# Cursor-Prompt — Referenzimplementierung Schicht 01 (Claim-Atom + Verifizierer)

> **So benutzt du das:** Öffne das Repo `mensch-als-republik` in Cursor, öffne `01-claim-atom.md`
> im Kontext (mit `@01-claim-atom.md`), und füge den Block unter „PROMPT" als Aufgabe ein. Der
> Prompt ist bewusst eng: **nur** Schicht 01. Trust-Flow, Profile etc. kommen in späteren Prompts.

---

## PROMPT

**Rolle.** Du implementierst die Referenz-Python für „Mensch als Republik", ein dezentrales
Koordinationsprotokoll. Die **normative Wahrheit** ist die Datei `@01-claim-atom.md` im Repo. Wenn
dein Code und die Spec je in Konflikt geraten, **gewinnt die Spec** — weiche nie eigenmächtig ab,
sondern melde den Konflikt.

**Ziel dieser Aufgabe.** Implementiere das **Claim-Atom** und den **Verifizierer** aus Schicht 01,
sodass die **Test-Vektoren aus Anhang C der Spec** exakt reproduziert werden und alle
Verifizierer-Regeln (§6 + Anhang B) greifen. Das Kriterium für „fertig" ist: die Vektoren stimmen
byte-genau und die Zustandsmaschine klassifiziert korrekt.

**Nicht-Ziele (bewusst außerhalb dieser Aufgabe).**
- **Keine** anderen Schichten (kein Trust-Flow, keine Profile über `vouch`/`accept-rules` hinaus als
  *Interpretation* — das Atom kennt nur Prädikat-*Strings*, keine soziale Bedeutung).
- **Kein** neues Atom-Feld, keine Key-Rotation, keine Delegation (Spec §8).
- **Keine** Wall-Clock-Ordnung: `t` ist nie ein Ordnungsprimitiv (§5.3). Ordnung kommt aus `h_prev`.
- Die bestehende `trust_flow.py` **nicht** anfassen (sie hat einen bekannten Bug, den wir separat in
  der 02-Aufgabe fixen).

**Abhängigkeiten (pinnen — kritisch für Reproduzierbarkeit).**
- Deterministisches CBOR: **`cbor2`** mit `canonical=True` ist DER kanonische Encoder dieser
  Referenz. Alle Vektoren wurden damit erzeugt. Implementiere zusätzlich den in §3 geforderten
  **Re-Serialisierungs-Check** (empfangene Bytes → dekodieren → kanonisch re-enkodieren →
  byte-genau vergleichen; Abweichung ⇒ `NON_CANONICAL_ENCODING`).
- Ed25519: **`cryptography`** (`cryptography.hazmat.primitives.asymmetric.ed25519`). Ed25519 ist
  deterministisch (RFC 8032), die Signatur-Vektoren stimmen also unabhängig von der Lib.
- Python ≥ 3.11, `pytest`. Keine weiteren Laufzeit-Deps ohne Rückfrage.

**Modul-Layout (erstellen).**
```
mensch_als_republik/
  __init__.py
  domains.py        # die drei Domänen-Separatoren als Konstanten
  cbor_canon.py     # kanonische Enkodierung + Re-Serialisierungs-Check
  predicates.py     # Grammatik (Anhang A), Namensraum/Scope-Parsing, Bindungsregel
  atom.py           # Claim-Datenstruktur, core-Bytes, claim_id, id-genesis, sign, verify
  verifier.py       # Fehlerklassen, strukturelle Gültigkeit, Zustandsmaschine, Aktiv-Set
tests/
  vectors/
    gen.py          # reproduziert die Vektoren aus Anhang C (feste Seeds)
    vectors_01.json # von gen.py erzeugt; die Golden-Fixtures
  test_cbor_canon.py
  test_atom.py
  test_predicates.py
  test_verifier.py
  test_vectors_01.py
```

**Präzise Anforderungen.**

1. `domains.py` — exakt diese Byte-Strings (gehen in Hashes/Signaturen ein, dürfen sich **nicht**
   ändern):
   ```
   DOM_SIG    = b"claim-atom/v1/sig"
   DOM_CID    = b"claim-atom/v1/cid"
   DOM_ID_GEN = b"claim-atom/v1/id-genesis"
   ```
   (`DOM_NUC_GEN = b"claim-atom/v1/nucleus-genesis"` gehört in die Governance-Schicht 00 und wird
   hier **nur** in `tests/vectors/gen.py` zum Reproduzieren von `N` verwendet, nicht im Atom-Code.)

2. `atom.py` — eine `Claim`-Struktur mit den Feldern aus §2 (CBOR-Keys 0–9). Funktionen:
   - `core_map(claim) -> dict[int, ...]` — Keys 0–8, **ohne** `σ`; abwesende optionale Felder
     lassen ihren Key weg (kein `null`, §3 Regel 5).
   - `core_bytes(claim) -> bytes` — `cbor_canon.encode(core_map(claim))`.
   - `claim_id(claim) -> bytes` — `sha256(DOM_CID + core_bytes)`; **signatur-unabhängig** (§4).
   - `sign(sk, claim) -> bytes` — `Ed25519-Sign(sk, DOM_SIG + core_bytes)`.
   - `verify_sig(claim) -> bool` — `Ed25519-Verify(I, DOM_SIG + core_bytes, σ)`.
   - `id_genesis_anchor(I: bytes) -> bytes` — `sha256(DOM_ID_GEN + I)`.
   - `is_equivocation_pair(c1, c2) -> bool` — `c1.claim_id != c2.claim_id` **und** gleiches
     `(I, h_prev)` (§4).

3. `predicates.py` — Grammatik aus Anhang A als Regex, **inklusive** der 64-Hex-Reservierung:
   - `parse_predicate(p) -> (namespace, name, version)` oder Fehler.
   - Nur `core` und `nuc:<scope>` sind gültige Namensräume; alles andere ⇒ `UNKNOWN_NAMESPACE`
     (§2.2). `core` nur mit Name ∈ `{revoke, supersede}`, sonst `RESERVED_CORE_PREDICATE`.
   - `resolve_scope(claim) -> bytes` und die **Bindungsregel** §2.2 Regel 3: bei kanonischer
     Hex-Kodierung MUSS `N == bytes.fromhex(scope_hex)`; bei Alias ist `N` die einzige Quelle;
     `nuc:` ohne `N` ⇒ `BAD_SCOPE_BINDING`. Alias darf `^[0-9a-f]{64}$` **nicht** matchen.

4. `verifier.py` — Fehlerklassen als Enum/Exceptions **exakt** nach Anhang B
   (`UNSUPPORTED_VERSION`, `NON_CANONICAL_ENCODING`, `MALFORMED_CBOR`, `UNKNOWN_J_TAG`,
   `UNKNOWN_NAMESPACE`, `BAD_SCOPE_BINDING`, `RESERVED_CORE_PREDICATE`, `FOREIGN_LIFECYCLE`,
   `BAD_SIGNATURE`, `INVALID_GENESIS_ANCHOR`, `INCOHERENT_EXPIRY`). Dann:
   - `structural_check(bytes) -> Claim` — führt §6 Punkte 1–7 in dieser Reihenfolge aus; wirft die
     passende Fehlerklasse. Enthält den `h_prev == 32×0x00` ⇒ `INVALID_GENESIS_ANCHOR`-Reject, den
     `t < t_exp`-Check (`INCOHERENT_EXPIRY`), und den Re-Serialisierungs-Check.
   - Zeit ist **lokal/subjektiv**: `now` ist ein **Parameter** (kein Zugriff auf die Systemuhr im
     Kern). Fehlt `now`, ist die `t_exp`-Auswertung **unentscheidbar** → Claim gilt für
     trust-gewährende Zwecke als nicht nutzbar (nicht: Reject). Bilde das über einen expliziten
     Zustand/Flag ab, nicht über eine Exception.
   - `classify(claim, store, now=None) -> State` — die Zustandsmaschine aus Anhang B:
     `malformed | pending | linked | active | revoked | superseded | expired | equivocation_flagged`.
     `pending` = strukturell gültig, aber `h_prev`-Vorgänger **nicht** im `store` (Partial-Sync) →
     **halten**, nicht ablehnen. `store` ist ein einfaches In-Memory-Interface
     (`get(claim_id)`, `by_author_hprev(I, h_prev)`, `add(claim)`), gegen das getestet wird.
   - `core/*`-Claims: `t_exp` **ignorieren** (Monotonie §5.3). `core/revoke`/`supersede` müssen
     `ziel.I == C.I` erfüllen, sonst `FOREIGN_LIFECYCLE`.
   - **Idempotenz:** ein bereits bekannter `claim_id` erneut `add` = No-op, kein Fehler.

**Golden-Werte (müssen exakt herauskommen; Quelle: Spec Anhang C, hier zur Test-Verankerung).**
```
Seeds:  ALICE = 0x01*32   BOB = 0x02*32
ALICE(pub) = 8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c
BOB(pub)   = 8139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b394

id_genesis_anchor(ALICE) = 62db0b05f44c17e2dfe7f371d631845fdd5858dd94c37d327a28f73b25625430
id_genesis_anchor(BOB)   = d507038f3b07c8642b65e9b3cf559204d9ad7aa0a3faee674d4284a5d9e43abe

Beispiel-Nukleus (aus 00 §3.1; via DOM_NUC_GEN reproduzierbar):
N     = 65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557
CONST = 890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e6585c352dcf19ccad5ea7e

claim_id-Erwartungen:
TV1 = f95d430e40df736cbdffd7bf82af4f77e0c7af8692565f3b2a151c2c1ae8660c
TV2 = 29b66881810bbbf1e254e061c35395e15da6c064327c2d33dfa6aa29d47dc2a6
TV3 = 8e76a2a9ee6677e6959bf9868dc6d162e5ff7e464a6bb4c6b839f89713e54629
TV4 = 0bd77591da5e480a8c9a573382d14407a1770e0a7f6d2d09776b630fbd7ca01c
NV1 = 9b25020fee7da6832416f8bcb61e4a05329776d051a4da282db7e973eb96c453   (malformed)
NV3 = e14ebd82eb172672a4a3ccbc330fef64fecd86e4664f72eab538855c9cef5c8b   (equivocation mit TV1)
```

**Akzeptanzkriterien (Tests müssen grün sein).**
- `tests/vectors/gen.py` reproduziert aus den festen Seeds **byte-genau** die `bytes`, `claim_id`
  und `σ` aller Vektoren aus Anhang C und schreibt `vectors_01.json`. Ein Test vergleicht die
  regenerierten `claim_id` mit den Golden-Werten oben.
- **TV1–TV4**: `structural_check` bestehen; `classify` ergibt `active` (bei vorhandenem Vorgänger im
  `store`), bzw. `pending`, wenn der Vorgänger fehlt. TV3 ist ein gültiger selbst-bezüglicher
  `core/revoke@1` und setzt TV1 auf `revoked`.
- **NV1**: `structural_check` wirft `INVALID_GENESIS_ANCHOR` (**nicht** `pending`), obwohl die
  Signatur gültig ist.
- **NV2** (nicht-kanonisches CBOR desselben Cores): `structural_check` wirft
  `NON_CANONICAL_ENCODING`; ein zusätzlicher Test zeigt, dass `reserialize(decode(nv2)) == TV1.bytes`
  (gleicher Core, nur falsch kodiert).
- **NV3**: bildet mit TV1 ein `is_equivocation_pair`; beide bleiben im `store`, Autor wird
  `equivocation_flagged`; Downstream-Claims werden **nicht** rückwirkend invalidiert.
- **Idempotenz/Replay**: TV1 zweimal `add` = No-op.
- **Negative Grammatik-Tests**: `svc:...`/`foo:...` ⇒ `UNKNOWN_NAMESPACE`; `core/vouch@1` ⇒
  `RESERVED_CORE_PREDICATE`; `nuc:<falsches-N>/vouch@1` ⇒ `BAD_SCOPE_BINDING`; ein Alias, der
  zufällig 64 Hex ist, wird abgelehnt/als kanonisch behandelt (deine Regel, dokumentiert).

**Vorgehen.**
1. Lies `@01-claim-atom.md` vollständig, besonders §3, §4, §6, Anhang A, Anhang B, Anhang C.
2. Baue zuerst `cbor_canon.py` + `domains.py` + `atom.py`, dann `tests/vectors/gen.py`, und
   verifiziere die Golden-`claim_id` — **bevor** du den Verifizierer baust.
3. Dann `predicates.py`, dann `verifier.py`, dann die restlichen Tests.
4. Halte Funktionen klein und rein; `now` immer als Parameter, nie aus der Systemuhr im Kern.
5. Wenn eine Spec-Stelle mehrdeutig ist: **stopp und frag**, statt zu raten. Erfinde keine Felder,
   keine zusätzlichen Prädikate, keine Wall-Clock-Ordnung.

**Definition of Done.** `pytest` grün; `gen.py` reproduziert Anhang C byte-genau; alle Fehlerklassen
aus Anhang B haben mindestens einen positiven und einen negativen Test; keine Änderung an
`trust_flow.py`; kein neues Atom-Feld.
