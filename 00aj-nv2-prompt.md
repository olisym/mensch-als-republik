# 00aj — NV2 wird gerechnet statt abgeschrieben

## Branch und Basis

Branch `00aj-nv2`, Basis ist der Splice-Commit mit D291 und D292 auf diesem Branch. Ein Commit am
Ende, kein Merge.

## Normative Grundlage

- **D291** — NV2 ist die vollständige signierte TV1-Map einschließlich `σ`, unsortiert kodiert.
- `01 §C.7` in der neuen Fassung, `01 §3` Regel 4, `01 §B.2` Vorrang.

## Auftrag

### 1. NV2 in `tests/vectors/gen.py`

Die handkopierte Hex-Konstante für NV2 entfällt. An ihre Stelle tritt eine Berechnung aus der
bereits im Modul vorhandenen signierten TV1-Map: die zehn Paare werden in der Reihenfolge
8, 6, 5, 3, 2, 1, 0, 7, 4, 9 hintereinandergesetzt, jedes Glied für sich kanonisch kodiert, davor
der Map-Header für zehn Paare. Die Reihenfolge steht als Liste im Code, nicht als Kommentar.

Der Eintrag für NV2 in der Vektorliste trägt danach `wire_bytes` und behält
`expect_reject: NON_CANONICAL_ENCODING`. Seine Stellung in der Liste ändert sich nicht.

Danach `tests/vectors/vectors_01.json` neu erzeugen. Kein anderer Vektor darf sich ändern.

### 2. Der Wächter über die Ausnahme

`tests/test_verifier.py` enthält einen Test, der behauptet, die Menge der Vektoren mit
`expect_reject`, aber ohne Drahtbytes sei genau `{"NV2"}`. Diese Menge ist jetzt leer. Der Test
wird umgeschrieben, nicht gelöscht: er behauptet fortan, dass **jeder** Vektor mit `expect_reject`
Drahtbytes trägt. Sein Name wird entsprechend angepasst, sein Docstring nennt D291.

## Nicht-Ziele

- **Keine Änderung an `01-claim-atom.md` und `07-decisions.md`.** Beide sind mit dem
  Splice-Commit fertig.
- **Keine Änderung an anderen Vektoren**, weder an ihren Bytes noch an ihrer Reihenfolge.
- **Keine Änderung an Produktivcode.** Der Verifizierer bleibt unangetastet.
- **Keine Berichtigung der `einlesen-a-*`-Dateien.** Sie halten einen vergangenen Stand fest.
- **Keine getippten Bytes.** NV2 wird gerechnet.

## Abnahmekriterien

1. `make check` läuft durch. Die Testzahl ist **669**: NV2 tritt in die parametrisierte
   Vektorprüfung ein, der umgeschriebene Wächter bleibt ein Test.
2. Die erzeugten Drahtbytes von NV2 sind **309 Byte** lang, dekodieren zu derselben Map wie die
   signierten Bytes von TV1, und ihre kanonische Re-Serialisierung ist byte-gleich mit TV1s
   signierten Bytes.
3. Der Hex-Block in `01 §C.7` und `wire_bytes` von NV2 in `tests/vectors/vectors_01.json` sind
   zeichengleich, wenn man den Zeilenumbruch und die Einrückung des Spec-Blocks entfernt.
4. `git diff` gegen den Branchpunkt zeigt Änderungen ausschließlich in `tests/vectors/gen.py`,
   `tests/vectors/vectors_01.json` und `tests/test_verifier.py`.
5. In `tests/vectors/vectors_01.json` ändert sich gegenüber dem Branchpunkt genau ein Eintrag.

## Rücknahmeprobe

Eine. Die Kanonizitätsprüfung im Verifizierer wird so zurückgenommen, dass sie nie fehlschlägt;
der Vektortest für NV2 muss rot werden. Danach wiederherstellen. Bleibt er grün, fängt ihn ein
anderes Tor, und das ist ein Befund: dann trägt NV2 wieder mehr als einen Mangel.

## Abschluss

Ein Commit auf `00aj-nv2`. Im Bericht: die Testzahl, die Länge der NV2-Bytes, das Ergebnis des
Vergleichs aus Kriterium 2 und 3, das Ergebnis der Rücknahmeprobe und der **vollständige**
`git diff` gegen den Branchpunkt.
