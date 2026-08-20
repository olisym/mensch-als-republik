# Lauf `00b` — Anker aus der Verfassung, Spaltung entwertet die Wurzel

## 0. Branch und Basis

Branch `00b-anker`, abgezweigt vom Kopf von `main`. Ein Commit am Ende. Kein Merge, kein
Push nach `main`.

## 1. Normative Grundlage

- `00-nucleus-genesis-constitution.md` §5.4 und §6.4, Stand des Branchpunkts. Die Spec ist bereits
  nachgezogen und wird in diesem Lauf **nicht** geändert.
- `03-profiles.md` §4 (`authorized_keys` als Parameter), `04-governance.md` §5 (Schlüsselpfad).
- Register D150, D151, D153, D154, D155, D161, D162, D163, D164.

Widerspricht eine Messung diesem Prompt: **melden, nicht anpassen.** Keine Golden Anchors
nachziehen, um einen Test grün zu bekommen.

## 2. Auftrag

### 2.1 `mensch_als_republik/findings.py` (neu)

Vermerke der Nukleus-Schicht, in der Bauform von `mensch_als_republik/profiles/findings.py`:
ein `str`-Enum `NucleusFinding` mit den beiden Werten `CONSTITUTION_UNAVAILABLE` und
`MALFORMED_NUCLEUS_KEY`, eine eingefrorene Dataclass `Finding` mit `kind` und `subject: bytes`,
und `dedupe_sort`. Eigenes Modul, weil `profiles`, `governance` und `trust` je eines haben und
`keys.py` in keiner dieser Schichten liegt. Die Namensgleichheit mit
`ProfileFinding.CONSTITUTION_UNAVAILABLE` ist beabsichtigt; die Enums werden **nicht**
zusammengelegt.

### 2.2 `resolve_authorized_keys` in `mensch_als_republik/keys.py`

```
resolve_authorized_keys(store, *, scope, genesis_obj, constitution_hash,
                        constitution_obj=None, now, policy=None)
    -> KeyResolution(keys: frozenset[bytes], findings: tuple[Finding, ...])
```

Ablauf, Schritt 1 aus `00 §6.4`:

1. `scope` gegen `SHA-256(DOM_NUC_GEN || cbor_canon.encode(genesis_obj))` nachrechnen. Abweichung
   ist `ValueError` (D161).
2. `genesis_obj[1]` lesen. Fehlt der Schlüssel, ist der Wert keine Liste, oder ist ein Eintrag
   nicht `bytes` der Länge 32: `ValueError` (D161). Eine leere Liste ist zulässig.
3. Ist `constitution_obj` `None`: Anker ist `frozenset(genesis_obj[1])`, ein Vermerk
   `CONSTITUTION_UNAVAILABLE` mit Subjekt `constitution_hash` (D164).
4. Sonst `constitution_hash` gegen die kanonische Hashung von `constitution_obj` nachrechnen.
   Abweichung ist `ValueError` (D161).
5. Nennt die Verfassung kein Feld `nucleus_keys`: Anker ist `frozenset(genesis_obj[1])`, keine
   Vermerke.
6. Nennt sie eines: Anker ist die Menge der wohlgeformten Einträge — `bytes` der Länge 32. Jeder
   formwidrige Eintrag erzeugt `MALFORMED_NUCLEUS_KEY` mit Subjekt `constitution_hash`; mehrere
   ergeben nach `dedupe_sort` einen Vermerk, und das ist beabsichtigt (D163). Ist der Wert keine
   Liste und kein Tupel — insbesondere ein `str` —, ist der Anker leer und der Vermerk gesetzt.
   **Ein gesetztes Feld fällt nie auf `genesis_obj[1]` zurück**, auch nicht, wenn kein Eintrag
   wohlgeformt ist (D163).
7. `resolve_current_key(store, scope=scope, anchor_keys=<Anker>, now=now, policy=policy)`
   aufrufen und das Ergebnis als `keys` zurückgeben.

`resolve_current_key` bleibt unverändert — Signatur und Rumpf, abgesehen von 2.3.

### 2.3 Erweiterte Equivocation-Prüfung in `_head_from`

