# Prompt 00aq — Nachtrag: Wortgrenzen und die sechste Kaltzahl

## Branch und Basis

Weiter auf `00aq-werkzeuge`, Basis für diesen Nachtrag ist `be6afcb`. **Ein zweiter Commit** auf
demselben Branch. Kein Merge, kein Push.

Der Lauf ist abgenommen (D318). Was hier steht, sind zwei Defektbehebungen, keine neuen Aufträge.

## Normative Grundlage

- **D318** — Abnahme, der Defekt, und der Beschluss über die sechs Kaltzahlen.
- **D209** — `tools/register_index.py` trägt den Schutz, um den es in Auftrag 1 geht.
- **D224** — Teil 1 und Teil 3 bleiben unberührt.

## Auftrag 1 — Nennungen dürfen nicht in Wortmitten greifen

In `tools/offen.py` findet der Ausdruck für Nennungen einen grossen Buchstaben O unmittelbar vor
einer Ziffernfolge auch dann, wenn ihm ein Buchstabe oder eine Ziffer unmittelbar vorausgeht. Eine
Normbezeichnung oder eine Summenformel wird damit als Postennummer gelesen.

**Zu tun, in Prosa:** eine Nennung zählt nur dann, wenn dem grossen O **kein** Buchstabe und
**keine** Ziffer unmittelbar vorausgeht. `tools/register_index.py` löst dieselbe Aufgabe für
Verweise und ist die Vorlage; die dortige Bedingung wird übernommen, nicht neu erfunden.

Die Kopfzeilenerkennung bleibt unverändert — sie ist bereits am Zeilenanfang verankert.

**Zwei Tests** in der bestehenden Testdatei, beide gegen erzeugten Text:

1. Ein Text, der eine Kennung aus Buchstaben und Ziffern enthält, deren vorletztes Zeichen ein
   grosses O ist und deren Ziffernteil keiner Postennummer entspricht, ergibt **keine** Nennung.
2. Ein Text, in dem dieselbe Ziffernfolge einmal als echte Nennung und einmal in einer Wortmitte
   steht, ergibt **genau eine** Nennung.

Die erwarteten Werte werden aus dem erzeugten Text abgeleitet, nicht getippt.

**Eine Rücknahmeprobe:** die Bedingung wieder entfernen und bestätigen, dass mindestens einer der
beiden neuen Tests rot wird. Die Rücknahme wird nicht committet; gemeldet wird, welcher Test fiel.

## Auftrag 2 — `tools/stand.py` trägt sechs Zahlen

D318 legt fest: Commit, Testzahl, Registerstand, Prüfregelzahl, Postenzahl, Branchzahl.

**Zu tun:**

1. Die **Branchzahl** aufnehmen. Sie wird über einen Aufruf von git ermittelt, mit derselben
   Fehlerbehandlung wie der Kurzhash: schlägt der Aufruf fehl, endet das Werkzeug mit Status 1
   und ohne Ausgabezeile. Gezählt wird die Menge, die `git branch -a` nennt — die Zahl schliesst
   die beiden Fernverweise ein, und das ist die in `arbeitsweise.md` festgehaltene Vorschrift.
2. Die **Zahl der Markdown-Dateien der Wurzel** entfernen. Sie ist nach D318 keine Kaltzahl.

Die Reihenfolge in der Ausgabezeile folgt der Aufzählung in D318. Die Zeile bleibt eine Zeile.

## Nicht-Ziele

- Keine Änderung an `tools/check_specs.py`, am Makefile, an `offen.md` oder an `arbeitsweise.md`.
- Keine Änderung an der Kopfzeilenerkennung in `tools/offen.py`.
- Keine weiteren Zahlen in `tools/stand.py`, auch keine, die sich anbieten.
- Kein Merge, kein Push.

## Abnahmekriterien

1. `make check` läuft grün durch.
2. Ein Text mit einer Kennung, deren vorletztes Zeichen ein grosses O ist, ergibt keine Nennung.
   Zwei Beispiele werden gefahren und ihre Ausgabe gemeldet.
3. Die Rücknahmeprobe aus Auftrag 1 war rot; gemeldet wird, welcher Test fiel.
4. `tools/stand.py` gegen eine gespeicherte Testausgabe liefert eine Zeile mit sechs Werten.
5. Der zweite Lauf von `tools/offen.py` gegen die unveränderte Datei liefert dieselbe Zahl wie
   der erste.

## Abschluss

Ein zweiter Commit auf `00aq-werkzeuge`. Der Bericht enthält den **vollständigen** `git diff`
gegen `be6afcb`, nicht gegen den Branchpunkt, sowie die Ausgaben zu den Punkten 2 bis 5.

Widerspricht eine Messung diesem Nachtrag, wird sie **gemeldet, nicht angepasst**.
## Auftrag 3 — Nachtrag: der zweite Test unterscheidet nicht

`test_real_mention_beside_midword_is_one` benutzt für die echte Nennung und für die Wortmitte
**dieselbe** Ziffernfolge. Da `mentioned_numbers` eine Menge liefert, kollabieren beide Treffer
auf einen Wert, und der Test bleibt auch ohne den Schutz grün. Der Supervisor hat das
unabhängig nachgerechnet und bestätigt; die Meldung des Werkzeugs war richtig.

Der Fehler liegt im Prompt, nicht im Bau. Ein Regressionstest, der die Regression nicht sieht,
ist keiner.

**Zu tun:** die echte Nennung und die Wortmitte tragen **verschiedene** Ziffernfolgen. Die Zahl
der Wortmitte darf keiner Postennummer entsprechen. Geprüft wird, dass die Menge genau die Zahl
der echten Nennung enthält und die Zahl aus der Wortmitte **nicht**. Beide Werte werden aus dem
erzeugten Text abgeleitet, nicht getippt.

Der erste Test bleibt unverändert; er unterscheidet bereits.

**Rücknahmeprobe:** den Schutz erneut entfernen und bestätigen, dass jetzt **beide** Tests rot
werden. Die Rücknahme wird nicht committet.

**Nicht-Ziele:** keine Änderung an `tools/offen.py`, an `tools/stand.py`, am Makefile oder an
den übrigen Tests. Kein Merge, kein Push.

**Abnahme:** `make check` grün; die Testzahl steigt nicht, weil kein Test hinzukommt; die
Rücknahmeprobe nennt beide gefallenen Tests namentlich.

**Abschluss:** ein dritter Commit auf `00aq-werkzeuge`, mit dem vollständigen `git diff` gegen
`bfe01fa`.
