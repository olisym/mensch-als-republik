# 00ad — Anhang C: negative Vektoren für den Fehlerkanal

## Branch und Basis

Branch `00ad-vektoren`, Basis-Commit `5362a35` auf `main`. Ein Commit am Ende, kein Merge.

## Normative Grundlage

- `01 §6` Punkte 1 bis 7: die strukturelle Gültigkeit und ihre sieben Bedingungen.
- Anhang B von `01-claim-atom.md`, Abschnitt B.2: die Fehlerklassen und ihre Auslöser.
- `01 §2.2` Regel 3: die Bindungsregel mit ihren zwei MUSS.
- D256: die Vorentscheidung, dass die Messfläche vor der Zweitimplementierung entsteht.
- D250: ein Anhang wird angehängt, nicht eingeschoben.

## Lage

Anhang C trägt zehn Abschnitte C.0 bis C.9. Drei der elf Reject-Codes haben dort einen Vektor
mit erwartetem Ausgang: `INVALID_GENESIS_ANCHOR` in C.5, `NON_CANONICAL_ENCODING` in C.7 und
C.8, `MALFORMED_CBOR` in C.8. Acht Codes haben keinen. Layer 01 hat als einziges Layer keine
eigene Datei mit Golden Anchors; Anhang C ist die gesamte Messfläche für eine
Zweitimplementierung.

`tests/test_verifier.py` sammelt in `_reject_vectors_with_wire` jeden Vektor mit dem Feld
`expect_reject` und Bytes und prüft ihn in `test_read_claim_reject_vectors` gegen den benannten
Code. Ein neuer Vektor im Generator erzeugt dort von allein einen Test. Ebenso erzeugt ein
Eintrag in `GOLDEN` in `tests/test_vectors_01.py` von allein einen Test auf die Claim-Kennung.

## Auftrag

Acht negative Vektoren NV4 bis NV11 bauen, sieben Fehlerklassen abdecken.

**Konstruktionsprinzip: genau ein Mangel je Vektor.** Alle Felder ausser dem genannten sind
gueltig, und jeder Vektor ist korrekt signiert. Nur so ist der erwartete Code eindeutig,
unabhaengig davon, an welcher Stelle seiner Prüfreihenfolge eine Implementierung ihn findet.
Das ist dieselbe Anforderung, die C.8 für die Byte-Vektoren im Text bereits festhält.

**Grundwerte, sofern unten nichts anderes steht:** die Felder von TV1, also `I` gleich ALICE,
`J` gleich Tupel aus 1 und BOB, `p` gleich das Vouch-Prädikat auf `N`, `v` gleich der
Vouch-Nutzlast von TV1, `N` gesetzt, `h_prev` gleich der Identitäts-Genesis-Anker von ALICE,
kein `t_exp`, signiert mit ALICE.

| Name | Abweichung vom Grundwert | `t` | erwartet |
|------|--------------------------|-----|----------|
| NV4 | `version` ist 2 | 1700000401 | `UNSUPPORTED_VERSION` |
| NV5 | erstes Glied von `J` ist 4 | 1700000402 | `UNKNOWN_J_TAG` |
| NV6 | `p` ist der Text foo/vouch@1, `N` abwesend | 1700000403 | `UNKNOWN_NAMESPACE` |
| NV7 | `N` ist 32 Byte h'11', `p` bleibt kanonisch auf `N` | 1700000404 | `BAD_SCOPE_BINDING` |
| NV8 | `p` trägt den Alias beispiel-alias, `N` abwesend | 1700000405 | `BAD_SCOPE_BINDING` |
| NV9 | `p` ist der Text core/rotate@1, `J` wie TV3, kein `v`, kein `N` | 1700000406 | `RESERVED_CORE_PREDICATE` |
| NV10 | signiert mit BOB statt ALICE, `I` bleibt ALICE | 1700000407 | `BAD_SIGNATURE` |
| NV11 | `t_exp` gleich `t` | 1700000408 | `INCOHERENT_EXPIRY` |

Zu NV7 und NV8: die Bindungsregel trägt zwei MUSS. NV7 prüft den Fall, dass `N` gesetzt ist und
nicht entspricht; NV8 den Fall, dass `N` bei Alias-Kodierung fehlt. Zwei Vektoren, weil ein
einzelner nur einen der beiden Zweige sieht.

