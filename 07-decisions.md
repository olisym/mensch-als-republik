# Entscheidungs-Register — Session 2026-08-10

Status: beschlossen · Protokollversion: 1 · Betroffene Layer: 00, 02, 04, 05, 06, VISION

Dieses Dokument ist ein **Register**, keine Spezifikation. Die normative Wahrheit bleibt in
`00`–`06`. Hier steht, *welche* Änderungen an diesen Dateien vorzunehmen sind und *warum* —
inklusive der explizit verworfenen Alternativen, damit sie nicht in einer späteren Sitzung
erneut als Neuvorschlag auftauchen.

Auslöser: die Frage, ob ein akkumuliertes Reputationsguthaben einen Anreiz zur Defektion
erzeugt („Sünden-Puffer"). Antwort: in Layer 02 nein (Vertrauen ist positional), in Layer 05
ja (Beta-Reputation ist ein Konto). Aus der Analyse sind 26 Entscheidungen gefolgt, davon
eine **Korrektur eines fehlerhaften Satzes in `02 §4`** (→ D6).

---

## Leitprinzipien der Sitzung

**L1 — Das Protokoll beantwortet keine Wertfragen, es macht sie entscheidbar.**
Wohlfahrts-, Solidaritäts- und Aufnahmemodelle sind Nukleus-Policy, nie Protokoll. Das
Protokoll liefert verifizierbare Reziprozitätshistorie, lokale Bewertung und funktionierenden
Exit; welches Verhalten als Beitrag zählt, entscheidet jeder Nukleus für sich. Der Markt der
Gesellschaftssysteme (`VISION §3`) ist der Selektionsmechanismus, nicht die Spec.

**L2 — Nicht verhindern, sondern sichtbar und bepreisbar machen.**
„detect-not-prevent", ausgeweitet auf Urteilsverzerrung, Kollusion und Machtkonzentration.
Ein systematisch voreingenommener Schiedsrichter wird nicht ausgeschlossen — seine
Verdikt-Historie wird auditierbar, und wer das Muster erkennt, senkt sein Gewicht.

**L3 — Downside-only.**
`02 §6.1` sagt über den Bond: „der Ehrliche gewinnt nichts, nur der Defektor verliert."
Dasselbe gilt für Bürgschaft (D18), Standing (D10) und `w` (D1). Man darf sich selbst
schlechter stellen, nie besser. Jeder Vorschlag, der eine positive Prämie einführt, ist
gegen dieses Prinzip zu prüfen.

**L4 — Begrenzte Voraussicht wird durch Exit getragen, nicht durch Vollständigkeit.**
Wir sitzen in derselben Position wie jeder Verfassungsgeber und denken nur an die Fälle, die
wir uns vorstellen können. Der Unterschied ist nicht größere Klugheit, sondern dass eine
verlassbare Ordnung nicht alle Fälle vorhersehen muss — sie muss überlebbar falsch sein
können. Daraus folgt: im Protokoll so wenig wie möglich fixieren.

---

## A. Kapazitätsmodell und Bürgschaft (Layer 02)

### D10 — Leitsatz: Vertrauen ist Zustand, kein Vermögen

Neu in `02 §1`. `C(x) = C₀·γ^{d(s,x)}` ist rein **positional** — durch Wohlverhalten lässt sich
kein höheres `C` erarbeiten. `t_s` ist ein Zustand des aktuellen Kantensets, kein Integral über
die Vergangenheit. Nicht akkumulierbar, nicht hortbar, nicht übertragbar. Damit existiert kein
Guthaben, das als Sünden-Puffer dienen könnte.

Diese Eigenschaft ist tragend, war aber nirgends benannt.

### D1 — Vouch-Gewicht `w` als Kanten-Obergrenze

Die Vouch-Kante `I_out → J_in` erhält Kapazität **`w · C(I)`** statt ∞.

```
w ∈ (0, 1]     Default w = 1
```

Bei `w = 1` identisch zum bisherigen Spec-Stand (die interne Knotenkante `C(I)` bleibt der
bindende Engpass). Untagged Vouches ⇒ `w = 1`.

**Warum Obergrenze und nicht Anteil:** Der Cap einer Kante hängt **nur von dieser Kante** ab.
Keine Kopplung an andere Kanten ⇒ neue Kanten können bestehende nie anheben ⇒ die Monotonie
aus `02 §7` bleibt erhalten (fehlendes Wissen senkt nur).

**Wirkung auf den Beweis in `02 §4`:** Das Argument „alle Vouch-Kanten haben ∞, also durchtrennt
kein Min-Cut sie" gilt nicht mehr. Die Schranke hält trotzdem — Kapazitätssenkung kann Max-Flow
nur senken. Ein Zusatzsatz, kein Beweisumbau.

### D2 — `w` als Rational mit nukleus-festem Nenner

```
w = n / D      n ∈ [1, D],  D = Nukleus-Policy,  Default n = D
Kantenkapazität = ⌊ n · C(I) / D ⌋
```

Abrunden ist die sichere Richtung (Unter-Vertrauen). Erhält die exakte Integer-Arithmetik der
harten Sicht; byte-reproduzierbar über Implementierungen hinweg.

**Verworfen:** Float (bricht Exaktheit). Festes Enum `{¼,½,¾,1}` (willkürlich granular).
Absoluter Integer-Cap (bricht die `C₀`-Skaleninvarianz aus `02 §8`).

### D3 — `Σw ≤ 1` als Selbstbindungsbudget

```
Für jede Identität I und Scope N:   Σ wᵢ ≤ 1
                                    über alle budget-bindenden ausgehenden Vouches von I
```

Bürgschaft wird knapp, weil sie **bindet**, nicht weil sie gezählt wird. Eine Bürgschaft für `X`
bindet Kapazität, die im Defektionsfall von `X` beim Bürgen haftet (→ D5).

**Ersetzt den zuvor erwogenen Out-Degree-Cap `k`.** Ein Zähler wäre eine willkürliche
Rationierung ohne ökonomische Begründung — und inkonsistent, solange unbegrenztes Bürgen keine
Haftung erzeugt. Die Bindung ist ein Preis, der Zähler war nur eine Grenze.

**Monotonie:** Die Budgetregel ist eine Gültigkeitsbedingung über dem Aktiv-Set, **keine
Normalisierung**. Bei Teilwissen ist das beobachtete `Σw` zu klein ⇒ eine Verletzung wird
möglicherweise **nicht erkannt**, aber nie eine erfunden. Teilwissen erzeugt Unter-Erkennung,
nie Falschbeschuldigung.

**Marktwirkung:** Bürgschaft wird zum Portfolio-Problem — `0.5` auf einen langjährigen Partner
oder `10 × 0.05` auf Neulinge? Sicherheit oder Reichweite? Preisbildung ohne eine einzige
Preisangabe im Protokoll, allein aus Knappheit plus Haftung.

### D4 — Über-Commitment ist ein selbst-validierender Fehler

`n` signierte Vouches derselben Identität mit `Σw > 1` im selben Scope sind ein unabhängig
nachrechenbarer Beweis — dieselbe Klasse wie Equivocation (Atom-Spec §4). **Mechanisch
slashbar, kein Verdikt nötig.** Kein neuer Beweistyp, keine neue Propagationsklasse.

### D5 — `w` wirkt dreifach

| Wirkung | Formel | Bedeutung |
|---|---|---|
| Durchsatz | Kante erhält `w · C(I)` | wie viel Vertrauen `I` weiterreicht |
| Knappheit | `Σw ≤ 1` | dass es begrenzt ist |
| Haftung | Defektion von `J` schlägt anteilig `w` auf `I` durch | was es `I` kostet |

Ein Parameter, drei gleichgerichtete Wirkungen. **Die Deklaration ist der Einsatz** — hohes
Vertrauen lässt sich nicht billig behaupten. Kein separater Ehrlichkeitsmechanismus nötig.
Konkretisiert `05 §6` („individuelle Haftung, eine Sprunghöhe"), das die Höhe offenließ.

### D5a — Haftungsdurchreichung nur bei selbst-validierenden Beweisen

- **Equivocation / Über-Commitment von `J`** ⇒ mechanischer Durchgriff `w · Schaden` auf `I`.
- **Subjektives Verdikt gegen `J`** ⇒ **kein** Bond-Slash beim Bürgen; nur Reputationswirkung
  (Enf-Spec Stufe 1).

Andernfalls haftete `I` für ein Urteil, an dem er nicht beteiligt war, und die Bürgschaft würde
zum Diffamierungshebel gegen den Bürgen — gegen die Schutzlogik von `05 §5`.

### D17 — Laufzeit, Widerruf und Freigabe

```
Widerruf   ⇒ Fluss stoppt sofort (Kante verlässt das Aktiv-Set)
           ⇒ Haftung endet
           ⇒ Budget bleibt gebunden bis t_exp
t_exp      ⇒ Budget wird frei
```

**Zwei Uhren, nicht eine.** Budget ist vorwärtsgerichtet (welche Kapazität kann ich künftig
binden?), Haftung rückwärtsgerichtet (wofür stehe ich ein?). Sie zusammenzulegen war der
ursprüngliche Fehler.

**Warum keine Nachhaftungsfrist:** Sie bräuchte „Defektion innerhalb Δ nach Widerruf", also eine
Cross-Chain-Zeitordnung, die MaR verweigert (`06` VR-06.3). `t_exp` wird lokal gegen `now`
ausgewertet und ist bereits gebaut.

**Warum Haftungsende beim Widerruf (Variante ii statt i):** Haftung bis `t_exp` wäre
unverhältnismäßig — man haftete für jemanden, von dem man sich vor 19 Monaten öffentlich
losgesagt hat — und würde alle `t_exp` nach unten drücken, also genau die langen Laufzeiten
entwerten, die das stärkste Signal tragen.

**Restfenster, bewusst getragen:** Ein Kollusions-Bürge kann kurz vor der Defektion seines
Komplizen widerrufen und der Haftung entgehen. Bepreist ist das durch den Verlust der gesamten
Bürgschaftskapazität für die Restlaufzeit — nicht über eine neue Identität rückholbar, weil
Standing positional ist (D10). Zusätzlich wird der Widerruf selbst zum sichtbaren Signal:
Ein Bürge, dessen Widerrufe auffällig oft kurz vor Defektionen liegen, hat eine lesbare
Historie (L2, wie D15/D18).

**Widerruf bleibt dominant:** Er kostet nichts extra und schützt andere; nicht zu widerrufen
hält die Haftung für einen Defektor lebendig. Niemand hat einen Grund zu zögern.

**Nebeneffekt:** `t_exp` wird zur ökonomischen Entscheidung statt zum bloßen Backstop — kurze
Laufzeit = liquides Budget, häufige Erneuerung, schwächeres Signal; lange Laufzeit = starkes
Signal, gebundenes Kapital. Erneuerung ist wiederholte aktive Bestätigung und damit frischere
Evidenz als ein zehn Jahre alter, nie widerrufener Vouch.

### D18 — Keine Kapazitätsbelohnung für erfolgreiche Bürgschaft

Ein erfolgreicher Vouch erhöht `C(I)` **nicht**. Begründung, an D10 anzuhängen, damit der
Vorschlag nicht erneut auftaucht:

- **D10 stirbt sonst.** `C` wäre akkumulativ — genau das Vermögen, dessen Abwesenheit das
  Feature ist.
- **Der Sünden-Puffer kehrt zurück**, eine Ebene versetzt: erst Kapazität sammeln, dann
  verbrennen.
- **Vouch-Farming.** Rational wäre, für möglichst *sichere* Kandidaten zu bürgen — also für
  längst Etablierte, nicht für Neulinge. Der Mechanismus würde Onboarding bestrafen.

**Die Belohnung existiert bereits, nur nicht in der Metrik:** Der Gebürgte wird zum
funktionierenden Gegenüber — Handelspartner, Lieferant, Poolmitglied. Der Ertrag liegt in der
Beziehung. Dazu L3: Der Lohn guten Bürgens ist, nichts zu verlieren und weiter bürgen zu können.

**Legitim ist zweite Ordnung:** Die eigene Vouch-Historie ist als Claim-Historie sichtbar; andere
lesen sie und entscheiden, wie viel `w` sie *mir* geben. Keine Protokollprämie, sondern
menschliches Urteil auf Basis von Information.

### D9 — Anteilige Kapazitätsteilung verworfen

`C(I)/deg_out(I)` bzw. Anteil `wᵢ/Σw` bricht die Monotonie aus `02 §7`: Bei Teilwissen ist `Σw`
zu klein ⇒ jeder bekannte Anteil zu groß ⇒ **fehlendes Wissen erhöht das errechnete Vertrauen**.
Über eine Mesh mit partial sync nicht tolerierbar.

Nicht durch eine Normalisierungsregel reparierbar: Jede Regel, in der andere Kanten den Anteil
einer Kante beeinflussen, hat diesen Defekt. Er liegt in der Kopplung, nicht in der Formel.

### D27 — Die PageRank-Relaxation liest `w`

Nachtrag aus der Prüfung des Spec-Nachzugs. D1 hinterließ `§5` unterspezifiziert: ob die
Übergangsmatrix das Vouch-Gewicht berücksichtigt, war offen — zwei Implementierungen hätten
legitim auseinanderlaufen können.

**Beschluss:** Der Übergangsanteil ist proportional zu `w`, danach spaltenstochastisch
normalisiert. Begründung: Ignorierte `§5` das Gewicht, behandelte es einen Probe-Vouch mit
`w = 0.05` wie eine volle Bürgschaft und wäre damit **großzügiger als die harte Sicht** — die
falsche Richtung. Eine Relaxation darf ungenauer sein, nie über-vertrauend.

**Kein Widerspruch zu D9.** Die dort verworfene Normalisierung bricht die Monotonie der *harten*
Schranke. In `§5` ist sie zulässig, weil dieser Abschnitt keine harte Schranke trägt und für
Gates verboten ist (`§5`, `§9`).

**Nebenbeschluss:** Übergangsmatrix `C` → `P` umbenannt (Kollision mit der Knotenkapazität
`C(x)`). Reine Notation.

**Weitere Nachbesserungen aus derselben Prüfung** (ohne eigene Entscheidungsnummer):
Symbolkollision `n` in `§3.1` aufgelöst; Abgrenzung des Knotenkapazitäts-Blockzitats in `§3`
gegen `§3.1`; `pending`-Vouches binden Budget (sonst umgeht ein zurückgehaltener Vorgänger die
Budgetregel).

---

## B. Sybil-Schranke und Kollusion (Layer 02) ⚠️

### D6 — `02 §4` überclaimt: Summe der Einzelflüsse ≠ Multi-Sink-Fluss

`02 §4` definiert `trust(s → T) = maxflow(s_out → T_in)` **pro Ziel** und behauptet dann
`Σ_{T ∈ S} trust(s → T) ≤ Σ_{h ∈ Grenze} C(h)`. Die Super-Sink-Herleitung beweist jedoch den
**simultanen** Multi-Sink-Fluss — eine andere Größe.

**Gegenbeispiel:** `C(h) = 10`, `h` bürgt für `g₁` und `g₂`. Einzeln berechnet ist
`trust(s→g₁) = trust(s→g₂) = 10`, Summe 20. Der simultane Fluss ist 10. Der Satz gilt für 10.

Praktische Folge: **Bei Einzelabfrage verdünnt nichts.** Alle Kanten innerhalb der Sybil-Region
sind ∞, also erreicht der bei `g` ankommende Fluss jedes `T ∈ S`. Jeder Sybil bekommt einzeln
den vollen Kantenwert.

**Was `Σw ≤ 1` hieran repariert — und was nicht.** Die Summenidentität wird **nicht** repariert
(eine Angriffskante hat genau einen Kopf, aber innerhalb `S` verteilt sich der Fluss über
∞-Kanten auf alle Ziele). Repariert wird der praktisch gefährliche Teil: Der Wert eines
einzelnen Sybils ist nicht mehr durch `C(h)` gedeckelt, sondern durch `w_e` — durch das, was der
ehrliche Bürge *dieser einen Kante* explizit zugewiesen hat. Um Sybils über eine Schwelle zu
heben, braucht der Angreifer ein großes `w`, und ein großes `w` bindet das Budget des Bürgen und
aktiviert seine Haftung. **Identitäten bleiben gratis; ohne teuer gebundenes fremdes `w` bleiben
sie wertlos.**

### D7 — Reparatur: Satz umformulieren + VR-02.1

Gewählt: **Variante (a)** — den Satz ehrlich auf den simultanen Fluss beschränken und die Grenze
sichtbar machen. **Verworfen: Variante (b)** (`trust()` generell als Multi-Sink definieren) —
teurer und ändert die Semantik jeder Einzelabfrage.

> **VR-02.1 — Aggregation MUSS simultan rechnen.** Jede Entscheidung, die Vertrauen über
> **mehrere** Identitäten verrechnet (Quorum, Abstimmung, „N unabhängige Attestierungen",
> Versicherungspool), MUSS den Multi-Sink-Fluss über der gesamten Anfragemenge berechnen.
> Die Summe einzeln berechneter `trust(s→Tᵢ)` ist **keine** gültige Näherung und trägt
> **keine** Sybil-Schranke.

Zusätzlich unter „bewusst getragene Grenzen": *Einzelabfragen verdünnen nicht; wer Sybil-Schutz
über eine Menge braucht, muss simultan rechnen.*

### D20 — Sybil-Schranke ist keine Kollusions-Schranke

Expliziter Satz in `02 §4`. Der Beweis funktioniert, weil zwischen ehrlicher Region `H` und
Sybil-Region `S` **wenige Angriffskanten** liegen; er bindet den Fluss an `Σ C(h)` über die
Grenzknoten. Bei echter Unterwanderung gilt diese Annahme nicht: Kollaborierende Menschen haben
je ihre eigenen, *echten* Beziehungen. Der Schnitt ist nicht dünn — er existiert nicht als
Schnitt.

**Die bewiesene Schranke schützt gegen gefälschte Identitäten, nicht gegen echte Menschen, die
sich abstimmen.** Keine Schwäche dieser Konstruktion, sondern die Grenze der gesamten Klasse —
Viswanath et al. (SIGCOMM 2010) zeigten, dass sozialgraph-basierte Sybil-Abwehren im Kern lokale
Community-Erkennung betreiben, dass Netzwerke mit ausgeprägter Community-Struktur dadurch
*anfälliger* sind, und dass die Erkennungsgenauigkeit fällt, je näher am vertrauten Knoten der
Angreifer seine Kanten platziert.

**Direkte Folge für MaR:** `C(x) = C₀γ^d` macht Seed-Nähe zur einzigen Ressource. Der optimale
Angriff ist damit bestimmt — **nicht viele Kanten, sondern wenige nahe.** Ein Komplize bei
`d = 1` ist mehr wert als hundert bei `d = 4`. Muss ein Implementierer wissen, sonst nimmt er
einen Schutz an, den er nicht hat.

### D19 — Pfad-Disjunktheit als Policy-Primitiv

Statt „N Attestierungen" verlangt eine Policy „N Attestierungen über **knoten-disjunkte** Pfade
vom Seed". Berechnung: Max-Flow mit Einheitskapazitäten — derselbe Dinic, andere
Kapazitätsbelegung.

**Wirkung:** Eine Koalition, die über *einen* Bürgen eingesickert ist, hat Min-Cut 1, egal wie
viele Mitglieder sie hat. Sie kann kein Quorum von 3 unabhängigen Zeugen stellen.

Strukturelle Übersetzung von „Zeugen dürfen nicht voneinander abhängen" — Rechtsordnungen kennen
das als Befangenheitsregel, hier als Graphenkennzahl. **Die einzige Anti-Kollusions-Maßnahme,
die aus der vorhandenen Mathematik direkt folgt.** Aufzunehmen in `02 §8` neben der Schwelle.

### D8 — Brückenbelohnung (Betweenness) verworfen

Erwogen als Gegenmittel zur Clan-Schließung, verworfen aus zwei unabhängigen Gründen:

1. **Falscher Anreiz.** Wer für das Verbinden zweier Cluster belohnt wird, hat ein Interesse
   daran, dass die Cluster getrennt *bleiben* (Burt, *structural holes* / *tertius gaudens*).
   Der Mechanismus prämiert im Gleichgewicht Fragmentierung.
2. **Sybil-anfällig.** Betweenness ist trivial fälschbar: Pseudo-Cluster erzeugen, sich als
   einzige Verbindung dorthin setzen, Prämie für eine Brücke ins Nichts kassieren. Max-Flow ist
   gegen genau diesen Angriff bewiesen robust; Betweenness ist es nicht.

**Das Problem löst D1/D3 besser:** Ein billiger Probe-Vouch (`w = 0.05`) macht Onboarding wieder
attraktiv. Anreiz an der Eintrittsschwelle statt Prämie für Vermittler.

### D24 — Beobachtungskennzahlen: Unabhängigkeit und Ersetzbarkeit

**Korrigierte Fassung.** Die ursprünglich vorgeschlagene Konzentrationsmetrik (Flussanteil der
Top-`k`-Knoten, Min-Cut Seed↔Mitgliedschaft) behandelte Konzentration als Pathologie. Sie kann
nicht zwischen drei vereinnahmten Engpässen und drei Menschen unterscheiden, denen tausend
andere unabhängig vertrauen — sie schlägt bei Kaperung und bei Exzellenz gleichermaßen an.

Stattdessen zwei Zahlen, beide auf dem eigenen Teilgraphen, ohne globale Sicht:

- **Quellenunabhängigkeit:** Sind die Bürgen von `X` untereinander pfad-disjunkt zum Seed?
  Tausend Bürgen aus einem Cluster sind ein Bürge; tausend aus disjunkten Regionen sind echte
  Mehrfachbestätigung. Derselbe Solver wie D19.
- **Ersetzbarkeit:** Ist `X` ein Schnittknoten — bricht der Fluss zur Peripherie zusammen, wenn
  `X` entfällt?

**Interpretation:** Hohe Stellung aus vielen unabhängigen Quellen bei vorhandenen
Alternativpfaden ist Leistung — verdient und jederzeit bestreitbar. Hohe Stellung aus einer
Quelle ohne Alternative ist ein Kaperungsziel, unabhängig von der Verdienstlage der Person.

Kein Protokollzwang, keine Schwelle. Eine Zahl, die jeder selbst rechnet (L2).

---

## C. Sanktionsmechanik (Layer 05)

### D11 — Sanktionsschwere ∝ Standing, beschränkt monoton

```
severity = base · f(standing)
f = 1 + c · min(t_s / t_ref, m)        c, m, t_ref = Policy
```

Reputation ist ein **Versprechen, kein Puffer**: Wer hohes Standing hat, hat viel versprochen,
der Bruch wiegt schwerer. Empirisch gestützt (Drittparteien sanktionieren hochstatus-Akteure
härter, wenn sie nach öffentlichem Kooperationsbekenntnis defektieren; Statustyp moderiert:
dominanzbasiert härter als prestigebasiert).

**Deckelung `m` ist konstitutiv, nicht kosmetisch.** Ohne sie entsteht ein neuer Fehlanreiz:
Standing zu *vermeiden* — unauffällig bleiben, nicht bürgen, keine Verantwortung übernehmen.
Kalibrierungsbedingung zum Policy-Knopf:

```
∂Nutzen/∂Standing  >  ∂Sanktionserwartung/∂Standing
```

Ein Nukleus, der sie verletzt, züchtet Duckmäuser — und soll das sehen können.

Zweitwirkung im Kontext von D25/D26: Für den Leistungsträger ist ein erwiesener Bruch teurer als
für jeden anderen. Das ist der Preis dafür, sich beeinflussen zu lassen, und er steigt mit dem,
was die Person zum lohnenden Ziel macht.

### D12 — Beta-Update multiplikativ **und** additiv

```
α ← α · (1 − k_slash)     # entfernt den Puffer
β ← β + 1                 # erhält die Rückfälligkeits-Akkumulation
```

**Der Defekt:** Mit `E = (α+1)/(α+β+2)` gilt `∂E/∂β ≈ −(α+1)/(α+β+2)²`. Der marginale Schaden
eines Fehltritts fällt **quadratisch** mit der Kontogröße — ein tausendfach bewährter Akteur
zahlt einen Bruchteil dessen, was ein Neuling zahlt. Falsche Richtung, nicht bloß falsche
Kalibrierung.

Nur die erste Zeile würde `05 §4` („Cure-Kosten steigen mit Rückfälligkeit") zerstören, weil `β`
die Historie trägt. Beide zusammen sind die richtige Asymmetrie.

**Kalibrierungshinweis zu `k_slash`:** konservativ (niedrig) ansetzen. Begründung → Abschnitt F.

---

## D. Macht, Rotation und Nachvollziehbarkeit (Layer 00/04/06)

### D13 — Mitgliedschaft und Ressourcen-Scope trennen

`grant-membership` darf **nicht** automatisch Zugang zu gepoolten Ressourcen bedeuten.
Zwei getrennte Claims ⇒ ein Nukleus kann offen aufnehmen **und** den Pool schützen.

**Begründung:** Offene Aufnahme wird nicht per se instabil, sondern erst in Kopplung mit
gepooltem Ressourcenzugang — dann trägt der Eintretende keine Eintrittskosten, zieht aber aus
gemeinsamem Bestand. Ostroms Design-Prinzipien sagen dasselbe: klare Grenzen sind für
*Common-Pool-Ressourcen* konstitutiv, nicht für Assoziation überhaupt.

### D21 — Losverfahren und Amtszeitbegrenzung als Nukleus-Policy

Gegen gezielte Unterwanderung wirksam, weil der Angreifer nicht weiß, wen er unterwandern muss.
**Lokal gezogen:** Jeder Verifizierer lost aus seiner eigenen berechtigten Menge mit eigener
Zufälligkeit. Kein globaler Randomness-Beacon, kein Konsens — und weil verschiedene Beobachter
verschieden ziehen, kann der Angreifer nicht einmal die Zielmenge bestimmen. Die
„nie global"-Invariante ist hier Verstärker, nicht Hindernis.

Amtszeitbegrenzung fast gratis: `t_exp` existiert, muss nur auf Mandate und Ämter angewandt
werden.

**⚠️ Nicht ohne D23 anwenden** (siehe dort).

### D23 — Rotation gilt der persistenten Schicht, nicht nur den Ämtern

**Warnung aus der Forschung:** Amtszeitbegrenzung allein verschiebt Macht in die persistente
Schicht. Polsby (1990) vor Kaliforniens Term-Limit-Initiative: Amtszeitbegrenzungen verschieben
Macht lediglich zu den unzugänglicheren Beamten und Einflussvermittlern im Umfeld. Bestätigt
durch Befragungen in Staaten mit und ohne Term Limits: Führungsfiguren in der Legislative
verloren Einfluss, Gouverneure, Stäbe und Verwaltungsapparate gewannen (Carey, Niemi, Powell
1998); Lobbyisten-Befragungen in fünf betroffenen Staaten fanden starken Konsens für dieselbe
Verschiebung. Mechanismus: Reduktion institutionellen Wissens stärkt die, die bleiben. Für
Sortition gilt das verschärft — wer zufällig ausgewählt wird, ist per Konstruktion unerfahren.

**Wo bei MaR Persistenz sitzt — drei Orte, nur einer ist ein Amt:**

1. **Nukleus-Seed `e_N`.** Wer im Ankerset steht, definiert die Linse für alle, die sie
   benutzen. Ohne Seed-Rotation ist jede Ämterrotation Kosmetik.
2. **Dienstbetreiber** (Zeitdienst, Validierungs-Nodes, `06 §5/§6`). Langlebig, alle hängen
   davon ab — strukturelle Macht ohne Amt.
3. **Positionale Kapazität.** `C(x) = C₀γ^d` verleiht Macht **ohne Amt**. Man kann jeden Posten
   rotieren, und dieselben Menschen bei `d = 1` halten weiterhin die strukturelle Kapazität.
   Amtszeitbegrenzung greift hier prinzipiell nicht.

**Beschluss:**

- **Seed und Dienst-Deklarationen tragen `t_exp` und müssen periodisch neu erklärt werden.**
  Ein Ankerset ist eine Erklärung, keine gewachsene Beziehung — rotierbar, ohne
  Vertrauenssemantik zu zerstören. Ablauf ohne Neuerklärung ⇒ sauberer Fallback auf `e_s`
  (`02 §6.3`). Das ist der eingebaute Sicherheitszustand, kein Ausnahmezustand.
- **Positionale Kapazität ist nicht rotierbar — nur messbar** (→ D24).
- **Einarbeitungslücke:** Wissen liegt in signierten, auditierbaren Claims, nicht in den Köpfen
  der Bleibenden. Ein ausgeloster Schiedsrichter liest die Verdikt-Historie seines Vorgängers
  (D15). Kein voller Ersatz für Erfahrung, aber genau der Vorsprung, den ein permanenter Apparat
  sonst monopolisiert.

### D25 — Ansehen und Torwächterschaft trennen (Policy-Default)

`t_s` trägt aktuell zwei verschiedene Dinge in einer Zahl:

- **Gehört-werden** — epistemische Autorität. **Nicht-rival:** Dass tausend Menschen einem guten
  Denker zuhören, nimmt niemandem etwas weg. Eine Obergrenze wäre Verschwendung.
- **Torwächterschaft** — wer wird aufgenommen, wer bekommt Zugang, wessen Bürgschaft trägt.
  **Rival und zwingend:** Was ich zulasse, müssen andere hinnehmen.

Nur die zweite Sorte ist ein lohnendes Unterwanderungsziel. Einen Denker zu bestechen bringt
wenig, wenn seine Argumente von jedem geprüft werden können. **Der Lobbyist kauft keine Ideen,
er kauft Entscheidungen.**

Mechanismus vorhanden: der **Zweck-Tag** (`02 §2`). Torwächter-Zwecke werden in eigenen Scopes
geführt; `Σw ≤ 1` bindet dann nur das Torwächter-Budget, nicht das Zuhören. Folge: **Ansehen
unbegrenzt, Torwächterschaft begrenzt.** Ungleiche Begabung darf sich ungleich auswirken, ohne
proportional Zugangsmacht zu erzeugen.

**Als Policy-Default, nicht als Invariante** (L1, L4): Die Referenz-Verfassung trennt, ein
Nukleus darf zusammenlegen — mit ausdrücklicher Warnung im Spec-Text. Ein Nukleus, der vermengt,
macht sich angreifbar; andere sehen an seiner Struktur, was daraus wird.

### D26 — Amtsführung in nachvollziehbarer Kette

**Das Problem ist nicht Macht, sondern Unnachvollziehbarkeit.** Was eine unantastbare Klasse
erzeugt, ist plausibles Abstreiten: dass nachträglich nicht rekonstruierbar ist, wer was auf
welcher Grundlage entschieden hat.

Primitiv dafür ist die **Autorenkette** (`h_prev`). Wer ein Amt bekleidet und Entscheidungen als
Claims signiert, erzeugt eine manipulationssichere Amtshistorie — nichts kann nachträglich
eingefügt, entfernt oder umdatiert werden, weil sonst die Kette bricht. Zwei widersprüchliche
Versionen derselben Kettenposition sind **Equivocation**: mechanisch slashbar, ohne Verdikt.
**„Das habe ich so nie gesagt" ist damit keine Verteidigung, sondern ein selbst-validierender
Beweis gegen den Sprecher.**

**Regel:** Eine Amts- oder Torwächter-Rolle wird per `obligation@1` angenommen; die Obligation
bindet daran, Entscheidungen im Scope als Claims in der eigenen Kette zu signieren. Bruch ist
dann kein subjektiver Vorwurf, sondern erwiesener Obligationsbruch über bestehende Mechanik.

> **VR-04.1 — Kettenlose Amtsführung trägt kein Vertrauen.** Ein Akteur, der eine Amts- oder
> Torwächter-Rolle innehat, ohne die zugehörige Kettenbindung eingegangen zu sein, wird für
> Entscheidungen in diesem Scope **nicht** als vertrauenswürdig gewertet.

Kein Verbot — die Bewertung fällt einfach aus. Dieselbe Bewegung wie „Neuling ≈ 0": kein
Sonderfall, nur die Abwesenheit von Grundlage.

**Zwei Sonderfälle:**

- **Lücken sind sichtbar, aber nicht beweisbar.** Wer eine Entscheidung gar nicht signiert,
  bricht die Kette nicht — er entscheidet außerhalb. Erkennbar nur, wenn die Wirkung sichtbar
  ist und der Claim fehlt („Abwesenheit von Evidenz ist keine Evidenz der Abwesenheit",
  `02 §7`). Was bleibt, ist Reputationswirkung.
- **Nachvollziehbarkeit ≠ Öffentlichkeit.** Eine Kette kann unmanipulierbar sein, während
  Inhalte erst später oder nur gegenüber einem Prüfgremium offengelegt werden.
  Verhandlungspositionen brauchen mitunter Vertraulichkeit *jetzt*, aber nie
  Unnachvollziehbarkeit *später*. Der Hash steht fest, bevor der Inhalt offen ist.

**Zweiseitigkeit:** Der Einflussnehmer hat selbst eine Identität. Ein erwiesener
Bestechungsversuch trifft sein Standing und seinen Bond — dieselbe Logik wie der Anklage-Stake
(`05 §5`). Beeinflussen wird ebenso riskant wie beeinflusst werden. Zusammen mit D11 (Preis
steigt mit Standing) und D5 (Bürgen verlieren mit, also Peer Monitoring dort, wo es am meisten
wert ist).

### D14 — Referenzimplementierung bleibt meinungsfrei

Die Referenzimplementierung implementiert **nur** Mechanismus und Policy-Knöpfe, ohne
Default-Meinung. Eine konkrete Wertvorstellung lebt als `example-nucleus.md` im Repo — klar als
*eine Instanz* gekennzeichnet, neben der später eine mit gegenteiligen Parametern stehen kann.

Andernfalls wird die Referenzimplementierung stillschweigend normativ, und jede abweichende
Implementierung wirkt wie eine Abweichung statt wie eine gleichberechtigte Variante.

### D15 — Verdikt-Historie auditierbar (`06`)

Kein neues Profil. Ein Schiedsrichter ist eine Identity mit `service-announce@1`; seine Verdikte
sind bereits Claims mit Autorenkette. Ergänzt wird der normative Satz:

> Wer als Schiedsrichter auftritt, dessen Verdikt-Historie MUSS abfragbar sein — sonst ist er
> nicht bewertbar.

Damit wird ein systematischer Milde-Bias gegenüber Angesehenen (*moral credentials*) nicht
verhindert, aber **beobachtbar und bepreisbar**: Verdikte reisen ohnehin als attribuierte
Meinungen, gewichtet mit dem Vertrauen des Beobachters in den Schiedsrichter (`05 §5`).

### D16 / D22 — Neue getragene Grenzen in `VISION §6`

1. **Reputationsgebundene Solidarität ist regressiv.** „Neuling ≈ 0" trifft Bedürftige und
   Angreifer identisch. Unglück korreliert negativ mit Standing (Krankheit, Pflege,
   kollabierende Region). `C(x) = C₀γ^d` verstärkt ererbte Netzwerkposition exponentiell.
   Historisches Vorbild mit dokumentierten Deckungslücken: Friendly Societies / Fraternal
   Societies (Beito, *From Mutual Aid to the Welfare State*) — Wandernde, chronisch Kranke,
   Konjunkturkrisen mit gleichzeitiger Anspruchsberechtigung (= korreliertes Risiko).
2. **Moral-Credentials-Residual.** Der Bias wirkt auf die Deutung mehrdeutigen Verhaltens, also
   vor der Signatur. Gegen einen nukleus-weit geteilten Bias hilft nur Exit. Kategorie:
   irreduzibler Orakel-Residual.
3. **Einzelabfragen verdünnen nicht** (→ D6/D7).
4. **Kollusion ist nicht Sybil** (→ D20). Gegen eine hinreichend große, geduldige, echt
   eingebettete Koalition hilft kein Protokoll. Die Mechanismen erhöhen die nötige
   Koalitionsgröße und machen die Vorbereitungszeit sichtbar — mehr ist nicht zu haben, und ein
   Protokoll, das mehr verspricht, lügt.
5. **D22 — Seed-Kompromittierung.** Wer `e_N` kompromittiert, kompromittiert jeden, der diese
   Linse benutzt. Der Fallback auf `e_s` (`02 §6.3`) ist **Eindämmung, keine Abwehr.**
6. **Restfenster bei Widerruf vor Defektion** (→ D17).
7. **Kettenlücken.** Entscheidungen außerhalb der Kette sind nicht beweisbar, nur auffällig
   (→ D26).

---

## E. Offene Lücken aus der Prüfung

**A — `t_exp` wird für Vouches verpflichtend.** `02 §6.2` formuliert `t_exp` als optional. Mit
D17 hängt die Budgetfreigabe daran: Ein Vouch ohne `t_exp` bindet Budget **für immer**. Also:
In Scopes mit `Σw ≤ 1` MUSS ein Vouch `t_exp` tragen, oder die Policy setzt eine Maximallaufzeit
als Default. Kein Fork, eine Lücke.

**B — Zwei Mengen, nicht eine.** Implementierungskritisch für `02a`:

| Menge | Inhalt | Verwendung |
|---|---|---|
| **Aktiv-Set** | nicht widerrufen, nicht abgelaufen | Kantensatz für den Fluss |
| **Budget-Set** | nicht abgelaufen (widerrufen **eingeschlossen**) | Prüfung `Σw ≤ 1` |

Wer beides zusammenlegt, bekommt entweder ein Budget-Leck oder Phantomkanten im Graphen.

**C — Bootstrap-Enge.** `Σw ≤ 1` macht die Frühphase quantitativ eng: Drei Gründer haben
zusammen Budget 3; zwanzig frühe Mitglieder bedeuten `w ≈ 0.05`, also Kantenkapazität
`0.05·C₀`. Ob das über der Admission-Schwelle liegt, hängt jetzt von `C₀`, `γ` **und** der
Schwelle gemeinsam ab — die Knöpfe aus `02 §8` sind nicht mehr unabhängig kalibrierbar. Kein
Fehler, aber eine neue Nebenbedingung im Parameterraum; gehört als Warnung dorthin. Testbar über
ein Bootstrap-Szenario, das zeigt, ab wann eine Gruppe wachsen kann.

---

## F. Kalibrierungshinweis: `w`-Haftung konservativ ansetzen

Was hier gebaut wird, ist strukturell **Joint Liability Lending** (Grameen, ab 1976): Ein Kreis
haftet füreinander, weil er sich besser kennt als jede zentrale Instanz. Peer Screening plus
Peer Monitoring.

Der empirische Befund ist unbequem: Die Institutionen, die Joint Liability erfunden haben —
Grameen, BancoSol, ASA — sind davon abgerückt und auf individuelle Haftung umgestiegen; ein
MFI-Panel (MIX Market, 2008–2014) belegt den Trend. Die Umstellung ließ die Rückzahlungsquoten
**unverändert**. Beibehalten wurden dagegen die regelmäßigen Gruppentreffen. **Die Gruppe wirkt,
die formale Mithaftung kaum** — was trägt, ist wiederholte Interaktion und geteilte Information.

Dokumentierte Kosten:

- Klienten mögen die durch Gruppenhaftung erzeugte Spannung nicht; übermäßige Spannung unter
  Mitgliedern ist häufiger Grund für freiwillige Abwanderung. Übertragen: Der Nachbar, dessen
  `w` ich binde, ist nicht mehr nur Nachbar.
- Strategische Defektion: Kreditnehmer, die unter Einzelhaftung zurückgezahlt hätten,
  defektieren, wenn sie die Gesamtlast der Gruppe nicht tragen können — der Effekt rührt
  möglicherweise eher von Gruppendruck als von der Haftung selbst her. Kaskadenrisiko; `05 §6`
  deckelt es auf eine Sprunghöhe.

**Ableitung:** Die `w`-Haftung ist nicht falsch, aber wahrscheinlich **nicht der
Hauptmechanismus**. Der Hauptmechanismus ist Knappheit (`Σw ≤ 1`) plus Sichtbarkeit — dass
sorgfältig ausgewählt werden *muss* und andere sehen, wie ausgewählt wurde. Haftung ist der
Backstop für den Extremfall, nicht der Alltagsanreiz. Daher `k_slash` niedrig, mit Kommentar in
`example-nucleus.md`, der auf diesen Befund verweist — Kalibrierung begründet statt geraten.

Theoretischer Anker für `w` als solches: **Costly Signaling** (Zahavi; Gintis/Smith/Bowles) —
Glaubwürdigkeit erfordert Kosten. Ostroms Design-Prinzip 5 (abgestufte Sanktionen) ist über
`05 §3` bereits erfüllt.

---

## G. Änderungsliste pro Datei

| Datei | Änderung | Quelle |
|---|---|---|
| `02-trust-flow.md §1` | Leitsatz „Vertrauen ist Zustand, kein Vermögen"; keine Kapazitätsprämie | D10, D18 |
| `02-trust-flow.md §2` | Torwächter-Zwecke in eigenen Scopes (Policy-Default) | D25 |
| `02-trust-flow.md §3` | `w`-Obergrenze `⌊n·C(I)/D⌋`, Default `n=D`; `Σw ≤ 1` über dem Budget-Set | D1, D2, D3 |
| `02-trust-flow.md §4` | **Satz auf simultanen Fluss korrigieren**; Monotonie-Zusatz für `w`-Caps; Satz *Sybil ≠ Kollusion* | D6, D7, D1, D20 |
| `02-trust-flow.md §6.2` | `t_exp` für Vouches verpflichtend; Widerruf/Freigabe-Semantik | E-A, D17 |
| `02-trust-flow.md §8` | Policy-Knöpfe `D`, Budgetgrenze; VR-02.1; Pfad-Disjunktheit; Kennzahlen; Bootstrap-Warnung | D2, D7, D19, D24, E-C |
| `02-trust-flow.md §9` | Getragene Grenzen: Einzelabfrage, Kollusion, Widerruf-Restfenster | D6, D20, D17 |
| `05-enforcement.md §1` | Beta-Update multiplikativ + additiv | D12 |
| `05-enforcement.md §3` | Über-Commitment ⇒ direkt Stufe 3 (wie Equivocation) | D4 |
| `05-enforcement.md §4` | `severity = base · f(standing)`, Deckelung, Kalibrierungsbedingung | D11 |
| `05-enforcement.md §6` | Sprunghöhe = `w · Schaden`; nur bei selbst-validierenden Beweisen | D5, D5a |
| `06-services.md` | Verdikt-Historie MUSS abfragbar sein; Dienst-Deklarationen mit `t_exp` | D15, D23 |
| `04-governance.md` | Losverfahren + Amtszeitbegrenzung als Policy; VR-04.1; `obligation@1` für Amtsannahme | D21, D23, D26 |
| `00-…-constitution.md` | Mitgliedschaft ≠ Ressourcen-Scope; Seed mit `t_exp` | D13, D23 |
| `VISION.md §6` | Sieben getragene Grenzen | D16, D22 |
| Repo-Wurzel | `example-nucleus.md` anlegen; `k_slash` niedrig, mit Begründung | D14, F |

---

## H. Konsequenzen für die Implementierung

**Golden Anchors neu rechnen.** D6/D7 betreffen unmittelbar die aggregate Sybil-Schranke und die
`|S|`-Unabhängigkeit. Für den kanonischen Testgraphen (ALICE-Seed, Kette ALICE→BOB→CAROL, drei
parallele Sybil-Kanten von CAROL, EVE unerreichbar) werden gebraucht:

1. `trust(s→gᵢ)` **pro Ziel einzeln**
2. **simultan** über `{g₁, g₂, g₃}` (Multi-Sink)
3. Differenz aus 1 und 2 als **Testvektor für VR-02.1**
4. `w`-Varianten neben den `w = 1`-Fällen
5. Budget-Fall mit widerrufenem-aber-nicht-abgelaufenem Vouch (prüft E-B)
6. Einheitskapazitäts-Lauf für Pfad-Disjunktheit (D19/D24)
7. Bootstrap-Szenario: ab wann wächst eine Gruppe unter `Σw ≤ 1`? (E-C)

**`w`-Caps sind additiv.** Bei `n = D` ist das Verhalten identisch zum bisherigen Stand — die
bestehenden Testvektoren bleiben gültig und bekommen `w`-Varianten als Ergänzung.

**Reihenfolge — Spec vor Prompt.** `02 §4` enthält aktuell einen falschen Satz. Ein Prompt gegen
eine fehlerhafte Spec produziert fehlerhafte Tests. Also: Spec-Nachzug (Änderungsliste G,
Layer 02) → Golden Anchors → `02a-maxflow` → `02b-pagerank` → Layer 03.

**Umfang `02a-maxflow`:** Dinic, Knoten-Splitting, `w`-Caps in exakter Rational-Arithmetik,
`Σw`-Prüfung über dem Budget-Set, Multi-Sink-Pfad, Einheitskapazitäts-Pfad für
Disjunktheitszählung, Über-Commitment-Erkennung als Fehlerklasse.

**`02b-pagerank`:** Die Relaxation bleibt für harte Entscheidungen verboten (`02 §5`), liest
aber nun das Vouch-Gewicht (D27). Golden-Anchor-Werte für die weiche Sicht sind entsprechend
mit gewichteter Adjazenz zu rechnen.

---

## I. Nicht entschieden

- Ist `Σw > 1` im Sinne von `05 §4` terminal oder kurierbar? (Policy, vor Merge)
- Konkrete Werte für `c`, `m`, `t_ref` (D11), `k_slash` (D12), `D` (D2) — gehören in
  `example-nucleus.md`, nicht in die Spec.
- Erneuerungsintervall für Seed und Dienst-Deklarationen (D23).
