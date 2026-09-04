# Prompt 00aq — Bindungsmuster und zwei Werkzeuge

## Branch und Basis

Branch `00aq-werkzeuge`, Basis-Commit `b5eabe1` auf `main`. Ein Commit am Ende, **kein Merge**.

## Normative Grundlage

- **D314** — die Bindungsregel für das Wurzelverzeichnis und die Meldung ohne Fehlschlag.
- **D316** — `offen.md` mit nummerierten Posten, fortgeschrieben statt neu geschrieben; Nummern
  werden nie wiederverwendet.
- **D209** — `tools/register_index.py` als Vorbild: gerechnet statt gepflegt, benannte Grenze.
- **Prüfregel 64** — eine Regel, die eine Menge ausdünnt, wird auf ihren zweiten Lauf geprüft.

## Auftrag 1 — `ALWAYS_BOUND` wird ein Muster

In `tools/check_specs.py` nennt `ALWAYS_BOUND` die Übergabedatei beim Namen. Der Eintrag lautet
auf eine Datei, die inzwischen im Archiv liegt. Da die Menge mit `root_md` geschnitten wird,
verschwindet der tote Eintrag stumm, und die aktuelle Übergabedatei wird als ungebunden gemeldet.

Zu tun:

1. Den namentlichen Eintrag für die Übergabedatei entfernen.
2. `arbeitsweise.md` und `offen.md` in `ALWAYS_BOUND` aufnehmen, jeweils mit einem
   Kommentar in der Form der vorhandenen Einträge. Beide sind Einstiegsdateien nach D316 und
   werden von niemandem mit Abschnitt zitiert.
3. Die **jüngste** Übergabedatei der Wurzel zur Laufzeit ermitteln und binden. Kandidaten sind
   alle Dateien der Wurzel, deren Name mit `sitzungsstart-` beginnt und auf `.md` endet.

**Die Auswahlregel, in Prosa.** Verglichen wird der Namensteil zwischen `sitzungsstart-` und
`.md`. Es gewinnt der **längere** Teil; bei gleicher Länge der alphabetisch spätere. Rein
alphabetisch zu sortieren wäre falsch: das Schema ist von einstelligen auf zweistellige Suffixe
übergegangen, und `00z` läge damit hinter `00aa`, obwohl es älter ist.

Gibt es keine Kandidatendatei, wird nichts gebunden und nichts gemeldet. Das ist kein Fehler.

Die Auswahl gehört in eine eigene, benannte Funktion mit Docstring, nicht in eine Zeile
innerhalb von `bound_root_files`. `ALWAYS_BOUND` bleibt eine Konstante; die dynamische Datei
kommt an der Stelle hinzu, an der die Menge heute mit `root_md` geschnitten wird.

## Auftrag 2 — `tools/offen.py`

Ein Prüfer für `offen.md`, im Aufbau und Ton von `tools/register_index.py`.

**Kopfzeilen.** Ein Posten beginnt mit einer Zeile aus drei Rauten, einem Leerzeichen, dem
Grossbuchstaben O und einer Ziffernfolge. Danach folgt Text derselben Zeile; er wird nicht
geprüft.

**Prüfungen:**

1. Die Nummern beginnen bei eins und sind lückenlos aufsteigend.
2. Keine Nummer kommt zweimal vor.
3. Jede Nummer, die in `07-decisions.md` oder in `offen.md` selbst in der Form Grossbuchstabe O
   unmittelbar gefolgt von einer Ziffernfolge genannt wird, hat einen Posten. Eine Nennung ohne
   Posten ist ein Befund; ein Posten ohne Nennung ist keiner.

**Ausgabe.** Bei Erfolg eine Zeile mit der Anzahl der Posten. Bei einem Befund je Problem eine
Zeile und Status 1. Kein eigener Trennstrich als Ersatz für eine Messung.

