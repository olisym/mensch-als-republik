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

---

## Herkunft der Nummern

Die Regeln 1–7 stammen aus `sitzungsstart-05.md`, 10–12 aus `sitzungsstart-anwendung.md`, 13–15
aus `sitzungsstart-einlesepfad.md`, 16–18 aus `sitzungsstart-buchfuehrung.md`, 19 aus
`sitzungsstart-kollision.md`, 20 aus `sitzungsstart-decke.md`, 21 aus D142, 22 aus D146, 23 aus
D148, 24 und 25 aus D160, 26 aus D169, 27 aus D173, 28 aus D179, 29 aus D184,
30 aus D192.

Die Nummern **8** und **9** wurden in D144 vergeben. Parallelenprüfung und Begründungsprüfung
liefen bis dahin unnummeriert als „die beiden älteren" mit; ohne Nummer waren sie in Prompts
nicht zitierbar.
