# Lauf `03b` — die Auflösungskette bekommt ihren Epochenschritt

## 0. Branch und Basis

Branch `03b-epochenschritt`, abgezweigt vom Kopf von `main`. Ein Commit am Ende. Kein Merge,
kein Push nach `main`.

## 1. Normative Grundlage

- `03-profiles.md` §1.2, §6 und §6.1, Stand des Branchpunkts.
- `03-golden-anchors.md` §4, Vektoren `P-A` bis `P-H`.
- `00-nucleus-genesis-constitution.md` §4, Key `4`.
- Register D82, D90, D92, D109, D157, D161, D167, D168.

Die Spec ist bereits nachgezogen und wird in diesem Lauf **nicht** geändert. Widerspricht eine
Messung diesem Prompt: **melden, nicht anpassen.**

## 2. Auftrag

### 2.1 `resolve_policy` in `mensch_als_republik/profiles/policy.py`

```
resolve_policy(*, scope, genesis_obj, constitution_hash,
               constitution_obj=None) -> PolicyResolution
```

`constitution_hash` ist Pflichtparameter ohne Vorgabewert. Ablauf:

1. `scope` gegen `SHA-256(DOM_NUC_GEN || cbor_canon.encode(genesis_obj))` nachrechnen.
   Abweichung ist `ValueError` — unverändert.
2. **`genesis_obj[4]` wird nicht mehr gelesen.** Die bisherige Prüfung auf Vorhandensein und Typ
   entfällt ersatzlos (D168). Ein Genesis ohne Key `4` ist nach `00 §4` defekt, aber nicht durch
   diesen Auflöser festzustellen.
3. Ist `constitution_obj` `None`: Sicherheits-Default `NucleusPolicy(scope, declared=frozenset())`
   plus ein Vermerk `CONSTITUTION_UNAVAILABLE` mit Subjekt **`constitution_hash`** — dem
   übergebenen Wert.
4. Sonst `constitution_hash` gegen die kanonische Hashung von `constitution_obj` nachrechnen.
   Abweichung ist **`ValueError`**, nicht mehr ein Vermerk (D167).
5. Sonst wie bisher: `irrevocable_predicates` durchreichen, `findings` leer.

### 2.2 `mensch_als_republik/profiles/findings.py`

`ProfileFinding.CONSTITUTION_HASH_MISMATCH` wird entfernt. Kein Ersatz, kein Alias, keine
Deprecation.

### 2.3 Die Aufrufstellen

`resolve_policy(` kommt außerhalb seiner eigenen Datei an **20** Stellen vor, gegrept:
`tests/profiles/test_policy.py` 7, `tests/profiles/test_invariants.py` 9,
`tests/profiles/test_credit.py` 2, `tests/profiles/test_payload.py` 2. Jede bekommt den passenden
`constitution_hash`. Wo ein Fixture den Hash schon führt, wird er benutzt; wo nicht, wird er aus
dem übergebenen Verfassungsobjekt **abgeleitet**, nicht getippt.

Stimmt die Zahl 20 nicht: melden, nicht stillschweigend anpassen.

### 2.4 Die Vektoren in `tests/profiles/test_policy.py`

- `P-A`, `P-B`, `P-C` — unverändert im Ergebnis, nur um den Hash ergänzt.
- `P-D` — unverändert: Hash A, kein Objekt, Vermerk mit Subjekt Hash A.
- `P-E` — Hash A, Objekt B. Erwartung ist jetzt `pytest.raises(ValueError)`; der bisherige
  Vermerkvergleich entfällt.
- `P-F` — unverändert.
- `P-G` — Genesis A **ohne Key `4`**, `scope` daraus gerechnet, Verfassung A mit ihrem Hash.
  Erwartung ist jetzt das **normale** Ergebnis: Boden, keine Vermerke. Der Docstring nennt D168
  als Grund. Das bisherige `broken`-Genesis führt `[6] = 1` und keinen Key `4`; es bleibt in
  dieser Form, ergänzt um nichts.
- `P-H` — **neu.** Genesis A, `constitution_hash` = Hash **B**, `constitution_obj=None`.
  Erwartung: Boden plus genau ein `CONSTITUTION_UNAVAILABLE` mit Subjekt Hash **B**. Der
  Docstring hält fest, dass dieser Vektor als einziger den übergebenen Hash von `genesis[4]`
  trennt (`03-golden-anchors.md §4`).

