# `03` — Abnahme

Gelesen: `index.py`, `profiles/{__init__,findings,payload,policy,membership,credit,verdict}.py`
gegen `03-profiles.md`, `03-golden-anchors.md` und Register D55–D91. 306 Tests grün,
Arbeitsbaum sauber.

**Ergebnis: vier Befunde, einer davon substanziell.** Kein Befund liegt in der Ausführung eines
Vektors — alle vier liegen an Stellen, an denen die Spec nichts oder zu wenig gesagt hat, und
drei davon sind Asymmetrien zwischen Funktionen, die dasselbe tun sollten.

---

## 1. Was bestätigt ist

- **`read_v`** hat den Rundlauf in einem `try`, in der Reihenfolge aus D83. `h'ff'` und
  `h'a100ff'` laufen in `UNPARSABLE_V`, nicht in eine Exception.
- **Die scope-lokale Anwendung sitzt in `classify_all`**, nicht in den Aufrufern (D91). Kein
  Store-Wrapper, kein Filter.
- **`protected` deckt `revoke` *und* `supersede`.** Das ist richtig — `01 §5.4` sagt „unter
  dieser Policy ignorieren `revoke`/`supersede`, die auf solche Prädikate zielen". Ein
  `protected`, das nur `revoke` blockte, hätte dem Schuldner den Weg über `supersede` gelassen.
- **`CV-1` bis `CV-4` erzeugen zwei Vermerke**, `PARTIAL_RECEIPT_UNSUPPORTED` und den Grund der
  Unlesbarkeit. Wirkung und Diagnose stimmen beide.
- **Der `assert` in `settlement`** trägt die drei unerreichbaren Zustände und zusätzlich einen
  zweiten auf `ACTIVE` — die D75-Behandlung, sauber ausgeführt.
- **Tie-Break** über `min(claim_id)` in `membership` und `sort(key=claim_id)` in `settlement`:
  deterministisch, wie in `groups.py`.
- **`subject`** ist überall gesetzt, bei den Auflösungsbefunden der deklarierte
  `constitution_hash` (D90).

---

## 2. Befunde

### B1 — `verdict_status` prüft weder Prädikat noch Scope des Verdikts ⚠️

`settlement` beginnt mit:

```python
if not _is_nuc_name(obligation, "obligation") or obligation.N != scope:
    raise ValueError(...)
```

`verdict_status` hat keine Entsprechung. Ein Verdikt aus Nukleus B, mit `scope = N_A`
ausgewertet, wird nicht abgewiesen: `path_i` vergleicht `verdict.I` gegen die Arbitratoren von
A, und wenn der Autor dort steht, lautet die Antwort `BINDING`. Ein Schiedsrichter, der in zwei
Nuklei sitzt, bindet damit einen Streit, der nie in seinem Nukleus verhandelt wurde.

Dasselbe gilt für das Prädikat: `verdict_status(store, verdict=<irgendein Claim>, …)` läuft
durch, solange der Claim im Store liegt.

**Die Lücke ist meine.** `03 §1.4` normiert Scope-Gleichheit für *Beziehungen zwischen zwei
Claims* — `receipt` ↔ `obligation`, `accept-rules` ↔ `grant-membership`,
`submit-arbitration` ↔ `verdict`. Für den bewerteten Claim **selbst** steht die Regel nur bei
`settlement` (§3.3.2, letzter Absatz) und nirgends allgemein. `VS-1` bis `VS-11` enthalten
keinen Vektor dagegen, weil ich keinen geschrieben habe.

**Behebung:** `verdict_status` wirft `ValueError`, wenn `verdict` kein
`nuc:{scope}/verdict@1` ist — gleiche Klasse wie bei `settlement`, gleiche Begründung (D73:
falsche Zuordnung, keine sichere Voreinstellung). Dazu ein Vektor `VS-12` und ein Satz in
`03 §1.4`, der die Regel vom Beziehungsfall auf den bewerteten Claim ausdehnt.

### B2 — `EXPIRING_OBLIGATION` erscheint genau dann, wenn er nutzlos ist

Der Vermerk wird nur im `EXPIRED`-Zweig gesetzt:

```python
if o_state == State.EXPIRED:
    if obligation.t_exp is not None:
        findings.append(Finding(EXPIRING_OBLIGATION, o_cid))
```

Eine **aktive** Obligation mit `t_exp` in der Zukunft erzeugt keinen Vermerk. Das ist der Fall,
für den er gedacht war: `03 §3.3.1` begründet ihn damit, dass der Gläubiger `t_exp` **vor der
Gegenleistung** sichtbar haben soll. Nach dem Verfall ist die Warnung wertlos — die Schuld ist
bereits erloschen, und `EXPIRED` sagt es ohnehin.

**Behebung:** Der Vermerk gehört unbedingt zu `obligation.t_exp is not None`, unabhängig vom
Zustand — also in `_obligation_v_findings` bzw. gleich daneben. `SE-8` bleibt grün; ein neuer
Vektor prüft die aktive befristete Obligation.

### B3 — `accusation.N != scope` meldet `UNKNOWN_ACCUSATION` statt `SCOPE_MISMATCH`

