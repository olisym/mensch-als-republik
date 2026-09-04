# Prompt `00w-zeilenlaenge` — Die Prosagrenze prüfbar machen (D222)

## 0. Rahmen

Branch `impl/00w`, abgezweigt von `main`. Basis ist der **Branchpunkt** — der Commit, der diese
Datei und die Berichtigung an D222 trägt; `git merge-base main HEAD` nennt ihn. Ein Commit am
Ende, **kein Merge, kein Push**.

Geändert werden `tools/check_specs.py` und elf `.md`-Dateien im Wurzelverzeichnis.

## 1. Normative Grundlage

- **D222** entscheidet: Prosa höchstens 100 Zeichen, Tabellenzeilen und Zeilen in Codeblöcken
  ausgenommen, Register und Sitzungsstart mitgeprüft. Für Python gilt keine Grenze.
- **D205** hat die Grenze für Python verneint. Daran ändert dieser Lauf nichts.

Bei einem Widerspruch zwischen diesem Prompt und D222 gilt D222, und der Widerspruch wird
gemeldet.

## 2. Auftrag

### (a) Eine neue Prüffunktion in `tools/check_specs.py`

Sie nimmt den Text einer Datei und liefert Befunde in der Form der übrigen Prüfungen — eine
Zeichenkette je Fund, mit Zeilennummer und gemessener Länge.

Gezählt werden **Zeichen**, mit `len()` über den dekodierten Text. Nicht Bytes: bei Umlauten
weicht das ab, und genau daran ist in einer früheren Sitzung eine Zählung gescheitert.

Zwei Klassen sind ausgenommen. Für beide gilt: führende Leerzeichen und führende
Blockzitat-Zeichen samt folgenden Leerzeichen werden vor der Prüfung abgezogen, sonst greift die
Klassifikation bei eingerückten Listen und in Blockzitaten daneben.

1. **Tabellenzeile** — der so bereinigte Anfang ist ein senkrechter Strich.
2. **Codeblock** — eine bereinigte Zeile, die mit drei Backticks beginnt, schaltet den Zustand um
   und ist selbst ausgenommen; alles dazwischen ebenso. Der Zustand gilt je Datei und beginnt
   ausserhalb.

### (b) Einbindung für **alle** Spec-Dateien

Die Prüfung läuft über dieselbe Dateimenge wie die übrigen `.md`-Prüfungen. Die bestehende
Ausnahme für `07-decisions.md` und `sitzungsstart-*.md` gilt **nur** für die Verweisprüfung und
wird hier **nicht** angewandt — D222 begründet das: Zeilenlänge ist keine Aussage über Inhalt.

### (c) Einundzwanzig Zeilen umbrechen

Verteilung, auf dem Branchpunkt gemessen:

| Datei | Zeilen |
|---|---|
| `01-claim-atom.md` | 4 |
| `06-services.md` | 3 |
| `00-nucleus-genesis-constitution.md` | 2 |
| `02-golden-anchors.md` | 2 |
| `04-governance.md` | 2 |
| `example-nucleus.md` | 2 |
| `werkzeuge.md` | 2 |
| `02-trust-flow.md` | 1 |
| `07-decisions.md` | 1 |
| `authoring-nachlauf-prompt.md` | 1 |
| `genesis-bindung-prompt.md` | 1 |

Für jede gilt: **nur umbrechen, nichts umformulieren.** Kein Wort wird hinzugefügt, entfernt oder
ersetzt, keine Abkürzung eingeführt, keine Klammer gestrichen. Der Umbruch erfolgt an einem
vorhandenen Leerzeichen. Die Folgezeile führt das Präfix ihres Blocks fort — bei einem
eingerückten Listenpunkt dessen Einzug, in einem Blockzitat dessen Zitatzeichen.

Die längste Zeile hat 522 Zeichen und steht im Register; sie braucht mehr als einen Umbruch.

Die Zahlen sind gemessen. Weicht eine ab: **melden, nicht suchen und still anpassen.**

## 3. Ausdrückliche Nicht-Ziele

- **Keine Grenze für Python.** D205 hat das verneint; `ruff` führt sie bewusst nicht.
- **Kein Formatierer.** Es wird keine Funktion gebaut, die Zeilen selbsttätig umbricht. Die
  einundzwanzig Umbrüche sind Handarbeit, weil jeder von ihnen eine Stelle wählt.
