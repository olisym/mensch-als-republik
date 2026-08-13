# Implementierungs-Prompt — Layer 04 (Governance)

Normative Quellen: `04-governance.md`, `04-golden-anchors.md`, Register D96–D105.
Wo dieser Prompt und die Spec auseinandergehen, gilt die Spec — und die Abweichung ist ein
Befund, kein Spielraum.

---

## 0. Vorarbeit

Zwei Änderungen unterhalb der neuen Schicht, beide klein, beide zuerst.

### 0.1 `mensch_als_republik/domains.py`

```python
DOM_NUC_EPOCH    = b"claim-atom/v1/nucleus-epoch"
DOM_NUC_PROPOSAL = b"claim-atom/v1/nucleus-proposal"
```

Zwei eigene Separatoren, damit ein `epoch_id` nie mit einem `proposal_hash`, einem
`constitution_hash`, einer `claim_id` oder einem `N` kollidieren kann.

### 0.2 `mensch_als_republik/policy.py` — D95 und ein geteilter Hash

**(a)** Neue Funktion, damit `profiles/policy.py` und `governance/` denselben Weg nehmen:

```python
def constitution_hash(constitution_obj: dict) -> bytes:
    return hashlib.sha256(cbor_canon.encode(constitution_obj)).digest()
```

`profiles/policy.py` benutzt sie statt der eigenen Inline-Zeile. Zwei Wege zu einem Hash sind
zwei Wege, die auseinanderlaufen können.

**(b) D95.** `NucleusPolicy.__post_init__` filtert `declared`:

- Ein Eintrag ist wohlgeformt, wenn er ein `str` ist, **genau ein** `@` enthält, beidseits davon
  nicht leer ist, und weder `/` noch `:` trägt.
- Alles andere fällt heraus, mit `PolicyWarning.MALFORMED_IRREVOCABLE_ENTRY` in `policy.warnings`,
  Subjekt der Eintrag selbst; ist er kein `str`, sein `repr`.
- `declared` wird als `Iterable[object]` entgegengenommen. Ist der Wert nicht iterierbar, gilt die
  Liste als vollständig ausgefallen: leere Menge, ein Vermerk.
- `profiles/policy.py` reicht `constitution_obj.get("irrevocable_predicates", [])`
  **unverändert** weiter. Das heutige `frozenset(raw)` fällt weg — es ist der Ort, an dem ein
  Textwert zur Zeichenmenge wird, und es wirft bei `42` einen unbehandelten `TypeError`.

Der Filter gehört in den Konstruktor, nicht in `resolve_policy`: D72 hat Boden und Filter dort
angesiedelt, damit ein Aufrufer, der die Klasse von Hand baut, keine unsichere Menge erzeugen
kann. Ein Filter im Resolver ist umgehbar, und genau damit hat D57 den Wrapper verworfen.

Vektoren: `P-7` Zeichenmenge aus einem Textwert, `P-8` Eintrag ohne `str`, `P-9`
`"nuc:N/obligation@1"` mit Scope-Präfix.

---

## 1. Was diese Schicht **nicht** ist

- **Kein zweites `classify`.** „Aktiv" kommt aus Layer 01 über `classify_all`. Die
  Unwiderruflichkeit einer Stimme entsteht **nicht** hier, sondern dadurch, dass `vote@1` in
  `irrevocable_predicates` steht und `is_irrevocable` greift (D105). Wer in `governance/` eine
  eigene Aktivitätsregel schreibt, ist rot.
- **Keine Uhr.** `now` wird durchgereicht, weil `classify_all` es braucht. Kein Pfad dieser
  Schicht vergleicht `t`, und `t_exp` wird ausschließlich auf **Anwesenheit** geprüft, nie auf
  seinen Wert.
- **Keine Gewichte.** Kein Import aus `trust/`. `weight_mode != 0` ist ein Abbruchgrund, kein
  Zweig.
- **Keine Bedeutung.** `participants` sind Bytes, `thresholds` sind Integer-Paare. Kein Eintrag
  wird interpretiert, keine Verfassung inhaltlich bewertet.
- **Keine Reject-Codes.** `errors.py` bleibt bei elf. Alles, was diese Schicht findet, ist ein
  Vermerk.
- **Keine Schlüsselauflösung.** `resolve_current_key` existiert nicht und wird nicht vorbereitet.
  Diese Schicht baut ausschließlich den Epochenpfad (`vote_mode = 0`).

---

## 2. Modulschnitt

