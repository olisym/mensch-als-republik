# Prompt: Rücknahmeproben für die vierzehn markierten Pflichten

## Branch und Basis

Branch `00ab-mussproben`, abgezweigt vom Commit, der diesen Prompt einführt. Ein Commit am Ende,
kein Merge, kein Push nach `main`.

## Normative Grundlage

D242 in `07-decisions.md` nennt die Menge der vierzehn Pflichten mit ihrem Ort und begründet das
Verfahren. D243 nennt die Grenze der Aussage. Beide sind vor diesem Prompt geschrieben und gelten
unverändert; die Tabelle wird hier absichtlich nicht wiederholt, damit sie nicht driften kann.

## Auftrag

Für jede der vierzehn Pflichten N01 bis N14 aus der Tabelle in D242, einzeln und nacheinander:

1. Die Stelle im Produktivcode finden, die die Pflicht durchsetzt.
2. Genau diese eine Stelle so neutralisieren, dass die Pflicht nicht mehr greift — die Bedingung
   dauerhaft falsch setzen, die Prüfung überspringen, den Vergleich immer wahr machen. Nichts
   sonst anfassen.
3. `.venv/bin/python -m pytest -q` laufen lassen und die Namen der fehlgeschlagenen Tests notieren.
4. Die Neutralisierung zurücknehmen und mit `git diff --quiet` bestätigen, dass der Baum wieder
   sauber ist, bevor die nächste Pflicht drankommt.

Das Ergebnis kommt in eine neue Datei `00ab-mussproben-befund.md`, je Pflicht mit: der Kennung,
der Datei und Funktion der durchsetzenden Stelle, der Zahl der rot gewordenen Tests, bis zu drei
Testnamen im Klartext, und einer der drei Klassen **geprüft**, **ungeprüft** oder **ohne Träger**.

**ungeprüft** heißt: die Stelle war zu finden und zu neutralisieren, der Lauf blieb grün.
**ohne Träger** heißt: es gibt keine Stelle, die die Pflicht durchsetzt.

## Nicht-Ziele

- Keine Tests schreiben, ändern oder ergänzen. Auch dort nicht, wo eine Lücke sichtbar wird.
- Keine Pflicht reparieren. Keine dauerhafte Änderung an Produktivcode.
- Keine Spec-Datei anfassen, keinen Registereintrag schreiben.
- Nicht nach weiteren normativen Aussagen suchen. Die Menge ist mit D242 geschlossen.
- Keine Neutralisierung, die zwei Pflichten zugleich aufhebt. Trägt eine Stelle mehrere, wird das
  gemeldet statt zusammengefasst.
- Keine Sammelläufe. Zwischen zwei Proben ist der Baum sauber.

## Abnahmekriterien

- Der `git diff` gegen den Branchpunkt enthält genau eine Datei, die neue
  `00ab-mussproben-befund.md`. Kein Produktivcode, kein Test, keine Spec-Datei ist geändert.
- `make check-all` ist grün. Grundlinie: 597 Tests plus 14 Eigenschaftstests.
- Die Befunddatei nennt für jede der vierzehn Pflichten entweder mindestens einen namentlich
  genannten fehlgeschlagenen Test oder ausdrücklich, dass der Lauf grün blieb.
- Die Zahl der roten Tests ist gemessen, nicht geschätzt, und stammt aus der Ausgabe des Laufs.
- Prosa bricht bei 100 Zeichen; Tabellenzeilen und Codeblöcke sind ausgenommen. Keine Escapes.

## Rückfragen

Wenn eine Pflicht keine durchsetzende Stelle hat, wenn die Neutralisierung mehrdeutig ist, oder
wenn eine Stelle sich nicht neutralisieren lässt, ohne den Lauf aus einem anderen Grund rot zu
machen: melden, nicht raten. Solche Fälle sind Kandidaten für Spec-Lücken und gehören ins
Register, nicht in den Code.

## Abschluss

Ein Commit auf `00ab-mussproben`. Der Bericht enthält den vollständigen `git diff` gegen den
Branchpunkt, nicht nur `--numstat`.