**Benannte Grenze.** Der Prüfer sichert, dass eine genannte Nummer **existiert**, nicht dass der
Posten die Nennung trägt. Das ist dieselbe Grenze wie bei den Abschnittsverweisen (D229) und
gehört in den Docstring.

**Make.** Ein neues Ziel `check-offen`, aufgenommen in `check` und in `check-all`. Es läuft nach
`check-specs`.

**Tests.** In `tests/` eine Datei mit Tests gegen erzeugten Text, nicht gegen `offen.md`. Die
erwarteten Werte werden aus dem erzeugten Text abgeleitet, nicht getippt.

## Auftrag 3 — `tools/stand.py`

Gibt die Kaltzahlen einer Sitzung als **eine** Zeile aus, geeignet als Kopftext der Projektkopie.

**Ein Argument:** der Pfad zu einer gespeicherten Ausgabe eines Testlaufs. Daraus wird die Zahl
gelesen, die unmittelbar vor dem Wort passed steht; gibt es sie nicht, endet das Werkzeug mit
Status 1 und ohne Ausgabezeile. Die Testzahl wird **nie** selbst erzeugt und **nie** geschätzt.

**Selbst gezählt werden:** Registerköpfe in `07-decisions.md`, Prüfregeln in `pruefregeln.md`,
Posten in `offen.md`, Markdown-Dateien der Wurzel. Die Zählvorschriften stehen in
`arbeitsweise.md`; sie sind zu übernehmen, nicht neu zu erfinden.

**Der Commit-Kurzhash** kommt aus einem Aufruf von git. Schlägt der fehl, endet das Werkzeug mit
Status 1.

**Kein Netzwerkzugriff, kein Schreiben in den Baum.**

## Nicht-Ziele

- Kein Umbau von `SPECS`, `LAYER_FILES` oder der Ausdrücke für Überschriften und Verweise.
- **Keine Änderung an der Ausnahme** für `07-decisions.md` und die Übergabedateien (D209).
- Keine neue Prüfklasse in `check_specs.py`, keine Änderung an der Meldung ohne Fehlschlag.
- Keine Archivierung, keine Umbenennung, keine Änderung an `offen.md` oder `arbeitsweise.md`.
- Keine Tests für `tools/stand.py`, die git aufrufen müssten.
- Kein Merge, kein Push.

## Abnahmekriterien

1. `make check` läuft grün durch.
2. Die Bindungsmeldung nennt weder `arbeitsweise.md` noch `offen.md` noch die aktuelle
   Übergabedatei. Welche Dateien sie noch nennt, wird gemeldet, nicht bewertet.
3. **Zweiter Lauf** von `check_specs.py` liefert dieselbe gebundene Menge wie der erste
   (Prüfregel 64). Beide Läufe werden gefahren und die Zahlen gegeneinander gehalten.
4. `tools/offen.py` meldet die Anzahl der Posten und läuft ohne Befund.
5. **Zwei Rücknahmeproben für Auftrag 2**, jede einzeln: eine Nummer aus der Mitte der Liste in
   einer Arbeitskopie entfernen, der Prüfer muss die Lücke melden; in einer Arbeitskopie eine
   Nummer nennen, für die es keinen Posten gibt, der Prüfer muss das melden. Die Arbeitskopien
   werden **nicht** committet; gemeldet wird, dass beide Proben rot waren.
6. `tools/stand.py` gegen eine gespeicherte Testausgabe liefert eine Zeile; gegen eine Datei ohne
   die Zahl liefert es Status 1 und keine Zeile.

## Abschluss

Ein Commit auf `00aq-werkzeuge`. Der Bericht enthält den **vollständigen** `git diff` gegen
`b5eabe1`, nicht nur die Zusammenfassung, sowie die Ausgaben zu den Punkten 2 bis 6.

Widerspricht eine Messung diesem Prompt, wird sie **gemeldet, nicht angepasst**. Was hier nicht
steht, wird gemeldet, nicht gebaut.