```
mensch_als_republik/domains.py       + zwei Separatoren           (§0.1)
mensch_als_republik/policy.py        + constitution_hash(), D95   (§0.2)
mensch_als_republik/governance/
  __init__.py    öffentliche Oberfläche
  findings.py    GovernanceFinding, Finding(kind, subject)
  objects.py     Epoch, Proposal, epoch_id(), proposal_hash()
  tally.py       decide(), reached(), hopeless(), ratio_max(), threshold_for()
  epoch.py       verify_ratification()
mensch_als_republik/profiles/membership.py   + participants       (§7)
```

Abhängigkeiten zeigen nach unten: `governance/*` benutzt `atom`, `cbor_canon`, `domains`,
`policy`, `predicates`, `verifier`, `index`. **Kein** Import aus `trust/`, und **kein** Import aus
`governance/` in `profiles/`.

`Finding` ist dieselbe Bauform wie in `trust/findings.py` und `profiles/findings.py` —
`@dataclass(frozen=True, slots=True, order=True)` mit `kind: GovernanceFinding` und
`subject: bytes`. Eigener Enum, gleiche Form. `findings` ist überall sortiert und dedupliziert.

---

## 3. Gemeinsame Bausteine

### 3.1 Verhältnisse

Nie dividieren. Ein Verhältnis ist ein `tuple[int, int]`.

```python
def ratio_max(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a if a[0] * b[1] >= b[0] * a[1] else b

def reached(yes: int, n: int, num: int, den: int) -> bool:
    return yes * den > num * n

def hopeless(no: int, n: int, num: int, den: int) -> bool:
    return (n - no) * den <= num * n
```

Das `>` in `reached` ist strikt. Bei `n = 4`, `[3,4]` und drei Ja steht `12` gegen `12`; ein `>=`
macht daraus eine Verfassungsänderung. Das ist `GV-3`.

### 3.2 Objektformen

```python
epoch_id      = SHA-256( DOM_NUC_EPOCH    || cbor([scope, index, constitution_hash]) )
proposal_hash = SHA-256( DOM_NUC_PROPOSAL || cbor({0: scope, 1: predecessor, 2: constitution_hash}) )
```

`cbor` ist immer `cbor_canon.encode`. Die Epoche ist ein **Array**, der Vorschlag eine **Map** —
das ist keine Willkür, sondern reproduziert die Anker; wer beides gleich kodiert, bekommt andere
Zahlen als `04-golden-anchors.md §3`.

```python
@dataclass(frozen=True, slots=True)
class Epoch:
    scope: bytes
    index: int
    constitution_hash: bytes
    @property
    def epoch_id(self) -> bytes: ...

@dataclass(frozen=True, slots=True)
class Proposal:
    scope: bytes
    predecessor: bytes
    constitution_hash: bytes
    @property
    def proposal_hash(self) -> bytes: ...
```

### 3.3 Prädikatnamen

`nuc:{scope_hex}/propose@1`, `.../vote@1`, `.../ratify@1`. Erkennung über `parse_predicate` wie in
`profiles/membership.py._is_nuc_name`, nicht über String-Vergleich auf `claim.p`.

---

## 4. `governance/tally.py`

```python
def decide(
    store: ClaimStore,
    *,
    epoch: Epoch,
    proposal: Proposal,
    genesis_obj: dict,
    constitution_obj: dict | None,
    target_constitution_obj: dict | None,
    known_proposals: Mapping[bytes, Proposal],
    now: int,
    policy: NucleusPolicy | None = None,
) -> TallyResult
```

`TallyResult` trägt `state: TallyState`, `yes: tuple[bytes, ...]`, `no: tuple[bytes, ...]`,
`participants: frozenset[bytes] | None`, `threshold: tuple[int, int] | None`,
`findings: tuple[Finding, ...]`. `n` ist **kein Feld**, sondern eine Eigenschaft:
`len(participants)`, oder `None`, wenn `participants` `None` ist.
`TallyState` hat vier Werte: `PASSED`, `FAILED`, `PENDING`, `UNEVALUABLE`.

`participants` ist genau dann `None`, wenn `state is UNEVALUABLE`. Das Feld ist der einzige Ort,
an dem die Wählerschaft nach der Auszählung steht; `verify_ratification` liest sie von dort und
bekommt sie nicht als eigenen Parameter (D106).

`yes` und `no` sind die sortierten `claim_id` der **zählenden** Stimmen.

### 4.1 Abbruchprüfungen — in dieser Reihenfolge

Die erste zutreffende Zeile beendet die Auswertung mit `UNEVALUABLE` und genau einem Vermerk.
`04 §3.5` gibt die Reihenfolge vor; sie ist normativ, weil sonst dieselbe Lage je nach
Implementierung verschiedene Diagnosen erzeugt.

