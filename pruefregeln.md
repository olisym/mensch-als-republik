# Prüfregeln

Die Regeln, nach denen in MaR geprüft wird. Sie sind aus Befunden entstanden, nicht aus
Prinzipien: jede steht hier, weil ihr Fehlen einmal einen Defekt durchgelassen hat. Wo eine
Regel aus einem Registereintrag stammt, ist er genannt.

Diese Datei ist der **einzige** Ort ihres Volltextes. Bis D144 standen sie verteilt über sechs
abgelöste `sitzungsstart-*.md`; ein `sitzungsstart` verweist auf diese Datei, er wiederholt sie
nicht.

Geordnet nach dem Zeitpunkt, an dem sie greifen.

---

## Beim Entwerfen

**1. Vor dem Schreiben rechnen.** Jede Zahl, die aus einer Regel folgt, wird gerechnet, bevor sie
geschrieben wird — nicht danach geprüft. Eine Eigenschaft so genau zu formulieren, dass eine
Maschine sie angreifen kann, ist selbst die Prüfung.

**2. Standprüfung.** Vor jedem Mechanismus zu Nebenläufigkeit, Ordnung oder Schwellen fragen,
unter welchem Namen das Problem außerhalb des Projekts gelöst ist. CALM und ein Raft-Befund haben
je einen eigenen Vorschlag widerlegt (D96, D102).

**15. Literaturprüfung vor der Entscheidung.** Bei jedem Fork, der außerhalb von MaR seit Jahren
bearbeitet wird, zuerst nachsehen, was dort gefunden wurde. D124 (did:plc, Keybase, CONIKS,
Nostr, SSB), D125 (TUF), D127 (Test-Doubles, ALICE, ARIES) sind so entschieden worden — und in
zwei Fällen billiger und schärfer, als eine eigene Analyse geworden wäre.

## Beim Definieren von Typen und Feldern

**3. Feldinventur.** Für jedes Feld eines Schemas benennen, welche Funktion es liest. Felder ohne
Leser sind zu streichen oder als deklarativ zu kennzeichnen (D114).

**4. Zugehörigkeitsliste am Datentyp.** Welche Felder eine Zugehörigkeit behaupten und wogegen sie
zu prüfen sind, wird bei der **Definition** des Typs aufgeschrieben (D112).

**10. Leserprüfung.** Trägt ein normativer Satz eine Pflicht an den *Autor* von Claims, wird bei
seiner Formulierung benannt, welche Funktion die Erfüllung liest. Gibt es keine, ist der Satz auf
SOLL zurückzunehmen oder mit einem Vermerk zu versehen (D119). Die Feldinventur fragt nach dem
Leser eines Feldes; diese Regel nach dem Leser einer Pflicht. `02 §6.2` hat zwei Layer
überdauert, weil seine einzige Wirkung war, dass ein wohlerzogener Autor etwas unterließ.

## Beim Formulieren normativen Textes

**9. Begründungsprüfung.** Ist eine Begründung an einen einzelnen Fehlermodus gebunden, und gibt
es einen zweiten? D77, D83, D87 und D91 sind alle aus Begründungen entstanden, die beim Wandern
still ihren Geltungsbereich verloren haben.

**11. Geschwisterformel.** Ein Verbot, das mit „an welcher Stelle auch immer" endet, fängt
Geschwister, die eine Aufzählung nicht kennt — billiger als eine vollständige Liste. Der Schnitt
in D122 nannte einen Helfer; das Verbot hat fünf gefunden.

**18. Aufzählung gegen Satz.** Steht in einer Spec eine Bedingung als Satz **und** als
ausgerechnete Aufzählung, gilt der Satz, und die Aufzählung wird als abgeleitet markiert (so in
`02a §2.6`). Aufzählungen verlieren beim Wandern still ihren Geltungsbereich — D77, D83, D87,
D91, D130, D135 sind alle diese Form. Ein allgemeiner Satz erbt den Geltungsbereich der
Aufzählung, die ihm vorausgeht; Prosabedingungen gehen abgeleiteten Aufzählungen vor.

**20. Kostenaussage braucht Kostenmodell.** Ein Satz, der etwas „billig", „teuer" oder „ohnehin
unattraktiv" nennt, ist eine Aussage über Angriffskosten. Steht in der Spec kein Kostenmodell,
das ihn trägt, fällt der Satz — auch und gerade dann, wenn der Satz daneben bewiesen ist. Ein
bewiesener Nachbar macht eine unbelegte Behauptung nicht wahr, er macht sie nur schwerer
sichtbar (D139).

**21. Eine Kapazität ist eine Schranke, kein Ertrag.** Wer eine Kapazität in eine Bilanz
einsetzt, muss den Weg rechnen, den der Fluss zu ihr nimmt. `Σ C(h)` ist eine Obergrenze, kein
Aufkommen; `cap(p → h)` ist eine Ausgangsschranke, kein Beitrag, wenn `p` weniger empfängt.
D139, D141 und D142 sind dreimal dieselbe Verwechslung. Zusatz: ein Term, den die Spec als
redundant beweist, kann von keiner Rücknahmeprobe rot gefärbt werden — eine Probe, die ihn
treffen soll, ist falsch gebaut (D142).

## Beim Prüfen von Code und Spec nebeneinander

