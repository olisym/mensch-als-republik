# 00aj — Nachzug der Go-Fassung auf den laufenden Spec-Stand

## Auftrag

In `~/mar-go` liegt ein Verifizierer für das Claim-Atom, gebaut gegen eine frühere Fassung von
`spec/01-claim-atom.md`. Die Spec-Datei in `spec/` ist gegen den heutigen Stand ausgetauscht
worden. Lies sie neu und bringe die Fassung mit ihr in Übereinstimmung.

Die Spec ist die einzige Quelle. Es gibt keine Referenzimplementierung zum Nachsehen, keine Liste
der Änderungen und keine weiteren Dateien.

## Wie gelesen wird

Der Text wird **ganz** gelesen, nicht diffweise. Welche Stellen sich geändert haben, wird nicht
mitgeteilt, und es wird auch nicht ermittelt: ein Vergleich mit der alten Fassung führte dazu, dass
nur die markierten Stellen geprüft werden. Gesucht ist, was der heutige Text verlangt, nicht was an
ihm neu ist.

Wo der Text etwas anderes verlangt, als die Fassung tut, wird die Fassung geändert. Wo er dasselbe
verlangt, bleibt sie unangetastet.

## Umfang und Schnittstelle

Unverändert. Zustandslose Prüfung, ein Ausgang je Bytefolge, kein Speicher, keine Kenntnis anderer
Claims. Die Schnittstelle bleibt die des ursprünglichen Auftrags: eine Hex-Zeile je Claim auf der
Standardeingabe, je Eingabezeile genau eine Ausgabezeile, `ok` mit Kennung oder `reject` mit dem
Namen der Fehlerklasse in der in der Spec gedruckten Schreibweise.

Die deterministische CBOR-Kodierung bleibt selbst geschrieben. Die Signaturprüfung bleibt aus der
Standardbibliothek. Sonst keine Abhängigkeiten außer der Standardbibliothek.

## Der Vektoranhang ist Messpunkt, nicht Vorlage

Der Anhang der Spec trägt jetzt mehr Vektoren als beim ersten Auftrag. Sie werden **nach** dem
Nachzug gefahren, nicht währenddessen, und ihr Ergebnis wird berichtet.

Ein Vektor, der nicht durchgeht, wird nicht dadurch repariert, dass sein erwarteter Code in die
Fassung geschrieben wird. Er wird repariert, indem der Abschnitt der Spec, den er belegt, noch
einmal gelesen wird — oder er wird als Befund gemeldet und bleibt rot. Ein rot gebliebener Vektor
mit einer benannten Begründung ist ein besseres Ergebnis als ein grüner, der aus der Erwartung
zurückgerechnet wurde.

## Was mitzuliefern ist: die Fragenliste

`FRAGEN.md` wird fortgeschrieben, nicht ersetzt. Neue Einträge für jede Stelle, an der der heutige
Text mehrdeutig, unvollständig oder widersprüchlich war und eine Entscheidung nötig wurde. Je
Eintrag: der Abschnitt, die Frage, die der Text offenlässt, die gewählte Lesart, die verworfene
Lesart und warum.

Bestehende Einträge, die der heutige Text beantwortet, werden **nicht gelöscht**. Sie bekommen eine
Zeile dahinter: dass der Text sie jetzt entscheidet, und an welcher Stelle. Ein Eintrag, dessen
Frage der Text weiterhin offenlässt, bleibt stehen, wie er ist.

Diese Datei ist das wichtigste Ergebnis dieser Arbeit. Es wird nicht zurückgefragt und nicht auf
eine Antwort gewartet. Es wird entschieden, gebaut und der Eintrag geschrieben.

## Nicht-Ziele

- Keine Zustandsmaschine, kein Speicher, keine Verkettung über mehrere Claims.
- Keine Netzwerk-, Datei- oder Zeitzugriffe im Verifizierer.
- Kein Zugriff auf Verzeichnisse außerhalb dieses Arbeitsverzeichnisses.
- Keine Änderung der Schnittstelle.
- Kein Vergleich der neuen Spec-Datei mit der alten.

## Abschluss

Ein Commit in diesem Verzeichnis, kein Merge. Der Bericht nennt: den Basis-Commit, gegen den
gearbeitet wurde, die geänderten Dateien, die Zahl der eigenen Tests, das Ergebnis jedes Vektors
aus dem Anhang, die Zahl der neuen Einträge in `FRAGEN.md` und die Zahl der als beantwortet
markierten alten. Dazu der vollständige Diff gegen den Basis-Commit.
