# Prompt: Nachlauf zu den Rücknahmeproben — N11 und N14 mit geschlossener Trägermenge

## Branch und Basis

Weiter auf `00ab-mussproben`, Basis ist `c9ada0e`. Ein Commit am Ende, kein Merge, kein Push.

## Normative Grundlage

D245 in `07-decisions.md`: eine Rücknahmeprobe misst die Stelle, nicht die Pflicht, solange die
Träger redundant sind. Die Messung aus `00ab-mussproben-befund.md` hat für N11 und N14 je einen
von mehreren Trägern neutralisiert; beide Ergebnisse sind damit unbestimmt.

## Auftrag

Zwei Proben, nacheinander, dazwischen ein sauberer Baum.

**N14 — es wird geworfen, nicht vermerkt.** Die Trägermenge ist zuerst zu bestimmen: alle Stellen
im Produktivcode, die den Genesis-Hash gegen `scope` vergleichen und bei Abweichung werfen. Der
Befund nennt vier, das ist zu bestätigen und nicht zu übernehmen. Anschließend werden **alle**
zugleich neutralisiert, ein Lauf `.venv/bin/python -m pytest -q`, dann alles zurückgenommen.

**N11 — dieses `N` ist der ausgewertete Scope.** Ebenso: die vollständige Menge der Stellen
bestimmen, die ein `N` gegen den ausgewerteten Scope prüfen, alle zugleich neutralisieren, ein
Lauf, zurücknehmen. Die Argumentprüfung in derselben Funktion, die der Befund als zweiten Träger
nennt, gehört dazu.

Das Ergebnis wird als neuer Abschnitt **an `00ab-mussproben-befund.md` angehängt**, nicht in eine
neue Datei und nicht in den bestehenden Text hinein. Je Pflicht: die vollständige Trägerliste mit
Datei und Funktion, die Zahl der rot gewordenen Tests, bis zu drei Testnamen, und die Klasse
geprüft oder ungeprüft nach D245.

Weicht die gefundene Trägermenge von der im bisherigen Befund genannten ab, wird die Abweichung
benannt. Sie ist ein Ergebnis, kein Fehler.

## Nicht-Ziele

- Keine Tests schreiben, ändern oder ergänzen.
- Keine Stelle zusammenlegen, keine Redundanz auflösen, keinen Produktivcode dauerhaft ändern.
- Keine Spec-Datei anfassen, keinen Registereintrag schreiben.
- Die zwölf übrigen Pflichten werden nicht erneut geprobt.
- Der bestehende Text in `00ab-mussproben-befund.md` wird nicht berichtigt, auch nicht dort, wo
  der Nachlauf ihm widerspricht. Der Widerspruch gehört in den neuen Abschnitt.

## Abnahmekriterien

- Der `git diff` gegen `c9ada0e` enthält genau eine Datei, `00ab-mussproben-befund.md`, und darin
  nur Einfügungen am Ende.
- `make check-all` ist grün. Grundlinie: 597 Tests plus 14 Eigenschaftstests.
- Für N14 und N11 steht je eine vollständige Trägerliste und ein gemessenes Ergebnis.
- Prosa bricht bei 100 Zeichen; Tabellenzeilen und Codeblöcke sind ausgenommen. Keine Escapes.

## Rückfragen

Wenn die Trägermenge nicht abschließend zu bestimmen ist, oder wenn eine geschlossene
Neutralisierung den Lauf aus einem anderen Grund rot macht als der geprüften Pflicht: melden,
nicht raten.

## Abschluss

Ein Commit auf `00ab-mussproben`. Der Bericht enthält den vollständigen `git diff` gegen
`c9ada0e`.
