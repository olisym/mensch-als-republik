# `03` — Profile II: Verdikt · Wert · Mitgliedschaft

Auftrag an den Implementierer. Normative Quelle: `03-profiles.md` und `03-golden-anchors.md`;
Register D55–D69, D77–D87.

Diese Schicht rechnet nicht. Sie hat keinen Graphen, keine Kapazitäten, keine Anker und keine
`TrustParams`. Sie ist **Komposition über Layer 01 plus Policy**: vier Funktionen, die Claims im
Store zueinander in Beziehung setzen und einen Zustand plus Vermerke zurückgeben.

Die Vektoren stehen vollständig in `03-golden-anchors.md`. Dieser Prompt sagt, wo der Code
hingehört und welche Fallen die Vektoren stellen — er wiederholt die Vektoren nicht.

---

## 0. Vorarbeit: `classify_all` verschieben und erweitern (D86, D87)

**Zuerst, in einem eigenen Commit, vor allem anderen.**

1. `mensch_als_republik/trust/index.py` → `mensch_als_republik/index.py`.
2. `trust/__init__.py` re-exportiert `classify_all` weiter aus dem neuen Ort. Die öffentliche
   Oberfläche von `trust` bleibt unverändert.
3. `trust/derive.py` importiert aus dem neuen Ort.
4. Signatur wird `classify_all(store, now, policy=None)`. Der Parameter geht an dieselbe
   Stelle, an der `verifier.classify` ihn auswertet — nicht an eine zweite, nachgebaute.
5. **Die Policy wird scope-lokal angewandt** (`03 §6`): sie geht an `nuc:`-Claims mit
   `N == policy.scope`, alle übrigen werden mit `None` klassifiziert. Ein Store trägt Claims
   mehrerer Nuklei; ein Wächter, der bei fremdem Scope wirft, machte ihn unklassifizierbar, und
   `SE-5`, `MB-9`, `VS-7` verlangen fremd-gescopte Claims ausdrücklich im selben Store.
6. Der Kopplungstest `T-02.4` bekommt einen zweiten Fall **mit** Policy, zweiteilig nach
   `PR-INV-11`; dazu `PR-INV-12` an einem Store aus `N_A`, `N_B` und `N_C` gemischt.

**Abnahme dieses Schritts einzeln:** 242 Tests grün, keiner geändert außer der Erweiterung von
`T-02.4`, keine Verhaltensänderung in `trust/`. Layer 02 ruft weiterhin ohne `policy` auf.

Warum das nicht optional ist: ohne den Parameter liefert `classify_all` für `SE-11` — Schuldner
widerruft seine eigene Obligation — den Zustand `REVOKED`, und `settlement()` bekäme einen
Zustand, für den §3.3.2 keine Antwort vorsieht. Das Schulden-Lösch-Loch stünde über den Umweg
des Helfers wieder offen.

---

## 1. Was diese Schicht **nicht** ist

- **Kein zweites `classify`.** Die Definition von „aktiv" kommt aus Layer 01 über
  `classify_all`. Wer sie hier nachbaut, erzeugt genau die Drift, gegen die `T-02.4` gebaut
  wurde.
- **Keine Bedeutung.** `amount` wird nie gelesen, nie verglichen, nie summiert; `unit_ref` nie
  dereferenziert; `outcome` nie interpretiert. Wo ein reservierter Key geprüft wird, wird sein
  **Typ** geprüft, nie sein Wert (Ausnahme: die bloße *Anwesenheit* von `receipt.v` Key `0`).
- **Keine Reject-Codes.** `errors.py` bleibt bei elf. Alles, was diese Schicht findet, ist ein
  Vermerk.
- **Keine Auflösung von Autorität.** `authorized_keys` und `arbitrators` sind Parameter.
  `resolve_current_key` existiert nicht und wird nicht vorbereitet.
- **Keine Governance.** Ob ein Verfassungsobjekt die *aktuelle* Version ist, entscheidet die
  Ratifizierung. Diese Schicht vergleicht Hashes byte-weise.

---

## 2. Modulschnitt