| Prüfung | Vermerk |
|---|---|
| `constitution_obj is None` oder Hash passt nicht zu `epoch.constitution_hash` | `CONSTITUTION_UNAVAILABLE` |
| `participants` fehlt | `PARTICIPANTS_UNDECLARED` |
| `participants` kein Array, Eintrag nicht 32 B, unsortiert, oder Duplikat | `MALFORMED_PARTICIPANTS` |
| `vote@1` nicht in `irrevocable_predicates` | `VOTE_REVOCABLE` |
| Klasse nicht bestimmbar, Schwelle fehlt oder formwidrig, `genesis[5] > 2` | `MALFORMED_THRESHOLD` |
| `genesis_obj[6] != 0` | `UNSUPPORTED_WEIGHT_MODE` |
| `target_constitution_obj is None` oder Hash passt nicht zu `proposal.constitution_hash` | `PROPOSAL_CONSTITUTION_UNAVAILABLE` |

Der Vergleich der `participants`-Sortierung ist ein Byte-Vergleich auf der gelieferten
Reihenfolge, keine Neusortierung. Eine unsortierte Liste ist ein Fehler, kein Anlass zum Ordnen —
sie gehört zu einem anderen `constitution_hash`.

### 4.2 Schwelle bestimmen

```python
def threshold_for(old_obj: dict, new_obj: dict, genesis_obj: dict) -> tuple[str, tuple[int, int]]
```

1. Unterscheiden sich `old_obj` und `new_obj` **ausschließlich** in `participants`, ist die Klasse
   `membership`. Sonst ist sie der Name zu `genesis_obj[5]` nach `0 = ordinary`, `1 = membership`,
   `2 = amendment` (D104).
2. `angewandt = ratio_max(old.thresholds[klasse], new.thresholds[klasse])` (`04 §3.4`).

Der Vergleich in Schritt 1 läuft über die **kanonische Kodierung** der beiden Objekte ohne das
Feld `participants`, nicht über einen Feldvergleich in Python. Ein Objekt mit demselben Inhalt in
anderer Schlüsselreihenfolge existiert nicht — `cbor_canon` ordnet.

Fehlt `thresholds[klasse]` in **einer** der beiden Verfassungen, ist das `MALFORMED_THRESHOLD`.

### 4.3 Welche Stimmen zählen

Für jeden Claim im Store mit Prädikat `vote@1`:

1. `vote.N == epoch.scope`
2. `vote.J == (3, proposal.proposal_hash)`
3. `proposal.predecessor == epoch.epoch_id` — sonst `STALE_EPOCH_VOTE`
4. `vote.I in participants` — sonst `NON_MEMBER_VOTE`
5. `by_cid[cid].state is State.ACTIVE`
6. `vote.v[0] in (0, 1)` — sonst `UNKNOWN_VOTE_CHOICE`
7. `vote.t_exp is None` — sonst `VOTE_WITH_EXPIRY`

`by_cid` kommt aus `classify_all(store, now, policy)` — **ein** Aufruf, nicht einer je Stimme.

Danach zwei Ausschlüsse:

- **Zwei zählende Stimmen desselben Autors auf denselben Vorschlag:** keine zählt.
  `AMBIGUOUS_VOTE`, Subjekt beide `claim_id`.
- **Doppelte Zustimmung in der Epoche** (`§4.4`, siehe unten).

### 4.4 Doppelte Zustimmung — die Falle

Für jeden Autor mit einer Ja-Stimme auf **diesen** Vorschlag werden **alle** aktiven `vote@1`
desselben Autors im Scope mit `v[0] == 1` betrachtet, auch die auf andere Vorschläge:

| Lage | Wirkung |
|---|---|
| `J[1]` ist derselbe Vorschlag | nichts (fällt unter `AMBIGUOUS_VOTE`) |
| `J[1]` in `known_proposals`, `predecessor == epoch.epoch_id` | `CONFLICTING_APPROVAL`, Autor zählt nicht |
| `J[1]` in `known_proposals`, anderer `predecessor` | nichts |
| `J[1]` nicht in `known_proposals` | `UNKNOWN_PROPOSAL`, Autor zählt nicht (D103) |

> **Die Falle.** Die naheliegende Implementierung filtert die Stimmen zuerst auf
> `J == (3, proposal_hash)` und sieht die konkurrierende Ja-Stimme danach nie. Dann ist `GV-15`
> rot und `INV-04.6` verletzt — zwei rivalisierende Nachfolger derselben Epoche werden möglich,
> und damit fällt D102. Die Konfliktprüfung läuft über **alle** `vote@1` im Scope, bevor gefiltert
> wird.

