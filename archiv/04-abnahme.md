# Layer 04 — Abnahme

Gegenstand: `impl/04-governance`, Commit `7ed93cd`, 16 Pfade, 370 Tests grün.
Geprüft gegen: `04-governance.md`, `04-golden-anchors.md`, Register D95–D107.

**Ergebnis: nicht abgenommen.** Fünf blockierende Befunde, zwölf weitere. Beschlüsse D108–D111
plus zehn Nachzüge ohne eigene Nummer; Korrektur über `04a-korrektur-prompt.md`.

## 0. Methode und Einordnung

Der Code wurde **zweimal unabhängig** gelesen, in zwei Sitzungen, ohne dass der zweite Durchgang
das Ergebnis des ersten kannte. `decide()` und `verify_ratification()` lagen beide Male
**nebeneinander**, nicht nacheinander (Konsequenz aus D106).

Der zweite Durchgang hat sich gelohnt: er hat einen Fehler im ersten korrigiert — die dort
behauptete Schwellengrenze `2*num > den` war zu streng und ohne Herleitung aufgeschrieben; richtig
ist `2*num >= den` — und sechs Befunde ergänzt, darunter einen Determinismusbruch. Der erste
Durchgang hatte fünf, die der zweite nicht fand.

**Kein einziger Befund ist eine Abweichung vom Prompt.** Das Werkzeug hat gebaut, was dastand, und
an der einzigen Stelle, an der die Spec keine Umsetzung zuließ (`§3.5`), hat es die Prüfung
konditionalisiert statt sie zu erfinden. Vier der fünf Blocker beschreiben Zeilen, die korrekt
befolgt wurden.

## 1. Blockierend

### A-1 — `2*num >= den` wird nirgends erzwungen

`governance/tally.py`, `_is_ratio`. D102 und `INV-04.6` stehen auf dem Quorenschnitt; geprüft wird
nur `int` und Länge 2. Mit `amendment = [1,3]` und `n = 5` genügen zwei Ja je Vorschlag — zwei
rivalisierende Vorschläge brauchen vier Stimmen aus fünf Mitgliedern und **kommen ohne jede
Überschneidung aus**. Zwei gültig ratifizierte Nachfolger derselben Epoche, ohne Doppelstimme.

`INV-04.6` ist grün, weil der geprüfte Bereich bei `1/2` beginnt: die Invariante prüft genau den
Bereich, in dem sie ohnehin gilt. → **D108**

### A-2 — Negativer Zähler macht `PASSED` ohne eine Stimme

Dieselbe Stelle. `[-1,2]` ergibt in `reached(0, n, -1, 2)` den Vergleich `0 > -n` — wahr. `[1,0]`
und `[5,4]` sind dauerhaft unerreichbar, diagnoselos. → **D108**

### A-3 — `verify_ratification` bindet `tally` an nichts

`governance/epoch.py`, Signatur. `epoch`, `proposal` und `tally` kommen unabhängig herein; nichts
prüft die Zusammengehörigkeit. Die Auszählung von Vorschlag A mit einem `ratify@1` für Vorschlag B
liefert eine Epoche. Dasselbe für `now`, das an beide Funktionen getrennt gereicht wird.

Das ist D106 eine Ebene höher: dort wanderte `participants` nach `TallyResult`, `epoch_id` und
`proposal_hash` blieben draußen. Die Reparatur wurde nicht auf die Geschwister ihrer eigenen Art
durchgezogen — dieselbe Form wie D105 zu D107. → **D109**

### A-4 — Die Paarprüfung lag in der Stimmschleife

`04 §3.1` führte `proposal.predecessor == epoch_id` als Stimmbedingung. Sie betrifft das Paar aus
Epoche und Vorschlag, nicht die einzelne Stimme. Folge bei wörtlicher Umsetzung: bei einem nicht
passenden Paar **ohne** Stimmen wird die Bedingung nie erreicht — die Auszählung läuft durch und
meldet `PENDING` statt eines Fehlers. → **D110**, Vektor `GV-41`

### A-5 — `membership()` prüft die Zugehörigkeit seiner Teilnehmerliste nicht

`profiles/membership.py`. `constitution_hash` und `participants` kommen unverbunden herein; eine
Liste aus Epoche 3 lässt sich mit dem Hash aus Epoche 2 verbinden und liefert `MEMBER`. Aus
`04-prompt.md §7`, nicht aus der Umsetzung. → **D111**

## 2. Weitere Befunde

