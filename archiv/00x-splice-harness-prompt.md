# Prompt `00x-splice-harness` — Ein Aufruf statt neun Zeilen (D225)

## 0. Rahmen

Branch `impl/00x`, abgezweigt von `main`. Basis ist der **Branchpunkt** — der Commit, der D225
und diese Datei trägt; `git merge-base main HEAD` nennt ihn. Ein Commit am Ende, **kein Merge,
kein Push**.

Neu entsteht genau eine Datei: `tools/splice_run.py`. Keine bestehende Datei wird geändert.

## 1. Normative Grundlage

- **D225** entscheidet den Harness und seine Bauform: Lauf im Arbeitsverzeichnis, kein
  Temp-Verzeichnis, Git als Rollback.
- **D222** gibt die Längenregel, die er prüft: Prosa höchstens 100 Zeichen, Tabellenzeilen und
  Zeilen in Codeblöcken ausgenommen.
- **Prüfregel 42** gibt den Zeitpunkt der Prüfung: am Ergebnis, nicht am eingesetzten Text.

Bei einem Widerspruch zwischen diesem Prompt und D225 gilt D225, und der Widerspruch wird
gemeldet.

## 2. Auftrag

`tools/splice_run.py` nimmt einen Pfad zu einem Splice-Skript und führt sechs Schritte aus. Bricht
einer ab, wird **zurückgesetzt** und mit Rückgabewert 1 beendet.

1. **Sauberer Baum.** `git status --porcelain` muss leer sein. Ist er es nicht, bricht der Harness
   ab, **bevor** er irgendetwas ausführt, und ändert nichts.
2. **Erster Lauf.** Das Skript wird mit demselben Interpreter gestartet, mit dem der Harness
   läuft, und im Wurzelverzeichnis des Repositories. Seine Ausgabe wird durchgereicht. Ein
   Rückgabewert ungleich 0 ist ein Abbruch.
3. **Zweiter Lauf.** Derselbe Aufruf noch einmal. Er **muss** scheitern — ein Splice, der zweimal
   durchläuft, hat keinen wirksamen Anker. Läuft er durch, ist die Datei doppelt verändert; dann
   ist der Rücksetzpfad besonders wichtig. Die Ausgabe des zweiten Laufs wird gekürzt gezeigt, es
   genügt die letzte Zeile.
4. **Was sich geändert hat.** `git diff --numstat` wird ausgegeben. Ändert der Splice **keine**
   Datei, ist das ein Abbruch: ein Splice, der nichts tut, hat seinen Anker verfehlt, ohne es zu
   merken.
5. **Zeilenlänge am Ergebnis.** Für jede geänderte `.md`-Datei wird die Zahl der zu langen
   Prosazeilen im Arbeitsstand mit der im Basisstand verglichen — `git show HEAD:<pfad>` liefert
   den Basisstand. Ist sie **grösser** geworden, ist das ein Abbruch, und die neuen Fundstellen
   werden mit Zeilennummer und Länge genannt. Gleich oder kleiner ist in Ordnung: der Altbestand
   trägt Zeilen über 100, und die sollen den Harness nicht bei jedem Lauf blockieren.
6. **Bericht.** Bei Erfolg eine knappe Zusammenfassung: geänderte Dateien, Zeilen hinzu und
   entfernt, und dass der zweite Lauf gescheitert ist. Der Harness **committet nicht** und
   **pusht nicht**.

**Rücksetzen** heisst `git checkout --` auf genau die Pfade, die `git diff --name-only` nennt.
Nicht `git checkout .`, nicht `git reset --hard` — ein Splice, der eine unversionierte Datei
anlegt, darf nicht dazu führen, dass fremde Arbeit verschwindet. Nach dem Rücksetzen wird
gemeldet, was zurückgenommen wurde.

