# Stufe 2 der Kampagne: Paare aus zwei Mängeln (00al)

## Branch und Basis

Branch `00al-stufe2`, Basis-Commit `71dab88`. Ein Commit auf diesem Branch. Kein Merge, kein Push.

## Normative Grundlage

D305 mit allen fünf Beschlüssen und dem Nachtrag zur Voraussetzung. Dazu D289 für die Bauform der
Mutation, D293 für den Schnitt zwischen Repo und Vergleich, D299 für die zweistufige Auswertung
und `01 §B.2` für Vorrang und freie Wahl.

## Auftrag

**1. Ein neues Werkzeug `tools/paare.py`.** Es baut die Mutantenmenge der Stufe 2 und gibt sie in
derselben Form aus wie `tools/gitter.py`: eine Hexzeile je Mutant, mit `--manifest` stattdessen die
Etiketten, gleich viele Zeilen in beiden Aufrufen, stabile Reihenfolge über zwei Läufe hinweg.

**2. Die Einzelmängel werden aus `tools/gitter.py` gelesen, nicht nachgebaut.** Das Werkzeug nimmt
die Ausgabe von `mutant_lines()` und leitet aus jedem Mutanten seine Feldänderung gegenüber der
Saat ab. Zeilen mit Präfix `C` bleiben aussen vor (D305 Beschluss 5).

**3. Was eine Feldänderung ist.** Ein Mutant der Familie `B` wird als ganze Map mit der Saat
verglichen; ein Mutant der Familie `A` nur in seinem Kern, also ohne den Signaturschlüssel, weil
diese Familie nach der Mutation neu signiert und sich dort immer unterscheidet. Paarbar ist ein
Mutant genau dann, wenn dieser Vergleich **genau einen** Schlüssel nennt, der hinzugekommen,
weggefallen oder anders belegt ist. Ist ein Mutant nicht paarbar, wird er übersprungen und am Ende
mit Etikett gemeldet — nicht stillschweigend weggelassen und nicht durch eine Sonderbehandlung
gerettet.

**4. Wie ein Paar entsteht.** Zwei paarbare Mutanten derselben Saat und derselben Familie, deren
Schlüssel verschieden sind, ergeben einen Paarmutanten: beide Feldänderungen werden auf die Saat
angewandt. Für Familie `A` wird danach mit dem Autorenschlüssel der Saat über den kombinierten
Kern neu signiert, genau wie im Bestand. Für Familie `B` wird nicht neu signiert; ist der
Signaturschlüssel selbst einer der beiden geänderten Schlüssel, trägt der Paarmutant dessen
mutierten Wert.

**5. Der Zuschnitt nach D305.** Jedes Paar wird nach den Verdikten seiner beiden Einzelmutanten
eingeordnet. Ausgegeben werden die Klassen eins bis drei vollständig, also alle Paare, bei denen
**keiner** der beiden Einzelmutanten allein `MALFORMED_CBOR` erzeugt. Klasse vier wird nicht
ausgegeben.

**6. Die Vorrangprobe.** Zusätzlich zu den Klassen eins bis drei entsteht eine benannte kleine
Menge: für jede Kombination aus Familie, Saat und Einzelcode ausser `MALFORMED_CBOR` genau ein
Vertreter, gepaart mit einem Einzelmutanten derselben Saat und Familie, der allein
`MALFORMED_CBOR` erzeugt und einen anderen Schlüssel betrifft. Die Auswahl ist deterministisch und
hängt nicht von einem Zufallswert ab; welche Regel sie festlegt, ist frei, solange sie in einem
Satz beschreibbar ist und über zwei Läufe dasselbe Ergebnis liefert.

**7. Etiketten.** Präfix `P`, danach die Klasse, danach Familie und Saat, danach beide Einzelmängel
in einer festen Reihenfolge, so dass dasselbe Paar nicht zweimal unter verschiedenen Etiketten
erscheint. Die Vorrangprobe trägt eine eigene, von den Klassen unterscheidbare Bezeichnung.

**8. Tests in `tests/test_paare.py`.**

- Jede ausgegebene Zeile unterscheidet sich von ihrer Saat in genau zwei Schlüsseln, im Sinne von
  Auftrag 3 gemessen.
- Etiketten und Bytes sind über die ganze Ausgabe paarweise verschieden, und keine Zeile ist gleich
  einer Saat.
- Zu jeder der drei Klassen und zur Vorrangprobe gibt es mindestens eine Zeile.
- Jede Zeile der Vorrangprobe wird vom Verdiktläufer mit `MALFORMED_CBOR` abgelehnt.
- Manifest und Hexausgabe sind gleich lang, und zwei Aufrufe liefern dasselbe.

## Nicht-Ziele

- **Keine inhaltliche Änderung an `tools/gitter.py`.** Die Stufe-1-Menge bleibt Zeile für Zeile
  dieselbe. Zulässig ist allein, eine bereits vorhandene Hilfsfunktion öffentlich zu machen, wenn
  das Werkzeug sie braucht; alles Weitere ist zu melden.
- **Keine Klasse vier in der Ausgabe** und keine gezogene Stichprobe irgendeiner Art (D305).
- **Keine Kombinationen aus drei Mängeln** (D305 Beschluss 4).
- **Keine Änderung an `tools/korpus.py`, `tools/verdikt.py`, am Verifizierer, am Kodierer oder an
  einer Spec-Datei.**
- **Kein Aufruf der Zweitfassung** aus dem Repo heraus (D293).
- Keine Paare über Saatgrenzen oder Familiengrenzen hinweg.

## Abnahmekriterien

- `make check` läuft grün; die Tests aus `tests/test_gitter.py` bleiben unverändert und grün.
- Die Ausgabe von `tools/gitter.py` ist gegenüber dem Basis-Commit byte- und etikettgleich.
- Die fünf neuen Tests sind grün.
- Der Bericht nennt die Zeilenzahl je Klasse und für die Vorrangprobe, dazu die Liste der nicht
  paarbaren Einzelmutanten mit Etikett. Die Zahlen werden gemessen und nicht aus D305 übernommen;
  weicht eine davon ab, ist das zu melden.

## Rücknahmeprobe

Zwei Proben, je mit dem Namen des roten Tests und seiner Meldung (Prüfregel 60). Nach Prüfregel 62
darf keine Probe die Menge leeren, über die der erwartete rote Test quantifiziert — beide unten
vergrössern die Menge oder entfernen einen Teil, während der tragende Test über einen anderen Teil
läuft:

1. Die Vorrangprobe aus der Ausgabe nehmen. Erwartet rot: der Test, der zu jeder Klasse und zur
   Vorrangprobe mindestens eine Zeile verlangt.
2. Die Paarbildung auch auf gleiche Schlüssel zulassen. Erwartet rot: der Test auf genau zwei
   geänderte Schlüssel.

Beide Proben werden zurückgenommen, bevor committet wird.

## Abschluss

Ein Commit auf `00al-stufe2`. Der Bericht enthält den vollständigen `git diff` gegen `71dab88`,
nicht nur `--numstat`, dazu die Ausgabe von `make check`, die Zeilenzahlen aus den
Abnahmekriterien und beide Rücknahmeproben mit Testnamen. Widerspricht eine Messung diesem Prompt,
wird sie gemeldet und nicht angepasst.
