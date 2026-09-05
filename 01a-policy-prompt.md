# `01a-policy` — Policy-Override in der Zustandsmaschine

Auftrag an den Implementierer. Normative Quelle: `01-claim-atom.md §5.4`, `§6`, Anhang B.1;
`00-nucleus-genesis-constitution.md §5`, `§5.2`; Register D57, D58, D70, D71, D72.

Der Umfang ist klein und die Grenze scharf: **ein neues Modul, ein zusätzlicher Parameter,
keine Verhaltensänderung ohne diesen Parameter.** Die 61 Layer-01-Tests und die 215 Tests
insgesamt müssen unverändert grün bleiben, weil `policy=None` exakt die heutige Semantik ist.

---

## 1. Warum es das gibt

`01 §5.4` sagt seit v1, eine Nukleus-Policy dürfe bestimmte Prädikate für *irrevocable*
erklären. Die Signatur `classify(claim, store, now)` hatte dafür keinen Ort — der Satz war zwei
Layer lang dekorativ. Layer 03 braucht ihn: ohne ihn kann ein Schuldner seine eigene
`obligation@1` per selbst-bezüglichem `core/revoke@1` löschen.

---

## 2. Neues Modul `symbolon/policy.py`

```python
PROTOCOL_IRREVOCABLE = frozenset({"obligation@1"})   # Boden, D70 / 00 §5.2
TRUST_GRANTING       = frozenset({"vouch@1"})        # Negativliste, D58 / 01 §5.4.3 b


class PolicyWarning(str, Enum):
    UNSAFE_IRREVOCABLE_PREDICATE = "UNSAFE_IRREVOCABLE_PREDICATE"


@dataclass(frozen=True, slots=True)
class NucleusPolicy:
    scope: bytes                      # das N, für das diese Policy gilt
    declared: frozenset[str] = frozenset()
    irrevocable: frozenset[str] = field(init=False, default=frozenset())
    warnings: tuple[PolicyWarning, ...] = field(init=False, default=())
```

### 2.1 Normalisierung im Konstruktor

`__post_init__` berechnet `irrevocable` und `warnings` aus `declared` und setzt sie per
`object.__setattr__`. **Die Invarianten leben im Typ** (D72): kein Aufrufer soll eine unsichere
Policy bauen können, auch nicht durch direkte Konstruktion.

```
irrevocable = (PROTOCOL_IRREVOCABLE ∪ declared) ∖ TRUST_GRANTING ∖ {core-Einträge}
```

Drei Regeln, in dieser Reihenfolge:

1. **Boden** (D70): `PROTOCOL_IRREVOCABLE` ist immer enthalten, auch wenn `declared` es nicht
   nennt und auch wenn `declared` andere Einträge trägt. Die Liste erweitert, sie verkleinert
   nie.
2. **Negativliste** (D58): Einträge aus `TRUST_GRANTING` fallen heraus und erzeugen
   `UNSAFE_IRREVOCABLE_PREDICATE`. Der Rest der Liste bleibt wirksam — **kein**
   Alles-oder-nichts.
3. **Core-Filter** (D71): Einträge, die auf `core`-Prädikate zeigen (`"revoke@1"`,
   `"supersede@1"`), fallen still heraus. Kein Warning: sie sind bedeutungslos, nicht
   gefährlich.

`warnings` ist sortiert und dedupliziert.

### 2.2 Prädikat-Abgleich (`01 §5.4.2`)

```python
def is_irrevocable(predicate: str, policy: NucleusPolicy | None) -> bool
```

Wahr gdw. `policy` nicht `None` ist, `predicate` mit `"nuc:"` beginnt, und der Teil **nach dem
letzten `/`** in `policy.irrevocable` liegt. Ein `core/*`-Prädikat ist nie irrevocable.

`irrevocable_predicates` trägt Profilnamen **ohne** Scope-Präfix: der Eintrag lautet
`"obligation@1"`, das Claim-Prädikat lautet `"nuc:<64 Hex>/obligation@1"`.

---

## 3. Änderung an `verifier.py`

```python
def classify(claim, store, now, policy: NucleusPolicy | None = None) -> Classification: ...
```

### 3.1 Wirkung

