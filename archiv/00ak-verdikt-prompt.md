# 00ak — Zeilenschnittstelle und Saatkorpus

## Branch und Basis

Branch `00ak-verdikt`, Basis ist der Register-Commit auf diesem Branch (D293 bis D295). Ein Commit
am Ende, kein Merge.

## Normative Grundlage

- **D293** — Korpusbauer und Verdiktläufer liegen im Repo, der Vergleich außerhalb. Der Korpus
  liest die committete Vektordatei. Die Hex-Konventionen der Go-Fassung werden gespiegelt.
- **D295** — die Vektordatei wird an ihren Generator gebunden.
- **D269** — die Hexzeilen sind Transport in den Harness, keine Wire-Form und keine Norm.
- `01 §B.2` — die Namen der zwölf Reject-Codes. `01 §6` — die strukturelle Prüfung.

## Auftrag

### 1. `tools/korpus.py`, neu

Ein Modul mit einer Funktion `seed_lines`, die eine Liste von Paaren aus Name und Drahtbytes in
Hex liefert, in der Reihenfolge der Vektordatei `tests/vectors/vectors_01.json`. Je Eintrag sind
die Drahtbytes das Feld `wire_bytes`, wenn es vorhanden ist, sonst das Feld `signed_bytes`. Fehlen
beide, ist das ein Fehler und kein stilles Überspringen.

Dazu ein `main`: ohne Argument werden die Hexzeilen ausgegeben, mit dem Argument `--manifest` die
Namen, je eine Zeile. Beide Ausgaben haben damit gleich viele Zeilen und lassen sich
nebeneinanderlegen.

Der Pfad zur Vektordatei wird aus dem Ort des Moduls abgeleitet, nicht aus dem Arbeitsverzeichnis.

### 2. `tools/verdikt.py`, neu

Die Zeilenschnittstelle des Verifizierers. Drei Funktionen und ein `main`.

**Erstens** eine Funktion, die eine rohe Zeile in Bytes verwandelt und `None` liefert, wenn die
Zeile keine Bytefolge bezeichnet. Sie kürzt die Zeile **am Ende** um Wagenrücklauf, Zeilenumbruch,
Tabulator und Leerzeichen; innen bleibt die Zeile unverändert. Danach gilt: ungerade Länge ergibt
`None`; ein Zeichen, das keine Hexziffer ist, ergibt `None`. Groß- und Kleinbuchstaben sind beide
zulässige Hexziffern. Die Prüfung auf Hexziffern ist ausdrücklich nötig und darf nicht der
Standardbibliothek überlassen werden: `bytes.fromhex` nimmt Innen-Whitespace an, die Go-Fassung
nicht.

**Zweitens** eine Funktion, die aus einer rohen Zeile die Verdiktzeile macht. Liefert die erste
Funktion `None`, ist das Verdikt eine Ablehnung mit `MALFORMED_CBOR`. Sonst entscheidet
`read_claim` aus `mensch_als_republik.verifier`, ohne Speicher. Ein Reject-Code ergibt das Wort
`reject`, ein Leerzeichen und den Namen des Codes. Ein Claim ergibt das Wort `ok`, ein Leerzeichen
und die `claim_id` in Hex in Kleinschreibung.

**Drittens** eine Funktion, die einen Eingabestrom Zeile für Zeile liest und je Eingabezeile genau
eine Verdiktzeile schreibt. `main` verbindet sie mit der Standardein- und -ausgabe.

### 3. `tests/test_verdikt.py`, neu

Die Erwartung je Vektor wird **aus der Vektordatei abgeleitet**, nicht getippt: trägt ein Eintrag
das Feld `expect_reject`, ist die Erwartung eine Ablehnung mit diesem Code, sonst eine Annahme mit
dem Feld `claim_id`.

