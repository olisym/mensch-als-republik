# Prompt 00ag — Feldsatz, Arity und sechs Vektoren (D270, D272)

## Branch und Basis

Branch `lauf/00ag-feldsatz`, gezogen von `origin/main` nach einem `git fetch` — das ist der
Commit, der diese Datei ins Repo bringt. Der Registerstand darunter ist `a05eaaf`. Ein einziger
Commit am Ende. Kein Merge, kein Push, kein Rebase.

## Normative Grundlage

- **D272** im Register: fünf gemessene Ausgänge der Fassung weichen vom geltenden Text ab. Die
  Norm ändert sich in diesem Lauf **nicht**; sie wird eingeholt.
- **D270** im Register und der Absatz „Die Eingabe ist genau ein Item (normativ)" in `01 §3`:
  die empfangenen Bytes sind die Kodierung genau eines CBOR-Items.
- **D266** im Register: Feldsatz-Verstöße sind `MALFORMED_CBOR`, und die Feldtabelle gilt je
  Version. Bei nicht unterstützter Version wird nicht mehr gegen `01 §2` geprüft.
- `01 §2` — die Feldtabelle mit Typ, Pflicht und Größe. `version`, `t`, `t_exp` und `J[0]` sind
  **uint**.
- `01 §6` Punkt 2 — kanonisch, dekodierbar, ohne doppelte Keys, mit dem Feldsatz aus `01 §2`:
  jedes Pflichtfeld vorhanden, kein Key außerhalb der Tabelle, Typen und Längen wie angegeben.
- `01 §B.2` — die Codetabelle und die beiden normativen Absätze darunter. `MALFORMED_CBOR` trägt
  seit D270 auch Restbytes hinter dem Item.
- **D262 und D265** — normiert ist der Vorrang über den **Inhalt der Aussage**, nicht die
  Prüfreihenfolge. Es wird keine Schrittfolge vorgeschrieben und auch keine implizit gebaut.
  Verboten ist allein der falsche Satz: ein Code, dessen Aussage die Bytefolge nicht trägt.
- **D250** — ein Anhangsabschnitt wird angehängt, nicht eingeschoben.

## Auftrag

### Schritt 1 — die sechs Ausgänge in `mensch_als_republik/verifier.py`

Für jede der folgenden Bytefolgen liefert `read_claim` den genannten Code. Wie die Fassung
dorthin kommt, ist ihr überlassen; die Reihenfolge der Prüfungen wird **nicht** normiert.

1. **Falscher Feldtyp in einem uint-Feld.** Ein Wert, der kein CBOR-uint ist, erfüllt `version`,
   `t`, `t_exp` oder `J[0]` nicht. Das betrifft ausdrücklich CBOR `true` und `false` (Major 7)
   und negative Integer (Major 1). → `MALFORMED_CBOR`.
   Hinweis zur Ursache: `bool` ist in Python eine Unterklasse von `int`, und `True == 1`. Ein
   Test auf `isinstance(x, int)` ist damit kein Test auf uint.
2. **Key außerhalb der Feldtabelle.** Ein Key, den `01 §2` nicht führt, macht die Bytefolge
   ungültig — auch dann, wenn der Autor über den erweiterten Core signiert hat und die Signatur
   verifiziert. → `MALFORMED_CBOR`.
3. **Doppelter Map-Key.** Ein Schlüsselwert, der zweimal vorkommt, ist ein Mangel, den keine
   Kodierung behebt. Maßgeblich ist die **semantische** Gleichheit der dekodierten Schlüssel,
   nicht die Gleichheit ihrer Kodierung: `h'01'` und `h'1801'` sind derselbe Key. →
   `MALFORMED_CBOR`.
4. **Nicht unterstützte Version.** Ist `version` ein uint, aber nicht 1, ist der Code
   `UNSUPPORTED_VERSION`, und Pflichtfelder, fremde Keys und Längen werden **nicht** mehr gegen
   `01 §2` geprüft — die Tabelle gilt je Version, und `MALFORMED_CBOR` behauptete dort einen
   Mangel, den erst die v1-Tabelle setzt. Fehlt `version` oder ist sie kein uint, bleibt es bei
   `MALFORMED_CBOR`: ohne lesbare Version ist nicht entscheidbar, welche Tabelle gilt.
