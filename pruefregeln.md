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
Zusatz: dasselbe gilt für einen Satz, der einen älteren **ersetzt**. Wer eine Bedingung neu
formuliert, benennt zuerst den Geltungsbereich der alten und prüft ihn gegen den Code, der sie
umsetzt. In D165 wurde aus „die Kette von k ist an einem Punkt equivoziert" ein Satz über k
allein; der Code prüfte weiter jedes Kettenglied, und die Spec stand hinter ihm.

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

**23. Die Rücknahmeprobe setzt an der ungeschützten Seite an.** Behauptet ein Test die
Übereinstimmung zweier Orte, sind die Orte selten gleich bewacht. Wer für die Probe den Ort
anfasst, an dem schon ein anderer Test hängt, bekommt Rot aus fremder Ursache — die Probe sieht
bestätigt aus und beweist nichts. Vor jeder Probe steht daher die Frage: **was außer dem
geprüften Test könnte hier noch rot werden?** Die Antwort muss „nichts" sein. In D147 wurde
`genesis_res[9]` verändert; das ändert den Hash und schlug beim Bestandsanker `N_res` an, bevor
`resolve_trust_params` überhaupt lief. Die ungeschützte Seite war das `TrustParams`-Literal, das
an keinem Hash hängt. Unterschied zum Zusatz in Regel 21: dort ist die Probe **unmöglich**, hier
ist sie **zweideutig**.

**25. Die Begründung wird beim Beschluss geprüft, nicht beim Widerspruch.** Für jede Stelle, die
eine Begründung zitiert, wird gefragt, ob sie den Fall des Beschlusses regelt oder einen
benachbarten. D152 nannte einen Angriff, den der Einlesepfad ausschließt; D156 nannte einen
Paragraphen über fehlende Objekte für den Fall eines fehlenden Aufrufs. Beide Beschlüsse trugen,
beide Begründungen nicht, und beide fielen erst auf, als eine Messung widersprach. Eine ungeprüfte
Begründung sieht aus wie eine geprüfte (D158, D159, D160).

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

**27. Ein Verweis im Prompt wird aufgeschlagen.** Bevor ein Zeiger auf eine Spec-Stelle in einen
Prompt geht, wird die Stelle gelesen und geprüft, ob sie die Aussage trägt — auch und gerade
dann, wenn der Zeiger aus dem eigenen Register stammt. `04-golden-anchors.md §8` hat vier
Stationen durchlaufen: D170 nannte es als bessere Stelle, D171 ließ es stehen, der `00c`-Prompt
zitierte es, das Werkzeug führte es aus. Keine Station hat die Datei aufgeschlagen; §8 ist die
Invariantentabelle und sagt zu Vermerken nichts. Regel 22 trägt den Fall nicht — ein
Abschnittsverweis ist kein Bezeichner: er lässt sich nicht aus der Quelle übernehmen, sondern
nur gegen sie prüfen (D173).

**16. Wirkungsprüfung.** Bevor einem Befund eine Folge zugeschrieben wird, wird der falsche Wert
**bis zu seinem Verbraucher** verfolgt. Bei D135 war `Σ n_budget` ausgerechnet, aber nicht
weiterverfolgt; der erste Wirkungsabsatz behauptete die Gegenrichtung, weil `derive.py` Schritt 5
geflaggte Autoren autorweit ausschließt und nicht gruppenweit. Die Wirkung liegt nie dort, wo die
Zahl entsteht.

**24. Ein Nicht-Ziel, das eine beschlossene Norm verletzt, ist keines.** Vor jedem „keine
Änderung an X" im Prompt wird geprüft, ob eine Norm desselben Laufs X zwangsläufig bewegt. Steht
die Normänderung im selben Prompt wie das Verbot, sie nachzuziehen, hat das Werkzeug keinen
erfüllbaren Weg — und der einzige verbleibende ist der stille Umbau, den das Nicht-Ziel
verhindern sollte (D157, D160).

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