**8. Parallelenprüfung.** Zwei Stellen, die dasselbe tun, werden nebeneinandergelegt —
Eingangsbedingungen, Fehlertypen, Diagnosen. Sequenzielles Lesen findet Asymmetrien nicht.

**17. Prompt-Dateien sind normativer Text, solange Code auf sie zeigt.** Die Parallelenprüfung
gilt nicht nur für Layer-Dateien. `02a-maxflow-prompt.md` trug Befund und Widerlegung **neun
Zeilen** voneinander entfernt: eine Aufzählung, die `EQUIVOCATION_FLAGGED` wegließ, direkt über
dem Satz, ein Vouch verlasse das Budget-Set ausschließlich durch `t_exp`. Der Code folgte der
Aufzählung. Ein Verweis auf gelöschten Text ist normativer Text ohne Quelle.

**5. Ausgänge aufzählen.** Wo eine Invariante einen Zustandsübergang ausschließt, werden **alle**
Ausgänge aus dem Zustand aufgezählt — aus dem Code, nicht aus dem Gedächtnis (D117).

**14. Zählregel.** Eine Aufzählung von Fundstellen wird **gegrept, nicht gelesen**. D119 nannte
zuerst einen Erzeuger, es waren drei. D127 nannte vier Kettenfortführungen, es waren fünf. D146
nannte einen Importeur von `_tally`, es waren zwei. Jedes Mal stimmte die Begründung und die Zahl
nicht.

**Ein Limit, das exakt erreicht wird, ist ein Nulltreffer.** Gibt `head -n` genau `n` Zeilen
zurück, sagt die Ausgabe nichts über das, was jenseits liegt — ein abgeschnittener Grep ist kein
Grep. Wer etwas verschiebt, greppt die Verwender, statt sie zu erinnern.

**22. Ein Bezeichner im Prompt ist ein Zitat.** Namen, Signaturen und Argumentlisten, die in
einen Prompt gehen, werden aus der Quelle übernommen, nicht aus dem Gelesenen rekonstruiert. In
D145 stand `passed()` im Prompt, weil der Rumpf der Funktion gelesen und ihre `def`-Zeile ergänzt
worden war; sie heißt `reached()`. Regel 14 trägt diesen Fall nicht — er ist keine Aufzählung,
sondern eine einzelne Angabe, und **gelesen** und **vollständig gelesen** sehen bei einem
Funktionsrumpf gleich aus.

**16. Wirkungsprüfung.** Bevor einem Befund eine Folge zugeschrieben wird, wird der falsche Wert
**bis zu seinem Verbraucher** verfolgt. Bei D135 war `Σ n_budget` ausgerechnet, aber nicht
weiterverfolgt; der erste Wirkungsabsatz behauptete die Gegenrichtung, weil `derive.py` Schritt 5
geflaggte Autoren autorweit ausschließt und nicht gruppenweit. Die Wirkung liegt nie dort, wo die
Zahl entsteht.

## Beim Ändern von Reihenfolgen und Stufen

**6. Monotonie stufenweise.** Eine Monotonieaussage gilt zunächst nur für die letzte Stufe. Jede
Stufe davor wird einzeln geprüft (D118).

**7. Abhängigkeitssatz bei Reihenfolgeänderungen.** Wird eine Reihenfolge geändert, wird für jede
Größe, die in der alten nebenbei entstand, benannt, woher sie in der neuen kommt (D113).

## Beim Bauen und Lesen von Tests

**12. Zwei Läufe, eine Variable.** Um zu zeigen, dass ein Mechanismus erreicht wird oder
wirkungslos ist, zwei Läufe über derselben Menge vergleichen, die sich in genau einer Größe
unterscheiden. Eine Bedingung zu prüfen, die auch andere Ursachen erfüllen könnten, ist schwächer
— und liest sich gleich.

**13. Neustart als Annahme.** Modelliert ein Test einen Neustart, wird gefragt, ob dieselbe
Ursache auch **ohne** Neustart eintreten kann. Wenn ja, ist der Weiterlauf ein eigener Vektor und
keine Variante. Die Absturzaufzählung in D128 konnte B-1 strukturell nicht sehen, weil jeder
ihrer Läufe nach dem Bruch ein frisches Objekt baute.

**19. Kalte Messung.** Ein grüner Testlauf auf der Arbeitskopie ist keine Aussage über den
Commit. Zustand außerhalb von git — `.hypothesis/`, `__pycache__`, warme Caches — wird vor jeder
Behauptung über `main` gelöscht. `make check-all` führt `check_tree.py` und hat damit ein Tor
gegen vergessene **Dateien**; gegen vergessene **Zustände** gibt es keines. Genau darin lag D137.

---

## Herkunft der Nummern

Die Regeln 1–7 stammen aus `sitzungsstart-05.md`, 10–12 aus `sitzungsstart-anwendung.md`, 13–15
aus `sitzungsstart-einlesepfad.md`, 16–18 aus `sitzungsstart-buchfuehrung.md`, 19 aus
`sitzungsstart-kollision.md`, 20 aus `sitzungsstart-decke.md`, 21 aus D142, 22 aus D146.

Die Nummern **8** und **9** wurden in D144 vergeben. Parallelenprüfung und Begründungsprüfung
liefen bis dahin unnummeriert als „die beiden älteren" mit; ohne Nummer waren sie in Prompts
nicht zitierbar.
