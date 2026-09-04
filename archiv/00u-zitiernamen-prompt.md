# Prompt `00u-zitiernamen` — Buchstabennamen in der Verweisprüfung binden (D219)

## 0. Rahmen

Branch `impl/00u`, abgezweigt von `main`. Basis ist der **Branchpunkt** — der Commit, der D219
und diese Datei trägt; `git merge-base main HEAD` nennt ihn. Ein Commit am Ende, **kein Merge,
kein Push**.

Geändert wird genau eine Datei: `tools/check_specs.py`. Keine andere Datei des Repositories wird
angefasst, auch nicht vorübergehend, ausser für die Rücknahmeprobe P2, die ihre Änderung selbst
wieder zurücknimmt.

## 1. Normative Grundlage

- **D209** hat die Zitierkonvention als nicht injektiv benannt und `LAYER_FILES` angelegt.
- **D215** hat die Verweisprüfung auf Python ausgedehnt.
- **D219** entscheidet Teil A: welche Datei jeder Buchstabenname bezeichnet, und was mit einem
  Namen geschieht, der in der Tabelle fehlt. D219 ist die Grundlage dieses Laufs; bei einem
  Widerspruch zwischen diesem Prompt und D219 gilt D219, und der Widerspruch wird gemeldet.

Heute erfasst `SECTION_REF` nur Verweise mit reinem Ziffernpräfix. Verweise wie der auf Abschnitt
2.6 der Datei `02a-maxflow-prompt.md` trifft die Regex nicht und fallen still durch.

## 2. Auftrag

Drei Eingriffe in `tools/check_specs.py`.

### (a) Vier Einträge in `LAYER_FILES`

| Schlüssel | Datei |
|---|---|
| `01a` | `01a-policy-prompt.md` |
| `02a` | `02a-maxflow-prompt.md` |
| `02b` | `02b-golden-anchors.md` |
| `04a` | `04a-korrektur-prompt.md` |

Der bestehende Kommentar über der Tabelle wird um einen Satz ergänzt: die gleichnamigen
Abnahme-Dateien sind **nicht** die Ziele, weil sie keine nummerierten Überschriften führen und
damit unter der geltenden Konvention kein Zitierziel sein können (D219). Reihenfolge der
Einträge: die Ziffernschlüssel bleiben, wo sie sind, die vier neuen kommen danach.

### (b) Optionaler Kleinbuchstabe in `SECTION_REF`

Die Regex erfasst zusätzlich einen einzelnen Kleinbuchstaben zwischen Ziffernpaar und Leerzeichen.
Die bestehende Zusicherung bleibt: kein Treffer, wenn unmittelbar davor ein Buchstabe oder eine
Ziffer steht. Nichts anderes an der Regex ändern.

### (c) Ein Präfix ohne Tabelleneintrag ist ein Befund

`check_section_refs` greift heute mit `headings[prefix]` zu. Nach (b) kann ein Präfix auftreten,
das die Tabelle nicht kennt — dann darf **kein `KeyError`** fliegen und der Verweis darf **nicht
still übersprungen** werden. Er wird als eigener Befund gemeldet, mit eigenem Text, der ihn vom
unbekannten Abschnitt unterscheidet, und mit der Zählung wie dort. Sinngemäss:

```
unbekannter Zitiername: 02c (3x)
```

Ein Name wird je Datei einmal gemeldet, nicht je Verweis. Die Meldung des unbekannten Abschnitts
bleibt im Wortlaut unverändert.

Die Wirkung muss auch über `check_python_section_refs` eintreten. Wenn das ohne weiteren Eingriff
folgt, weil dieselbe Funktion gerufen wird, ist das der richtige Weg — keine zweite Fassung der
Logik anlegen.

## 3. Ausdrückliche Nicht-Ziele

- **Keine Datei umbenennen.** Die Abnahme-Dateien behalten ihre Namen (D219).
- **Die präfixlosen Verweise bleiben unangetastet.** 185 der 260 Paragraphenverweise in Python
  tragen kein Präfix. Sie sind Teil B und ausdrücklich nicht Gegenstand dieses Laufs. Keine
  Zuordnung Verzeichnis auf Schicht, kein Vorgriff, keine vorbereitende Struktur dafür.