**26. Ein Hashtest hat ein Verfallsdatum.** Der Abgleich einer Projektkopie gegen das Repo gilt
für den Commit, an dem er gemacht wurde, und für keinen späteren. Jeder Merge, der eine Datei
anfasst, entwertet ihn — die Kopie sieht danach unverändert lesbar aus, und nichts wird rot. Vor
jeder Zählung, die in einen Prompt geht, wird gefragt: hat seit dem Abgleich ein Lauf diese Datei
berührt? In D169 hat der Supervisor `_policy(` in einer Kopie von vor dem `00b`-Merge gezählt und
sechs Aufrufstellen genannt, wo zehn standen; die vier fehlenden hatte `00b` selbst angelegt.

**28. Ein Abnahmekriterium behauptet einen Weltzustand.** Bevor ein Kriterium in einen Prompt
geht, wird nicht nur gefragt, ob die erwartete Aussage stimmen soll, sondern ob der Zustand, in
dem sie geprüft würde, überhaupt konstruierbar ist. Der Prüfgriff ist, ihn vor dem Schreiben zu
bauen: welche Claims, welche Objekte, welche Verfassung. Vier der neun Testfälle aus `00d`
behaupteten unmögliche Lagen — ein Objekt, das für den Übergang bekannt und für das Ergebnis
unbekannt ist; zwei Objekte unter einem Schlüssel; eine Rückwirkung, die überlappende
Teilnehmermengen ausschließen; der Widerruf eines Prädikats, das die Verfassung zwingend schützt.
Alle vier lasen sich schlüssig und alle vier waren vor dem Lauf entschieden.
Und: die Welt, die im Prompt steht, ist Feld für Feld die Welt, die gemessen wurde. In `00j` war
sie in der Designrunde richtig gebaut und ging beim Abschreiben verloren — die Feldliste nannte
Schwellen, Schlichter, `participants` und `nucleus_keys` und ließ `irrevocable_predicates` weg,
ohne die nach `04 §3.5` keine Auszählung evaluierbar ist. Konstruieren ist die eine Hälfte,
vollständig übertragen die andere.

**29. Ein Grep-Kriterium verbietet Namen.** Ein Abnahmekriterium der Form „`grep X` liefert null"
trifft nicht nur den Zustand, den es verbieten soll, sondern jede Zeichenkette, die `X` enthält. In
`00e` verlangte das Kriterium für `_is_nuc_name` null Treffer; ein Test namens
`test_is_nuc_name_...` hätte es rot gemacht, ohne dass etwas falsch gewesen wäre. Das Werkzeug hat
die Testnamen deshalb danach ausgerichtet und es gemeldet. Ein Kriterium, das die Namensgebung
lenkt, misst nicht mehr. Ein Grep-Kriterium wird so eng gefasst, dass nur der verbotene Zustand
hineinfällt: `def _is_nuc_name` statt `_is_nuc_name`.

**30. Eine Variantenwelt braucht eine Nullprobe.** Wer eine Welt baut, um darin genau ein Feld zu
verändern, baut sie zuerst mit **unverändertem** Feld und weist nach, dass sie die Referenzwelt
reproduziert — bei Claims claim-ID-genau. Ohne diese Nullprobe misst die Variantenmessung den
Bauapparat und nicht die Variante. In `00k` hat sie im ersten Messwert gefangen, dass beide Welten
aus denselben `Identity`-Objekten gebaut waren: `Identity` führt `h_prev` intern fort, die zweite
Welt zeigte auf Vorgänger, die in ihrem eigenen Speicher nicht liegen, ihre Stimmen waren nicht
`ACTIVE`, und der daraus gelesene Befund war ein Artefakt des Baus.

**31. Der Vergleichspunkt eines Laufs ist der Prompt-Commit.** Ein Abnahmekriterium über einen
Diff nennt den Commit, auf dem der Prompt liegt, nicht den Registercommit darunter. Der Prompt ist
selbst eine Datei im Wurzelverzeichnis und erscheint sonst in genau dem Diff, den er beschreibt.
In `00k` setzte der Supervisor `32c55c9` als Basis, obwohl der Prompt auf `2a02104` lag, und maß
das Kriterium „genau fünf Dateien" gegen sechs; das Werkzeug hat es gemeldet und nichts
nachgezogen. Die Regel stand seit langem in der dauerhaften Anweisung und in jedem Sitzungsstart,
war aber nicht nummeriert — und was hier nicht steht, wird beim Schreiben eines Prompts nicht
geprüft. Dieselbe Begründung wie bei den Nummern 8 und 9 in D144.

