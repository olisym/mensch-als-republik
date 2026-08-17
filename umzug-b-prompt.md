# Umzugslauf B: die Simulation auf `Autor` (D127, D129)

Branch: `impl/umzug-b`. Ein Commit am Ende.

## Was dieser Lauf tut

Zieht `tools/sim/welt.py` und `tools/sim/szenario.py` auf `tools.autor.Autor` um — die letzte der
fünf Kettenfortführungen. Dazu zwei veraltete Docstrings aus Lauf A.

**Reine Refaktorierung.** Kein Claim ändert sich um ein Byte, kein `erwarte`-Block in einem
Szenario bewegt sich. Jede Abweichung ist ein **Befund** und kein Anlass, eine Erwartung
anzupassen.

## 1. `Teilnehmer` trennt Rückhalt und Autor

`Teilnehmer` ist heute beides in einem: es führt `h_prev` als Hexdatei **und** signiert. Nach dem
Umzug hält es einen `Autor` über

- `DateiRueckhalt(self.path)` — Dateien `spitze` und `redo` im Teilnehmerverzeichnis,
- einen `Ausgang`, der die Inbox ist.

Der Ausgang ist bereits vorhanden, nur nicht so benannt: `hat_claim(cid)` **ist** `kennt`, und
`claim_einlegen(claim)` **ist** `aufnehmen`. Es genügt ein kleiner Adapter (oder `Teilnehmer`
erfüllt das Protokoll direkt) — baue keinen zweiten Weg, der Dateien anlegt.

`wiederaufnehmen()` wird einmal in `Teilnehmer.anlegen` gerufen, nach der Konstruktion des
`Autor`.

**Das Verzeichnislayout ändert sich, und das ist in Ordnung.** Die Datei `h_prev` entfällt; im
Zustand `GENESIS` schreibt `Autor` nichts, `spitze` entsteht mit dem ersten Claim. `Welt.anlegen`
räumt bei jedem Lauf per `rmtree` auf, es gibt also keinen Altbestand. Geprüft: `h_prev`,
`read_h_prev` und `write_h_prev` kommen außerhalb von `welt.py` nirgends vor — beide Methoden
entfallen ersatzlos.

**Unverändert bleiben:** `read_now` / `write_now` (die Uhr des Beobachters ist keine Sache der
Kette), `store_laden`, `inbox_path`, `Welt.zustellen`. Insbesondere darf `zustellen` **nicht**
über `Ausgang.aufnehmen` laufen: es kopiert rohe Bytes ohne zu dekodieren, und Zustellung ist
keine Autorschaft.

**Prüfe, ob das Feld `seed` auf `Teilnehmer` noch gelesen wird.** Wenn nicht, entfällt es; der Seed
liegt ohnehin in `key.bin`. Wird es gelesen, ist das eine Rückfrage — die Oberflächenregel aus
D122 gilt für `Autor`, und ob sie sich auf einen Simulationsteilnehmer fortsetzt, ist nicht
entschieden.

## 2. Das Flag verschwindet aus der Python-Oberfläche

`Teilnehmer` bekommt **zwei** benannte Operationen statt eines Bool-Arguments (D129):

```
claim_signieren(*, p, J, t, v=None, N=None, t_exp=None)   ->  autor.signieren(...)
claim_gabeln(*, p, J, t, v=None, N=None, t_exp=None)      ->  autor.gabeln(...)
```

Der Parameter `kette_fortschreiben` verschwindet aus beiden Signaturen.

`szenario.py:_schritt_claim` liest das Feld weiter aus dem Szenario und verzweigt:

```
kette_fortschreiben = bool(step.get("kette_fortschreiben", True))
...
if kette_fortschreiben:
    claim = autor.claim_signieren(p=p, J=J, t=t, v=v, N=scope, t_exp=t_exp)
else:
    claim = autor.claim_gabeln(p=p, J=J, t=t, v=v, N=scope, t_exp=t_exp)
```

**Das Szenario-Schema bleibt unangetastet.** `tools/sim/scenarios/*.json` und `sim-abnahme.md`
werden **nicht** geändert. Die Grenze liegt zwischen Datei und Aufrufkonvention: ein
Szenarioautor, der `false` schreibt, hat es getippt; ein Programmierer, der ein Argument wegläßt,
hätte es nicht (D129).

## 3. Zwei Docstrings aus Lauf A

- `tests/property/welten.py`, `_Signer`: „``kette_fortschreiben=False`` hält ``h_prev``" trifft
  nicht mehr zu — es ruft `gabeln`. Neu formulieren, `fuzz-prompt.md §7` als Verweis behalten.
- `tools/example_nucleus.py`, `_Author`: der Satz über den Beginn von `h_prev` beschreibt nicht
  mehr, was diese Klasse tut. Neu formulieren.

Zwei Zeilen, keine Logik.

## 4. Abnahmekriterien

Abgeleitet, nicht aufgezählt:

```
grep -rn "_h_prev\|build_signed\|id_genesis_anchor" tools/ tests/
grep -rn "kette_fortschreiben" tools/ tests/
```

Der erste Befehl darf nur noch `tools/autor.py` treffen. Der zweite nur noch `szenario.py` — die
eine Zeile, die das Szenariofeld liest — und die Szenariodateien selbst.

Dazu:

- `make check-all` grün: **474** Tests und **11** Eigenschaftstests, beide Zahlen unverändert.
  Dieser Lauf fügt keine Tests hinzu; `tests/test_sim.py` fährt die Szenarien S1–S6 samt ihrer
  `erwarte`-Blöcke, und das ist die eigentliche Prüfung.
- `git diff main --stat` zeigt genau vier Dateien: `tools/sim/welt.py`, `tools/sim/szenario.py`,
  `tests/property/welten.py`, `tools/example_nucleus.py`. Eine fünfte — insbesondere eine
  `scenarios/*.json` — ist ein Befund.
- Ein Weltverzeichnis nach einem S5-Lauf enthält `spitze`, kein `h_prev`, und keinen offenen
  `redo`.

## 5. Was nicht Teil dieses Laufs ist

- Jede Änderung an `mensch_als_republik/`, `tools/autor.py`, `tests/helpers.py`,
  `tests/test_autor.py`.
- Jede Änderung an `scenarios/*.json` oder an einer Spec-Datei.
- `store_laden` liest fremde Bytes mit `claim_from_bytes`, das nach D121 dafür untauglich ist.
  Bekannt, offen, **nicht** hier zu reparieren.
- **B-4**, die Zwillingsbuchführung in `welten()`.

## 6. Rückfragen

An den Spec-Supervisor. Insbesondere:

- wenn ein `erwarte`-Block sich bewegt,
- wenn `Teilnehmer.seed` doch gelesen wird,
- wenn sich `Teilnehmer` nicht als `Ausgang` einsetzen lässt, ohne `Autor` zu erweitern,
- wenn der Wegfall von `h_prev` im Verzeichnis irgendwo auffällt.

## 7. Abschluss

```
make check-all
git add tools/sim/welt.py tools/sim/szenario.py tests/property/welten.py tools/example_nucleus.py
git commit
```

`git add` nach `make check-all`: alle vier Dateien sind bereits versioniert.