- **Keine Tests unter `tests/`.** Für `tools/` gibt es heute keine Tests. Ob das so bleibt, ist
  eine offene Frage und wird hier nicht beantwortet. Wer beim Arbeiten einen Grund sieht, meldet
  ihn, baut ihn nicht.
- **Keine Änderung** an `check_escapes`, `check_control_chars`, `check_decisions`,
  `check_references`, `heading_covers`, `layer_headings`, `python_sources` oder an
  `tools/check_tree.py`.
- **Keine Zeilenlängenregel für Python.** D205 hat das mit Zahlen verneint; `ruff` führt sie
  bewusst nicht.
- **Das Ausgabeformat der bestehenden Zeilen bleibt.** Nur die eine neue Befundzeile kommt hinzu.

## 4. Abnahmekriterien

Alle Zahlen unten sind auf dem Branchpunkt gemessen, nicht geschätzt. Widerspricht eine Messung
diesem Prompt: **melden, nicht anpassen.**

1. `make check-specs` läuft grün. Die letzte Zeile vor der Schlusszeile lautet danach
   `ok  Python-Dateien   ...   120 Dateien, 75 Verweise`. Vorher steht dort `60 Verweise`. Die
   Dateizahl bleibt 120.
2. `make check` grün, **597** Tests.
3. Die Zahl der Verweise mit Buchstabenpräfix in `.md` und `.py` zusammen ist **31**, verteilt auf
   **15** Dateien, mit **vier** Namen: 24 mal `02a`, 3 mal `01a`, 2 mal `02b`, 2 mal `04a`. Diese
   Zahl wird **abgeleitet** — per Grep über den Baum, nicht aus diesem Prompt abgeschrieben — und
   sie darf sich durch den Lauf **nicht ändern**. Ändert sie sich, ist eine Zeile eingefügt
   worden, die es nicht sollte.
4. `ruff` bleibt grün.

## 5. Rücknahmeproben

Drei Eingriffe, zwei Proben. Der Grund steht dabei; eine dritte Probe wird **nicht** erfunden.

**P1 — trägt (a) und (c), und mittelbar (b).** Den Eintrag `02a` aus `LAYER_FILES` entfernen,
sonst nichts ändern, `make check-specs` laufen lassen. Erwartung: **rot**, mit dem neuen Befund
über den unbekannten Zitiernamen, in mehreren Dateien. Kein `KeyError`, kein Absturz. Danach den
Eintrag wieder einsetzen und die Rückkehr nach grün zeigen. Diese Probe deckt (b) mit ab: ohne
den optionalen Buchstaben in der Regex bliebe das Entfernen wirkungslos und der Lauf grün.

**P2 — trägt (b) in der Sache.** In `budget-set-prompt.md` einen der beiden vorhandenen
`02a`-Verweise vorübergehend auf einen Abschnitt zeigen lassen, den `02a-maxflow-prompt.md` nicht
führt (etwa 99). `make check-specs` laufen lassen. Erwartung: **rot**, mit dem Befund über den
unbekannten Abschnitt, genau einmal, in genau dieser Datei. Danach die Zeile **wortgleich**
zurücksetzen und mit `git diff --quiet budget-set-prompt.md` belegen, dass die Datei unverändert
ist.

Beide Proben werden mit ihrer **wörtlichen Ausgabe** berichtet, nicht als Zusammenfassung.

**Ohne eigene Probe bleibt:** dass die Meldung je Datei einmal statt je Verweis erscheint. Das ist
eine Formeigenschaft der Ausgabe und fällt in P1 auf, wenn sie verletzt ist; eine eigene Probe
dafür wäre eine erfundene.

## 6. Abschluss

Ein Commit auf `impl/00u`. Kein Merge, kein Push, kein Rebase.

Zurückgemeldet werden: der Commit-Hash, `git diff --numstat` gegen den Branchpunkt, die Ausgabe
von `make check-specs` in den letzten drei Zeilen, die Testzahl, und die wörtlichen Ausgaben
beider Proben.

## 7. Rückfragen

Rückfragen gehen an den Supervisor, nicht in den Code. Was hier nicht steht, wird gemeldet und
nicht gebaut.