5. **Restbytes hinter dem Item.** Enthalten die empfangenen Bytes nach dem ersten vollständigen
   CBOR-Item noch etwas, ist die Folge keine Kodierung eines Claims — auch dann nicht, wenn die
   Restbytes selbst ein gültiger Claim sind. → `MALFORMED_CBOR`.
6. **Der Kommentar an der Schlüsselprüfung**, doppelte Keys seien vom Dekoder bereits
   ausgeschlossen, ist gemessen falsch und wird berichtigt oder entfernt.

### Schritt 2 — sechs Vektoren in `tests/vectors/gen.py`

Sechs neue Einträge, alle in der Form der BV-Vektoren aus `01 §C.8`: ein Feld `wire_bytes` und
ein Feld `expect_reject`, kein `claim_id`, kein `core_bytes`, kein `sigma`. Sie stehen hinter
`NV13` in der Liste. Die Bytes werden **erzeugt**, nicht getippt: aus dem TV1-Core, der in
`gen.py` bereits gebaut wird, und dem vorhandenen Alice-Seed.

Grundlage aller sechs ist der TV1-Core aus `01 §C.1`, Feld für Feld unverändert, außer wo unten
etwas anderes steht:

`{ 0:1, 1:ALICE, 2:[1, BOB], 3:"nuc:<N>/vouch@1", 4:h'a1001864', 5:N, 6:1700000000,
7:1735689600, 8:h_prev_genesis(ALICE) }`, dazu `9:σ` mit `σ` über `DOM_SIG ‖ core_bytes`.

- **NV14** — der TV1-Core zusätzlich mit Key **20**, Wert uint **1**. Der Core wird mit dem
  Alice-Seed **neu signiert**, `σ` deckt den erweiterten Core also ab. `wire_bytes` ist die
  kanonische Kodierung der Map aus Core und `σ`. Erwartet: `MALFORMED_CBOR`.
- **NV15** — der TV1-Core, Key 6 trägt CBOR `true` (`h'f5'`) statt der Zahl. Neu signiert.
  Erwartet: `MALFORMED_CBOR`.
- **NV16** — der TV1-Core, Key 6 trägt die negative Zahl **-5**. Neu signiert. Erwartet:
  `MALFORMED_CBOR`.
- **NV17** — das **unveränderte** signierte TV1-Objekt, aber Key 6 kommt zweimal vor: zuerst mit
  `1700000000`, unmittelbar danach mit `1700000001`. Die elf Paare stehen in nicht fallender
  Key-Ordnung, der Map-Header nennt elf Paare, jedes Paar ist für sich kürzest kodiert, und `σ`
  bleibt TV1s Signatur. Diese Bytefolge wird von Hand zusammengesetzt, weil keine Map sie
  darstellt. Erwartet: `MALFORMED_CBOR`.
- **NV18** — der TV1-Core mit Key 0 = **2** und **ohne** Key 6, sonst unverändert. Neu signiert,
  die Signatur verifiziert also über den eigenen Core. Erwartet: `UNSUPPORTED_VERSION`.
- **NV19** — das unveränderte signierte TV1-Objekt, gefolgt von einem einzigen Byte `h'00'`.
  Erwartet: `MALFORMED_CBOR`.

Danach `tests/vectors/vectors_01.json` neu erzeugen (`python -m tests.vectors.gen` oder der in
`gen.py` vorgesehene Weg). Die Datei wird **nicht** von Hand bearbeitet.

### Schritt 3 — Träger in `tests/test_vectors_01.py`

Je Vektor ein Träger, der die Bytes aus `vectors_01.json` liest und prüft, dass `read_claim`
genau den Code aus `expect_reject` liefert. Der erwartete Code wird aus der Vektordatei
**abgeleitet**, nicht im Test getippt. Die bestehenden Träger, `GOLDEN` und `GOLDEN_SIGMA`
bleiben unangetastet.