Die Klassifikation der Zeilen ist dieselbe wie in `check_specs.py`: führende Leerzeichen und
führende Blockzitat-Zeichen abziehen, dann Tabellenzeile am senkrechten Strich und Codeblock an
drei Backticks erkennen. **Die Funktion wird importiert, nicht abgeschrieben** — zwei Fassungen
derselben Klassifikation laufen auseinander, und genau diesen Defekt soll der Harness fangen.
Ist `check_line_length` dafür nicht in der passenden Form, wird das **gemeldet**, nicht durch
eine Kopie gelöst.

## 3. Ausdrückliche Nicht-Ziele

- **Kein Temp-Verzeichnis, kein Trockenlauf gegen eine Kopie.** D225 hat das verworfen.
- **Kein Commit, kein Push, kein `git add`.** Der Harness verändert die Historie nicht.
- **Keine Änderung an `tools/check_specs.py`.** Wird dort etwas gebraucht, das nicht importierbar
  ist, ist das eine Meldung an den Supervisor.
- **Keine Änderung** an `tools/check_tree.py`, `tools/register_index.py`, am `Makefile` oder an
  einer `.md`-Datei.
- **Kein Ziel `make`.** Der Harness wird direkt aufgerufen; ein `make`-Ziel hätte einen eigenen
  Namen zu entscheiden und ist nicht Gegenstand.
- **Keine Tests unter `tests/`.** Für `tools/` gibt es keine.
- **Keine Prüfung der Splice-Skripte selbst**, etwa auf Modulkonstanten oder Namensform.

## 4. Abnahmekriterien

1. `make check` grün, **597** Tests, `ruff` grün. Die neue Datei muss `ruff` mit den geltenden
   Gruppen bestehen.
2. Der Harness läuft gegen einen Splice, der sauber durchgeht, und meldet Erfolg. Als Material
   dient ein Wegwerf-Splice **in `/tmp`**, nicht im Repository; er wird nach dem Lauf gelöscht.
3. `git diff --numstat` gegen den Branchpunkt weist genau eine neue Datei aus,
   `tools/splice_run.py`.

## 5. Rücknahmeproben

Drei Fehlerpfade, drei Proben. Alle mit Wegwerf-Splices in `/tmp`, alle mit anschliessend
sauberem Baum.

**P1 — der zweite Lauf geht durch.** Ein Splice, der an eine Datei etwas anhängt, ohne einen
Anker zu prüfen, läuft zweimal. Erwartung: der Harness meldet den Fehlschlag, setzt zurück, und
`git status --porcelain` ist danach **leer**. Der doppelte Anhang darf nicht liegenbleiben.

**P2 — eine zu lange Prosazeile entsteht.** Ein Splice, der eine Zeile mit 101 Zeichen anhängt
und einen Anker prüft. Erwartung: der Harness meldet die Fundstelle mit Zeilennummer und Länge,
setzt zurück, Baum sauber.

**P3 — der Baum ist vorher schmutzig.** Eine beliebige versionierte Datei ändern, dann den
Harness starten. Erwartung: Abbruch **vor** dem ersten Lauf, und die vorhandene Änderung ist
**unangetastet** — der Harness darf fremde Arbeit nicht wegräumen. Danach die Änderung von Hand
zurücknehmen.

Alle drei werden mit ihrer **wörtlichen Ausgabe** berichtet.

**Ohne eigene Probe bleibt** der Abbruch bei null geänderten Dateien aus Schritt 4. Er ist mit P1
und P2 nicht zu verwechseln und wäre eine vierte Probe für einen Pfad, der dieselbe
Rücksetzlogik nutzt wie P2; sie brächte keine neue Aussage.

## 6. Abschluss

Ein Commit auf `impl/00x`. Kein Merge, kein Push, kein Rebase.

Zurückgemeldet werden: der Commit-Hash, `git diff --numstat` gegen den Branchpunkt, **der
vollständige `git diff` gegen den Branchpunkt**, die Testzahl, und die wörtlichen Ausgaben der
drei Proben.

## 7. Rückfragen

Rückfragen gehen an den Supervisor, nicht in den Code. Was hier nicht steht, wird gemeldet und
nicht gebaut.