- **Tabellenzeilen bleiben, wie sie sind.** Auch die 244, die über 100 Zeichen liegen. Sie sind
  ausgenommen, nicht geduldet.
- **Codeblöcke bleiben, wie sie sind.**
- **Keine Änderung** an `check_escapes`, `check_control_chars`, `check_decisions`,
  `check_references`, `check_section_refs`, `layer_headings`, `heading_covers`, `python_sources`
  oder an `tools/check_tree.py`.
- **Keine Tests unter `tests/`.**
- **Keine Ausnahmeliste** für einzelne Dateien.

## 4. Abnahmekriterien

1. `make check-specs` grün, `make check` grün, **597** Tests, `ruff` grün.
2. **Abgeleitet, nicht abgeschrieben:** eine Zählung über alle `.md` im Wurzelverzeichnis, mit
   Python `len()` und derselben Klassifikation wie die Prüfung, ergibt **null** Prosazeilen über
   100 Zeichen. Nicht mit `awk length` — das zählt Bytes.
3. `git diff --numstat` gegen den Branchpunkt weist je Datei genau so viele **Löschungen** aus,
   wie die Tabelle in (c) Zeilen nennt. Einfügungen sind mehr als Löschungen. Mehr Löschungen als
   genannt heisst, dass eine Zeile umgeschrieben statt umbrochen wurde.
4. **Kein Wort ist verändert.** Zu belegen mit `git diff --word-diff` über die elf `.md`-Dateien:
   die Ausgabe darf keine hinzugefügte oder entfernte Wortgruppe zeigen. Fällt der Beleg anders
   aus als hier beschrieben, wird die tatsächliche Ausgabe berichtet.

## 5. Rücknahmeproben

Zwei Eingriffe an der Prüfung, ein Eingriff am Bestand, zwei Proben.

**P1 — trägt (a), (b) und (c) zusammen.** Die einundzwanzig Umbrüche zurücknehmen, sonst nichts,
`make check-specs` laufen lassen. Erwartung: **rot**, mit **21** Befunden in **11** Dateien, in
der Verteilung aus der Tabelle in (c). Darunter einer in `07-decisions.md` — das belegt zugleich,
dass die Ausnahme aus (b) nicht angewandt wurde. Danach die Umbrüche wieder einsetzen und die
Rückkehr nach grün zeigen.

**P2 — trägt die Klassifikation in drei Richtungen.** In `distanzkauf-prompt.md` vorübergehend
vier Zeilen anfügen: eine Prosazeile mit 101 Zeichen, eine Tabellenzeile mit 101 Zeichen, und
einen vollständigen Codeblock aus öffnender Zeile, einer Zeile mit 101 Zeichen und schliessender
Zeile. `make check-specs` laufen lassen. Erwartung: **rot** mit **genau einem** Befund in dieser
Datei, nämlich über die Prosazeile. Die Tabellenzeile und die Zeile im Codeblock dürfen **keinen**
Befund erzeugen. Danach alle Zeilen entfernen und mit `git diff --quiet distanzkauf-prompt.md`
belegen, dass nichts zurückbleibt.

Beide Proben werden mit ihrer **wörtlichen Ausgabe** berichtet.

**Ohne eigene Probe bleibt** die Zählweise in Zeichen statt Bytes. Sie ist Abnahmekriterium 2 und
wird dort direkt abgelesen; eine rote Probe dafür bräuchte eine Zeile, die in Bytes über und in
Zeichen unter der Grenze liegt, und die einzurichten hiesse, den Bestand für die Probe zu
verbiegen.

## 6. Abschluss

Ein Commit auf `impl/00w`. Kein Merge, kein Push, kein Rebase.

Zurückgemeldet werden: der Commit-Hash, `git diff --numstat` gegen den Branchpunkt, die letzten
zwei Zeilen von `make check-specs`, die Testzahl, die abgeleitete Zählung aus Kriterium 2, der
Beleg aus Kriterium 4 und die wörtlichen Ausgaben beider Proben.

## 7. Rückfragen

Rückfragen gehen an den Supervisor, nicht in den Code. Was hier nicht steht, wird gemeldet und
nicht gebaut.
