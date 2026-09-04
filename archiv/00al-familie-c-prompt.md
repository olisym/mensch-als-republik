# Familie C: nicht-kanonische Kodierung im Gitter (00al)

## Branch und Basis

Branch `00al-familie-c`, Basis-Commit `5c8ce86`. Ein Commit auf diesem Branch. Kein Merge, kein
Push, kein zweiter Branch.

## Normative Grundlage

D303 mit allen vier Beschlüssen. Dazu `01 §3` für den Kanonizitätsbegriff und `01 §B.2` für die
Fehlerklasse und ihren Vorrang. Die Bauform der bestehenden Familien steht in D289 und D297.

## Auftrag

**1. Eine dritte Familie in `tools/gitter.py`.** Sie nimmt jede Saat unverändert, dekodiert sie
nicht und mutiert ihren Inhalt nicht. Sie kodiert dieselbe Aussage nicht-kanonisch. Etikettpräfix
ist `C`, danach der Saatname, danach der Operatorname; wo ein Operator feldweise greift, folgt der
Schlüssel als vierter Teil. Die Familie geht durch dieselbe Aufnahme wie A und B, damit Duplikate
und Saatbytes weiter ausgeschlossen bleiben.

**2. Fünf Operatoren.** Jeder erzeugt Bytes, deren kanonische Neukodierung wieder die Saatbytes
ergibt, und die selbst von den Saatbytes verschieden sind. Greift ein Operator auf einer Saat
nicht, erzeugt er dort keine Zeile statt einer gleichen.

- **Reihenfolge.** Die Paare der obersten Map stehen in absteigender Schlüsselfolge. Alle Items
  bleiben minimal kodiert. Greift nur bei mehr als einem Schlüssel.
- **Map-Kopf indefinite.** Die oberste Map wird als indefinite-length geschrieben, mit Break am
  Ende. Der Inhalt bleibt unverändert.
- **Map-Kopf breiter.** Die Anzahl der Paare steht in einem breiteren Längenfeld als nötig.
- **Schlüsselköpfe breiter.** Jeder Schlüssel der obersten Map trägt einen breiteren Kopf als
  nötig. Ein einziger Mutant je Saat, nicht einer je Schlüssel.
- **Feldkopf breiter.** Der Kopf genau eines Feldwerts wird verbreitert, die übrigen bleiben
  minimal. Ein Mutant je Schlüssel und Saat, einschliesslich des Signaturfelds.

**Was "breiter" heisst.** Der Kopf eines Items trägt einen Major-Type und eine Additional
Information. Ist die Additional Information kleiner als 24, tritt an ihre Stelle der Wert 24 und
der ursprüngliche Wert folgt als ein Byte. Ist sie 24, tritt 25 an ihre Stelle und der Wert folgt
als zwei Bytes. Ist sie 25, tritt 26 an ihre Stelle und der Wert folgt als vier Bytes. Ist sie 26
oder 27, greift der Operator nicht. Auf Major-Type 7 greift er nicht, weil die Additional
Information dort keine Länge bezeichnet.

**3. Der Bestandstest wird nachgezogen.** `test_reject_codes_are_all_error_classes_minus_two_named`
in `tests/test_gitter.py` nimmt heute zwei Klassen aus. Mit Familie C ist nur noch
`FOREIGN_LIFECYCLE` unerreichbar, weil er einen Speicher braucht (D263, D268). Die
Ausnahmemenge und der Testname werden entsprechend angepasst; die Menge selbst bleibt aus
`ErrorCode` abgeleitet und wird nicht getippt.

**4. Zwei neue Tests in `tests/test_gitter.py`.**

- **Bauart.** Für jede Zeile mit Präfix `C` gilt: die kanonische Neukodierung ihres dekodierten
  Inhalts ist gleich den Bytes der zugehörigen Saat, und die Zeile selbst ist von diesen Bytes
  verschieden. Für jede Zeile ohne dieses Präfix gilt umgekehrt, dass sie bereits kanonisch ist.
- **Erreichbarkeit je Operator.** Zu jedem der fünf Operatornamen gibt es mindestens eine Zeile,
  und jede Zeile der Familie C wird vom Verdiktläufer mit `NON_CANONICAL_ENCODING` abgelehnt. Die
  Operatornamen kommen aus einer Konstanten des Moduls, nicht aus den Etiketten der Ausgabe.

## Nicht-Ziele

- **Keine Kombination mit Inhaltsmutationen.** D303 Beschluss 2 schliesst sie aus. Familie C setzt
  ausschliesslich auf der unveränderten Saat auf.
- **Keine Änderung an den Familien A und B.** Ihre Etiketten, ihre Reihenfolge und ihre Bytes
  bleiben gleich. Wird das verletzt, ist es zu melden, nicht zu reparieren.
- **Keine Änderung an `tools/korpus.py`, `tools/verdikt.py`, am Verifizierer, am Kodierer oder an
  einer Spec-Datei.**
- **Keine neuen Vektoren** in `tests/vectors/vectors_01.json` und kein neuer Abschnitt in Anhang C.
- **Kein Aufruf der Zweitfassung** aus dem Repo heraus (D293).
- Kein Rekursionsoperator innerhalb von Arrays oder Maps unterhalb der obersten Ebene.

## Abnahmekriterien

- `make check` läuft grün, ohne dass ein Bestandstest ausser dem unter Auftrag 3 genannten
  angefasst wurde.
- Die Zahl der Zeilen ohne Präfix `C` ist unverändert gegenüber dem Basis-Commit. Sie wird
  gemessen, nicht abgeschrieben: der Vergleich läuft gegen die Ausgabe von `tools/gitter.py` auf
  `5c8ce86`.
- Die beiden neuen Tests sind grün.
- Der Manifest-Aufruf und der Hex-Aufruf liefern weiterhin gleich viele Zeilen.

## Rücknahmeprobe

Zwei Proben, je mit dem Namen des roten Tests und seiner Meldung im Bericht (Prüfregel 60):

1. Familie C aus der Ausgabe entfernen. Erwartet rot: der unter Auftrag 3 nachgezogene Test, weil
   `NON_CANONICAL_ENCODING` dann in der erreichten Menge fehlt.
2. Die Bytes der Familie C vor der Ausgabe kanonisch neu kodieren. Erwartet rot: der Bauart-Test.
   Ein zusätzlich roter Test ist zu melden, nicht wegzunehmen.

Beide Proben werden zurückgenommen, bevor committet wird.

## Abschluss

Ein Commit auf `00al-familie-c`. Der Bericht enthält den vollständigen `git diff` gegen `5c8ce86`,
nicht nur `--numstat`, dazu die Ausgabe von `make check` und die beiden Rücknahmeproben mit
Testnamen. Widerspricht eine Messung diesem Prompt, wird sie gemeldet und nicht angepasst.