Heute prüft `_head_from`, ob ein **Rotate** von `k_cur` im Zustand `EQUIVOCATION_FLAGGED` ist.
Neu: hat `k_cur` **irgendeinen** Claim in diesem Zustand — beliebiges Prädikat, beliebiger Scope
—, liefert `k_cur` keinen Kopf (D162). Die neue Prüfung subsumiert die alte; die alte wird
entfernt, nicht danebengestellt.

Keine Scope-Einschränkung: die Autorenkette ist identitäts- und nicht scopegebunden.

### 2.4 `tools/example_nucleus.py`

Neue Prüffunktion `check_anchor_resolution(ex)`, in `verify_all()` aufgenommen und in
`tests/test_example_nucleus.py` mit einem eigenen Test versehen, in der Form der übrigen. Drei
Lagen, die sich in genau einer Größe unterscheiden:

Alle Felder unten sind Felder von `ex`:

| Lage | `constitution_obj` | `constitution_hash` | erwartet |
|---|---|---|---|
| 1 | `constitution_gov` | `constitution_hash_gov` | `frozenset(genesis_gov[1])`, keine Vermerke |
| 2 | `constitution_2` | `constitution_hash_2` | dieselbe Menge, keine Vermerke |
| 3 | `None` | `constitution_hash_gov` | dieselbe Menge, ein `CONSTITUTION_UNAVAILABLE` |

Die erwartete Menge wird aus `ex.genesis_gov[1]` **abgeleitet**, nicht getippt. Dass sie
`{BRUNO, ANNA}` ist, sichert `build()` bereits über `_eq(anna.pub, DOC_ANNA)` und
`_eq(bruno.pub, DOC_BRUNO)`; das wird nicht wiederholt. Lage 2 gegen Lage 1 zeigt, dass das
Amendment den Anker nicht bewegt.

Ein leerer Store genügt, weil der Beispielnukleus keine Rotation führt. Das ist der Fall und
keine Lücke.

Zusätzlich reicht `_member` die hergeleitete Menge an `membership` weiter, statt
`authorized_keys=frozenset()` zu übergeben. `check_membership_epoch1` und
`check_membership_epoch2` müssen unverändert grün bleiben — der Beispielnukleus führt kein
`grant-membership@1`, die Mitgliedschaft läuft über `participants`.

### 2.5 Tests

**Neu: `tests/nucleus/test_anchor.py`.** Elf Lagen, jede mit einem Satz, welche Entscheidung sie
trägt:

- a) Verfassung ohne `nucleus_keys` → Anker ist `root_keys`, keine Vermerke.
- b) `nucleus_keys` mit zwei wohlgeformten Einträgen, verschieden von `root_keys` → genau diese;
  kein Eintrag aus `root_keys` ist enthalten. Ersetzung, nicht Vereinigung (D150).
- c) `nucleus_keys = []` → leere Menge, **nicht** `root_keys` (D163, `00 §5.4`).
- d) ein formwidriger Eintrag neben einem wohlgeformten → der wohlgeformte wirkt, genau ein
  `MALFORMED_NUCLEUS_KEY` mit Subjekt `constitution_hash`.
- e) zwei formwidrige Einträge neben einem wohlgeformten → weiterhin genau ein Vermerk.
- f) alle Einträge formwidrig → leere Menge, nicht `root_keys`, Vermerk gesetzt.
- g) `nucleus_keys` ist ein `str` → leere Menge, Vermerk gesetzt.
- h) `constitution_obj=None` → `root_keys` plus genau ein `CONSTITUTION_UNAVAILABLE` mit Subjekt
  `constitution_hash`.
- i) `constitution_hash` passt nicht zu `constitution_obj` → `ValueError`.
- j) `scope` passt nicht zu `genesis_obj` → `ValueError`.
- k) `genesis_obj` ohne Schlüssel 1, mit einem Eintrag falscher Länge, und mit einem Eintrag, der
  kein `bytes` ist → je `ValueError`.
- l) Anker aus `nucleus_keys` **plus** vollständige Rotation: `root` rotiert vollständig auf `X`,
  die Verfassung nennt `Y`. Ergebnis ist `Y`, und weder `root` noch `X` sind enthalten. Das ist
  die Lage, für die `§5.4` geschrieben ist — der Rotate eines nicht mehr genannten Schlüssels
  verliert seine Wurzel.

**Erweiterung von `tests/nucleus/test_rotate_key.py`.** Zwei Läufe über derselben Menge, die
sich in genau einer Größe unterscheiden (Prüfregel 12):