Ist `is_irrevocable(claim.p, policy)` wahr, werden bei der Zustandsbestimmung von `claim`
**ignoriert**:

- jeder `core/revoke@1` mit `R.I == C.I` und `R.J == [claim-ref, C.claim_id]`,
- jeder `core/supersede@1` desselben Autors auf dasselbe Ziel.

Der Claim ist dann `active`, sofern er es sonst wäre. **Sonst ändert sich nichts:**

| bleibt unberührt | warum |
|---|---|
| `malformed`, `pending`, `linked` | strukturell bzw. Kettenlage, keine Lebenszyklus-Frage |
| `expired` | `01 §5.4.3 a` — Irrevocability schlägt die Uhr nicht |
| `equivocation-flagged` | `01 §4`, keine Policy-Frage |
| der Widerruf **selbst** | bleibt gültig, gespeichert, `active` (A3, `01 §5.2`) |

Der letzte Punkt ist der wichtigste: ein ignorierter Widerruf wird **nicht versteckt und nicht
abgelehnt**. Er ist soziale Information; er hat nur keine Wirkung auf den Zustand seines Ziels.

### 3.2 Scope-Prüfung

Ist `policy` gesetzt und `claim.p` beginnt mit `"nuc:"`, dann MUSS `claim.N == policy.scope`
gelten. Andernfalls: `raise ValueError("policy scope does not match claim scope")`.

Begründung: eine Policy des falschen Nukleus stillschweigend zu ignorieren wäre die **unsichere**
Richtung — ein Widerruf auf eine `obligation@1` würde wirken, obwohl die zuständige Verfassung
das ausschließt. Ein lauter Fehler ist hier besser als ein leiser. Für `core/*`-Claims wird
`policy` vollständig ignoriert, ohne Prüfung.

### 3.3 `policy=None`

Kein Override. Jeder Widerruf und jedes Supersede wirken wie bisher. Das ist der Pfad, den alle
bestehenden Aufrufer nehmen.

> **Nachtrag (D156, D159).** Abgelöst. Ohne Policy gilt seit D156 der Protokoll-Boden aus
> `00 §5.2`; ein Widerruf auf ein Bodenprädikat wirkt nicht. Der Absatz oben war eine
> Migrationsaussage aus einem Schritt ohne Resolver (§4) und wird nicht nachgezogen. Betroffen
> sind die Vektoren `M-5`, `C-1` und `C-9`.

---

## 4. Ausdrücklich nicht in diesem Schritt

- **Der Resolver.** `NucleusPolicy` aus Genesis- und Verfassungsobjekt aufzulösen braucht ein
  Objektmodell für `00 §4`/`§5`, das es noch nicht gibt. Kommt mit `03` (D72). Tests bauen
  `NucleusPolicy` von Hand.
- **`classify_all` in `trust/index.py`.** Bekommt **keinen** `policy`-Parameter. Layer 02 wertet
  ausschließlich `vouch@1` aus, und `vouch@1` kann nach D58 nie irrevocable sein — der Parameter
  hätte dort keine Wirkung. Nicht anfassen.
- **Ein Findings-Kanal in Layer 01.** `Classification` bleibt unverändert und trägt die
  angewandte Policy nicht (D72). `warnings` lebt in `NucleusPolicy` und wird von Layer 03
  ausgewertet.
- **Neue Reject-Codes.** `errors.py` bleibt bei elf Codes. Eine unsichere Deklaration ist kein
  Reject eines Claims, sondern ein Vermerk an der Policy.
- **`obligation@1` als Profil.** Es gibt in `01a` kein Obligations-Profil und keine
  Tilgungslogik — nur ein Prädikat, das anders klassifiziert wird. Alles Weitere ist `03`.

---

## 5. Tests

Alle Vektoren nutzen `tests/trust/helpers.py` (`Identity`, `scope_id`, `store_with`). Für
Prädikate jenseits von `vouch@1` wird ein generischer Anhänger gebraucht — falls `helpers.py`
ihn nicht hat, ergänze eine minimale Methode statt `vouch_raw` zweckzuentfremden, und melde das
zurück.

### 5.1 Normalisierung (`policy.py`)