Nein-Stimmen sind von dieser Prüfung nicht betroffen. Gegen mehrere Vorschläge gleichzeitig zu
sein ist erlaubt.

### 4.5 Zustand

```
n = len(participants)
PASSED  wenn reached(len(yes), n, num, den)
FAILED  wenn hopeless(len(no), n, num, den)
sonst   PENDING
```

`PASSED` wird vor `FAILED` geprüft; beide können nach `INV-04.2` nie gleichzeitig zutreffen, und
ein Test, der das erzwingt, gehört in die Suite.

---

## 5. `governance/epoch.py`

```python
def verify_ratification(
    store: ClaimStore,
    *,
    ratify: Claim,
    epoch: Epoch,
    proposal: Proposal,
    tally: TallyResult,
    now: int,
    policy: NucleusPolicy | None = None,
) -> RatificationResult
```

`RatificationResult` trägt `next_epoch: Epoch | None` und `findings`.

`next_epoch` ist gesetzt genau dann, wenn:

1. `ratify.N == epoch.scope`, `ratify.J == (3, proposal.proposal_hash)`
2. `ratify.I` steht in `participants`, und `ratify` ist `ACTIVE`
3. jede `claim_id` in `ratify.v[0]` steht in `tally.yes`
4. `reached(len(zitierte), n, num, den)`

Dann ist `next_epoch = Epoch(scope, epoch.index + 1, proposal.constitution_hash)`.

Bedingung 2 liest `participants` aus `tally`, nicht aus einem eigenen Parameter. Ist
`tally.state is UNEVALUABLE`, ist `tally.participants` gleich `None` und `next_epoch` gleich
`None`.

Zwei Vermerke, nach der Lage der zitierten `claim_id` (D106):

| Lage | Vermerk |
|---|---|
| `store.get(cid) is None` | `UNKNOWN_WITNESS_VOTE` |
| Claim vorhanden, steht aber nicht in `tally.yes` | `UNSUPPORTED_RATIFICATION` |

Die Trennung ist die Diagnose: das eine heißt „mir fehlt ein Claim", das andere „die Behauptung
stimmt nicht" (D94). Beide führen dazu, dass keine Epoche entsteht — sichere Richtung —, aber nur
im ersten Fall nützt es, den Claim zu holen. Vektoren `GV-30` und `GV-2`.

Aus den Bedingungen 3 und 4 folgt, dass `verify_ratification` nur dann eine Epoche liefern kann,
wenn `tally.state is PASSED`. Ein expliziter Test darauf ist überflüssig, ein Test **dagegen**
gehört in die Suite.

Die Zeugenmenge ist **nicht** Teil der Epochenidentität. Zwei `ratify@1` mit verschiedenen
Zeugenmengen für denselben Vorschlag liefern denselben `epoch_id` (`GV-1`, D99).

---

## 6. `governance/__init__.py`

Öffentlich: `Epoch`, `Proposal`, `TallyResult`, `TallyState`, `RatificationResult`,
`GovernanceFinding`, `Finding`, `decide`, `verify_ratification`, `epoch_id`, `proposal_hash`.

`reached`, `hopeless`, `ratio_max` und `threshold_for` bleiben modulintern, werden aber getestet.

---

## 7. Änderung an `profiles/membership.py`

Ein zusätzlicher Schlüsselwort-Parameter, sonst nichts:

```python
participants: frozenset[bytes] | None = None
```

Ist er gesetzt, gilt `subject in participants` als **zweite Aufnahmequelle** neben einer aktiven
`grant-membership@1`. Die `accept-rules`-Strecke bleibt vollständig unverändert.

`grant_claim_id` bleibt `None`, wenn die Aufnahme aus `participants` stammt — es gibt keinen
Claim, auf den zu zeigen wäre. Die vier Zustände sind unverändert; ein Subjekt in `participants`
ohne aktive `accept-rules` ist `GRANT_ONLY`.

Kein neues Prädikat, kein neuer Zustand, **keine zweite Mitgliedschaftsfunktion**. Zwei
Funktionen, die dasselbe tun, waren die Fehlerform der `03`-Abnahme (D92).

Die bestehenden `03`-Vektoren müssen alle grün bleiben; `participants=None` ist das
Bestandsverhalten.

---

## 8. Tests

### 8.1 Fixtures — `tests/governance/fixtures.py`

Profil D aus `04-golden-anchors.md §2`. Identitäten aus den Seeds `01×32` bis `05×32`. Die drei
Verfassungsobjekte, das Genesis-Objekt, die drei Epochen und die beiden Vorschläge werden
**gerechnet**, nicht als Konstanten eingetragen — und gegen die Hexwerte der Anker geprüft. Ein
Test, der die Anker als Literale trägt, prüft die Anker gegen sich selbst.