- Lauf A: `root` schreibt `obligation@1`, dann einen vollständigen Rotate auf `nxt`. Ergebnis ist
  `{nxt}`.
- Lauf B: dieselbe Menge, dazu ein zweites `obligation@1` von `root` auf derselben `h_prev` —
  ein Equivocation-Paar an einem Nicht-Rotate-Claim. Ergebnis ist die leere Menge (D162).

Der Test bestätigt vorher über `classify_all`, dass der Rotate selbst `ACTIVE` und nicht
`EQUIVOCATION_FLAGGED` ist; sonst misst er den alten Mechanismus. Das ist der Grund, aus dem
`test_equivocation_at_chain_point_drops_that_root` diese Lage nicht abdeckt: dort equivozieren
die Rotationen selbst.

### 2.6 Vier Rücknahmeproben

Je Änderung eine, jeweils mit dem Namen des Tests, der rot wird, und mit der Bestätigung, dass
**sonst nichts** rot wird (Prüfregel 23):

1. Die Prüfung aus 2.3 auf die alte Fassung zurücksetzen — nur Rotationen. Erwartet: Lauf B aus
   2.5 wird rot, `test_equivocation_at_chain_point_drops_that_root` bleibt grün.
2. In 2.2 Schritt 6 auf Alles-oder-nichts umstellen — ein formwidriger Eintrag verwirft die ganze
   Liste. Erwartet: Lage d wird rot, Lage f bleibt grün.
3. In 2.2 Schritt 6 bei leerer wohlgeformter Menge auf `genesis_obj[1]` zurückfallen. Erwartet:
   Lage c und f werden rot, Lage b bleibt grün.
4. In 2.2 Schritt 3 den Vermerk weglassen und nur die Menge zurückgeben. Erwartet: Lage h wird
   rot, und zwar an der Vermerk-Zusicherung, nicht an der Menge.

Nach jeder Probe der Zustand vor der Probe wieder her. Die Proben stehen nicht im Commit.

## 3. Nicht-Ziele

Was hier steht, wird **gemeldet, nicht gebaut**.

- Keine Änderung an der Signatur oder am Rumpf von `membership()` in
  `mensch_als_republik/profiles/membership.py`. `authorized_keys` bleibt Parameter (`03 §4`).
- Keine Änderung an der Signatur von `resolve_current_key` (D151).
- Keine Änderung an einer Spec-Datei, an `example-nucleus.md` oder an einer Prompt-Datei im
  Wurzelverzeichnis. Der Nachzug dort wird bei der Abnahme gemacht.
- Keine Änderung an den `DOC_*`-Konstanten in `tools/example_nucleus.py`, an `genesis_gov`,
  `genesis_res`, den Verfassungsobjekten oder an einem Golden Anchor irgendeiner Schicht. Keine
  Norm dieses Laufs bewegt sie.
- `check_scope_separation` bleibt unverändert.
- Keine Funktion, die die jüngste ratifizierte Epoche bestimmt, und kein Lauf über die
  Epochenkette (D161). Die Verfassung wird übergeben.
- Keine Schwelle und kein `k`-von-`n` für `nucleus_keys`; das ist seit D126 offen.
- Keine neue Abhängigkeit. Kein `float`, kein `fractions`. `now` bleibt Parameter.

## 4. Abnahmekriterien

1. `make check-all` grün, kalt gemessen: `.hypothesis/` und alle `__pycache__` vorher gelöscht
   (Prüfregel 19).
2. Testzahl vorher und nachher, **gegrept, nicht geschätzt**.
3. Die vier Rücknahmeproben aus 2.6, jede mit dem Namen des roten Tests und der Aussage, dass
   sonst nichts rot wurde.
4. `python3 tools/example_nucleus.py` läuft durch und gibt dieselbe Tabelle aus wie vor dem Lauf.
5. Kein `git add -A`; explizite Pfade. Neue Dateien vor `make check` adden.

## 5. Abschluss

Ein Commit auf `00b-anker`. Im Bericht: `git diff --stat` gegen den Branchpunkt (`git merge-base main 00b-anker`), die Testzahlen, die
vier Proben, und alles, was nach Abschnitt 3 gemeldet statt gebaut werden musste.

Rückfragen gehen an den Supervisor, nicht ins eigene Fenster. Sie sind Kandidaten für
Spec-Lücken.