**32. Wo eine Prüfung sitzt, ist eine eigene Gabel.** Steht fest, dass geprüft werden soll, ist die
Stelle damit nicht entschieden. Die Gegenprobe wird an jeder plausiblen Stelle gebaut, und
verglichen werden die **erzeugten Aussagen**, nicht die Zahl der gefallenen Tests. In D200 kosteten
alle drei Varianten genau einen Test; die Wahl fiel erst, als die Vermerke nebeneinander lagen und
zwei Varianten `UNEVALUABLE` meldeten, wo `PASSED` gemessen war.

**33. Der Prompt wird gegen den Spec-Satz gelesen, den er umsetzt.** Prüfregel 27 verlangt, dass
ein Verweis die behauptete Aussage trägt. Das genügt nicht: der Verweis kann stimmen und die
Anweisung daneben liegen. In `00m` zitierte der Prompt `04 §4.1` richtig und schrieb den
ValueError-Wächter trotzdem hinter die Bedingungen 1 bis 5, wo die Spec ihn an keine Bedingung
knüpft. Das Werkzeug hat den Prompt korrekt umgesetzt, und der Defekt wurde erst in der Abnahme
sichtbar. Wo ein Prompt eine Reihenfolge oder einen Ort festlegt, wird der Spec-Satz danebengelegt,
nicht nur aufgeschlagen.

**34. Eine Rücknahmeprobe, die eine Prüfung entfernt, belegt nicht ihren Ort.** Wer eine Prüfung an
eine bestimmte Stelle setzt, nimmt sie in der Probe nicht heraus, sondern **verschiebt** sie an die
verworfene Stelle. In `00m` fielen bei entfernter Prüfung beide Fälle rot, bei verschobener nur der
neue — und erst das zeigte, dass der ältere die Stelle nie gehalten hat. Dieselbe Begründung wie
bei Prüfregel 23: die Probe muss die unbewachte Seite treffen.

**35. Eine Grenze auf zwei Schichten braucht auf jeder einen Wächter.** Wird ein Verhalten von zwei
Stellen zugleich erzwungen, hält ein Prüffall auf der äusseren die innere nicht: die Probe an der
inneren Stelle bleibt grün, weil die äussere das Ergebnis ohnehin verwirft. In D203 blieb der
Kettentest grün, als die Weitergabe auf den tragenden Pfad von `§4.1` gelegt wurde, weil
`resolve_epoch` dessen Vermerke gar nicht liest. Wer eine Grenze prüft, misst zuerst, wie viele
Stellen sie halten.

**36. Eine neue Behauptung wird danach eingeordnet, was sie hinzufügt: Erkennung oder Adresse.**
Gemessen wird das, indem die Welt falsch gemacht und die Rotmenge mit und ohne die neue Behauptung
verglichen wird. Sind beide gleich, kommt keine Erkennung hinzu, sondern eine bessere Auskunft.
Das ist ein zulässiger Zweck, aber ein anderer, und der Registereintrag sagt welchen. In D205 waren
die Rotmengen identisch — ein falsches `n` bricht ohnehin jeden Vertrauenswert; was die neuen
Behauptungen halten, ist die Übertragung der Ankertabelle in den Test.

**37. Die Basis eines Laufs ist der Commit, der den Prompt enthält.**
Ein Prompt, der geschrieben wird, bevor er committet ist, kann seine eigene Basis nicht nennen; wer
den Registercommit darunter einträgt, lässt den Lauf an einem Punkt verzweigen, an dem der Prompt
noch nicht existiert. Die Abnahme bleibt davon oft unberührt, der Merge nicht: ein Fast-Forward
setzt voraus, dass die Zielspitze der Branchpunkt ist, und das ist bei dieser Reihenfolge nie
gegeben. Deshalb wird der Prompt zuerst committet und die Basis danach eingetragen. In `00q` fiel
es erst beim Merge auf (D208).

