# Prompt 00ao — Archiv und Bindungsregel für das Wurzelverzeichnis

## Branch und Basis

Branch `00ao-archiv`, abgezweigt vom Kopf von `main` — dem Commit, der diesen Prompt und D314
einführt. Lies ihn zu Beginn ab und nenne ihn im Bericht. Ein Commit am Ende, kein Merge.

## Normative Grundlage

`07-decisions.md`, Eintrag **D314** mit vier Beschlüssen. Dazu D225 für die zurückgenommene Sorge
um die Kopiengrösse und D229 für den Umfang der Verweisprüfung. Lies D314 vor Beginn.

## Auftrag 1 — die Bindungsregel in `tools/check_specs.py`

Eine Markdown-Datei im Wurzelverzeichnis heisst **gebunden**, wenn mindestens eines gilt:

- Sie steht in `LAYER_FILES`.
- Sie ist eine von: das Regelwerk, `README.md`, `VISION.md`, `werkzeuge.md`,
  `example-nucleus.md`, die Ankerdatei zu `02`, die Ankerdatei zu `03`, die aktuelle
  Übergabedatei. Diese Menge steht als benannte Konstante im Modul, mit einem Satz, warum jeder
  Eintrag darin steht.
- Eine andere Markdown-Datei **im Wurzelverzeichnis** oder eine Python-Datei nennt sie in der Form
  eines Abschnittsverweises, also mit Dateinamen oder Kurzform gefolgt von einem Paragraphenzeichen
  und einer Abschnittsnummer. Der vorhandene Ausdruck für Abschnittsverweise wird dafür
  wiederverwendet, nicht nachgebaut. Dateien unterhalb von `archiv/` zählen dabei **nicht** als
  Quelle.

Eine blosse Nennung des Dateinamens ohne Abschnitt bindet nicht.

## Auftrag 2 — die Meldung

`check_specs` gibt am Ende seines Laufs zwei Zahlen aus: wie viele Wurzeldateien gebunden sind und
wie viele nicht. Die ungebundenen werden namentlich genannt, alphabetisch.

**Die Prüfung schlägt nicht fehl.** Ungebundene Dateien sind eine Meldung, kein Befund. Der
Rückgabewert des Werkzeugs bleibt von dieser Meldung unberührt.

## Auftrag 3 — das Verschieben

Alle ungebundenen Markdown-Dateien des Wurzelverzeichnisses wandern per `git mv` nach `archiv/`.
Kein Löschen, keine Umbenennung, keine Unterordner innerhalb von `archiv/`.

Die Liste wird **abgeleitet**, nicht getippt: aus derselben Funktion, die Auftrag 1 baut. Führe
sie zuerst gegen den unveränderten Baum und melde das Ergebnis, bevor du verschiebst.

Nach dem Verschieben läuft `check_specs` erneut und meldet null ungebundene Dateien.

## Nicht-Ziele

- Keine Änderung an `07-decisions.md`, `pruefregeln.md` oder einer Layer-Datei.
- Kein Aufteilen, Kürzen oder Zusammenfassen des Registers.
- Keine Änderung am Inhalt einer verschobenen Datei, auch nicht an ihren Verweisen.
- Kein Verschieben von Dateien ausserhalb des Wurzelverzeichnisses; `tools/`, `tests/`,
  `mensch_als_republik/` und ihre Unterverzeichnisse bleiben unberührt.
- Keine neue Prüfung, die fehlschlägt. Siehe Auftrag 2.
- Kein rekursives Globben in `check_specs` für die Spec-Prüfung selbst — die geprüfte Menge bleibt
  die Wurzel.
- Kein Merge, kein Push nach `main`.

## Abnahmekriterien

1. `make check` ist grün. Die Testzahl wird gemeldet.
2. Gemeldet werden, aus einem Aufruf abgelesen: die Zahl der gebundenen und der ungebundenen
   Wurzeldateien **vor** dem Verschieben, und beide Zahlen **danach**.
3. Die Zahl der Dateien unter `archiv/` und die Zahl der Markdown-Dateien in der Wurzel nach dem
   Lauf.
4. `git status` zeigt ausschliesslich Umbenennungen und die Änderung an `tools/check_specs.py` —
   keine Löschung, keine unverfolgte Datei.

## Abschluss

Ein Commit auf `00ao-archiv`. `git add` mit expliziten Pfaden.

Melde den `git diff --stat` gegen den Branchpunkt **und** den vollständigen `git diff` für
`tools/check_specs.py`. Für die verschobenen Dateien genügt die Umbenennungsliste; ihr Inhalt ist
unverändert und muss nicht im Bericht erscheinen.
