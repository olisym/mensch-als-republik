# 00ai — Vektoren für die Feldtabelle und ein Träger für die Codewerte

**Branch:** `00ai-feldtabelle`. Basis ist der Commit, der diese Datei einführt.

**Normative Grundlage:** `01 §2` (Feldtabelle), `01 §B.2` (Fehlerklassen), `01 §C.13` (Muster für
Aufbau und Darstellung der negativen Vektoren), D266, D272, D279, D280.

**Worum es geht.** Eine Mutantenkampagne hat gemessen, dass der Bestand elf der zwölf Tore, mit
denen der Verifizierer die Feldtabelle durchsetzt, nie auslöst. Der Lauf legt je einen negativen
Vektor darauf und bindet zusätzlich die Werte der Reject-Codes. Der Verifizierer selbst ist
richtig; es fehlt nur, was ihn festhält.

## Auftrag

### 1. Elf negative Vektoren in `tests/vectors/gen.py`

Nach dem Muster von NV14 bis NV19: der Core von TV1, an genau einer Stelle geändert, mit
`_signed_wire` über den geänderten Core neu signiert, in der Vektorliste als Eintrag mit
`wire_bytes` und `expect_reject` gleich `MALFORMED_CBOR`. Die Namen sind NV20 bis NV30, die
Reihenfolge in der Liste ist die hier genannte, und alle elf stehen hinter NV19.

| Name | Änderung am TV1-Core |
|---|---|
| NV20 | Key 0 trägt CBOR `true` statt 1 |
| NV21 | Key 1 trägt die ersten 31 Byte seines bisherigen Wertes |
| NV22 | Key 2 trägt ein Array aus drei Elementen: 1, `BOB_PUB`, `BOB_PUB` |
| NV23 | Key 2 trägt ein Array aus zwei Elementen: CBOR `true`, `BOB_PUB` |
| NV24 | Key 3 trägt die Zahl 1 statt einer Zeichenfolge |
| NV25 | Key 4 trägt die Zahl 1 statt einer Bytefolge |
| NV26 | Key 5 trägt die ersten 31 Byte seines bisherigen Wertes |
| NV27 | Key 7 trägt CBOR `true` |
| NV28 | Key 8 trägt die ersten 31 Byte seines bisherigen Wertes |
| NV29 | Core unverändert; im signierten Map trägt Key 9 die ersten 63 Byte der Signatur |
| NV30 | Key 3 fehlt |

NV29 ist der einzige, dessen Core mit dem von TV1 übereinstimmt. Er wird nicht über `_signed_wire`
gebaut, sondern über eigene Zeilen, die den Core kanonisch kodieren, über `DOM_SIG` signieren, die
Signatur kürzen und die vollständige Map kodieren.

Kein Vektor wird von Hand gerechnet und keiner wird getippt. Jeder entsteht aus dem TV1-Core im
Generator.

### 2. `tests/vectors/vectors_01.json` neu erzeugen

Die Datei wird durch den Lauf von `tests/vectors/gen.py` erzeugt und nicht von Hand geändert. Die
bestehenden Einträge müssen dabei byteweise unverändert bleiben.

### 3. Ein neuer Anhangsabschnitt in `01-claim-atom.md`

Hinter dem Abschnitt zu NV14 bis NV19 und vor der Änderungshistorie. **Angehängt, nicht
eingeschoben** (D250): keine bestehende Anhangsnummer ändert sich, keine bestehende Überschrift
wird umgeschrieben.

Aufbau nach dem Muster des Abschnitts zu NV14 bis NV19: eine Überschrift für den Abschnitt, ein
einleitender Absatz, und je Vektor ein Unterabschnitt mit dem verletzten Feld in der Überschrift,
einem oder zwei Sätzen zur Begründung des Codes und einem Codeblock mit `bytes` und `erwartet`. Die
Bytes werden aus der erzeugten Vektordatei übernommen, nicht abgeschrieben und nicht gekürzt; der
Zeilenumbruch im Codeblock folgt dem bestehenden Muster.

Der einleitende Absatz hält fest, dass jeder der elf genau eine Zeile der Feldtabelle oder den
Pflichtfeldsatz verletzt, im Übrigen kanonisch kodiert und über seinen eigenen Core signiert ist.

### 4. Ein Träger für die Codewerte in `tests/test_verifier.py`

Ein Test, der über alle Member von `ErrorCode` läuft und für jeden behauptet, dass sein Wert mit
seinem Membernamen übereinstimmt (D279).

### 5. Rücknahmeproben

Je Vektor eine Probe: das zugehörige Tor im Verifizierer so neutralisieren, dass seine Bedingung
nie zutrifft, den vollen Bestand fahren, bestätigen, dass genau dieser Vektor rot wird, und die
Neutralisierung zurücknehmen. Neun Proben treffen ihr Tor allein.

Zwei Tore sind doppelt geschützt und brauchen zwei Neutralisierungen zugleich (D280):

- **NV24** — das Typtor auf Key 3 in `_validate_field_types` **und** die Prüfung auf eine
  Zeichenfolge in `parse_predicate`. Dabei fallen weitere Tests rot; erwartet wird nur, dass NV24
  darunter ist.
- **NV30** — die Prüfung auf den Pflichtfeldsatz **und** das Typtor auf Key 3 in
  `_validate_field_types`.

Für den Träger aus Punkt 4 eine eigene Probe: den Wert eines beliebigen `ErrorCode`-Members ändern
und bestätigen, dass genau dieser Test rot wird.

Widerspricht eine Probe diesem Prompt, wird das gemeldet und nicht angepasst.

## Nicht-Ziele

- **Kein Produktivcode ändert sich.** Kein Tor wird verschoben, umformuliert, zusammengefasst oder
  ergänzt, keine Datei unter `mensch_als_republik/` wird angefasst. Findet der Lauf dabei einen
  Defekt im Verifizierer, wird er gemeldet und nicht behoben.
- **Keine bestehende Anhangsnummer und kein bestehender Vektorname ändert sich.** Kein bestehender
  Eintrag in `tests/vectors/vectors_01.json` ändert seinen Inhalt.
- Kein Registereintrag, keine neue Prüfregel, keine Änderung an `pruefregeln.md`.
- Die übrigen ungebundenen Erzeugerstellen im Verifizierer, im Index und in `predicates.py` bleiben
  unberührt. Sie stehen in D280 als benannter Rückstand.
- Keine Änderung an `tools/check_specs.py` und keinem anderen Werkzeug.

## Abnahmekriterien

- `make check` grün. Die Testzahl steigt um genau zwölf: elf Vektoren, ein Träger.
- Die elf neuen Einträge in `tests/vectors/vectors_01.json` tragen alle `expect_reject` gleich
  `MALFORMED_CBOR`; die bestehenden Einträge sind unverändert.
- Der neue Anhangsabschnitt trägt die nächste freie Anhangsnummer, und die Bytes in seinen elf
  Codeblöcken stimmen mit den erzeugten Vektoren überein.
- Elf Rücknahmeproben, elf rote Vektoren, jeweils der beauftragte; dazu die Probe für den Träger.
- `python3 tools/check_specs.py` grün.

## Abschluss

Ein Commit auf `00ai-feldtabelle`, kein Merge. Der Bericht enthält den **vollständigen** `git diff`
gegen den Branchpunkt, nicht nur `--numstat`, und die Ausgabe der zwölf Proben. Ein Bericht, der
den Diff als geliefert bezeichnet, ohne ihn zu enthalten, gilt nicht als Lieferung.