**38. Eine Position wird erst bezogen, nachdem der zuständige Abschnitt aufgeschlagen ist.**
Prüfregel 27 verlangt das Aufschlagen vor dem Prompt, Prüfregel 33 das Danebenlegen des Spec-Satzes.
Beide greifen zu spät: entschieden wird, wenn eine Position auf eine Gabel bezogen wird, und das
geschieht davor. Wer eine Lage für ungeklärt hält, schlägt zuerst nach, wer sie schon geklärt hat —
`tools/register_index.py` nennt die Einträge zu einem Abschnitt. In der Sitzung zu D207 wurden drei
von vier Positionen zurückgenommen, jede davon gegen eine Entscheidung, die es bereits gab (D209).

**39. Eine Ausgabe ist keine Bedingung.**
In einer `and`-Kette entscheidet der Rückgabewert, nicht der gedruckte Text. `git branch
--show-current`, `git log` und `grep -c` liefern Status 0, auch wenn sie das Falsche zeigen; wer
einen Zustand sichern will, braucht `test`, `--is-ancestor`, `--quiet` oder `-c` mit Vergleich. In
`00r` galt eine Branchausgabe als Prüfung, und der Lauf-Commit landete auf `main` (D211).

**40. Der erwartete Kopf des nächsten Blocks wird abgeleitet, nicht erinnert.**
Was ein Block hinterlässt, steht im Block, nicht im zuletzt gesehenen Hash. Ein Block, der
committet und nicht pusht, lässt `main` und `origin/main` auseinanderlaufen; ein Block, der einen
Branch anlegt, lässt `main` stehen; ein Übergabe-Commit hebt den Kopf über den Stand, auf dem die
eigene Kopie steht. Wer im nächsten Zug `test (git rev-parse HEAD ...) = <hash>` schreibt, ohne
diesen Zustand gemessen zu haben, hält die Kette auf einer Zahl an, die nie galt — und der
Operator zahlt einen Zug für einen Fehler, der keiner war. Liegt kein gemessener Hash vor, wird
die **Beziehung** geprüft: `git rev-parse main` gegen `impl/00x^`, `--is-ancestor`, oder
`origin/main` statt `main`. In `00s` zweimal gerissen (D214).

**41. Die Vorabvariante ist Erwartungsquelle, nicht Vorbild.**
Eine vollständig gebaute Variante liefert die Zahlen, gegen die abgenommen wird — sie bindet das
Werkzeug nicht. Weicht der Lauf ab, wird die Abweichung zuerst gegen den **Prompt** geprüft und
erst danach gegen die Variante; deckt der Prompt das ab, was das Werkzeug gebaut hat, ist die
Variante der Fehler und nicht der Lauf. In `00t` zählte die Variante alle Python-Befunde als
einen, der Prompt verlangte die Zählung je Datei, und die vier Zeilen Abweichung waren die
Reparatur (D217).

**42. Der Assert eines Splices prüft das Ergebnis, nicht den eingesetzten Text.**
Ein Splice, der eine Länge, eine Anzahl oder eine Form zusichert, misst sie an der Datei, wie sie
nach dem Schreiben aussieht — nicht am Block, den er einsetzt. Der Unterschied ist nicht
theoretisch: eine Ersetzung mitten in einem Absatz kann jede Zusicherung des eingesetzten Textes
erfüllen und die Zeile daneben auf das Doppelte der Grenze bringen (D223).

---

## Herkunft der Nummern

Die Regeln 1–7 stammen aus `sitzungsstart-05.md`, 10–12 aus `sitzungsstart-anwendung.md`, 13–15
aus `sitzungsstart-einlesepfad.md`, 16–18 aus `sitzungsstart-buchfuehrung.md`, 19 aus
`sitzungsstart-kollision.md`, 20 aus `sitzungsstart-decke.md`, 21 aus D142, 22 aus D146, 23 aus
D148, 24 und 25 aus D160, 26 aus D169, 27 aus D173, 28 aus D179, 29 aus D184,
30 aus D192, 31 aus D196, 32 aus D200, 33 und 34 aus D201, 35 aus D203, 36 aus D205,
37 aus D208, 38 aus D209, 39 aus D211, 40 aus D214, 41 aus D217, 42 aus D223.

Die Nummern **8** und **9** wurden in D144 vergeben. Parallelenprüfung und Begründungsprüfung
liefen bis dahin unnummeriert als „die beiden älteren" mit; ohne Nummer waren sie in Prompts
nicht zitierbar.