Der Modulname im Kopf der Datei nennt heute „P-A … P-F"; er wird auf den tatsächlichen Umfang
gezogen.

### 2.5 `tools/example_nucleus.py`

`_policy` baut die Policy heute von Hand aus `ex.constitution_gov["irrevocable_predicates"]` und
umgeht damit die normative Auflösung. Neu geht es durch `resolve_policy` und nimmt die Verfassung,
zu der es gehört:

```
_policy(ex, constitution_h, obj) -> NucleusPolicy
```

Die Funktion prüft, dass `findings` leer ist, und bricht sonst mit `AssertionError` ab — ein
stiller `CONSTITUTION_UNAVAILABLE` darf sich hier nicht als Boden tarnen.

Die sechs Aufrufstellen: `_member` reicht das Paar weiter, das es ohnehin bekommt; die übrigen
fünf übergeben `ex.constitution_hash_gov, ex.constitution_gov`. **Kein Ergebnis darf sich
bewegen** — `constitution_2` entsteht als `dict(constitution_gov)` mit geändertem `participants`,
`irrevocable_predicates` ist in beiden Fassungen dieselbe Liste.

## 3. Nicht-Ziele

Was hier steht, wird **gemeldet, nicht gebaut**.

- Keine Änderung an einer Spec-Datei, an `03-golden-anchors.md`, an `example-nucleus.md` oder an
  einer Prompt-Datei im Wurzelverzeichnis.
- Keine Änderung an den erwarteten Werten der Vektoren über die in 2.4 genannten hinaus. Keine
  Änderung an `DOC_*`-Konstanten, an den Fixtures `GENESIS_A/B/C`, `CONSTITUTION_A/B/C` oder an
  einem Golden Anchor einer anderen Schicht.
- Keine Vorgabe für `constitution_hash`. Ein Default auf `genesis_obj[4]` wäre genau der stille
  Rückfall, den D167 abschafft.
- Keine Funktion, die die geltende Verfassung aus der Epochenkette bestimmt (D161).
- Keine Änderung an `membership`, an `resolve_authorized_keys` oder an `NucleusPolicy`.
- Keine neue Abhängigkeit. Kein `float`, kein `fractions`.

## 4. Abnahmekriterien

1. `make check-all` grün, kalt gemessen: `.hypothesis/` und alle `__pycache__` vorher gelöscht
   (Prüfregel 19).
2. Testzahl vorher und nachher, **gegrept, nicht geschätzt**.
3. `.venv/bin/python tools/example_nucleus.py` läuft durch und gibt dieselbe Tabelle aus wie vor
   dem Lauf.
4. `grep -rn "CONSTITUTION_HASH_MISMATCH" --include=*.py .` liefert nach dem Lauf **null**
   Treffer. In den Spec- und Prompt-Dateien bleibt der Name stehen; das ist kein Rückstand,
   sondern D168.
5. Die drei Rücknahmeproben aus 4.1.
6. Kein `git add -A`; explizite Pfade.

### 4.1 Rücknahmeproben

Je Änderung eine, mit dem Namen des roten Tests und der Bestätigung, dass sonst nichts rot wird
(Prüfregel 23). Nach jeder Probe den Zustand davor wiederherstellen; die Proben stehen nicht im
Commit.

1. Schritt 4 wieder als Vermerk statt `ValueError`. Erwartet: `test_P_E` rot, `test_P_D` grün.
2. Die Prüfung auf `genesis_obj[4]` aus Schritt 2 wieder einbauen. Erwartet: `test_P_G` rot,
   `test_P_F` grün.
3. Subjekt des Vermerks in Schritt 3 auf `genesis_obj.get(4)` umstellen. Erwartet: `test_P_H`
   rot und **`test_P_D` grün** — dort sind beide Hashes derselbe Wert, und genau deshalb gibt es
   `P-H`. Wird auch `P-D` rot, ist der Vektor anders gebaut als beschrieben: melden.

## 5. Abschluss

Ein Commit auf `03b-epochenschritt`. Im Bericht: `git diff --numstat` gegen den Branchpunkt
(`git merge-base main 03b-epochenschritt`), die Testzahlen, die drei Proben, und alles, was nach
Abschnitt 3 gemeldet statt gebaut werden musste.

Rückfragen gehen an den Supervisor, nicht ins eigene Fenster.