- Die Namen des Saatkorpus gleichen den Namen der Vektordatei, in der Reihenfolge.
- Je Vektor: die Verdiktzeile gleicht der abgeleiteten Erwartung.
- Dieselbe Zeile in Großbuchstaben ergibt dasselbe Verdikt.
- Diese Zeilen bezeichnen keine Bytefolge und ergeben je eine Ablehnung mit `MALFORMED_CBOR`: die
  leere Zeile; eine Zeile aus drei Leerzeichen; die beiden Zeichen a und 1; eine Hexfolge aus
  sieben Zeichen; die beiden Zeichen z und z; eine achtstellige Hexfolge mit zwei eingestreuten
  Leerzeichen, deren Gesamtlänge gerade ist; eine achtstellige Hexfolge mit drei eingestreuten
  Leerzeichen, deren Gesamtlänge ungerade ist. Die letzten beiden Fälle trennen das Längentor vom
  Hexziffern-Tor; ohne beide prüft nur eines von ihnen.
- Eine Zeile mit angehängtem Zeilenumbruch ergibt dasselbe Verdikt wie ohne. Eine Zeile mit
  angehängtem Leerzeichen und Tabulator ebenfalls.

### 4. Der Bindungstest in `tests/test_vectors_01.py`

Eine einzige neue Testfunktion, die die geladene Vektordatei vollständig mit dem Ergebnis von
`build_vectors()` vergleicht. Die beiden vorhandenen Fixtures werden genutzt, keine neuen gebaut.
Nichts anderes in dieser Datei wird angefasst.

## Nicht-Ziele

- **Kein Mutationsgitter.** Die Mutationsmenge bleibt in diesem Lauf leer; der Korpus ist Anhang C.
  Das Gitter aus D289 ist der nächste Lauf.
- **Kein Aufruf der Go-Fassung** und kein Verweis auf sie in einer Datei des Repos.
- Keine Änderung an `mensch_als_republik/verifier.py`, `errors.py`, `atom.py`, an
  `tests/vectors/gen.py` oder an `tests/vectors/vectors_01.json`.
- Keine Änderung an einer Spec- oder Prompt-Datei.
- Keine Änderung an vorhandenen Tests außer der einen neuen Funktion aus Punkt 4.
- Kein `__init__.py` in `tools`. Die Testkonfiguration legt das Wurzelverzeichnis bereits auf den
  Suchpfad.
- Keine neue Abhängigkeit.

## Abnahmekriterien

1. `make check` grün.
2. Die Zeilenzahl der Hexausgabe gleicht der Zeilenzahl der Manifestausgabe und gleicht der Zahl
   der Einträge in der Vektordatei. Abgeleitet, nicht getippt.
3. Fünf Rücknahmeproben an `tools/verdikt.py`, jede einzeln und jede danach zurückgenommen. Melde
   je Probe die Zahl der roten Tests; jede muss mindestens einen roten Test erzeugen.
   - das Tor auf ungerade Länge entfernt
   - das Tor auf Hexziffern entfernt
   - das Kürzen am Zeilenende auf Wagenrücklauf und Zeilenumbruch verkürzt
   - die Großbuchstaben aus der Menge der zulässigen Hexziffern entfernt
   - die `claim_id` in Großschreibung ausgegeben
4. Drei Rücknahmeproben am Bindungstest, jede in `tests/vectors/vectors_01.json` und jede danach
   zurückgenommen: ein geänderter Vektorname, eine geänderte Erwartung, eine geänderte `claim_id`.
   Jede muss den Bindungstest allein rot machen. Am Ende muss `git diff --quiet` auf diese Datei
   durchgehen.
5. Widerspricht eine Messung diesem Prompt, wird sie **gemeldet, nicht angepasst**. Keine
   Erwartung wird nachgezogen, damit ein Test grün wird.

## Abschluss

Ein Commit auf `00ak-verdikt`. Danach der **vollständige** `git diff` gegen den Branchpunkt, nicht
nur `--numstat`, zusammen mit den acht Probenergebnissen aus Punkt 3 und 4.
