# 00d-Nachlauf — Vektoren, isolierende Tests, drei Befunde

## Branch und Basis

Branch `00d-epochenkette`, bereits vorhanden. Basis ist der Kopf nach dem Merge von `main` in den
Branch; darin stehen `04 §4.5`, `04 §4.4` in der erweiterten Fassung und D174 bis D178.
Ein weiterer Commit. Kein Merge nach `main`, kein Push.

## Lage

Der Lauf `46b045e` ist geprüft. Drei Abnahmekriterien des vorigen Prompts waren falsch, die
Messung war richtig; die betreffenden Tests sind rot, weil sie unmögliche oder ungenau gedachte
Weltzustände behaupteten. Sie werden **nicht gestrichen**. Was gemessen wurde, wird als Vektor
festgeschrieben, und die Normen, die eigentlich geprüft werden sollten, bekommen daneben je einen
eigenen, isolierenden Test.

Drei weitere Befunde aus der Abnahme kommen dazu.

## Auftrag A — die drei Messungen werden Vektoren

Die Erwartungen sind aus der Spec **abzuleiten**, nicht aus einem Testlauf abzuschreiben. Wo die
Ableitung nicht aufgeht, ist das zu melden, nicht anzugleichen.

**A1 — ohne `C3` endet die Kette bei Epoche 2.** `test_chain_missing_c3_still_reaches_epoch_3`
wird zu einem Vektor mit sprechendem Namen. Ableitung: `PROPOSAL_2` zielt auf `C3`; fehlt das
Objekt, ist `target_constitution_obj` leer, `decide` liefert `UNEVALUABLE` (`04 §3.5`), und
`verify_ratification` gibt `TALLY_UNEVALUABLE` (`04 §4.1`). Erwartet werden
`EPOCH_2.epoch_id`, `constitution_obj == C2` und die daraus folgende Vermerksmenge.
Der Docstring nennt den Grund: das Verfassungsobjekt der Epoche `i+1` ist zugleich das Zielobjekt
des Übergangs. Daraus folgt der Satz, der auch in A4 geprüft wird — `constitution_obj` kann nur
an Epoche 1 leer sein.

**A2 — ohne `PROPOSAL_2` endet die Kette bei Epoche 1.** `test_chain_missing_proposal_2` behält
den Namen und bekommt die gemessene Erwartung. Ableitung: die Teilnehmer von `C1` sind Teilmenge
der Teilnehmer von `C2`, also stimmen dieselben Autoren zweimal. Ist `PROPOSAL_2` unbekannt,
blockieren ihre Stimmen aus Runde zwei nach `04 §4.4` ihre Stimmen aus Runde eins; alle vier
landen in `excluded`, und schon der erste Übergang trägt nicht. Erwartet werden `EPOCH_1`,
ein `EPOCH_PROPOSAL_UNAVAILABLE` mit `PROPOSAL_2.proposal_hash` und je ein
`UNSUPPORTED_RATIFICATION` auf jede von `r1` zitierte Stimme.
Der Docstring verweist auf **D178**. Dieser Test ist der Beleg für den dort festgehaltenen
Befund und darf nicht durch einen bequemeren ersetzt werden.

**A3 — ein falsch geschlüsseltes `C3` lässt die Kette bei Epoche 1.**
`test_chain_miskeyed_c3_like_missing` wird zu einem Vektor mit sprechendem Namen. Ableitung: liegt
`C3` unter dem Hash von `C2`, fehlt `C2`; damit fehlt das Zielobjekt des **ersten** Übergangs.
Erwartet werden `EPOCH_1`, `constitution_obj == C1` und die daraus folgende Vermerksmenge.

## Auftrag B — drei isolierende Tests

**B1 — `constitution_obj` ist leer, wenn die Verfassung der Epoche 1 fehlt.** Ein Speicher ohne
Ratifizierung, `known_constitutions` leer. Erwartet: Epoche 1, `constitution_obj` leer, keine
Vermerke. Das ist die einzige erreichbare Stelle für ein leeres Feld.

**B2 — ein unbekannter Vorschlag ohne Rückwirkung nach `04 §4.4`.** Zum Aufbau der zwei Übergänge
kommt eine Ratifizierung auf `PROPOSAL_ALT_A` (Vorgänger ist Epoche 2), **ohne** dass irgendjemand
auf `PROPOSAL_ALT_A` stimmt, und `PROPOSAL_ALT_A` fehlt in `known_proposals`. Ohne Ja-Stimme
greift `§4.4` nicht. Erwartet: `EPOCH_3.epoch_id` und genau ein `EPOCH_PROPOSAL_UNAVAILABLE` mit
`PROPOSAL_ALT_A.proposal_hash`.

**B3 — die Schlüsselprüfung schützt `resolve_policy`.** `known_constitutions` enthält `C2` unter
`CONSTITUTION_HASH_1`, also ein falsches Objekt unter dem Hash der **aktuellen** Epoche. Erwartet:
**kein** `ValueError`, sondern ein ordentliches Ergebnis bei Epoche 1. Ohne die Prüfung in
`chain.py` liefe `resolve_policy` in seinen `ValueError` nach D167. Das ist der eigentliche Zweck
dieser Prüfung; gegenüber `decide` ist sie sonst redundant.

