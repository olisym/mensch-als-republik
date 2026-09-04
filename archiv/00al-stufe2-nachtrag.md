# Nachtrag zum Prompt für Stufe 2 (00al)

Der Stopp war richtig. Alle drei gemeldeten Punkte sind nachgemessen und in D306 entschieden.
Dieser Nachtrag ändert den Prompt `00al-stufe2-prompt.md` an drei Stellen; alles Übrige bleibt.

## Basis

Weiter auf `00al-stufe2`. Der Basis-Commit wandert auf den Commit, der D306 und diesen Nachtrag
trägt; er steht im Auftrag, mit dem dieser Nachtrag übergeben wird. Ein Commit, kein Merge.

## Änderung 1 — der Klassenschnitt bleibt, die Zahlen in D305 waren falsch

Auftrag 5 gilt unverändert: ausgegeben wird, wobei keiner der beiden Einzelmängel allein
`MALFORMED_CBOR` erzeugt. Die gemessenen 4382 in Klasse zwei und 199749 in Klasse vier sind
richtig, die Zahlen aus D305 waren es nicht; D306 berichtigt sie. Es ist nichts zu ändern — die
Abweichung war zu melden, und sie wurde gemeldet.

## Änderung 2 — die Vorrangprobe erwartet einen abgeleiteten Code

Der vierte Test aus Auftrag 8 wird ersetzt. Er lautet nicht mehr, dass jede Zeile der
Vorrangprobe `MALFORMED_CBOR` trägt, sondern:

> Jede Zeile der Vorrangprobe wird abgelehnt. Der Code ist `UNSUPPORTED_VERSION`, wenn einer ihrer
> beiden Einzelmängel allein diesen Code erzeugt, und sonst `MALFORMED_CBOR`.

Die Erwartung wird je Zeile aus den Einzelverdikten abgeleitet, nicht als Liste getippt. Die zwölf
betroffenen Zeilen bleiben in der Menge; sie herauszunehmen würde den einzigen Fall entfernen, in
dem die Probe eine Verschachtelung prüft. Die normative Grundlage steht in `01 §B.2` unter der
Überschrift zur Feldtabelle je Version.

Schlägt dieser Test trotzdem an, ist das zu melden und nicht zu reparieren: ein struktureller
Mangel bleibt auch unter fremder Version wahr, und ein solcher Fall wäre ein Befund über die
Vorrangordnung.

## Änderung 3 — doppelte Drahtfolgen und die Reihenfolge der Ausgabe

Zwei Saaten können denselben Paarmutanten ergeben. Es gilt dieselbe Regel wie im Gitter: die in
der stabilen Reihenfolge spätere Zeile wird verworfen, Etikett und Bytes bleiben damit paarweise
verschieden. Die Verwerfung wirkt über die ganze Ausgabe, nicht nur innerhalb einer Klasse.

Damit die Vorrangprobe davon nie getroffen wird, steht sie in der Ausgabereihenfolge **vor** den
Klassen eins bis drei. Der Bericht nennt die Zahl der verworfenen Doppelten.

## Unverändert

Alle Nicht-Ziele, die Abnahmekriterien und beide Rücknahmeproben gelten wie im Prompt. Der Bericht
enthält weiterhin den vollständigen `git diff` gegen den Basis-Commit, die Zeilenzahl je Klasse und
für die Vorrangprobe, und die Liste der nicht paarbaren Einzelmutanten — dass sie leer ist, wurde
unabhängig bestätigt und deckt sich mit dem Lauf.
