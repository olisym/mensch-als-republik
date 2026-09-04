# 00ad — Zweitimplementierung Layer 01 in Go

## Auftrag

Baue in Go einen Verifizierer für das Claim-Atom, das in `spec/01-claim-atom.md` beschrieben ist.

Die Spec ist die einzige Quelle. Es gibt keine Referenzimplementierung zum Nachsehen und keine
weiteren Dateien.

## Umfang

Gebaut wird die **zustandslose** Prüfung: aus den Bytes eines einzelnen Claims wird ein Ausgang
bestimmt. Kein Speicher, keine Kenntnis anderer Claims, keine Vorgängerauflösung, keine
Zustandsmaschine über mehrere Claims. Alles, was Weltwissen braucht, bleibt draußen.

## Schnittstelle

Ein ausführbares Programm. Es liest von der Standardeingabe eine Zeile je Claim, jede Zeile die
Bytes des Claims in Hex. Es schreibt je Eingabezeile genau eine Ausgabezeile:

- bei Annahme: das Wort ok, ein Leerzeichen, die Claim-Kennung in Hex
- bei Ablehnung: das Wort reject, ein Leerzeichen, der Name der Fehlerklasse

Die Namen der Fehlerklassen werden der Spec entnommen, in der dort gedruckten Schreibweise.

## Vorgaben

- Die deterministische CBOR-Kodierung wird selbst geschrieben. Keine CBOR-Bibliothek.
- Die Signaturprüfung kommt aus der Standardbibliothek. Sie wird nicht selbst gebaut.
- Sonst keine Abhängigkeiten außer der Standardbibliothek.
- Eigene Tests sind erwünscht.

## Der Anhang mit den Vektoren ist unvollständig

Er enthält einen vollständig gerechneten Vektor. Weitere sind absichtlich zurückgehalten und
werden nicht nachgereicht. Aus dem Fehlen eines Vektors folgt nichts: eine Bedingung der Spec ist
nicht deshalb unwichtig, weil kein Beispiel dazu abgedruckt ist.

## Was mitzuliefern ist: die Fragenliste

Neben dem Code entsteht eine Datei `FRAGEN.md`. Darin steht jede Stelle, an der die Spec
mehrdeutig, unvollständig oder widersprüchlich war und eine Entscheidung nötig wurde. Je
Eintrag:

- der Abschnitt der Spec
- die Frage, die der Text offenlässt
- die Lesart, für die entschieden wurde
- die verworfene Lesart, und warum sie verworfen wurde

Diese Datei ist nicht Beiwerk, sondern das wichtigste Ergebnis dieser Arbeit. Eine Stelle, an der
geraten wurde, ohne dass sie hier steht, ist verloren. Lieber ein Eintrag zu viel.

Es wird nicht zurückgefragt und nicht auf eine Antwort gewartet. Es wird entschieden, gebaut und
der Eintrag geschrieben.

## Nicht-Ziele

- Keine Zustandsmaschine, kein Speicher, keine Verkettung über mehrere Claims.
- Keine Netzwerk-, Datei- oder Zeitzugriffe im Verifizierer.
- Kein Zugriff auf Verzeichnisse außerhalb dieses Arbeitsverzeichnisses.
- Keine Vollständigkeitsannahme über den Vektoranhang.

## Abschluss

Ein Commit in diesem Verzeichnis. Kein Merge. Der Bericht nennt: die gebauten Dateien, die Zahl
der eigenen Tests, und die Zahl der Einträge in `FRAGEN.md`.