```
mensch_als_republik/index.py            classify_all(store, now, policy=None)   ← aus §0
mensch_als_republik/profiles/
  __init__.py    öffentliche Oberfläche
  findings.py    ProfileFinding, Finding(kind, subject)
  payload.py     v lesen (§3.1)
  policy.py      resolve_policy() -> PolicyResolution
  membership.py  membership()     -> MembershipResult
  credit.py      settlement()     -> SettlementResult
  verdict.py     verdict_status() -> VerdictStatus
```

Abhängigkeiten zeigen nach unten: `profiles/*` benutzt `atom`, `cbor_canon`, `policy`,
`predicates`, `verifier`, `index`. **Kein** Import aus `trust/`.

`Finding` ist dieselbe Bauform wie in `trust/findings.py` — `@dataclass(frozen=True,
slots=True, order=True)` mit `kind: ProfileFinding` und `subject: bytes`. Eigener Enum, gleiche
Form. `findings` ist überall sortiert und dedupliziert, und **jeder** der vier Ergebnistypen
trägt sie.

`subject` ist in der Regel eine `claim_id`. Wo kein Claim betroffen ist, ist es das Objekt, um
das es geht — bei `CONSTITUTION_UNAVAILABLE` und `CONSTITUTION_HASH_MISMATCH` der im Genesis
**deklarierte** `constitution_hash` (`genesis_obj[4]`), nicht der berechnete Hash des
übergebenen Objekts und nie ein Leerwert.

---

## 3. Gemeinsame Bausteine

### 3.1 `payload.py` — `v` lesen

Eine Funktion, von allen drei Clustern benutzt. Sie ist die Stelle, an der `03 §1.3` und D77/D83
zusammenkommen, und die Reihenfolge ist normativ:

```python
def read_v(v: bytes | None) -> tuple[dict | None, tuple[ProfileFinding, ...]]
```

1. `v is None` → `(None, ())`. Kein Fehler; kein Key dieser Schicht ist Pflicht.
2. Rundlauf `decode → is_canonical` im **selben** `try`. Jede Exception →
   `(None, (UNPARSABLE_V,))`.
3. `not canonical` → `(None, (NON_CANONICAL_V,))`.
4. Kein `dict` → `(None, (UNPARSABLE_V,))`.
5. Sonst `(obj, ())`.

Die Vorlage steht in `trust/groups.py::_decode_weight` und ist dort seit `02c` korrekt. **Nicht
importieren** — sie liefert `n`, nicht die Map, und ihre Wertprüfungen sind Layer-02-Semantik.
Die Reihenfolge ist zu übernehmen, nicht der Code.

Typprüfung reservierter Keys geschieht beim jeweiligen Leser, nicht hier: fehlender Key ist kein
Fehler, falscher Typ erzeugt `INVALID_V_TYPE` und lässt den Key wegfallen.

**`h'ff'` und `h'a100ff'` sind die Vektoren, die Schritt 2 von Schritt 4 trennen.** Beide
dekodieren ohne Fehler, das zweite sogar zu einem `dict`; erst das Re-Enkodieren wirft. Eine
Implementierung, die `is_canonical` hinter die `dict`-Prüfung schiebt, ist bei `h'a100ff'` rot.

### 3.2 Scope-Gleichheit

Jede Beziehung zwischen zwei Claims verlangt `a.N == b.N == scope` (`03 §1.4`). Das ist **nicht**
von Layer 01 abgedeckt: `01 §2.2` Regel 3 erzwingt nur, dass `N` gesetzt und selbstkonsistent
ist. Ein Verstoß erzeugt `SCOPE_MISMATCH`, und der betroffene Claim **zählt nicht** — er wird
nicht etwa mit Vermerk gewertet.

### 3.3 Prädikatnamen

Prädikate dieser Schicht heißen `nuc:{scope.hex()}/{name}@1`, wie `vouch@1` in
`tests/helpers.py::vouch_raw`. Zum Vergleich `parse_predicate` benutzen, nicht Stringvergleich
auf dem ganzen `p`.

`J`-Tags nach `01 §2.2`: `1 = identity`, `2 = claim-ref`, `3 = object-hash`.

---

## 4. `profiles/policy.py`

