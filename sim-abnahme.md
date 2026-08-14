# Simulation — Abnahme

Gegenstand: `impl/sim`, Commits `31534e7` und `30484b2`. 405 Tests, `make check` grün in drei
Blöcken.

**Abgenommen.**

## 1. Die Leitfrage

Nicht „läuft es", sondern: **läuft es getrennt.** Eine Simulation mit einem gemeinsamen Store
sieht von außen genauso aus und zeigt genau das nicht, worum es geht — Teilwissen, Konvergenz,
Partition. Sie wäre eine Blockchain im Kleinen und würde es nicht merken.

**Sie ist getrennt.** Jeder Teilnehmer hat ein eigenes Verzeichnis mit Schlüssel, Uhr und Inbox.
`store_laden()` baut den Store bei jedem Aufruf aus der eigenen Inbox; `zustellen` kopiert Dateien
und nichts bewegt sich ohne ausdrücklichen Schritt. Kein gemeinsames Objekt, das pro Teilnehmer
gefiltert wird.

Claims liegen als einzelne Dateien, benannt nach ihrer `claim_id`. Das ist keine Bequemlichkeit,
sondern die Bauform, die `01 §4` beschreibt: ein Claim ist offline selbstenthalten und trägt
seinen eigenen Verify-Key. Man könnte ihn ausdrucken.

Alles Rechnende kommt aus dem Paket. Die Simulation baut auf, stellt zu und zeigt an.

## 2. Befunde

Zwei, beide behoben in `30484b2`, beide klein.

**S-1 — `fork` hieß falsch.** Der Schalter tat das Richtige (`if not fork: write_h_prev`), aber
sein Name behauptete eine Protokolleigenschaft, die es nicht gibt. Es entsteht kein Fork, sondern
zwei Claims mit demselben `h_prev`; ob daraus Equivocation folgt, entscheidet Layer 01 allein.
Umbenannt in `kette_fortschreiben`, Voreinstellung `true`.

**S-2 — S6 hatte einen Beobachter zu viel und zu wenig.** Chris sah mit `now = 1000` dasselbe wie
Anna; damit stand zweimal dasselbe und einmal das Gegenteil, und Chris war zugleich das Subjekt
der ablaufenden Kante. Umgestellt auf vier Uhren um die Grenze herum.

## 3. Der Zugewinn

Zwei Dinge, die mit einem gemeinsamen Store unerreichbar waren.

**D117 — Equivocation als dritter Ausgang aus `ACTIVE`.** Beim Durchrechnen von S5 aufgefallen,
nicht beim Lesen. Zwei Registerinvarianten waren zu stark formuliert; sie haben jetzt einen
Vorbehalt. In einem gemeinsamen Store trifft der Zwilling sofort ein, `PASSED` entsteht gar nicht
erst, und der Rückfall bleibt unsichtbar.

**Der Grenzwert `now = t_exp`.** `01 §6` legt seit Layer 01 fest, dass ein Claim zeitlich gültig
ist **gdw. `now ≤ t_exp`** — die Grenze schließt ein. Geprüft war das nirgends: nicht in den
Vektoren von `01`, nicht in den Ankern, nicht in 399 Tests. S6 setzt jetzt zwei Beobachter einen
Tick auseinander, `5000` gegen `5001`, und trennt damit gültig von abgelaufen.

Ein Off-by-one in `_is_temporally_valid` fällt an keiner anderen Stelle auf, weil überall sonst
die Testwerte komfortabel links oder rechts der Grenze liegen. Derselbe Fund wie `GV-3` bei der
Auszählung: ein Zeichen im Quelltext entscheidet, und nur ein Vektor genau auf der Kante zeigt es.

**Offen und notiert:** dieser Grenzwerttest lebt bisher nur unter `tools/`. Ein Zufallsfund in
einem Werkzeug ist keine Zusicherung; er gehört in die Vektoren von Layer 01. Beim nächsten
Anfassen von `01` nachzuziehen.

## 4. Was jetzt vorführbar ist

`08 §2.2` war bis heute ein Satz: Equivocation wird nicht verhindert, sondern unbestreitbar. S5
zeigt, wann genau — **erst in dem Moment, in dem zwei Getäuschte einander zustellen.** Vorher sieht
keiner von beiden etwas Verdächtiges. Nur der Täter weiß von Anfang an, was er getan hat; er ist
der einzige Beobachter, dem seine eigene Equivocation sofort auffällt.

S3 und S6 gehören nebeneinander gelesen: dieselbe Erscheinung — zwei Beobachter, zwei Antworten —
mit zwei Ursachen. Die eine heilt beim Zustellen, die andere nie. Das ist die Grenze, die MaR
gezogen hat, und sie war bisher ein Satz im Register.

## 5. Fehlerformen dieser Runde

Beide Funde liegen **zwischen zwei Sichten** auf dieselbe Sache, nicht in einer Funktion. Damit
gehören sie zur Familie der Feldinventur aus D114: kein Durchgang durch den Code findet sie, weil
dort nichts falsch ist.

Die Konsequenz aus D117 hat sich sofort bewährt — Eigenschaften über Wissenszuwachs mit
**mehreren** Beobachtern zu prüfen, die verschiedene Teilmengen halten. Und die Konsequenz aus der
Beispielnukleus-Abnahme, **vor dem Schreiben zu rechnen**, hat in dieser Runde zum ersten Mal
präventiv gewirkt: alle sechs Szenarien waren durchgerechnet, bevor der Prompt entstand, und D117
fiel dabei an — vor der Implementierung statt in der Abnahme.