Die Anklage ist bekannt; sie liegt nur im falschen Nukleus. `UNKNOWN_ACCUSATION` schickt den
Betreiber in die Partitionsecke, obwohl das Objekt vor ihm liegt. `03 §1.4` sieht für genau
diese Lage `SCOPE_MISMATCH` vor.

Wirkung unverändert (Pfad (ii) nicht auswertbar), Diagnose falsch — dieselbe Klasse wie D74 und
D90. Behebung: eine Zeile, plus Präzisierung in `03 §2.4.4`, welcher Vermerk zu welchem der vier
Nicht-Auflösbar-Fälle gehört.

### B4 — `verdict_status` wirft `KeyError`, wo `settlement` `ValueError` wirft

`by_cid[v_cid]` läuft in einen `KeyError`, wenn das Verdikt nicht im Store liegt. `settlement`
fängt denselben Fall ab (`store.get(o_cid) is None` → `ValueError`). Zwei Funktionen, dieselbe
Lage, zwei Fehlertypen. Behebung geht mit B1 zusammen.

### B5 — `_dedupe_sort` ist als privat benannt und wird von vier Modulen importiert

Der Unterstrich sagt „modul-privat", der Import sagt das Gegenteil. Kosmetisch, aber es erzeugt
beim nächsten Leser eine falsche Annahme über die Oberfläche. `dedupe_sort` ohne Unterstrich.

### B6 — `resolve_policy` wirft `KeyError` bei einem Genesis ohne Key `4`

Der Scope-Check schützt nicht davor: `scope` wird *aus* `genesis_obj` gerechnet, also passiert
jedes Objekt den Vergleich, das der Aufrufer selbst gehasht hat.
`resolve_policy(scope=sha(DOM ‖ cbor({})), genesis_obj={})` läuft in den `KeyError`. Ein Genesis
ohne `constitution_hash` ist kein Teilwissen, sondern ein defektes Objekt — dieselbe Klasse wie
der Scope-Fehler, also `ValueError`. Ebenfalls ungeprüft: ob `irrevocable_predicates` eine Liste
von Strings ist.

---

## 3. Getragene Grenzen

- **Die Duplikation in `index.py` ist mit D87 tiefer geworden.** Vorher dupliziert das Modul die
  Zustandsmaschine, jetzt zusätzlich die Policy-Semantik. Das ist die bewusste Bauform dieses
  Moduls, aber `PR-INV-11` ist damit die einzige Sicherung gegen Drift in zwei Dimensionen statt
  einer. Wer `verifier.classify` anfasst, muss `index.py` mit anfassen — und der Kopplungstest
  ist das Einzige, was ihn daran erinnert.
- **Ein inaktives Verdikt sammelt weiterhin alle übrigen Vermerke ein**, bevor
  `INACTIVE_VERDICT` gesetzt wird. Das ist mehr Information, nicht weniger, und bleibt so.
- **`membership` vermerkt `CONSTITUTION_VERSION_MISMATCH` auch für inaktive `accept-rules`.**
  Rauschen, aber in die harmlose Richtung.

---

## 4. Folgeänderungen

| Datei | Änderung |
|---|---|
| `03-profiles.md §1.4` | Scope-Gleichheit gilt auch für den **bewerteten** Claim, nicht nur für Beziehungen (B1) |
| `03-profiles.md §2.4.2` | `ValueError` bei falschem Prädikat oder Scope des Verdikts (B1, B4) |
| `03-profiles.md §2.4.4` | welcher Vermerk zu welchem Nicht-Auflösbar-Fall gehört (B3) |
| `03-profiles.md §3.3.1` | `EXPIRING_OBLIGATION` gilt unbedingt bei `t_exp`, nicht nur bei Verfall (B2) |
| `03-profiles.md §1.2` | `ValueError` bei defektem Genesis-Objekt (B6) |
| `03-golden-anchors.md §9` | `VS-12` Verdikt aus fremdem Scope, `VS-13` falsches Prädikat (B1) |
| `03-golden-anchors.md §8` | Vektor: aktive Obligation mit `t_exp` in der Zukunft (B2) |
| `03-golden-anchors.md §9` | `VS-7`-Zeile: Anklage aus fremdem Scope liefert `SCOPE_MISMATCH` (B3) |
| `profiles/verdict.py` | B1, B3, B4 |
| `profiles/credit.py` | B2 |
| `profiles/findings.py` | B5 |
| `profiles/policy.py` | B6 |

---

## 5. Muster

**Drei der sechs Befunde sind Asymmetrien zwischen `settlement` und `verdict_status`** —
Eingangsprüfung, Fehlertyp, Vermerkwahl. Beide Funktionen nehmen einen Claim entgegen, bewerten
ihn im Scope und geben Zustand plus Vermerke zurück; sie hätten dieselbe Eingangsstrecke haben
müssen. `03 §3.3.2` hat sie für `settlement` ausgeschrieben und `§2.4.2` für `verdict_status`
nicht, weil ich beim Schreiben von `§2.4` in der Bindungsfrage steckte und nicht in der
Eingangsprüfung.

Das ist eine neue Form gegenüber D74/D75/D83/D87/D91: dort verlor eine Begründung beim
Übertragen ihren Geltungsbereich. Hier wurde eine Regel gar nicht erst übertragen — sie steht
an einer Stelle richtig und an der parallelen nicht. Für den Sitzungsabschluss vermerkt.
