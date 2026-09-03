# Prompt 00an — Szenario Absicherung, Stufe A

## Modus

Das hier ist ein **Prototyp** nach D311 Beschluss 1. Der Code ist Wegwerfcode. Es gibt keine
Golden Numbers, keine Rücknahmeproben, keine Zweitimplementierung, keine Abnahme gegen erwartete
Zahlen. Was zählt, sind die **Befunde**: jede Stelle, an der die Spec keine Antwort hat, eine
falsche gibt, oder eine erzwingt, die ein Zentrum voraussetzt.

Erfinde nichts still. Stösst du auf eine Stelle, an der du eine Entscheidung treffen musst, die
weder die Spec noch dieser Prompt hergibt: **triff sie, markiere sie im Bericht als Befund, und
begründe, warum keine andere Wahl blieb.** Genau diese Liste ist das Ergebnis des Laufs.

## Branch und Basis

Branch `00an-szenario-a`, abgezweigt vom Kopf von `main` — dem Commit, der diesen Prompt und D311
einführt. Lies ihn zu Beginn ab und nenne ihn im Bericht. Ein Commit am Ende, kein Merge.

## Normative Grundlage

`07-decisions.md`, Eintrag **D311** — er trägt den Modus, den Zuschnitt und drei Befunde, die
bereits vor dem Bauen gemessen wurden. Dazu `03 §3.3.2` für Obligation und Quittung, `03 §2.4`
für die Bindungskraft eines Verdikts, `04 §2` für Vorschlag und Auszählung, `02 §8` für das
Budget. Lies D311 vor Beginn.

## Was gebaut wird

Ein Skript `tools/szenario_absicherung.py` nach der Bauform von `tools/example_nucleus.py`: erst
die Welt bauen, dann `check_*`-Funktionen, die sie befragen, dann eine `main`, die alles fährt und
eine Tabelle ausgibt. Aufruf als Modul.

Vier Beteiligte mit eigenen Verzeichnissen unter einem Basispfad, der als Argument übergeben wird
und per Voreinstellung unter `/tmp` liegt. Jeder Beteiligte bekommt einen `Autor` mit
`DateiRueckhalt` auf sein eigenes Verzeichnis.

Dazu die beiden fehlenden Teile aus D311 Befund 3, **im Skript, nicht in `mensch_als_republik/`**:
ein Ausgang, der jeden ausgesendeten Claim als Datei ablegt, und ein Leser, der ein Verzeichnis in
einen `InMemoryStore` lädt. Der Dateiname eines Claims ist seine `claim_id` in Hex.

Die Verteilung von Claims zwischen den vier ist ein ausdrücklicher Schritt im Skript, kein
Nebeneffekt: eine Funktion, die eine Menge von Claims in die Verzeichnisse anderer Beteiligter
kopiert. Wer was weiss, muss jederzeit ablesbar sein.

## Der Durchlauf

**Aufbau.** Ein Nukleus mit vier Beteiligten, Verfassung mit `obligation@1` unter den
unwiderruflichen Prädikaten und Schwellen für die drei Klassen. Genesis, Scope, Epoche 1, alle
vier akzeptieren die Regeln.

**Phase 1 — Fonds mit Verwahrer.** Einer der vier wird Verwahrer. Über drei Perioden signiert
jeder der anderen drei je eine `obligation` an ihn; er quittiert jede mit `receipt`. Dann tritt
bei einem der Beteiligten der Fall ein. Er meldet ihn. Es wird entschieden, ob ausgezahlt wird
(siehe unten). Bei Annahme signiert der Verwahrer eine `obligation` an den Betroffenen, der
quittiert.

Danach dieselbe Phase ein zweites Mal, aber der Verwahrer quittiert nicht und zahlt nicht aus.
Bestimme mit `settlement`, was das Protokoll darüber aussagt, und halte fest, was es **nicht**
aussagt.

**Phase 2 — Umlage ohne Verwahrer.** Kein Verwahrer, keine laufenden Beiträge. Der Fall tritt ein,
und jeder der anderen drei signiert eine `obligation` direkt an den Betroffenen; er quittiert.
Einer der drei quittiert nie beziehungsweise leistet nicht — bestimme auch hier den Zustand.

**Die Entscheidung über die Auszahlung.** D311 Befund 2 stellt fest, dass `04` nur Abstimmungen
über Verfassungen kennt. Wähle einen der Wege, fahre ihn, und melde den anderen als verworfen mit
Begründung: entweder die Auszahlung als Verfassungsänderung mit eigener Epoche, oder gar keine
kollektive Entscheidung, sondern nur die Beobachtung, wer sich verpflichtet hat. Wenn beide Wege
scheitern, ist **das** der Befund, und dann wird nichts erfunden, um die Phase zu retten.

## Die Prüfungen

Nach jeder Phase, für jeden der vier Beteiligten getrennt aus seinem eigenen Verzeichnis heraus:

- Der Tilgungszustand jeder Obligation nach `settlement`.
- Wer die offenen Obligationen sind und wem gegenüber.
- Ob alle vier zum selben Ergebnis kommen. Wenn nicht: welcher Claim fehlt bei wem, und ob das
  eine Frage der Verteilung ist oder des Protokolls.

Zusätzlich, einmal am Ende: läuft dieselbe Welt aus frisch gelesenen Verzeichnissen ein zweites
Mal mit demselben Ergebnis durch?

## Nicht-Ziele

- Keine Änderung an `mensch_als_republik/`, an einer Layer-Datei, an `07-decisions.md` oder
  `pruefregeln.md`.
- Keine Schlichtung, kein `submit-arbitration`, kein `verdict`. Das ist Stufe C.
- Kein Netz, kein Server, keine Oberfläche.
- Kein Trust-Flow und kein Budget in diesem Lauf, auch wenn `02 §8` als Deckungsmechanismus
  naheliegt. Erst muss die Verpflichtungsschicht stehen.
- Keine neuen Tests in `tests/`. Das Skript prüft sich selbst über seine `check_*`-Funktionen.
- Kein Merge, kein Push nach `main`.

## Abschluss

Ein Commit auf `00an-szenario-a`. `git add` mit expliziten Pfaden.

Melde:

1. Die Ausgabe des Skripts, gekürzt auf das Lesbare.
2. **Die Befundliste** — jede Stelle, an der du etwas entscheiden musstest, das die Spec nicht
   hergibt, mit der Wahl und ihrer Begründung. Das ist der wichtigste Teil des Berichts.
3. Den vollständigen `git diff` gegen den Branchpunkt.

Wenn der Durchlauf an einer Stelle nicht weitergeht, ist der Abbruch mit einer benannten Ursache
das bessere Ergebnis als ein Durchlauf, der über die Stelle hinweggeht.