```python
@dataclass(frozen=True, slots=True)
class PolicyResolution:
    policy: NucleusPolicy
    findings: tuple[Finding, ...]

def resolve_policy(*, scope: bytes, genesis_obj: dict,
                   constitution_obj: dict | None = None) -> PolicyResolution
```

`NucleusPolicy` wird aus `mensch_als_republik.policy` **importiert**, nicht neu definiert. Die
Normalisierung (Boden D70, Negativliste D58, `core`-Filter D71) geschieht in ihrem Konstruktor
und wird hier nicht wiederholt.

**Der Resolver rechnet nach** (D82):

| Lage | Antwort |
|---|---|
| `scope != SHA-256(DOM_NUC_GEN ‖ cbor(genesis_obj))` | `ValueError` |
| `constitution_obj is None` | Sicherheits-Default, `CONSTITUTION_UNAVAILABLE` |
| `genesis_obj[4] != SHA-256(cbor(constitution_obj))` | Sicherheits-Default, `CONSTITUTION_HASH_MISMATCH` |
| beides passt | `NucleusPolicy(scope, declared=frozenset(irrevocable_predicates))` |

> **Nachtrag (D167, D168).** `constitution_hash` ist Parameter von `resolve_policy`;
> `genesis_obj[4]` wird nicht mehr gelesen und deshalb auch nicht geprüft. Die dritte Zeile der
> Tabelle ist `ValueError` statt Vermerk, `CONSTITUTION_HASH_MISMATCH` entfällt ersatzlos, und
> das Subjekt von `CONSTITUTION_UNAVAILABLE` ist der übergebene Hash, nicht `genesis_obj[4]`.
> Der Wortlaut oben bleibt stehen, weil dieser Prompt erteilt ist; normativ gilt
> `03-profiles.md §1.2`.

Sicherheits-Default heißt `NucleusPolicy(scope, declared=frozenset())` — der Boden setzt
`{obligation@1}` von selbst. **Nicht** `{"obligation@1"}` von Hand übergeben; das schriebe den
Boden ein zweites Mal auf.

> **Nachtrag (D153).** Der Boden trägt seit D153 zusätzlich `rotate-key@1` und `rotate-ack@1`.
> Die Anweisung bleibt unverändert richtig: nichts von Hand übergeben.

Fehlt der Key `irrevocable_predicates` in einem vorhandenen Verfassungsobjekt, ist das
**kein** Sonderfall und **kein** Vermerk: `declared` ist leer, der Boden greift. Das ist Profil C
und der Grund, warum `P-A`, `P-C` und `P-D` dieselbe Menge und verschiedene Vermerke liefern.

**`findings` trägt nur Auflösungsbefunde** (D84). `UNSAFE_IRREVOCABLE_PREDICATE` wird **nicht**
hierher übersetzt — er lebt als `PolicyNote` in `policy.warnings`. Eine Diagnose, ein Produzent.

---

## 5. `profiles/membership.py`

```python
def membership(store, *, subject: bytes, scope: bytes, constitution_hash: bytes,
               now: int, authorized_keys: frozenset[bytes],
               policy: NucleusPolicy | None = None) -> MembershipResult
```

`MembershipResult` trägt `state: MembershipState`, `accept_claim_id: bytes | None`,
`grant_claim_id: bytes | None`, `findings: tuple[Finding, ...]`.

Ein `accept-rules@1` zählt, wenn er aktiv ist, `I == subject`, `N == scope` und
`J == (3, constitution_hash)`. Ein `grant-membership@1` zählt, wenn er aktiv ist,
`J == (1, subject)`, `N == scope` und `I ∈ authorized_keys`.

Zählt einer nicht, ist **der Grund zu vermerken** und nicht nur die Wirkung:
`CONSTITUTION_VERSION_MISMATCH`, `UNAUTHORIZED_GRANT_AUTHOR`, `SCOPE_MISMATCH`.

Vier Zustände aus der Konjunktion. `MB-5` und `MB-6` sind das Paar, für das es vier gibt:
Austritt liefert `GRANT_ONLY`, Ausschluss `APPLICANT`. Ein `bool` macht beide zu `False`, und
`05 §1` Stufe 4 muss sie unterscheiden können.

