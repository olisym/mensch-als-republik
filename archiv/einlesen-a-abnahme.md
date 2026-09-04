# Abnahme: Einlesepfad Lauf A (`impl/einlesen`, `65b457e`)

**Ergebnis: angenommen mit zwei Defekten.** Beide liegen in Tests, keiner im Produktivcode. Sie
werden vor dem Merge auf demselben Branch behoben.

## 1. Was geprüft wurde

`verifier.py` ist richtig. Der `try` steht in Schritt 2c an seinem Platz, nicht in 2a; die
Reihenfolge §6 2a→2b→2c→2d ist unverändert. `read_claim` fängt `VerifierError` und sonst nichts.
`ErrorCode` und `read_claim` sind exportiert. `grep -c 'except Exception'` ergibt 2 — beide um
einen fremden Aufruf, wie D131 es verlangt.

BV3 wird in `gen.py` aus `signed_map(tv1)` **gerechnet**, nicht abgetippt. Der Kopplungstest zieht
seine Claims aus `welten()` und baut keine eigene Kette — kein D129-Verstoß.

Die abgeleitete Parametrisierung erreicht vier Vektoren: NV1 über `signed_bytes`, BV1–BV3 über
`wire_bytes`. NV2 fällt heraus, weil es keine Draht-Bytes trägt, und wird vom Zwilling
`test_nv2_non_canonical_encoding_read_claim` getragen. Die Rechnung geht auf: 474 + 10 + 2 = 486,
Eigenschaftstests 11 → 13.

Kriterium 5 ist bestätigt und im Commit-Text dokumentiert.

## 2. Defekte

### A-1 — Die Parametrisierung kann still auf null fallen

`_reject_vectors_with_wire()` läuft beim Import und liefert heute vier Einträge. Wird die JSON
umbenannt, ein Feld anders geschrieben oder ein Vektor ohne Draht-Bytes ergänzt, schrumpft die
Liste — und `pytest` meldet eine leere Parametrisierung als **skip**, nicht als Fehler. Der Test
sähe grün aus und prüfte nichts.

Das ist dieselbe Klasse wie der Befund aus der `impl/authoring`-Abnahme, nur seitenverkehrt: dort
wurde gegen eine getippte Menge verglichen statt abgeleitet, hier wird abgeleitet, ohne die
Ableitung zu verankern.

**Zu bauen:** die Liste der **ausgeschlossenen** Vektoren wird geprüft. Vektoren mit
`expect_reject`, aber ohne `wire_bytes` und ohne `signed_bytes`, sind genau `{"NV2"}` — und NV2 hat
einen eigenen Test. Ein `assert`, das diese Menge festhält, fällt auf, sobald ein weiterer Vektor
still herausfällt. Die Zahl vier wird **nicht** getippt; geprüft wird die Ausnahme, nicht die
Summe.

### A-2 — BV3 ist nicht an seine Bedeutung gebunden

Geprüft wird nur, daß BV3 `NON_CANONICAL_ENCODING` ergibt. Das erfüllt jede beliebige
nicht-kanonische Bytefolge. Was BV3 laut `Anhang C.8` **ist** — TV1s signierte Map in
indefinite-length-Form, 310 statt 309 Byte, re-serialisiert auf TV1s `signed_bytes` — prüft nichts.

Die Parallelenprüfung macht es sichtbar: NV2 hat zwei Tests, den Reject **und**
`test_nv2_reserializes_to_tv1_core`. BV3 hat nur den ersten.

Das wiegt bei BV3 schwerer als bei NV2, weil NV2 eine handkopierte Konstante ist und BV3 gerechnet
wird. Ein Fehler in der Schleife in `gen.py` — falsche Schlüsselreihenfolge, `core_map` statt
`signed_map` — erzeugte andere Bytes, die weiterhin `NON_CANONICAL_ENCODING` ergäben. Die JSON
wird committet; die Abweichung vom Hex in `Anhang C.8` fiele nie auf.

**Zu bauen:** ein Test analog zu `test_nv2_reserializes_to_tv1_core` —
`cbor_canon.reserialize(BV3) == TV1.signed_bytes` und `len(BV3) == len(TV1.signed_bytes) + 1`. Der
Generator prüft sich damit gegen den Vektor, den er erzeugt.

## 3. Notizen ohne Auftrag

**Der Ablehnungszweig der Kopplung ist praktisch tot.** Bei 2 von 534 Claims betritt ihn ein Lauf
mit `max_examples=100` selten und unter `schnell` fast nie. Die Aussage „`read_claim` und
`structural_check` stimmen auf Rejects überein" trägt in Wahrheit die Vektorparametrisierung aus
§2.2 zusammen mit `test_bv_structural_check`, nicht der Eigenschaftstest. Das ist vertretbar —
beide Wege sind abgedeckt —, aber der Eigenschaftstest klingt stärker, als er ist. Kein Auftrag;
festgehalten, damit ein späterer Lauf ihn nicht für die Absicherung hält, die er nicht leistet.

**`read_claim` setzt voraus, daß jede `VerifierError` ein `code`-Attribut hat.** Alle elf
Unterklassen tragen es als Klassenattribut, die Basisklasse nicht. Ein `raise VerifierError()`
irgendwo im Prüfpfad ergäbe im `except` einen `AttributeError` und bräche die Totalität — nicht
lautstark, sondern genau an der Stelle, die nie werfen soll. Heute existiert keine solche Stelle.
Der Nachlauf prüft das per `grep` und hält das Ergebnis fest; ergibt es Fundstellen, ist es ein
eigener Befund.

## 4. Nachgang, nicht Teil dieses Laufs

**`welten()` erzeugt strukturell ungültige Claims.** Die Messung sagt: 2 von 534, ausschließlich
`INCOHERENT_EXPIRY`. Die Population ist im übrigen sauber — der Befund ist kleiner als befürchtet,
aber er ist echt. Die Lage `"vergangen"` will einen **abgelaufenen** Claim, also `t < t_exp ≤ now`,
und zieht heute `t_exp ∈ [1, now-1]` ohne Blick auf `t`. Wo `t ≥ t_exp` herauskommt, entsteht kein
abgelaufener Claim, sondern gar keiner.

Der Grund, warum es nie aufgefallen ist: `classify_all` ruft `structural_check` nur für
Lifecycle-Kandidaten, nie für den Claim selbst. Die Eigenschaftstests klassifizieren also Claims,
die ein Empfänger zurückgewiesen hätte. Erst der Einlesepfad macht die Lücke sichtbar — das ist der
erste Ertrag von D131 jenseits seines eigenen Zwecks.

Die Reparatur gehört in einen eigenen Lauf an `welten.py`, zusammen mit **B-4** (die
Zwillingsbuchführung zieht kein Budget ab). Beide sind Buchführungsfehler desselben Erzeugers;
getrennt zu reparieren hieße, zweimal dieselbe Datei anzufassen und zweimal die Anker zu bewegen.