| # | `declared` | `irrevocable` | `warnings` |
|---|---|---|---|
| P-1 | `∅` | `{obligation@1}` | `()` |
| P-2 | `{obligation@1}` | `{obligation@1}` | `()` |
| P-3 | `{foo@1}` | `{obligation@1, foo@1}` | `()` |
| P-4 | `{vouch@1}` | `{obligation@1}` | `(UNSAFE_…,)` |
| P-5 | `{vouch@1, foo@1}` | `{obligation@1, foo@1}` | `(UNSAFE_…,)` |
| P-6 | `{revoke@1, supersede@1}` | `{obligation@1}` | `()` |

> **Nachtrag (D153, D157, D159).** Der Boden ist seit D153 `{obligation@1, rotate-key@1,
> rotate-ack@1}` und gilt seit D156 auch ohne Policy. Die Tabellen dieses Abschnitts zeigen den
> Stand bei Erteilung des Auftrags und werden nicht nachgezogen; die lebenden Erwartungswerte
> stehen in `03-golden-anchors.md`, und `M-5`, `C-1` und `C-9` sind durch D159 abgelöst.

**P-3 ist der D70-Vektor** und der einzige, der die alte Fassung von `00 §5.2` von der neuen
trennt: nach altem Wortlaut griff der Default nur bei Schweigen, `obligation@1` wäre hier
**nicht** enthalten gewesen.

**P-5 ist der D70-Zusatzvektor:** die unsichere Deklaration entwertet die übrige Liste nicht.

### 5.2 Prädikat-Abgleich

| # | Prädikat | erwartet |
|---|---|---|
| M-1 | `nuc:<hex>/obligation@1` | irrevocable |
| M-2 | `nuc:<hex>/vouch@1` | nicht |
| M-3 | `core/revoke@1` | nicht (D71) |
| M-4 | `nuc:<hex>/obligation@2` | nicht — Version ist Teil des Namens |
| M-5 | `policy = None` | nie irrevocable |

### 5.3 Zustandsmaschine

| # | Aufbau | `policy` | erwarteter Zustand |
|---|---|---|---|
| C-1 | Obligation + eigener Revoke | `None` | `revoked` |
| C-2 | dieselbe Lage | Policy des Scopes | **`active`** |
| C-3 | Obligation + eigener Supersede | Policy | **`active`** |
| C-4 | Vouch + eigener Revoke | Policy | `revoked` — D58 greift |
| C-5 | Obligation mit `t_exp < now` + Revoke | Policy | `expired` — `§5.4.3 a` |
| C-6 | der Revoke aus C-2, für sich klassifiziert | Policy | `active` — er bleibt gültig |
| C-7 | Obligation, Vorgänger fehlt | Policy | `pending` — unberührt |
| C-8 | Obligation, `policy.scope ≠ claim.N` | Policy | `ValueError` |

**C-2 ist der Kernvektor.** Er ist zugleich der einzige, der die alte von der neuen
Implementierung trennt — alle anderen prüfen, dass sich nichts geändert hat.

**C-5 ist der Vektor, der die häufigste Fehlannahme fängt:** „irrevocable" liest sich wie
„unantastbar", ist aber nur „nicht widerrufbar".

### 5.4 Regression

Die 61 Layer-01-Tests und die 154 Layer-02-Tests laufen unverändert. Jeder Aufruf ohne `policy`
muss byte-gleiche Ergebnisse liefern wie vor der Änderung. Wird an einem bestehenden Test etwas
angepasst, ist das ein Befund und gehört zurückgemeldet, nicht repariert.

---

## 6. Abnahme

```
make check
```

Drei grüne Blöcke: Arbeitsbaum ohne unversionierte Quelldateien, sechzehn Spec-Dateien,
Register D1–D72, Tests. Erwartete Testzahl: 215 + 19 = **234**.

Branch `impl/01a-policy`, Merge auf `main` erst bei grün.

---

## 7. Rückfragen

Fragen zur Spec sind **keine** Implementierungsentscheidungen. Wenn etwas hier nicht steht oder
sich widerspricht, ist das ein Spec-Fehler und geht zurück in die Spec-Sitzung — so sind in
`02a` und `02b` die besseren Lösungen für die geteilte Schnittstelle und PR-INV-4 entstanden.
Nicht selbst entscheiden, nicht raten, nicht „naheliegend" ergänzen.
