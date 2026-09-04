# 00r — Registerindex und Verweisprüfung

## 1. Branch und Basis

Branch `00r` vom Commit, der diese Datei enthält. Ein Commit, kein Merge, kein Push.

## 2. Normative Grundlage

`07-decisions.md` D209. Der Eintrag entscheidet beide Werkzeuge, ihre Einschränkungen und die
benannten Grenzen. `pruefregeln.md` Regel 38 nennt `tools/register_index.py` beim Namen; der
Aufruf muss deshalb so heissen.

## 3. Auftrag

Drei Teile. Der dritte ist eine Berichtigung und muss **vor** dem zweiten sitzen, sonst ist
`make check` rot.

### Teil A — `tools/register_index.py`

Ein Abfragewerkzeug, keine generierte Datei. Nimmt einen Abschnittsnamen als Argument und gibt die
Registereinträge aus, die ihn nennen.

    python3 tools/register_index.py "04 §4.1"
    04 §4.1   D106 D107 D174 D193 D194 D201 D207 D209

Gemessen am Prompt-Commit ist genau diese Zeile das Ergebnis für `04 §4.1`; für `03 §2.4` sind es
`D67 D78 D114`. Beide Mengen sind aus dem Register abzuleiten, nicht als Testkonstante zu tippen.

- Zerlegt `07-decisions.md` an Zeilen der Form `### D<zahl>` und sammelt je Eintrag die Verweise
  der Form `<praefix> §<abschnitt>`. Ein Verweis zählt je Eintrag einmal, auch wenn er mehrfach
  vorkommt; die Ausgabe hält die Registerreihenfolge.
- Ohne Argument: eine Übersicht, welche Abschnitte wie oft entschieden wurden, absteigend.
- Kein Argument-Parsing über `argparse` nötig, aber ein unbekannter Abschnitt gibt eine leere
  Trefferzeile und Rückgabewert 0 — nicht 1. Eine Abfrage ohne Treffer ist kein Fehler.
- Das Werkzeug liest nur; es schreibt keine Datei und verändert nichts.

### Teil B — `check_specs.py` prüft Abschnittsverweise

Eine neue Prüfung neben den bestehenden, mit den Einschränkungen aus D209:

- Geprüft werden **nur** Verweise mit reinem Ziffernpräfix, `00` bis `08`, gegen die zugehörige
  Layer-Datei. Die Zuordnung Präfix zu Datei steht als explizite Tabelle im Code, nicht über einen
  Glob — die Präfixe sind nicht eindeutig, `03` und `04` bezeichnen je vier Dateien.
- **Ausgenommen sind `07-decisions.md` und `sitzungsstart-*.md`.** Beide beschreiben vergangene
  Stände; ein Verweis auf einen inzwischen umgebauten Abschnitt ist dort richtig.
- Ein Verweis gilt als getroffen, wenn eine Überschrift der Ebene 2 bis 4 in der Zieldatei mit
  genau dieser Nummer beginnt, oder wenn eine Überschrift existiert, deren Nummer mit der
  gesuchten plus einem Punkt beginnt — `02 §3` ist auch dann getroffen, wenn es nur `3.1` gibt.
- Befunde werden wie die übrigen gemeldet: Datei, Verweis, Anzahl. Rückgabewert 1.

Gemessen am Prompt-Commit liegen über alle Dateien **704** solche Verweise; nach der Ausnahme
für Register und Sitzungsstart bleiben **238**, und darin genau **ein** Befund, der in Teil C
behoben wird. Die Zahlen sind im Lauf nachzumessen und bei Abweichung zu melden.

### Teil C — Berichtigung in `welten-prompt.md`

Die Datei verweist auf einen Unterabschnitt 6.7 von `01 §6`. Der Abschnitt ist nicht
untergliedert; gemeint ist
Listenpunkt 7 darin, „falls `t` und `t_exp` vorhanden: `t < t_exp`". Der Verweis wird zu `01 §6`,
der Satz bleibt sonst unverändert und behält seine Aussage.

## 4. Ausdrücklich nicht in diesem Schritt

- **Keine Tabelle für Buchstabenpräfixe.** `01a`, `02a`, `04a` und die übrigen bleiben ungeprüft.
  Wer sie prüfen will, braucht zuerst eine Entscheidung, welche Datei welchen Zitiernamen führt;
  die gibt es nicht.
- **Keine generierte Indexdatei im Baum.** D209 hat das mit Grund verworfen.
- **Keine Zeilenlängenprüfung.** Die 100-Zeichen-Konvention bleibt ungeprüft; das ist ein eigener
  Fork und nicht Teil dieses Laufs.
- **Kein Nachziehen der zwei Registerverweise** auf die Abschnitte 5.1 und 11 in `03`. Sie sind
  von der Prüfung ausgenommen und bleiben, wie sie stehen.
- Kein Anfassen der bestehenden Prüfungen in `check_specs.py`, kein Umbau ihrer Ausgabe.
- Keine weiteren Funde beheben, auch wenn die neue Prüfung welche zeigt. Melden.

## 5. Abnahmekriterien

- `make check` grün. `check_specs.py` meldet nach Teil C **null** Verweisbefunde.
- Testzahl bleibt **589**, sofern für die Werkzeuge keine Tests entstehen; entstehen welche, ist
  die neue Zahl zu nennen und zu begründen.
- `ruff check` ohne Fund, auch in `tools/`.
- `git diff --numstat` zeigt `tools/register_index.py` (neu), `tools/check_specs.py` und
  `welten-prompt.md`. Neue Datei vor `make check` mit explizitem Pfad adden, nie `-A`.
- `python3 tools/register_index.py "04 §4.1"` gibt die acht oben genannten D-Nummern aus.

## 6. Zwei Rücknahmeproben

**Probe A.** Die Berichtigung aus Teil C zurücknehmen, also den Unterabschnitt 6.7 wieder
einsetzen.
Erwartet: `make check` **rot** mit genau einem Verweisbefund in `welten-prompt.md`. Bleibt es grün,
greift die Prüfung nicht und das ist ein Befund.

**Probe B.** In einer Prompt-Datei einen erfundenen Verweis auf den Abschnitt 99 in `02`
einfügen — nicht im Register, sonst greift die Ausnahme. Erwartet: `make check` rot
mit diesem Befund. Danach zurücknehmen.

Zwei Änderungen, zwei Proben. Probe A prüft, dass die Prüfung den echten Fund sieht; Probe B, dass
sie nicht nur diesen einen Fall kennt.

## 7. Abschluss

Ein Commit auf `00r`. Zurück kommen: Commit-Hash, `git diff --numstat`, Testzahl, die Ausgabe von
`register_index.py` für `04 §4.1` und `03 §2.4`, die gemessene Zahl geprüfter Verweise, und je
Probe das Ergebnis. Weicht eine Messung ab, wird sie gemeldet und nicht angeglichen.