Zu NV11: gewählt ist die Gleichheit und nicht der offensichtliche Fall `t_exp` kleiner `t`, weil
`01 §6` Punkt 7 die echte Kleiner-Beziehung verlangt und die Gleichheit damit genau auf der
Grenze liegt.

Zu den `t`-Werten: acht verschiedene Zeitpunkte, damit acht verschiedene Claim-Kennungen
entstehen. Dass die Vektoren untereinander und mit TV1 dasselbe Paar aus Autor und `h_prev`
teilen, ist ohne Folge: sie werden abgelehnt und gelangen in keinen Store.

### Was zu ändern ist

1. `tests/vectors/gen.py`: die acht Vektoren bauen, jeder mit `expect_reject`.
2. `tests/vectors/vectors_01.json`: neu erzeugen.
3. `tests/test_vectors_01.py`: `GOLDEN` um die acht Claim-Kennungen erweitern. Die Werte kommen
   aus dem Generator, nicht aus der Hand.
4. `01-claim-atom.md`: Anhang C um einen Abschnitt C.10 erweitern, mit NV4 bis NV11 als
   Unterabschnitte in der Form von C.8. Je Vektor: der Core in Feldschreibweise, die Bytes als
   Hex im Umbruchstil der bestehenden Vektoren, die Claim-Kennung, die Signatur und die Zeile
   mit dem erwarteten Reject. Dazu ein Satz je Vektor, welche Bedingung aus `01 §6` verletzt ist.

### Rücknahmeprobe

Fuer jeden der acht Vektoren wird die Prüfung neutralisiert, die ihn nach Anhang B ablehnt, und
gemeldet, welche Tests rot werden. Wo zwei Vektoren dieselbe Prüfstelle haben, wird das
gemeldet und nicht künstlich getrennt. Die Ausgabe ist eine Tabelle aus Vektorname,
neutralisierter Stelle und Anzahl roter Tests; die rohe Trefferliste gehört in eine Datei im
Sandkasten, nicht in den Bericht. Nach jeder Probe wird der Stand zurückgesetzt.

Ein Vektor, dessen Probe keinen einzigen Test rot färbt, ist ein Befund und wird gemeldet, nicht
repariert.

## Nicht-Ziele

- Kein Vektor für `FOREIGN_LIFECYCLE`. Sein aktiver Träger sitzt nach D138 in der
  Zustandsprüfung und verlangt ein bekanntes Ziel; er gehört nicht in die zustandslose Stufe.
- Keine Änderung an `mensch_als_republik/`. Kein neuer Reject-Code, keine geänderte
  Prüfreihenfolge, keine Anpassung eines bestehenden Auslösers.
- Keine Änderung an TV1 bis TV5, NV1 bis NV3, BV1 bis BV3 oder ihren goldenen Werten.
- Keine Umnummerierung in Anhang C. C.10 wird angehängt; ein Einschub zwischen C.7 und C.8 ist
  ausgeschlossen, weil eine Umnummerierung genau der Fehlertyp ist, den die Verweisprüfung nicht
  sehen kann.
- `test_reject_vectors_without_wire_are_exactly_nv2` bleibt unverändert. Jeder neue Vektor
  trägt Bytes.
- Kein neuer Testcode in `tests/test_verifier.py`. Die vorhandene Sammelfunktion nimmt die
  Vektoren auf.

## Abnahmekriterien

1. `make check` grün, `ruff` grün.
2. Mindestens 617 Tests grün. Die Zahl ist eine untere Schranke: acht Vektoren erzeugen acht
   Tests in der Reject-Parametrisierung und acht in der Kennungs-Parametrisierung, gerechnet auf
   601 vor dem Lauf. Fällt sie höher aus, wird die Differenz erklaert, nicht angeglichen.
3. Vier Dateien geändert, keine weitere.
4. Anhang C trägt danach elf Abschnitte, C.0 bis C.10.
5. Die Probentabelle liegt vor, mit einer Zeile je Vektor.
6. Der vollständige `git diff` gegen `5362a35`, nicht nur `--numstat`.

## Meldepflichten

Widerspricht eine Messung diesem Prompt, wird sie gemeldet und nichts angeglichen. Insbesondere:
faellt ein Vektor mit einem anderen Code durch als hier genannt, ist der Prompt falsch oder der
Vektor trägt zwei Mängel — beides ist ein Befund und keine Reparatur am erwarteten Wert.

## Abschluss

Ein Commit auf `00ad-vektoren`. Kein Merge, kein Push nach `main`.