Gibt es **mehrere** zählende Claims derselben Art — etwa zwei aktive `accept-rules` auf
denselben Hash —, ist der Zustand davon unberührt; welche `claim_id` im Ergebnis steht, ist die
lexikographisch kleinste. Das ist dieselbe Tie-Break-Regel wie in `groups.py::build_groups`,
und sie steht hier, damit das Ergebnis deterministisch ist, nicht weil der Fall häufig wäre.

---

## 6. `profiles/credit.py`

```python
def settlement(store, *, obligation: Claim, scope: bytes, now: int,
               policy: NucleusPolicy) -> SettlementResult
```

**`policy` ohne Default** (D80) — als einzige Funktion dieser Schicht. `membership()` und
`verdict_status()` behalten `policy=None`. Die Asymmetrie ist Absicht und in `03 §5` begründet;
sie ist nicht zu „vereinheitlichen".

`SettlementResult` trägt `state: SettlementState`, `receipt_claim_id: bytes | None`,
`findings: tuple[Finding, ...]`.

### 6.1 Zustandsbestimmung

Erst der Zustand der Obligation aus `classify_all(store, now, policy)`:

| Zustand der Obligation | Ergebnis |
|---|---|
| `ACTIVE` | weiter zu §6.2 |
| `EXPIRED` | `EXPIRED` |
| `PENDING` | `INDETERMINATE` + `OBLIGATION_PENDING` |
| `EQUIVOCATION_FLAGGED` | `INDETERMINATE` + `OBLIGATION_AUTHOR_FLAGGED` |
| `REVOKED`, `SUPERSEDED`, `LINKED` | **unerreichbar** — `assert`, kein Zweig |

Der `assert` ist die Zusicherung einer Unmöglichkeit, nicht ein Test einer Semantik (D75):
`revoked`/`superseded` sind unter dem Boden aus D70 nicht erreichbar, `linked` nur bei
`now is None`, und `now` ist hier immer ein `int`.

Ist `obligation` kein `obligation@1` im Scope: `ValueError`, vor jedem Store-Zugriff.

### 6.2 Passende Quittung

Vier Bedingungen (D63), alle vier notwendig:

```
R.J  == (2, claim_id(O))
R.I  == O.J[1]   und  O.J[0] == 1
R.N  == O.N      und  O.N == scope
R aktiv
```

Die dritte ist nicht redundant. Ohne sie quittiert eine Identität in Nukleus B eine Schuld aus
Nukleus A (`SE-5`).

Dann `read_v(R.v)`:

- Ergebnis `None` (unlesbar) → **tilgt nicht**, `PARTIAL_RECEIPT_UNSUPPORTED` **zusätzlich** zum
  Vermerk aus `read_v`. Beide erscheinen. Ein unlesbares `v` *könnte* Key `0` tragen, und die
  sichere Richtung ist, das anzunehmen (`03 §1.3`).
- Key `0` vorhanden → tilgt nicht, `PARTIAL_RECEIPT_UNSUPPORTED`.
- Key `0` vorhanden mit falschem Typ → tilgt nicht, `PARTIAL_RECEIPT_UNSUPPORTED` **und**
  `INVALID_V_TYPE`. „Trägt Key `0`" ist eine Frage der Anwesenheit, nicht des Typs.
- sonst → `SETTLED`.

`CV-1` bis `CV-4` prüfen den ersten Punkt und erwarten **zwei** Vermerke. Eine Implementierung,
die beim ersten abbricht, hat die richtige Wirkung und die falsche Diagnose.

---

## 7. `profiles/verdict.py`

```python
def verdict_status(store, *, verdict: Claim, scope: bytes,
                   arbitrators: frozenset[bytes], now: int,
                   policy: NucleusPolicy | None = None) -> VerdictResult
```

`VerdictResult` trägt `status: VerdictStatus` und `findings: tuple[Finding, ...]`.
`VerdictStatus` hat zwei Werte, `BINDING` und `ATTRIBUTED_OPINION` — kein dritter. Die Vermerke
tragen den Grund; `VS-7`, `VS-8` und `VS-9` wären ohne diesen Kanal nicht prüfbar.