Ein eigener Test reproduziert zusätzlich die **Bestandsanker** aus `00 §3.1`
(`890b21e7…`, `65309fe2…`) über denselben Kodierungsweg. Bricht er, ist die Kodierung falsch und
nicht die Governance.

### 8.2 Vektoren

`GV-1` bis `GV-29` aus `04-golden-anchors.md`, je ein Test. Zwei davon sind
**Gegenbilder** und müssen als solche benannt sein:

- `GV-12` — drei von fünf senken die Änderungsschwelle, **wenn** `ratio_max` fehlt.
- `GV-14` — dasselbe beim Anheben.

Beide prüfen, dass die Regel wirkt, indem sie zeigen, was ohne sie passierte. Ein weggelassener
Schutz erzeugt sonst keinen roten Test.

`GV-28` ist der Vektor gegen den häufigsten Fehler: ein widerrufener `vote@1` in einer Verfassung,
die `vote@1` schützt, **zählt weiter**. Wer `classify_all` ohne die scope-lokale Policy aufruft,
bekommt `REVOKED` und ist hier rot (D91).

### 8.3 Invarianten

`INV-04.1` bis `INV-04.7` aus `§8` der Anker. Drei davon sind Eigenschaftstests über einem
Bereich, nicht Einzelfälle:

- `INV-04.2` — `n` von 1 bis 12, alle gekürzten `[num, den]` mit `den <= 8` und
  `1/2 <= num/den < 1`, alle `yes`, `no` mit `yes + no <= n`. `PASSED` und `FAILED` nie zugleich.
- `INV-04.6` — über denselben Bereich: höchstens ein Vorschlag je Epoche kann `PASSED` erreichen,
  solange kein Autor zwei Ja hält.
- `INV-04.7` — Store schrittweise füllen, nach jedem Schritt auszählen; die Menge der zählenden
  `claim_id` wird nie kleiner. Das ist die Invariante, auf der D96, D101 und D102 gemeinsam
  stehen.

`INV-04.5` negativ: zwei Läufe mit verschiedenen `now` liefern byte-identische Ergebnisse.

---

## 9. Ausdrücklich nicht in diesem Schritt

- `resolve_current_key`, `rotate-key@1`, der Schlüsselpfad aus `04 §5` (D62)
- gewichtete Auszählung, `weight_mode = 1` (D98)
- der Zweck-Tag am Vouch, `02d` (D56)
- VR-04.1 und die Kettenbindung von Ämtern (D26)
- Föderationszahlen; `04 §7.2` ist eine Belegung desselben Loops
- das Zeugenquorum für Fristen (D100)
- jede Änderung an `errors.py`, `verifier.py`, `atom.py` oder `trust/`

---

## 10. Abnahme

`make check` grün in drei Blöcken: Arbeitsbaum ohne unversionierte Quelldateien, Spec-Dateien
sauber, Register lückenlos. Alle Bestandstests bleiben grün — die Zahl steigt, sie fällt nicht.

`git add` mit **expliziten Pfaden**. Ein Commit, der mehr Dateien meldet, als geliefert wurden,
ist ein Abbruchgrund und kein Schönheitsfehler.

---

## 11. Rückfragen

Jede Frage, die beim Bauen aufkommt und in `04-governance.md` keine Antwort hat, ist eine
**Spec-Lücke** und geht zurück ins Spec-Gespräch. Nicht im Implementierungsfenster entscheiden,
auch nicht, wenn die Antwort naheliegt — D103, D104 und D105 sind allein beim Entwerfen der
Signaturen dieses Prompts entstanden, und alle drei sahen vorher wie Selbstverständlichkeiten aus.

Besonders erwartbar:

- **Zwei gleichlautende Ja-Stimmen desselben Autors auf denselben Vorschlag.** `§4.3` lässt beide
  entfallen, auch wenn sie dasselbe sagen. Das ist gewollt und die sichere Richtung, aber es ist
  strenger als `03`, das mit `min(claim_id)` auflöst. Wer es unangenehm findet, meldet es — er
  ändert es nicht.
- **Zustände aus `classify_all`, die in keiner Tabelle dieses Prompts vorkommen.** Taucht einer
  auf, ist das kein Randfall, sondern eine fehlende Zeile in der Spec.
- **Der Umgang mit `known_proposals`, wenn der Aufrufer den eigenen Vorschlag nicht mitgibt.**
  Die Spec setzt voraus, dass er drin steht; was passiert, wenn nicht, steht nirgends.
