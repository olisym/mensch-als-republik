# Lauf 00o — dritte `ruff`-Gruppe `ARG` und die zwei ungenutzten Ankerspalten

## Branch und Basis

```
git switch -c impl/00o-arg
set BASIS (git rev-parse HEAD)
echo $BASIS
```

## Normative Grundlage

- `07-decisions.md`, **D205**. Die Entscheidung, die Zahlen und die ausdrückliche Verneinung einer
  Zeilenlängenregel für Python stehen dort.
- `07-decisions.md`, **D182**, das den Nachweis verlangt hat, und **D199**, das die
  Zeilenlängenfrage hierher verwiesen hat.
- `02-golden-anchors.md §7`, Tabelle „Erreichbarkeit nachgerechnet" — die fünf Spalten, die
  `tests/trust/test_bootstrap.py` parametrisiert.
- **Prüfregel 36**: die beiden neuen Behauptungen fügen eine Adresse hinzu, keine Erkennung. Das
  ist beabsichtigt und kein Grund, sie stärker zu bauen als beschrieben.

## Auftrag

### 1. `ARG` zuschalten

In `pyproject.toml` wird die Auswahl unter `[tool.ruff.lint]` von `["F401", "F811"]` auf
`["ARG", "F401", "F811"]` erweitert. Sonst nichts an der Datei.

`check-lint` ruft `ruff check mensch_als_republik tests tools` ohne eigene Select-Liste; die
Gruppe greift damit unmittelbar. Am `Makefile` wird nichts geändert.

### 2. Den toten Parameter entfernen

`tools/check_specs.py`: `check_references` nimmt `path_name` entgegen und benutzt es nicht. Der
Parameter wird **entfernt**, nicht mit einem Unterstrich stillgelegt, und die eine Aufrufstelle
wird mitgezogen. Ein toter Parameter ist kein Fall für eine Ausnahme.

### 3. Die zwei ungenutzten Ankerspalten prüfen

`tests/trust/test_bootstrap.py`: `test_bootstrap_rows` parametrisiert `expected_n` und
`expected_cap` und benutzt beide nicht. Beide werden benutzt.

**`expected_n`** wird gegen die tatsächlich erzeugte Welt gehalten, nicht gegen eine Formel im
Test. Aus den Claims der Welt werden über `build_groups` aus
`mensch_als_republik.trust.groups` die Gruppen gebildet, und die Menge der `n_kante` über alle
Gruppen muss genau `{expected_n}` sein. `build_groups` braucht die Klassifikation aus
`classify_all(store, NOW, None)`, den Scope, `PARAMS.D` und `NOW`.

**`expected_cap`** wird gegen die Arithmetik der Ankertabelle gehalten: `expected_trust` muss
`m * expected_cap` sein. Eine direkte Behauptung gegen die Implementierung ist nicht möglich —
`cap` ist über `TrustResult` nicht sichtbar und wäre als nachgerechnete Formel im Test zirkulär.
Diese Einschränkung ist in D205 benannt; sie ist **nicht** durch Aufbohren der Schnittstelle zu
umgehen.

Beide Behauptungen kommen unmittelbar nach dem Aufbau von `store` und `anchors` und vor der
Schleife über die Neulinge. Es entstehen **keine neuen Testfunktionen**; die Testzahl bleibt bei
587.

## Nicht-Ziele

Was hier nicht steht, wird **gemeldet, nicht gebaut**.

- **Keine `line-length` in `pyproject.toml`**, weder 88 noch 100 noch sonst ein Wert. D205 hat das
  mit Zahlen verneint.
- **Kein Umbrechen bestehender langer Zeilen**, auch nicht der zwölf über 120 Zeichen in
  `test_vectors.py` und `test_invariants.py`.
- **Keine weitere `ruff`-Gruppe** neben `ARG`.
- **Keine `noqa`-Kommentare und keine `per-file-ignores`.** Bleibt nach der Reparatur ein
  `ARG`-Fund übrig, wird er **gemeldet**, nicht stillgelegt.
- **Keine Änderung an `02-golden-anchors.md`** oder einer anderen Spec-Datei.
- **Keine Änderung an `mensch_als_republik/`.** Der Produktivcode hat null `ARG`-Funde.
- **Kein Aufbohren von `TrustResult`**, um `cap` sichtbar zu machen.

## Abnahmekriterien

1. `make check` grün. Der `ruff`-Lauf umfasst jetzt `ARG` und meldet **null** Funde.
2. Testzahl **587**, unverändert. Steigt sie, ist eine Testfunktion entstanden, die nicht
   beauftragt war.
3. `git diff --numstat $BASIS` nennt **genau drei** Dateien: `pyproject.toml`,
   `tools/check_specs.py`, `tests/trust/test_bootstrap.py`.
4. Drei Rücknahmeproben, jede einzeln gefahren und danach zurückgenommen.

**Probe N** — in der Zeile für `m = 1` der Parametrisierung `expected_n` von 4 auf 3 setzen.
Erwartet rot, **genau einer**: `test_bootstrap_rows` in der `m = 1`-Zeile.

**Probe O** — in derselben Zeile `expected_cap` von 2 auf 1 setzen. Erwartet rot, **genau einer**:
`test_bootstrap_rows` in der `m = 1`-Zeile.

**Probe P** — `path_name` in `tools/check_specs.py` wieder einführen, ohne es zu benutzen.
Erwartet: `ruff check` meldet **genau einen** `ARG001`. Das ist der Nachweis, dass die neue Gruppe
tatsächlich beisst und nicht nur in der Konfiguration steht.

Die Proben N und O treffen jeweils eine Zeile der Tabelle, nicht die Implementierung. Das ist
richtig so: die beiden Behauptungen bewachen die Übertragung des Ankers in den Test. Eine Probe,
die stattdessen die erzeugte Welt verfälscht, färbt fünf Fälle rot und belegt damit nichts über die
neuen Zeilen (D205, Prüfregel 36).

## Abschluss

**Ein** Commit auf `impl/00o-arg`. **Kein** Merge, **kein** Push.

Der Bericht nennt `$BASIS`, den Commit-Hash, `git diff --numstat $BASIS`, die Testzahl, die Zahl
der `ruff`-Funde und für jede der drei Proben das tatsächliche Ergebnis.

Widerspricht eine Messung diesem Prompt, wird sie **gemeldet**. Kein Wert wird nachgezogen.