```
BINDING  gdw.  verdict aktiv  und  ( (i) oder (ii) )

(i)   verdict.I ∈ arbitrators
(ii)  für beide Parteien P: ein aktiver Claim S mit
          S.p == nuc:{scope}/submit-arbitration@1
          S.I == P
          S.J == (1, verdict.I)
          S.N == scope
```

Parteien (D67 b): Ankläger ist `accusation.I`. Beschuldigter ist `accusation.J[1]`, falls
`accusation.J[0] == 1`; sonst der **Autor** des Claims mit `claim_id == accusation.J[1]`.

Die Anklage wird über `verdict.J` gefunden. Nicht auflösbar heißt: `verdict.J[0] != 2`, Anklage
lokal unbekannt, `accusation.N != scope`, oder der bestrittene Claim lokal unbekannt. Dann ist
**Pfad (ii) nicht auswertbar**, Pfad (i) bleibt es. Vermerke: `UNKNOWN_ACCUSATION`,
`UNRESOLVED_ACCUSED`, `SCOPE_MISMATCH`.

**Drei Fallen, jede mit einem Vektor:**

- **Der Zustand der Anklage ist irrelevant** (`VS-10`). Sie wird nur gelesen, um die Parteien zu
  bestimmen. Wer sie auf „aktiv" prüft, ist hier rot.
- **Ein inaktives Verdikt liefert `ATTRIBUTED_OPINION` mit `INACTIVE_VERDICT`** (`VS-9`) — kein
  dritter Rückgabewert.
- **„Vorab" heißt „aktiv zum Bewertungszeitpunkt"** (`VS-6`, D78). Eine widerrufene Unterwerfung
  bindet nicht. Wer „irgendwann einmal ausgestellt" liest, ist hier rot.

Pfad (i) ist ein **Byte-Vergleich**. Keine Schlüsselauflösung, kein `authorized_keys`; ein
FROST-Panel verifiziert als gewöhnliche Ed25519-Signatur unter seinem Gruppenschlüssel.

---

## 8. Tests

### 8.1 Fixtures — `tests/profiles/fixtures.py`

Die Scopes dieser Schicht sind **echte Genesis-Hashes**, nicht `scope_id(label)`. Zu bauen:

- `ALICE`, `BOB` wie bisher aus `tests/helpers.py::Identity`; **`CAROL`** kommt dazu.
- Die drei Verfassungs- und Genesis-Objekte aus `03-golden-anchors.md §2` und `§3`.
- `N_A`, `N_B`, `N_C` **berechnet**, nicht als Konstante eingetragen — und in einem Test gegen
  die Werte aus dem Ankerdokument geprüft. Das ist der Anker: stimmen die berechneten Hashes
  nicht mit den dokumentierten überein, ist die Kodierung falsch, und alles Weitere wäre
  Selbstbestätigung.

`helpers.Identity` leitet den Schlüssel bisher aus dem **Label** ab und trifft die normativen
Seeds `01×32`/`02×32` damit nicht. Der Konstruktor bekommt deshalb einen optionalen Seed:

```python
class Identity:
    def __init__(self, label: str, *, seed: bytes | None = None) -> None:
```

Bei `seed is None` bleibt alles, wie es war; bestehende Aufrufe ändern sich nicht. Kein zweiter
Identity-Typ für `tests/profiles/` — zwei Implementierungen von Kettenfortführung und Signatur
driften, aus demselben Grund, aus dem `classify_all` geteilt und nicht kopiert wird.

**Die drei Seeds bekommen genau eine Definition.** Erzeugt `tests/vectors/gen.py` sie heute
selbst, kommen sie ab jetzt aus `tests/helpers.py`. Zwei Stellen mit denselben Konstanten sind
die Bauform, die in dieser Sitzung viermal einen Befund erzeugt hat.

Claims jenseits von `vouch@1` baut `Identity.claim(p=…, J=…, t=…, v=…, N=…, t_exp=…)`, das
bereits existiert. `store_with(*claims)` wie gehabt.

### 8.2 Vektoren → Dateien

