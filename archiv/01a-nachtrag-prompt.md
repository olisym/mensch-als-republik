# `01a-policy` — Nachtrag aus der Abnahme

Drei Befunde aus der Durchsicht von `policy.py`, `verifier.py` und `tests/test_policy.py`.
**Keiner ist ein Rechenfehler**, alle drei sind Strukturfragen — zwei davon Vorgabefehler in
`01a-policy-prompt.md`, einer Hygiene. Normative Quelle für die Neuerungen: Register D74–D76.

Der bestehende Code ist korrekt und bleibt in seiner Wirkung unverändert. Nichts an der
Semantik von `classify` wird angefasst.

---

## B1 — Policy-Vermerke tragen ihr Subjekt (D74)

Heute:

```python
warnings = (PolicyWarning.UNSAFE_IRREVOCABLE_PREDICATE,) if unsafe else ()
```

Der Betreiber erfährt, dass *etwas* Unsicheres deklariert war, nicht *was*. Bei einer
Verfassung mit zwanzig Einträgen ist das unbrauchbar, und der Resolver in `03` soll den
konkreten Eintrag an die Oberfläche bringen. Layer 02 hat für genau diesen Zweck
`Finding(kind, subject)`.

**Umsetzung in `mensch_als_republik/policy.py`:**

```python
@dataclass(frozen=True, slots=True)
class PolicyNote:
    code: PolicyWarning
    predicate: str
```

`NucleusPolicy.warnings` wird zu `tuple[PolicyNote, ...]` — ein Eintrag **je** unsicher
deklariertem Prädikat, sortiert nach `predicate`. Sortiert, weil `declared` ein `frozenset` ist
und die Iterationsreihenfolge sonst zwischen Läufen schwankt; ein Testvektor über zwei unsichere
Einträge wäre andernfalls nicht reproduzierbar.

`PolicyNote` gehört in `__all__`.

**Testanpassung:** P-4 erwartet `(PolicyNote(UNSAFE_IRREVOCABLE_PREDICATE, "vouch@1"),)`, P-5
dasselbe. Die Konstante `_UNSAFE` in `tests/test_policy.py` entfällt oder wird zur Funktion.

---

## B2 — Die drei Prädikatmengen müssen disjunkt sein (D75)

Heute:

```python
irrevocable = (PROTOCOL_IRREVOCABLE | self.declared) - TRUST_GRANTING - _CORE_ENTRIES
```

Der Boden wird gesetzt, **dann** gefiltert. Läge je ein Prädikat in `PROTOCOL_IRREVOCABLE`
*und* `TRUST_GRANTING`, verschwände der Boden aus D70 still. Heute unmöglich, weil die
Konstanten disjunkt sind — und genau deshalb kann **kein** Testvektor die Regelreihenfolge
prüfen: P-1 bis P-6 bestehen unter jeder Anordnung.

Der richtige Fix ist nicht ein weiterer Vektor, sondern eine Invariante, die den Fall abschafft.
**Auf Modulebene, direkt unter den Konstanten:**

```python
assert not (PROTOCOL_IRREVOCABLE & TRUST_GRANTING), (
    "D70/D58: der Boden darf nie in der Negativliste stehen"
)
assert not (PROTOCOL_IRREVOCABLE & _CORE_ENTRIES), (
    "D70/D71: der Boden darf nie ein core-Prädikat sein"
)
```

Ein künftiger Widerspruch zwischen den drei Mengen wird damit beim **Import** laut, nicht in der
Semantik leise. Kein eigener Test — die Zusicherung *ist* die Prüfung, und ein Test, der sie
nachbaut, prüft nur sich selbst.

---

## B3 — `helpers.py` liegt eine Ebene zu tief

`tests/test_policy.py` ist ein Layer-01-Test und importiert aus `tests/trust/helpers.py`. Die
Abhängigkeit zeigt nach oben. `helpers.py` selbst benutzt nur `atom`, `cbor_canon` und
`verifier` — es hat nie unter `trust/` gehört, es ist dort nur entstanden, weil `02a` der erste
Nutzer war.

```
git mv tests/trust/helpers.py tests/helpers.py
```

Alle Importe nachziehen: in `tests/trust/tp02.py`, `tests/trust/pr02.py` und jedem Testmodul,
das `from .helpers import …` oder `from tests.trust.helpers import …` benutzt. Danach zeigt
keine Datei mehr auf den alten Pfad — bitte per Suche verifizieren, nicht aus dem Kopf.

`tests/trust/__init__.py` bleibt.

---

## Ein neuer Testvektor (D76)

Bei der Durchsicht ist eine Rangfolge sichtbar geworden, die niemand entschieden hat und die
`01` Anhang B nicht festlegt:

| Lage | `policy=None` | mit Policy |
|---|---|---|
| Obligation, abgelaufen **und** widerrufen | `REVOKED` | `EXPIRED` |

Ohne Policy greift der Widerruf-Zweig vor der Zeitprüfung; mit Policy fällt die Auswertung auf
den `temporal`-Zweig durch. Beides ist vertretbar (der Claim ist so oder so inaktiv), aber die
Umkehrung ist eine getragene Konsequenz und muss einen Vektor haben, sonst ändert sie sich
unbemerkt.

**C-9**, neben C-5 in `tests/test_policy.py`: derselbe Aufbau wie C-5 (`t_exp=50`, `now=100`,
eigener Revoke), aber `policy=None` ⇒ `State.REVOKED`.

**Die Reihenfolge in `classify` nicht ändern.** C-9 hält den Ist-Zustand fest; er ist kein
Auftrag, ihn zu vereinheitlichen.

---

## Abnahme

```
make check
```

Erwartete Testzahl: **235** (234 + C-9). Ändert sich eine andere Zahl, ist das ein Befund.

Die 215 bestehenden Tests dürfen inhaltlich nicht angefasst werden — nur ihre `helpers`-Importe
(B3). Muss an einem Test etwas anderes geändert werden, ist auch das ein Befund und geht zurück
in die Spec-Sitzung.

---

## Rückfragen

Wie beim Hauptlauf: Fragen zur Spec sind keine Implementierungsentscheidungen. Nicht raten,
nicht „naheliegend" ergänzen — zurückmelden. Die Rückfrage zu `helpers.py` im ersten Lauf war
richtig und hat B3 überhaupt erst sichtbar gemacht.