## Auftrag C — drei Befunde

**C1 — `_is_nuc_name` ist dupliziert.** Die Funktion steht zeichengleich in `chain.py` und in
`epoch.py`. Dieselbe Regel an zwei Stellen ist der Defekt, den D147 notiert. `chain.py`
importiert sie aus `epoch.py`; die Kopie entfällt.

**C2 — der Nachzug in `decide` hat den Zweig verdoppelt.** Der neue Block prüft den Schlüssel und
schreibt `UNKNOWN_PROPOSAL` samt `excluded.add(author)`; der bestehende `else`-Zweig fünfzehn
Zeilen tiefer tut wörtlich dasselbe. Beide Fälle sind zu **einem** Zweig zusammenzuführen: ein
Eintrag, der fehlt oder nicht auf seinen Schlüssel passt, ist unbekannt und läuft in denselben
Pfad. Verhalten und Vermerke bleiben unverändert; der bestehende Test aus dem vorigen Lauf muss
grün bleiben.

**C3 — inaktive Ratifizierungen erzeugen Vermerke.** `ratifies` wird aus `all_claims()` gebildet,
und `EPOCH_PROPOSAL_UNAVAILABLE` entsteht, bevor `verify_ratification` gelaufen ist. Ein
widerrufener oder ersetzter `ratify` auf einen unbekannten Vorschlag meldet damit trotzdem.
Zu beheben: nur Claims im Zustand `ACTIVE` werden betrachtet. Die Form ist die, die `decide` und
`verify_ratification` bereits nutzen — `classify_all` je Iteration, weil die Policy je Epoche
wechselt.

**Ausdrücklich nicht mitgefiltert wird `t_exp`.** Ein Ratify mit Ablauf trägt zwar nicht, hat aber
nach `04 §4.1` einen eigenen Vermerk (`RATIFY_WITH_EXPIRY`). Diese Meldung muss erhalten bleiben.

Test dazu: derselbe Aufbau wie B2, aber die Ratifizierung auf `PROPOSAL_ALT_A` wird widerrufen.
Erwartet: `EPOCH_3.epoch_id` und **keine** Vermerke.

**C4 — ein Kommentar, wo heute nur Verhalten steht.** `findings` wird innerhalb der Schleife neu
angelegt; dadurch überleben nur die Vermerke der letzten Iteration. Das erfüllt `04 §4.5`, aber
durch Verwerfen statt durch Auswahl, und nichts sagt, dass es Absicht ist. Ein Kommentar mit dem
Verweis auf `§4.5` gehört an die Stelle, sonst zieht der nächste Umbau die Liste nach oben.

## Nicht-Ziele

- **Kein Test auf `EPOCH_FORK`.**
- **Keine Zyklusprüfung**, kein `policy`-Parameter, kein neues Protocol.
- **Keine Änderung** an den Erwartungen der acht Tests aus dem vorigen Lauf, die grün sind.
- **Keine Änderung** an `objects.py`, `keys.py`, `profiles/` oder an einer Spec-Datei.
- **Kein Anschluss** an `membership`, `resolve_authorized_keys` oder `tools/example_nucleus.py`.
- Was hier nicht steht, wird **gemeldet, nicht gebaut**.

## Abnahmekriterien

1. `make check` ist grün. Kein Test ist rot.
2. Die 544 Tests des Bestands bleiben grün.
3. `chain.py` enthält keine eigene Definition von `_is_nuc_name`.
4. In `decide` steht die Behandlung eines unbekannten Vorschlags an genau **einer** Stelle.
5. Jeder Vektor aus Auftrag A trägt einen Docstring, der den Grund nennt, nicht nur das Ergebnis.

## Rücknahmeproben

Drei Änderungen mit Schutzwirkung, drei Proben. Alle werden ausgeführt, das Ergebnis wird
berichtet, der Zustand danach wiederhergestellt.

- **Probe 1 (C3).** Den Aktivitätsfilter in `chain.py` entfernen. Erwartung: der Widerrufs-Test
  wird rot.
- **Probe 2 (B3).** Die Schlüsselprüfung für `known_constitutions` in `chain.py` entfernen.
  Erwartung: B3 wird rot, und zwar mit `ValueError`.
- **Probe 3 (C2).** Nach dem Zusammenführen die Schlüsselprüfung im vereinigten Zweig entfernen.
  Erwartung: `test_decide_miskeyed_proposal_is_unknown` wird rot. Bleibt er grün, hat das
  Zusammenführen die Reparatur verloren.

Widerspricht eine Messung diesem Prompt, ist das zu **melden, nicht anzupassen**.

## Abschluss

Ein Commit auf `00d-epochenkette`. `git add` mit expliziten Pfaden. Kein Merge, kein Push.
Der Bericht nennt: `git diff --numstat`, die neue Testzahl, das Ergebnis aller drei
Rücknahmeproben, und jede Stelle, an der der Prompt nicht ausgereicht hat.