| Datei | Vektoren aus `03-golden-anchors.md` |
|---|---|
| `tests/profiles/test_policy.py` | `P-A` … `P-F` (§4) |
| `tests/profiles/test_payload.py` | `TV-O1`, `TV-R0/1/2`, `TV-V1`, `TV-T1` (§5), `CV-1` … `CV-6` (§6) |
| `tests/profiles/test_membership.py` | `MB-1` … `MB-9` (§7) |
| `tests/profiles/test_credit.py` | `SE-1` … `SE-12` (§8) |
| `tests/profiles/test_verdict.py` | `VS-1` … `VS-11` (§9) |
| `tests/profiles/test_invariants.py` | `PR-INV-1` … `PR-INV-11` (§11) |

Die Byte-Vektoren aus §5 und §6 sind als **Hex-Literale** zu schreiben, nicht über
`cbor_canon.encode` zu erzeugen. Ein Vektor, der sein eigenes Sollergebnis berechnet, prüft
nichts.

### 8.3 Invarianten

`PR-INV-1` ist ein Eigenschaftstest über alle drei Profile plus die fehlende Verfassung, kein
vierter Einzelvektor: der Boden gilt unbedingt, und „unbedingt" ist eine Aussage über alle
Eingaben.

`PR-INV-5` prüft, dass `settlement()` ohne `policy` einen `TypeError` wirft und die beiden
anderen ihn nicht werfen.

`PR-INV-10` ist ein Identitätsvergleich der Funktionsobjekte, kein Verhaltensvergleich.

---

## 9. Ausdrücklich nicht in diesem Schritt

- **Der Kompositionspfad aus `04 §3`** (`vote_mode = 0`): Mitgliedschaft ohne einzelnen
  `grant-membership`-Autor. Nur der claim-basierte Pfad wird gewertet (D62).
- **`rotate-key@1` / `resolve_current_key`** (D62).
- **Der Zweck-Tag `vouch.v` Key `1`** (D56) — eigener Durchgang, Layer-02-Semantik.
- **Atomarer Tausch** (`03 §3.4`) — Anwendungsschicht, Adaptor-Signaturen.
- **Emissionsschranke** (`03 §3.3.4`) — ungedeckte Emission ist auditierbar, nicht mechanisch.
- **Eine Rangfolge der inaktiven Zustände.** `settlement()` unterscheidet `expired` und die
  beiden `INDETERMINATE`-Ursachen; das ist in `03 §3.3.2` normativ festgelegt und **nicht** aus
  `01` Anhang B abgeleitet. Anhang B wird nicht angefasst.
- **Layer 01 und `trust/`** bleiben unverändert, mit der einen Ausnahme aus §0.

---

## 10. Abnahme

1. `make check` grün in allen drei Blöcken.
2. §0 ist ein **eigener Commit**, und nach ihm sind es 242 Tests. Erst danach beginnt `profiles/`.
3. Jeder Vektor aus `03-golden-anchors.md` §4 bis §11 hat genau einen Test, unter dem
   dokumentierten Namen auffindbar.
4. `N_A`, `N_B`, `N_C` sind berechnet und gegen die dokumentierten Werte geprüft.
5. `git status --short` leer, `git diff --stat main` ohne Datei außerhalb von
   `mensch_als_republik/index.py`, `mensch_als_republik/profiles/`, `mensch_als_republik/trust/`
   (nur Importzeilen) und `tests/`.
6. Ein frischer Clone des Branches ist grün.

---

## 11. Rückfragen

Jede Frage, die beim Bauen aufkommt und in `03-profiles.md` keine Antwort hat, ist eine
**Spec-Lücke** und geht zurück ins Spec-Gespräch. Nicht im Implementierungsfenster entscheiden,
auch nicht, wenn die Antwort naheliegt — vier der letzten fünf Befunde lagen in Formulierungen,
die naheliegend und unvollständig waren.

Besonders erwartbar: die Ableitung der Testidentitäten (§8.1); das Verhalten bei mehreren
zählenden Claims derselben Art (§5); Zustände von `classify_all`, die in keiner Tabelle dieses
Prompts vorkommen. Der letzte Punkt ist der wichtigste — wenn ein Zustand auftaucht, den §6.1
nicht nennt, ist das kein Randfall, sondern eine fehlende Zeile in der Spec.