### Schritt 4 — Anhang C.13 in `01-claim-atom.md`

Ein neuer Abschnitt `### C.13 NV14–NV19 — Feldsatz, doppelte Keys, Version und Arity`,
**angehängt** hinter C.12 und vor der Änderungshistorie. Aufbau und Zeilenbreite wie bei den
BV-Vektoren in C.8: eine kurze Einleitung, dann je Vektor ein Absatz mit Begründung und ein
Codeblock mit der `bytes`-Zeile zu **64 Hexzeichen** je Zeile, elf Zeichen Einzug für die
Folgezeilen, und einer Schlusszeile `erwartet = Reject: <CODE>`. Die Hexwerte werden aus der
erzeugten `vectors_01.json` übernommen, nicht abgeschrieben.

Die Einleitung hält zwei Dinge fest: dass fünf der sechs genau einen Mangel tragen, und dass
NV18 zwei trägt und deshalb — wie BV2 in C.8 — den **Vorrang** prüft und keine Prüfreihenfolge.
Bei NV14 wird gesagt, dass der Autor den erweiterten Core mitsigniert hat, damit
`BAD_SIGNATURE` keine wahre Aussage über die Folge ist.

## Ausdrückliche Nicht-Ziele

- **Keine neue Fehlerklasse.** `01 §B.2` behält seine zwölf Zeilen.
- **Keine normierte Prüfreihenfolge** und keine Umbenennung der Kommentarmarken in
  `verifier.py`. Nur Ausgänge sind verlangt (D262).
- **Keine Änderung an `pyproject.toml`.** Reicht die installierte `cbor2`-Fassung für einen der
  sechs Ausgänge nicht aus, wird das **gemeldet** und nicht durch ein Anheben des Pins gelöst.
- **Indefinite-Length bleibt erlaubt und bleibt `NON_CANONICAL_ENCODING`.** BV3 darf sich nicht
  bewegen.
- **Keine Änderung an bestehenden Vektoren**, an `GOLDEN`, an `GOLDEN_SIGMA` oder an C.1 bis
  C.12.
- **Kein `float` und kein `fractions` im Produktivcode**, `now` bleibt Parameter.
- **Kein Anfassen der Layer 02 bis 04** und keiner Datei außerhalb der oben genannten.
- Widerspricht eine Messung diesem Prompt, wird sie **gemeldet, nicht angepasst**. Keine
  Erwartung wird nachgezogen, um einen Test grün zu bekommen.

## Abnahmekriterien

1. `make check` läuft grün. Die Testzahl wird **genannt**, vorher und nachher.
2. Alle bisherigen Tests bleiben grün; keiner wird geändert oder entfernt.
3. `vectors_01.json` ist neu erzeugt und enthält genau sechs zusätzliche Einträge, jeder mit
   `wire_bytes` und `expect_reject`, keiner mit `claim_id`.
4. Für jeden der sechs Vektoren liefert `read_claim(wire_bytes)` genau den erwarteten Code.
5. Die Hexwerte in Anhang C.13 sind byte-gleich mit den `wire_bytes` aus `vectors_01.json`.
6. `tools/check_specs.py` meldet keinen Befund.

## Rücknahmeproben

Fünf Stück, eine je Reparatur aus Schritt 1 — Punkte 1 bis 5. Jeweils: die Reparatur
zurücknehmen, den Testlauf fahren, **melden welche Träger rot werden und wie viele**, die
Rücknahme wieder aufheben. Nicht abgekürzt und nicht zusammengefasst. Wird bei einer Rücknahme
**kein** Träger rot, ist das der wichtigste Befund des Laufs und gehört an den Anfang des
Berichts.

## Abschluss

Ein Commit auf `lauf/00ag-feldsatz`. Der Bericht enthält den **vollständigen** `git diff` gegen
den Branchpunkt, nicht nur `--numstat`, dazu die Testzahlen und die fünf Rücknahmeproben. Kein
Merge, kein Push.
