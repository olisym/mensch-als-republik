# 00t — Zeiger im Code berichtigen und prüfbar machen

## Branch und Basis

Branch: `impl/00t`, abgezweigt von `main` genau bei dem Commit, der diese Datei einführt —
also `git switch -c impl/00t main` ohne vorheriges Auschecken eines älteren Standes.
Normative Grundlage: **D215** und **D216** in `07-decisions.md`, unverändert seit **`ce75944`**.

## Auftrag

Fünf Dateien, vier voneinander unabhängige Eingriffe. Kein Verhalten ändert sich; die Testzahl
bleibt bei **597**.

### 1. `mensch_als_republik/findings.py` — drei Zeiger auf `00 §10`

Drei Docstrings zeigen auf Abschnitte, die ihre Aussage nicht tragen. Alle drei nennen künftig
`00 §10`:

| Zeile | steht heute | steht danach |
|---|---|---|
| 1 | `(00 §5.4, D163, D164)` | `(00 §10, D163, D164)` |
| 16 | `(00 §5.4, D163, D164)` | `(00 §10, D163, D164)` |
| 23 | `(04-prompt.md §2)` | `(00 §10)` |

Der Text der Docstrings bleibt sonst Wort für Wort stehen. Danach kommt in dieser Datei weder
`§5.4` noch `04-prompt` vor.

### 2. `mensch_als_republik/predicates.py` — `is_nuc_predicate` löschen

Die Funktion samt Docstring entfernen, neun Zeilen einschliesslich der Leerzeilen davor. Sonst
nichts: `_NUC_PREDICATE` bleibt, es wird von `parse_predicate` selbst benutzt.

### 3. `tests/test_predicates.py` — Modulkonstante und der Wegfall

- Eine Modulkonstante `NICHT_STR_FORMEN` mit den vier Formen, die heute zweimal als Literal
  in einem `parametrize` stehen. Reihenfolge unverändert.
- Beide `parametrize` beziehen sich darauf statt auf ein Literal.
- `is_nuc_predicate` aus dem Import entfernen.
- In `test_praedikatpruefer_non_str_p_returns_false` die Zusicherung zu `is_nuc_predicate`
  streichen. Die beiden anderen bleiben.

### 4. `tests/trust/test_distanzkauf.py` — ein Zeiger

Der Docstring von `_n_auf_der_schwelle` nennt einen Abschnitt 2.7 von `02`, den es nicht gibt.
`02` führt unter Abschnitt 2 keine Unterabschnitte. Die Aussage der Zeile steht in `02 §3`.
Nur der Abschnittsverweis ändert sich, der Rest des Docstrings bleibt.

### 5. `tools/check_specs.py` — die Verweisprüfung über Python

`check_section_refs` läuft zusätzlich über alle `.py`-Dateien unterhalb der Wurzel.

- Dateimenge: `ROOT.rglob("*.py")`, stabil sortiert, **`.venv` ausgeschlossen**.
- Es läuft **nur** `check_section_refs`. `check_escapes` und `check_control_chars` laufen
  **nicht** über Python — Backslashes sind dort legitim.
- Befunde nennen den Pfad relativ zur Wurzel und werden wie die übrigen Befunde gezählt: bei
  mindestens einem Befund endet das Werkzeug mit Rückgabewert 1.
- Ohne Befund eine `ok`-Zeile in der Bauform der übrigen, die die Zahl der geprüften Dateien
  und die Zahl der gefundenen Verweise nennt.

## Nicht-Ziele

Was hier nicht steht, wird gemeldet und nicht gebaut.

- **`mensch_als_republik/governance/findings.py` bleibt unangetastet.** Der dortige
  `dedupe_sort`-Docstring nennt dieselbe Quelle und ist richtig, weil Governance die eigene
  Schicht ist (D215).
- **`mensch_als_republik/policy.py` und `tests/governance/test_anchors.py` bleiben
  unangetastet.** Beide zeigen ebenfalls auf die Prompt-Datei der Schicht 04.
- **Keine weiteren Zeigerkorrekturen.** Fällt ein weiterer falscher Verweis auf: melden.
- **`mensch_als_republik/verifier.py` und `mensch_als_republik/index.py` bleiben unangetastet.**
  `is_core_predicate` wird nicht angefasst.
- **Keine Spec-Datei ändert sich.** Auch `07-decisions.md` nicht.
- **Keine Verhaltensänderung.** Kein neuer Reject-Code, keine geänderte Fangbreite, keine
  geänderte Grammatik.
- **Keine Zeilenlängenregel für Python.** D205 hat das entschieden.

## Abnahmekriterien

Abgeleitet aus einer vollständig gebauten Variante auf `ce75944`. Weicht eine Messung ab:
**melden, nicht anpassen.**

1. `.venv/bin/python -m pytest -q` meldet **597 passed**.
2. `.venv/bin/ruff check mensch_als_republik tests tools` ist sauber.
3. `.venv/bin/python tools/check_specs.py` gibt Rückgabewert 0 und nennt in der neuen Zeile
   **120 Dateien** und **60 Verweise**.
4. `grep -rn is_nuc_predicate mensch_als_republik tests tools` findet **nichts**.
5. `grep -c "00 §10" mensch_als_republik/findings.py` ergibt **3**.
6. `grep -c NICHT_STR_FORMEN tests/test_predicates.py` ergibt **3** — Definition und zwei
   Bezugnahmen.
7. Zur Orientierung die Vorabmessung der Zeilenmengen; eine Abweichung ist kein Fehler, aber
   sie wird gemeldet und erklärt:

   | Datei | + | − |
   |---|---|---|
   | `mensch_als_republik/findings.py` | 3 | 3 |
   | `mensch_als_republik/predicates.py` | 0 | 9 |
   | `tests/test_predicates.py` | 9 | 20 |
   | `tests/trust/test_distanzkauf.py` | 1 | 1 |
   | `tools/check_specs.py` | 33 | 0 |

## Proben

Beide werden gefahren und **wörtlich** berichtet, mit Rückgabewert und der vollständigen
Meldung. Danach wird der Zustand vor der Probe wiederhergestellt und die Wiederherstellung
belegt.

**Probe A — die neue Prüfung muss rot werden.** Den Abschnittsverweis in
`tests/trust/test_distanzkauf.py` zurück auf den alten, nicht existierenden Abschnitt setzen.
Erwartet: `tools/check_specs.py` gibt Rückgabewert **1** und genau **eine** Meldung, die die
Datei und den nicht existierenden Abschnitt nennt. Nach dem Zurücksetzen wieder Rückgabewert 0.

**Probe B — die Kopplung der beiden `parametrize`.** Eine fünfte Form `3.5` an `NICHT_STR_FORMEN`
anhängen. Erwartet: `.venv/bin/python -m pytest -q tests/test_predicates.py` meldet **25 passed**
statt 23 — zwei zusätzliche Prüffälle, nicht einer. Nach dem Zurücksetzen wieder 23.

**Ohne Probe bleiben Eingriff 1 und Eingriff 2.** Für die drei Zeiger in `findings.py` gibt es
keine, weil `00 §5.4` existiert und die neue Prüfung bei einer Rücknahme grün bliebe. Für die
Löschung gibt es keine, weil es keinen Aufrufer gibt, der rot werden könnte. Beides ist in D215
und D216 so festgehalten; es wird **nicht** versucht, dafür eine Probe zu erfinden.

## Abschluss

Ein Commit auf `impl/00t`. Kein Merge, kein Push, kein Rebase. Der Bericht nennt den
Commit-Hash, die Ausgabe der beiden Proben und jede Abweichung von den Zeilenmengen.