| Nr. | Stelle | Befund | Folge |
|---|---|---|---|
| B-1 | `tally.py` | Identitätsprüfung des Zielobjekts kommt **nach** Klassen- und Schwellenprüfung, die es bereits lesen | Diagnose aus einem Objekt, das nicht das gemeinte ist → D110 |
| B-2 | `tally.py` | leere `participants` passiert die Formprüfung; `n = 0` macht jeden Vorschlag sofort `FAILED` | „abgelehnt" statt „niemand konnte abstimmen" |
| B-3 | `tally.py` | Klassenbestimmung steht zweimal: inline in `decide` und in `threshold_for` | zwei Implementierungen einer Regel in einer Datei |
| B-4 | `epoch.py` | `§4.1` Bedingung 4 („kein Autor zweimal") ist durch eine Invariante impliziert, nicht geprüft | bricht lautlos, wenn sich die Auszählung ändert |
| B-5 | `epoch.py` | `tally.state = UNEVALUABLE` liefert `UNSUPPORTED_RATIFICATION` | „Behauptung falsch" statt „nicht auswertbar" → `TALLY_UNEVALUABLE` |
| B-6 | `tally.py` | `STALE_EPOCH_VOTE` trifft auch Stimmen auf unbeteiligte Vorschläge | Rauschen; entfällt mit D110 |
| B-7 | `tally.py` | `SCOPE_MISMATCH` für jede `vote@1` eines fremden Nukleus im Store | Vermerkliste schwemmt im Multi-Nukleus-Store über |
| B-8 | `policy.py` | `NucleusPolicy.declared` wird im Konstruktor überschrieben | „erklärt gegen wirksam" nicht mehr feststellbar |
| B-9 | `policy.py` | `warnings` ohne `dedupe_sort`; bei `frozenset`-Eingabe unbestimmte Reihenfolge | **zwei Läufe, zwei verschiedene Tupel** — Determinismusbruch |
| B-10 | `policy.py` | ein `str` in `irrevocable_predicates` erzeugt zwölf Zeichen-Vermerke | zwölf Symptome, keine Ursache; Präzisierung zu D95 |
| B-11 | `04 §3.1` | Umsetzung prüft `t_exp` und `choice` vor `ACTIVE` | **Diagnose besser als die Spec** — Spec wird nachgezogen |
| B-12 | `04 §3.5` | `MALFORMED_THRESHOLD` vor `PROPOSAL_CONSTITUTION_UNAVAILABLE` | nicht implementierbar; Reihenfolge korrigiert |

B-9 ist der ernsteste der zwölf. B-11 ist der einzige Befund, bei dem die Spec dem Code folgt und
nicht umgekehrt — wie bei `Derivation(bfs, findings)` in Layer 02.

## 3. Was tragfähig ist

- `objects.py` exakt: Array für die Epoche, Map für den Vorschlag. Die Anker reproduzieren, und
  ein eigener Test reproduziert zusätzlich `890b21e7…` und `65309fe2…` aus `00 §3.1`.
- `findings.py` führt alle neunzehn Vermerke in der Hausform, mit `dedupe_sort`.
- **Die Falle aus `04-prompt.md §4.4` ist nicht zugeschnappt.** Die Konfliktprüfung läuft über die
  volle Stimmenliste, nicht über die bereits gefilterten Kandidaten. Das war die Stelle, an der
  der Lauf hätte kippen können, und sie ist richtig gebaut.
- `_is_yes_choice` prüft `type(value) is int` und schließt damit `True` aus. Nirgends verlangt,
  sauber gedacht.
- `verify_ratification` trennt `UNKNOWN_WITNESS_VOTE` von `UNSUPPORTED_RATIFICATION` korrekt an
  `store.get(cid) is None` (D106) und behandelt `UNEVALUABLE` als Ausschluss.
- D95 sitzt im Konstruktor, nicht im Resolver; `resolve_policy` reicht den Rohwert durch.
- Die vier Zustände aus `03` sind unverändert; `participants` wirkt rein additiv als zweite
  Aufnahmequelle.

## 4. Parallelenprüfung

| | `decide` | `verify_ratification` |
|---|---|---|
| Wählerschaft | aus `constitution_obj`, Hash geprüft | aus `tally` (D106) |
| Schwelle | aus beiden Verfassungen | aus `tally` |
| Epoche und Vorschlag | Parameter, gegen die Objekte geprüft | Parameter, **gegen nichts geprüft** (A-3) |
| Vermerk oder Schweigen | jede fehlgeschlagene Bedingung eigen | fünf Bedingungen teilen einen Sammelvermerk |

Zeile drei ist A-3. Zeile vier ist eine Beobachtung ohne Befund: Scope-Fehler, falscher Autor und
inaktiver Claim liefern denselben `UNSUPPORTED_RATIFICATION`, während `decide` an jeder Stelle
unterscheidet. Nach D94 wäre feiner besser; die Spec verlangt es nicht, und ich ziehe es nicht
nachträglich ein.

## 5. Konsequenzen

**A-3 ist die dritte Wiederholung derselben Form.** D105 schützte `vote@1` und vergaß `ratify@1`
(→ D107). D106 zog `participants` nach `TallyResult` und ließ `epoch_id` und `proposal_hash`
draußen (→ A-3). D109 löst es für `verify_ratification` und übersieht beinahe `membership()`
(→ D111). Jedes Mal war die Reparatur richtig und **unvollständig auf die Geschwister ihrer
eigenen Art**.

> **Erweiterung der Prädikatendurchgangs-Regel aus D107:** Wandert eine Eingabe aus
> Sicherheitsgründen an einen anderen Ort, werden **alle übrigen Eingaben derselben Funktion**
> daraufhin geprüft, ob dasselbe Argument für sie gilt — und die, für die es nicht gilt, werden
> ausdrücklich als geprüft benannt.

**A-1 ist die Voraussetzungsprüfung.** Die Bedingung `2*num >= den` stand in D102 in einem
Nebensatz der Begründung und in keiner prüfbaren Zeile. Trägt eine Invariante eine Voraussetzung,
gehört diese in dieselbe normative Tabelle wie die Invariante.

**Und eine über die Abnahme hinaus.** Der erste Durchgang hat eine Schranke behauptet statt sie
herzuleiten, und die eigene „Prüfung" bestätigte nur die eigene Annahme. Gefunden hat es der
zweite Durchgang, nicht ein Test. Wo eine Zahl eine Grenze zieht, gehört die Herleitung in den
Registertext — nicht die Behauptung.

## 6. Erwartung an die zweite Abnahme

Nach der Korrektur **mehr als 370 Tests**. Fällt die Zahl, ist etwas abgeschwächt worden. Neu
mindestens: `GV-35` bis `GV-45`, die Herleitungsprobe zu D108 als Eigenschaftstest über allen
`[num, den]` mit `den <= 12`, und ein Test, der `[1,2]` ausdrücklich als **zulässig** festhält.

---

## 7. Abschluss

Drei Korrekturrunden, alle Befunde behoben.

| Runde | Commit | Beschlüsse | Tests |
|---|---|---|---|
| Lauf | `7ed93cd` | — | 370 |
| 04a | `e576663` | D108–D111 | 384 |
| 04b | `5714bbc` | D112 | 387 |
| 04c | `8c1f255` | D113 | 387 |

Abgenommen mit `8c1f255`, gemergt als `c9e585c` — Layer 04 Governance (D96–D113). `make check`
grün in drei Blöcken, Register D1–D113 lückenlos, 387 Tests.

**Neunzehn Befunde, elf davon zwischen zwei Stellen statt in einer.** Kein einziger war eine
Abweichung vom Prompt: das Werkzeug hat jedes Mal gebaut, was dastand, hat viermal zurückgefragt
statt umzudeuten, und hat an der einen Stelle, an der die Spec keine Umsetzung zuließ (`§3.5`),
die Prüfung konditionalisiert statt sie zu erfinden. Was gefehlt hat, hat in den Dokumenten
gefehlt.

**Vier Konsequenzen im Register, alle vor dem Beheben ansetzend:**

- **Standprüfung** (D96, D102) — vor jedem Mechanismus zu Nebenläufigkeit, Ordnung oder Schwellen
  fragen, unter welchem Namen das Problem außerhalb des Projekts gelöst ist. Zwei eigene
  Vorschläge sind an CALM und an einem zehn Jahre alten Raft-Befund gescheitert, beide vor der
  Implementierung.
- **Prädikatendurchgang** (D107) — wird ein Prädikat mit einer Zustandsbedingung belegt, werden
  alle Prädikate derselben Schicht durchgegangen.
- **Zugehörigkeitsliste am Datentyp** (D112) — welche Felder eine Zugehörigkeit behaupten und
  wogegen sie zu prüfen sind, wird bei der Definition des Typs aufgeschrieben, nicht beim Beheben
  eines Befunds.
- **Abhängigkeitssatz bei Reihenfolgeänderungen** (D113) — wird eine Reihenfolge normativ
  geändert, wird für jede Größe, die in der alten nebenbei entstand, benannt, woher sie in der
  neuen kommt.

Die Kette D105 → D107 → D109 → D111 → D112 war viermal dieselbe Unvollständigkeit auf die
Geschwister der eigenen Art. D113 ist eine neue Form. Die ersten beiden Konsequenzen haben sie
nicht verhindert, weil sie beim Beheben ansetzen; die letzten beiden setzen beim Schreiben an.

**Zur inhaltlichen Bilanz.** Die Schicht ist kleiner geworden, als sie geplant war: keine
gewichtete Auszählung, kein Snapshot, kein Zweckgraph. Übrig blieb eine Kopfzahl über einer
deklarierten Wählerschaft, zwei Ungleichungen und eine Kette von Verfassungen. Entschieden hat das
nicht die Technik, sondern das Aufnahmekriterium aus `08 §3`: ein Mechanismus, der Macht verteilt,
gehört in die Verfassung eines Nukleus, nicht ins Protokoll.
