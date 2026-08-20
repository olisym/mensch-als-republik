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

**Präzisiert durch D40:** `w` ist in `§5` das Gewicht der **Gruppe** `(I, J, N)`, also
`n_kante / D`, nicht das eines einzelnen Claims. Sonst trüge ein erneuerter Vouch in der
Relaxation doppeltes Gewicht, während er in der harten Sicht einfach zählt — wieder die falsche
Richtung.

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

> **Korrigiert durch D38 und D40:** Das Budget-Set schließt `superseded` und `pending` ein
> und wird je `(I, J, N)` über `max n` aggregiert. Die Tabelle oben gibt den Stand vor der
> Golden-Anchor-Rechnung wieder.

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
| `01-claim-atom.md §7.1` | `v`-Payload Key `0: n` normativ, Key-Vergabe; Float-Vorschlag entfernt; `t_exp` in Budget-Scopes Pflicht | D37, E-A |
| `02-trust-flow.md §2` | eine Kante je `(I, J)`, `max n`; keine Kante ohne gültiges `n` | D40, D37 |
| `02-trust-flow.md §3` | `⌊·⌋` bei `C`; BFS über `E⁺`; Ankerset und Super-Source an `a_in` | D28, D31, D36 |
| `02-trust-flow.md §3.1` | Aggregation je `(I,J,N)`; Out-Degree aus Budget; Budget-Set inkl. `superseded`; ungültiges `n` | D40, D33, D38, D37 |
| `02-trust-flow.md §4` | Definition auf `s_in`; Super-Sink an `T_in`; schärfere Schranke; zwei Divergenzursachen; Angriffsform | D31, D30 |
| `02-trust-flow.md §8` | `C₀` nicht verhältniserhaltend; `D` scope-fest + SHOULD `≥ C₀`, keine Kurzform; Granularitätsboden; Bootstrap-Ungleichungen; `r_max`; knoten-disjunkt mit Endpunkt-Regel; `include_flagged` | D28, D32–D35, D39 |
| Repo-Wurzel | `02-golden-anchors.md` aufnehmen | J |
| `02-trust-flow.md §3.1` | Budget-Austritt als `t_exp`-Prädikat, nicht als Zustand | D41 |
| `02-trust-flow.md §8` | Vouch-Kanten im Disjunktheitslauf tragen `1`, nicht ∞ | D42 |
| `02-golden-anchors.md §8` | INV-2 als Schranke; INV-8 verengt | D42, D44 |
| Repo-Wurzel | `02a-abnahme.md` aufnehmen | D41–D44 |
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

**`02b-pagerank` unverändert** — die Relaxation war nie kapazitätstragend (`02 §5`) und bleibt
für harte Entscheidungen verboten.

---

## I. Nicht entschieden

- Ist `Σw > 1` im Sinne von `05 §4` terminal oder kurierbar? (Policy, vor Merge)
- Konkrete Werte für `c`, `m`, `t_ref` (D11), `k_slash` (D12), `D` (D2) — gehören in
  `example-nucleus.md`, nicht in die Spec.
- Erneuerungsintervall für Seed und Dienst-Deklarationen (D23).
- `D` (D2) ist für den `example-nucleus` auf **100** festgelegt, damit TV1 byte-identisch
  bleibt und `n` sich als Prozent liest. `C₀ ≤ 100` folgt aus D34. Die konkreten Werte für
  `c`, `m`, `t_ref`, `k_slash` bleiben offen.

---

## J. Aus der Golden-Anchor-Rechnung (Layer 01/02)

Sieben Ankerwerte wurden von Hand gerechnet, dann gegengerechnet. Die Rechnung hat acht
Definitionslücken freigelegt, die keiner der Spec-Durchgänge gefunden hat — weil sie erst sichtbar
werden, wenn man eine Zahl produzieren muss. Zwei davon fielen erst beim **zweiten** Durchgang,
als die Zahlen gegen die Prosa geprüft wurden, die sie belegen sollte. Das ist der Ertrag von
„Golden Numbers vor Prompt".

### D28 — `C(x)` wird abgerundet, einmal am Ende

```
C(d) = ⌊ C₀ · γ^d ⌋        γ = γ_num / γ_den, exakt rational
     = (C₀ · γ_num^d) // γ_den^d
```

`§3` schrieb `C(x) = C₀·γ^d` ohne Rundung, während `§3.1` nur die Kantenkapazität rundet. Bei
`γ = ½, C₀ = 16` divergiert das ab `d = 5` (`½` gegen `0`).

**Einmal am Ende, nicht pro Schritt.** Bei `γ = ⅔, C₀ = 16, d = 2` ist das `7`, iterativ gerundet
wäre es `6`. Iteratives Runden macht das Ergebnis von der Auswertungsreihenfolge abhängig.

Folge: alle Kapazitäten sind `int`, der gesamte Solver rechnet ganzzahlig.

**Verworfen:** exakte Rationale für `C` (zwingt `Fraction` in den Fluss und damit gebrochene
Flusswerte, ohne dass irgendeine Aussage davon profitiert).

### D29 — Budgetprüfung ist eine Integer-Summe

```
Σw ≤ 1   ⟺   Σn ≤ D
```

Weil `D` scope-fest ist (D35), teilen alle `w` eines Scopes denselben Nenner. Die Prüfung braucht
keine Rationalarithmetik. Zusammen mit D28: **kein `Fraction`, kein `decimal`, kein `float` in der
gesamten harten Sicht.**

### D30 — Super-Sink hängt an `T_in`

`§4` sagt „∞-Kanten von jedem `g ∈ S`" — nach Knoten-Splitting mehrdeutig. Normativ:
`gᵢ_in → T*`. Konsistent zur Einzelabfrage; bei `gᵢ_out` zählte die interne Kante des Ziels mit
und die Multi-Sink-Semantik wiche von der Einzelabfrage ab.

### D31 — Super-Source hängt an `a_in` ⚠️

`§6.3` kennt ein Anker**set**, `§3`/`§4` sprechen durchgehend von einem einzelnen `s`. Normativ:
`S* → a_in` mit ∞ für jeden Anker `a`, und `d(x) = min_a d(a,x)`. Die Definition in `§4` lautet
damit `trust(s → T) = maxflow(s_in → T_in)`.

**Warum `a_in` und nicht `a_out`.** Die zuerst gewählte Fassung `a_out` — begründet mit der
Gleichheit zur bestehenden `s_out`-Konvention — bricht den Satz aus `§4`. Sie umgeht die interne
Kante des Ankers, also genau die Kapazität, über die der Beweis argumentiert. Gegenbeispiel
(Anker A′): ein Anker mit `C₀ = 16, D = 4` bürgt für drei Sybils mit je `n = 4`; die Kanten tragen
je `⌊4·16/4⌋ = 16`, der simultane Fluss ist **48** gegen eine behauptete Schranke von
`Σ_h C(h) = 16`.

Bei gültigem Budget sind beide Fassungen identisch, weil `Σ_e cap(e) ≤ C(a)` gilt. Sie
unterscheiden sich **genau dann**, wenn der Anker über-committet ist — und dort ist `a_in` die
sichere Richtung. Der Preis ist nominell: die Definition liest `s_in` statt `s_out`. Der Ertrag
ist ein **unbedingter** Satz, der auch gegen einen kompromittierten Anker trägt.

Nebenwirkung, ins Positive korrigiert: `C₀` bindet damit auf der Quellseite direkt. Die
Bootstrap-Ungleichung `θ ≤ f·C₀/M` ist dadurch tatsächlich eine Kapazitätsaussage; unter `a_out`
folgte sie aus der Budgetregel und das Etikett „Kapazitätsbedingung" war falsch.

**Kein Ankerwert von `TP-02` ändert sich** — ALICE ist budgetgültig, `cap(ALICE→BOB) = 16 = C₀`.

### D32 — Der Einheitskapazitäts-Lauf ist knoten-disjunkt, Endpunkte ungespalten

`§8` sagt „derselbe Max-Flow mit Einheitskapazitäten", D19 sagt „knoten-disjunkte Pfade". Beides
zusammen ist unterbestimmt. Normativ: **interne Kanten `= 1`, Vouch-Kanten `= ∞`.** Kantendisjunkt
wäre die falsche Größe — zwei Pfade durch denselben Bürgen sind ein Bürge.

**Endpunkte werden nicht gespalten:** die internen Kanten der Anker tragen `∞`; die des Ziels
liegt wegen D30 ohnehin nicht auf dem Pfad. Knoten-Disjunktheit zählt *Zwischen*knoten. Ohne diese
Ausnahme wäre jede Disjunktheitszahl von einem einzelnen Anker aus trivial `1` — die interne
Kante der Quelle läge auf jedem Pfad —, und die Kennzahl aus D24 wäre wertlos.

Damit unterscheidet sich der Einheitslauf in zwei Punkten vom Kapazitätslauf (Belegung **und**
Quellanbindung). Beide teilen Topologie und Indizes; getauscht werden nur die Kapazitätsvektoren.

### D33 — `D` ist zugleich der Out-Degree-Cap

Aus `n ∈ [1,D]` ganzzahlig und `Σn ≤ D` folgt: **höchstens `D` gleichzeitig bebürgte Subjekte pro
Identität und Scope** — gezählt werden Subjekte, nicht Claims (D40), und nur solche im Budget-Set.
Aus `cap ≥ 1 ⟺ n·C(I) ≥ D` folgt schärfer:

```
wirksame Out-Degree(I)  ≤  min( D , C(I) )
```

D3 hatte den Out-Degree-Cap `k` als „willkürliche Rationierung" verworfen. Die Granularität führt
ihn wieder ein — aber in der richtigen Form: **bei `D ≥ C₀` (D34) bindet `C(I)`, und damit ist die
Grenze positional statt gezählt.** Deine Out-Degree ist deine Kapazität. Der Einwand aus D3 ist
damit nicht umgangen, sondern erfüllt.

### D34 — `D ≥ C₀` als SHOULD, nicht MUST

Bei `D < C(I)` bindet `D` statt der Position — genau die willkürliche Rationierung aus D3. Ein
Produktivnukleus SOLL daher `D ≥ C₀` setzen.

**Kein MUST**, weil das Testprofil `TP-02` (`D = 4 < C₀ = 16`) genau das Regime prüft, in dem der
Out-Degree-Cap bindet. Ein MUST machte den eigenen Testgraphen illegal.

**Keine Kurzform.** Die Fassung „bei `D = C₀` vereinfacht sich `cap` zu `⌊n·γ^{d(I)}⌋`" ist
**falsch** und ist gestrichen. `cap = ⌊ n·⌊C₀γ^d⌋ / D ⌋` ist doppelt gerundet und lässt sich nur
zusammenziehen, wenn `C₀γ^d` ganzzahlig ist. Gegenbeispiel `C₀ = D = 16, γ = ⅔, d = 2, n = 9`:
`C = 7`, `cap = ⌊63/16⌋ = 3`, die Kurzform sagt `⌊4⌋ = 4`. Eine Implementierung, die abkürzt,
divergiert bei jedem nicht-dyadischen `γ`.

### D35 — `D` ist über die Lebensdauer eines Scopes unveränderlich

`n` steht im signierten Claim, `D` in der Policy. Änderte ein Nukleus `D`, würden **alle
bestehenden Vouches still umbewertet** (aus `w = 1` würde `w = 1/6`) und jede `Σn ≤ D`-Prüfung
kippte rückwirkend. Das ist keine Kalibrierung, sondern eine unbemerkte Neuinterpretation
signierter Aussagen.

Normativ: **ein anderes `D` bedeutet einen neuen Scope.** Passt zur Scope-Partition aus `§2` und
präzisiert D2 („nukleus-fest") — ein Nukleus mit getrennten Torwächter-Scopes (D25) darf je Scope
ein eigenes `D` führen, innerhalb eines Scopes nie.

**Verworfen:** `D` im Claim mitführen — bringt gemischte Nenner in die Budgetprüfung und damit
die Rationalarithmetik zurück, die D29 gerade beseitigt.

### D36 — Die BFS läuft über dem wirksamen Kantenset

```
E⁺ = { e ∈ Aktiv-Set : cap(e) ≥ 1 }
d(s,x) = kürzeste Pfadlänge über E⁺
```

`§3` definierte `d` über `E`, kapazitätsblind. Eine Kante mit `cap = 0` verkürzte damit die
Distanz und schenkte dem Ziel positionale Kapazität, ohne je Fluss zu tragen.

**Der bindende Grund ist der Disjunktheitslauf (D32).** Dort tragen alle Vouch-Kanten `∞`; eine
`cap = 0`-Kante ist von einer vollwertigen nicht mehr unterscheidbar. Ohne Filter wäre die
Quellenunabhängigkeit aus D24 mit subgranularen Vouches gratis fälschbar: unter `TP-BOOT`
(`C₀ = 16, D = 24`) erzeugen drei Kolludierende bei `d = 2` mit je `n = 1` drei knoten-disjunkte
Pfade auf ein gemeinsames Ziel, deren Vertrauensfluss exakt null ist (`⌊1·4/24⌋ = 0`).

**Keine Zirkularität:** `cap(I→J)` hängt nur von `d(I)` ab, und `d(I)` steht fest, wenn die BFS
`I` expandiert. Ein Durchlauf, `O(V+E)`.

**Zum Einwand „ein Vouch ist eine soziale Aussage, die auch ohne Durchsatz Position verleihen
sollte":** dann ist es kein Vouch. D5 — ein Parameter, drei gleichgerichtete Wirkungen, die
Deklaration ist der Einsatz. Ein gratis übertragbarer Positionskanal neben dem teuren wäre genau
die Ressource, die D20 als knapp identifiziert. Wer Bekanntschaft ohne Kapazitätsgewährung
ausdrücken will, braucht ein eigenes Prädikat, das in `§2` gar nicht erst als Kante zählt.

### D37 — `v`-Payload für `vouch@1` festgelegt

`01 §7.1` schlug `{ weight ∈ [0,1], … }` vor — ein **Float**, gegen `01 §3` Regel 6 („keine
Floats") und gegen die Integer-Arithmetik aus D28/D29. Der Vorschlag stammt aus der Zeit vor
D1/D2 und wurde nie nachgezogen.

```
v = { 0: n, … }     n : uint,  1 ≤ n ≤ D
v abwesend          ⇒  n = D   (w = 1, Default nach 02 §3.1)
```

**Geprüft wird Key `0`, nicht die Map als Ganzes.** Weitere Keys sind zulässig und für das Atom
opak — `§2` liest einen Zweck-Tag aus `v`, `§6.1` nennt `v.bond_ref`. Eine strikte Lesart
(„`v` muss exakt `{0: uint}` sein") hätte beide getötet. Reserviert: `0` = `n` (normativ),
`1` = Zweck-Tag, `2` = `bond_ref`; deren Kodierung wird mit `03`/`05` festgelegt und trägt bis
dahin keinen Testvektor.

| Fall | Kante | Budget-Beitrag |
|---|---|---|
| `n = 0` oder `n > D` | verworfen | **keiner** |
| `v` keine CBOR-Map, Key `0` fehlt oder ist kein `uint` | verworfen | **keiner** |

**Kein Budget-Beitrag bei unlesbarem `n`.** Eine geratene Zahl könnte eine Falschbeschuldigung
wegen Über-Commitment erzeugen. D3: Teilwissen erzeugt Unter-Erkennung, nie Falschbeschuldigung.
Die Kante fällt weg, weil das Unter-Vertrauen ist. Beides ist die sichere Richtung, in
verschiedene Richtungen.

**TV1 bleibt byte-identisch.** Sein `v = h'a1001864'` ist `{0: 100}`; mit `D = 100` im
`example-nucleus` ist das exakt `n = D`, also der Default `w = 1`. Alle Layer-01-Testvektoren
bleiben gültig, und `n` liest sich nebenbei als Prozent.

### D38 — Nur `t_exp` gibt Budget frei ⚠️

E-B und `§3.1` definieren das Budget-Set als „nicht abgelaufen, widerrufen eingeschlossen". Über
`superseded` schweigen beide — und der Referenz-Verifizierer liefert für Widerruf und Supersede
denselben `trust_usable = False`.

**Der Angriff:** Ein Bürge setzt `n = D` mit zehn Jahren Laufzeit (maximales Signal, gebundenes
Kapital), supersediert den Vouch per `core/supersede@1` und hat das Budget sofort zurück. Beliebig
oft. Damit ist `t_exp` als ökonomische Entscheidung (D17) wertlos: man wählt immer die längste
Laufzeit und rotiert per Supersede.

Normativ:

> Das **Budget-Set** enthält alle nicht abgelaufenen Vouches — **widerrufen, supersediert und
> `pending` eingeschlossen** —, aggregiert je `(I, J, N)` nach D40. Eine Gruppe verlässt das
> Budget-Set erst, wenn **alle** ihre Mitglieder abgelaufen sind. **Kein selbst-bezüglicher
> Lebenszyklus-Akt gibt Budget frei — Budget folgt der Uhr, nicht dem Willen des Autors.**

Der letzte Satz ist die eigentliche Regel; er schließt jeden künftigen Lifecycle-Akt mit ein.
Ohne D40 wäre er zu scharf: er machte jede Erneuerung zur Straftat gegen sich selbst.

### D39 — Geflaggte Autoren: Policy, nicht Metrik

`01 §4` sagt, Equivocation invalidiert Downstream nicht rückwirkend. Ob ein geflaggter Bürge
Fluss trägt, ist damit Policy und gehört nicht in die Metrik. Normativ: ein Parameter
`include_flagged`, Default **`False`** (sichere Richtung). Gilt für `equivocation-flagged` und
für Über-Commitment.

**Das Budget-Set ist davon unberührt** — ein Flag darf die Budgetrechnung nie ändern, sonst
verschöbe eine Erkennung rückwirkend die Erkennungsgrundlage.

### D40 — Aggregation je `(I, J, N)` über `max n` ⚠️

```
Gruppe(I, J, N) = alle vouch@1-Claims von I auf J im Scope N
n_budget = max n über die Gruppenmitglieder im Budget-Set   (0, wenn leer)
n_kante  = max n über die Gruppenmitglieder im Aktiv-Set     (0 ⇒ keine Kante)

Budget:  Σ_J n_budget(I, J, N)  ≤  D
Kante:   cap(I→J) = ⌊ n_kante · C(I) / D ⌋
```

Weil Aktiv-Set ⊆ Budget-Set gilt, ist stets `n_kante ≤ n_budget`.

**Der Befund.** D38 (Budget-Set inkl. `superseded`, Freigabe nur bei `t_exp`) zusammen mit D4
(Über-Commitment ist selbst-validierend, `05 §3` Stufe 3, mechanischer Slash ohne Verdikt) machte
die gewöhnliche Erneuerung eines Vouch zu einem signierten Beweis gegen den eigenen Autor: wer
`n = D` mit langer Laufzeit setzt und den Claim später ersetzt, hat `Σn = 2D > D`. Auch beim
**Herabsetzen** von `n`. Der Angriff aus D38 ist real, die Regel in Summenform bestrafte aber
jede Korrektur bis `t_exp` — und zwar in derselben Klasse wie Equivocation.

**Warum Gruppierung und nicht Supersede-Kette.** Layer 01 verlinkt den Nachfolger nicht mit dem
Vorgänger: `core/supersede@1` zeigt gezielt auf ein Ziel (`J = [claim-ref, ziel.claim_id]`,
`01 §5.3`), trägt aber keinen Ersatz-Claim. Eine Ketten-Semantik verlangte eine Layer-01-Änderung.
Gruppierung nach `(Autor, Subjekt, Scope)` ist rein lokal, `O(|E|)` und lässt Layer 01
unangetastet.

Vier Wirkungen:

- **Erneuerung und Herabstufung sind frei.** Ein Autor kann seine Aussage jederzeit korrigieren;
  er kann nur ihr Gewicht nicht vorzeitig anderswo einsetzen.
- **Der D38-Angriff bleibt tot.** Das Gruppenmaximum steht bis `t_exp`. Ein Vouch auf ein
  *anderes* Subjekt ist eine andere Gruppe und kostet volles Budget.
- **Fluss folgt dem Willen, Budget folgt der Uhr.** Eine Herabstufung wirkt sofort über
  `n_kante`, nie über `n_budget`. Das ist die Trennung, die D38 behauptet, sauber durchgezogen.
- **Schließt eine bestehende Lücke.** `§2` erzeugte eine Kante *je Claim*, also parallele Kanten
  mit addierten Kapazitäten: zwei aktive Vouches auf dasselbe Subjekt kosteten einfaches Budget
  und trugen doppelte Kapazität. `max` statt Summe beseitigt das.

Teilwissen bleibt sicher: fehlende Claims senken beide Maxima ⇒ Unter-Erkennung, nie
Falschbeschuldigung (D3).

**Verworfen:** Trennung von Ausstellungssperre und slashbarer Klasse (Budget über dem
Budget-Set, Beweis nur über dem Aktiv-Set). Das repariert die Erneuerung ebenfalls, öffnet aber
die Umgehung aus `§3.1`: ein Autor hält Vorgänger zurück oder widerruft reihum und hält seine
aktive Menge stets klein.

### D41 — Budget-Austritt ist ein `t_exp`-Prädikat, kein Zustand

Der `02a`-Prompt verkürzte den Austritt aus dem Budget-Set auf `state == EXPIRED`. Das ist falsch,
und die Spec sagt bereits das Richtige: `02 §3.1` definiert das Budget-Set als „nicht abgelaufen
(widerrufen, supersediert und `pending` eingeschlossen)". **„Nicht abgelaufen" ist ein Prädikat
über `t_exp` und `now`, kein Zustand der Layer-01-Zustandsmaschine.**

Der Fehler war folgenreich, weil `classify()` `REVOKED`/`SUPERSEDED`/`PENDING` **vor** der
Ablaufprüfung entscheidet. Ein einmal widerrufener Claim erreicht `EXPIRED` daher nie. Unter der
Prompt-Fassung bände ein widerrufener Vouch **für immer** Budget — kein konservatives Verhalten,
sondern ein Deadlock: der Autor bekäme die Kapazität nie zurück, und Anker 5 Schritt S2 wäre
unerreichbar.

Normativ:

```
im Budget-Set  ⟺  state ∈ {ACTIVE, REVOKED, SUPERSEDED, PENDING}
                  UND (t_exp fehlt ODER now ≤ t_exp)
```

Die Ablaufbedingung wird **unabhängig vom Layer-01-State** geprüft. Die Grenzkonvention ist
`now ≤ t_exp` und stimmt mit dem Verifizierer überein — gleiche Konvention, zwei
Auswertungsstellen. Das ist der Preis dafür, dass Layer 01 eingefroren ist; die Kopplung ist
dokumentiert und getestet, aber sie ist eine Kopplung. Ändert Layer 01 je seine Ablaufkonvention,
muss Layer 02 mitgezogen werden.

### D42 — Vouch-Kanten tragen im Disjunktheitslauf Kapazität 1, nicht ∞ ⚠️

Korrigiert D32. Die dortige Belegung „interne Kanten `1`, Vouch-Kanten `∞`" ist **defekt**, aus
zwei unabhängigen Gründen.

**Der Sentinel ist nicht wohldefiniert.** `INF = Σ(endliche Kapazitäten) + 1` war gegen den
Kapazitätslauf definiert. Im Einheitslauf sind die Vouch-Kanten selbst die ∞-Kanten; „Summe der
endlichen" ist dort zirkulär.

**Ohne Zwischenknoten degeneriert jeder Pfad.** Anker intern ∞ (D31/D32), Vouch-Kante ∞, Ziel
intern wegen D30 nicht auf dem Pfad — jede Kante des Pfades trägt ∞, und der Solver liefert den
Sentinel statt einer Pfadzahl. In `TP-BOOT` bürgen die Gründer **direkt** für die Neulinge; es
gibt keinen Zwischenknoten. Gemessen wurden 219 statt 1. In `TP-02` fällt es nicht auf, weil BOB
und CAROL dazwischenliegen — die Konvention wurde an einem Graphen entworfen, der den Fehler
nicht zeigen kann, und `TP-BOOT` stand mit seiner Disjunktheitsspalte daneben, ohne dass der
Widerspruch auffiel.

Normativ:

| Lauf | interne Kanten | interne Kanten der Anker | Vouch-Kanten |
|---|---|---|---|
| Fluss | `C(d(x))` | `C(0)` wie alle | `⌊n_kante·C(I)/D⌋` |
| Disjunktheit | `1` | `INF` | **`1`** |

**Die Änderung ist beweisbar verlustfrei.** Zwei knotendisjunkte Pfade teilen nie eine Kante —
teilten sie `I→J`, teilten sie die Knoten `I` und `J`. In jedem knotendisjunkten Pfadsystem trägt
also jede Kante höchstens eine Einheit. Die Kappung entfernt kein gültiges Pfadsystem und lässt
keines zusätzlich zu. Sie ist äquivalent, wo ∞ wohldefiniert war, und wohldefiniert, wo ∞ es
nicht war. Wegen D40 existiert ohnehin nur eine Kante je Paar, es entsteht keine
Aggregationsfrage.

Die Endpunkt-Regel aus D32 bleibt unberührt: die internen Kanten der Anker tragen weiterhin
`INF`. `TP-FAN` prüft, dass die Kappung sie nicht mitgekappt hat.

### D43 — Equivocation ist global, Über-Commitment ist scope-gebunden

D39 nennt zwei Flags, ohne ihren Geltungsbereich zu klären. Sie unterscheiden sich, und zwar
zwingend:

- **Equivocation** ist eine Aussage über die **Hash-Kette einer Identität** — zwei Claims mit
  demselben `h_prev`. Die Kette ist scope-übergreifend, also ist der Befund es auch. Ein Autor,
  der in *irgendeinem* Scope äquivoziert, hat seine Kette gebrochen; das ist keine Eigenschaft
  eines Scopes.
- **Über-Commitment** ist `Σ n_budget ≤ D` je Scope, und `D` ist scope-fest (D35). Der Befund
  kann gar nicht anders als scope-gebunden sein.

Normativ: bei `include_flagged = False` trägt keine Kante eines Autors, der (a) in irgendeinem
Scope `equivocation-flagged` ist **oder** (b) im **abgefragten** Scope über-committet ist. Das
Budget-Set bleibt in beiden Fällen unberührt (D39).

### D44 — Subgranularität gilt nur für erreichbare Autoren

Ein Befund „Kante ohne Durchsatz" entsteht genau dann, wenn ein Autor mit `d(I) < ∞` eine Gruppe
mit `n_kante ≥ 1` trägt, deren Kapazität `⌊n_kante·C(I)/D⌋` null ist.

Bei `C(I) = 0` wegen **Unerreichbarkeit** ist die Ursache nicht Granularität, sondern Position.
Ein Subgranularitäts-Befund wäre dort eine Falschaussage über die Ursache und würde bei jeder
Abfrage für jeden nicht erreichten Teil des Stores feuern — Rauschen proportional zur
Store-Größe statt einer Aussage über den ausgewerteten Graphen.

Folge für D39: Der Befund ist damit **flag-abhängig**. Fällt die Kante eines geflaggten Autors
weg, verschlechtern sich stromabwärts die Distanzen, sinken die Kapazitäten, und Kanten rutschen
unter die Granularitätsgrenze. Das ist konstruktiv so — die Budgetbefunde bleiben flag-invariant,
der Subgranularitätsbefund nicht.

### D45 — `P` ist sub-stochastisch, ohne Rückführung ⚠️ (korrigiert D27)

`§5` schrieb „spaltenstochastisch normalisiert" über `Σw`. Die Fassung hat zwei Defekte.

**Der absolute Pegel von `w` verschwindet.** Normalisiert man je Knoten über `Σn`, kürzt sich
`D` heraus. Ein Autor mit **einer** ausgehenden Kante und `n = 1` bei `D = 100` bekommt
`P = 1` — exakt wie bei `n = 100`. Damit erreicht D27 sein erklärtes Ziel nicht: der
Probe-Vouch mit `w = 0.05` wird sehr wohl wie eine volle Bürgschaft behandelt, sobald er
allein steht. Die Begründung von D27 trug die Regel von D27 nicht.

**Die Monotonie aus `§7` bricht.** Eine zusätzliche Kante von `I` senkt den Anteil jeder
bestehenden Kante von `I`. Umkehrschluss: **fehlendes Wissen hebt fremde Werte** — wörtlich
der Defekt, den D9 als nicht reparierbar verworfen hat. Erschöpfend gemessen an Variante B
(alle 32 Teilgraphen): **9 Verletzungen** unter der alten Fassung, **0** unter der neuen.

Normativ:

```
P[J][I] = n_kante(I, J) / D          — absolut, keine Kopplung an andere Kanten
Sigma t <= 1 − (1 − alpha)^K         — das Defizit ist das ungenutzte Budget
```

**Keine Rückführung des Defizits.** Die zunächst gewählte Fassung leitete das Defizit auf den
Restart-Vektor, um `Σt = 1` zu erhalten. Sie ist überflüssig: mit `T = (I − (1−α)Pᵀ)⁻¹` ist
der Fixpunkt mit Rückführung `t = (α + (1−α)ℓ(t))·T·e_s` und ohne `t' = α·T·e_s`; weil `ℓ(t)`
ein **Skalar** ist, gilt `t = (s/α)·t'`. Beide Fixpunkte sind proportional — gleiche Ordnung,
gleiche Verhältnisse, nur andere Normierung. Die Rückführung kostet einen Rang-1-Term je
Iteration und ein `min()` je Knoten und ist zudem ein Informationsverlust: ohne sie ist
`1 − Σt` das ungenutzte Budget, als Zahl lesbar (Anker PR-5).

**Die D9-Ausnahme entfällt ersatzlos.** Es gibt keine Normalisierung über `Σw` mehr. Der
Sonderstatus von `§5` gegenüber D9 wird gestrichen, nicht umformuliert — `§5` ist damit frei
von der Kopplung, die D9 verbietet, und `§7` gilt in **beiden** Sichten.

**Nebenwirkung:** Dangling Nodes sind kein Fall. Ein Knoten ohne ausgehende Kante in `E⁺`
reicht nichts weiter; die bei ihm angekommene Masse bleibt bei ihm.

### D46 — Exakte Integer-Arithmetik über festem Nenner

```
u_0[J]     = 0
u_{k+1}[J] = a·D·(b·D)^k · [J in A]  +  (b−a) · Sum_{(I,J) in E+} u_k[I] · n_kante(I,J)
t[J]       = u_K[J] / Delta_K              Delta_K = |A| · (b·D)^K,  alpha = a/b
```

Der Streckfaktor je Runde ist `Δ_{k+1}/Δ_k = bD`; damit sind Restart- und Transferterm
ganzzahlig, und `|A|` kürzt sich aus der Rekursion heraus. **Es gibt an keiner Stelle eine
Division, also keine Rundung und keine Rundungsrichtung.** Kein `Fraction`, kein `decimal`,
kein `float` — dieselbe Aussage wie D28/D29, ein zweites Mal.

Nur unter D45 ist das billig: die spaltenstochastische Fassung hätte knotenweise Nenner
`Σn_I`, deren kgV unkontrolliert wächst. Dann bliebe Festkomma mit Abrundung je
Multiplikation, samt Rundungsrichtungs-Fork und Fehlerakkumulation. **Das ist das praktische
Argument für D45, unabhängig vom prinzipiellen.**

Bei `TP-02` (`a=1, b=2, D=4, K=20`) ist `Δ = 8²⁰ = 2⁶⁰` — unter `2⁶³` und damit auch in einer
Sprache ohne Bigints darstellbar.

### D47 — Feste Rundenzahl, `t₀ = 0`

Mit `t₀ = 0` ist `t_K = α · Σ_{i=0}^{K−1} (1−α)^i (Pᵀ)^i e_s` die abgeschnittene
Neumann-Reihe. Bei sub-stochastischem `P` gilt `‖t_K − t_*‖₁ ≤ (1−α)^K`, und die Folge ist
**monoton wachsend** in `K` — jeder Abbruch ist eine Untergrenze und damit die sichere
Richtung.

`t₀ = e_s` wäre die naheliegendere Wahl und ist schlechter: die Schranke verdoppelt sich auf
`2(1−α)^K`, die Monotonie in `K` geht verloren, und `u₀` ist teurer.

**Normativ ist `t_K`, nicht `t_*`.** Der Fixpunkt ist die Motivation, nicht die Definition.
Nur so ist der Wert exakt und byte-reproduzierbar. Ein Konvergenztest zur Laufzeit ist damit
verboten: er machte das Ergebnis implementierungsabhängig.

`K` folgt aus `α` und der Zielgenauigkeit: `K = ⌈log ε / log(1−α)⌉`. Für `α = ½, ε = 2⁻²⁰`
ist `K = 20`.

### D48 — `α = 1 − γ` als Profilkopplung

Entlang eines Pfades zerfällt die Masse in `§5` wie `(1−α)^d`, die Kapazität in `§3` wie
`γ^d`. Mit `α = 1 − γ` zerfällt `§5` **mindestens** so schnell wie `§3` — schneller, weil
sich die Masse zusätzlich über die Kanten aufteilt. Das ist die sichere Richtung, und das
Profil hat einen Knopf weniger.

Der Standardwert `α = 0.15` aus der Suchmaschinenliteratur ist auf globale Reichweite
kalibriert und steht quer zum Lokal-Ethos aus `§1`/`§8` („Default eher schnelles Abklingen").

**SHOULD, nicht MUST.** `§5` trägt keine Schranke, also ist die Kopplung nicht beweisbar —
sie ist begründbar und dokumentierbar, mehr nicht. Eine Policy darf `α` unabhängig setzen;
sie sollte es begründen. Für `γ = ½` folgt `α = ½`, also `a = 1, b = 2`.

### D49 — `§5` läuft über demselben Kantensatz wie `§4`

Gruppen-Aggregation `max n` (D40), `E⁺`-Filter (D36) und Flag-Anwendung (D39) gelten
unverändert. `§5` selbst sagt es: „Beide Sichten teilen denselben Graphen."

Drei Klarstellungen, die im Code sonst schiefgehen:

- **`C(x)` geht in `§5` ein, aber nur als Filter, nie als Faktor.** Ohne `E⁺` wäre der
  D36-Angriff eins zu eins übertragbar: drei Kolludierende mit `n = 1` bei `d = 2`, die in
  `§4` exakt null Fluss tragen, bekämen volle Übergangswahrscheinlichkeit. Eine Gewichtung
  mit `cap(e)` statt `n_e` wurde geprüft und verworfen — knotenweise kürzt sich `C(I)` bis
  auf Rundungsartefakte weg, das kauft nichts und bringt Rauschen.
- **Kein Knoten-Splitting.** Der Split ist eine Max-Flow-Konstruktion für Knotenkapazitäten;
  `§5` hat keine. Wer den `02a`-Graphbauer arglos wiederverwendet, rechnet über einer
  verdoppelten Knotenmenge und bekommt einen zusätzlichen `(1−α)`-Faktor je Hop. Belegt durch
  Anker PR-4 (`TP-FAN`).
- **Das Budget-Set spielt keine Rolle.** `§5` liest `n_kante` aus dem Aktiv-Set. Das
  Budget-Set dient der Über-Commitment-Erkennung, und die geschieht vor der Sichttrennung.

Folge für die Implementierung: `02b` teilt die Ableitungsstufe mit `02a` und beginnt danach.

### D50 — „Nie über-vertrauend" ist eine Kanalaussage, keine Wertaussage ⚠️ (präzisiert D27)

`§4` liefert Fluss in Kapazitätseinheiten, `§5` stationäre Wahrscheinlichkeitsmasse. **Die
Größen sind nicht kommensurabel.** „`§5 ≤ §4`" ist punktweise nicht formulierbar, und die
Ordnungen stimmen im Allgemeinen auch nicht überein: `§4` misst Engpässe, `§5` misst
Erreichbarkeitsmasse.

Prüfbar ist allein, dass `§5` **keinen Signalkanal ignoriert, den `§4` benutzt, um einen Wert
zu senken**:

| Kanal | Regel |
|---|---|
| Gewicht `w` | D45 |
| wirksames Kantenset `E⁺` | D36/D49 |
| Gruppenmaximum `n_kante` | D40/D49 |
| Flag | D39/D49 |

Vier Kanäle, vier Tests. Ohne diese Präzisierung steht in `§5` und D27 ein Satz, den niemand
widerlegen und niemand prüfen kann — und die nächste Abnahme sucht vergeblich nach dem
Testvektor.

### D51 — Restart-Vektor gleichverteilt über das Ankerset

`e_a = 1/|A|` für `a ∈ A`, sonst `0`. Eine gewichtete Fassung bräuchte einen Mechanismus, aus
dem Gewichte kämen; `§6.3` kennt keinen.

**Zu benennende Asymmetrie:** in `§4` hängt der Super-Source mit ∞ an *jedem* Anker — ein
zweiter Anker kann den Wert nur heben. In `§5` verdünnt ein zweiter Anker den ersten: das
Hinzufügen eines Ankers kann einen Knotenwert **senken**. Das ist kein `§7`-Bruch (`§7`
handelt von Kanten), aber ein echter Verhaltensunterschied zwischen den Sichten. Er gehört
ins Register, nicht in einen Codekommentar.

### D52 — Die Oberfläche trägt die Trennlinie aus `§9`

`§9`: „PageRank nur als Relaxation — bei Missbrauch für harte Gates verliert man die
Schranke. Diese Trennlinie ist nicht verhandelbar." Im Code ist die Oberfläche die einzige
verfügbare Durchsetzung.

Normativ: eigenes Modul, eigener Name, eigener Rückgabetyp. **Nicht `trust`, nicht
`TrustResult`.** Der Rückgabetyp führt `Δ` mit; wer eine Schwelle vergleichen will, muss sich
sichtbar dafür entscheiden.

Mehr ist mechanisch nicht zu haben, und das steht so in der Spec, statt Sicherheit zu
suggerieren.

### D53 — Kein Clamp für über-committete Autoren ⚠️

Ohne Deckel kann ein über-committeter Autor (`Σn_I > D`) in `§5` Masse **erzeugen**. Gemessen
an Variante D (`gᵢ` mit `Σn = 8 > 4`): `t(gᵢ) = 17/64` gegen `131071/4194304` in der
budgetgültigen Variante C, und `Σt = 107/64 > 1`. `§4` liefert für beide `3/3/3` (INV-5).
Die schnelle Sicht überzeichnet also um das Achtfache.

**Jede Reparatur wurde geprüft und verworfen.** Ob `n/max(D, N_I)` oder `ñ = ⌊n·D/N_I⌋` — der
Anteil einer Kante hinge an den **anderen** Kanten desselben Autors. Das ist wörtlich der
D9-Defekt: bei Teilwissen ist `N_I` zu klein, der Clamp greift nicht, und fehlendes Wissen
hübe Werte. Wir hätten die Monotonie, für die D45 überhaupt gewählt wurde, gegen einen
Randfall wieder eingetauscht.

Zwei Eigenschaften erledigen den Fall stattdessen:

- **Der Default schützt.** `include_flagged = False` entfernt die Kanten über-committeter
  Autoren. Gemessen: Variante D mit `False` ist **byte-gleich mit B**. Wer `True` setzt, sagt
  ausdrücklich „ich weiß, dass dieser Autor über-committet ist, und will ihn trotzdem
  zählen", und trägt die Deutung.
- **Die Massenbilanz ist ein Detektor, kostenlos.** Bei budgetgültigem Kantensatz gilt per
  Induktion `Σt ≤ 1 − (1−α)^K`. Also:

  ```
  Sigma t > 1 − (1 − alpha)^K   ==>   ein einbezogener Autor ist ueber-committet
  ```

  Einseitig — kein Falschalarm, nur Unter-Erkennung. Exakt D3, exakt die Richtung, die `§3.1`
  für das beobachtete `Σw` schon festhält. Eine Summe, die ohnehin gebildet wird.

**Getragene Grenze:** `§5` ist gegen einen über-committeten Autor bei `include_flagged = True`
nicht konservativ. Das ist die dokumentierte Grenze der Relaxation und gehört in `§9` zu den
bewusst getragenen v1-Grenzen.

### D54 — Die Massenschranke exakt und profilunabhängig

Die Schranke aus D45 lautet `Σt ≤ 1 − (1−α)^K`. `02b-golden-anchors.md` Rev 1 gab dafür keine
ganzzahlige Form an, und die naheliegende Umsetzung `Δ − Δ // 2^K` ist **profilabhängig**: sie
ist nur exakt, wenn `2^K` den Nenner `Δ = |A|·(b·D)^K` teilt — also genau für `α = ½`.

Der Implementierer hat das in der `02b`-Abnahme gemeldet. Die allgemeine Form ist exakt und
für jedes `α` ganzzahlig, weil sich `b^K` vollständig gegen `Δ` kürzt:

```
Delta * (1-alpha)^K  =  |A| * (b*D)^K * (b-a)^K / b^K  =  |A| * D^K * (b-a)^K

mass  <=  Delta - |A| * D^K * (b-a)^K
```

Ein Produkt aus Ganzzahlen, ohne Division und ohne Fallunterscheidung.

Nachgerechnet bei `TP-02` (`|A| = 1, D = 4, K = 20, b−a = 1`): `2⁶⁰ − 2⁴⁰ =
1152920405095219200`, identisch zur profilabhängigen Form, und Variante F erreicht die
Schranke mit **Gleichheit**. Gegenprobe an einem Profil, in dem die alte Form bricht
(`α = 1/3, D = 6, K = 7, |A| = 2`): `Δ = 1224440064`, Schranke `1152776448`; `Δ // 2^K` ist
dort bedeutungslos, weil `(1−α)^K` den Nenner `3^7` trägt.

**Dieselbe Klasse wie D41/D42:** eine Zahl in den Vorgaben, die der kanonische Testgraph nicht
widerlegen konnte, weil das Profil der Sonderfall ist. `α = ½` ist der einzige Wert, unter dem
der Fehler unsichtbar bleibt — und es ist der Default (D48). Ein Profil mit `α = 1/3` hätte
ihn sofort gezeigt; genau deshalb steht ein solcher Vektor jetzt als offener Punkt in
`02b-golden-anchors.md §11`.

Normativ ist die Produktform. Sie ersetzt jede Fassung mit `//`, auch dort, wo die Division
zufällig aufgeht.

---

## K. Aus der Forkanalyse Layer 03 (Profile II — Verdikt · Wert · Mitgliedschaft)

Fünfzehn Forks aus 183 Zeilen. Drei der zehn eingebrachten Punkte waren bereits in `00`
entschieden und in `03` nur nicht nachgezogen — `03-profiles.md` ist im Bestand die älteste
Profil-Datei, und ihre Antworten sind nach `00` gewandert, ohne dass sie mitkam. Ein
Widerspruch zwischen zwei Dateien auf `main` wurde dabei sichtbar (→ D68).

**Vorab geklärt (kein Befund):** `trust()` mit leerem Ankerset auf Variante A liefert
`OVERCOMMITTED_AUTHOR` für CAROL, byte-identisch zum Lauf mit ALICE-Anker. INV-8 hält in
Layer 02a. Der Vektor aus `02b-golden-anchors.md §11` ist fällig, nicht offen, und gehört
nach `tests/trust/test_invariants.py`.

---

### D55 — `v`-Kodierung der Layer-03-Profile: typ-normativ, bedeutungsblind

Der Keyraum von `v` ist **prädikat-lokal**. `v` ist für das Atom opak; ein Key trägt nur
innerhalb seines Profils Bedeutung. Key `0` in `vouch@1` und Key `0` in `obligation@1` sind
verschiedene Dinge und kollidieren nicht.

```
obligation@1   0 : uint   amount      uninterpretiert
               1 : bstr   unit_ref    byte-vergleichbar, nie geparst
receipt@1      0 : uint   amount      löst KEINE Tilgung aus (D65)
verdict@1      0 : uint   outcome     Bedeutung ist Policy
               1 : bstr   reason_ref
accusation@1   keine reservierten Keys — vollständig opak (D67)
```

**Normativ ist der Typ, nicht die Bedeutung.** Ist ein reservierter Key vorhanden, MUSS er den
deklarierten Typ tragen; ein Verstoß erzeugt ein Finding, keinen Reject. Fehlt der Key, ist das
kein Fehler. Weitere Keys sind zulässig und opak. Das ist exakt die Bauform aus D37: geprüft
wird der Key, nicht die Map als Ganzes.

**Verworfen — vollständig opak.** Dann gäbe es in `03` keinen einzigen Byte-Vektor. Die
`02b`-Abnahme lief beim ersten Versuch durch, weil die Golden Numbers exakt und rundungsfrei
waren; eine Schicht ohne prüfbare Bytes hat kein Äquivalent dazu und fällt auf „der Code stimmt
mit sich selbst überein" zurück.

**Verworfen — semantisch normativ** (Beträge werden gelesen und verglichen). Bricht die
Preisblindheit aus `03 §3.1` und A2, und braucht eine Einheiten-Registry, die es nicht gibt.
Wäre nur nötig, wenn ungedeckte Emission eine mechanische Schranke bekäme — sie bekommt keine
(D66).

### D56 — Vouch-`v` Key `1` wird vertagt, Key `2` nur typ-fest

D37 sagte, die Kodierung der Keys `1` (Zweck-Tag) und `2` (`bond_ref`) werde „mit `03`/`05`
festgelegt". Das war eine Terminplanung, keine Ableitung. **Key `1` ist Layer-02-Semantik und
hat in `03` keine Verwendung.**

Er ist außerdem teurer als er aussieht. Sobald er kodiert ist, ziehen drei Dinge nach:

1. `trust()` und `rank()` brauchen einen `purpose`-Parameter. Er fehlt in beiden Signaturen.
2. Der Gruppenschlüssel aus D40 ist `(I, J, N)`. Mit Zweck-Tag muss `n_kante` über der
   **gefilterten** Teilmenge maximiert werden, sonst erbt ein Probe-Vouch für `π₁` das Gewicht
   eines vollen Vouch für `π₂` — die falsche Richtung, und zwei Implementierungen laufen dort
   legitim auseinander.
3. Das Budget bleibt `(I, N)` über **alle** Zwecke, sonst kauft ein Autor durch Zweck-Splitting
   neues Budget. Das ist zugleich die Begründung, warum D25 für Torwächterschaft eigene
   *Scopes* verlangt und nicht eigene Zwecke.

**Beschluss:** Key `1` bleibt unkodiert bis zu einem eigenen Durchgang `02c-purpose`, nach `03`.
Key `2` bekommt jetzt nur den Typ — `2 : bstr`, Länge 32, nie dereferenziert —, damit `03` und
`05` denselben Slot nicht verschieden belegen. Kein Testvektor, keine Wirkung.

### D57 — Die Policy ist Parameter der Klassifikation und wird aus dem Claim aufgelöst ⚠️

`01 §5.4` und `§6` sagen beide, eine Nukleus-Policy dürfe die Aktiv-Sicht überschreiben. Die
eingefrorene Signatur `classify(claim, store, now)` hat dafür keinen Ort. Der Satz war zwei
Layer lang dekorativ und fällt erst auf, weil `03` ihn braucht: ohne ihn ist `03 §3.3.3`
(`obligation@1` irrevocable) unauswertbar, und das Schulden-Lösch-Loch bleibt offen.

```python
def classify(claim, store, now, policy: NucleusPolicy | None = None) -> Classification: ...
```

**Der Aufrufer wählt die Policy nicht — sie wird aufgelöst.** Der Claim trägt `N`; `N` bestimmt
das Genesis; das Genesis bestimmt `constitution_hash`; die Verfassung bestimmt
`irrevocable_predicates` (`00 §5`). Ist das Verfassungsobjekt lokal nicht bekannt (Partition),
greift der Sicherheits-Default aus `00 §5.2`: **exakt** `["obligation@1"]`, nichts sonst.

**Warum kein Wrapper in `03` (Variante b).** Die Regel muss unumgehbar sein. Ein Wrapper ist es
nie: jeder Aufrufer, der ihn vergisst, reißt das Loch wieder auf — genau der Fehlermodus, vor
dem `03 §5` warnt. Zusätzlich entstünde eine zweite Definition von „aktiv" neben `02 §2`, und
zwei Definitionen driften.

**Warum kein Store-Filter (Variante c).** Revokes zu verstecken bricht A3 und `01 §5.2`: sowohl
der Claim als auch sein Widerruf bleiben sichtbar.

**Der Preis, offen benannt:** Layer 01 wird für einen additiven Parameter mit Default
aufgetaut. Feldsatz, Serialisierung, Signatur, elf Reject-Codes und acht Zustände bleiben
unberührt; `policy=None` ist die heutige Semantik, die 61 Tests bleiben grün. Der Durchgang
heißt `01a-policy` und läuft **vor** `03`, weil drei `03`-Funktionen den Parameter nehmen.

### D58 — Trust-gewährende Prädikate dürfen nicht irrevocable sein ⚠️

`00 §5` deklariert `irrevocable_predicates` als freies `array[text]`. Ein Nukleus, der dort
`vouch@1` einträgt, macht Widerrufe wirkungslos — also genau die **eine gefährliche Richtung**
aus `02 §7`, und zwar permanent und strukturell statt nur partitionsbedingt.

> **Normativ:** Irrevocable darf nur ein Prädikat sein, dessen **Fortbestehen** die konservative
> Lesart ist. Steht `vouch@1` in `irrevocable_predicates`, ist die Deklaration unwirksam: Finding
> `UNSAFE_IRREVOCABLE_PREDICATE`, und Widerrufe wirken weiterhin.

Für `obligation@1` ist Fortbestehen konservativ (die Schuld bleibt stehen), für `vouch@1` ist es
das Gegenteil (Vertrauen bleibt stehen). Die Asymmetrie ist der ganze Punkt und stand nirgends.

Testvektor: eine Verfassung, die es versucht.

### D59 — `obligation.t_exp` bleibt erlaubt, wird aber zum Finding

`03 §3.3.1` erlaubt `t_exp` als „harte Decke". Zusammen mit `§3.3.3` ergibt das: der Schuldner
kann seine Schuld nicht widerrufen, darf sie aber bei Ausstellung so programmieren, dass sie
von selbst verfällt. Irrevocability schützt gegen den **nachträglichen** Willen, nicht gegen
den vorprogrammierten.

Entschärft ist es dadurch, dass die Obligation einseitig ist: es gibt keine signierte Annahme
des Gläubigers, also trägt er die Prüfpflicht ohnehin, und `t_exp` ist für ihn vor der Lieferung
sichtbar.

**Beschluss:** erlauben, aber sichtbar machen. Eine `obligation@1` mit `t_exp` erzeugt
`EXPIRING_OBLIGATION`. Bedeutungsblind, billig, und es macht die Falle für Werkzeuge lesbar.

**Verworfen — Policy-Verbot.** Befristete Verpflichtungen sind ein legitimer Fall (`06 §5`,
SLA-Fenster). Ein Verbot verlöre mehr, als es schützt.

### D60 — Mitgliedschaft hat vier Zustände, nicht zwei

```python
def membership(store, *, subject, scope, constitution_hash, now,
               authorized_keys, policy=None) -> MembershipResult
```

```
MEMBER        beide Claims aktiv
APPLICANT     nur accept-rules aktiv
GRANT_ONLY    nur grant-membership aktiv
NONE          keiner
```

**Kein bool.** `05 §1` Stufe 4 unterscheidet Ausschluss (N widerruft den Grant) von Austritt
(X widerruft die Annahme); mit einem Wahrheitswert sind beide `False` und nicht
auseinanderzuhalten. `03 §4` nennt `GRANT_ONLY` „ungültig" — das ist richtig als Wirkung, aber
der Zustand muss benennbar bleiben.

`MembershipResult` trägt zusätzlich die beiden `claim_id` und `findings`, in der Form von
`TrustResult`.

**„Aktiv" heißt dasselbe wie `02 §2`** — Layer-01-`active`, `pending` zählt nicht —, ausgewertet
unter der Policy aus D57. Da weder `accept-rules@1` noch `grant-membership@1` irrevocable sind,
fallen beide Begriffe in `03` faktisch zusammen; die Regel steht trotzdem einmal geschrieben,
sonst driftet sie beim nächsten Prädikat.

### D61 — Der `constitution_hash` ist Parameter, nicht Auflösung

`accept-rules@1.J = [object-hash, H(Verfassung)]` bindet eine Mitgliedschaft an eine **Version**.
Nach einem Amendment sind alte Annahmen strukturell weiter aktiv, zeigen aber auf den falschen
Hash. Welcher Hash gilt, entscheidet die Ratifizierung über die `amendment`-Schwelle
(`00 §5.3`) — eine Layer-04-Frage.

**Beschluss:** `membership()` nimmt `constitution_hash` als Parameter und vergleicht byte-weise.
`03` löst nicht auf, welche Version aktuell ist. Damit bleibt `03` frei von Layer 04 und
bedeutungsblind.

Testvektoren gegen den Bestandsanker aus `00 §3.1`: `890b21e7…` ⇒ `MEMBER`; ein abweichender
Hash ⇒ die Annahme zählt für diese Version **gar nicht**, also `GRANT_ONLY` bzw. `NONE`.

### D62 — `resolve_current_key` gehört nicht in `03`

`00 §7` ersetzt die alte Regel `I == N` durch `akt.I ∈ resolve_current_key(akt.N)`. Damit ist
die Frage „trägt `03` einen Gruppenschlüssel?" beantwortet und zwar mit **nein**: `key_mode = 1`
bedeutet einen FROST-Gruppenschlüssel, und eine FROST-Signatur verifiziert als gewöhnliche
Ed25519-Signatur unter diesem Schlüssel. Layer 01 bleibt unberührt. Die Tabelle in `03 §4`
(`I = N`) ist toter Text und wird ersetzt.

`resolve_current_key` selbst ist eine Kettenauflösung über `rotate-key@1` ab `root_keys`, mit
eigenen Equivocation-Fällen (`01 §8`: ein gestohlener Schlüssel, der zwei Nachfolger signiert).

**Beschluss:** `03` nimmt `authorized_keys: frozenset[bytes]` als Parameter.
`resolve_current_key` und `rotate-key@1` bekommen einen eigenen Durchgang `00a`. Sonst zöge `03`
die Schlüsselrotation samt Diebstahlsfällen herein — ein größerer Brocken als alle drei Cluster
zusammen.

**Ebenfalls ausgeklammert:** der Kompositionspfad aus `04 §3` (`vote_mode = 0`), bei dem eine
Mitgliedschaft ohne einzelnen `grant-membership`-Autor durch Auszählung entsteht. `03` wertet
nur den claim-basierten Pfad. Getragene Grenze, in `03 §5` zu nennen.

### D63 — „Passende" Quittung ist ein vierteiliges strukturelles Prädikat

`03 §3.3.2` verlangt eine „passende" Quittung, ohne sie zu definieren.

```
receipt.J  == [claim-ref, obligation.claim_id]
receipt.I  == obligation.J.value    und  obligation.J.tag == identity
receipt.N  == obligation.N
beide aktiv (Obligation unter der Policy aus D57)
```

Die dritte Bedingung ist **nicht** redundant. `01 §2.2` Regel 3 erzwingt nur, dass `N` gesetzt
und selbstkonsistent ist, nicht dass zwei Claims denselben Scope teilen. Ohne sie quittiert eine
Identität in Nukleus B eine Schuld aus Nukleus A.

Trennende Vektoren: Quittung vom Schuldner statt vom Gläubiger; Quittung mit fremdem `N`;
Quittung auf eine Obligation, deren `J.tag` `claim-ref` statt `identity` ist.

### D64 — Die Quittung bleibt widerrufbar

Aus D63 folgt eine Asymmetrie, die nirgends stand: die Obligation ist irrevocable, die Quittung
nicht. Der Gläubiger kann quittieren und den Widerruf nachschieben — die Schuld lebt wieder auf.
Tilgung ist damit **nicht monoton**.

**Beschluss: getragen.** Die Quittung bleibt per A3 sichtbar, ihr Widerruf ist selbst Evidenz,
und der Missbrauch ist ein oracle-abhängiger Streit — also genau der Fall, für den `§2.3` das
Verdikt vorsieht. Gehört als getragene Grenze in `03 §5`.

**Verworfen — `receipt@1` ebenfalls irrevocable empfehlen.** Sieht sicherer aus und erzeugt den
schlechteren Fehlerzustand: eine irrtümliche Quittung wäre unheilbar, und die Korrektur wäre
eine neue `obligation@1` des Gläubigers — also eine Schuld, die es nie gab.

### D65 — Teil-Tilgung: ein `amount` im Receipt tilgt nicht

`03 §5` („in v1 nicht modelliert") und `§3.3.2` („optional, z. B. Teilbetrag") widersprechen
sich in derselben Datei. Die naive Auflösung — `receipt.v` opak lassen und jede Quittung als
Voll-Tilgung werten — ist die gefährliche: ein Gläubiger, der einen Teilbetrag meint, quittiert
versehentlich die ganze Schuld. Über-Tilgung, also die falsche Richtung.

> **Normativ:** Trägt `receipt.v` Key `0`, **tilgt die Quittung nicht** und erzeugt
> `PARTIAL_RECEIPT_UNSUPPORTED`. Die Schuld bleibt stehen.

Sichere Richtung, testbar, und der Erweiterungspfad bleibt offen, ohne dass v1 rät. `§3.3.2`
wird auf diese Formulierung nachgezogen, `§5` bleibt.

### D66 — Ungedeckte Emission ist auditierbar, nicht selbst-validierend

`03 §3.3.4` zieht die Parallele zum Über-Commitment aus `02 §3.1`. Dort trägt sie die
Deckungsgrenze `Σn ≤ D`. Hier gibt es keine — die Parallele trägt nicht.

**Beschluss:** `§3.3.4` umformulieren. „Beweisbar" heißt hier **auditierbar** (der signierte
Schuldgraph ist vollständig nachvollziehbar), nicht **selbst-validierend**. Kein mechanischer
Slash, kein Stufe-3-Auslöser in `05 §3`.

**Verworfen — Schranke `Σ amount ≤ credit_limit(I)` aus der Verfassung.** Der Grund ist nicht
der Aufwand: die Prüfung wäre in genau dem Sinn bedeutungsblind, in dem `n ≤ D` es ist, ein
Integer-Vergleich ohne Interpretation. Der Grund ist, dass die Grenze willkürlich wäre.
`Σw ≤ 1` ist ökonomisch begründet, weil es **Haftung** bindet (D3, D5). Eine Emissionsgrenze
bindet nichts. In einem Mutual-Credit-System setzt der **Gläubiger** das Limit pro Trustline,
nicht die Verfassung pro Person; diese Form gehört in eine Wert-/Exchange-Schicht, die es nicht
gibt (L4: im Protokoll so wenig wie möglich fixieren).

**Namensbereinigung.** `Über-Commitment` (Vouch-Budget, D4, mechanisch slashbar) und
`Über-Emission` (IOU, sozial) unterscheiden sich um zwei Silben und um die gesamte Konsequenz.
Da `05 §3` laut Änderungsliste G „Über-Commitment ⇒ Stufe 3" bekommt, stehen beide bald in
derselben Datei. `Über-Emission` wird durchgängig zu **`ungedeckte Emission`**.

### D67 — Verdikt-Status ist eine Funktion, und `submit-arbitration@1` ist ein Profil

Drei Teile.

**(a) Die Funktion.** `00 §5.1` ist bereits maschinenlesbar formuliert und nennt sich selbst
„die maschinenlesbare Antwort auf E-1"; `05 §3` hängt daran. Also implementieren:

```python
def verdict_status(store, *, verdict, scope, arbitrators, now,
                   policy=None) -> VerdictStatus   # BINDING | ATTRIBUTED_OPINION
```

**(b) Parteienauflösung.** Pfad (ii) verlangt, dass **beide Parteien** vorab gezeigt haben. Wer
sie sind, stand nirgends. Normativ: Ankläger ist `accusation.I`. Der Beschuldigte ist
`accusation.J.value`, falls `J.tag == identity`; bei `J.tag == claim-ref` ist es der **Autor**
des bestrittenen Claims. Je ein Vektor.

**(c) `submit-arbitration@1` bekommt eine Profiltabelle.** `03 §2.4` nennt es beiläufig
„optional", `00 §5.1` macht es zur normativen Bedingung für Pfad (ii). Ohne Tabelle ist der
Absatz nicht auswertbar.

| Feld | Belegung |
|------|----------|
| `I`  | die sich unterwerfende Partei |
| `J`  | `[identity, schiedsrichter]` |
| `N`  | **Pflicht** — der Schlichtungs-Kontext |
| `v`  | opak |

Lebenszyklus über `core/revoke@1`, selbst-bezüglich. Bindung ist selbst ein Claim — das ist die
Komposition, die `§2.4` behauptet, sauber durchgezogen.

**Nicht implementiert:** die Beweise in `accusation.v`. `§2.1` verlangt „self-contained
Beweise", aber Layer 01 flaggt Equivocation ohnehin aus dem Store; ein zweiter Prüfpfad in `03`
wäre Redundanz mit eigener Fehlerfläche. `accusation.v` bleibt vollständig opak (D55). Der Satz
in `§2.1` ist als Konvention für Menschen zu lesen, nicht als Verifizierer-Pflicht — und so
umzuformulieren.

### D68 — `00 §5.1` behauptet eine Fassung von `05 §3`, die es nicht gibt

`00 §5.1` verweist auf „Enforcement-Spec §3, geänderte Fassung — siehe DF-2". `05 §3` auf `main`
enthält weder `attributed_opinion` noch überhaupt eine Statusunterscheidung. Ein Widerspruch
zwischen zwei Dateien im Bestand, unabhängig von `03`.

**Vor `03` nötig ist nur das Vokabular**, weil `03` es produziert: `BINDING` und
`ATTRIBUTED_OPINION`. Severity-Schwellen, Cure-Kurven und Slash-Höhen bleiben Policy und Layer
05.

**Für den zweiten `05`-Durchgang vorgemerkt:** `§3` bekommt den Satz, dass ein Verdikt ohne
Bindung nach `00 §5.1` **keinen** Statuswechsel auslöst, unabhängig von seiner Severity.

### D69 — Oberfläche und Modulschnitt von Layer 03

```
mensch_als_republik/profiles/
  policy.py      NucleusPolicy, Auflösung, Sicherheits-Default (00 §5.2)
  membership.py  membership()      -> MembershipResult
  credit.py      settlement()      -> SettlementResult
  verdict.py     verdict_status()  -> VerdictStatus
  findings.py
```

`03` ist reine Komposition über Layer 01 plus Policy: kein Graph, keine Anker, kein
`TrustParams`. `classify_all` aus `02` wird **geteilt, nicht kopiert**, abgesichert durch
denselben Identitätsvergleich der Funktionsobjekte, den PR-INV-4 für `derive()` eingeführt hat.

Drei getrennte Funktionen statt einer, weil `03 §1` drei getrennte Cluster behauptet und die
Trennung sonst nur in der Prosa steht — dieselbe Bewegung wie D52 (`§9` trägt die Trennlinie in
die Oberfläche).

---

## L. Golden Anchors für Layer 03 — anderer Maßstab, gleiche Disziplin

`03` ist weitgehend nicht-numerisch. Die Trennschärfe kommt hier nicht aus Arithmetik, sondern
aus **Negativvektoren**. Drei Sorten:

1. **Byte-exakte CBOR-Vektoren** für die Kodierungen aus D55, im Format von TV1
   (`v = h'a1001864'` = `{0: 100}`). Von Hand nachrechenbar, byte-vergleichbar.
2. **Bestandsanker.** `00 §3.1` liefert `constitution_hash = 890b21e7…` und
   `N = 65309fe2…`, byte-identisch mit `01` Anhang C. `03` bindet daran, statt neue Zahlen zu
   erfinden — dieselbe Disziplin wie „die ganze Spec-Reihe testet gegen denselben Anker".
3. **Konjunktionstabellen:** Mitgliedschaft (vier Zustände, D60), Tilgung (vier Bedingungen,
   D63), Verdikt-Status (zwei Pfade × zwei Parteiformen, D67).

**Das unbequeme zweite Profil (Konsequenz aus D54) ist hier keine Parameterwahl, sondern eine
zweite Verfassung.** Das kanonische Beispiel aus `00 §3.1` trägt jeden Default, den es gibt:
`irrevocable_predicates: ["obligation@1"]`, ein Arbitrator, `key_mode = 0`, Ankerset der
Größe 1. Das Gegenprofil verletzt fünf davon, und jede Verletzung trennt zwei plausible
Implementierungen:

| Abweichung | prüft |
|---|---|
| Verfassung **schweigt** zu `irrevocable_predicates` | Sicherheits-Default `00 §5.2` |
| Verfassung nennt `vouch@1` als irrevocable | D58 |
| **zwei** Arbitratoren, einer davon nicht in `arbitration.arbitrators` | D67, Pfad (i) vs (ii) |
| `accept-rules` auf einen **anderen** `constitution_hash` | D61 |
| `grant-membership` von einem Schlüssel **außerhalb** `authorized_keys` | D62 |

Keiner dieser fünf Fälle ist unter dem kanonischen Profil sichtbar.

---

## M. Änderungsliste Layer 03

| Datei | Änderung | Quelle |
|---|---|---|
| `01-claim-atom.md §5.4`, `§6` | `policy`-Parameter der Klassifikation; Auflösungsregel; Sicherheits-Default | D57 |
| `01-claim-atom.md §5.4` | Negativliste: trust-gewährende Prädikate nicht irrevocable | D58 |
| `01-claim-atom.md §7.1` | Key `1` bleibt unkodiert (Verweis auf `02c`); Key `2` typ-fest `bstr[32]` | D56 |
| `00-…-constitution.md §5` | `UNSAFE_IRREVOCABLE_PREDICATE`; Verweis auf die Negativliste | D58 |
| `03-profiles.md` | **vollständig ersetzt** — drei Abschnitte durch `00` überholt, zwei intern widersprüchlich, `submit-arbitration@1` fehlt | D55–D69 |
| `03-profiles.md §2.1` | `accusation.v` opak; „self-contained Beweise" als Konvention, nicht als Pflicht | D67 |
| `03-profiles.md §2.4` | `submit-arbitration@1` mit Profiltabelle; Parteienauflösung | D67 |
| `03-profiles.md §3.3.1` | `v`-Keys typ-normativ; `EXPIRING_OBLIGATION` | D55, D59 |
| `03-profiles.md §3.3.2` | „passend" als vierteiliges Prädikat; Teilbetrag tilgt nicht | D63, D65 |
| `03-profiles.md §3.3.3` | Verweis auf `00 §5` statt freistehender Pflicht | D57 |
| `03-profiles.md §3.3.4` | auditierbar statt selbst-validierend; `ungedeckte Emission` | D66 |
| `03-profiles.md §4` | `I ∈ authorized_keys` statt `I = N`; vier Zustände; `constitution_hash` als Parameter | D60–D62 |
| `03-profiles.md §5` | getragene Grenzen: widerrufbare Quittung, Kompositionspfad, keine Emissionsschranke | D64, D62, D66 |
| `05-enforcement.md §3` | Vokabular `BINDING`/`ATTRIBUTED_OPINION`; kein Statuswechsel ohne Bindung | D68 |
| Repo-Wurzel | `03-golden-anchors.md`; zweite Verfassung als Gegenprofil | L |
| Repo-Wurzel | `02b-golden-anchors.md §11`: INV-8-Vektor bei leerem Ankerset ist fällig, nicht offen | K |

**Reihenfolge:** `01a-policy` → `03` (Anker → Prompt → Abnahme → Merge) → `02c-purpose` →
`00a-rotate-key` → zweiter Durchgang `05`/`06`/`04`/`00`/`VISION`.

---

## N. Aus dem Spec-Nachzug `01a-policy`

Drei Festlegungen, die beim Schreiben des Ersatztextes zu D57/D58 nötig wurden und über beide
hinausgehen. D70 ist formal eine **Wiedereröffnung** von `00 §5.2` und daher als eigener Fork
geführt, nicht als Nachtrag.

### D70 — Der Sicherheits-Default ist ein Boden, keine Rückfallebene ⚠️

`00 §5.2` lautete: „Schweigt die Verfassung zu `irrevocable_predicates`, gilt **trotzdem**
`obligation@1` als irrevocable. Weitere Prädikate werden nur durch explizite Nennung
irrevocable."

**Der Befund.** Der Satz regelt nur das Schweigen. Er sagt nicht, was gilt, wenn eine Verfassung
`["foo@1"]` deklariert und `obligation@1` weglässt. Wörtlich gelesen greift der Default dann
nicht — und das Schulden-Lösch-Loch ist durch das bloße Nennen einer beliebigen anderen Zeile
wieder offen. Genau das Loch, das der Abschnitt „nicht durch Vergessen" aufreißbar machen
wollte, nur mit einem Zwischenschritt.

```
wirksame Menge  =  { "obligation@1" }  ∪  irrevocable_predicates  ∖  unsicher (01 §5.4.3 b)
```

**Beschluss:** Der Default ist ein **Boden**. Die Liste erweitert die Menge, sie kann sie nie
verkleinern. Drei Fälle — Schweigen, Nennung, Nennung anderer Prädikate ohne `obligation@1` —
sind damit identisch geschützt.

**Verworfen — Alles-oder-nichts bei unsicherer Deklaration.** Nennt eine Verfassung `vouch@1`
(D58), wäre es denkbar, die ganze Liste zu verwerfen. Das ist schlechter: eine einzelne
Fehldeklaration nähme dem Nukleus auch den Schuldenschutz. Der unsichere Eintrag fällt heraus,
der Rest bleibt wirksam.

Dieselbe Bewegung wie D37 („kein Budget-Beitrag bei unlesbarem `n`"): der defekte Teil fällt
weg, nicht die Aussage als Ganzes.

### D71 — `core/*` kann nie irrevocable sein

`00 §5` deklariert `irrevocable_predicates` als freies `array[text]`. Ein Eintrag `"revoke@1"`
würde Widerrufe gegen Widerruf immunisieren — das ist keine Aussage über einen Lebenszyklus,
sondern ein Fixpunkt in ihm.

**Beschluss:** Der Abgleich greift nur für `nuc:`-Prädikate (`01 §5.4.2`). Einträge, die auf
`core`-Prädikate zeigen, werden ignoriert — nicht als Fehler, sondern weil `core/revoke@1` und
`core/supersede@1` *der* Lebenszyklus sind und das geschlossene Aufnahmekriterium aus `01 §5`
sie genau deshalb enthält.

Zusammen mit D58 ergibt das zwei Ausschlussgründe verschiedener Natur: D58 schließt aus, was
gefährlich wäre; D71 schließt aus, was bedeutungslos wäre.

### D72 — Oberfläche: der Typ trägt die Invarianten, der Resolver liegt in `03`

```python
@dataclass(frozen=True, slots=True)
class NucleusPolicy:
    irrevocable: frozenset[str]      # normalisiert: Boden gesetzt (D70), Unsicheres entfernt (D58)
    warnings: tuple[str, ...]        # UNSAFE_IRREVOCABLE_PREDICATE, …

def classify(claim, store, now, policy: NucleusPolicy | None = None) -> Classification: ...
```

**Die Invarianten leben im Konstruktor**, nicht in der Aufrufkonvention. Nach D57 darf die
Regel nicht umgehbar sein; ein Aufrufer, der `NucleusPolicy` baut, kann keine unsichere Menge
erzeugen, weil Boden und Filter beim Bauen greifen. Layer 01 honoriert die Menge und ignoriert
`warnings`.

**`NucleusPolicy` liegt in Layer 01, der Resolver in Layer 03.** Der Typ muss aus `01`
importierbar sein, sonst wird der Import zyklisch. Die Auflösung aus Genesis- und
Verfassungsobjekt braucht dagegen ein Objektmodell, das `01` nicht kennt — sie lebt in
`profiles/policy.py` und liefert `NucleusPolicy` plus Diagnose.

**`Classification` bleibt unverändert** und trägt die angewandte Policy **nicht**. Erwogen als
Nachvollziehbarkeitshilfe (zwei Verifizierer mit verschiedenen Ergebnissen sähen sofort, woran
es liegt), verworfen: `Classification` ist heute ein reiner Zustandswert, jedes Zusatzfeld
verkompliziert die Vergleichbarkeit in Tests, und der Aufrufer kennt die Policy ohnehin — er
hat sie übergeben.

**`resolve_policy` wird in `01a` nicht gebaut.** `00 §4` und `§5` sind Schemata, kein Code; ein
Objektmodell dafür entsteht erst mit `03` (D61 braucht die Verfassungsobjekte ohnehin). `01a`
liefert Typ und Honorierung, mit handgebauten `NucleusPolicy`-Instanzen in den Tests.

---

**Konsequenz für die Zustandsmaschine, offen benannt.** `01` Anhang B sagte bisher, alle
Zustände außer `expired` seien „deterministisch gegeben denselben Bytes". Ab jetzt gilt
„gegeben denselben Bytes **und derselben Policy**". Das ist eine echte Abschwächung eines
tragenden Satzes. Sie ist vertretbar, weil abweichende Verfassungen für dasselbe `N` kein
legitimer Uneinigkeitsfall sind, sondern ein Synchronisationsdefekt: `N` ist der Hash des
Genesis, der Genesis fixiert `constitution_hash`, und die Ratifizierung einer neuen Version ist
selbst prüfbar (`00 §5.3`). `expired` bleibt damit der einzige Zustand, in dem zwei korrekte
Verifizierer legitim uneins sein dürfen.

### D73 — Die Policy trägt ihren Scope, und eine Fehlpaarung ist laut ⚠️

Lücke in D72, sichtbar geworden beim Schreiben des `01a`-Prompts: `NucleusPolicy` hatte kein
Feld, das sagt, für **welchen** Nukleus sie gilt. Layer 01 kann die Auflösung aus `C.N` nicht
selbst leisten (`01 §5.4.1` braucht Genesis- und Verfassungsobjekte, die Layer 01 nicht kennt) —
also hätte ein Aufrufer die Policy des Nukleus A auf einen Claim aus Nukleus B anwenden können,
und nichts hätte es gemerkt.

Das ist kein akademischer Fall: sobald Layer 03 über Stores mit mehreren Scopes läuft, ist die
falsche Paarung der Normalfall eines Programmierfehlers.

**Beschluss:** `NucleusPolicy` trägt `scope: bytes` als Pflichtfeld. Trifft `classify` auf einen
`nuc:`-Claim mit `claim.N ≠ policy.scope`, wird `ValueError` geworfen. Für `core/*`-Claims wird
die Policy ohne Prüfung ignoriert.

**Warum ein Fehler und kein stilles Ignorieren.** Eine nicht angewandte Policy heißt: der
Widerruf auf eine `obligation@1` wirkt. Das ist die **unsichere** Richtung — genau das
Schulden-Lösch-Loch, das D57 schließt. Anders als bei Teilwissen (D3) gibt es hier keine sichere
Voreinstellung, weil der Zustand nicht unvollständig, sondern falsch zugeordnet ist. Ein lauter
Fehler ist die einzige Antwort, die nicht rät.

**Verworfen — `scope: bytes | None = None` mit „gilt für alles".** Bequemer in Tests, aber der
Default wäre der unsichere Fall, und Defaults setzen sich durch.

**Verworfen — `NucleusPolicy` als Abbildung `scope → Prädikate`.** Löst dasselbe Problem und
nimmt die Auflösung gleich mit, verlagert aber Mehr-Scope-Logik nach Layer 01. Die Auflösung
gehört nach `03` (D72); ein Objekt, das mehrere Nuklei kennt, ist dort zu bauen, nicht hier.

---

## O. Aus der `01a`-Abnahme

Der Lauf war beim ersten Versuch grün: 234 Tests, alle neunzehn Vektoren aus dem Prompt beim
ersten Anlauf richtig, eine Rückfrage (`helpers.py` hatte keinen generischen Anhänger — korrekt
gemeldet statt `vouch_raw` zweckzuentfremden). Die drei Befunde der Durchsicht sind **allesamt
Strukturfragen, keine Rechenfehler** — dasselbe Muster wie bei `02b`, wo beide Vorgabefehler in
Formulierungen lagen.

Zwei der drei sind Fehler in meinem Prompt, nicht in der Ausführung.

### D74 — Policy-Vermerke tragen ihr Subjekt

`01a-policy-prompt.md §2` gab `warnings: tuple[PolicyWarning, ...]` vor — einen nackten Code
ohne Subjekt. Der Betreiber erfährt damit, dass *etwas* Unsicheres deklariert war, nicht *was*.
Bei einer Verfassung mit zwanzig Einträgen ist das unbrauchbar.

**Beschluss:** `PolicyNote(code, predicate)`, ein Eintrag je unsicher deklariertem Prädikat,
sortiert nach `predicate`.

Die Sortierung ist nicht Kosmetik: `declared` ist ein `frozenset`, die Iterationsreihenfolge
schwankt zwischen Läufen, und ein Vektor über zwei unsichere Einträge wäre sonst nicht
reproduzierbar. Dieselbe Erwägung wie bei `TrustResult.findings` („sortiert, dedupliziert").

**Der Vorgabefehler ist der eigentliche Eintrag:** Layer 02 hatte `Finding(kind, subject)`
bereits richtig gebaut. Der Prompt hat die Form nicht übernommen, obwohl der Zweck identisch
ist. Neue Schichten erben die Diagnoseform der bestehenden, statt sie neu zu erfinden.

### D75 — Die drei Prädikatmengen sind disjunkt, geprüft beim Import

Die Normalisierung aus D70/D58/D71 lautet:

```
irrevocable = (PROTOCOL_IRREVOCABLE ∪ declared) ∖ TRUST_GRANTING ∖ CORE_ENTRIES
```

Boden setzen, dann filtern. Läge je ein Prädikat in `PROTOCOL_IRREVOCABLE` **und**
`TRUST_GRANTING`, verschwände der Boden aus D70 still — und **kein Testvektor kann das
prüfen**, weil die Konstanten heute disjunkt sind. P-1 bis P-6 bestehen unter jeder Anordnung
der drei Regeln.

**Beschluss:** zwei `assert` auf Modulebene statt eines weiteren Vektors. Ein künftiger
Widerspruch zwischen den Mengen wird beim Import laut, nicht in der Semantik leise.

**Das ist die D54-Lage in neuer Form.** Dort versteckte das kanonische Profil (`α = ½`) einen
Formelfehler; hier verstecken disjunkte Konstanten eine Reihenfolgefrage. Die Lehre aus D54 war
„ein zweites Testprofil mit unbequemen Zahlen". Sie greift hier nicht, weil sich der unbequeme
Fall nicht konstruieren lässt, ohne die Konstanten selbst zu verfälschen. Die Ergänzung:
**wo ein Fall untestbar ist, weil er heute unmöglich ist, wird die Unmöglichkeit zugesichert —
nicht die Semantik getestet.**

### D76 — Unter Policy schlägt `expired` den Widerruf, ohne Policy umgekehrt

Sichtbar geworden am Kontrollfluss von `classify`: ohne Policy greift der Widerruf-Zweig vor der
Zeitprüfung, mit Policy fällt die Auswertung auf den `temporal`-Zweig durch.

| Lage | `policy=None` | mit Policy |
|---|---|---|
| Obligation, abgelaufen **und** widerrufen | `REVOKED` | `EXPIRED` |

`01` Anhang B legt zwischen `revoked`, `superseded` und `expired` **keine** Rangfolge fest —
alle drei sind inaktiv, und für jeden Konsumenten der Zustandsmaschine ist das die einzige
Aussage, die zählt. Die Umkehrung ist damit kein Fehler.

**Beschluss:** Ist-Zustand festhalten, nicht vereinheitlichen. Vektor C-9 hält ihn fest, damit
er sich nicht unbemerkt ändert. Eine Vereinheitlichung würde entweder den Kontrollfluss von
`classify` umbauen (Risiko ohne Ertrag) oder eine Rangfolge in Anhang B einführen, die dort
bewusst fehlt.

**Vorgemerkt für Layer 03:** Sobald ein Konsument die Zustände *unterscheidet* statt nur
„aktiv/inaktiv" zu fragen, wird die Rangfolge relevant und muss dann entschieden werden. In
`03` ist das nicht der Fall — D60 und D63 fragen ausschließlich auf `active`.

---

## P. Aus dem Eigenauftrag zur Sitzung `03`

### D77 — Kanonizität von `v` prüft die lesende Schicht, nicht das Atom ⚠️

D37 verlangt kanonisches CBOR für `v`. **Durchgesetzt war es nirgends.** `cbor_canon.decode` ist
ein dünner `cbor2.loads`-Wrapper ohne Prüfung; `is_canonical` steht an genau einer Stelle im
Paket (`verifier.py`, Re-Serialisierung des **Cores** nach `01 §6` Regel 2). `v` ist im Core eine
`bstr`, deren Inhalt dabei uninterpretiert bleibt. `trust/groups.py` liest sie per nacktem
`decode`. Nicht-minimale Ganzzahlen, indefinite-length Maps, unsortierte und doppelte Schlüssel
gehen durch.

**Kein Testvektor konnte es zeigen.** Jedes `v` im Repo entsteht durch `cbor_canon.encode`
(`helpers.py`, `tests/trust/test_payload.py`, `tests/vectors/gen.py`) — kanonisch by
construction. Es gibt keinen Pfad, auf dem ein nicht-kanonisches `v` in einen Test gerät.
Dieselbe Mechanik wie beim unversionierten `02b`: eine einzige Darstellung des Zustands, und die
stimmt mit sich selbst überein.

**Nicht in Layer 01.** Ein zwölfter Reject-Code hieße, das Atom liest `v`. Das bricht die
Bedeutungsblindheit und D55 in derselben Bewegung. Layer 01 bleibt eingefroren.

**Beschluss:** Jede Schicht, die `v` liest, prüft vorher `is_canonical` und behandelt einen
Verstoß als **unlesbar** im Sinne von D37 — Vermerk `NON_CANONICAL_V`, defekter Teil fällt weg,
Claim bleibt gültig und sichtbar.

| Schicht | liest | Wirkung bei Verstoß |
|---|---|---|
| 02 | `vouch.v` Key `0` | keine Kante, kein Budget-Beitrag (D37, Zeile 2) |
| 03 | `receipt.v` Key `0` | tilgt nicht (D65-Richtung) |
| 03 | `obligation.v`, `verdict.v` | Vermerk, sonst folgenlos |

Drei Festlegungen, die den Beschluss erst ausführbar machen:

**(a) Nicht wie ein abwesendes `v`.** Der Abwesend-Default `n = D` (`w = 1`) auf einen defekten
Payload angewandt wertet ihn zu maximalem Vertrauen auf — Über-Vertrauen, die eine gefährliche
Richtung (`02 §7`). Nicht-kanonisch fällt in den Zweig „unlesbar", nie in den Zweig „abwesend".

**(b) Vor der Wertprüfung.** Kanonizität ist eine Eigenschaft der Bytes und geht der
Interpretation voraus. Beobachtbar an genau einem Fall: `v = h'a2001864001865'` bei `D = 100`
dekodiert zu `{0: 101}`, also `n > D`. Heute `INVALID_VOUCH_WEIGHT`, künftig `NON_CANONICAL_V`.
Ohne diesen Vektor ist der Vorrang nicht festgelegt und zwei Implementierungen laufen legitim
auseinander.

**(c) Nach dem Dekodieren.** `is_canonical` dekodiert selbst und **wirft** bei undekodierbarer
Eingabe, statt `False` zu liefern (gemessen: `h'a1'` → `CBORDecodeEOF`, `h'ff'` →
`CBOREncodeError` beim Re-Enkodieren). Ein Wächter vor dem `try` verwandelt
`UNPARSABLE_VOUCH_PAYLOAD` in eine durchschlagende Exception. Die Prüfung steht **nach** dem
geglückten `decode`.

**Der doppelte Schlüssel ist der tragende Fall.** Bei den übrigen Verstößen liefert das
Dekodieren den richtigen Wert und der Schaden bleibt bei der Byte-Vergleichbarkeit. Bei einem
doppelten Key `0` verliert `decode` einen Eintrag, und welcher gewinnt, steht in keiner
Spezifikation, sondern in cbor2. `01 §6` Regel 2 verlangt „ohne doppelte Keys" — für den Core.
Für `v` galt der Satz bis hier nicht, und damit hing `n` an einer undokumentierten
Bibliotheksentscheidung.

**Verworfen — `encode(obj) != v` statt `is_canonical(v)`.** Rechnerisch identisch und spart den
zweiten Dekodierdurchlauf, dupliziert aber die Definition von „kanonisch" an eine zweite Stelle.
Zwei Definitionen driften; die Ersparnis liegt bei einem Payload von vier Bytes.

**Der Vermerk trägt in jeder Schicht denselben Namen, das Enum wird nicht geteilt.** Layer 02 und
Layer 03 haben nach `02a §5` und D69 je einen eigenen Findings-Enum — richtig so, weil beide
keine Claim-Rejects sind. Die **Zeichenkette** muss beide Male `"NON_CANONICAL_V"` lauten, sonst
trägt derselbe Defekt zwei Namen und wer `grep` benutzt, findet die Hälfte.

**Reihenfolge.** Der Durchgang heißt `02c-canon-v` und läuft **vor** `03`, weil `03 §5.1` der
Anker Byte-Vektoren gegen die `v`-Kodierungen aus D55 setzt; ohne durchgesetzte Kanonizität sind
diese Vektoren illustrativ statt normativ. Der bisher als `02c-purpose` geführte Durchgang
(D56) heißt ab hier **`02d-purpose`**. Änderungsliste M liest damit: `01a-policy` →
`02c-canon-v` → `03` → `02d-purpose` → `00a-rotate-key` → zweiter Durchgang.

**Kein Bestandsanker ändert sich.** `TrustFinding` ist ein `str`-Enum und `Finding` sortiert
`(kind, subject)`; `NON_CANONICAL_V` reiht sich alphabetisch zwischen `INVALID_VOUCH_WEIGHT` und
`OVERCOMMITTED_AUTHOR` ein. Da kein bestehender Vektor die neue Art trägt, verschiebt sich keine
bestehende Findings-Liste. **235 grüne Tests sind damit Abnahmekriterium, nicht Hoffnung:** ein
roter Bestandstest wäre der Beweis, dass die Prüfung an der falschen Stelle sitzt.

**Änderungsliste:**

| Datei | Änderung |
|---|---|
| `02-trust-flow.md §3.1` | neuer Absatz „Nicht-kanonisches `v` ist unlesbar" (vollständige Datei geliefert) |
| `mensch_als_republik/trust/findings.py` | `NON_CANONICAL_V` |
| `mensch_als_republik/trust/groups.py` | Prüfung in `_decode_weight`, nach `decode`, vor der Wertprüfung |
| `tests/trust/test_payload.py` | `V-CANON-1` bis `V-CANON-6` |
| `tests/helpers.py` | roher `v`-Anhänger für den End-zu-End-Vektor |
| `03-profiles.md` | `NON_CANONICAL_V` im Vermerk-Katalog (mit `03`) |
| `03-golden-anchors.md §5.1` | Negativvektoren gegen die vier Verstoßklassen (mit `03`) |
| `01-claim-atom.md §7.1` | Satz, dass die Durchsetzung bei der lesenden Schicht liegt (zusammen mit der D56-Zeile) |

---

## Q. Beim Schreiben von `03-profiles.md`

Vier Forks aus der Widerspruchsprüfung vor dem Schreiben, ein fünfter beim Schreiben selbst,
dazu zwei Reparaturen im Register. Keine der fünfzehn Entscheidungen aus Abschnitt K wurde dabei
neu aufgemacht — alle fünf schließen Lücken, die K offen ließ.

### D78 — „Vorab" heißt „aktiv zum Bewertungszeitpunkt" ⚠️

`00 §5.1` und `03 §2.4` verlangen für Pfad (ii), dass beide Parteien sich **vorab** dem
Schiedsrichter unterworfen haben. D67 übernimmt das als normative Bedingung.

**Der Befund.** Zwischen zwei verschiedenen Autoren gibt es keine Ordnung. `01 §5.3` und
`00 §6.1` sagen beide: Ordnung kommt aus der Autorenkette, nie aus Wall-Clock `t` — und zwei
Autoren teilen keine Kette. `submit-arbitration` der Partei A und das `verdict` des
Schiedsrichters stehen in verschiedenen Ketten. „Vorab" ist damit prinzipiell nicht auswertbar,
nicht bloß aufwendig.

**Beschluss:** Pfad (ii) verlangt, dass beide Unterwerfungen zum Bewertungszeitpunkt `now`
**aktiv** sind. `00 §5.1` zieht im zweiten Durchgang auf dieselbe Formulierung nach.

Das ist auch die bessere Regel, nicht nur die berechenbare: wer widerruft und dabei bleibt,
trägt die Bindung nicht mehr; wer sie nachreicht, trägt sie. Beobachter dürfen über `now`
legitim uneins sein — dieselbe Lage wie bei `t_exp` (`01 §6`), mit derselben sicheren Richtung:
im Zweifel `ATTRIBUTED_OPINION`.

**Verworfen — `t` als Ordnung heranziehen.** Es wäre die einzige Stelle im ganzen Protokoll,
an der Wall-Clock eine Rangfolge zwischen zwei Autoren stiftet. Genau das schließt `01 §5.3`
aus, und ein Angreifer mit falscher Uhr bekäme Kontrolle über die Bindungsfrage.

### D79 — `settlement()` hat vier Zustände

D60 gab der Mitgliedschaft vier Zustände, D67 dem Verdikt zwei; `settlement()` stand in D69 nur
als Name. Dieselbe Begründung wie bei D60 trägt hier: mit einem Wahrheitswert fallen „nie
quittiert", „Quittung widerrufen" (D64) und „Teilbetrag, tilgt nicht" (D65) auf denselben Wert
zusammen — obwohl D64 und D65 diese Unterscheidung gerade erzeugt haben.

```
SETTLED         Obligation aktiv, passende aktive Quittung ohne Key 0
OPEN            Obligation aktiv, keine passende Quittung oder eine, die nicht tilgt
EXPIRED         Obligation durch t_exp erloschen
INDETERMINATE   Obligation pending oder unverlinkt — Teilwissen
```

**`EXPIRED` ist nicht kosmetisch.** Nach D70 ist `obligation@1` **immer** irrevocable, also ist
`t_exp` der einzige Weg, auf dem eine Obligation inaktiv wird. Der Fall ist nicht selten,
sondern der einzige, und er verlangt vom Gläubiger etwas anderes als `OPEN`.

**`INDETERMINATE` folgt D3.** Auf Teilwissen `OPEN` zu behaupten hieße, eine Schuld zu
behaupten, die es vielleicht nicht gibt — die Falschbeschuldigungsrichtung.

Falsches Prädikat oder falscher Scope: `ValueError`, kein fünfter Zustand. Präzedenz D73 — eine
falsche Zuordnung ist kein unvollständiger Zustand.

**`revoked`/`superseded` sind für `obligation@1` unerreichbar**, weil der Boden aus D70
unbedingt gilt. Das ist die D75-Lage in neuer Form: die Unmöglichkeit wird zugesichert
(`assert`), die Semantik nicht getestet.

### D80 — `policy` ist in `settlement()` Pflicht, sonst nicht

D57 verwarf den Wrapper mit dem Satz „die Regel muss unumgehbar sein". D72 machte sie über den
Konstruktor unumgehbar für die **Menge** — eine unsichere `NucleusPolicy` lässt sich nicht bauen
—, nicht für den **Aufruf**. `policy=None` bleibt erreichbar, und in `settlement()` ist das
exakt das Schulden-Lösch-Loch, eine Schicht höher: der Schuldner-Widerruf würde wirken.

**Beschluss:** `settlement(store, *, obligation, scope, now, policy)` — Pflicht-Keyword ohne
Default. `membership()` und `verdict_status()` behalten `policy=None`, weil keines ihrer
Prädikate irrevocable ist und der Parameter dort folgenlos bleibt.

**Verworfen — überall Pflicht, der Symmetrie halber.** Symmetrie ist kein Sicherheitsargument.
Ein Pflichtparameter ohne Wirkung erzieht Aufrufer dazu, irgendeine Policy zu bauen, damit der
Aufruf durchgeht — und die dann auch dort zu benutzen, wo sie falsch ist.

### D81 — Scope-Gleichheit gilt im ganzen Verdikt-Cluster

D63 normierte `receipt.N == obligation.N` mit der Begründung, `01 §2.2` Regel 3 erzwinge nur
Selbstkonsistenz, nicht geteilten Scope. Dieselbe Lücke bestand für `accusation`, `verdict` und
`submit-arbitration`: eine Unterwerfung aus Nukleus B konnte einen Streit in Nukleus A binden.

**Beschluss:** Wo zwei Claims in Beziehung gesetzt werden, müssen beide dasselbe `N` tragen, und
dieses `N` muss der ausgewertete Scope sein. Als eigener Absatz `03 §1.4` geschrieben statt
dreimal wiederholt, damit die Regel nicht beim nächsten Profil vergessen wird. Vermerk
`SCOPE_MISMATCH`, ein Negativvektor je Prädikatpaar.

### D82 — Der Resolver rechnet nach; Genesis-Fehler werfen, Verfassungs-Fehler fallen zurück

Beim Schreiben von `03 §1.2` sichtbar geworden. `resolve_policy` bekommt Genesis- und
Verfassungsobjekt übergeben. Prüft es nicht nach, ist die Content-Adressierung aus `00 §3` eine
Behauptung des Aufrufers — und der Sicherheits-Default aus D70 hinge an dessen Sorgfalt.

**Beschluss:** Der Resolver rechnet `scope == SHA-256(DOM_NUC_GEN ‖ cbor(genesis))` und
`genesis.constitution_hash == SHA-256(cbor(constitution))` nach.

| Lage | Antwort |
|---|---|
| Genesis passt nicht zu `scope` | `ValueError` |
| Verfassung fehlt | Sicherheits-Default, `CONSTITUTION_UNAVAILABLE` |
| Verfassung passt nicht zum Hash | Sicherheits-Default, `CONSTITUTION_HASH_MISMATCH` |

Die Asymmetrie folgt D73 gegen D3: ein falsches Genesis ist eine **falsche Zuordnung**, dafür
gibt es keine sichere Voreinstellung. Eine fehlende oder nicht passende Verfassung ist
**Teilwissen**, und dafür gibt es genau eine: `{"obligation@1"}`.

**Nicht geprüft wird die Ratifizierung.** Ob dieses Verfassungsobjekt die *aktuelle* Version
ist, entscheidet die `amendment`-Schwelle (`00 §5.3`) — Layer 04, nicht hier. D61 hält.

---

### Reparaturen

**Abschnitt L, Zeile 3 der Gegenprofil-Tabelle** lautete „zwei Arbitratoren, einer davon nicht
in `arbitration.arbitrators`" — in sich widersprüchlich; wer in der Verfassung steht, ist per
Definition darin. Gemeint und ab hier gültig: **die Verfassung nennt zwei Arbitratoren, das
Verdikt kommt von einem Dritten.** Pfad (i) fällt, Pfad (ii) muss tragen. Das ist der Vektor,
der die beiden Pfade aus D67 trennt.

**Abschnitt M, Zeile `01-claim-atom.md §7.1`** (D56: Key `1` unkodiert, Key `2` typ-fest
`bstr[32]`) ist noch offen — `01 §7.1` sagt auf `main` weiterhin „die Kodierung von `1` und `2`
wird mit `03`/`05` festgelegt". Sie gehört in diesen Durchgang, zusammen mit dem D77-Satz zur
lesenden Schicht: beide betreffen denselben Absatz, und eine Datei zweimal vollständig zu
liefern wäre unnötig.

---

## R. Aus dem `02c`-Lauf

### D83 — Der Kanonizitäts-Rundlauf zählt in beide Richtungen ⚠️

Aus einer Rückfrage im Implementierungsfenster, nicht aus einem roten Test der neuen Regel: ein
**Bestandstest** wurde rot. D77 (c) legte fest, die Kanonizitätsprüfung stehe *nach* dem
Dekodieren, weil `is_canonical` bei undekodierbarer Eingabe wirft. Das war richtig und zu wenig.

**Der Befund.** `cbor2.loads` ist an zwei Stellen nachsichtiger, als CBOR erlaubt. Ein nacktes
Break-Byte dekodiert zu einem Sentinel-Objekt, statt zu werfen:

```
h'a1'      decode RAISE CBORDecodeEOF
h'ff'      decode ok (Sentinel), kein dict, encode RAISE CBOREncodeError
h'a100ff'  decode ok, IST ein dict,         encode RAISE CBOREncodeError
h'a1ff01'  decode ok, IST ein dict,         encode RAISE CBOREncodeError
```

Die beiden letzten schließen die naheliegende Reparatur aus — die Prüfung hinter einen
`isinstance(obj, dict)`-Test zu schieben. Sie **sind** Dicts. Es gibt keine Vorprüfung, die den
Fall abfängt.

**Beschluss:** Scheitert der Rundlauf `decode → encode` an irgendeiner Stelle mit einer
Exception, ist `v` **unlesbar** (`UNPARSABLE_VOUCH_PAYLOAD` bzw. `UNPARSABLE_V`). Liefert er ein
Ergebnis, das den Eingabebytes nicht gleicht, ist `v` **nicht kanonisch** (`NON_CANONICAL_V`).
Beide Vermerke führen in denselben Zweig aus D37: keine Kante, kein Budget-Beitrag. In Layer 03
gilt dasselbe für das Lesen der reservierten Keys.

Implementierung: `decode` und `is_canonical` stehen im **selben** `try`.

**Warum unlesbar und nicht nicht-kanonisch.** `h'a100ff'` ist kein Wert, der falsch geschrieben
wurde — es ist kein Wert. `NON_CANONICAL_V` würde behaupten, es gebe eine kanonische Form
desselben Inhalts, und die gibt es nicht. Die Wirkung ist in beiden Fällen dieselbe; die
Unterscheidung ist Diagnose, und eine falsche Diagnose schickt den Betreiber in die falsche
Richtung.

**Nicht-Map-Payloads.** Für Bytes, die kein CBOR-Map kodieren, gilt dieselbe Reihenfolge; welcher
Vermerk erscheint, hängt von der Verstoßklasse ab (`h'c11a514b67b0'` — ein Datums-Tag —
dekodiert, ist keine Map und ist nicht kanonisch, liefert also `NON_CANONICAL_V`). Die Zuordnung
ist für jede Eingabe eindeutig; das ist die Anforderung, nicht die Übereinstimmung mit der
Intuition.

**Herkunft des Fundes.** Der Implementierer hat die Frage zurückgegeben, statt sie im
Implementierungsfenster zu entscheiden — die Regel aus `§7` der Prompts hat gehalten. Es ist
der dritte Befund in Folge, der in einer **Formulierung des Prompts** lag und nicht in der
Ausführung (nach D74 und D75). Alle drei entstanden dadurch, dass eine Bedingung mit einer
plausiblen, aber unvollständigen Begründung geschrieben wurde. D77 (c) begründete die
Platzierung mit *einem* Fehlermodus; es gab zwei.

**Betroffene Dateien:** `02-trust-flow.md §3.1`, `03-profiles.md §1.3`, `02c-canon-v-prompt.md`
§3 und §5 (alle drei vollständig geliefert). `01 §7.1` bleibt unberührt — dort steht keine
Reihenfolgeaussage.

---

## S. Aus dem Abgleich mit dem tatsächlichen Code vor `03-prompt`

Vier Befunde, alle aus dem Lesen von fünf Bestandsdateien (`policy.py`, `trust/__init__.py`,
`trust/index.py`, `trust/derive.py`, `tests/helpers.py`) vor dem Schreiben des Prompts. Keiner
davon wäre beim Schreiben aufgefallen; alle vier hätten im Implementierungsfenster als Rückfrage
oder — schlimmer — als stille Umdeutung geendet.

### D84 — Eine Diagnose, ein Produzent

`03 §6.1` führte `UNSAFE_IRREVOCABLE_PREDICATE` im `ProfileFinding`-Katalog. Der Vermerk
existiert aber schon: `NucleusPolicy.__post_init__` erzeugt ihn als
`PolicyNote(PolicyWarning.UNSAFE_IRREVOCABLE_PREDICATE, predicate)` in `policy.warnings`.

**Beschluss:** Der Eintrag fällt aus dem `ProfileFinding`-Katalog. `PolicyResolution.findings`
trägt ausschließlich Befunde der **Auflösung** (`CONSTITUTION_UNAVAILABLE`,
`CONSTITUTION_HASH_MISMATCH`); die unsichere Deklaration liest der Aufrufer aus
`policy.warnings`.

Zwei Kanäle für denselben Befund tragen verschiedene Subjekte — `PolicyNote` ein Prädikat,
`Finding` eine `claim_id` — und laufen auseinander, sobald einer gepflegt wird. Die Übersetzung
wäre außerdem verlustbehaftet: es gibt keine `claim_id`, an der eine unsichere
Verfassungsdeklaration hinge.

### D85 — `INDETERMINATE` deckt auch Gabelung, nicht nur Teilwissen

D79 nannte für `INDETERMINATE` nur `pending`. `State` hat mehr: eine Obligation, deren Autor
equivokiert hat, steht in `EQUIVOCATION_FLAGGED` und ist weder aktiv noch abgelaufen noch
schwebend.

**Beschluss:** `INDETERMINATE` heißt nicht mehr „Teilwissen", sondern **„der Zustand der
Obligation erlaubt keine Aussage"**, mit zwei Ursachen und je eigenem Vermerk:

| Zustand | Vermerk | Grund |
|---|---|---|
| `pending` | `OBLIGATION_PENDING` | ich weiß zu **wenig** |
| `equivocation_flagged` | `OBLIGATION_AUTHOR_FLAGGED` | ich weiß zu **viel** |

Die zweite Zeile ist die interessantere: bei einer Gabelung existiert die Obligation womöglich
in zwei Fassungen mit verschiedenen Konditionen, und `OPEN` behauptete eine bestimmte davon.
Beide Male ist die Alternative eine Schuldbehauptung ohne Deckung — D3.

`LINKED` kommt hinzu und ist unerreichbar: es entsteht nur bei `now is None`, und `now` ist in
dieser Schicht immer ein `int`. D75-Behandlung, `assert` statt Vektor — wie `revoked` und
`superseded` unter dem Boden aus D70.

### D86 — `classify_all` wandert nach `mensch_als_republik/index.py`

`03` teilt `classify_all`, statt es zu kopieren (D69). Der Helfer lag in `trust/index.py`, was
`profiles/ → trust/` erzwungen hätte — eine Abhängigkeit quer zur Schichtung zwischen zwei
Geschwistern, von denen das eine vom anderen nichts braucht.

**Beschluss:** `classify_all` liegt in `mensch_als_republik/index.py`. Beide Schichten
importieren von dort; `trust/` re-exportiert weiter, damit die bestehende Oberfläche
unverändert bleibt.

Das Argument ist nicht Ästhetik. Der Kopplungstest `T-02.4` sichert, dass `classify_all` und
`verifier.classify` nicht auseinanderlaufen — eine Aussage über Layer 01 und ihren schnellen
Zwilling, nicht über den Trust-Solver. Der Helfer gehört dorthin, wo seine Invariante hingehört.

### D87 — `classify_all` bekommt den `policy`-Parameter ⚠️

`01a-policy-prompt.md §4` schloss ihn ausdrücklich aus: „Layer 02 wertet ausschließlich
`vouch@1` aus, und `vouch@1` kann nach D58 nie irrevocable sein — der Parameter hätte dort keine
Wirkung. Nicht anfassen."

**Der Satz stimmt für Layer 02 und trägt für Layer 03 nicht.** `settlement()` steht und fällt
damit, dass `obligation@1` **unter der Policy** klassifiziert wird. Ohne Parameter liefert
`classify_all` für den Kernvektor `SE-11` — Schuldner widerruft seine eigene Obligation — den
Zustand `REVOKED`, und `settlement()` bekäme einen Zustand, für den D79 keine Antwort vorsieht.
Das Schulden-Lösch-Loch wäre auf dem Umweg über den Helfer wieder offen.

**Beschluss:** `classify_all(store, now, policy=None)`. Layer 02 ruft weiterhin ohne auf,
Verhalten dort unverändert. Die Kopplungsinvariante erweitert sich mit:

```
∀ c ∈ store:  classify_all(store, now, policy)[claim_id(c)] == classify(c, store, now, policy)
```

**Verworfen — `03` ruft `classify()` je Claim.** Gibt die geteilte Definition von „aktiv" auf,
für die D69 und `PR-INV-10` gerade eingerichtet wurden.

**Verworfen — `03` rechnet den Irrevocable-Fall nach.** Die Regel stünde zweimal da. Genau die
Duplikation, gegen die `T-02.4` gebaut wurde.

D86 und D87 sind derselbe Eingriff: die Verschiebung ist damit keine Aufräumarbeit, sondern
notwendig.

---

**Muster, vierter Fall.** D74, D75, D83 und jetzt D87 haben dieselbe Form: eine Bedingung, deren
Begründung im damaligen Kontext trug und im nächsten nicht mehr. Bei D87 war die Begründung
sogar wörtlich richtig — sie sagte „Layer 02", und niemand las mit, dass sie damit ihren eigenen
Geltungsbereich benannte. Konsequenz für den Sitzungsabschluss vorgemerkt, nicht hier
entschieden.

---

## T. Aus den Rückfragen zum `03`-Lauf

Drei Befunde aus dem Implementierungsfenster, alle zurückgegeben statt entschieden. Der erste
ist eine echte Lücke, der zweite ein Widerspruch in derselben Datei, der dritte eine
Unbestimmtheit.

### D88 — Testidentitäten kommen aus festen Seeds, der Helfer bekommt einen Konstruktionspfad dazu

`tests/helpers.py::Identity` leitet den Schlüssel aus einem **Label** ab. Die Anker in
`00 §3.1` und `03-golden-anchors.md §3.1` stammen aus den Seeds `01×32`, `02×32`, `03×32`. Beide
treffen sich nicht — `Identity("ALICE")` liefert `3e18794e…`, die Spec verlangt `8a88e3dd…`.

**Verworfen — das Ankerdokument auf Label-Seeds umstellen.** Die Seeds sind normativ: sie stehen
in `00 §3.1`, und `tests/vectors/vectors_01.json` trägt `8a88e3dd…` und `8139770e…` bereits als
Bytes. Es bräche einen eingefrorenen Vektorsatz.

**Verworfen — ein eigener Fixture-Helfer für `tests/profiles/`.** Das wäre eine zweite
Implementierung von Kettenfortführung, Signatur und `h_prev`. Zwei Implementierungen desselben
Dings driften — dieselbe Begründung, mit der D86 `classify_all` teilt statt kopiert.

**Beschluss:** `Identity.__init__(self, label, *, seed=None)`. Bei `seed is None` bleibt die
Label-Ableitung; bestehende Aufrufe ändern sich nicht. Ein Konstruktionspfad, ein Label für die
Lesbarkeit, ein optionaler Seed für die Fälle, in denen der Schlüssel normativ ist.

**Die drei Seeds bekommen genau eine Definition** — in `tests/helpers.py`. Wo sie heute ein
zweites Mal stehen (`tests/vectors/gen.py`), kommen sie von dort. Konstanten an zwei Stellen
sind die Bauform, die in dieser Sitzung viermal einen Befund erzeugt hat.

### D89 — `verdict_status()` gibt `VerdictResult` zurück, nicht den Enum

`03 §2.4.2` schrieb `-> VerdictStatus` mit zwei Werten; `03 §11` (`PR-INV-9`) verlangte
`findings` in **allen vier** Ergebnistypen. Zwei Sätze derselben Datei, die sich widersprechen —
gefunden nicht durch Nachdenken, sondern beim Versuch, beide gleichzeitig zu erfüllen.

**Beschluss:** `VerdictResult(status: VerdictStatus, findings: tuple[Finding, ...])`.
`VerdictStatus` bleibt zweiwertig — die Zweiwertigkeit ist eine Aussage über den **Status**, nicht
über den Rückgabetyp (D67 hält).

Der Widerspruch war folgenreich und nicht kosmetisch: `VS-7` (`SCOPE_MISMATCH`), `VS-8`
(`UNRESOLVED_ACCUSED`) und `VS-9` (`INACTIVE_VERDICT`) liefern alle `ATTRIBUTED_OPINION` und
unterscheiden sich **ausschließlich** im Vermerk. Ohne Kanal wären drei Vektoren nicht prüfbar,
und `03 §2.4.4` — „Teilwissen senkt, was ich behaupten kann" — bliebe unbelegbar.

### D90 — `subject` ohne Claim ist der deklarierte `constitution_hash`

`CONSTITUTION_UNAVAILABLE` und `CONSTITUTION_HASH_MISMATCH` betreffen keinen Claim. `03 §6`
verlangt trotzdem ein Subjekt (D74).

**Beschluss:** `subject = genesis_obj[4]`, der im Genesis **deklarierte** `constitution_hash`.

Nicht der **berechnete** Hash des übergebenen Objekts: der ist eine Eigenschaft dessen, was der
Aufrufer gereicht hat, und wechselt mit jedem falschen Objekt. Der deklarierte Hash ist der
stabile Bezeichner und der, unter dem ein Betreiber suchen würde.

Nicht `scope`: der steht bereits im Aufruf, und ein Subjekt, das für alle Vermerke desselben
Aufrufs gleich ist, trägt keine Information. Nie ein Leerwert — das war der Befund, der D74
ausgelöst hat.

**Allgemeine Regel, hier zum ersten Mal ausgeschrieben:** `subject` ist in der Regel eine
`claim_id`; wo kein Claim betroffen ist, ist es das **Objekt, um das es geht**, in der Form, in
der der Betreiber es benennen würde.

---

### D91 — Die Policy wird scope-lokal angewandt ⚠️

Aus dem `03`-Lauf, zurückgegeben statt entschieden. `classify_all(store, now, policy)` wirft bei
jedem `nuc:`-Claim mit `N != policy.scope`, weil D73 genau das für einen einzelnen Claim
verlangt. Damit ist **jeder Store mit mehr als einem Nukleus unklassifizierbar** — und die
Vektoren `SE-5`, `MB-9` und `VS-7` legen fremd-gescopte Claims ausdrücklich in denselben Store,
weil sie prüfen, dass `03 §1.4` sie nicht zählt.

**Der Fehler liegt in D87, nicht in D73.** D73 entschied über `classify(claim, …)`: dort behauptet
der Aufrufer für **einen** Claim, diese Policy gelte für ihn, und eine Fehlpaarung ist eine
falsche Zuordnung ohne sichere Voreinstellung. D87 hat den Parameter an `classify_all`
weitergereicht, ohne zu bedenken, dass diese Funktion über einen **heterogenen Bestand** läuft
und gar nichts behauptet.

**Beschluss:** `classify_all` wendet `policy` auf genau die Claims an, für die sie definiert ist
— `nuc:`-Prädikate mit `N == policy.scope`. Alle übrigen klassifiziert sie mit `policy=None`.
D73 bleibt für `classify()` unverändert in Kraft.

Kopplungsinvariante entsprechend zweiteilig (`PR-INV-11`), dazu `PR-INV-12`: `classify_all`
wirft nie, gleich wie viele Nuklei der Store trägt.

**Getragene Grenze.** Der Zustand eines fremd-gescopten Claims ist damit policy-frei bestimmt
und kann für dessen eigenen Nukleus falsch sein. Er ist nirgends tragend: jede Beziehung dieser
Schicht verlangt `N == scope` (D81), und der einzige Claim, der außerhalb des Scopes gelesen
wird — der bestrittene Claim in D67 (b) — wird nur nach seinem **Autor** gefragt, nie nach
seinem Zustand. Wer das ändert, muss diese Zeile mit ändern.

**Verworfen — gefilterter Store-Wrapper.** Der Implementierer hat ihn gebaut und wieder
entfernt, richtigerweise: er nimmt den drei Vektoren genau die Claims weg, deren Nichtzählen sie
prüfen. Ein Filter, der das Prüfobjekt entfernt, macht den Test grün und die Aussage leer.

**Fünfter Fall desselben Musters** (nach D74, D75, D83, D87): eine Bedingung, deren Begründung
im ursprünglichen Kontext trug — ein Claim, ein Aufrufer, eine Behauptung — und beim Übertragen
auf einen anderen Kontext still ihren Geltungsbereich verlor. Diesmal war der Übertragende ich,
im selben Register, vier Einträge später.

---

## U. Aus der `03`-Abnahme

Drei Beschlüsse aus sechs Befunden. Die anderen drei (`_dedupe_sort`-Benennung, `KeyError` statt
`ValueError` im Verdikt, `KeyError` bei defektem Genesis) sind Ausführung und brauchen keinen
Registereintrag — sie fallen unter D92 bzw. sind kosmetisch.

### D92 — Der bewertete Claim wird an der Eingangstür geprüft ⚠️

`03 §1.4` normierte Scope-Gleichheit für **Beziehungen zwischen zwei Claims** —
`receipt` ↔ `obligation`, `accept-rules` ↔ `grant-membership`, `submit-arbitration` ↔ `verdict`.
Für den Claim, den eine Funktion als **Argument** entgegennimmt, stand die Regel nur bei
`settlement()` (`§3.3.2`) und nirgends allgemein. `verdict_status()` hatte sie deshalb nicht.

**Die Folge war real.** Ein Verdikt aus Nukleus B, mit `scope = N_A` ausgewertet, wurde nicht
abgewiesen: steht sein Autor in A's Arbitratorenliste, lautete die Antwort `BINDING`. Ein
anerkannter Schiedsrichter sitzt typischerweise in mehreren Nuklei — der Fall ist der Normalfall.

**Beschluss:** Jede Funktion dieser Schicht, die einen Claim als Argument nimmt, prüft als
Erstes: erwartetes Prädikat, `N == scope`, im Store. Sonst `ValueError`, vor jedem weiteren
Zugriff. Vektoren `VS-13`, `VS-14`, Invariante `PR-INV-13`.

**Der Unterschied zum Beziehungsfall ist die Herkunft des Claims.** Einen Claim, den ich im
Bestand *finde*, darf ich nicht zählen — Vermerk, weiter. Bei einem, den der Aufrufer mir
*reicht*, hat er eine Behauptung aufgestellt, die falsch ist, und dafür gibt es keine sichere
Voreinstellung (D73). Dass diese Unterscheidung nirgends stand, ist der ganze Befund.

Derselbe Beschluss deckt das defekte Genesis-Objekt ab: `resolve_policy` bekommt es gereicht,
also wirft es, statt still in einen `KeyError` zu laufen (Vektor `P-G`).

### D93 — `EXPIRING_OBLIGATION` erscheint unbedingt, nicht beim Verfall

Der Vermerk stand im `EXPIRED`-Zweig und erschien damit genau dann, wenn er wertlos ist: nach
dem Erlöschen sagt `EXPIRED` es ohnehin.

`03 §3.3.1` begründet ihn damit, dass `t_exp` dem Gläubiger **vor der Gegenleistung** sichtbar
sein soll — die einseitige Obligation hat keine signierte Annahme, er trägt die Prüfpflicht
allein.

**Beschluss:** `obligation.t_exp is not None` ⇒ `EXPIRING_OBLIGATION`, unabhängig vom Zustand.
Vektor `SE-13`: aktive Obligation mit `t_exp` in der Zukunft, `OPEN` plus Vermerk.

Die Fehlform ist notierenswert, weil sie nicht falsch *aussah*: die Bedingung stand in einem
Zweig, der sie erwähnt, statt an der Stelle, an der sie gilt. Ein Vermerk, der nur im
Schadensfall erscheint, ist kein Warnhinweis, sondern ein Nachruf.

### D94 — Vier Nicht-Auflösbar-Fälle, drei Vermerke

`03 §2.4.4` sagte „mit dem entsprechenden Vermerk", ohne die Zuordnung auszuschreiben. Die
Implementierung wählte für **alle** Fälle `UNKNOWN_ACCUSATION`, auch für eine Anklage aus
fremdem Scope.

**Beschluss:**

| Lage | Vermerk |
|---|---|
| `verdict.J.tag` ist nicht `claim-ref` | `UNKNOWN_ACCUSATION` |
| Anklage lokal unbekannt | `UNKNOWN_ACCUSATION` |
| Anklage in einem anderen Nukleus | `SCOPE_MISMATCH` |
| bestrittener Claim lokal unbekannt | `UNRESOLVED_ACCUSED` |

Die dritte Zeile ist der Grund für die Tabelle: eine Anklage aus fremdem Scope ist **bekannt**
und zählt nur nicht. `UNKNOWN_ACCUSATION` schickte den Betreiber in die Partitionsecke, während
das Objekt vor ihm liegt. Wirkung identisch, Diagnose entscheidend — dritte Wiederholung von
D74. Vektor `VS-12`.

---

**Neue Fehlerform.** D74, D75, D83, D87 und D91 hatten dieselbe Bauart: eine Begründung verlor
beim Übertragen still ihren Geltungsbereich. D92 ist anders — die Regel wurde **gar nicht erst
übertragen**. `settlement()` und `verdict_status()` nehmen beide einen Claim entgegen, bewerten
ihn im Scope und geben Zustand plus Vermerke zurück; sie hätten dieselbe Eingangsstrecke haben
müssen. `§3.3.2` hat sie ausgeschrieben, `§2.4.2` nicht, weil beim Schreiben von `§2.4` die
Bindungsfrage im Vordergrund stand und nicht die Eingangsprüfung.

Drei der sechs Abnahmebefunde waren Asymmetrien zwischen genau diesen beiden Funktionen.

---

## V. Vor Layer 04 — Verfassungsdefekte, Epochen, Auszählung

Acht Beschlüsse. D95 stammt aus dem `03a`-Lauf; D96 bis D102 entstehen aus der Forkanalyse für
Layer 04 und aus einer Recherche zum Stand der Technik, die zwei eigene Vorschläge widerlegt hat.

### D95 — Formwidriger Eintrag in `irrevocable_predicates`

Gemessen im `03a`-Lauf: eine Verfassung, die statt eines Arrays den Text `"obligation@1"` trägt,
wird in `resolve_policy` über `frozenset(raw)` still zu einer Menge von zwölf Einzelzeichen. Der
Hash stimmt, das Objekt ist richtig zugeordnet, die Wirkung ist heute harmlos — Müll trifft
keinen echten Prädikatnamen, und der Boden `obligation@1` (D70) hält unabhängig davon.

Die Harmlosigkeit ist allerdings zufällig: sie beruht darauf, dass kein Prädikatname aus einem
Zeichen besteht. Sie ist keine zugesicherte Eigenschaft.

**Kein `ValueError`.** D92 lässt werfen, wenn ein gereichtes Objekt **fehlzugeordnet** ist. Hier
ist die Zuordnung korrekt und der Defekt liegt im Inhalt. Also die D37/D70-Bewegung: der defekte
Teil fällt weg, der Rest gilt.

**Beschluss:**

- Formkriterium, bedeutungsblind: ein Eintrag ist wohlgeformt, wenn er ein `str` ist, genau ein
  `@` enthält, beidseits davon nicht leer ist und weder `/` noch `:` trägt. Alles andere fällt
  heraus.
- Vermerk `PolicyWarning.MALFORMED_IRREVOCABLE_ENTRY`, Subjekt ist der Eintrag selbst, bei
  Nicht-`str` als `repr`. **Nicht** in `PolicyResolution.findings` und **nicht** mit dem
  `constitution_hash` als Subjekt: D84 hat für den strukturgleichen Fall in derselben Liste
  bereits `policy.warnings` mit dem Eintrag als Subjekt festgelegt. Zwei Defekte einer Liste über
  zwei Kanäle zu führen wäre die D92-Asymmetrie.
- Ort ist `NucleusPolicy.__post_init__`, nicht `resolve_policy`. D72 hat Boden und Filter genau
  deshalb in den Konstruktor gelegt: ein Aufrufer, der die Klasse von Hand baut, darf keine
  unsichere Menge erzeugen können. Läge die Prüfung im Resolver, umginge sie jeder Testaufbau —
  derselbe Umgehungsvorwurf, mit dem D57 den Wrapper verworfen hat.
- `resolve_policy` reicht den gelesenen Wert **unverändert** weiter und zwingt ihn nicht mehr
  vorab in ein `frozenset`. Der Konstruktor nimmt ein `Iterable[object]` entgegen. Ist der Wert
  gar nicht iterierbar, gilt die Liste als vollständig ausgefallen: leere Menge plus ein Vermerk.

Damit hat die Liste drei Ausschlussgründe mit drei Behandlungen: `core/*` still ignoriert (D71),
unsicher mit Vermerk (D58), formwidrig mit Vermerk (D95). Wirkung gleich, Diagnose verschieden —
D94.

**Vektoren:** `P-7` Zeichenmenge aus einem Textwert; `P-8` Eintrag, der kein `str` ist; `P-9`
Eintrag mit Scope-Präfix, etwa `nuc:N/obligation@1`. Der dritte ist der wichtigste: `01 §5.4.2`
verlangt Profilnamen **ohne** Präfix, der Fehler ist der wahrscheinlichste echte Betreiberfehler,
und heute schützt so ein Eintrag lautlos niemanden.

**Nebenbefund.** `frozenset(42)` wirft heute einen unbehandelten `TypeError`. Nach D92 hätte ein
gereichtes defektes Objekt einen definierten Ausgang; er fehlte. Der Beschluss oben schließt das
mit ein.

### D96 — Epochenkette statt Snapshot ⚠️

`04 §4.2` band die Auszählung an einen Snapshot: eine Merkle-Wurzel über die `claim_id` der zum
Zeitpunkt der Vorschlagserstellung aktiven Vouch-Kanten, mit der Behauptung, die Auszählung sei
damit deterministisch und Uneinigkeit reduziere sich auf fehlende Claims.

**Die Behauptung hält aus drei unabhängigen Gründen nicht.**

1. Die Wurzel bindet `claim_id`, nicht Aktivität. Aktivität ist eine Funktion von Bytes, Store,
   `now` und Policy. Nach E-A trägt jeder Vouch in einem Budget-Scope ein `t_exp`, und `01 §6`
   erklärt genau den Ablauf zum einzigen legitimen Uneinigkeitsfall. Zwei Beobachter mit
   identischem Snapshot und identischem Bestand rechnen verschiedene Kantensätze. Wegen
   `C = C0 * gamma^d` verschiebt eine ablaufende Brückenkante die Kapazität eines ganzen
   Teilbaums exponentiell.
2. Der Seed ist selbst `now`-abhängig. `§4.2` nannte ihn genesis-deklariert; D23 verlangt
   `t_exp` und Neuerklärung, und der Ablauf fällt nach `02 §6.3` auf das **persönliche**
   Ankerset zurück. Läuft die Nukleus-Linse während einer Abstimmung ab, divergiert die
   Auszählung nicht, sie wird pro Beobachter beliebig.
3. Der Snapshot deckt die falsche Menge. Der Nenner einer Schwelle ist die stimmberechtigte
   Menge; die steht nicht darin und ist unter Teilwissen unter-bekannt. Ein zu kleiner Nenner
   macht die Schwelle **leichter** erreichbar — die Über-Ratifizierungsrichtung, also die
   Umkehrung von `02 §7`.

**Die Folge reicht über `04` hinaus.** D72 hält fest, abweichende Verfassungen für dasselbe `N`
seien kein legitimer Uneinigkeitsfall, weil die Ratifizierung selbst prüfbar ist, und schließt
daraus, `expired` bleibe der einzige Zustand, in dem zwei korrekte Verifizierer uneins sein
dürfen. Ist die Auszählung `now`-abhängig, wandert `expired` durch die Ratifizierung in die
Policy, und `01` Anhang B ist nicht mehr deterministisch gegeben dieselben Bytes und dieselbe
Policy, sondern gegeben dieselbe Uhr.

**Der erste Reparaturversuch war falsch und wird mitprotokolliert.** Vorgeschlagen war, den
Snapshot total zu machen: zwei Merkle-Wurzeln, `t_exp` innerhalb der Auszählung nicht
ausgewertet. Das funktioniert formal, verschiebt die Koordination aber auf den Vorschlagenden,
der damit auch die Wählerschaft aussucht. Nach dem CALM-Theorem hat ein Problem genau dann eine
konsistente koordinationsfreie Implementierung, wenn es monoton ist; ein nicht-monotones Problem
wird nicht dadurch monoton, dass man seine Eingabemenge einfriert — die Koordination taucht an
anderer Stelle wieder auf. Hier tauchte sie als Agenda-Macht auf.

**Beschluss:** Der Snapshot entfällt ersatzlos. `§4.2` wird gestrichen.

An seiner Stelle steht die **Epochenkette**:

- Eine Epoche beginnt mit einem ratifizierten Verfassungsobjekt. Der Genesis ist Epoche 1.
- Die stimmberechtigte Menge `P` und die Schwelle stehen in der Verfassung der laufenden Epoche.
  `P` wird deklariert, nie aus dem Bestand abgeleitet: eine abgeleitete Menge wäre unter
  Teilwissen unter-bekannt, und das ist die gefährliche Richtung.
- Eine Stimme ist ein Claim, gebunden an Instanz, Epoche und Vorschlag.
- Eine Entscheidung ist ein Claim, der die zählenden Stimmen mitführt. Jeder Beobachter prüft
  ihn offline gegen die Epochenverfassung. Kein `now`, keine Merkle-Wurzel über Vouch-Kanten.

`P` als Verfassungsfeld ist **optional**, damit das kanonische Beispiel es weglässt und `N`
byte-identisch bleibt (`65309fe2…`). Ein Nukleus ohne deklariertes `P` ist nicht auszählbar; die
Anker für `04` brauchen deshalb ein eigenes Profil.

**Getragene Grenze.** Die Epochenverfassung ist ein Stand, kein Livewert. Wer nach ihrer
Ratifizierung aufgenommen wird, stimmt erst in der nächsten Epoche mit.

### D97 — Stimmen sind innerhalb einer Epoche unwiderruflich

Damit die Auszählung monoton bleibt, darf die Stimmenmenge nur wachsen. Ein Widerruf oder ein
ausgewertetes `t_exp` lässt sie schrumpfen und macht das Prädikat nicht-monoton — womit D96
wieder aufgehoben wäre.

**Beschluss:** Eine Stimme in einer laufenden Epoche ist unwiderruflich. Ihr `t_exp` wird nicht
ausgewertet; trägt sie eines, bleibt es folgenlos. Die Verhältnismäßigkeit zu E-A ist beim
Schreiben von `04` gegen `02 §6.2` zu prüfen: bindet `vote@1` kein Budget, greift E-A nicht.

**Verhältnis zu D58.** Dem Wortlaut nach kollidiert das mit dem Verbot unwiderruflicher
vertrauensgewährender Prädikate; dem Kriterium nach nicht. D58 fragt, ob **Fortbestehen** die
konservative Lesart ist. In einem Verfahren, in dem der Status quo der Default ist und eine
Stimme sich nur von ihm weg bewegen kann, hält Fortbestehen eine getroffene Entscheidung, statt
Vertrauen künstlich am Leben zu erhalten. Eine Stimme gewährt zudem keine fortdauernde Autorität,
sondern ist ein einmaliger Akt — anders als `vouch@1` und `submit-arbitration@1`.

**Was an die Stelle des Ablaufs tritt.** Ein `t_exp` darf auf dem **Vorschlag** stehen und wird
von den Abstimmenden gelesen, nicht vom Protokoll ausgewertet. Uhren informieren Verhalten, nie
Gültigkeit.

### D98 — Auszählung nach Kopfzahl; `weight_mode = 1` vertagt

`04 §4` sah eine gewichtete Auszählung über dem Vertrauensgraphen vor. Sie fällt für v1 aus drei
Gründen, von denen der dritte allein trägt.

1. Gewichte aus dem Graphen sind keine Eigenschaft der Epoche; an ihnen hing die ganze
   `now`-Kette aus D96.
2. Der Zweckbegriff aus `§4.1` verlangt den Vouch-Zweck-Tag, der mit D56 vertagt ist. `§4` war
   in seiner bisherigen Form nicht implementierbar.
3. Ein Stimmgewicht ist eine übertragbare, akkumulierbare Größe, sobald jemand bemerkt, dass es
   sich lohnt. Vertrauen ist in diesem Protokoll ein Flussverstärker und kein Zahlungsmittel
   (`08 §4`); die gewichtete Auszählung verwandelt es in genau das, was es nicht sein darf. Das
   ist derselbe Einwand, mit dem D25 Ansehen von Torwächterschaft trennt.

**Beschluss:** Auszählung nach Kopfzahl über deklariertem `P`. `weight_mode = 1` bleibt im
Genesis-Schema zulässig, ist in v1 aber nicht ausgewertet; ein Nukleus, der es setzt, bekommt
kein Ergebnis, sondern den unentschiedenen Zustand.

**Was dabei nicht verloren geht.** `04 §4` verortet den Sybil-Schutz bei der **Mitgliedschaft**,
nicht beim Gewicht. Der Vertrauensgraph bleibt in voller Wirkung als das, was Mitglieder bei der
Aufnahmeentscheidung lesen. Er ist nur nicht mehr das, was das Protokoll multipliziert.

**Getragene Grenze.** Die zweck-gescopte Gewichtung war eine eigenständige Idee des Entwurfs. Sie
wird nicht widerlegt, sondern aus der Schicht genommen: sie ist Policy und keine Infrastruktur.

### D99 — Epochenidentität über dem Ergebnis, nicht über dem Beleg

Zwei ehrliche Mitglieder können dieselbe gesättigte Entscheidung unabhängig materialisieren, mit
verschiedenen Zeugenmengen — beide gültige Supermajoritäten, beide auf dasselbe Ergebnis. Steckt
die Zeugenmenge im gehashten Objekt, sind das zwei Identitäten für eine Entscheidung, und die
Verfassungskette spaltet sich ohne jedes Fehlverhalten.

**Beschluss:** Die Epochenidentität hasht das Ergebnis, nicht den Beleg.

```
epoch_id = SHA-256( DOM_NUC_EPOCH || cbor_deterministic([N, i, constitution_hash_neu]) )
```

Die Zeugenmenge reist daneben als austauschbarer Beleg. Zwei Materialisierungen desselben
Ergebnisses sind damit zwei Claims über dieselbe Epoche, und wer beide sieht, sieht keinen
Widerspruch.

Dieselbe Fehlerform wie D92 — zwei Wege, die dasselbe tun sollen, und nur einer trägt die Regel.
Diesmal vor der Abnahme gefunden.

### D100 — Die Stimme bindet an das Vorschlagsobjekt; Schließung durch Epochenwechsel

Ein Stichtag setzt voraus, dass zwei Beobachter sich einig sind, welche Stimmen davor abgegeben
wurden. Das `t`-Feld setzt der Autor selbst, und `01 §5.3` nimmt die Ordnung ausschließlich aus
der Autorenkette. Eine Frist würde von genau der Person durchgesetzt, die sie binden soll; und
selbst bei ehrlichen Uhren ist „zu spät abgegeben" von „zu spät zugestellt" nicht unterscheidbar,
womit die Frist zur Waffe dessen wird, der Zustellung verzögern kann. Ein Wahllokal ist eine
Autorität in Konventionsform. Mit ihr fällt die Frist.

**Beschluss:**

- Eine Stimme gilt einem **konkreten Vorschlagsobjekt**, nie einer Sachfrage. Wer seine Meinung
  ändert, holt seine Zustimmung zu diesem Objekt nicht zurück — sie hilft aber auch nur diesem
  Objekt.
- Eine Abstimmung wird nicht durch Zeit geschlossen, sondern durch den **Epochenwechsel**:
  Stimmen sind an Instanz, Epoche und Vorschlag gebunden, und mit der Materialisierung einer
  Entscheidung sind alle Stimmen der alten Epoche erledigt.
- Wer nicht abstimmt, senkt den Nenner nicht. Nichtteilnahme wirkt wie Ablehnung. Die Schwelle
  gilt gegenüber den **Berechtigten**, nicht gegenüber den Erschienenen.

**Getragene Grenze.** In einer Epoche, in der nichts durchgeht, hängt ein Vorschlag unbegrenzt.
Eine Entscheidung bildet damit gesetzte Zustimmung ab und nicht, wer an einem bestimmten Tag
besser mobilisiert hat. Für `example-nucleus.md`: eine hohe Schwelle bei lauer Beteiligung macht
die Verfassung faktisch unveränderlich; die Schwelle ist gegen realistische Beteiligung zu wählen.

**Verworfen — Zeugenquorum für Fristen.** Die Verfassung könnte `k` Zeugen benennen, die Stimmen
mit ihrer beobachteten Zeit gegenzeichnen; rechtzeitig wäre, was ein Zeugenquorum bestätigt.
Scope-lokal, also kein Bruch von „nie global", und additiv nachrüstbar. Für v1 verworfen: es
schafft eine Rolle mit Verfügbarkeitsanforderung und einen neuen Fehlermodus, denn kolludierende
Zeugen können Stimmen ausschließen. Zensur ist schlimmer als Hängenbleiben.

### D101 — Nein ist arithmetisch neutral und trotzdem ausgezeichnet

Würde die Schwelle gegen `Ja + Nein` gerechnet, könnte eine hinzukommende Nein-Stimme ein bereits
wahres Ergebnis wieder falsch machen. Der feste Nenner `n = |P|` ist es, der es überhaupt
erlaubt, das Nein aufzuschreiben: **wir können es uns leisten, weil es nicht mitzählt.**

**Beschluss:** Drei Antworten — Ja, Nein, keine Äußerung. Nein und Nichtteilnahme wirken gleich;
sie werden getrennt geführt, weil die Diagnose verschieden ist (D94). Mit `n = |P|` und der
Schwelle `num/den` gilt, in exakter Integer-Form ohne Division:

```
durchgekommen:   |Ja| * den   >  num * n
gescheitert:     (n - |Nein|) * den   <=   num * n
```

Beide Mengen wachsen nur, beide Bedingungen sind einmal wahr für immer wahr, und sie schließen
einander aus. Drei Zustände, zwei davon absorbierend, ohne jede Frist. Ein Vorschlag scheitert
daran, dass genug Berechtigte ihn ausdrücklich ablehnen — nicht daran, dass ein Tag vorbei ist.

**Höchstens ein Ja je Mitglied je Epoche. Neins beliebig viele.** Gegen mehrere Vorschläge
gleichzeitig zu sein ist kohärent; zwei verschiedene Dokumente gleichzeitig als das geltende zu
benennen ist es nicht. Niemand muss Nein zu A sagen, um Ja zu B sagen zu können, und ein Ja zu A
wird B **nicht** als Nein angerechnet.

**Abgrenzung zu `03`.** `membership()` löst mehrere aktive `accept-rules` mit `min(claim_id)` auf,
weil alle dasselbe sagen. Zwei aktive Stimmen desselben Autors sagen Verschiedenes: dann zählt
**keine**, plus Vermerk — die Parallele ist `02 §2`, wo ohne gültige Belegung keine Kante
entsteht. Wer `03` als Vorbild liest, harmonisiert das falsch; der Prompt muss es ausschreiben.

**Getragene Grenze.** Ein Vorschlag ist damit ein Bündel — eine ganze Verfassungsversion, nicht
eine einzelne Regeländerung. Der feinere Weg, Änderungen je Slot mit unabhängiger Geltung, bringt
Parallelität, erlaubt aber die Teilannahme eines Pakets und braucht eine Slot-Zerlegung. Grob
gebündelt und fein zerlegt sind beide sicher; gefährlich ist das Mischen.

### D102 — Rivalisierende Nachfolger sind arithmetisch unmöglich ⚠️

**Dieser Eintrag ersetzt einen eigenen Fehler.** Zunächst war beschlossen worden, bei zwei
Entscheidungen auf derselben Epoche setze sich die **erste Materialisierung** durch. Beim
Nachlesen von Rafts Konfigurationswechsel fiel auf, dass „zuerst" hier keine Bedeutung hat: zwei
Materialisierungen sind Claims verschiedener Autoren, und zwischen ihnen gibt es keine Ordnung.

Es ist derselbe Fehler, den Ongaro 2015 für Rafts Einzelserver-Wechsel dokumentiert hat: zwei
nebenläufige konkurrierende Konfigurationsänderungen können Quoren haben, die sich nicht
überschneiden, und erzeugen Split Brain. Die Produktionsantwort dort ist Serialisierung — höchstens
eine uncommittete Konfiguration zur Zeit —, die theoretische ist Joint Consensus, bei dem je zwei
konkurrierende Konfigurationen eine gemeinsame haben und sich deshalb überschneiden.

**Geprüft und verworfen: kleinster `epoch_id` gewinnt.** Deterministisch, uhrenfrei und sogar
konvergent, weil das Minimum über einer wachsenden Menge einen Halbverband bildet. Aber ein
Beobachter, der unter A gehandelt hat und später ein kleineres B lernt, muss zurückrollen. Das ist
Fork Choice mit Reorg und steht quer zu allem, wofür dieses Protokoll gebaut ist.

**Beschluss:** Es braucht keine Auflösung, weil der Fall nicht eintreten kann. Aus D101 folgt
höchstens ein Ja je Mitglied je Epoche; bei einer Schwelle über der Hälfte müssten sich die
Ja-Mengen zweier rivalisierender Versionen überschneiden, und niemand hat zweimal Ja gesagt. Zwei
gültig ratifizierte Nachfolger derselben Epoche sind arithmetisch unmöglich, solange kein Mitglied
doppelt gestimmt hat — und Doppelstimmen sind nach D101 nicht bloß verboten, sondern zählen nicht.

Das ist das Überschneidungsargument aus Joint Consensus, nur aus dem Stimmverhalten geholt statt
aus der Konfiguration. Damit entfällt auch der Fall, um dessentwillen der Eintrag begonnen wurde:
einen unterlegenen Vorschlag mit echter Supermajorität kann es nicht geben.

---

**Zur Fehlerform dieses Abschnitts.** D96 und D102 sind beide eigene Vorschläge, die an
Bestandsliteratur gescheitert sind — der erste am CALM-Theorem, der zweite an einem zehn Jahre
alten Raft-Befund. Beide Male war der Vorschlag intern stimmig und die widerlegende Eigenschaft
lag außerhalb des Registers. Das ist eine andere Bauart als D74 bis D92, wo die Begründung beim
Übertragen ihren Geltungsbereich verlor.

**Konsequenz — Standprüfung:** Bevor ein Mechanismus normiert wird, der Nebenläufigkeit,
Ordnung oder Schwellen betrifft, wird gefragt, unter welchem Namen dieses Problem außerhalb des
Projekts gelöst ist. Die beiden Fälle hier haben je eine Runde gekostet; ohne die Recherche
hätten sie eine Abnahme gekostet.

---

## W. Nachzug zu Layer 04 — Auflösbarkeit, Klassen, Unwiderruflichkeit

Drei Beschlüsse aus dem Entwurf des Modulschnitts. Alle drei sind Lücken, die beim Schreiben von
`04-governance.md` nicht sichtbar waren und erst auftraten, als die Signaturen der Funktionen
neben den Zustandsautomaten aus Layer 01 gelegt wurden.

### D103 — Unauflösbare Epochenzugehörigkeit einer fremden Ja-Stimme

`04 §4.4` verlangt, dass zwei aktive Ja-Stimmen desselben Autors auf verschiedene Vorschläge
**derselben Epoche** beide nicht zählen. Aus dieser Regel folgt D102: bei einer Schwelle über der
Hälfte können zwei rivalisierende Nachfolger keine getrennten Ja-Mengen haben.

Eine Stimme trägt aber nur `J = (3, proposal_hash)`. Die Epochenzugehörigkeit steht in
`proposal[1]`. Ist das Vorschlagsobjekt lokal unbekannt, ist die Bedingung nicht auswertbar, und
`04 §4.4` sagte dazu nichts.

**Beschluss:** Eine aktive Ja-Stimme auf einen lokal unbekannten Vorschlag gilt als
**möglicherweise epochengleich** und blockiert die andere Ja-Stimme desselben Autors. Vermerk
`UNKNOWN_PROPOSAL`, Subjekt die `claim_id` der unauflösbaren Stimme.

Die Richtung ist erzwungen: die Gegenannahme — unbekannt heißt fremde Epoche, also kein Konflikt —
lässt bei Teilwissen zwei gültige Nachfolger derselben Epoche entstehen. Das ist die
Über-Ratifizierungsrichtung, die `INV-04.3` ausschließt.

**Getragene Grenze.** Eine Ja-Stimme auf einen Vorschlag, dessen Objekt nie verbreitet wurde,
setzt ihren Autor für diese Epoche aus. Heilbar, indem jemand das Objekt nachreicht — es ist
content-adressiert und nicht fälschbar. Verhindern kann das Mitglied es nicht.

**Verworfen — die Epoche in der Stimme führen.** `vote.v` könnte einen Key `1` mit dem `epoch_id`
tragen; dann wäre die Zugehörigkeit ohne das Vorschlagsobjekt auswertbar. Verworfen, weil es eine
zweite Darstellung desselben Zustands neben `proposal[1]` schafft, die ihr widersprechen kann.
Zwei Darstellungen desselben Zustands haben in diesem Projekt viermal einen Befund erzeugt; bei
Widerspruch zählte die Stimme dann ohnehin nicht, und der Fall wäre nur verschoben.

### D104 — Die Reihenfolge der Schwellenklassen ist normativ

`04 §3.4` verweist für die Klasse eines allgemeinen Vorschlags auf `genesis[5]`, einen `uint`. Das
Beispiel in `00 §3.1` trägt den Wert `2` und eine Verfassung mit drei benannten Schlüsseln in
`thresholds`. Welcher Index welchen Namen bezeichnet, stand nirgends — die Zuordnung war
offensichtlich und unaufgeschrieben.

**Beschluss:** `0 = ordinary`, `1 = membership`, `2 = amendment`.

Fehlt der benannte Schlüssel in `thresholds`, ist der Vorschlag nicht auszählbar. Ein Index über
`2` ist ebenfalls nicht auszählbar und wird **nicht** auf `amendment` zurückgeführt: ein unbekannter
Index ist ein unbekannter Wille, und die sichere Richtung ist, keine Ratifizierung zu erzeugen.

### D105 — `vote@1` ist irrevocable; `t_exp` macht eine Stimme ungültig ⚠️

D97 verlangt, dass eine Stimme innerhalb einer Epoche unwiderruflich ist und ihr `t_exp` nicht
ausgewertet wird. `04 §3.1` Bedingung 5 verlangte, dass eine zählende Stimme nach `classify_all`
`ACTIVE` ist.

**Beides zusammen geht nicht.** `_classify_one` liefert für eine widerrufene Stimme `REVOKED` und
für eine abgelaufene `EXPIRED`. Wer Bedingung 5 wörtlich umsetzt, hat eine schrumpfende
Stimmenmenge — und damit fallen D96, D101 und D102 gemeinsam, weil alle drei auf der Monotonie der
Ja- und Nein-Mengen stehen.

Der naheliegende Ausweg wäre eine eigene Aktivitätsdefinition in `04`. Er ist versperrt: eine
zweite Lesart von „aktiv" neben `classify()` und `classify_all()` ist genau die Drift, gegen die
`T-02.4` gebaut wurde.

**Beschluss, dreiteilig:**

1. **`irrevocable_predicates` MUSS `vote@1` enthalten.** Damit greift der bestehende Schutz aus
   D70/D72 — `is_irrevocable` setzt `protected`, und Widerruf wie Supersede laufen ins Leere. Kein
   neuer Mechanismus, keine Sonderregel in `04`.
2. **Eine `vote@1` mit gesetztem `t_exp` ist keine gültige Stimme.** Sie zählt weder als Ja noch
   als Nein; Vermerk `VOTE_WITH_EXPIRY`. Nicht still ignoriert: `protected` schützt nicht vor
   Ablauf, und ein Feld, dessen Wert wortlos übergangen wird, ist die Stummheit, die D95 gekostet
   hat.
3. **Ein Nukleus, dessen Verfassung `vote@1` nicht führt, ist nicht auszählbar.** Vermerk
   `VOTE_REVOCABLE`, Zustand `UNEVALUABLE`. Seine Auszählung wäre nicht monoton, und dann darf sie
   kein Ergebnis liefern statt eines fragilen.

**Verhältnis zu D58.** Die Negativliste dort nennt `vouch@1`, und das Kriterium lautet, ob
Fortbestehen die konservative Lesart ist. Eine Stimme gewährt keine fortdauernde Autorität; sie ist
ein einmaliger Akt an einem einzelnen, content-adressierten Objekt. D97 hatte die Begründung
bereits geschrieben, ohne den Mechanismus zu benennen.

**Kosten.** Profil D in `04-golden-anchors.md` wurde vollständig neu gerechnet: alle drei
`constitution_hash`, `N_D`, alle drei `epoch_id` und beide `proposal_hash` ändern sich. Die
Schwellenarithmetik ist davon unberührt. Die Bestandsanker aus `00 §3.1` bleiben unangetastet;
Profil D ist ein eigener Nukleus.

**Nebenbefund.** Der Bestandsnukleus `65309fe2…` führt nur `obligation@1` und trifft damit
zusätzlich zu `weight_mode = 1` auch diese Bedingung. Er bleibt nicht auszählbar, jetzt aus zwei
unabhängigen Gründen.

---

**Zur Fehlerform dieses Abschnitts.** D105 ist die Parallelenprüfung, die diese Sitzung zweimal
selbst empfohlen und beim Schreiben von `04 §3.1` unterlassen hat: die Bedingung wurde formuliert,
ohne den Zustandsautomaten aus `01` Anhang B danebenzulegen. D103 und D104 sind Lücken, die erst
beim Entwerfen der Funktionssignaturen sichtbar wurden.

**Konsequenz — Signaturprüfung:** Der Modulschnitt wird entworfen, **bevor** der Prompt geschrieben
wird, nicht als sein erster Abschnitt. Drei der Befunde dieser Runde lagen zwischen zwei
Funktionen, nicht in einer.

---

## X. Aus dem Layer-04-Lauf

### D106 — `participants` auf `TallyResult`; zwei Vermerke für die Zeugenmenge

Zwei Rückfragen aus dem Implementierungslauf, beide korrekt zurückgegeben statt umgedeutet.

**(a) Woher kennt `verify_ratification` die Wählerschaft?** `04 §4.1` Bedingung 2 verlangt
`ratify.I` in `P`. Die Signatur im Prompt reichte `store`, `ratify`, `epoch`, `proposal`, `tally`,
`now` und `policy` — `P` war in keinem davon enthalten. Aus `tally.yes` und `tally.no` ist es nicht
rekonstruierbar: `P` wird deklariert, nie abgeleitet (D96), und ein Mitglied, das nicht abgestimmt
hat, darf materialisieren.

**Beschluss:** `TallyResult` trägt `participants: frozenset[bytes] | None`. Das bisherige Feld `n`
entfällt und wird eine abgeleitete Eigenschaft. Die Signatur von `verify_ratification` bleibt
unverändert.

Ein zusätzlicher Parameter an `verify_ratification` ist verworfen: er erlaubte, die Ratifizierung
gegen eine andere Wählerschaft zu prüfen als die, mit der ausgezählt wurde. `n` neben
`participants` wäre derselbe Fehler eine Ebene tiefer — zwei Darstellungen desselben Zustands, die
einander widersprechen können.

Folgesatz: ist `tally.state` gleich `UNEVALUABLE`, ist `participants` gleich `None`, und
`verify_ratification` liefert nie eine Epoche.

**(b) Zwei Vermerke, nicht einer.** Eine in `ratify.v[0]` zitierte `claim_id` kann auf zwei
verschiedene Weisen nicht tragen, und die Diagnose ist verschieden (D94):

| Lage | Vermerk | Bedeutung |
|---|---|---|
| Claim im Store nicht vorhanden | `UNKNOWN_WITNESS_VOTE` | mir fehlt ein Claim |
| Claim vorhanden, zählt aber nicht | `UNSUPPORTED_RATIFICATION` | die Behauptung stimmt nicht |

Beide führen dazu, dass keine Epoche entsteht — die Wirkung ist gleich, die Diagnose entscheidet.
Im ersten Fall weiß der Beobachter, welche `claim_id` er holen muss; im zweiten weiß er, dass
Holen nichts nützt.

`04-prompt.md §5` hatte `UNKNOWN_WITNESS_VOTE` auf jede `claim_id` außerhalb von `tally.yes`
angewandt und damit beide Lagen zusammengezogen. `04-governance.md §4.1` nannte nur
`UNSUPPORTED_RATIFICATION` und stellte den zweiten Vermerk nie daneben. Der Lauf hat die Lücke
zwischen beiden gefunden.

Neuer Vektor `GV-30`: `ratify@1` zitiert eine `claim_id`, die im Store nicht vorhanden ist.
Erwartung `UNKNOWN_WITNESS_VOTE`, keine Epoche. `GV-2` bleibt unverändert und deckt den zweiten
Fall.

**Zur Form dieser Runde.** Beide Punkte sind zwischen zwei Artefakten entstanden, nicht in einem:
(a) zwischen einer Spec-Bedingung und einer Prompt-Signatur, (b) zwischen einer Spec-Vermerkliste
und einer Prompt-Vermerkliste. Die Signaturprüfung aus Abschnitt W hätte (a) gefunden, wenn sie
auch die zweite Funktion erfasst hätte statt nur die erste.

---

## Y. Symmetrie an der Epochengrenze

### D107 — `ratify@1` ist irrevocable; `propose@1` ist ungeprüft ⚠️

Aus der Parallelenprüfung, die D106 als Konsequenz aufgeschrieben hatte: `decide()` und
`verify_ratification()` nebeneinandergelegt statt nacheinander gelesen.

**Der Befund.** `04 §4.1` Bedingung 2 verlangt, dass der `ratify@1`-Claim `ACTIVE` ist. D105 hat
`vote@1` in `irrevocable_predicates` gezwungen; `ratify@1` stand dort nicht.

Folge: eine bereits etablierte Epoche kann wieder verschwinden. Wer als Einziger materialisiert
hat, widerruft seinen `ratify@1`, und für jeden Beobachter, der nur diesen einen Beleg kennt,
fällt der Nukleus auf die alte Verfassung zurück — bei unveränderter Stimmenlage im Store.

Das ist derselbe Monotoniebruch, den D105 eine Ebene tiefer geschlossen hat, nur an der
Epochengrenze statt an der Stimme. `INV-04.7` sichert die Stimmenmenge; darüber war nichts
gesichert. Kein Angriff — die Tatsache bleibt nachrechenbar und jedes Mitglied kann neu
materialisieren —, aber ein Hebel in einer Hand, die ihn nicht haben sollte: nicht die Änderung
rückgängig machen, sondern sie aussetzen, bis jemand tätig wird.

**Beschluss, in der Form von D105:**

1. **`irrevocable_predicates` MUSS `ratify@1` enthalten.** Der Schutz entsteht über `is_irrevocable`
   (D70/D72), nicht über eine Sonderregel in `04`.
2. **Eine `ratify@1` mit gesetztem `t_exp` etabliert keine Epoche.** Vermerk
   `RATIFY_WITH_EXPIRY`. `protected` schützt nicht vor Ablauf, und ein still übergangenes Feld ist
   die Stummheit aus D95.
3. **Ein Nukleus, dessen Verfassung `ratify@1` nicht führt, ist nicht auszählbar.** Vermerk
   `RATIFY_REVOCABLE`, Zustand `UNEVALUABLE`.

Zu D58 verhält es sich wie bei D105: eine Materialisierung gewährt keine fortdauernde Autorität.
Sie bezeugt eine unabhängig nachrechenbare Tatsache an einem content-adressierten Objekt, und
Fortbestehen ist die konservative Lesart.

**Die Gegenrichtung, im selben Zug festgestellt.** `propose@1` wird von der Auszählung **nie
gelesen**. Eine Stimme zeigt auf den `proposal_hash`, nicht auf den `propose@1`-Claim; dieser
dient allein der Auffindbarkeit. Er braucht deshalb keinen Schutz, und eine Aktivitätsprüfung auf
ihn wäre ein Fehler — sie gäbe dem Vorschlagenden nachträglich Macht über eine Abstimmung, die
ohne ihn weiterläuft. Das stand bisher nirgends und ist die Sorte Selbstverständlichkeit, die im
Implementierungsfenster still zu einer Zeile wird.

**Verworfen — die Aktivitätsprüfung auf `ratify@1` streichen.** Billiger, aber es wäre eine
Sonderregel neben `classify_all` statt der bestehenden Mechanik, und Equivocation des
Materialisierenden bliebe ungeprüft.

**Verworfen — als getragene Grenze stehen lassen.** Selbstheilend, sobald jemand neu
materialisiert. Verworfen, weil „selbstheilend, sobald jemand tätig wird" bei einer Verfassung
etwas anderes bedeutet als bei einem Vouch: bis dahin gilt für einen Teil des Nukleus eine andere
Verfassung, und `03` bindet `constitution_hash` daran (D61).

**Kosten.** Profil D zum zweiten Mal in dieser Sitzung neu gerechnet: alle drei
`constitution_hash`, `N_D`, alle drei `epoch_id`, beide `proposal_hash`. Die Arithmetik ist
unberührt. Neue Vektoren `GV-31` bis `GV-34` und die Invariante `INV-04.8`. Der Prompt wurde vor
dem Losschicken des Werkzeugs korrigiert; es hat nie gegen die alten Zahlen gebaut.

**Zur Fehlerform.** D105 und D107 sind dieselbe Lücke auf zwei Ebenen. D105 entstand, weil `§3.1`
ohne den Zustandsautomaten aus `01` Anhang B danebengelegt geschrieben wurde; D107, weil die
Korrektur danach nur auf `vote@1` angewandt und nicht auf jedes Prädikat dieser Schicht geprüft
wurde. Eine Reparatur ist selbst eine Regel und braucht dieselbe Übertragungsprüfung wie die
Bedingung, die sie ersetzt.

**Konsequenz — Prädikatendurchgang:** Wird ein Prädikat einer Schicht mit einer
Zustandsbedingung belegt, werden **alle** Prädikate derselben Schicht daraufhin durchgegangen,
und die, die keine bekommen, werden ausdrücklich als ungeprüft benannt.

---

## Z. Aus der Layer-04-Abnahme

Drei Beschlüsse. Alle drei betreffen Zeilen, die die Umsetzung korrekt befolgt hat — es sind
Spec-Fehler, keine Implementierungsfehler.

### D108 — Eine Schwelle unterhalb der Mehrheit ist nicht auswertbar ⚠️

D102 begründet die Eindeutigkeit einer Epoche damit, dass sich die Ja-Mengen zweier rivalisierender
Vorschläge überschneiden müssen. Diese Aussage gilt nicht für jede Schwelle. Bei
`amendment: [1,3]` können zwei disjunkte Ja-Mengen von je mehr als einem Drittel entstehen — zwei
gültig ratifizierte Nachfolger derselben Epoche, und die Argumentation aus D102 fällt vollständig.

Weder `04-governance.md` noch die Anker noch der Code prüften es. **Die Voraussetzung stand in D102
in einem Nebensatz der Begründung und in keiner prüfbaren Zeile.** Das ist die Bauform aus D74 und
D87: eine Begründung, die in ihrem Ursprungskontext trug und beim Übertragen ihren Geltungsbereich
verlor — hier beim Übertragen von der Begründung in die Norm.

**Die Rechnung.** Seien `A` und `B` disjunkte Ja-Mengen, die beide durchkommen. Dann gilt
`|A| * den > num * n` und `|B| * den > num * n`; addiert und mit `|A| + |B| <= n`:

```
n * den   >=   (|A| + |B|) * den   >   2 * num * n        ->        den > 2 * num
```

Zwei disjunkte Ja-Mengen sind also genau dann unmöglich, wenn **`2 * num >= den`**. Die Grenze ist
nicht strikt: `[1,2]` bleibt zulässig, `[1,3]` und `[2,5]` nicht. Erschöpfend nachgeprüft über alle
`n` bis 60.

Weil `[1,2]` zulässig bleibt, betrifft die Bedingung `ordinary: [1,2]` aus `00 §3.1` nicht, und der
Bestandsanker `890b21e7…` bleibt gültig. Geprüft wird trotzdem nur die **angewandte** Klasse — eine
Verfassung soll nicht daran scheitern, dass ein in v1 unbenutzter Eintrag unglücklich gesetzt ist.

**Beschluss:** Die angewandte Schwelle einer Auszählung MUSS `2 * num >= den` erfüllen. Andernfalls
ist der Vorschlag nicht auswertbar: Zustand `UNEVALUABLE`, Vermerk `THRESHOLD_BELOW_MAJORITY`. Die
Prüfung gilt der **angewandten** Schwelle nach der Maximum-Regel (`04 §3.4`), also nach
`ratio_max`.

**Zur Auswertungszeit, nicht zum Inkrafttreten.** Geprüft wird beim Auszählen, nicht bei der
Ratifizierung der Verfassung, die die Schwelle setzt. Die Alternative wäre sauberer — eine
Verfassung mit zu niedriger Schwelle träte gar nicht erst in Kraft —, greift aber beim Genesis
nicht, dessen Verfassung ohne Abstimmung gilt. Die Regel stünde dann an zwei Stellen, und zwei
Darstellungen derselben Regel sind in diesem Projekt die häufigste Fehlerquelle.

Folge, offen getragen: ein Nukleus kann eine Verfassung mit zu niedriger Schwelle in Kraft haben.
Er kann dann nichts mehr ändern, weil jede Auszählung `UNEVALUABLE` liefert. Das ist eine
Sackgasse, aber eine sichtbare mit eigenem Vermerk — und die sichere Richtung gegenüber einer
Verfassung, die sich in zwei Nachfolger spaltet.

### D109 — `TallyResult` bindet sich an Epoche und Vorschlag

`verify_ratification` nahm `epoch`, `proposal` und `tally` als unabhängige Argumente und prüfte
nie, ob die Auszählung zu diesem Paar gehört. Ein Aufrufer mit einem fremden `TallyResult` bekam
die Zeugenmenge gegen eine fremde `yes`-Menge validiert und konnte eine Epoche etablieren, die
niemand beschlossen hat.

Das ist D106 eine Ebene höher. Dort wurde `participants` als Parameter gestrichen, damit die
Wählerschaft nicht auseinanderlaufen kann; dabei blieb unbemerkt, dass das ganze `tally` genauso
frei gereicht wird.

**Beschluss:** `TallyResult` trägt `epoch_id: bytes` und `proposal_hash: bytes`.
`verify_ratification` vergleicht beide mit `epoch.epoch_id` und `proposal.proposal_hash` und wirft
bei Abweichung `ValueError`.

`ValueError` und kein Vermerk: nach D82 und D92 ist ein fehlzugeordnetes Objekt ein Aufruferfehler.
Ein Vermerk hieße, der Fall sei eine Lage der Welt; er ist ein Programmierfehler.

### D110 — Kein Urteil aus einem Objekt mit ungeprüfter Zugehörigkeit

Zwei Befunde derselben Regel.

**(a) `STALE_EPOCH_VOTE` ist eine Paar-Eigenschaft, keine Stimmbedingung.** `04 §3.1` führte
`proposal.predecessor == epoch_id` als Bedingung 3 unter den Stimmen auf. Die Bedingung betrifft
das Paar `(epoch, proposal)` und ist einmal zu prüfen, nicht je Stimme. Wörtlich umgesetzt entsteht
Rauschen über Stimmen fremder Epochen — und, schwerer, bei einem nicht passenden Paar **ohne**
Stimmen wird die Bedingung nie erreicht: die Auszählung läuft durch und liefert `PENDING` statt
eines Fehlers.

**(b) Die Identitätsprüfung des Zielobjekts kam zu spät.** `04 §3.5` führte
`PROPOSAL_CONSTITUTION_UNAVAILABLE` als letzte Zeile, während die Klassen- und Schwellenprüfung
darüber das Zielobjekt bereits las. Passt dessen Hash nicht, wird eine Diagnose aus einem Objekt
gezogen, das nicht das gemeinte ist.

**Beschluss:**

1. Die Paarprüfung wandert an den Anfang von `decide()`, **vor** die Abbruchtabelle. Abweichung
   ergibt `UNEVALUABLE` mit `STALE_EPOCH_VOTE`, Subjekt der `proposal_hash`. Innerhalb der
   Stimmschleife entfällt die Bedingung ersatzlos.
2. Die Identitätsprüfung beider Verfassungsobjekte steht **vor** jeder Prüfung, die ihren Inhalt
   liest.

Die gemeinsame Regel, ab hier normativ für alle Schichten: **kein Vermerk und kein Zustand wird aus
einem Objekt abgeleitet, dessen Zugehörigkeit nicht vorher bestätigt wurde.**

### Nachzug ohne eigene Nummer

Aus derselben Abnahme, ohne Fork und deshalb hier statt als eigener Eintrag:

- **Schwellenform.** `_is_ratio` prüfte zwei Integer. Bei `den = 0` ist jeder Vorschlag lautlos
  sofort `FAILED`, bei `num < 0` ist er ohne eine einzige Stimme `PASSED` — `reached(0, n, -1, 2)`
  vergleicht `0 > -n`. Verlangt sind `den >= 1`, `num >= 0`, `num <= den`, dazu `2 * num >= den`
  aus D108; sonst `MALFORMED_THRESHOLD`.
- **Doppelte Klassenbestimmung.** `decide()` leitet die Klasse inline ab und ruft danach
  `threshold_for()` auf, das dieselbe Ableitung wiederholt. Zwei Implementierungen einer Regel in
  einer Datei, mit der Driftgefahr, gegen die `T-02.4` gebaut wurde. `decide()` benutzt
  `threshold_for()`.
- **`§4.1` Bedingung 4 ist impliziert, nicht geprüft.** Die Spec verlangt, dass keine zwei
  zitierten `claim_id` Stimmen desselben Autors bezeichnen; der Code prüft doppelte `claim_id`.
  Das genügt nur, weil `tally.yes` je Autor höchstens eine Stimme führt — eine Invariante trägt
  eine Bedingung, statt dass sie geprüft wird.
- **`SCOPE_MISMATCH` für jede fremde Stimme.** Jede `vote@1` eines beliebigen anderen Nukleus im
  Store erzeugt einen Vermerk. `membership()` vergibt ihn erst, nachdem Subjekt und Prädikat
  passen; in einem Multi-Nukleus-Store schwemmt die Liste sonst über.
- **`NucleusPolicy.declared` wird überschrieben.** Der Konstruktor ersetzt das Feld durch die
  gefilterte Menge. Nach der Konstruktion ist nicht mehr feststellbar, was die Verfassung erklärt
  hat; der Vergleich „erklärt gegen wirksam" ist verloren. Entweder bleibt `declared` unangetastet
  oder es tritt ein zweites Feld daneben.
- **`NucleusPolicy.warnings` ist nicht sortiert und nicht dedupliziert.** Die Malformed-Notizen
  werden in Eingabereihenfolge angehängt. Bekommt der Konstruktor ein `frozenset` — was
  `resolve_policy` in zwei von drei Rückgabepfaden tut —, ist die Reihenfolge nicht bestimmt:
  **zwei Läufe über dieselbe Verfassung liefern verschiedene Tupel.** Jede andere Vermerkliste im
  Projekt geht durch `dedupe_sort`; diese muss es auch.
- **Leere `participants`.** Eine leere Liste ist sortiert und duplikatfrei und passiert die
  Formprüfung. Mit `n = 0` ist jeder Vorschlag sofort `FAILED`, und die Diagnose sagt „abgelehnt",
  wo „niemand konnte abstimmen" gemeint ist. Mindestens ein Eintrag, sonst
  `MALFORMED_PARTICIPANTS`.
- **`TALLY_UNEVALUABLE`.** `verify_ratification` meldete bei nicht auswertbarer Auszählung
  `UNSUPPORTED_RATIFICATION` — „die Behauptung stimmt nicht", wo „ich konnte nicht auswerten"
  gemeint ist. Eigener Vermerk nach D94.
- **Bedingungsreihenfolge in `04 §3.1`.** Die Umsetzung prüft `t_exp` und `choice` vor `ACTIVE`.
  Wirkung identisch, Diagnose besser: eine abgelaufene Stimme mit gesetztem `t_exp` bekommt
  `VOTE_WITH_EXPIRY` statt lautlos zu verschwinden. **Die Spec wird auf die Implementierung
  nachgezogen**, wie bei `Derivation(bfs, findings)` in Layer 02.
- **Textwert in `irrevocable_predicates`.** Ein `str` ist iterierbar; `list("obligation@1")` liefert
  zwölf Einzelzeichen und damit zwölf Vermerke auf Symptome statt einen auf die Ursache. Ein `str`
  wird wie ein nicht iterierbarer Wert behandelt: ein Vermerk mit `repr`, Liste vollständig
  ausgefallen. Präzisierung zu D95.

### D111 — `membership()` prüft die Zugehörigkeit seiner Teilnehmerliste

Dieselbe Regel wie D109, eine Schicht tiefer. `membership()` nimmt `constitution_hash` und
`participants` als unabhängige Argumente entgegen und prüft nie, dass die Liste zu genau dieser
Verfassungsversion gehört. Ein Aufrufer kann `participants` aus Epoche 3 mit dem
`constitution_hash` aus Epoche 2 verbinden und bekommt `MEMBER`.

Die Lücke stammt aus `04-prompt.md §7`, nicht aus der Umsetzung: dort steht der Parameter genau so.

**Beschluss:** `membership()` nimmt statt `participants` ein `constitution_obj: dict | None`. Ist
es gesetzt, prüft die Funktion `constitution_hash(constitution_obj)` gegen den Parameter
`constitution_hash` und wirft bei Abweichung `ValueError` (D82, D92, D109); die Teilnehmerliste
wird daraus gelesen, nicht separat gereicht.

Damit zeigen beide Konjunkte der Mitgliedschaft auf **dasselbe** content-adressierte Objekt, wie
`04 §6.1` es beschreibt. Die vier Zustände und die `accept-rules`-Strecke bleiben unverändert.

**Zur Fehlerform.** Von siebzehn Abnahmebefunden aus zwei unabhängigen Durchgängen lagen elf
**zwischen** zwei Stellen, nicht in einer. Vier der fünf Blocker beschreiben Zeilen, die die
Umsetzung korrekt befolgt hat.

Der zweite Durchgang war die Kontrolle wert: er hat D108 korrigiert — die dort zunächst behauptete
Grenze `2 * num > den` war zu streng und ohne Herleitung aufgeschrieben — und sechs Befunde
ergänzt, von denen einer (`warnings` ohne feste Reihenfolge) ein Determinismusbruch ist.

**Konsequenz — Voraussetzungsprüfung:** Trägt eine Invariante eine Voraussetzung, gehört diese in
dieselbe normative Tabelle wie die Invariante, nie in ihren Begründungstext. D108 wäre sonst erst
an einem echten Nukleus aufgefallen.

---

## AA. Zugehörigkeit aller Felder

### D112 — `proposal.scope` wird geprüft; Schwellenvalidierung vor Umwandlung ⚠️

Zwei Befunde aus der zweiten Abnahme (`impl/04a-korrektur`, `e576663`). Beide sind klein, beide
gehören zu derselben Regel, und der erste ist die **vierte** Wiederholung derselben Form.

**(a) `proposal.scope` wird nirgends geprüft.** `Proposal` trägt ein eigenes `scope`-Feld. Weder
`decide()` noch `verify_ratification()` vergleichen es mit `epoch.scope`. Ein Vorschlagsobjekt
eines fremden Nukleus, dessen `predecessor` zufällig oder absichtlich auf diese Epoche zeigt, wird
ausgezählt; die daraus entstehende Epoche trägt `scope = epoch.scope` und eine Verfassung, die für
einen anderen Nukleus geschrieben wurde.

Das ist wörtlich der Satz, den D110 normativ gemacht hat: kein Vermerk und kein Zustand aus einem
Objekt, dessen Zugehörigkeit nicht vorher bestätigt wurde. D109 hat `epoch_id` und
`proposal_hash` gebunden; das dritte Feld desselben Objekts blieb ungeprüft.

**Beschluss:** `proposal.scope != epoch.scope` ist ein **`ValueError`**, geprüft als erste
Bedingung in `decide()` und in `verify_ratification()`, vor der Paarprüfung. Kein Vermerk: ein
fehlzugeordnetes Objekt ist ein Aufruferfehler und keine Lage der Welt (D82, D92, D109).

**(b) Die Schwellenvalidierung läuft nach der Umwandlung.** `threshold_for()` coerciert mit
`int(old_th[0])`, bevor `_is_ratio` je aufgerufen wird. Bei `thresholds.amendment = ["a","b"]`
wirft `int("a")` einen `ValueError`, der in der `except (KeyError, TypeError, IndexError)`-Liste
von `decide()` nicht steht: eine formwidrige Verfassung reißt den Aufruf ab, statt
`MALFORMED_THRESHOLD` zu liefern.

**Beschluss:** `_is_ratio` läuft auf den Rohwerten beider Verfassungen, **bevor** `threshold_for`
sie anfasst. `threshold_for` coerciert nicht mehr; sie bekommt bereits geprüfte Integer-Paare.

Vektoren: `GV-46` fremder `proposal.scope` → `ValueError`; `GV-47` `thresholds` mit Textwerten →
`MALFORMED_THRESHOLD`, kein Abbruch.

**Zur Fehlerform — vierte Wiederholung.** D105 schützte `vote@1` und vergaß `ratify@1` (→ D107).
D106 zog `participants` nach `TallyResult` und ließ `epoch_id` und `proposal_hash` draußen
(→ D109). D109 band beide und übersah `membership()` (→ D111). D111 band die Teilnehmerliste und
übersah `proposal.scope` (→ D112). Jedes Mal war die Reparatur richtig und unvollständig auf die
Geschwister ihrer eigenen Art.

Die bisherigen Konsequenzen — Prädikatendurchgang (D107) und die Eingabenprüfung aus der Abnahme —
setzen beide beim **Beheben** an. Das ist zu spät: wer einen Befund behebt, sieht die Geschwister
des Befunds, nicht die Geschwister des Feldes.

**Konsequenz — Zugehörigkeitsliste am Datentyp:** Trägt ein Datentyp Felder, die seine
Zugehörigkeit zu einem Kontext behaupten, wird die vollständige Liste dieser Felder **bei seiner
Definition** aufgeschrieben, zusammen mit dem Kontext, gegen den jedes zu prüfen ist. Für
`Proposal` sind es drei: `scope`, `predecessor`, `constitution_hash`. Die Liste wird nicht beim
Beheben eines Befunds angelegt, sondern beim Schreiben des Typs — sonst wächst sie immer nur um
das eine Feld, das gerade wehgetan hat.

---

## AB. Reihenfolge und Abhängigkeit

### D113 — `threshold_for` wird geteilt

Befund aus der dritten Abnahme (`impl/04b-korrektur`, `5714bbc`). Klein, aber es ist die
Wiederkehr eines bereits behobenen Befunds, und der Grund dafür ist lehrreich.

**Was passiert ist.** D112 verlangte, dass `_is_ratio` auf den Rohwerten läuft, **bevor**
`threshold_for` sie anfasst. `threshold_for` liefert aber zugleich die Klasse, und die
`_is_ratio`-Schleife braucht sie. Ohne Umbau der Signatur gab es genau einen Weg: die
Klassenableitung wurde ein zweites Mal inline in `decide()` eingesetzt, und `threshold_for`
bestimmt sie danach erneut.

Damit ist **B-3 der ersten Abnahme wiederhergestellt** — zwei Implementierungen derselben Regel in
derselben Datei, in `04a` behoben, in `04b` zurück. Laufen sie je auseinander, wird die Schwelle
einer anderen Klasse validiert als angewandt.

Zusätzlich ist das `try/except (KeyError, TypeError, IndexError)` um `threshold_for` seit der
vorgezogenen Validierung **unerreichbar**. Unerreichbarer Code, der einen Fehlerfall vortäuscht,
ist die stille Variante des Problems: er suggeriert eine Absicherung, die nichts absichert.

**Beschluss:** `threshold_for` wird in zwei Funktionen geteilt.

```
threshold_class(old_obj, new_obj, genesis_obj) -> str
applied_threshold(old_obj, new_obj, klass)     -> tuple[int, int]
```

`decide()` ruft `threshold_class` **einmal**, validiert beide Schwellen mit `_is_ratio`, ruft dann
`applied_threshold`. Das `try/except` entfällt. Eine Implementierung der Regel, kein unerreichbarer
Zweig, und die Reihenfolge aus D112 bleibt.

Keine neue Bedingung, keine neue Zahl: die Testzahl bleibt unverändert.

**Zur Fehlerform — eine neue.** Die Kette D105 bis D112 war viermal dieselbe Unvollständigkeit auf
Geschwister. Dies hier ist etwas anderes: eine Reparatur hat eine **Reihenfolge** vorgeschrieben,
ohne zu sagen, wie die Abhängigkeit aufzulösen ist, die in der alten Reihenfolge miterledigt wurde.
Die einzig mögliche Auflösung hat einen früheren Befund zurückgebracht.

Der Korrekturprompt schrieb „die Klassenbestimmung darf vorher laufen" und ließ offen, **woher**
sie dann kommt. Die Umsetzung war die einzige, die ohne Signaturänderung möglich war.

**Konsequenz — Abhängigkeitssatz bei Reihenfolgeänderungen:** Wird eine Reihenfolge normativ
geändert, wird für jede Größe, die in der alten Reihenfolge nebenbei entstand, ausdrücklich
benannt, woher sie in der neuen kommt. Fehlt der Satz, wählt die Umsetzung den kürzesten Weg — und
der ist Duplikation.

---

## AC. Trennung, Nachfolge und der Schnitt bei der Gründung

### D114 — `parent_scope` ist deklarativ; Governance und Substanz gehören getrennt

Ausgelöst durch eine Frage, die kein Randfall ist: zwei Gründer zerstreiten sich. Aldi und
Vapiano sind die bekannten Fälle, und in beiden war die Auflösung nicht eine Abstimmung, sondern
eine Trennung.

**Die Ausgangslage ist unparametrierbar.** Bei `n = 2` verlangt **jede** nach D108 zulässige
Schwelle Einstimmigkeit — das folgt direkt aus `2 * num >= den`: was zwei disjunkte Ja-Mengen
ausschließt, ist mit einer von zwei Stimmen nicht erreichbar. Es gibt keinen Wert, der hilft. Bei
`n = 3` gibt es Klassen ohne Einstimmigkeit, aber nur mit `num/den` nahe der Hälfte; ab `2/3`
fällt es zurück. Der neutrale Dritte ist damit ausdrückbar — als **Mitglied** unter Gleichen, nie
als Instanz darüber, denn die gibt es in MaR nicht (`04 §8`).

Bleibt die Frage, was eine Trennung kostet. Und die entscheidet sich bei der Gründung.

**(a) `parent_scope` ist eine Behauptung, keine Beziehung.** Das Feld steht seit `00 §4` im
Genesis-Schema, wird aber von **keiner** Funktion gelesen — nicht in `02`, nicht in `03`, nicht in
`04`. Sein Name suggeriert eine Über-/Unterordnung, die es nicht gibt und nach `02 §2` auch nicht
geben kann: es gibt einen Graphen je `N`, Vertrauen fließt nicht über Scope-Grenzen, und D92
verbietet scope-fremde Verdikte.

**Beschluss:** Das Feld ist rein deklarativ und bekommt in `00 §4.1` einen ausdrücklichen Satz
dazu. Es begründet keine Autorität, keine Übertragung, keinen Vorrang. Es behauptet eine
Zugehörigkeit oder Nachfolge, prüfbar über die Genesis-Kette, bewertet vom Leser — das Protokoll
erzwingt Zurechenbarkeit, nicht Wahrheit (`08 §2.1`).

Ausdrücklich zugelassen: **mehrere Nuklei dürfen dieselbe Elternschaft behaupten.** Spaltet sich
eine Gemeinschaft, berufen sich beide Hälften auf denselben Vorgänger, und keine kann die andere
daran hindern. Welche als Fortsetzung gilt, entscheiden die Beteiligten. Das Protokoll bildet den
Streit ab, statt ihn zu entscheiden.

**(b) Governance und Substanz gehören in getrennte Scopes.** Empfehlung, keine Prüfung, in
`00 §4.2`. Vouches, Obligationen und Quittungen gehören nicht in den Scope, dessen `participants`
abgestimmt werden. Der Governance-Scope regiert genau eine Sache: sich selbst. Die Substanz lebt
daneben, in einem Scope ohne `participants` — er ist damit nach `04 §3.5` nicht auszählbar und
braucht es nicht, weil Bürgen, Verpflichten und Quittieren zweiseitige Akte ohne Kollektivbeschluss
sind.

Damit kostet ein Zerwürfnis das Regelwerk und nicht die Substanz: die Kanten tragen ein anderes
`N` und bleiben unberührt, egal wie fest der Governance-Scope steckt. Wer beide Hälften trennen
will, gründet zwei neue Governance-Scopes und bleibt im gemeinsamen Substanz-Scope — verschiedene
Regelwerke, dieselbe Wirtschaft.

**Der Preis, offen benannt:** ein Scope ohne Governance hat **unveränderliche Arbitratoren**, weil
`03 §2.4` sie aus der Verfassung des eigenen Scopes nimmt. Mit zwei Personen bekommt man nicht
beides — änderbare Regeln und unangreifbare Substanz —, ohne einen dritten Scope oder einen der
beiden Nachteile.

Und der teure Fall bleibt teuer: wollen die Hälften auch getrennte Wirtschaften, beginnt eine bei
null. Das folgt aus der Kontextbindung in `02 §2` und lässt sich für den Trennungsfall nicht
aussetzen, ohne die Eigenschaft aufzugeben, wegen der das Ganze funktioniert.

**(c) Keine Stilllegungsmarkierung.** Ein Nukleus, in dem niemand mehr signiert, ist stillgelegt;
das erkennt jeder Beobachter an seinem eigenen Bestand. Eine Markierung wäre eine globale Aussage
über etwas, das nur lokal beobachtbar ist.

**Nebenbei korrigiert.** `00 §4` Key 5 trug noch „in v1 selbst unveränderlich" — überholt durch
die Maximum-Regel aus `04 §3.4`, und die Klassenzuordnung aus D104 fehlte. Beides nachgezogen.

**Zur Fehlerform.** `parent_scope` stand seit Layer 00 im Schema und hatte nie eine Wirkung. Kein
Durchgang hat es gefunden, weil alle Prüfungen von einer Funktion ausgingen und fragten, ob sie
richtig ist — nicht von einem Feld und ob es überhaupt gelesen wird.

**Konsequenz — Feldinventur:** Vor der Abnahme einer Schicht wird für jedes Feld ihrer Schemata
benannt, welche Funktion es liest. Felder ohne Leser sind entweder zu streichen oder als
deklarativ zu kennzeichnen; sie schweigend stehen zu lassen erzeugt eine Erwartung, die niemand
einlöst.

---

## AD. Trust-Parameter bekommen einen Ort

### D115 — Optionaler Genesis-Key 9 `trust_params`

`C₀`, `γ` und `D` haben seit Layer 02 keinen deklarierten Ort. `02 §8` nennt sie „Policy-Knöpfe",
ohne zu sagen wo; die acht Genesis-Keys und die vier Verfassungsfelder tragen sie nicht. Für
Layer 04 war das folgenlos, seit D98 die Gewichtung herausgenommen hat. Für einen **rechenbaren**
Nukleus ist es das nicht: ohne festen Ort rechnen zwei Betreiber verschiedene Kapazitäten, und
`trust()` ist nicht reproduzierbar.

**Beschluss:** Optionaler Genesis-Key `9`.

```
9 trust_params : { 0: C₀, 1: γ_num, 2: γ_den, 3: D }     ; alle uint
```

**Genesis, nicht Verfassung.** `D` steckt über `n/D` in signierten Vouches; eine änderbare
Deklaration würde Bestandssignaturen still umbewerten. D35 verlangt genau deshalb
Unveränderlichkeit über die Lebensdauer eines Scopes, und unveränderlich ist nur das Genesis.
`C₀` und `γ` reisen mit, weil sie zur selben Kalibrierung gehören und ein Nukleus, der die eine
Hälfte festlegt und die andere nicht, keine reproduzierbare Kapazität hat.

**Optional.** Fehlt der Key, gilt Bestandsverhalten: die Parameter sind out-of-band und
`trust()`/`rank()` verlangen sie weiterhin als Aufruferargument. Damit bleibt der Bestandsanker
`65309fe2…` unberührt — das kanonische Beispiel aus `00 §3.1` lässt den Key weg.

**Wohlgeformtheit**, geprüft bei Anwesenheit: `C₀ >= 1`, `D >= 1`, `1 <= γ_num < γ_den`. Dazu die
Empfehlung aus `02 §8` als SHOULD: `D >= C₀`, damit stets `C(I)` bindet und nicht `D`.

Die Reichweite folgt daraus und ist keine Wahl mehr, sondern eine Rechnung:
`r_max = ⌊log_{1/γ} C₀⌋`. Bei `C₀ = 100` und `γ = 1/2` sind das sechs Hops — jenseits davon ist
`⌊C₀γ^d⌋ = 0`, und kein Vouch trägt mehr.

**Was das nicht ist.** Ein Nukleus darf jeden Wert wählen; das Protokoll fixiert keinen Default.
Ein Reichweitenparameter entscheidet, wie weit jemand wirken kann, und verteilt damit Macht —
nach `08 §3` gehört er in die Verfassung eines konkreten Nukleus und nicht in die Schicht. Das
Genesis ist hier nur der **Ort der Festlegung**, nicht der Ort der Wahl.

---

## AE. Wer entscheidet und wer gebunden ist

### D116 — `participants` und Mitgliedschaft sind zwei Fragen

Aufgefallen beim Vervollständigen des Beispielnukleus, also an einem gerechneten Fall und nicht
beim Lesen.

**Zwei Abschnitte derselben Datei definieren „gehört dazu" verschieden.** `04 §2.1` macht die
Stimmberechtigung an `vote.I ∈ P` fest — der deklarierten Liste, mehr nicht. `04 §6.1` macht
Mitgliedschaft an der Konjunktion aus `participants` und einer aktiven `accept-rules` auf genau
diesen `constitution_hash` fest (D60).

Nach jeder Ratifizierung fallen beide auseinander: der Hash ist neu, die alten Annahmen zeigen auf
den vorigen, und `03 §4` zählt sie für die neue Version ausdrücklich **gar nicht**
(`CONSTITUTION_VERSION_MISMATCH`).

**Folge: unmittelbar nach jeder Verfassungsänderung ist niemand mehr `MEMBER`.** Alle sind
`GRANT_ONLY`, bis jede und jeder einzeln die neue Fassung annimmt — und zugleich dürfen alle
weiter abstimmen, weil `participants` unverändert gilt. Es stimmt also jemand unter einer
Verfassung ab, der ihr ausdrücklich nicht zugestimmt hat.

**Beschluss: keine Mechanikänderung.** Die Mechanik ist richtig, die Spec war stumm.

Die Alternative wäre schlechter: verlangte die Stimmberechtigung `MEMBER`, könnte eine
Ratifizierung den Nukleus einfrieren — niemand dürfte abstimmen, bis alle angenommen haben, und
wer nie annimmt, blockiert dauerhaft. Das ist die Sackgasse aus dem Zwei-Personen-Fall, nur mit
einem zusätzlichen Schritt davor.

Normativ in `04 §6`:

> `participants` und Mitgliedschaft beantworten zwei verschiedene Fragen. Die Liste bestimmt,
> **wer entscheidet**; die Annahme bestimmt, **wer gebunden ist**. Nach einer Ratifizierung ist
> jedes Mitglied `GRANT_ONLY`, bis es die neue Fassung annimmt; die Stimmberechtigung bleibt davon
> unberührt. Wer eine Änderung ablehnt, behält damit die Mittel, sie rückgängig zu machen.

Getragene Grenze in `04 §8` und Betriebswarnung in `example-nucleus.md`: **eine
Verfassungsänderung entzieht allen still den `MEMBER`-Status.** Alles, was auf `MEMBER` prüft,
hört auf zu wirken, bis neu signiert ist. Kein Fehler, aber eine Rechnung, die ein Betreiber vor
der ersten Änderung kennen muss.

**Zur Fehlerform.** Kein Durchgang hat das gefunden — weder die Parallelenprüfung noch die
Feldinventur, weil beide Definitionen für sich richtig sind und erst über einen **Epochenwechsel**
hinweg auseinanderlaufen. Sichtbar wurde es, als ein Beispiel mit echten Zahlen zwei Epochen
durchlaufen musste.

**Konsequenz — Zustandsübergang statt Zustand:** Wo zwei Begriffe denselben Sachverhalt
beschreiben, werden sie nicht nur nebeneinandergelegt, sondern über den Übergang geführt, der
beide berührt. Nebeneinander waren `§2.1` und `§6.1` widerspruchsfrei; erst die Ratifizierung
zwischen ihnen zeigt die Lücke.

---

## AF. Der dritte Ausgang aus `ACTIVE`

### D117 — Equivocation hebt Monotonie auf ⚠️

Gefunden beim Durchrechnen eines Simulationsszenarios mit **vier getrennten Stores** — nicht
beim Lesen des Codes und nicht in einem Durchgang durch die Spec.

**Der Befund.** D105 und D107 haben die Monotonie der Stimmen- und Epochenmenge gesichert, indem
`vote@1` und `ratify@1` in `irrevocable_predicates` stehen: Widerruf und Supersede laufen ins
Leere, Ablauf ist über `VOTE_WITH_EXPIRY` ausgeschlossen. Damit waren zwei Ausgänge aus `ACTIVE`
geschlossen.

Es gibt einen dritten. In `_classify_one` steht die Equivocation-Prüfung **vor** allem anderen und
vor der Ermittlung von `protected`:

```
if _is_in_equivocation_pair(claim, store):
    return Classification(state=EQUIVOCATION_FLAGGED, trust_usable=False)
```

`is_irrevocable` schützt nicht davor — und soll es nicht, denn ein Schutz gegen Equivocation wäre
ein Schutz des Doppelzüngigen. Eine Stimme, die eben noch zählte, hört auf zu zählen, sobald ihr
Zwilling beim Beobachter eintrifft.

**Damit sinkt die Ja-Menge durch Wissenszuwachs.** Gerechnet, `n = 3`, Schwelle `[1,2]`, zwei Ja
nötig. Anna signiert zwei Stimmen mit demselben `h_prev` — ein Ja an Bruno, ein Nein an Chris.
Chris stimmt mit Ja.

| Beobachter | kennt | Ja | Nein | Zustand |
|---|---|---|---|---|
| Bruno, vor Austausch | Anna-Ja, Chris-Ja | 2 | 0 | **`PASSED`** |
| Chris, vor Austausch | Anna-Nein, Chris-Ja | 1 | 1 | `PENDING` |
| beide, nach Austausch | Anna geflaggt, Chris-Ja | 1 | 0 | `PENDING` |

Brunos `PASSED` kippt zurück — `INV-04.7` ist verletzt. Hat er zwischenzeitlich materialisiert,
zitiert sein `ratify@1` eine nicht mehr zählende Stimme, es entsteht
`UNSUPPORTED_RATIFICATION`, und die Epoche fällt — `INV-04.8` ist verletzt.

**Beschluss: keine Mechanikänderung.** Die Mechanik ist richtig, die Invarianten waren zu stark
formuliert.

Richtig, weil die Richtung sicher ist: es fällt weg, es entsteht nichts. Und weil der Vorgang
einen vom Urheber **selbst signierten** Beweis seiner Doppelzüngigkeit hinterlässt — das ist
`08 §2.2` in Reinform, nicht verhindert, sondern unbestreitbar. Die Folge gehört nach Layer 05,
nicht in eine Sonderregel hier.

Normativ, als Vorbehalt an `INV-04.7` und `INV-04.8`:

> Beide Invarianten gelten unter der Bedingung, dass kein Mitglied equivociert. Eine Equivocation
> entzieht der betroffenen Stimme rückwirkend die Wirkung; eine darauf gestützte Ratifizierung
> wird `UNSUPPORTED_RATIFICATION`, und die Epoche fällt. Die Richtung ist stets abwärts.

Ein einzelnes Mitglied kann damit eine Epoche kippen — aber nur einmal, nur unter Hinterlassung
des Beweises, und nur nach unten.

**Zur Fehlerform.** Bei D105 wurden die Ausgänge aus `ACTIVE` aufgezählt und zwei genannt:
Widerruf und Ablauf. Der dritte stand als **erste Zeile** derselben Funktion.

Und er wurde von keinem Durchgang gefunden, weil alle bisherigen mit einem gemeinsamen Wissensstand
gerechnet haben. In einem gemeinsamen Store trifft der Zwilling sofort ein, `PASSED` entsteht gar
nicht erst, und der Rückfall ist unsichtbar. Sichtbar wurde es erst beim Entwurf einer Simulation
mit **getrennten** Stores.

**Konsequenz — Ausgänge aufzählen:** Wo eine Invariante einen Zustandsübergang ausschließt, werden
**alle** Ausgänge aus dem Zustand aufgezählt und einzeln geprüft — nicht die, an die man beim
Schreiben dachte. Die Aufzählung entsteht aus dem Code der Zustandsfunktion, nicht aus dem
Gedächtnis.

**Konsequenz — getrennte Sicht:** Eigenschaften über Wissenszuwachs werden mit **mehreren**
Beobachtern geprüft, die verschiedene Teilmengen halten. Ein einzelner Store kann Konvergenz nicht
widerlegen, weil in ihm nichts auseinanderläuft.

---

## AG. Monotonie gilt für den Graphen, nicht für den Bestand

### D118 — Die Budgetprüfung ist die zweite gefährliche Richtung ⚠️

Gefunden beim Durchrechnen einer Fuzzing-Eigenschaft, **bevor** sie aufgeschrieben wurde. Die
Eigenschaft lautete zunächst „eine Teilmenge des Claim-Bestands liefert nie höheres Vertrauen als
der volle Bestand". Sie ist falsch.

**Was `02 §7` zusagt.** Max-Flow ist monoton in den Kanten; fehlende Vouch-Kanten können den
Fluss nur senken, das Ergebnis ist eine konservative Untergrenze, im Zweifel wird
unter-vertraut. Und: „Die einzige gefährliche Richtung: ein fehlender *Widerruf*."

**Was tatsächlich gilt.** Der Satz stimmt für den **Graphen**. Zwischen Claim-Bestand und Graph
sitzt aber die Budgetprüfung `Σ n ≤ D`, und die ist **nicht monoton**: ein hinzukommender Vouch
kann `Σ n` über `D` heben, und dann fallen nach `02 §3.1` **alle** Kanten dieses Autors aus —
nicht die letzte, nicht anteilig.

Gerechnet, `D = 100`, Anna bürgt dreimal mit `n = 50`:

| Beobachter kennt | `Σ n` | Kanten von Anna |
|---|---|---|
| einen Vouch | 50 | zählt |
| zwei Vouches | 100 | beide zählen |
| alle drei | 150 | **alle drei fallen aus** — `OVERCOMMITTED_AUTHOR` |

**Wer weniger weiß, sieht mehr Vertrauen.** Das ist Über-Vertrauen bei Teilwissen, also die
gefährliche Richtung — und der fehlende Claim ist eine **Bürgschaft**, die `02 §7` ausdrücklich
als harmlos führt.

Die drei dort genannten Abwehren greifen nicht: `t_exp` ist eine Decke gegen alte Kanten, nicht
gegen unbekannte; Priorität beim Widerruf betrifft ein anderes Prädikat; frische positive Evidenz
hilft nicht, wenn gerade die Evidenz das Problem ist.

Kleinstes Gegenbeispiel: **zwei Vouches mit `n = 51`** bei `D = 100`. Zwei Claims genügen.

**Beschluss: keine Mechanikänderung.** Die Mechanik ist richtig, `02 §7` war zu stark.

Richtig, weil der Ausfall aller Kanten die einzige Antwort ist, die nicht interpretiert: welche
zwei der drei Bürgschaften „gemeint" waren, kann niemand entscheiden, und eine anteilige Kürzung
wäre eine Erfindung des Verifizierers. Und weil der Fall selbstheilend ist: sobald der dritte
Vouch eintrifft, fällt alles, und die Richtung ist danach dauerhaft konservativ. Ein Angriff mit
Gewinn ist es nicht — der Überzeichnende verliert sein gesamtes Budget und hinterlässt einen
signierten Beweis. Die Folge gehört nach Layer 05 (D40), nicht in eine Sonderregel hier.

Normativ in `02 §7`:

> Die Monotonie gilt für den **Graphen**, nicht für den **Claim-Bestand**. Zwischen beiden liegt
> die Budgetprüfung, und sie ist nicht monoton: ein hinzukommender Vouch kann `Σ n > D` auslösen
> und damit alle Kanten seines Autors entfernen. Ein Beobachter mit Teilwissen kann deshalb
> **über**-vertrauen. Das ist neben dem fehlenden Widerruf die zweite gefährliche Richtung; sie
> heilt beim Zustellen und hinterlässt einen signierten Beweis.

**Zur Fehlerform.** Dritte Wiederholung derselben Bauart nach D117 und D116: eine Zusage, die auf
ihrer eigenen Stufe stimmt und beim Blick über die Stufengrenze nicht mehr. Bei D116 war es der
Übergang zwischen zwei Epochen, bei D117 der dritte Ausgang aus einem Zustand, hier die Stufe
zwischen Bestand und Graph.

**Konsequenz — Monotonie stufenweise:** Wird eine Monotonieaussage über eine Ableitung gemacht,
gilt sie zunächst nur für die **letzte** Stufe. Jede Stufe davor — Filter, Budgetprüfung,
Zustandsauswertung, Kanonizitätsprüfung — wird einzeln daraufhin geprüft, ob sie monoton ist, und
das Ergebnis wird im Text benannt. Max-Flow ist monoton; der Weg dorthin ist es an zwei Stellen
nicht.

## AH. Autorschaft, Werkzeug und Schreibautorität

### D119 — `02 §6.2` bekommt einen Leser

`02 §6.2` verlangt: in Scopes mit Budgetregel MUSS ein Vouch `t_exp` tragen, oder die Policy
setzt eine Maximallaufzeit als Default. `§8` macht `Σw ≤ 1` zum Default, ein schweigender
Nukleus trägt die Regel also, und `check_overcommit` rechnet sie im Beispiel durch.

**Beide Zweige sind im Bestand unausdrückbar.** `_Author.claim()` hat keinen `t_exp`-Parameter,
und das Verfassungsschema hat kein Feld für eine Maximallaufzeit. Schwerer wiegt: **niemand
liest die Pflicht.** `§3.1` sagt ausdrücklich, fehlendes `t_exp` binde unbegrenzt; es fällt kein
Vermerk, nichts wird abgelehnt. Der Satz hat zwei Layer überdauert, weil seine einzige Wirkung
darin bestand, dass ein wohlerzogener Autor etwas hinschreibt.

**Beschluss:**

- Vermerk `TrustFinding.VOUCH_WITHOUT_TEXP`, Subjekt die `claim_id` des Vouch, wenn ein Vouch
  in einem Scope mit Budgetregel kein `t_exp` trägt.
- **Ohne Wirkung.** Der Vouch bleibt im Budget-Set und bindet weiter unbegrenzt. Ihn
  auszuschließen gäbe Budget frei, und `§3.1` schließt das aus: kein Akt außer der Uhr gibt
  Budget frei. Diagnose verschieden, Wirkung gleich — D94.
- `claim()` bekommt `t_exp`, `vouch()` reicht durch, der Beispielnukleus setzt eine Laufzeit.

**Warum kein Verfassungsfeld.** Der zweite Zweig aus `§6.2` verlangte ein neues Feld, damit einen
neuen `constitution_hash`, ein neues `N` und die Neuberechnung von `00 §3.1`. Kosten am gesamten
Bestand für einen Knopf, den kein Nukleus bisher braucht. Der Zweig bleibt möglich und bekommt
einen eigenen Durchgang, falls er je gebraucht wird.

**Kein Ankerbruch.** Geprüft: keine Ankerdatei fixiert eine Vouch-`claim_id`. `02` und `02b`
führen keine, `03` und `04` nennen `claim_id` nur in strukturellen Invarianten, `example-nucleus.md`
gar nicht. Die Zahlen der Trust-Schicht hängen an `n`, `D`, `C₀`, `γ` und der Graphform. Ein
`t_exp > now` lässt Aktiv-Set und Budget-Set unverändert. Es ändern sich die `claim_id` der
Vouches und das `h_prev` ihrer Kettennachfolger — beides nirgends festgeschrieben.

**Nebenertrag.** Derselbe Parameter macht den Grenzwertvektor `now = t_exp` in Layer 01 baubar.
Die Vektorlücke folgte aus einer Erzeugerlücke: nicht geprüft werden kann, was nicht erzeugt
werden kann.

**Konsequenz — Leserprüfung.** Trägt ein normativer Satz eine Pflicht an den **Autor** von
Claims, wird bei seiner Formulierung benannt, welche Funktion die Erfüllung liest. Gibt es keine,
ist der Satz entweder auf SOLL zurückzunehmen oder mit einem Vermerk zu versehen. Die
Feldinventur (D114) fragt nach dem Leser eines Feldes; diese Regel fragt nach dem Leser einer
Pflicht.

**Nachzug: Reichweite.** Die erste Fassung dieses Eintrags nannte als Erzeuger nur
`tools/example_nucleus.py`. Es sind **drei**, und alle drei bauen Vouches ohne `t_exp`:

1. `tools/example_nucleus.py`
2. die Fixtures unter `tests/`, die die Golden Anchors materialisieren
3. `tools/sim/scenarios/`

Sobald der Vermerk existiert, feuert er in allen dreien. Die Reparatur an einer Stelle wäre die
sechste Wiederholung der Kette D105 bis D112 gewesen: richtig und nicht auf die Geschwister der
eigenen Art durchgezogen.

**Beschluss:** alle drei Stellen setzen `t_exp` weit jenseits ihres jeweiligen `now`, nie gleich
`now` — der Grenzwert ist einem eigenen Vektor vorbehalten. Damit feuert der Vermerk in keiner
bestehenden Prüfung, alle dokumentierten Finding-Mengen der Ankerdateien bleiben unverändert, und
der Vermerk wird durch **neue** Tests belegt statt durch veränderte alte.

**Verworfen:** die Fixtures unangetastet lassen und die Finding-Listen der Ankerdateien um einen
universellen Zusatz erweitern. Das schriebe in jede Ankerzeile einen Vermerk, der über den Anker
nichts aussagt.

**Kein Feld in `TrustParams`.** „Scopes mit Budgetregel" aus `02 §6.2` hat im Code keine
Entsprechung: `derive()` prüft `Σ n_budget > D` unbedingt, und nichts löst `TrustParams` aus einer
Verfassung auf. Ein Feld dafür hätte weder Schreiber noch Leser — D114. Die Einschränkung des
Satzes ist damit heute gegenstandslos, und der Vermerk gilt für jeden Vouch ohne `t_exp`.

**Ort des Vermerks:** `build_groups`, nach `_decode_weight` und nur für Vouches, die einen
Budget-Beitrag tragen. Ein Vouch mit defektem `v` trägt nach `02 §3.1` keinen Beitrag, bindet
also nichts unbefristet; für ihn zu vermerken wäre Rauschen über ein Nichtproblem.

**Erlaubte Abweichung.** `build_groups` bricht den Gleichstand über `sorted(...)` der `claim_id`.
Ein zusätzliches `t_exp` ändert alle `claim_id` der Vouches, daher kann die gewählte
`kante_claim_id` bei zwei aktiven Vouches derselben Gruppe mit gleichem `n` umspringen. `n_kante`,
jede Kapazität und jeder Fluss bleiben unverändert. Eine Abweichung dort ist **kein** Fehler.

### D120 — Absturzordnung, und die Monotonie ist eine Beobachtereigenschaft

`_Author.claim()` rückt die Spitze bei der Konstruktion vor, unabhängig davon, ob der Claim je
gespeichert oder ausgesandt wird. In einem Prozess harmlos, für ein dauerhaftes Werkzeug nicht.

| Ordnung | Absturz dazwischen | Folge |
|---|---|---|
| signieren, dann persistieren | Spitze veraltet | nächster Claim auf dasselbe `h_prev` ⇒ Equivocation, beweisbar, dauerhaft |
| Spitze festschreiben, dann signieren | Spitze zeigt auf einen nie ausgesandten Claim | alle Nachfolger bleiben bei jedem Beobachter `pending`, unheilbar |
| Core festschreiben, signieren, aussenden, Spitze festschreiben | Core liegt vor | Wiederaufnahme erzeugt denselben Claim |

Die dritte trägt, weil Ed25519 deterministisch signiert (RFC 8032): aus denselben Core-Bytes
entsteht dieselbe Signatur, also derselbe Claim, byteweise. Die Wiederaufnahme ist **idempotent**
und nicht bloß möglich. Das ist der Unterschied zwischen einer Rettung und einer Gabelung.

**Beschluss:** Core-Redo-Eintrag festschreiben, signieren, aussenden, Spitze festschreiben. Beim
Start wird ein offener Redo-Eintrag **fortgesetzt**, nie neu gebaut. Die Zustandsmaschine der
Spitze hat fünf Ausgänge:

1. leer ⇒ Genesis, `h_prev = id_genesis_anchor(I)`
2. gesetzt, Claim im eigenen Store ⇒ Normalfall
3. gesetzt, Redo-Eintrag offen ⇒ fortsetzen
4. gesetzt, Store kennt sie nicht ⇒ **anhalten**
5. zwei eigene Claims auf dieselbe Spitze ⇒ selbst equivociert, **anhalten**

Drei davon halten an. Anhalten und nicht warnen: Weiterschreiben ist in beiden Fällen genau der
Fehler, den die Prüfung erkannt hat.

**Der allgemeine Satz.** Die Monotonie aus `08 §2.2` und `02 §7` — fehlendes Wissen senkt ein
Ergebnis nur — ist eine **Beobachtereigenschaft**. Für den Autor über seine eigene Kette gilt sie
nicht: fehlt ihm sein letzter Claim, senkt das nichts, es erzeugt einen Fork gegen ihn selbst.
Das ist die dritte gefährliche Richtung neben den beiden aus `02 §7`, und sie ist die einzige,
in der der Schaden beim Wissenden selbst entsteht.

**Wiederherstellung ist Migration, nicht Vervielfältigung.** Ein Sicherungsblob trägt Seed **und**
Spitze. Wer ihn zweimal einspielt, läuft in Ausgang 5. Ein Seed allein ist keine Sicherung,
sondern die Waffe.

**Verworfen: die Spitze aus dem Netz rekonstruieren.** Aus fremden Stores lässt sich der letzte
bekannte Claim eines Autors lesen, aber nicht, dass es der letzte ist. Teilwissen wählt eine zu
frühe Spitze — und das ist exakt der Fork, den die Rekonstruktion verhindern sollte.

### D121 — Einlesepfad: ein Ausgang statt vier, und ein unsigniertes Bündel

`claim_from_bytes` dekodiert und baut direkt. Für fremde Bytes wirft es `KeyError`, `IndexError`,
`TypeError` oder `ValueError` und prüft keine Kanonizität. Es ist damit kein Einlesepfad: wer
Empfangenes darüber liest, umgeht die elf Reject-Codes aus `01 Anhang B`.

**Beschluss:**

- Fremde Bytes gehen durch eine Funktion, die **nie wirft** und entweder einen Claim oder einen
  Reject-Code liefert. Die Kanonizitätsprüfung liegt im selben `try` wie das Dekodieren (D83).
- Die Abgrenzung zu D92: dessen `ValueError` gilt für ein vom **Programmierer** fehlzugeordnetes
  Objekt. Fremde Bytes sind eine Lage der Welt und folgen der D95-Bewegung — der defekte Teil
  fällt weg, der Vermerk bleibt.
- Ein Bündel ist ein **unsigniertes** CBOR-Array aus Claim-Bytes plus eine Map
  `object-hash → Objektbytes`. Keine Ordnungsgarantie, Duplikate harmlos, Import idempotent.
  Jedes Element wird einzeln geprüft; dem Container wird nie geglaubt.

**Warum unsigniert.** Nach `08 §3` senkt ein Container keine Feststellungskosten — jeder Claim
ist nach A1 selbstenthalten und trägt seine Signatur schon. Ein signiertes Bündel wäre eine
Aussage über eine **Menge**, also Bedeutung, und ein zweites Ding, das verifiziert werden müsste.
Werkzeugkonvention, kein Transport-Profil.

### D122 — Bauform gegen Feldverlust, und der Modulschnitt der Autorschaft

Weil `Claim` frozen ist, baut `_Author.claim()` zweimal und zählt acht Felder von Hand auf.
`t_exp` ist der Beweis, dass die Aufzählung unvollständig sein kann, ohne dass es auffällt: es
steht in der Kopie und ist trotzdem tot.

Die Fehlerform ist das Gefährliche. Ein vergessenes Feld erzeugt keinen defekten Claim, sondern
einen **in sich stimmigen und gültigen** mit anderem `claim_id` und korrekter Signatur über genau
das, was dasteht. Kein Verifizierer findet das. Der Autor hat etwas anderes gesagt, als er sagen
wollte, und nichts zeigt es an.

**Beschluss:** `dataclasses.replace(unsigned, sigma=...)`, normativ für alles, was Claims erzeugt.
Der zugehörige Test iteriert über `Claim.__dataclass_fields__` und nicht über eine Liste im Test
— sonst trägt die Prüfung dieselbe Schwäche wie die Sache, die sie prüft.

**Modulschnitt.** `_Author` verschmilzt drei Dinge; nur eines ist protokollbestimmt.

| Teil | Ort | Grund |
|---|---|---|
| Bau und Signatur | Paket | `core_bytes`, `DOM_SIG`, Feldsatz sind `01`; zwei Kodierwege driften |
| Kettenspitze | Werkzeug, mit Persistenz | braucht Dauerhaftigkeit und die Zustandsmaschine aus D120 |
| Schlüsselverwahrung | Werkzeug | Betriebsfrage, nach `08 §3` nicht Protokoll |

**Oberflächenregel.** Keine Operation gibt den Schlüssel oder die Spitze heraus. Es gibt genau
eine: gib mir einen signierten Claim zu diesem Inhalt. Überquert der Schlüssel die Grenze nie,
ist ein späterer entfernter Aufruf (D123) eine Transportfrage und kein Umbau.

### D123 — Ein Schreiber, ein Ort; Geräte sind Endpunkte

**Nicht der Claim lebt an einem Ort, die Schreibautorität.** Claims sind selbstenthalten und
müssen überall hinreisen (A1) — Kollision entsteht durch Verbreitung. Singulär sind Schlüssel und
Spitze. Speicher ist repliziert, Autorschaft ist es nie.

**Der Ort ist der Sequenzer.** `h_prev` ordnet, und zwei gleichzeitige Schreiber verlangten eine
Einigung darüber, wer die Spitze fortschreibt — Konsens, unabhängig davon, wie klein die Menge
ist. Auch FROST löst das nicht: ein Gruppenschlüssel gibt eine Identität und eine Kette, aber er
**ordnet nichts**; zwei Signiersitzungen können dieselbe Spitze greifen. FROST löst Verlust und
Diebstahl, nicht Nebenläufigkeit.

**Geräte signieren die Anfrage, nicht den Claim.** Ein Gerät hält ein eigenes Schlüsselpaar und
autorisiert damit eine Anfrage; der Ort signiert den Claim. Die Gerätesignatur betritt das
Protokoll **nie** — kein Atom-Feld, keine zweite Kette, keine zweite Identität im Trust-Graph.
Nach außen eine Identität, nach innen eine kleine Hierarchie, die niemanden angeht. Das ist die
Stelle, an der Matrix' Cross-Signing passt: unterhalb des Protokolls, nicht darüber. Oberhalb
löste es das falsche Problem — es beantwortet „gehört dieses Gerät zu Alice", während `08 §2.1`
„hat Alice anderswo etwas anderes gesagt" beantwortet, und parallele Geräteketten machen
Equivocation zu einer freien Handlung.

**Schlüsselträger ist nicht Schreiber.** Ein Secure Element oder NFC-Träger darf den Schlüssel
halten, solange die Spitze am selben Ort geführt wird. Wandert der Träger ohne die Spitze zu
einem zweiten Ort, gibt es zwei Schreiber. Als reines Transportmittel ist NFC ohnehin gedeckt.

**Getragene Grenze: Autorschaft ist erreichbarkeitsabhängig, Lesen nicht.** Wer seinen Ort nicht
erreicht, kann nicht bürgen, nicht abstimmen, keine Obligation eingehen. Verifikation bleibt
offline vollständig. Die Milderung für längere Trennung ist **Migration** der Kette (D62), nicht
Delegation. Der Alltagsfall trägt sich selbst über die selektive Stille aus `01 §7`: was keinen
Claim erzeugt, braucht keinen Ort — und die Akte, die einen erzeugen, sind die, die warten können.

**Der Trust-Score offline ist über-vertrauend.** Ein alter Store hat weder den fehlenden Widerruf
(`02 §7`) noch den fehlenden über-zeichnenden Vouch (D118); beide zeigen nach oben. Als Gate für
Hochrisiko ist er damit ungeeignet — dieselbe Linie, die `02 §5` zwischen Relaxation und harter
Sicht zieht. D119 mildert es: abgelaufene Vouches fallen gegen die lokale Uhr weg, auch ohne Netz.

**Zur Reihenfolge:** D62 (`00a-rotate-key`, `resolve_current_key`) wird damit zur Voraussetzung
des ersten echten Nukleus und nicht zur Nacharbeit. Ein zweiter Ort ist eine Rotation, und der
Fall tritt beim ersten Gerätewechsel ein.

> **Nachgezogen durch D124.** Der letzte Satz trägt nicht. `00 §6` regelt ausschließlich die
> Nukleus-Autorität; für einen Menschen gibt es keine Rotation, die die Identität erhält. Der
> Gerätewechsel ist **Migration von Seed und Spitze** und damit D120s Fall — dieselbe Aussage, die
> D120 unter „Wiederherstellung ist Migration, nicht Vervielfältigung" bereits trifft. `00a` bleibt
> fällig, aber nicht aus diesem Grund und nicht zu diesem Zeitpunkt.

---

## AI. Rotation: was sie erhält und was sie kostet

Ausgelöst durch die Frage, was Schritt 1 der Anwendungssitzung (`00a-rotate-key`) eigentlich
lösen soll. Die Antwort war, dass er zwei verschiedene Dinge löst und das dringendere davon
nirgends spezifiziert ist. Vorgeschaltet: eine Literaturprüfung, weil das Problem außerhalb von
MaR seit einem Jahrzehnt bearbeitet wird.

### D124 — Persönliche Rotation ist nicht identitätserhaltend

**Die Frage.** Alice wechselt den Schlüssel. Bleibt sie dieselbe Identity?

**Der Befund.** `00 §6` regelt ausschließlich die **Nukleus**-Autorität. Kettenanker ist
`genesis.root_keys`, `I` ist der aktuell autorisierte Nukleusschlüssel, `N` der Scope. Ein Mensch
hat kein Genesis-Objekt, also ist `R_1 ist gültig ⟺ R_1.I ∈ genesis.root_keys` für ihn nicht
auswertbar. D123s Satz „die Milderung für längere Trennung ist Migration der Kette (D62)" hat beim
Transfer vom Nukleus auf die Person seinen Anker verloren — Begründungsprüfung, dieselbe Klasse
wie D77, D83, D87, D91.

**Beschluss: nein.** Ein neuer Schlüssel ist eine neue Identity. Der alte Schlüssel darf als
letzten Akt seiner Kette einen Nachfolger benennen; diese Aussage ist ein gewöhnlicher Claim,
bedeutungsblind wie jeder andere. `02` folgt ihr **nicht**, `03` kennt sie nicht. Trust wird durch
Neu-Bürgen wiederhergestellt.

**Begründung.** Identitätserhaltende Rotation verlangt, dass zwei Leser nicht verschiedene
Rotationsgeschichten sehen. Das ist Nichtequivokation über eine gemeinsame Historie, also ein
globales Log. **Es ist D123, auf den Leser angewandt:** dort verlangten zwei gleichzeitige
Schreiber eine Einigung darüber, wer die Spitze fortschreibt; hier verlangen zwei konkurrierende
Rotationen eine Einigung darüber, welche gilt. Derselbe Satz, andere Seite.

**Belege aus der Literatur.** Jedes System, das die Identität über die Rotation rettet, bezahlt
mit globaler Ordnung:

| System | Bauform | Preis |
|---|---|---|
| did:plc (AT Protocol) | Genesis-Objekt, dessen Hash der Identifikator ist; Operationen per Hash verkettet | zentrales Verzeichnis, Streit über ein 72-Stunden-Fenster gelöst |
| Keybase | Sigchain je Konto, Vorgängerhash, alte Links bleiben nach Widerruf gültig | öffentlicher Merkle-Baum plus Verankerung in einer Fremdkette gegen Rollback |
| CONIKS / Key Transparency | signierte, verkettete Verzeichnis-Snapshots | Auditoren oder Gossip; rückwirkend, schützt den isolierten Leser nicht |
| Nostr | Pubkey **ist** Identität, kein Verzeichnis — MaRs Randbedingungen | NIP-41 nennt sich selbst bestmöglich und nicht garantiert; Rückdatierung offen; Fenster zählen ab dem lokalen Sehen |
| Secure Scuttlebutt | ein Feed je Gerät, weil zwei Schreiber einen Feed nicht teilen können | Fusion IDs verbinden Feeds **oberhalb** des Protokolls |

Die erste Spalte von did:plc ist bemerkenswert: es ist strukturell MaRs Nukleus. Das zeigt, dass
die Bauform nicht das Problem ist — die Zustellgarantie ist es. Und SSB ist unabhängig auf D123
gekommen und hat es außerhalb des Feed-Begriffs beantwortet.

**Verworfen — Auflösung bei jedem `I` und `J`** (did:plc-Form für Personen: `I` wäre ein
Genesis-Hash statt eines Pubkeys). Knüpft Offline-Prüfung an eine Nachschlage-Vorbedingung —
wörtlich das Argument, mit dem `01 §2` den 16-Byte-Truncation-Hash verworfen hat. Ändert außerdem
die Feldsemantik von Layer 01: Protokollversion 2, kein Layer.

**Verworfen — Widerspruchsfenster** (Nostr NIP-41). Zählt ab dem lokalen Sehen und nicht ab dem
Zeitstempel, weil ohne Ordnung nichts anderes möglich ist. MaR hat über `h_prev` eine Ordnung **je
Autor**, aber keine zwischen Autoren; ein Fenster wäre eine Wall-Clock-Regel gegen `01 §5.3`.

**Einordnung nach `08 §3`.** Die Nachfolgeaussage senkt keine Kosten — sie ist bereits
feststellbar, weil signiert und verkettet — und verteilt keine Macht. **Werkzeug.** Kein Layer,
keine Golden Anchors, keine Zahl im Dateinamen. Das ist die dritte Spalte, dieselbe wie beim
Wallet in D122.

**Getragene Grenze.** Wer den Schlüssel verliert, verliert seinen Trust-Score und baut ihn sozial
neu auf. Das ist der Preis für „alles lokal, nie global" und wird bewusst getragen. Sollte eine
spätere Fassung ihn senken wollen, ist die Stelle benannt: sie braucht eine Zustellgarantie, die
`01` heute ausdrücklich nicht gibt.

**Nicht betroffen: der Gerätewechsel.** Er ist Migration von Seed und Spitze an einen anderen Ort
(D120), keine Rotation. Ein Schreiber, eine Kette, keine neue Identity, kein
Protokollmechanismus. Rotation braucht es nur bei Kompromittierung oder Verlust.

### D125 — Rotation gilt erst mit Gegenzeichnung des Nachfolgers

**Geltung.** Die Nukleus-Rotation nach `00 §6.1` — nach D124 die einzige, die es gibt.

**Bisher genügt eine Signatur von `K_{n-1}`.** Das lässt drei Fälle offen: die einseitige
Einsetzung eines Dritten, den Rotate auf einen Schlüssel, dessen Halter nichts davon weiß, und
den zweiten Rotate an anderer Stelle derselben Kette.

**Beschluss.** Eine Rotation ist **vollständig**, wenn `K_n` sie gegenzeichnet — ein Claim in
`K_n`s eigener Kette, der die `claim_id` des Rotate-Claims nennt. Eine unvollständige Rotation ist
wirkungslos: kein Zustand, kein eigener Vermerk, sie zählt nicht. Der **erste vollständige** Rotate
bindet.

**Begründung.** TUF verlangt für neue Root-Metadaten einen Schwellenwert an Signaturen aus dem
**alten und dem neuen** Schlüsselsatz. Dieselbe Form, mit Schwelle eins. Sie kommt ohne Uhr und
ohne globale Ordnung aus: beide Signaturen sind selbstenthalten, das Paar reist zusammen. Sie
erledigt außerdem drei offene Forks auf einmal und erzeugt damit **weniger** Spec als ihre
Alternative.

**Verworfen — letzter gewinnt.** Ein Altschlüssel bliebe dauerhaft mächtig; ein Diebstahl wäre
nie ausheilbar.

**Verworfen — einseitig mit Widerspruchsfenster.** Uhr, wie in D124.

**`00 §6.3` bleibt unberührt.** Signiert `K_{n-1}` zwei Nachfolger auf dieselbe `h_prev`, ist das
Equivocation und bleibt es, auch wenn beide gegenzeichnen. Auflösung weiterhin über §6.2.

**`00 §6.2` bleibt unberührt.** Ist `K_{n-1}` verloren, kann niemand gegenzeichnen — dafür ist der
Governance-Pfad da.

**Parallelenprüfung.** Die Regel steht auch in `00 §6.5`: im FROST-Pfad zeichnet der **neue**
Gruppenschlüssel gegen. Ohne diesen Satz nähme `key_mode = 1` sich still aus.

**Getragene Grenze.** Ein Rotate auf einen Schlüssel, dessen Halter nicht mitwirkt, wirkt nicht.
Das ist die Absicht.

**Offen bis `00a`.** Das Prädikat der Gegenzeichnung ist benannt, nicht kodiert. Kein Testvektor
bis dahin.

### D126 — `key_mode` unterscheidet die Signaturform, nicht die Kardinalität

**Widerspruch auf `main`, innerhalb von vier Zeilen.** `00 §7` schreibt die Regel als
`akt.I ∈ resolve_current_key(akt.N)` — Mengenzugehörigkeit, für jede Mächtigkeit definiert — und
setzt darunter „für `key_mode = 0`: genau ein Schlüssel". Der Beispiel-Nukleus aus `00 §3.1` führt
`root_keys = [BRUNO, ANNA]` bei `key_mode = 0` und folgt damit der Formel, nicht der Prosa. Der
Fall ist keine Randlage, sondern der Zustand unmittelbar nach der Gründung.

**Beschluss: die Formel gilt, der Satz fällt.** `key_mode` wählt zwischen gewöhnlicher
Ed25519-Signatur und FROST-Gruppensignatur; in beiden Fällen trägt der Akt genau **eine**
Signatur. Bei mehreren autorisierten Schlüsseln genügt einer.

**Bestätigt durch die Literatur.** Weder TUF noch did:plc verwechseln Signaturform mit
Kardinalität: beide führen **mehrere** Schlüssel je Rolle, TUF mit einer Schwelle, did:plc mit
einer nach Autorität sortierten Liste.

**Nicht entschieden: die Schwelle.** Ob ein Nukleus statt „einer genügt" ein `k`-von-`n` verlangen
können soll, bleibt offen. Es wäre ein Verfassungsknopf nach `00 §4`, kein Protokolldefault, und
es ist der Punkt, an dem `root_keys` von einer Liste zu einer Rolle würde.

**Zur Fehlerform.** Zwei Durchgänge über `00` haben den Widerspruch nicht gesehen, weil Formel und
Prosa je für sich richtig aussehen und erst am gerechneten Beispiel auseinanderlaufen — dieselbe
Fehlerform wie D116, dort über einen Epochenwechsel, hier über eine Mächtigkeit größer eins.

### D127 — Der Rückhalt, nicht die Kette

D120 legt die Absturzordnung fest, sagt aber nicht, wo sie im Code sitzt. Die Frage stellte sich
beim Zählen: **die Kettenfortführung existiert dreimal.**

| Ort | Bestand |
|---|---|
| `tools/example_nucleus.py` | `_Author.claim`, `_h_prev = id_genesis_anchor(pub)` |
| `tests/helpers.py` | `Identity._append`, dieselben acht Argumente an `build_signed`, gleiche Zuweisung |
| `tools/sim/welt.py` | `Teilnehmer.claim_signieren`, `h_prev` als Hexdatei |

D122 hat **Bau und Signatur** ins Paket gezogen — `build_signed` — und die **Fortführung** an allen
drei Stellen gelassen. Die Oberflächen sind bereits auseinander: `helpers.py` trägt vier Helfer,
`_Author` einen. Und `welt.py` trägt D120s Defekt wörtlich: signieren, einlegen, Spitze schreiben,
ohne Redo, ohne `fsync`, ohne atomaren Rename. Harmlos nur, weil `Welt.anlegen` bei jedem Lauf
`rmtree` ruft.

**Beschluss 1 — die Naht liegt unter der Kettenfortführung.** Eine Fortführung, zwei Rückhalte
(Speicher, Dateien), ein Testsatz über beide. Der Rückhalt kennt fünf Operationen ohne
Protokollsemantik: Spitze lesen, Spitze schreiben, Redo lesen, Redo schreiben, Redo schließen. Er
rechnet **nie** `h_prev`.

Damit ist der Einwand aus `03-prompt` — „zwei Implementierungen von Kettenfortführung und Signatur
driften" — erfüllt statt umgangen: was doppelt ist, kann über `h_prev` nicht uneins werden, weil es
`h_prev` nicht kennt. Die Literatur gibt dazu die schärfere Fassung: ein Test-Double hält sich
nicht notwendig an den Vertrag der Sache, die es ersetzt, und veraltet unbemerkt, wenn die echte
Implementierung sich ändert. Die dort gezogene Konsequenz ist nicht Verzicht, sondern **ein
Testsatz über beide** — und Treue wird am Vertrag gemessen, nicht an der Implementierung.

**Beschluss 2 — der Redo-Eintrag trägt die signierten Claim-Bytes.** Abweichung vom Wortlaut
„Core-Redo-Eintrag" in D120, mit Begründung: die Signatur ist eine deterministische reine Funktion
der Core-Bytes (RFC 8032), und bei atomarem Schreiben ist „Core schreiben, dann signieren"
genauso sicher wie „signieren, dann Bytes schreiben" — die Absturzordnung, um die es D120 geht,
betrifft die **Spitze**. Der Gewinn: die Wiederaufnahme benutzt `claim_from_bytes` und braucht
**keinen zweiten Dekodierweg für Core-Bytes**, den es heute nicht gibt. Einen zweiten Kodierweg zu
vermeiden war der Zweck von D122; ihn beim Wiederanlauf einzuführen wäre derselbe Fehler mit
umgekehrtem Vorzeichen. Nebenertrag: `t` bleibt beim Fortsetzen zwingend unverändert, weil es aus
den Bytes kommt und nicht neu gesetzt werden **kann** — die Idempotenz hängt daran, und eine
Eigenschaft, die nicht verletzt werden kann, braucht keinen Test, der sie prüft.

**Beschluss 3 — Redo vor Spitze.** Die Prüfreihenfolge ist normativ. D120 zählt fünf Ausgänge auf;
der Zustand hat aber drei unabhängige Bits (Spitze gesetzt, Redo offen, Claim der Spitze bekannt),
und die Lage „Spitze leer, Redo offen" fehlt. Prüfte man die Spitze zuerst, führe sie in Ausgang 1
und baute einen **zweiten Genesis-Claim** mit neuem `t` — Selbst-Equivocation, genau der Fehler,
den D120 verhindern soll. Die Reihenfolge beseitigt die Lage, statt einen sechsten Ausgang zu
brauchen.

**Beschluss 4 — `claim_id` ist die Hochwassermarke.** D120 ist strukturell ein Redo-only-Log mit
idempotenter Wiederholung, also ARIES' „Repeating History". ARIES erkauft die Idempotenz über den
Vergleich der `pageLSN` mit der LSN des Log-Eintrags: ein zusätzliches Feld, eine zusätzliche
Invariante. MaR bekommt sie geschenkt, weil der Claim inhaltsadressiert ist — die Wiederaufnahme
fragt den Store, ob er die rekonstruierte `claim_id` kennt. **Kein „erledigt"-Flag, kein
zusätzlicher Zustand.** Daraus folgt, dass Ausgang 3 keine Fallunterscheidung braucht, wo der
Absturz lag: die Folge ab „aussenden" ist durchgehend idempotent, und die Wiederaufnahme ist
schlicht ihre Fortsetzung von vorn.

**Der Fork-Schalter.** `welt.py` trägt `kette_fortschreiben: bool = True`, damit die Simulation
absichtlich equivozieren kann. Die Fähigkeit bleibt nötig, das Flag nicht: der gefährlichste
Zustand der Kette darf kein Default-Argument an der gewöhnlichen Operation sein. Er wird eine
eigene, anders benannte Operation, und sie entsteht mit dem Umzug von `welt.py`, nicht vorher.

**Vertagt: Ausgang 5** (zwei eigene Claims auf dieselbe Spitze). Er ist keine Eigenschaft des
Spitzenzustands, sondern eine Abfrage über den Store, und die dafür nötige Schnittstelle
(`index.py`) ist ungeprüft. Schwerer wiegt: ein doppelt eingespielter Sicherungsblob erzeugt den
Fork in **zwei getrennten Stores**, von denen keiner beide Zweige sieht. Der Ausgang ist damit
durch eine Startprüfung gar nicht erreichbar, sondern erst bei der Vereinigung — was ihn zu einer
Frage an den Einlesepfad (D121) macht und nicht an die Spitze.

**Getragene Grenze: die Persistenzeigenschaften.** Der Datei-Rückhalt setzt drei Eigenschaften
voraus — atomares `os.replace`, `fsync` der Datei vor dem Rename, `fsync` des Verzeichnisses
danach. Sie werden im Modul benannt und sind **nicht geprüft**. Die Literatur ist an dieser Stelle
unangenehm eindeutig: ALICE (OSDI '14) fand 60 Crash-Vulnerabilities in elf ausgereiften
Anwendungen — darunter Git, SQLite, PostgreSQL, ZooKeeper —, weil die Persistenzeigenschaften
zwischen sechs verbreiteten Linux-Dateisystemen weit auseinandergehen; insbesondere garantiert ein
`fsync` auf eine Datei nicht, dass ihr Verzeichniseintrag persistiert ist, und ext3 im
Ordered-Mode persistiert in Reihenfolge und erzeugt damit eine falsche Sicherheit. Ohne
ALICE-Klasse-Werkzeug ist die Annahme argumentierbar, nicht prüfbar. Sie wird benannt statt
behauptet.

**Was dagegen prüfbar ist: die Zustandsmaschine.** Die Absturzpunkte liegen in der **Reihenfolge
der Operationen**, nicht im Rückhalt. Ein Rückhalt, der beim k-ten Schreibvorgang wirft,
aufgezählt über alle k, prüft sie erschöpfend — im Speicher, deterministisch, ohne Dateisystem.
`signieren` schreibt viermal (Redo, Aussenden, Spitze, Redo-Schluss), also fünf Läufe je Vektor
einschließlich des ungestörten. Der ungestörte Lauf ist die Referenz für alle anderen: **zwei
Läufe, eine Variable**, und deshalb braucht dieser Lauf **keinen neuen Golden Anchor**.

**Schnitt.** Zwei Läufe. Der erste baut `tools/autor.py` und rührt nichts an; der zweite zieht die
drei Stellen um und prüft gegen „426 grün, alle Anker byteweise unverändert". Neubau und Umzug
gemischt hieße, am Ende nicht zu wissen, welche der beiden Änderungen einen Anker bewegt hat.

### D128 — Der Halt ist eine Ableitung, und eine abgefangene Ausnahme ist ein Absturz mit Zeugen

Zwei Befunde aus der Abnahme des Autorlaufs, die dieselbe Wurzel haben: D120 beschreibt den
**Absturz**, und ein Absturz ist der einzige Fall, in dem das schreibende Objekt danach nicht mehr
existiert.

**Beschluss 1 — der Halt klebt am Objekt, nicht am Rückhalt.** `wiederaufnehmen` leitet den
Zustand bei jedem Aufruf aus Rückhalt und Ausgang neu ab; ein Halt aus Ausgang 4 heilt, sobald der
fehlende Claim nachgeliefert ist. Begründung: Ausgang 4 sagt „der Ausgang kennt die Spitze nicht",
und das ist eine Aussage über den Ausgang und nicht über die Kette. Ein klebriger Halt verlangte
einen Eingriff, wo keiner nötig ist, und wäre eine zweite Wahrheit neben dem Rückhalt — dieselbe
Linie wie D61: keine abgeleitete Größe wird zusätzlich gespeichert.

Der fremde Redo bleibt dagegen angehalten, solange er offen ist. Das ist keine Ausnahme von der
Regel, sondern dieselbe Ableitung über eine Lage, die sich nicht von selbst ändert. Der Prompt
hatte „nach `ANGEHALTEN` bleibt jeder weitere Aufruf `ANGEHALTEN`" verlangt; das war zu grob und
wird hier zurückgenommen.

**Beschluss 2 — innerhalb eines Objekts klebt der Halt sehr wohl.** Bricht in `signieren` ein
Schreibvorgang mit einer Ausnahme ab und **fängt der Aufrufer sie**, ist der Zustand des Objekts
derselbe wie nach einem Absturz — nur läuft der Prozess weiter. Ohne Halt baut der nächste Aufruf
einen zweiten Claim auf dasselbe `h_prev`: Selbst-Equivocation, beweisbar und dauerhaft, also
genau der Fehler, gegen den das Modul existiert.

Das ist keine Randlage. `DateiRueckhalt` wirft `OSError` bei vollem Datenträger, bei `EACCES`, bei
einer schreibgeschützt neu eingehängten Partition. Das sind Lagen der Welt, und ein Prozess, der
sie behandeln will, ist danach in einem Zustand, den D120 als „anhalten" führt.

**Beschluss 3 — der Halt gilt einheitlich für alle vier Schreibvorgänge**, auch für den letzten.
Bricht `redo_schliessen` ab, ist die Lage sachlich unbedenklich: der Claim ist ausgesandt, die
Spitze steht. Der Halt kostet dort ein `wiederaufnehmen` und nichts sonst, weil die Wiederaufnahme
idempotent ist. Eine Fallunterscheidung nach Schritt wäre teurer zu lesen als der Gewinn — und
jede Fallunterscheidung an dieser Stelle wäre eine Behauptung darüber, was der abgebrochene
Schritt bereits bewirkt hat, die das Objekt nicht prüfen kann.

**Zur Fehlerform — neue Prüfregel.** Die Absturzaufzählung konnte den Befund strukturell nicht
sehen: **jeder** ihrer Läufe baut nach dem Bruch einen frischen `Autor`. Der Injektor modellierte
den Absturz und nicht die abgefangene Ausnahme, obwohl beide durch denselben Code laufen.

> **Prüfregel 13 — Neustart als Annahme.** Modelliert ein Test einen Neustart, wird gefragt, ob
> dieselbe Ursache auch **ohne** Neustart eintreten kann. Wenn ja, ist der Weiterlauf ein eigener
> Vektor und keine Variante.

Sie ist die Umkehrung der Lehre aus dem Autorschaftslauf: dort lagen vier von vier Befunden in
Tests, hier liegt der Befund im Produktivcode und wurde durch die Frage gefunden, was der Test
**nicht** tut.

**Beschluss 4 — der Halt fängt `BaseException`, nicht `Exception`.** `KeyboardInterrupt` und
`SystemExit` erben nicht von `Exception`. In einem bedienten Werkzeug ist Strg-C während des
Signierens der wahrscheinlichste Abbruch überhaupt — wahrscheinlicher als der volle Datenträger,
mit dem Beschluss 2 begründet wurde —, und eine Schleife, die `KeyboardInterrupt` fängt und
weiterläuft, ist die übliche Bauform und keine exotische. Ohne die weite Klausel liefe genau
dieser Fall am Halt vorbei und ließe `_zustand` auf `NORMAL` stehen.

Die Klausel **schluckt nichts**: sie setzt den Zustand, räumt `_h_prev` und wirft mit nacktem
`raise` unverändert weiter. Das ist die anerkannte Ausnahme von der Regel gegen weite
`except`-Klauseln — die Regel selbst bleibt unangetastet, und für jede Klausel, die eine Ausnahme
nicht weiterreicht, gilt sie fort. Nebenbei gedeckt: `asyncio.CancelledError`, seit Python 3.8
ebenfalls `BaseException`.

**Beschluss 5 — der Halt am Objekt ist über `wiederaufnehmen` verlassbar.** Hier berühren sich
Beschluss 1 und 2: der Halt klebt am Objekt, aber die Ableitung liest den dauerhaften Zustand neu.
Dasselbe Objekt nimmt die Kette also wieder auf, ohne weggeworfen werden zu müssen — das ist der
vorgesehene Weg nach einem behandelten `OSError`. Der Satz braucht eine eigene Zusicherung, weil
ein späterer Lauf, der den Halt „richtig klebrig" machte, die Erholung bräche und dabei durch jede
bestehende Prüfung liefe.

**Abgenommen** mit `impl/autor` (`8615889`), 468 Tests. Der Weg dorthin ging über drei Läufe und
vier Befunde, von denen die letzten beiden — die Ausnahmeklasse und die Erholung — erst sichtbar
wurden, nachdem der Halt existierte. Das ist die gewöhnliche Reihenfolge: ein Mechanismus wirft
seine eigenen Fragen erst auf, wenn er da ist.

## AJ. Der absichtliche Fork

### D129 — `gabeln` fasst den dauerhaften Zustand nicht an

Die Zählung aus D127 war zu niedrig. Die Kettenfortführung existiert **fünfmal**:
`tools/example_nucleus.py`, `tests/helpers.py`, `tools/sim/welt.py` und zusätzlich
`tests/property/welten.py` (`_Signer`, Zeilen 64–91) — dazu seit dem Autorlauf `tools/autor.py`
als die einzige richtige. Zwei der vier alten erzeugen absichtlich Forks: `welt.py` über
`kette_fortschreiben` und `welten.py` über denselben Namen, gesteuert von `twin`.

D127 hatte entschieden, dass das Flag aus der Signieroberfläche verschwindet — der gefährlichste
Zustand der Kette darf kein Default-Argument sein. Die Ersatzoperation heißt **`gabeln`**.

**Beschluss: `gabeln` signiert und sendet aus, schreibt aber weder Redo noch Spitze.**

Der Punkt ist nicht offensichtlich und trägt die Entscheidung allein: Schriebe `gabeln` einen
Redo-Eintrag, machte ein späteres `wiederaufnehmen` den absichtlichen Fork zur **echten Spitze** —
der Zwilling würde zum Hauptzweig und der Hauptzweig zum Zwilling, und zwar still. Schriebe
`gabeln` die Spitze, wäre es kein Fork, sondern ein gewöhnlicher Anhang.

Es bleibt also nur, den dauerhaften Zustand gar nicht zu berühren. Das ist auch die richtige
Aussage über die Sache: ein absichtlicher Fork ist etwas, das ein Autor **neben** seine Kette
stellt, nicht etwas, das seine Kette tut. Die Wächter aus D128 gelten unverändert — `gabeln`
verlangt ein vorheriges `wiederaufnehmen` und verweigert im Zustand `ANGEHALTEN`.

**Das Szenario-Schema behält `kette_fortschreiben`.** `s5.json` führt das Feld viermal,
`szenario.py` liest es, und `sim-abnahme.md` schreibt Namen und Voreinstellung fest. Der Konflikt
mit D127 ist keiner: dort steht `false` ausdrücklich in einer Datendatei, von einem Autor, der
genau das will. Die Grenze liegt zwischen **Datei und Aufrufkonvention** — ein Szenarioautor, der
`false` schreibt, hat es getippt; ein Programmierer, der ein Argument wegläßt, hätte es nicht.
`szenario.py` verzweigt auf zwei benannte Operationen, statt ein Bool durchzureichen.

**Die vier alten Klassen bleiben als Oberflächen.** `Identity`, `_Author`, `_Signer` und
`Teilnehmer` behalten ihre Signaturen; damit ändert sich in den 26 Testdateien, die sie benutzen,
keine Zeile. Sie hören nur auf, Implementierungen zu sein. Der Zähler `_t` in `_Signer` bleibt bei
ihm: er ist eine Eigenschaft des Weltgenerators und nicht der Kette, und `t` bleibt Parameter von
`signieren`.

**Das Abnahmekriterium wird abgeleitet, nicht aufgezählt** (Lehre aus D122): nach dem Umzug findet
`grep -rn "_h_prev" tools/ tests/` nichts außerhalb von `tools/autor.py`, und keine der vier
Dateien importiert noch `build_signed` oder `id_genesis_anchor`. Eine Liste erlaubter Fundstellen
im Kriterium trüge dieselbe Schwäche wie die Sache, die sie prüft.

**Nicht mitrepariert: B-4** (die Zwillingsbuchführung in `welten()` zieht kein Budget ab). Der
Befund liegt in der Buchführung des Generators, nicht in der Kettenfortführung, und ist vom Umzug
unabhängig. Ihn mitzunehmen hieße, bei einer Ankerabweichung nicht zu wissen, welche der beiden
Änderungen sie bewegt hat.

## AK. Eine Tür pro Sprache

### D130 — Der Rundlauf ist eine Form, keine Fundstelle

D83 hat entschieden, dass `decode` und `is_canonical` im selben `try` stehen: der Rundlauf ruft
`encode` auf, und `encode` wirft bei Werten, die `decode` durchlässt. Der Beschluss wurde auf
`trust/groups.py` angewandt, von `profiles/payload.py` übernommen — und ist nie nach Layer 01
zurückgegangen. `verifier.structural_check` prüft die Kanonizität zwei Schritte nach dem
Dekodier-`try`, ungeschützt.

Die Parallelenprüfung zeigt Layer 01 als den Ausreißer unter drei gleichartigen Stellen:

```
02 groups.py:41   try: decode ; is_canonical   except Exception → UNPARSABLE_VOUCH_PAYLOAD
03 payload.py:18  try: decode ; is_canonical   except Exception → UNPARSABLE_V
01 verifier.py    try: decode                  except Exception → MalformedCbor
                  … is_canonical zwei Schritte später, ungeschützt
```

Der Vektor ist `h'a100ff'` — eine Map, deren **Wert** zu Schlüssel `0` das Break-Sentinel ist.
`decode` liefert ein `dict`, die Schlüsselprüfung 2b sieht nur Integer-Schlüssel und läßt es
durch, `is_canonical` ruft `encode` und bekommt `CBOREncodeError`. Die Ausnahme verläßt
`structural_check` als Nicht-`VerifierError`.

`h'a1ff01'` — Sentinel im **Schlüssel** — ist auf Layer 01 dagegen harmlos: Schritt 2b fängt es
vorher ab. Auf Layer 02 waren beide Vektoren gefährlich, weil `_decode_weight` keinen
Schlüsseltypfilter hat. **Ein Vektor, nicht zwei.** Die Tabelle aus D83 gilt für die dortige
Fundstelle und nicht für diese; sie ungeprüft zu übernehmen wäre derselbe Fehler noch einmal.

**Beschluss: der Rundlauf steht auf jeder Schicht im selben `try` wie das Dekodieren; was von dort
kommt, ist unlesbar.** Auf Layer 01 heißt das `MALFORMED_CBOR`.

Nicht aufgezählt wird, welche Ausnahmen `cbor2` werfen kann. Das ist eine Eigenschaft der
Bibliothek, nicht von MaR, und über die Version nicht stabil; tiefe Verschachtelung, die beim
Dekodieren durchgeht und beim Enkodieren rekursiert, wäre ein weiterer Geschwisterfall, den keine
Liste kennt. Der `try` fängt die Form, nicht die Namen.

**Kein `False` aus `is_canonical`.** Die naheliegende Vereinfachung — die Hilfsschicht fängt selbst
und meldet „nicht kanonisch" — löscht die Unterscheidung, die D83 gerade begründet hat: eine
Ablehnung als `NON_CANONICAL_ENCODING` behauptet, es gebe eine kanonische Kodierung desselben
Inhalts. Bei `h'a100ff'` gibt es die nicht. Auf Layer 01 wiegt das schwerer als auf 02, weil dort
zwei verschiedene Reject-Codes daran hängen und ein Absender in die falsche Richtung suchen würde.
`cbor_canon` bleibt dünn und wirft; die Zuordnung zum Code bleibt am Aufrufer.

**Die Reihenfolge bleibt erhalten.** „Im selben `try`" wörtlich genommen zöge die Kanonizität vor
die Schlüsseltypprüfung 2b. Der trennende Vektor ist `h'bf616100ff'` — die
indefinite-length-Kodierung von `{"a": 0}`: dekodierbar, nicht kanonisch, Schlüssel ist `str`.
Vorgezogen ergäbe er `NON_CANONICAL_ENCODING`, und das wäre falsch, denn die kanonische
Neukodierung derselben Map bliebe ein ungültiger Claim; Anhang B führt den falschen Feldtyp unter
`MALFORMED_CBOR`. Der Rundlauf bekommt also einen eigenen `try` **an seinem bisherigen Platz**,
nicht einen gemeinsamen weiter vorn. §6 Punkte 1–7 behalten ihre normative Ordnung, und D113
braucht keinen Abhängigkeitssatz.

**Warum es nicht folgenlos ist, obwohl die Entscheidung dieselbe bleibt.** `h'a100ff'` scheitert
zwei Schritte später ohnehin an der Längenprüfung von `m[1]`; falsch ist allein der Fehlerkanal.
Der trägt aber zwei Dinge: `_build_lifecycle_index`, `_find_revoking_claim` und
`_find_superseding_claim` fangen `VerifierError` und überspringen — ein `CBOREncodeError`
überspringt nicht, er reißt den Index-Aufbau ab, und ein einziger solcher Claim im Store legt
`classify_all` still. Und er ist die Ausnahme, an der D131 bräche, bevor sie geschrieben ist.

**Testpunkt an der Hilfsschicht.** `test_cbor_canon.py` hat keinen Vektor, der `is_canonical` zum
Werfen bringt. Drei Aufrufer verlassen sich darauf, dass sie es tut. Die Zusicherung gehört dorthin,
wo die Eigenschaft entsteht.

**Mitbefund: `Anhang B.2` führte indefinite-length unter `MALFORMED_CBOR`.** Der Code sagt etwas
anderes, und der Code hat recht. Eine indefinite-length-Kodierung, deren einziger Mangel die
Längenform ist, dekodiert sauber, passiert die Schlüssel- und Feldtypprüfung und scheitert erst am
Rundlauf — `NON_CANONICAL_ENCODING`. Das ist auch die richtige Aussage: es gibt eine kanonische
Kodierung desselben Inhalts, und sie ist eine andere. Genau die Bedingung, an der dieser Eintrag
die beiden Codes trennt. Unter `MALFORMED_CBOR` gehört die Längenform nur, wenn sie
**unabgeschlossen** ist, und das deckt „nicht dekodierbar" ab. B.2 verliert das Stichwort und
gewinnt „Nicht-uint-Schlüssel", das dort fehlte, obwohl §6 Punkt 2b es prüft.

Belegt durch **BV3** (`Anhang C.8`): TV1s signierte Map in indefinite-length-Form, 310 statt 309
Byte, re-serialisiert zu TV1s Bytes, `NON_CANONICAL_ENCODING`. Die drei Byte-Vektoren `BV1`–`BV3`
sind zusammen mit diesem Eintrag entstanden und normativ.

### D131 — Der Einlesepfad fängt `VerifierError`; „wirft nie" wird zugesichert, nicht gefangen

D121 verlangt eine Funktion, die nie wirft und entweder einen Claim oder einen Reject-Code liefert.
Die Frage, die der Beschluss offenließ: **was fängt sie?**

Fängt sie `Exception`, ist der Wortlaut erfüllt und die Sache verdorben. Ein Programmierfehler im
Erkenner würde dann zu `MALFORMED_CBOR` auf **jedem** Claim: das Netz sähe aus, als bestünde es aus
kaputten Bytes, der Store bliebe leer, und nichts zeigte an, dass die Ursache lokal ist. Das ist
D92 eine Ebene höher — eigene Fehler sind keine Lage der Welt.

Die Literatur hat die Grenze vor MaR gezogen. Joe Duffys Bericht über Midoris Fehlermodell
(2016) trennt **Bugs** von **behebbaren Fehlern** und behandelt sie mit verschiedenen Mitteln:
Fail-Fast für die einen, geprüfte Ausnahmen für die anderen, mit der Begründung, dass Bugs
grundsätzlich nicht behebbar sind und der Versuch, sie zu behandeln, systematisch zu unzuverlässigem
Code führt. Die Einteilung ist seither Konsens — Go, Rust, Swift und Zig sind bei ihr angekommen.

**Beschluss: der Einlesepfad fängt `VerifierError` und nichts sonst.** Alles andere schlägt durch.

**Die Totalität wird zugesichert, nicht erkauft.** Ein Eigenschaftstest über beliebige Bytes
behauptet, dass nichts anderes als ein `Claim` oder ein `ErrorCode` herauskommt. Dieselbe Bewegung
wie D75: eine Unmöglichkeit wird geprüft statt eine Semantik. Der Test ist zugleich derjenige, der
D130 heute rot machen würde.

**Verworfen: die Umkehrung.** Naheliegende Alternative wäre, `structural_check` selbst auf
Rückgabewerte umzubauen — elf `raise` werden elf `return` — und die werfende Fassung zum dünnen
Adapter zu machen. Das entspräche der Literatur besser. Der Grund dagegen ist nicht der Diff:
**auch diese Bauform macht „wirft nie" nicht strukturell.** Ein `AttributeError` im Erkenner
entkommt der Rückgabefassung genauso wie dem Wrapper. Die Totalität hängt in beiden Fällen am Test,
und dann gewinnt die Bauform, die elf Stellen mitten in Layer 01 und die daran hängenden
`pytest.raises`-Vektoren nicht anfaßt.

**Die Grenze verläuft an der Herkunft des Codes, nicht an der Breite der Klausel.**
`groups.py` und `payload.py` fangen `Exception` und bleiben richtig: in ihrem `try` steht ein
**fremder** Aufruf, dessen Ausnahmemenge weder aufzählbar noch versionsstabil ist. Im `try` des
Einlesepfads steht **eigener** Code, und dort verwandelt dieselbe Klausel Bugs in Weltlagen.
Gleiche Syntax, gegensätzliche Wirkung. Ein späterer Lauf, der D131 als „schmal fangen" liest und
auf die beiden anderen Stellen anwendet, macht sie kaputt.

### D132 — Fremde Bytes gehen an keiner Stelle durch `claim_from_bytes`

`structural_check` ist ein ordentlicher Erkenner: eine Tür, feste Reihenfolge, liefert strukturierte
Daten. Daneben steht `atom.claim_from_bytes` — dieselbe Sprache, schwächere Grammatik, keine
Kanonizitätsprüfung, keine Feldtypen, keine Signatur.

Das ist das Muster, gegen das LangSec geschrieben ist: der faktische Erkenner verteilt sich über
das Programm und deckt sich nicht mit den Annahmen der Programmierer über die Gültigkeit der Daten.
Die Gegenform heißt Recognizer Pattern — erst Erkennung, dann eine klare Grenze, jenseits derer die
Rohbytes nicht mehr erreichbar sind. Ein Wrapper um Tür eins läßt Tür zwei offen und ändert am
Muster nichts.

**Beschluss: fremde Bytes gehen an keiner Stelle durch `claim_from_bytes`.**

Der legitime Rest bleibt: `tools/autor.py` liest über diesen Weg den **eigenen** Redo, und das ist
nach D92 richtig. Die Voraussetzung wandert aus dem Kommentar in den Namen. Der Satz ist als Regel
formuliert und nicht als Liste von Aufrufstellen, weil eine Liste den nächsten Aufrufer nicht kennt
— Prüfregel 11.

Heute hat der Satz genau einen Verstoß im Produktivcode: `tools/sim/welt.py:86` in `store_laden`.
Alle übrigen Fundstellen sind Tests, die Vektor-Hex aus der Spec dekodieren, also eigene Bytes.

**Der Container wird auch im Dateinamen nicht geglaubt.** Die Inbox der Simulation adressiert über
`{cid.hex()}.cbor`, `zustellen` kopiert Bytes ohne Prüfung, und `hat_claim` beantwortet „kenne ich"
allein aus der Existenz des Dateinamens. Niemand rechnet nach, dass in `abc….cbor` ein Claim mit
`claim_id == abc…` steht. Die Inbox **ist** das unsignierte Bündel aus D121, nur als Verzeichnis;
der Satz „dem Container wird nie geglaubt" gilt für sie mit demselben Wortlaut. Der Zusammenhang
ist nicht bloß formal: `claim_id` ist der Hash über `core_bytes`, und erst die Kanonizitätsprüfung
bindet empfangene Bytes an diese Id. Ohne sie ist die Zuordnung von Name zu Inhalt eine Behauptung
des Absenders.

**Zuschnitt: zwei Läufe.** D130 und D131 sind Paketarbeit an Layer 01 — Reparatur im Bestand plus
`read_claim` daneben. D132 ist Werkzeugarbeit — Bündelformat, `store_laden` und `zustellen` über
den neuen Pfad, `claim_id` nachgerechnet. Getrennt, damit ein roter Bestandstest nicht in einer
Abnahme über neues Bündelformat untergeht.

## AL. Was der Erzeuger schuldet

### D133 — `welten()` erzeugt gültige Claims; die Vorbedingung liegt beim Aufrufer

Der Einlesepfad hat beim ersten Lauf etwas gefunden, wofür er nicht gebaut war. Die Messung aus
`impl/einlesen`: von 534 erzeugten Claims liefert `read_claim` 532 mal einen `Claim` und zweimal
`INCOHERENT_EXPIRY`. Die Lage `"vergangen"` in `tests/property/welten.py` zieht
`t_exp ∈ [1, now-1]` ohne Blick auf `t`; wo `t ≥ t_exp` herauskommt, entsteht kein abgelaufener
Claim, sondern gar keiner. Zwei Fundstellen — die Ziehung steht für den ersten Claim und für den
Zwilling.

**Warum es nie auffiel.** `classify_all` ruft `structural_check` nur für Lifecycle-Kandidaten beim
Indexaufbau, nie für den zu klassifizierenden Claim selbst. Die Eigenschaftstests klassifizieren
also Claims, die ein Empfänger zurückgewiesen hätte, ohne dass irgendwo eine Prüfung liegt, die es
merkt.

**`classify_all` trägt daran keine Schuld.** `02a §3` setzt strukturelle Gültigkeit voraus und legt
die Prüfung ausdrücklich beim Aufrufer ab; das ist der Grund, warum der schnelle Zwilling schnell
ist. Der Befund lautet nicht „`classify_all` prüft zu wenig", sondern „die Vorbedingung wird in der
Testschicht von niemandem hergestellt". Dieser Satz steht hier, damit kein späterer Lauf
`classify_all` repariert und es dabei langsamer und falscher zugleich macht.

**Beschluss: `welten()` erzeugt in der Voreinstellung ausschließlich strukturell gültige Claims.**

Die Begründung kommt aus D131 und ist erst seit ihm formulierbar: ein Store in einem
Eigenschaftstest modelliert, was ein Beobachter hält — und ein Beobachter hält seit dem
Einlesepfad genau das, wofür `read_claim` einen `Claim` geliefert hat. Ohne diese Regel sagen der
Erzeuger und der Einlesepfad Widersprüchliches über denselben Gegenstand, und jeder Lauf, der auf
beidem aufbaut, erbt den Widerspruch.

**Kein Verbot, nur eine Voreinstellung.** Ein Erzeuger, der auf Verlangen ungültige Claims baut,
ist etwas, das dem Einlesepfad noch fehlt. Der Unterschied liegt zwischen *versehentlich
ungültig* und *ungültig, wenn man es verlangt*; das erste ist der Befund, das zweite eine
Fähigkeit. Die Schalter `erlaube_ueberzeichnung` und `erlaube_equivocation` sind das Muster.

**Die Reparatur ist nicht die Schranke, sondern die Sichtbarkeit von `t`.** `_Signer.claim()` zählt
`_t` **innerhalb** der Methode hoch; der Aufrufer kennt das `t` erst, wenn der Claim signiert ist,
und kann deshalb keine Untergrenze setzen. Nach D129 bleibt der Zähler bei `_Signer` — er ist eine
Eigenschaft des Weltgenerators und nicht der Kette — und genau deshalb darf er auch gelesen werden.

Verworfen: eine feste Untergrenze wie `min_value=100`. Sie hielte nur, solange keine Welt mehr als
hundert Claims je Identität baut, und diese Schranke stünde nirgends.

**Vierte Lage `"grenze"` mit `t_exp = now`.** Die drei bestehenden Lagen decken `now ≤ t_exp`
überall ab **außer** an der Kante: `künftig` beginnt bei `now + 1`, `vergangen` endet bei
`now - 1`. Der Grenzwertvektor `now = t_exp` steht seit D119 als „baubar und ungebaut" in der
Offen-Liste — er war ungebaut, weil der Erzeuger ihn nicht ziehen konnte. Gewichtung
`4 : 4 : 1 : 1`; ein einzelner Punkt braucht keine Masse, er muss nur erreichbar sein.

**Der Schaden ist heute null, und das gehört dazu.** Ein Claim mit `t ≥ t_exp` und `t_exp < now`
landet ohnehin in `EXPIRED` — demselben Zustand wie ein sauber gebauter abgelaufener Claim — und
bindet kein Budget. Kein Fingerabdruck ändert sich, kein bestehender Anker bewegt sich. Der
Beschluss ist vorwärtsgerichtet und keine Fehlerbehebung an einem falschen Ergebnis.

### D134 — Die Budgetbuchführung des Erzeugers ist gruppenweise

`02 §3.1`: `n_budget = max n` über die Mitglieder einer Gruppe `(I, J, N)` im Budget-Set,
`Σ_J n_budget ≤ D` über die Gruppen. **Maximum innerhalb, Summe darüber.**

`welten()` führt `remaining[author] -= n` **pro Claim**. Das ist die falsche Form, und sie hat zwei
Symptome:

- **Der Zwilling.** Erster und Zwilling teilen `(I, J, N)`. Die Gruppe zahlt `max(n, n2)`, nicht
  `n + n2`. Im Regelfall `n2 = n - 1` kostet der Zwilling **nichts**; nur im Zweig
  `min(d_budget, n+1)` bei `n = 1` steigt das Maximum, und dann um eins.
- **Die Wiederholung.** Bürgt derselbe Autor in zwei Schleifendurchläufen für denselben
  Empfänger, zieht `remaining` zweimal ab, wo die Spec einmal das Maximum zählt.

**Verworfen: die wörtliche Reparatur von B-4.** „Der Zwilling zieht Budget ab wie der erste"
überzieht — sie addiert, wo die Spec maximiert, und verschärft die Unterschätzung, statt sie zu
beheben. B-4 war als eigener Befund richtig beobachtet und als Ursache falsch benannt; er geht in
diesem Eintrag auf und verschwindet aus der Offen-Liste.

**Der Zwilling gehört ins Budget-Set.** `02 §8`: ob ein geflaggter Bürge Fluss trägt, ist Policy
(`include_flagged`), die Budgetrechnung ist davon unberührt — ein Flag darf die Grundlage nicht
verschieben, auf der es erkannt wurde. „Zwilling ignorieren" ist damit ebenso ausgeschlossen wie
„Zwilling addieren".

**Die Ablaufregel erbt dieselbe Form.** `02 §3.1` gibt Budget erst frei, wenn **alle** Vouches der
Gruppe abgelaufen sind. `welten()` prüft `t_exp` je Claim. Eine Gruppe bindet also weiter, solange
ein Mitglied nicht abgelaufen ist — auch dann, wenn das nicht abgelaufene Mitglied der Zwilling
ist.

**Ein dritter Symptompfad, und er kehrt die Richtung um (Nachtrag).** Die beiden Symptome oben
teilen eine stillschweigende Annahme: dass der erste Claim einer Gruppe lebt. Trifft sie nicht zu,
bucht der Erzeuger nichts ab — richtig, denn ein abgelaufener Claim ist nicht im Budget-Set — aber
`lage2` wird unabhängig gezogen. Ist der Zwilling lebend, ist er das einzige Mitglied, das
`_in_budget_set` passiert, und die Gruppe zahlt `n2`, während der Erzeuger null gebucht hat. Über
mehrere Empfänger summiert sich das unbeschränkt: `Σ_J n_budget > D` ist bei
`erlaube_ueberzeichnung = False` erreichbar, und `derive.py` Schritt 4 setzt
`OVERCOMMITTED_AUTHOR`.

**Der Satz, den das ersetzt**, lautete: zu wenig Budget heiße zu wenige Vouches, nie eine
verletzte Invariante, `erlaube_ueberzeichnung = False` halte, was es verspreche. Er war aus der
zweigliedrigen Aufzählung darüber abgeleitet und hat deren Geltungsbereich still verloren —
dieselbe Form wie D77, D83, D87, D91, D130 und D135, und der Grund, warum Prüfregel 18 existiert.
Die Wirkung lag wieder nicht dort, wo die Zahl entsteht (Prüfregel 16): verfolgt worden war der
Zweig „der Erste lebt", nicht der andere.

**Kein falsches Grün heute, und das ist kein Trost.** Die Kombination
`erlaube_ueberzeichnung = False` mit `erlaube_equivocation = True` kommt einmal vor, in
`test_p3b_finds_equivocation_passed_to_pending`, und dessen Prädikat liest ausschließlich den
Auszählungszustand; Budget geht dort nirgends ein. Die Lücke ist heute folgenlos und wäre es ab
dem ersten Test nicht mehr, der auf dieser Kombination eine Trust-Aussage trifft. Genau der ist
der Zweck dieses Eintrags.

**Die Buchführung wird deshalb über lebende Mitglieder formuliert, nicht über den ersten Claim.**
`gruppe[(I, J)] = max n über die lebenden Mitglieder`, `verbraucht[I] = Σ_J gruppe[(I, J)]`,
Schranke `verbraucht[I] ≤ D`. Ein abgelaufenes Mitglied trägt null, gleich an welcher Stelle es
gezogen wurde. Der Preis der ersten beiden Symptome bleibt Abdeckung; der des dritten war es nie.

**Warum es trotzdem fällig ist.** Eine Eigenschaft mit `erlaube_ueberzeichnung = False` **und**
`erlaube_equivocation = True` ist heute nicht schreibbar: der Erzeuger kann nicht sagen, wie viel
Budget eine Welt mit Zwillingen verbraucht hat. Genau diese Kombination braucht jeder Test, der
Equivocation unter gültigem Budget prüfen will — und das ist die interessante Lage, weil
`include_flagged` dort seinen einzigen Sinn hat.

## AM. Ein Flag verschiebt die Grundlage nicht

### D135 — `EQUIVOCATION_FLAGGED` gehört ins Budget-Set

Gefunden auf dem Weg zu D134, an einer Zeile, die nicht zur Sache gehörte: `BUDGET_STATES` in
`trust/groups.py` führt `{ACTIVE, REVOKED, SUPERSEDED, PENDING}` und lässt
`EQUIVOCATION_FLAGGED` weg. Weil **beide** Claims eines Equivocation-Paars geflaggt werden, fällt
die ganze Gruppe `(I, J, N)` aus der Budgetrechnung.

**Gerechnet.** Ein Autor bürgt für B mit `n = D = 16`, equivoziert auf diesen Vouch
(`n₂ = 15`) und bürgt danach für C mit `n = 16`. Drei signierte Vouches, `Σ n_budget = 16`,
keine Findings. Der Autor hat sein Budget zweimal ausgegeben, und die Rechnung sieht ihn bei
einmal.

**Equivocation ist damit ein Budget-Reset — und er wirkt bei `include_flagged = True`.**
`derive.py` Schritt 5 schließt geflaggte Autoren **autorweit** aus den Kantenkandidaten aus, nicht
gruppenweit: bei `include_flagged = False` verliert der equivozierende Autor **alle** seine Kanten
im Scope, auch die zu C, und der Reset kauft ihm dort nichts. Bei `True` dagegen werden die Flags
vollständig ignoriert — und dann ist `Σ n_budget ≤ D` die einzige verbleibende Schranke gegen
einen Autor. Genau die hatte die Equivocation ersatzlos entfernt.

Das ist keine Randeinstellung. `02a` hält fest, dass die Ankerwerte in
`02-golden-anchors.md §3–§5` bei `include_flagged = True` gelten; die dokumentierte
Bezugskonfiguration ist die, in der das Loch klaffte.

`02 §3.1` sagt: „Kein selbst-bezüglicher Lebenszyklus-Akt gibt Budget frei; Budget folgt der Uhr,
nicht dem Willen des Autors." Equivocation ist kein Lebenszyklus-Akt und umgeht den Satz an ihm
vorbei. Der tragende Satz desselben Abschnitts — „die Deklaration selbst ist der Einsatz" — hält
nicht, wenn der Einsatz durch Doppelsignatur zurückgeholt werden kann.

**Beschluss: das Budget-Set ist `{ACTIVE, REVOKED, SUPERSEDED, PENDING, EQUIVOCATION_FLAGGED}`
und nicht abgelaufen. Ein Vouch verlässt es ausschließlich durch `t_exp`.**

Die Begründung ist dieselbe, mit der `02 §3.1` `pending` einschließt: der
Über-Commitment-Beweis beruht auf **Signaturen, nicht auf Aktivität**. Und `02 §8` sagt es
direkt — ein Flag darf die Grundlage nicht verschieben, auf der es erkannt wurde.

**Vier Stellen gegen eine.** `02 §8`, `02a §2.6` Satz nach der Tabelle („ausschließlich durch
`t_exp`"), `02a` zu `include_flagged` („Flags ändern nie die Budgetrechnung") und
`02-spec-nachzug §…` sagen dasselbe; allein die Aufzählung in `02a §2.6` sagt etwas anderes. Sie
steht **neun Zeilen** über ihrer eigenen Widerlegung, in derselben Tabelle-plus-Absatz-Einheit.
Die Parallelenprüfung hätte sie gefunden — sie ist auf diese Datei nie angewandt worden, weil
`02a` als erledigte Prompt-Datei galt und nicht als Text, gegen den geprüft wird.

**Wie es entstand.** Die Aufzählung listet die Zustände, in denen ein *gewöhnlicher* Claim landet.
Als Beschreibung war sie richtig; als Definition übernommen, hat sie still ihren Geltungsbereich
verloren. Prüfregel 8, zum vierten Mal nach D77, D83, D87, D91 — und diesmal in der teuersten
Fassung, weil die falsche Hälfte in Code gegossen wurde.

**Sprengweite gemessen, bevor entschieden wurde.** Mit erweitertem `BUDGET_STATES`: 488 Tests
grün, einer rot. Die Golden Anchors aus `02-golden-anchors.md §3–§5` bewegen sich **nicht**;
Variante A bleibt trotz geflaggter CAROL innerhalb `D`.

**Der rote Test ist der Befund selbst.** `test_no_vouch_without_texp_on_flagged_author` behauptet,
ein geflaggter Vouch ohne `t_exp` erzeuge kein `VOUCH_WITHOUT_TEXP`. Das folgt aus der Whitelist
und aus nichts sonst. Unter dem Beschluss bindet dieser Vouch Budget **für immer** — genau die
Lage, vor der das Finding warnt (`02 §…`: `t_exp` ist für Vouches in Scopes mit Budgetregel
verpflichtend). Die Erwartung dreht sich um: das Finding **muss** fallen. Findings sind
bedeutungsblinde Diagnosen; dass der Autor ohnehin slashbar ist, macht die Dauerbindung nicht
kleiner.

**D134 hängt daran.** Die gruppenweise Buchführung in `welten()` kann nicht gebaut werden, bevor
feststeht, wogegen sie rechnet. Reihenfolge: D135, dann `welten.py`.

**Nachtrag zur Wirkung.** Der Absatz über den Budget-Reset stand zuerst in der Gegenrichtung: er
behauptete, der Reset wirke bei `include_flagged = False`, weil der Autor dort „nur die Kante zu B"
verliere. Das war falsch — die Ausschlussmenge in `derive.py` Schritt 5 ist autorweit. Aufgefallen
ist es beim Lesen des Regressionstests, nicht beim Schreiben des Eintrags: `Σ n_budget` war
ausgerechnet, aber nicht bis zu seinem Verbraucher verfolgt.

Daraus die **Wirkungsprüfung**: bevor einem Befund eine Folge zugeschrieben wird, wird der falsche
Wert bis zu der Stelle verfolgt, die ihn verbraucht. Die Wirkung liegt nie dort, wo die Zahl
entsteht. Der Beschluss selbst ist davon unberührt — vier normative Stellen gegen eine Aufzählung,
und das Finding muss fallen.

## AN. Ein Verweis auf gelöschten Text

### D136 — Gelöschte Prompt-Dateien werden umgelenkt, nicht wiederhergestellt

Achtzehn Docstring-Zitate in zwölf Quelldateien zeigen auf `fuzz-prompt.md` und `sim-prompt.md`.
Beide Dateien sind gelöscht. `check_specs.py` führt sie nicht, kann sie also nicht prüfen — und
nach Prüfregel 17 sind sie normativer Text, solange Code auf sie zeigt.

**Ein Verweis auf gelöschten Text ist schlechter als kein Verweis.** Er sieht aus wie eine
Verankerung und ist keine. Wer `welten.py` liest und `fuzz-prompt.md §2` nachschlagen will, findet
nichts und muss raten, ob die Regel noch gilt, wo sie steht oder ob sie je bestand. Ein Docstring
ohne Quellenangabe hätte ihn wenigstens nicht in die Irre geschickt.

**Beschluss: die Zitate werden auf `werkzeuge.md` umgelenkt. Die gelöschten Dateien kehren nicht
zurück.**

Die Begründung ist, dass `werkzeuge.md` kein Ersatzdokument ist, sondern der Nachfolger mit
demselben Inhalt in eigenen Paragraphen: `§4.1` der Generator, `§4.2` die sechs Eigenschaften
`P-1` bis `P-6`, `§2.4` `gabeln` — dort ausdrücklich „für die Simulation (S5) und die
Eigenschaftstests (P-3b) und für nichts sonst" —, `§3.1` bis `§3.3` die Simulation. Die Löschung
war richtig; nur die Docstrings wurden nicht nachgezogen.

**Verworfen: Wiederherstellung aus der Historie.** Sie brächte zwei Dateien zurück, die dasselbe
sagen wie `werkzeuge.md`, und schüfe genau die Parallele, deren stilles Auseinanderdriften
Prüfregel 8 fängt. Zwei Quellen für eine Aussage sind auf Dauer teurer als ein toter Verweis, weil
der tote Verweis wenigstens beim Nachschlagen auffällt.

**Die Tabelle ist normativ.**

| Zitat im Code           | Ziel                |
|-------------------------|---------------------|
| `fuzz-prompt.md §2`     | `werkzeuge.md §4.1` |
| `fuzz-prompt.md §3`     | `werkzeuge.md §4.2` |
| `fuzz-prompt.md §7`     | `werkzeuge.md §2.4` |
| `sim-prompt.md` (ohne §)| `werkzeuge.md §3`   |
| `sim-prompt.md §2`      | `werkzeuge.md §3.1` |
| `sim-prompt.md §3`      | `werkzeuge.md §3.2` |
| `sim-prompt.md §6`      | `werkzeuge.md §3.3` |

Beigefügte Zusätze bleiben, wie sie sind: `02 §7`, `01 §6`, `INV-04.3`, `P-1`. Sie zeigen auf
lebende Dateien. Passt ein Zitat nicht in die Tabelle, wird es gemeldet und nicht geraten.

**Stehende Prüfung daraus.** Vor der Löschung einer Prompt-Datei wird gegriffen, ob Code auf sie
zeigt. Zeigt er, wird im selben Lauf umgelenkt. Eine Löschung, die Verweise hinterlässt, ist nicht
abgeschlossen — und beide hier haben zwei Sitzungen überdauert, weil niemand die Frage gestellt
hat.

## AO. Eine Existenzbehauptung handelt keine Abdeckung

### D137 — `find` bekommt ein festes Budget und einen festen Seed

Drei Tests behaupten die **Existenz** einer Welt statt einer Eigenschaft über viele:
`test_p3a_finds_overcommit_violation`, `test_p3b_finds_equivocation_passed_to_pending` und
`test_finds_budget_exit_via_clock`. Alle drei rufen `find(..., settings=settings())` und erben
damit das Profil aus `tests/property/conftest.py` — unter `schnell` zehn Beispiele, dazu einen
frischen Zufallsseed je Lauf.

**Der Befund: `main` bei `40ee7a5` ist auf einem kalten Klon rot.** Gemessen mit gelöschtem
`.hypothesis/` und altem Generator: `p3a` und `p3b` scheitern beide mit `NoSuchExample`. Grün
waren sie zwei Sitzungen lang, weil die Beispieldatenbank die gefundenen Welten vorhielt — und
`.hypothesis/` ist gitignored. Grün war eine Eigenschaft der Arbeitskopie, nicht des Commits.

**Aufgefallen ist es auf dem Weg zu etwas anderem.** Der Lauf `impl/welten` meldete `p3a` als neu
fragil und vermutete die geänderte Ziehungsreihenfolge. Die Gegenprobe kehrt das um: kalt bei
`4da3304` grün, kalt bei `40ee7a5` rot, einzige verhaltenswirksame Variable `welten.py`. Der Lauf
hat den Test nicht zerbrochen, er hat ihn repariert. Der Defekt lag woanders und war älter.

**Beschluss: `find` läuft mit `max_examples=200` und `derandomize=True`, unabhängig vom Profil.**

Die Begründung ist, dass `schnell` gegen `voll` **Abdeckung gegen Zeit** handelt. Bei einer
Eigenschaft über viele Welten ist das ein sinnvoller Handel: weniger Beispiele heißt weniger
geprüfte Fälle, aber jede geprüfte Aussage bleibt wahr. Eine Existenzbehauptung hat nichts zu
handeln — die Antwort ist ja oder nein. Ein Nein aus Zeitmangel ist von einem Nein aus Sachgrund
nicht zu unterscheiden, und genau diese Verwechslung hat hier zwei Sitzungen überdauert.

`derandomize=True` nimmt dem Test das Streuen über Läufe. Bei einer Eigenschaft wäre das ein
Verlust; hier ist es der Zweck. Findet ein Lauf nichts, ist das nach `werkzeuge.md §4.2` der
Befund — und er soll reproduzierbar sein, nicht launisch.

**Die Zahl ist gemessen, nicht geraten.** Unter festem Seed genügen zehn Beispiele für alle drei.
Zweihundert ist Faktor zwanzig Abstand zum Rand. Null Abstand wäre auf andere Weise spröde: die
nächste Generatoränderung verschiebt den Ziehungsstrom, und ein fester Seed ohne Reserve ist dann
dauerhaft rot statt gelegentlich.

**Verworfen: die gefundene Welt als festen Vektor einfrieren.** `test_p3.py` führt zwei solche
Vektoren, und sie behaupten etwas anderes als die Suche. Ein Vektor sagt „diese Welt verletzt die
Eigenschaft"; die Suche sagt „**der Erzeuger erreicht diese Gegend**". Das zweite ist die Aussage,
die hier gebraucht wird, und genau sie ist eingetreten und war unsichtbar. Ein späterer Lauf, der
die Suche gegen einen Vektor tauscht, löscht die Aussage und hält es für Aufräumen. Dieser Absatz
steht hier, damit er es nicht tut.

**Der gemessene Preis, und was er wirklich ist.** Nach der Umstellung steht `make check` bei 16,46 s gegen 10,09 s zur Prompt-Grundlinie und gegen 6,44 s zum warmen Arbeitsstand. Die zweite Zahl ist die ehrliche: `find` spielt nicht mehr aus `.hypothesis/` ab, und die alte Laufzeit war ein Cache-Preis, kein Rechenpreis. Die Kosten sind nicht gestiegen, sie sind zum ersten Mal sichtbar. Dieser Absatz steht hier, damit der Satz "D137 hat den Testlauf verlangsamt" nicht in einem Jahr als Argument gegen D137 wiederkommt.

**Verworfen: `.hypothesis/` einchecken.** Es macht den Cache zur Grundlage statt ihn zu
entwerten — dieselbe Abhängigkeit, nur committet.

**Messfehler in der eigenen Vorarbeit, für die Akte.** Die Laufzeiten zu dieser Entscheidung waren
zuerst unbrauchbar: `derandomize=True` schaltet die Beispieldatenbank nicht ab, der erste
Messlauf füllte sie, der zweite las daraus. `n=200` kam auf 7,59 s, `n=10` auf 12,45 s — bei
festem Seed unmöglich. Zwei Läufe, zwei Variablen. Der Fund-Befund selbst ist davon unberührt,
weil er unter festem Seed nicht vom Cache abhängt; die Kosten misst deshalb `make check` und
nichts sonst.

## AP. Die Tür der Simulation

### D138 — Lauf B ist zwei Funktionen; der Einlesepfad lädt ohne Store

Drei Beschlüsse, jeder mit eigener Begründung, weil sie unabhängig voneinander falsch sein können.

**Erstens: das Bündelformat gehört nicht in diesen Lauf.**

Der Zuschnitt-Absatz in D132 zählt Lauf B als drei Dinge auf — Bündelformat, `store_laden` und
`zustellen` über den neuen Pfad, `claim_id` nachgerechnet. Das erste folgt aus keinem der beiden
normativen Sätze von D132. D132 schreibt selbst: die Inbox **ist** das unsignierte Bündel aus
D121, nur als Verzeichnis. Wenn sie es ist, verlangt D132 kein neues Format; die Aufzählung hat es
aus D121s Kontext mitgebracht, wo es hingehört.

Dieselbe Form wie D77, D83, D87, D91, D130, D134 und D135: ein Satz und eine Aufzählung, und die
Aufzählung hat beim Wandern still ihren Geltungsbereich gewechselt. Prüfregel 18.

**Lauf B ist damit `store_laden` und `hat_claim`, und sonst nichts.** `zustellen` schiebt
unvertraute Bytes zwischen unvertrauten Verzeichnissen; die Grenze liegt beim Lesen, nicht beim
Kopieren. Ein zweiter Erkenner an der Kopierstelle wäre genau der über das Programm verteilte
Erkenner, gegen den D132 geschrieben ist.

**Zweitens: `store_laden` ruft `read_claim(data)` ohne Store.**

`structural_check` benutzt den Store an genau einer Stelle: `_check_foreign_lifecycle`. Ohne Store
ist diese Prüfung nicht falsch, sondern **stumm** — Ziel unbekannt, also kein Reject. Dasselbe
Muster wie in `classify`: „bei bekannter Ziel-Identity".

Der Grund gegen einen durchgereichten Store ist nicht, dass er beim Laden halbfertig wäre; das ist
das Symptom. Der Grund ist, dass ein Teilstore `FOREIGN_LIFECYCLE` **an die Hex-Sortierung von
Dateinamen bindet**. Derselbe Claim wäre je nach Ladereihenfolge Reject oder nicht. Ein Reject,
den ein Beobachter nur bei günstiger Hash-Reihenfolge sieht, ist schlimmer als keiner: er macht
die Ablehnung selbst zu einer lokalen Laune. `werkzeuge.md §4.2` P-1 — Reihenfolgeunabhängigkeit —
ist die Eigenschaft, gegen die dieses Projekt seit zwei Sitzungen prüft, und sie gilt für den
Einlesepfad genauso wie für die Ableitung.

Ohne Store ist die Prüfung stumm und **gleichbleibend** stumm. Die Kontextarbeit macht
`classify_all` später auf dem vollständigen Bestand, wo sie hingehört.

**Vermerk, damit es niemand für einen Fehler hält.** `FOREIGN_LIFECYCLE` hat damit im
Produktivcode keinen Träger mehr. Der Code existiert, Vektortests prüfen ihn, und der einzige
Produktivpfad, der ihn auslösen könnte, ruft ohne Store. Das ist vertretbar, weil `index.py` die
Prüfung als Zustandsprüfung ein zweites Mal führt und dort `ForeignLifecycle` wirft. Es ist aber
eine Aussage und kein Zufall, und ohne diesen Absatz hält sie in einem Jahr jemand für einen Bug
und repariert sie in die falsche Richtung.

**Drittens: `hat_claim` glaubt dem Dateinamen nicht.**

Heute ist `hat_claim` ein `is_file()` auf `{cid.hex()}.cbor`. Niemand rechnet nach, dass in
`abc….cbor` ein Claim mit `claim_id == abc…` steht. `claim_id` ist der Hash über `core_bytes`,
und erst die Kanonizitätsprüfung bindet empfangene Bytes an diese Id — ohne sie ist die Zuordnung
von Name zu Inhalt eine Behauptung des Absenders.

Der Name bleibt der Hinweis, wo nachzusehen ist. Die Antwort kommt aus dem Inhalt.

**Die Wirkung liegt nicht dort, wo der Fehler entsteht.** `Teilnehmer.kennt` ist der
`Ausgang.kennt`-Port, den `Autor.wiederaufnehmen` in `tools/autor.py:189` befragt, um zu
entscheiden, ob die gespeicherte Spitze im Ausgang vorliegt. Ein falsches „kenne ich" aus einem
Dateinamen lässt `wiederaufnehmen` die Kette über einen Vorgänger fortschreiben, den niemand hält
— statt sie nach D120 anzuhalten. Ein Absender kann heute die Kette des Empfängers stören, **ohne
eine einzige Signatur zu fälschen.** Das ist der Grund für diesen Lauf; die nachgerechnete
`claim_id` ist nur das Mittel.

**Der Preis ist gemessen und wird bezahlt.** `zustellen` fragt für jede Datei bei jedem Ziel
`hat_claim`; aus einem `is_file()` wird ein Lesen plus Prüfen. Die Szenarien laufen mit `nur=` und
über Inboxen einstelliger Größe, die Zahlen tragen es. Kein Cache und kein Index — ein Index wäre
wieder etwas, dem geglaubt wird, und damit derselbe Fehler eine Ebene höher.

**Zurückgestellt: eine Meldung übersprungener Claims.** `store_laden` überspringt still, was
`read_claim` als `ErrorCode` liefert; das ist nach D133 die richtige Semantik — ein Beobachter
hält genau das, wofür `read_claim` einen `Claim` geliefert hat. Ein Zähler oder ein Protokoll wäre
ein zweiter Kanal aus derselben Funktion und verbreiterte den Port, den D127 schmal hält. Wenn
sich beim Debuggen von Szenarien herausstellt, dass die Stille teuer ist, ist das ein eigener
Fork mit eigener Begründung und nicht ein Zusatz hier.

**Gemessen vor dem Prompt:** es gibt heute keinen Test, in dem Dateiname und Inhalt
auseinanderfallen. `tests/test_sim.py` führt einen parametrisierten Szenariotest und berührt
weder `inbox_path` noch `fromhex`. Der Regressionstest ist deshalb neu zu bauen, und die
Rücknahmeprobe hat einen eindeutigen Ort.

### D139 — Distanz ist kaufbar; der Satz vom doppelten Schutz fällt

**⚠️ Die Zahlen dieses Eintrags sind durch D141 ersetzt** (`02 §4`, Warnblock). Der Befund
bleibt, die Rechnung war falsch: `Σ C(h)` ist eine Schranke, kein Ertrag.

Ausgelöst durch die Frage, was ein erster realer Einsatz eigentlich prüfen würde. Vorgeschaltet
war eine Literaturprüfung (Prüfregel 15), weil das Problem außerhalb von MaR seit
fünfundzwanzig Jahren bearbeitet wird. Ergebnis der Prüfung: die Feldfrage und die
Angriffsfrage sind verschiedene Fragen, und die zweite ist heute entscheidbar, ohne einen
einzigen weiteren Menschen.

**Erstens: der Satz vom doppelten Schutz fällt.**

Das Korollar in `02 §4` schließt mit der Beobachtung, eine seed-ferne Angriffskante sei ohnehin
billig, weil `C(h) = ⌊C₀ γ^{d(s,h)}⌋` mit der Distanz falle. Der Satz behandelt `d(s,h)` als
Eigenschaft des ehrlichen Knotens. Das ist sie nicht: `d` ist die BFS-Distanz über dem
**aktuellen** wirksamen Kantenset `E⁺`, und dieses Kantenset gestaltet der Angreifer mit.

Der Satz ist außerdem eine **Kostenaussage** — „billig" —, und ein Kostenmodell für verwirrte
ehrliche Knoten hat die Spec nirgends. Die Schranke selbst braucht keines: sie ist eine Aussage
über den Graphen, wie er vorliegt. Der angehängte Satz behauptet mehr, als der bewiesene Satz
trägt, und verliert dabei still den Geltungsbereich seiner eigenen Begründung.

**Zweitens: der Angriff wird benannt, nicht abgewehrt.**

Ein Angreifer, der einen seed-nahen ehrlichen Knoten `p` verwirrt, kann durch Bürgschaften bis zu
`min(D, C(p))` andere ehrliche Knoten gleichzeitig näher an den Seed ziehen und damit deren
Kapazität heben. Entscheidend ist die Rollenverteilung: `p` bürgt für **ehrliche** Knoten, nicht
für Sybils, ist also kein Grenzknoten im Sinne des Satzes und taucht in `Σ_{h ∈ Grenze} C(h)`
überhaupt nicht auf. Gekauft wird genau der Knoten, den die Schranke nicht sieht, und er
multipliziert die Kapazität derer, die sie sieht.

`02 §4` bekommt dazu einen Warnabsatz. Kein neuer Mechanismus, keine Änderung an Kapazität,
Budget oder Fluss: die Spec sagt an der Stelle, was gilt, statt an der Stelle etwas zu
versprechen, was sie nicht hält.

**Drittens: der Min-Cut-Beweis bleibt unangetastet.**

`maxflow(s → S) ≤ Σ_{h ∈ Grenze} C(h)` ist korrekt, die `|S|`-Unabhängigkeit steht, und
„Identitäten gratis, Kanten teuer" steht ebenfalls. Was fällt, ist allein die Behauptung, die
zweite Verteidigungslinie sei von der ersten unabhängig. Sie ist es nicht — beide werden aus
demselben Vorrat verwirrter ehrlicher Menschen bezahlt.

**Gemessen vor dem Prompt.** Mit den Anker-Parametern `γ = ½`, `C₀ = 16` und `D ≥ C₀` (§8) ist
`C(d) = 16, 8, 4, 2, 1, 0` für `d = 0…5`. Ein verwirrter Knoten `p` bei `d = 1` trägt `C(p) = 8`
und hat wirksamen Out-Degree `min(D, C(p)) = 8`. Acht ehrliche Knoten bei `d ≥ 5` tragen `C = 0`
und sind nach `§3` nicht einmal bürgschaftsfähig; nach `p`s Bürgschaft sitzen sie bei `d = 2` und
tragen je `C = 4`. Die Grenzsumme steigt damit von `0` auf `32`. Allgemein ist der Ertrag
`C(p) · ⌊γ · C(p)⌋`, also **quadratisch in der Kapazität des einen teuren Knotens**. Ohne den
Trick müsste derselbe Angreifer acht Menschen bei `d = 2` verwirren; sobald Seed-Nähe teurer ist
als Seed-Ferne — und darauf beruht das gesamte Distanz-Decay-Argument —, ist der Trick strikt
billiger. Die Zahlen sind gerechnet, nicht gemessen; der Simulationslauf hat damit einen
abgeleiteten Erwartungswert und keine getippte Menge.

**Belege aus der Literatur.** Levien betrieb die Advogato-Metrik jahrelang mit echten Nutzern und
berichtet als Ergebnis, die Metriken hätten ihren Zweck erfüllt, entscheidend sei aber die
Deckung zwischen den Annahmen der abstrakten Berechnung und der realen Implementierung. Der
eigentliche Defekt kam nicht aus dem Feldbetrieb: Ruderman fand beim Nachlesen des Beweises, dass
dieser über die Kapazitäten **nach** dem Angriff beschränkt statt über die davor, und
konstruierte daraus einen Ertrag im Quadrat der Angriffskosten. MaRs Kapazitätsmodell ist
dasselbe Distanz-Decay, also überträgt sich die Konstruktion. Bei Secure Scuttlebutt fand der
Feldbetrieb dafür anderes — Replikationslecks, eine Kanonisierung ohne deterministische
Schlüsselordnung, ein einzelnes langlebiges Signaturschlüsselpaar. Zwei davon sind in MaR
strukturell geschlossen, das dritte ist die offene Schlüsselrotation. Die Lehre für die
Reihenfolge: **Feldbetrieb findet Implementierungsränder, Nachrechnen findet Beweislücken.**

**Nicht entschieden.** Ob ein Mechanismus reagieren soll, bleibt offen und ist ein eigener Fork
mit sozialer Konsequenz — es geht darum, wessen Position kaufbar ist. Offen bleibt insbesondere,
ob die PageRank-Relaxation aus `02 §5` an dieser Stelle robuster ist als der maßgebliche
Max-Flow; Ruderman hält PageRank für unempfindlich, weil der erlangte Score durch den
Vor-Angriffs-Score der verwirrten Knoten beschränkt bleibt. `02 §5` ist zum Zeitpunkt dieses
Eintrags ungelesen, die Übertragung daher Hypothese und ausdrücklich keine Entscheidung.

**Prüfregel 20 — Kostenaussage braucht Kostenmodell.** Ein Satz, der etwas „billig", „teuer"
oder „ohnehin unattraktiv" nennt, ist eine Aussage über Angriffskosten. Steht in der Spec kein
Kostenmodell, das ihn trägt, fällt der Satz — auch und gerade dann, wenn der Satz daneben
bewiesen ist. Ein bewiesener Nachbar macht eine unbelegte Behauptung nicht wahr, er macht sie
nur schwerer sichtbar.

**Neuntes Auftreten der Form „Satz und Anhang".** Nach D77, D83, D87, D91, D130, D134, D135 und
dem Zuschnitt-Absatz in D132 ist dies der neunte Fall, in dem eine tragende Aussage einen zweiten
Satz mitführt, der ihren Geltungsbereich still überschreitet. Prüfregel 18 fängt die Form beim
Hinsehen; gefunden wurde sie auch diesmal nicht beim Lesen der Spec, sondern beim Versuch, gegen
sie zu argumentieren.

### D140 — Abschnitt 5 wird auf D45 nachgezogen; die Relaxation ist gegen den Distanzkauf immun

Aufgefallen beim Versuch, die in D139 offengelassene Frage aus `02 §5` zu beantworten: der
Abschnitt beschrieb das Gegenteil dessen, was seit D45 gilt.

**Erstens: die Layer-Datei widersprach dem Register.**

`02 §5` führte `P` als spaltenstochastisch über `Σw` normalisiert — zweimal im Fließtext und in
einem Blockabsatz, der diese Normalisierung gegen `§4` rechtfertigte und sie „genau die
Trennlinie zwischen beiden Sichten" nannte. D45 hat beides aufgehoben: normativ gilt
`P[J][I] = n_kante(I, J) / D` ohne Kopplung an andere Kanten, und die D9-Ausnahme für `§5`
entfällt **ersatzlos**, womit `§7` in beiden Sichten gilt. Der Rechtfertigungsabsatz, der noch
in der Layer-Datei stand, **war** der gestrichene Sonderstatus.

`02b-golden-anchors.md` führt unter K9 die richtige Fassung, die Implementierung folgt K9, und
die Testnamen in `tests/trust/` nennen die spaltenstochastische Fassung ausdrücklich als die
verworfene. Kein Test konnte deshalb rot werden: **nur die Spec war falsch.** Genau das ist die
Driftform, gegen die das Register gebaut ist — die Entscheidung war getroffen, begründet und
implementiert, und die Datei, die ein Leser zuerst aufschlägt, sagte das Gegenteil.

Nachgezogen wird ausschließlich Text. Kein Mechanismus, keine Zahl, kein Anker ändert sich.

**Zweitens: die überholte Zeile in `02-spec-nachzug.md` wird markiert, nicht stillschweigend
umgeschrieben.** Sie steht unter „Was danach noch offen ist" und trägt die D27-Fassung. Ein
falscher normativer Satz in einer Bestandsliste ist teurer als ein sichtbar aufgehobener, also
bleibt der ursprüngliche Verweis stehen und bekommt die Aufhebung danebengeschrieben.

**Drittens: die offene Frage aus D139 ist beantwortet — mit korrigierter Begründung.**

Der Distanzkauf greift in `§5` nicht. Ich hatte das zunächst damit begründet, `§5` kenne keinen
Distanzterm. Das ist **falsch**: `C(x)` geht sehr wohl ein, nämlich als Filter darüber, welche
Kanten in `E⁺` liegen (Anker K13, so auch der Kommentar in `trust/relax.py`). Ein verwirrter
seed-naher Knoten kann den Kantensatz von `§5` also durchaus verändern — Knoten mit `C = 0`
werden emissionsfähig, sobald sie näher an den Seed rücken.

Der tragende Grund ist ein anderer und ist Rudermans eigener: das **Gewicht** einer Kante hängt
nicht von `C` ab, und wegen `Σ n ≤ D` ist jede Spalte von `P` sub-stochastisch. Ein Knoten gibt
höchstens weiter, was er empfängt. Der Ertrag des Angriffs bleibt damit durch die
**Vor-Angriffs-Masse** der verwirrten Knoten beschränkt; ein quadratischer Term entsteht nicht.
Die Immunität kommt aus der Massenerhaltung, nicht aus der Abwesenheit einer Größe.

Das macht `§5` **nicht** zum Ersatz für `§4`. Die Relaxation trägt keine harte Schranke und ist
für Gates verboten; sie ist unverwundbar, weil sie nichts verspricht. Damit steht der Trade-off
sauber: **die Verwundbarkeit von `§4` ist der Preis der harten Schranke.** Der Min-Cut-Beweis
braucht eine harte Knotendecke, die Decke braucht eine Positionsgröße, und jede Positionsgröße
über dem Vouch-Graphen ist mit Vouches beeinflussbar.

**Der Fork lautet damit präziser als in D139:** Gibt es eine harte Knotendecke, die nicht über
den Graphen gekauft werden kann? Das ist eine Literaturfrage — die SybilLimit-Linie arbeitet mit
Random Routes statt mit Distanz — und sie ist groß genug für eine eigene Runde. Sie bleibt offen
und wird hier ausdrücklich nicht entschieden.

**Gemessen.** Einträge, die im Titel eine Korrektur eines älteren Eintrags ausweisen: **genau
einer**, D45. Und genau dieser eine war nicht nachgezogen. Die Stichprobe ist klein, die
Trefferquote ist eins. Träger des veralteten Satzes außerhalb des Registers: zwei Zeilen in
`02-trust-flow.md` plus der Rechtfertigungsabsatz, eine Zeile in `02-spec-nachzug.md`. Alle
übrigen Fundstellen — `02b-abnahme.md`, `02b-golden-anchors.md`, zwei Testmodule — nennen die
spaltenstochastische Fassung korrekt als die verworfene.

**Konvention:** Hebt ein Registereintrag einen älteren auf, weist der Titel das aus und der Text
nennt **Datei und Abschnitt**, die nachzuziehen sind. Ohne diese Angabe ist die Aufhebung im
Register vollständig und in der Spec unsichtbar — der Zustand, der hier zwei Jahre gehalten hat.

### D141 — Der Distanzkauf entfernt eine Decke, er trägt keinen Fluss (korrigiert D139)

Nachzuziehen war `02-trust-flow.md §4`, Warnblock „Distanz ist kaufbar". Der Befund von D139
bleibt vollständig bestehen; falsch war die Rechnung darin.

**Der Fehler.** D139 schrieb, die Grenzsumme steige von `0` auf `32`, und nannte das den
„Ertrag `C(p) · ⌊γ · C(p)⌋`, quadratisch in `C(p)`". `Σ_{h ∈ Grenze} C(h)` ist aber eine
**obere Schranke**, kein erzielter Fluss. Die dort beschriebene Konstruktion — acht vorher
unerreichbare Knoten mit `C = 0`, neu angehängt an `p` — trägt sogar **gar keinen** zusätzlichen
Fluss: aller Fluss zu diesen Knoten müsste durch `p` laufen, und `p` deckelt bei `C(p)`. Der
Angriff, wie ich ihn aufgeschrieben hatte, ist wertlos. Die Verwechslung von Schranke und Ertrag
ist genau die Sorte Fehler, die Prüfregel 20 im Nachbarsatz gefunden hat und im eigenen Satz
nicht.

**Aufgefallen beim Versuch, den Testgraphen zu bauen.** Die Behauptung war zwei Tage alt und
hatte einen Registereintrag, einen Warnblock in der Layer-Datei und eine Runde Prosa überstanden.
Sie fiel in dem Moment, in dem sie für eine Maschine präzise genug formuliert werden musste —
das D118-Muster, inzwischen zum wiederholten Mal.

**Gemessen** (`γ = ½`, `C₀ = 16`, `D = 16`, Messlauf gegen `trust()` und `derive()`):

| | ohne Angriff | mit Angriff |
|---|---|---|
| `d(h)` | 4 | 2 |
| `C(h)` | 1 | 4 |
| Zufluss zu `h` | 8 | 9, davon 1 von `p` |
| `Σ C(h)` über der Grenze | 1 | 4 |
| `maxflow(A → S)` | **1** | **4** |
| `disjoint_paths` | 1 | 1 |

Die Topologie: ein Anker `A`, vier Ketten `A → a_i → b_i → x_i → h` der Länge 4, dann `h → S`.
`h` hat damit `8` Zufluss und sitzt bei `d = 4` mit `C(h) = 1` — die Knotendecke schneidet sieben
Achtel des vorhandenen ehrlichen Zuflusses ab. Der Angreifer verwirrt `p` bei `d = 1` und lässt
`p` mit `n = 2` von Budget `16` für `h` bürgen. Die Kante trägt `cap = ⌊2 · 8 / 16⌋ = 1`, genügt
aber, um in `E⁺` zu liegen; `bfs_capacities` setzt `distance` beim **ersten** Sehen und
schichtweise, also rutscht `h` auf `d = 2` und `C(h)` auf `4`.

**Die korrigierte Aussage.** Gekauft wird nicht Fluss, sondern das **Entfernen einer Decke**. `p`
steuert genau eine Kapazitätseinheit bei; drei der vier Einheiten sind ehrlicher Fluss, der
vorher an `C(h) = 1` abgeschnitten wurde. Daraus folgt, welcher Grenzknoten für einen Angreifer
lohnt: nicht der unerreichbare — der trägt nichts —, sondern der **gut verbundene, aber
seed-ferne**. Peripherie mit Substanz. Wer lange dabei und weit vom Seed ist, ist das lohnendste
Ziel, und das ist eine unangenehmere Aussage als die ursprüngliche.

`disjoint_paths` bleibt bei `1` und ist damit die Größe, die der Angriff **nicht** bewegt. Ob das
trägt oder ein Artefakt dieser Topologie ist, ist nicht gemessen und wird hier nicht behauptet.

**Was unverändert bleibt.** Der Min-Cut-Satz stimmt, die Schranke steigt mit (`1 → 4`) und bleibt
wahr — sie ist eine Aussage über den Graphen nach dem Angriff. Was fällt, bleibt der gestrichene
Satz vom doppelten Schutz aus D139. Die Immunität der Relaxation aus D140 ist von dieser
Korrektur nicht berührt: dort ging es um Masse, nicht um Decken.

**Offen und ausdrücklich nicht entschieden.** Wie der Effekt mit `p`s Budget skaliert — `p` kann
`⌊D / (D/C(p))⌋ = C(p)` solcher Kanten legen, ohne dass der eigene Durchsatz von `C(p)` je
gebraucht wird — ist gerechnet plausibel und **nicht gemessen**. Es steht deshalb in keiner
Spec-Datei. Ebenso offen bleibt der Fork aus D140: gibt es eine harte Knotendecke, die nicht über
den Graphen gekauft werden kann?

**Nächster Schritt.** Der Messlauf wird zu einem Charakterisierungstest unter `tests/trust/`. Er
repariert nichts; er nagelt fest, dass die Zahl `4` ist und nicht `1` oder `8`. Entsteht je ein
Mechanismus gegen den Distanzkauf, wird genau dieser Test rot — das ist die Rücknahmeprobe im
Voraus.

### D142 — Die Decke wandert genau dann, wenn `d` sich bewegt (ergänzt D141)

**Die Frage.** D141 hält fest, dass `Σ_{h ∈ Grenze} C(h)` beim Distanzkauf von `1` auf `4`
steigt und der Min-Cut-Satz davon unberührt bleibt. Ungemessen war, **unter welcher Bedingung**
die Schranke mitwandert — und ob es Züge gibt, bei denen sie stillsteht. Der Satz „bleibt
unberührt" ist wahr und liest sich wie eine Beruhigung; ohne die Bedingung ist er keine.

**Gemessen** (`γ = ½`, `C₀ = 16`, `D = 16`, `tests/trust/test_deckenelastizitaet.py`). Der
Beitrag von `p` ist der **zugeführte Fluss** `min(cap(A → p), Σ cap(p → h))`, nicht die
Ausgangskapazität. Der Term `C(p)` ist nach `02 §3`, Nachtrag seit D1, redundant und darum nicht
Teil der Definition.

| Fall | Zug | `Σ C(h)` ohne → mit | `maxflow` ohne → mit | Beitrag `p` | Hebel |
|---|---|---|---|---|---|
| A | Distanzkauf, `p → h` mit `n = 2` | 1 → 4 | 1 → 4 | 1 | **3** |
| B | Spende, `d(h)` bleibt `1`, ungesättigt | 8 → 8 | 1 → 5 | 4 | **1** |
| B2 | Spende, `d(h)` bleibt `1`, gesättigt | 8 → 8 | 1 → 8 | 8 | **7/8** |
| C, `k = 1` | `1` gekaufte Kante | 1 → 4 | 1 → 4 | 1 | 3 |
| C, `k = 2` | `2` gekaufte Kanten | 2 → 8 | 2 → 8 | 2 | 3 |
| C, `k = 3` | `3` gekaufte Kanten | 3 → 12 | 3 → 12 | 3 | 3 |

**Erstens: die Elastizität hat eine Bedingung.** In A und C bewegt der Zug `d(h)`, und `Σ C(h)`
wandert exakt mit dem Fluss. In B und B2 bewegt er `d(h)` nicht, und `Σ C(h)` steht still,
während der Fluss steigt. Die Schranke ist nicht generisch angreiferabhängig — sie ist es genau
dann, wenn der Zug eine **Distanz** verschiebt. Alles andere lässt sie unberührt.

**Zweitens: nur der Distanzkauf hat Hebel.** Ein Zug, der keine Distanz ändert, ändert keine
Kapazität und kann folglich höchstens den Fluss addieren, den er selbst trägt — Hebel `≤ 1`.
B zeigt den Gleichstand (`4` zugeführt, `4` Zuwachs), B2 den Verfall an der Decke (`8` zugeführt,
`7` Zuwachs). Der Distanzkauf zahlt `1` und bekommt `3`. Das ist der ganze Unterschied zwischen
den beiden Angriffsformen, und er sitzt nicht in der Größe des Einsatzes.

**Drittens: die Schranke ist schlaff, wo die Decke nicht bindet.** In B steht `maxflow = 5`
gegen `Σ C(h) = 8`. `Σ C(h)` ist dort keine Näherung des Flusses, sondern überzeichnet ihn um
`60 %`. In A, B2 und C ist sie scharf. Wer `Σ C(h)` als Kennzahl liest statt als Schranke, liest
je nach Graphlage etwas anderes.

**Skalierung — das offene Stück aus D141 ist geschlossen.** Der Hebel ist über `k = 1, 2, 3`
konstant `3`; `Σ C(h)` und `maxflow` wachsen beide linear. D141 vermutete, `p` könne `C(p)`
solcher Kanten legen. Gemessen bindet in dieser Topologie **das Budget des Ankers zuerst**:
`A` liegt bei `k = 3` mit `4 + 4k = 16` genau auf `D`, während `p` bei `2k = 6` noch weit unter
`D` sitzt. Die ehrliche Substanz, die der Kauf freilegt, musste selbst durch das Ankerbudget.
Das ist ein Befund über diese Topologie, keine allgemeine Aussage — behauptet wird nur, dass
`p`s Budget **nicht** notwendig die bindende Größe ist.

**Literaturprüfung (PR-15).** Cheng/Friedman (P2PECON 2005) zeigen, dass keine symmetrische,
nichttriviale Reputationsfunktion sybilproof sein kann, und geben für **flussbasierte,
quellrelative** Funktionen Bedingungen an, unter denen sie es sind. `02 §4` liegt damit in der
erreichbaren Klasse; verwundbar ist nicht der Fluss, sondern die darübergelegte
Kapazitätszuweisung, deren Eingang `d(s,h)` ein Kürzeste-Pfad-Maß ist — und ein kürzester Pfad
ist genau das, was eine einzelne Kante verkürzt. SumUp (Tran et al., NSDI 2009) benutzt dieselbe
Konstruktion (mit der Distanz fallende Kantenkapazität, approximierter Max-Flow zu einem
vertrauten Sammler) und hat **keine** unkaufbare Knotendecke: die Garantie sitzt dort an der
Zahl der Angriffskanten, nicht am Knoten. Die SybilLimit-Linie scheitert an MaRs Constraints vor
der Arithmetik: sie braucht `r = Θ(√m)` und eine Schätzung der Mixing-Zeit, also lokale
Schätzungen **globaler** Größen.

**Was daraus folgt.** Eine harte Knotendecke, die nicht über den Graphen kaufbar ist, existiert
in dieser Familie nicht, und die reifsten Systeme haben die Garantie stattdessen auf den Schnitt
verlegt. `02 §4` tut das bereits. Der Distanzkauf ist der Preis der harten Schranke, nicht ein
Fehler in der Wahl der Sicht.

**Methodik.** Der Lauf brauchte vier Anläufe, und alle vier Defekte lagen im Prompt, nicht in der
Arbeit des Werkzeugs. Zweimal derselbe Fehlertyp: eine **Kapazität als Ertrag** geführt — erst
`cap(p → h) = 8` als Beitrag, obwohl `p` über `A → p` nur `4` empfängt, dann `C(p)` als Term
einer Minimumsbildung, obwohl `02 §3` ihn als nie allein bindend beweist. Beide Male fiel die
Behauptung erst, als sie an einer konkreten Topologie präzise werden musste. Daraus **Prüfregel
21: eine Kapazität ist eine Schranke, kein Ertrag** — wer eine Kapazität in eine Bilanz
einsetzt, muss den Weg rechnen, den der Fluss zu ihr nimmt. Und als Zusatz: ein Term, den die
Spec als redundant beweist, kann von keiner Rücknahmeprobe rot gefärbt werden; eine Probe, die
ihn treffen soll, ist falsch gebaut.

**Was unverändert bleibt.** Der Min-Cut-Satz, die `|S|`-Unabhängigkeit, VR-02.1, die Immunität
der Relaxation aus D140. D141 ist in keinem Punkt korrigiert, nur ergänzt.

**Offen und ausdrücklich nicht entschieden.** Ob `02 §4` einen normativen Satz erhält, der
`Σ C(h)` für Gates ausschließt — die Größe ist schlaff, wo die Decke nicht bindet, und sie
wandert mit dem Angreifer, wo sie es tut. Ebenso offen bleibt der Fork selbst: ob ein Mechanismus
gegen den Distanzkauf gebaut wird. Beides sind Entscheidungen des Operators.

### D143 — Kein Mechanismus gegen den Distanzkauf (schließt den Fork aus D140/D141)

**Entschieden.** Es wird kein Mechanismus gebaut, der den Distanzkauf verhindert, erkennt oder
abmildert. `C(x) = ⌊C₀ · γ^{d(s,x)}⌋` bleibt wie in `02 §3`. Die Kaufbarkeit von `d` bleibt eine
benannte, gemessene und getestete Eigenschaft der Schicht.

**Erstens — das Aufnahmekriterium schließt es aus.** `08 §3` fragt: senkt der Mechanismus die
Kosten dafür, festzustellen, wer was gesagt hat, oder verteilt er Macht? Eine Positionsgröße
gegen Bürgschaften zu stabilisieren, senkt keine Feststellungskosten. Es legt fest, wessen
Position beweglich ist und wessen nicht — das ist Machtverteilung, also Policy, nicht Protokoll.

**Zweitens — und das trägt die Entscheidung: der Schaden ist zu einem großen Teil gar keiner.**
D141 hat gemessen, dass `p` eine Kapazitätseinheit beisteuert und der Fluss um drei steigt. Die
drei Einheiten sind **ehrlicher Fluss, den die Decke vorher abgeschnitten hat**: `h` hatte einen
Zufluss von `8` und durfte `1` weiterreichen. Der Kauf hebt eine Unterschätzung auf, die die
Schicht selbst erzeugt hat. Ein Mechanismus, der den Kauf verhindert, hält genau diesen ehrlichen
Fluss weiter draußen — er macht das Protokoll über einen gut verbundenen, seed-fernen ehrlichen
Knoten dauerhafter falsch, um einem Angreifer einen Hebel zu nehmen, den dieser mit dem Budget
eines verwirrten Menschen bezahlen muss. Der Tausch lohnt nicht.

**Drittens — die Literatur kennt die gesuchte Größe nicht.** Nach D142: eine harte Knotendecke,
die nicht über den Graphen kaufbar ist, existiert in der Familie sozialgraph-basierter Abwehren
nicht; die reifsten Systeme (SumUp) haben die Garantie stattdessen an die Zahl der Angriffskanten
gehängt. `02 §4` tut das bereits. Die Alternative mit der stärksten Schranke (SybilLimit) setzt
Schätzungen globaler Größen voraus und ist mit „alles lokal, nichts global" unvereinbar.

**Was damit als Preis angenommen ist.** Ein Angreifer, der einen seed-nahen ehrlichen Menschen
verwirrt, kann seed-ferne ehrliche Knoten näher an den Anker ziehen und deren Decke heben — mit
Hebel `3` bei Kosten von einer Kapazitätseinheit, linear in der Zahl der so behandelten
Grenzknoten, gedeckelt in der gemessenen Topologie durch das Budget des Ankers. Das ist der Preis
der harten Schranke aus `02 §4` und keine Schwäche in der Wahl der Sicht: die Schranke braucht
eine Obergrenze pro Knoten, die Obergrenze braucht eine Positionsgröße, und jede Positionsgröße
über dem Vouch-Graphen wird mit Vouches gestaltet. `02 §5` ist davon frei, weil es nichts
verspricht — keine harte Schranke, für Gates verboten.

**Rücknahmeprobe im Voraus.** Entsteht je ein Mechanismus gegen den Distanzkauf, werden
`tests/trust/test_distanzkauf.py` und `tests/trust/test_deckenelastizitaet.py` rot. Diese
Entscheidung ist damit nicht still zurücknehmbar: wer sie aufhebt, muss zwei Testdateien
anfassen und diesen Eintrag überschreiben.

**Nicht entschieden.** Ob `02 §4` einen normativen Satz über die Verwendung von
`Σ_{h ∈ Grenze} C(h)` erhält (D142, letzter Absatz). Der Fork ist geschlossen, diese Frage nicht.

### D144 — Die Prüfregeln bekommen eine Datei; sechs abgelöste Sitzungsstarts fallen

**Der Befund.** `sitzungsstart-decke.md` schrieb „die neunzehn aus den Vorsitzungen gelten
unverändert" und führte nur Regel 20 aus. Der Volltext der Regeln 1–19 stand **verteilt über
fünf abgelöste Sitzungsstart-Dateien**: sieben in `05`, drei in `anwendung`, drei in
`einlesepfad`, drei in `buchfuehrung`, eine in `kollision`. Das Register nennt sie nur als
Verweise. Der meistbenutzte methodische Bestand des Projekts hatte damit keinen Ort — er lag in
Dateien, deren einziger Zweck es ist, abgelöst zu werden.

Das ist kein Aufräumproblem. Ein Aufräumen ohne diesen Befund hätte die Regeln gelöscht, und
zwar in einem Commit, dessen Nachricht „abgelöste Sitzungsstarts entfernt" gelautet hätte.

**Entschieden.** Neue Datei `pruefregeln.md` mit den Regeln 1–21 im Volltext, thematisch
gruppiert nach dem Zeitpunkt, an dem sie greifen, mit der Nummer als stabilem Bezeichner. Sie ist
der einzige Ort ihres Volltextes. Ein `sitzungsstart-*.md` **verweist** künftig darauf und
wiederholt ihn nicht; neue Regeln entstehen weiter aus Befunden und wandern von dort in diese
Datei.

**Nummern 8 und 9 vergeben.** Parallelenprüfung und Begründungsprüfung liefen seit
`sitzungsstart-05.md` unnummeriert als „die beiden älteren" mit. Ohne Nummer waren sie in
Prompts nicht zitierbar, und beide sind laufend im Gebrauch. 8 ist die Parallelenprüfung, 9 die
Begründungsprüfung.

**Regel 21 ist neu** und stammt aus D142: eine Kapazität ist eine Schranke, kein Ertrag.

**Löschung geprüft, nicht angenommen.** Nach Prüfregel 17 ist eine Datei normativer Text, solange
Code oder Spec auf sie zeigt. Gegrept über alle `*.py` und `*.md` außerhalb der
`sitzungsstart-*`-Familie und außerhalb von `.venv`: **keine einzige Fundstelle**. Damit fallen
`sitzungsstart-03.md`, `-05.md`, `-anwendung.md`, `-buchfuehrung.md`, `-einlesepfad.md` und
`-kollision.md`. `sitzungsstart-decke.md` fällt mit dem Schreiben seines Nachfolgers.

**Was mit den Dateien verlorengeht — benannt, nicht behauptet.** Die Abschnitte „Was die letzte
Sitzung gelehrt hat" sind Erzählung, nicht Regel; was daran trug, ist entweder in eine Regel
geworden oder steht in einem Registereintrag. Was in keinem von beidem steht, war nicht wichtig
genug, es dorthin zu schaffen — das ist die Aussage dieses Eintrags und nicht ihr Nebeneffekt.
Wer sie doch braucht, findet sie in der Historie.

### D145 — Das Genesis wird in `04` geglaubt, nicht nachgerechnet

**Die Lage.** `decide()` liest `genesis_obj[5]` (Schwellenklasse) und `genesis_obj[6]`
(Gewichtungsmodus) und rechnet nie nach, dass
`SHA-256(DOM_NUC_GEN ‖ cbor(genesis_obj)) == epoch.scope`. `resolve_policy` rechnet genau das
nach, mit ausformulierter Begründung in `03 §1.2`: der Resolver rechnet nach statt zu glauben,
sonst wäre die Content-Adressierung eine Behauptung.

**Die Fehlerform — Prüfregel 18, mit dem Beweis im selben Abschnitt.** `04 §3` schreibt den
allgemeinen Satz selbst: „Dann die Objektidentitäten, vor jedem Zugriff auf ihren Inhalt." Die
darunterstehende Tabelle führt zwei Objekte, beide Verfassungen. Das Genesis fehlt in der
Aufzählung, obwohl der Satz es erfasst — und der Code ist der Aufzählung gefolgt, nicht dem
Satz. Zugleich Prüfregel 9: die Begründung aus `03 §1.2` ist an keine Eigenschaft von `03`
gebunden, sie gilt für jeden Leser eines Genesis. Sie ist beim Übergang nach `04` nicht
mitgereist.

**Die Wirkung liegt beim Konsumenten, nicht am Ort des Defekts** (Prüfregel 16). `genesis[5]`
wählt die Schwellenklasse. Ein nicht gebundenes Genesis mit `[5] = 0` lässt eine
Verfassungsänderung mit der `ordinary`-Schwelle ratifizieren — genau der Routine-Capture, gegen
den `00 §6.2` die `amendment`-Schwelle setzt. `[6] = 0` erlaubt Kopfzahl-Auszählung in einem
Nukleus, der gewichtet abstimmt. Beide Wege enden in `RATIFIED`, wohlgeformt und ohne Vermerk.
Das ist die stille Variante: nicht ein Fehler, der auffällt, sondern eine Entscheidung, die
falsch fällt und richtig aussieht.

**Beschluss: `ValueError`, unmittelbar nach der Scope-Prüfung.** Kein Vermerk, kein zwölfter
Code. Die Begründung ist die Asymmetrie aus `03 §1.2`: ein falsches Genesis ist eine falsche
Zuordnung — der Zustand ist nicht unvollständig, sondern falsch, und dafür gibt es keine sichere
Voreinstellung. Eine fehlende Verfassung ist Teilwissen und behält ihren Vermerk. `decide` wirft
bereits an dieser Stelle für `proposal.scope != epoch.scope`; die neue Prüfung ist derselbe Typ
und steht daneben.

**Verworfen — ein Vermerk `GENESIS_MISMATCH`.** Er behauptete, der Zustand sei auswertbar und
nur unvollständig. Er ist nicht unvollständig. Ein Vermerk gäbe `decide` außerdem einen
Rückgabewert für eine Lage, in der keine der gelesenen Zahlen einem Nukleus zurechenbar ist —
eine Auszählung ohne Nukleus.

**Zwei Golden-Anchor-Vektoren konstruieren eine unmögliche Lage.** `GV-24` und `GV-29` mutieren
`GENESIS_D` und übergeben das Ergebnis an eine Epoche mit `N_D`; das mutierte Genesis hat einen
anderen Hash. Nach dieser Entscheidung ist das kein zulässiger Zustand mehr. **Die
Erwartungswerte bleiben unverändert** — beide Befunde sind weiterhin erreichbar, über ein eigenes
Genesis mit eigenem Scope und eine Epoche darauf; `STOCK_GENESIS` mit `[6] = 1` und `STOCK_N` ist
genau diese Bauform und liegt bereits im Fixture. Geändert wird die Konstruktion, nicht die
Erwartung. Wäre eine Erwartung zu ändern, wäre das der Abbruchgrund und nicht der nächste
Schritt.

**Nicht repariert: `threshold_class`.** Sie ist exportiert, liest `genesis_obj[5]` ungeschützt
und wird in `tools/example_nucleus.py` direkt aufgerufen, wo `decide`s Indexprüfung nicht greift.
Eine eigene Prüfung dort brächte die zweite Implementierung derselben Regel zurück, die D111
gerade beseitigt hat. Die Vorbedingung gehört in den Docstring, nicht in den Code.

**Offen, eigener Fork: `trust_params`.** `trust/params.py` trägt `TrustParams` eigenständig,
`00 §4` Key 9 deklariert dieselben Zahlen unveränderlich im Genesis, und nichts gleicht sie ab.
D35 verlangt Unveränderlichkeit von `D`, weil `n/D` in jeder Vouch-Signatur steckt. Dieselbe
Klasse wie dieser Eintrag, anderer Layer — nicht in diesem Lauf.

### D146 — Regel 14 zum dritten Mal, und eine neue Regel 22

**Zwei Prompt-Defekte im Lauf zu D145.** Der Prompt nannte `passed()`, die Funktion heißt
`reached()`. Und er behauptete, `_tally` habe einen Importeur außerhalb seiner Datei; es waren
zwei, und `test_invariants.py` wäre ohne die Meldung des Werkzeugs rot geworden.

**Der zweite ist kein neuer Befund.** Regel 14 sagt bereits, dass eine Aufzählung von Fundstellen
gegrept und nicht gelesen wird, und führt zwei Präzedenzen: D119 nannte einen Erzeuger, es waren
drei; D127 nannte vier Kettenfortführungen, es waren fünf. „Ein Importeur, es waren zwei" ist der
dritte Fall derselben Regel. Ihn zum Anlass einer neuen Regel zu nehmen, hätte die bestehende
verwässert und den eigentlichen Punkt verdeckt: die Regel stand, sie wurde nicht angewandt.

**Ein Zusatz zu 14 trägt trotzdem.** Die Behauptung stammte aus einem `head -20`, das genau
zwanzig Zeilen zurückgab. Eine Ausgabe an der Grenze ihres Limits sieht aus wie eine
vollständige, und darin unterscheidet sie sich von einem leeren Ergebnis, das sich selbst
anzeigt. Deshalb: ein Limit, das exakt erreicht wird, ist ein Nulltreffer.

**Der erste Defekt ist neu.** Ein Bezeichner ist keine Aufzählung. `passed()` entstand daraus,
dass der Rumpf der Funktion gelesen und die `def`-Zeile ergänzt wurde — und ein Funktionsrumpf
ohne seine Signatur sieht nicht abgeschnitten aus. Dagegen hilft keine Zählregel, sondern nur die
Herkunft: **Regel 22**, Namen und Signaturen im Prompt werden übernommen, nicht rekonstruiert.

**Auch nicht „Modulcode vor Prompt".** Der Modulcode war gelesen. Gelesen und vollständig gelesen
sind zwei Zustände, und die Differenz war beide Male unsichtbar.

**Zur Fehlerform.** Der Supervisor war in dieser Sitzung wie in der vorigen die Fehlerquelle, und
beide Male hat das Werkzeug gemeldet statt still anzupassen. Das ist die Bedingung, unter der ein
falscher Prompt billig bleibt — keine Erlaubnis, ihn falsch zu schreiben, aber die Erklärung
dafür, warum der Schaden ein Nachlauf war und kein Defekt in `main`.

**Offen, aus D145 mitgenommen: die Genesis-Felder haben keinen gemeinsamen Durchgang.**
`[5]`/`[6]` waren ungebunden und sind es nicht mehr. `[4]` ist an die Epochenkette nicht gebunden
— `GV-24` führt ein Genesis, dessen deklarierte Verfassung in der Auszählung nirgends vorkommt.
`[9]` hat mit `trust/params.py` eine zweite Quelle ohne Abgleich, obwohl D35 Unveränderlichkeit
von `D` verlangt, weil `n/D` in jeder Vouch-Signatur steckt. `[1]`, `[2]`, `[3]` und `[7]` haben
gar keinen Träger. Das ist einmal zu beantworten und nicht viermal: welches Feld hat einen
Träger, und woran ist er gebunden. Der Durchgang steht vor `00a`, weil `root_keys` eines der
trägerlosen Felder ist.

### D147 — Die Kalibrierung bekommt einen Herleitungsort, die Rechnung bleibt parametrisiert

**Die Lage.** `TrustParams` trägt `C0`, `gamma_num`, `gamma_den`, `D` — feldgleich mit
`genesis[9]` nach `00 §4`. Nichts gleicht beide ab. `derive`, `trust` und `rank` nehmen die
Parameter vom Aufrufer entgegen; `tools/sim/szenario.py` und `tools/example_nucleus.py` tippen
sie als Literale. D35 verlangt Unveränderlichkeit von `D` über die Lebensdauer eines Scopes,
weil `n/D` in jeder signierten Vouch steckt. Ein Leser kann heute mit einem anderen `D` rechnen
als der Scope deklariert, und nichts zeigt es an.

**Zweitens, kleiner:** `TrustParams.__post_init__` prüft dieselben Wohlgeformtheitsbedingungen
wie `00 §4.0`, in eigener Formulierung. Sie stimmen heute überein — `C0 > 0` und `C₀ >= 1` sind
über `int` dasselbe, ebenso `0 < γ_num < γ_den` und `1 <= γ_num < γ_den`. Zwei Orte, eine Regel:
notiert, nicht zusammengelegt, weil eine Zusammenlegung `params.py` an die Spec-Prosa binden
würde statt an ein Objekt.

**Die Literaturprüfung hat den Fork aufgelöst, statt ihn zu entscheiden** (Prüfregel 15). Die
Frage war, was ein Verifizierer ohne Genesis tun soll. Zwei Familien antworten:

| System | Bauform | Antwort bei fehlender oder abweichender Quelle |
|---|---|---|
| TUF | Trust Anchor out-of-band, alles Weitere aus signierten Metadaten | Schwellen nie aus Client-Konfiguration; abgelaufenen Metadaten wird nicht vertraut |
| go-ethereum | Genesis trägt nur einen Teil der Chain-Spec, der Rest liegt im Client | `CheckCompatible` meldet `ConfigCompatError` mit Rückspulpunkt, kein Vermerk |
| Web-PKI (OCSP) | Widerrufsstatus wird online geholt | Soft-Fail — und er ist wirkungslos, weil der Angreifer den Kanal hält |

**Ethereum ist derselbe Fall, nicht nur ein ähnlicher:** dass die Parameter teils im
content-adressierten Anker und teils in der Implementierung stehen, ist dort die benannte Ursache
dafür, dass zwei Clients dasselbe Netz verschieden sehen. Genau diese Lücke hatte MaR.

**Die Web-PKI liefert die Begründung dafür, warum ihre eigene Antwort hier nicht gilt.** Der
Soft-Fail existiert, weil ein Responder ausfallen kann und ein Hard-Fail dann funktionierende
Verbindungen bricht. Ein Genesis ist kein Responder: unveränderlich, klein, content-adressiert,
und über `N` in jedem Claim referenziert. Die Antwort der Praxis auf den Soft-Fail war Stapling
und Mitliefern — die Information reist mit, statt nachgeschlagen zu werden. In MaR ist das der
Normalfall und nicht die Verschärfung; D121s Bündel trägt die Objektmap bereits.

**Beschluss: `resolve_trust_params` in `mensch_als_republik/trust/params.py`.** Signatur und
fünf Lagen stehen in `02 §8.1`. Die Bindungsprüfung ist die aus D145, mit derselben Begründung
aus `03 §1.2`: ein falsches Genesis ist eine falsche Zuordnung, kein Teilwissen.

**Der eigentliche Defektfall ist die dritte Lage** — Schlüssel 9 vorhanden **und** abweichende
Parameter übergeben. Nur dort behauptet jemand zwei verschiedene Kalibrierungen für denselben
Scope, und nur dort kann eine Vouch still umbewertet werden. Die anderen vier Lagen sind
Nebenwirkungen einer sauberen Signatur.

**Verworfen — `derive` bindet das Genesis selbst.** Das zöge ein Objekt in Layer 02, das Layer 02
nie brauchte, und machte den Trust-Graphen ohne Nukleus unrechenbar. Die Naht aus `03 §1.2` ist
billiger und bereits erprobt.

**Verworfen — Rückgabe eines Vermerks statt einer Ausnahme.** Ein Trust-Score, der unter
bestrittener Kalibrierung entstanden ist, ist keine schwächere Aussage, sondern eine über einen
anderen Scope. Und `02 §7` verlangt, dass fehlendes Wissen ein Ergebnis nur **senkt**; ein
falsches `C₀` senkt nicht, es verschiebt — dieselbe dritte Richtung, die D120 für den Autor über
seine eigene Kette gefunden hat.

**Nicht entschieden: `anchor_set` (`genesis[3]`).** Nach TUFs Trennung ist es der Trust Anchor
und nicht ein abgeleiteter Parameter; `02 §6.3` führt es ausdrücklich als out-of-band etabliert.
Wer bewusst mit einer Teilmenge der Anker rechnet, tut nichts Falsches. Bleibt ungebunden, als
benannte Grenze und nicht als Versehen.

**Offen: `D >= C₀` ist ein SHOULD in `00 §4.0` und `02 §8` und wird nirgends geprüft.** Kein
Defekt — ein SHOULD erzwingt nichts —, aber ein Kandidat für einen Vermerk, sobald es einen Ort
gibt, der ihn trägt.

### D148 — Prüfregel 23: die Rücknahmeprobe setzt an der ungeschützten Seite an

**Der Vorgang.** Der Nachlauf zu D147 sollte feststellen, dass `genesis_res[9]` und das
`TrustParams`-Literal im Beispielnukleus dieselben vier Zahlen tragen. Die Rücknahmeprobe im
Prompt lautete: eine Zahl in `genesis_res[9]` ändern und bestätigen, dass der Test rot wird. Er
wurde rot — mit der Meldung `N_res: got …, expected …`, also aus dem Bestandsanker in `build()`
und nicht aus dem neuen Test. Eine Änderung an `genesis_res` ändert den Scope, und den prüft der
Beispielnukleus seit Layer 04.

**Die beiden Seiten waren ungleich bewacht.** `genesis_res[9]` hängt am Hash und damit an einem
Golden Anchor. `ExampleNucleus.params` hängt an nichts. Der neue Test existiert für die zweite
Seite, und die Probe hatte die erste angefasst.

**Die Wiederholung an der richtigen Seite hat gegriffen:** `D=100` auf `D=99` im Literal ergibt
`ValueError: out_of_band does not match genesis trust_params`, sechs andere Tests bleiben grün.
Der Test ist damit berechtigt und der Nachlauf gut.

**Beschluss: Prüfregel 23.** Vor jeder Probe die Frage, was außer dem geprüften Test hier noch
rot werden könnte; die Antwort muss „nichts" sein.

**Abgegrenzt gegen Regel 21.** Deren Zusatz aus D142 betrifft die **unmögliche** Probe: ein von
der Spec als redundant bewiesener Term lässt sich nicht rot färben. Hier war die Probe möglich
und hat gefärbt — nur aus fremder Ursache. Unmöglich gegen zweideutig; die zweite Form ist die
gefährlichere, weil sie wie eine Bestätigung aussieht.

**Zur Fehlerform.** Die Meldung nannte `N_res` und einen Ankerwert, also einen Test, den es
vorher schon gab. Die Diagnose war ohne zweiten Lauf möglich; der Supervisor hat das Rot als
Bestätigung durchgewinkt, statt die Meldung zu lesen. Der Bericht des Werkzeugs war korrekt und
vollständig — er hätte die Frage beantwortet, wenn sie gestellt worden wäre. Das ist die
Umkehrung der bekannten Regel: nicht der Bericht ersetzt das Lesen nicht, sondern **das Rot
ersetzt das Lesen nicht**.

**Nachtrag zum eigenen Splice, gleiche Sitzung, gleiche Klasse.** Der erste Anlauf dieses
Eintrags scheiterte am Endanker: der Supervisor hatte den Schlusssatz von D147 aus dem eigenen
Entwurf rekonstruiert statt aus der Datei abgelesen, und der Zeilenumbruch lag anderswo als
erinnert — Prüfregel 22, eine Runde nach ihrer Einführung. Der Trockenlauf verdeckte es, weil die
Schlusszeile für die Simulation von Hand getippt worden war. Daraus die operative Fassung: **eine
selbst getippte Ankerzeile prüft den Anker nicht.** Ein Anhang ans Dateiende braucht überhaupt
keinen Prosa-Anker; die tragende Vorbedingung ist, dass der letzte Registereintrag der erwartete
ist, und die lässt sich ohne Zitat prüfen.

### D149 — Die Schwellenfrage war bereits verortet; `00a` ist kleiner als vermutet

**Der Anlass.** Vor der Design-Runde zu `00a` standen vier vermeintliche Forks: das
Gegenzeichnungsprädikat kodieren, „die längste Kette" bei mehreren `root_keys`, ein uhrfreier
Effektivpunkt der Governance-Rotation, und der Befund, dass `rotate-key@1` mit
`J = [identity, K_n]` nicht ausdrücken kann, was mit den übrigen Schlüsseln geschieht. Drei davon
sind keine.

**`00 §7` hatte die Frage gestellt und beantwortet.** Wörtlich: `∈` ist Mengenzugehörigkeit und
für jede Mächtigkeit definiert; bei mehreren autorisierten Schlüsseln genügt einer; und ob ein
Nukleus stattdessen eine Schwelle verlangen können soll, ist **nicht entschieden und wäre ein
Verfassungsknopf nach §4, kein Protokolldefault**. Der Supervisor hat diese Verortung über eine
`08 §3`-Prüfung und drei Literaturrecherchen neu hergeleitet, statt den Absatz zu lesen — obwohl
`§6` und `§7` als gelesen geführt wurden. Prüfregel 22 in ihrer teuersten Form: nicht ein
falscher Bezeichner, sondern ein übersprungener Absatz, und die Kosten waren eine ganze
Sitzungshälfte.

**Die `08 §3`-Prüfung bestätigt die Verortung** und braucht keine Auslegung: die Bestandstabelle
führt „Schwellenwerte, Arbitratorenlisten, Ressourcengrenzen" bereits unter Policy. Die Spec ist
darin konsistent — `genesis[5]` ist ein **Index auf eine Klasse**, die Ratios selbst stehen in der
Verfassung. Dieselbe Trennung, die für die Autorität gesucht wurde, ist eine Ebene tiefer schon
gebaut. Damit entfällt auch die Spannung, an der die Runde hing: eine Schwelle im unveränderlichen
Genesis wäre für immer festgeschrieben, in der Verfassung ist sie per `amendment` änderbar.

**Was für `00a` folgt.** `resolve_current_key` liefert eine **Menge**; `|root_keys| = 2` bedeutet
zwei parallele Ketten, deren Köpfe beide darin landen. Es gibt keine Auswahl zwischen
konkurrierenden Ketten zu treffen, weil jede Rotation den Schlüssel **ihres eigenen Autors**
ersetzt — Konkurrenz entsteht nur innerhalb einer Wurzel, und das ist Equivocation, die Layer 01
seit jeher führt. `J = [identity, K_n]` ist damit korrekt und nicht defekt, und die
Gegenzeichnung bleibt ein einzelner Claim. Offen bleibt allein das Gegenzeichnungsprädikat
(D125, Belegung) und der uhrfreie Effektivpunkt der Governance-Rotation.

**Die Literatur, damit sie nicht ein zweites Mal gesucht wird** (Prüfregel 15):

| Quelle | Befund | Trägt für MaR |
|---|---|---|
| TUF-Spec, Root-Rolle | mehrere Schlüssel **plus** Schwelle; ein Angreifer unterhalb der Schwelle kompromittiert nichts; jeder Schlüssel zählt einmal | ja — die Kette ab einem out-of-band-Anker ist normativ, kein Vorschlag |
| TUF TAP 8 | Rotate trägt Menge **und** Schwelle, dazu Zyklusprüfung und Selbstwiderruf per Selbstschleife | **nein** — seit 2017 nicht angenommen, TAP 20 legt einen Teil neu auf, und TAP 8 erklärt ausdrücklich, den Root-Fall nicht anzufassen |
| did:plc | `rotationKeys` nach Autorität geordnet; ein höherrangiger Schlüssel überschreibt Historie **innerhalb von 72 Stunden** | nein — die Rangordnung ist uhrfrei, das Fenster nicht, und ohne Fenster bleibt ein Altschlüssel dauerhaft mächtig (D125 hat das verworfen) |
| Web-PKI, Soft-Fail vs. Hard-Fail | Soft-Fail ist wirkungslos, wo der Angreifer den Kanal hält; die Antwort der Praxis war Mitliefern statt Nachschlagen | ja, als Begründung in D147 |
| go-ethereum | Parameter teils im content-adressierten Anker, teils im Client — die benannte Ursache dafür, dass zwei Clients dasselbe Netz verschieden sehen | ja, als Begründung in D147 |

**Ein Verweisdefekt, mitkorrigiert.** `00 §7` schrieb dem Beispiel-Nukleus in `§3.1` zwei
Wurzelschlüssel zu. `§3.1` und `04-golden-anchors.md` führen `[ALICE]`, also einen;
`example-nucleus.md` führt an zwei Stellen `[BRUNO, ANNA]`. Die Zahl stimmte, die Fundstelle
nicht. Nach Prüfregel 17 ist das schlechter als ein fehlender Verweis, weil er auf eine Stelle
zeigt, die das Gegenteil belegt. Der Verweis geht auf `example-nucleus.md`.

**Notiert, nicht entschieden.** `example-nucleus.md` führt damit eine **1-von-2-Autorität**: Bruno
und Anna dürfen jeder allein als der Nukleus handeln. Das ist nach `§7` zulässig und bewusst. Es
ist zugleich der erste Ort, an dem diese Bauform auf echte Menschen träfe, und damit der erste
Kandidat für den Verfassungsknopf, falls er je gebaut wird.

### D150 — Die Governance-Rotation bekommt einen Träger: `nucleus_keys` in der Verfassung

**Der Befund.** `00 §6.2` verlangt „ein `propose@1`/Abstimmung, dessen Payload den neuen
autorisierten Schlüssel deklariert". Diese Payload gibt es nicht. Das Vorschlagsobjekt
(`04 §2.4`) trägt genau drei Felder — `{0: scope, 1: predecessor, 2: constitution_hash}`, fest
kodiert in `governance/objects.py` — und das Verfassungs-Minimal-Schema (`00 §5`) trägt vier,
von denen keines einen Schlüssel aufnimmt. `§6.4` Schritt 3 war damit nicht bloß im
Effektivpunkt unterbestimmt; er verwies auf ein Objekt, das die Aussage nicht ausdrücken kann.

**Die Fehlerform ist die von D145.** Der allgemeine Satz existiert und ist richtig; die
Aufzählung darunter trägt ihn nicht. Gefunden nicht beim Lesen von `00`, sondern beim Lesen
von `objects.py` gegen `00 §6.2` — dieselbe Bewegung wie in D118.

**Beschluss.** Die Verfassung bekommt ein fünftes normatives Feld `nucleus_keys`
(`array[bytes32]`, optional). Fehlt es, gilt `genesis.root_keys`. Ist es gesetzt, **ersetzt** es
den Anker der Key-Chain (`00 §5.4`, `§6.4` Schritt 1).

**Begründung, in dieser Reihenfolge.**

1. Die Bauform steht schon da. `arbitration.arbitrators` ist bereits eine Autoritätsliste im
   Verfassungsobjekt: wer im Scope urteilen darf. `nucleus_keys` ist dieselbe Form für: wer als
   der Nukleus handeln darf. Kein neues Primitiv, und `08 §3` fällt eindeutig aus — die
   Bestandstabelle führt Autoritätslisten unter Policy.
2. Die Schwelle stimmt ohne Zusatzregel. `§6.2` verlangt die `amendment`-Schwelle; eine
   Verfassungsänderung **ist** diese Schwelle (`00 §5.3`, `04 §5`).
3. Der Effektivpunkt löst sich ersatzlos auf. Die Epochenkette ist über `predecessor` total
   geordnet und uhrfrei. Die Verfassung der jüngsten ratifizierten Epoche setzt den Anker neu,
   statt mit einem Kettenende verglichen zu werden. Der verbotene Vergleich zweier Ordnungen aus
   `§6.4` Schritt 3 entsteht nicht mehr — und die Frage, ob ein Rotate-Claim vor oder nach der
   Epoche liegt, entsteht ebenfalls nicht: ein Rotate eines nicht mehr genannten Schlüssels
   verliert seine Wurzel und wirkt nicht, unabhängig davon, wann er signiert wurde.
4. Kein Golden Anchor bricht. `proposal_hash` bleibt unverändert, `04`s Vektoren bleiben gültig.

**Verworfen — ein viertes Feld im Vorschlagsobjekt.** Ändert die CBOR-Kodierung von
`proposal_hash` und damit jeden Anker in `04-golden-anchors.md`. Außerdem trägt heute jeder
Vorschlag einen `constitution_hash`; ein Vorschlag ohne Verfassungsänderung ist nicht vorgesehen,
und eine Rotation ohne Verfassungsänderung wäre genau das.

**Verworfen — ein eigenes Profil `govern-rotate@1`.** Ein neuer Mechanismus für eine Aussage,
die ein bestehendes Objekt tragen kann. `08 §3`: keines von beidem, also nicht ins Protokoll.

**Neu und nicht vorgelegt: die leere Liste.** `nucleus_keys = []` bedeutet **keine** autorisierten
Schlüssel; Nukleus-Akte sind dann nicht autorisiert. Das ist die sichere Richtung, dieselbe wie in
`§6.4` Schritt 3 und `§9` („lieber kein gültiger Akt als ein falsch autorisierter"). Die
Gegenrichtung — leer wie fehlend behandeln, also zurück auf `genesis.root_keys` — lässt eine
Governance, die entmachten will, ins Leere laufen und lässt den alten Schlüssel mächtig. Der
Preis ist, dass eine Verfassung den Nukleus per Amendment handlungsunfähig machen kann. Das ist
ausdrückbar und wird nicht verhindert.

### D151 — `00a` baut die Key-Chain, `00b` den Verfassungsanker

**Beschluss.** Der Lauf `00a-rotate-key` baut `resolve_current_key` mit dem Anker als
**Parameter** und `rotate-key@1`/`rotate-ack@1` als Kettenmechanik. Das Bestimmen des Ankers aus
der jüngsten ratifizierten Epoche (D150) ist ein eigener Lauf `00b`.

**Begründung.** D150 zieht `00a` sonst in Layer 04 hinein — Epochenkette lesen, jüngste
ratifizierte Epoche bestimmen, `policy.py` um ein Verfassungsfeld erweitern — und diese Arbeit
teilt mit der Kettenauflösung nichts außer der Signatur. Die Entscheidung fällt trotzdem jetzt,
damit `00a` keine Signatur baut, die `00b` umbauen muss.

**Die Naht ist die bekannte.** `03 §4` nimmt `authorized_keys` als Parameter (D62),
`resolve_policy` trägt die Bindungsprüfung für die Verfassung (`03 §1.2`),
`resolve_trust_params` die für die Kalibrierung (D147). `resolve_current_key` nimmt den Anker
gleichermaßen als Parameter; das Herleiten des Ankers bekommt in `00b` seinen eigenen Ort.

**Getragene Grenze bis `00b`.** Ein vorgefundenes `nucleus_keys` wird nicht ausgewertet. Das ist
die **unsichere** Richtung — ein Leser vertraut weiter dem alten Schlüssel, obwohl die Mitglieder
ihn abgesetzt haben. Als benannte Grenze tragbar, als Schweigen wäre sie eine Lücke; derselbe
Satz und derselbe Grund wie beim „Zustand vor `00a`" in `§6.4`.

### D152 — Die Gegenzeichnung ist `nuc:N/rotate-ack@1`, ein vierteiliges Strukturprädikat

**Die offene Stelle aus D125.** `00 §6.1` sagt „ein Claim `C` mit `C.I == K_n`, der die
`claim_id` des Rotate nennt" und lässt die Feldbelegung offen.

**Der Satz ist zu weit.** Ein `core/revoke@1` mit `J = [claim-ref, claim_id(R_n)]`, signiert von
`K_n`, erfüllt ihn wörtlich. Eine Rücknahme als Zustimmung zu lesen ist nicht die abwegigste
Belegung, sondern die naheliegendste Fehlbelegung: `claim-ref` ist der Tag, den die
`core`-Prädikate ohnehin führen (`01 §5`).

**Beschluss.** Ein eigenes Prädikat, vierteilig nach dem Muster von D63:

```
ack.p  == nuc:N/rotate-ack@1
ack.J  == [claim-ref, claim_id(R_n)]
ack.I  == R_n.J.value    und   R_n.J.tag == identity
ack.N  == R_n.N
```

**Die vierte Bedingung ist nicht redundant** — dieselbe Begründung wie die dritte in D63.
`01 §2.2` Regel 3 erzwingt nur, dass `N` gesetzt und selbstkonsistent ist, nicht dass zwei Claims
denselben Scope teilen. Ohne sie zeichnet eine Ack aus Nukleus B eine Rotation in Nukleus A gegen.

**Trennende Vektoren für `00a`:** Ack vom Vorgängerschlüssel statt vom Nachfolger; Ack mit
fremdem `N`; Ack als `core/revoke@1` statt `rotate-ack@1`; Rotate, dessen `J.tag` `claim-ref`
statt `identity` ist.

### D153 — `rotate-key@1` und `rotate-ack@1` sind Protokoll-Default irrevocable

**Der Fall.** Wäre `rotate-ack@1` widerrufbar, könnte `K_n` die eigene Zustimmung
zurücknehmen und die Autorität spränge auf `K_{n-1}` zurück. Das ist der Zustand, den D125
unter „Verworfen — letzter gewinnt" ausgeschlossen hat, nur von der anderen Seite erreicht.
Dasselbe gilt für den Rotate selbst.

**Beschluss.** Beide Prädikate gehören in die Protokoll-Default-Menge der irrevocablen
Prädikate, neben `obligation@1` (`00 §5.2`, D70). `irrevocable_predicates` kann die Menge
weiterhin nur erweitern.

**Wirkungsprüfung (Prüfregel 16).** Der Träger ist `PROTOCOL_IRREVOCABLE` in `policy.py`, heute
`frozenset({"obligation@1"})`. Der Konsument ist `is_irrevocable`, aufgerufen aus der
Klassifikation; die Wirkung ist, dass ein `core/revoke@1` auf einen Rotate oder eine Ack ignoriert
und vermerkt wird. Die Erweiterung gehört in den `00a`-Lauf, nicht in diese Spec-Runde — sie ist
ohne Kettenmechanik nicht prüfbar.

**Getragene Grenze.** Ein Vertipper in der Ack ist nicht heilbar, sondern nur über die
Governance-Rotation (`§6.2`). Das ist derselbe Preis, den D125 für den Rotate bereits akzeptiert
hat, und dieselbe Bauform wie beim Schuldenschutz: ein Boden, keine Rückfallebene.

### D154 — Ordnung über die Autorenkette; der Kopf kann unter Wissenszuwachs zurückspringen

**Der Fall.** `K_{n-1}` signiert nacheinander `R_a` und `R_b` auf verschiedene Nachfolger mit
**verschiedener** `h_prev`. Das ist keine Equivocation (`§6.3` verlangt dieselbe `h_prev`), beide
sind nach der Kettenregel gültig, und D125 sagt: der **erste vollständige** bindet. Trifft
zuerst nur die Ack zu `R_b` ein, bindet nach lokalem Wissen `R_b`; trifft später die Ack zu `R_a`
ein, bindet `R_a`, und alle Akte des zwischenzeitlichen Kopfes verlieren rückwirkend ihre
Autorisierung.

**Beschluss.** „Erster" ist die Position in der eigenen Kette von `K_{n-1}` (`h_prev`), nicht die
Empfangsreihenfolge. Der Rücksprung wird **benannt** und getragen.

**Verworfen — erster nach Empfang.** Zwei Leser mit demselben Claim-Bestand kämen zu
verschiedenen Ergebnissen. Das ist schlechter als Nicht-Monotonie: nicht reproduzierbar statt
revidierbar.

**Die Klasse ist bekannt.** Mehr Wissen revidiert einen Zustand — dieselbe Lage wie nachträglich
entdeckte Equivocation, Detect-not-Prevent (`01 §A3`, `02 §7`). Neu ist nur, dass sie hier die
Autorität trifft und damit indirekt jeden Nukleus-Akt.

**Ein defektes Kettenglied blockiert nichts.** Eine ungültige oder unvollständige Rotation ist
schlicht kein Nachfolger; der Kopf bleibt beim letzten vollständigen Glied. Der Betriebsschaden
der TUF-Referenzimplementierung — eine ungültige Version blockierte alle folgenden dauerhaft —
setzt eine lückenlos versionsnummerierte Kette voraus. Die Kette hier ist autorverkettet und hat
diese Voraussetzung nicht. Damit ist der dritte offene Punkt aus dem Sitzungsstart keiner.

**Ebenfalls erledigt: „folge der längsten Kette".** Nach D149 gibt es nichts zu maximieren; der
Wortlaut fällt aus `§6.4` und wird durch „bis zum Schlüssel ohne vollständigen Nachfolger"
ersetzt.

### D155 — Vier Belegungen, ohne die `resolve_current_key` nicht rechenbar ist

Die vier Stellen fielen beim Lesen von `verifier.py` und `index.py` gegen `§6.4` an. Keine
folgt aus D150 bis D154; jede wäre sonst im Implementierer entschieden worden.

**(a) Zwei vollständige Rotationen desselben Autors, die nicht vergleichbar sind.** D154 ordnet
über die eigene Kette: bindend ist die frühere. Rechenbar ist das, indem geprüft wird, ob `R_a`
auf dem `h_prev`-Pfad von `R_b` liegt (`store.get(h_prev)` läuft rückwärts). Fehlt ein Glied
dazwischen im lokalen Bestand, liegt keine auf dem Pfad der anderen und die Ordnung ist
unbestimmt. **Beschluss: dann liefert diese Wurzel keinen Kopf**, wie bei Equivocation. Die
Alternative — irgendeine nehmen — wählt eine Autorität aus Unwissen.

**(b) Welcher Zustand zählt.** **Beschluss: Rotate und Ack müssen `ACTIVE` sein**, wie die vierte
Bedingung in D63 („beide aktiv"). Kein neuer Satz, nur die Übernahme des Präzedenzfalls. Damit
fallen `PENDING` (Vorgänger unbekannt) und `EQUIVOCATION_FLAGGED` von selbst heraus.

**(c) `t_exp` auf Rotate oder Ack.** Heute nicht verboten. Wäre es wirksam, liefe eine Rotation
ab und die Autorität spränge zum Vorgänger zurück — dieselbe Nicht-Monotonie, aus der `01 §5.3`
bereits folgert, dass `core/*` sein `t_exp` ignoriert. **Beschluss: `EXPIRED` zählt bei diesen
beiden Prädikaten wie `ACTIVE`**, geprüft in `keys.py`. Das geht (b) vor.

Verworfen — eine Ignorierregel nach dem Muster von `01 §5.4`: ein Eingriff in eine eingefrorene
Schicht für einen Fall, den `00a` lokal erledigen kann. Die getragene Grenze: ein `t_exp` auf
einer Rotation bleibt sichtbar und wirkt woanders, nur nicht auf die Autoritätsauflösung.

**(d) Zyklen. Neu und nicht vorgelegt.** Rotiert `K_1` auf `K_2` und `K_2` zurück auf `K_1`, läuft
ein naiver Vorwärtslauf endlos. **Beschluss: der Lauf führt die Menge der besuchten Schlüssel;
trifft er einen bereits besuchten, liefert die Wurzel keinen Kopf.** Eine zyklische Kette ist
keine Nachfolge. TAP 8 hat für dieselbe Lage eine Zyklusprüfung vorgesehen (Literaturtabelle in
D149); übernommen wird die Prüfung, nicht der übrige Vorschlag.

**Zur Equivocation, die keine dieser vier ist.** `§6.4` Schritt 3 sagt: ist die Kette an einem
Punkt equivoziert, liefert die Wurzel keinen Kopf. Das gilt **unabhängig von Vollständigkeit** —
ein Equivocation-Paar aus zwei Rotationen ohne Gegenzeichnung blockiert ebenso. Andernfalls bliebe
im Diebstahlfall (`§6.3`) der kompromittierte Schlüssel selbst der Kopf, und die Entscheidung
fiele nicht an die Mitglieder. Das steht bereits in der Spec und wird hier nur ausgeschrieben,
weil der Zustandstest aus (b) allein es nicht leistet.

### D156 — Der Protokoll-Boden gilt auch ohne Policy ⚠️

**Der Befund**, aus der `00a`-Abnahme. `is_irrevocable(predicate, policy)` in `policy.py` gibt
`False` zurück, sobald `policy is None` ist — vor jeder weiteren Prüfung. Der Boden aus
`00 §5.2` und D70 hängt damit an der Anwesenheit einer aufgelösten Policy.

**Das widerspricht normativem Text.** `01 §5.4.1` sagt: fehlt das Verfassungsobjekt lokal
(Partition, noch nicht synchronisiert), gilt der Sicherheits-Default aus `00 §5.2`. Der Anker
`P-D` in `03-golden-anchors.md` schreibt genau das aus: `constitution_obj=None`, Ergebnis
trotzdem der Boden. Es wäre widersinnig, dass „gar keine Policy aufgelöst" weniger Schutz trägt
als „Verfassung fehlt".

**Die Wirkung trifft nicht nur die Rotationen.** Ohne Policy wirkt ein `core/revoke@1` auf eine
`obligation@1` — das Schulden-Lösch-Loch aus D57, das D70 auf der Verfassungsebene geschlossen
hat, eine Ebene höher wieder offen. Gefunden wurde es nur, weil `00a` einen zweiten Nutzer des
Bodens bekam; für `obligation@1` allein war es fünfzig Registereinträge lang unsichtbar.

**Beschluss.** `is_irrevocable` prüft bei `policy is None` gegen `PROTOCOL_IRREVOCABLE` statt
gegen nichts. Die übrigen Bedingungen — `nuc:`-Präfix, Profilname nach dem letzten Schrägstrich
— bleiben unverändert, ebenso D73 (Fehlpaarung bleibt laut) und D91 (scope-lokale Anwendung).

**Verworfen — `keys.py` fingiert sich eine Policy.** Der Lauf `0c3f9ad` hat
`NucleusPolicy(scope=scope)` konstruiert, um an der Stelle vorbeizukommen. Das Ergebnis war
richtig, die Bauform nicht: eine Funktion, die keine Verfassung kennt, erfindet eine, und der
Aufrufer kann die echte nicht mehr einspeisen. `resolve_current_key` bekommt stattdessen
`policy` als durchgereichten Parameter, dieselbe Naht wie `membership` in `03 §4`.

**Getragene Grenze.** Ein Aufrufer ohne Policy bekommt weiterhin nur den Boden, nicht die
erweiterte Menge der Verfassung. Das ist richtig so: mehr kann er ohne das Objekt nicht wissen.

### D157 — Die `03`-Anker zur wirksamen Menge werden nachgezogen, nicht die Tests gelöst

**Der Fall.** D153 macht die wirksame Menge dreielementig. `03-golden-anchors.md` schreibt sie in
`P-A` bis `P-E` als `{obligation@1}` aus. Der `00a`-Lauf hat die betroffenen Tests daraufhin
gegen `PROTOCOL_IRREVOCABLE` verglichen statt gegen die Ankerwerte. Damit prüft `P-B` — der
einzige Vektor, der D58 und D70 gleichzeitig stellt — nichts mehr: er vergleicht die Konstante
mit sich selbst.

**Der Prompt war schuld.** Das Nicht-Ziel „keine Änderung an den Golden Anchors irgendeiner
Schicht" war unerfüllbar, sobald D153 im selben Lauf steht. Die Wirkungsprüfung zu D153 hat
`is_irrevocable` als Konsumenten geführt und nicht gefragt, welche Datei die Menge **ausschreibt**.

**Beschluss.** `P-A` bis `P-E` tragen `{obligation@1, rotate-ack@1, rotate-key@1}`, der
`P-B`-Absatz entsprechend. Die Tests binden wieder an die Ankerwerte.

**Warum das kein nachgezogener Anker im verbotenen Sinn ist.** Die Regel lautet: keinen Anker
bewegen, um einen Test grün zu bekommen. Hier hat sich die **Norm** geändert (D153), und der
Anker war ihr Abbild. Der Unterschied ist prüfbar: ein verbotener Nachzug hat keinen
Registereintrag, der die Normänderung nennt. Dieser hat einen, und D153 steht vor dem Lauf.

**Nicht geändert: `01a-policy-prompt.md §5.1` und `03-prompt.md`.** Beide schreiben die Menge
ebenfalls aus, sind aber erteilte Aufträge und zum Zeitpunkt ihrer Erteilung richtig gewesen.
Sie bekommen eine Hinweiszeile auf D153, keine neuen Zahlen. Eine erteilte Vorgabe
umzuschreiben, damit sie heute stimmt, nimmt der Datei ihren Zweck als Beleg.

### D158 — Berichtigung der Begründung von D152: der Vektor ist die Quittung, nicht der Widerruf

**Der Beschluss von D152 bleibt.** Nur seine Begründung nannte einen Fall, den es nicht gibt.

D152 argumentierte, „ein Claim `C` mit `C.I == K_n`, der die `claim_id` nennt" sei zu weit, weil
ein `core/revoke@1` von `K_n` auf den Rotate von `K_{n-1}` ihn wörtlich erfülle. Ein solcher
Claim ist nicht einlesbar: `_check_foreign_lifecycle` wirft `FOREIGN_LIFECYCLE`, weil das Ziel
einen anderen Autor hat als der Widerruf (`01 §4`). Der Angriff war nicht konstruierbar, und der
`00a`-Lauf hat es beim Bauen des Vektors gemessen.

**Der tragende Vektor ist die Quittung.** Ein `nuc:N/receipt@1` von `K_n` mit
`J = [claim-ref, claim_id(R)]` erfüllt **alle vier** Bedingungen aus D152 — Autor, Ziel, Scope,
Zustand — und unterscheidet sich einzig in `p`. Er ist einlesbar, weil `receipt@1` kein
`core`-Prädikat ist und der Lifecycle-Test ihn nicht sieht. Damit ist die Notwendigkeit des
eigenen Prädikats schärfer belegt als vorher: die Belegung allein trennt nicht, erst der Name
tut es.

Dass ausgerechnet D63s Quittung die Form trifft, ist kein Zufall — D152 hat ihr Muster
übernommen, und zwei Prädikate mit gleichem Muster sind ohne Namensprüfung ununterscheidbar.

**Für `00a`:** Testlage 6 wird auf `receipt@1` umgebaut. Der Widerrufsvektor entfällt ersatzlos.

### D159 — M-5, C-1 und C-9 aus `01a` sind abgelöst; D156 trägt aus `00 §5.2`, nicht aus `§5.4.1`

**Zwei Dinge auf einmal.** Der `00a`-Nachtrag (`11658b4`) hat drei Bestandstests rot gemacht,
und keiner davon ist ein Kollateralschaden: alle drei schreiben aus, dass ohne Policy ein
Widerruf auf eine `obligation@1` wirkt.

| Vektor | Erwartung aus `01a` | unter D156 |
|---|---|---|
| `M-5` | `policy = None` ist nie irrevocable | Bodenprädikate sind es |
| `C-1` | Obligation + eigener Revoke, `policy=None` → `revoked` | `active` |
| `C-9` | abgelaufen und widerrufen ohne Policy → `revoked` | `expired` |

**Die Begründung von D156 war zu stark und wird berichtigt.** D156 stützte sich auf `01 §5.4.1`
(„fehlt das Verfassungsobjekt lokal, gilt der Sicherheits-Default"). Der Satz regelt den Fall
eines **fehlenden Objekts**, nicht den eines Aufrufers, der die Auflösung gar nicht beschritten
hat. Das ist nicht dasselbe, und die Gleichsetzung war ein Fehler.

**Der Beschluss trägt aus `00 §5.2`.** Die Menge heißt dort **Protokoll**-Default. Eine Menge,
die per Definition von keiner Verfassung abhängt, hinter einem Verfassungsparameter zu
verstecken, ist die Fehlform — unabhängig davon, was `§5.4.1` über Partitionen sagt. `P-D` ist
weiterhin ein Beleg, aber kein Beweis.

**`01a §3.3` hat die Frage nie sicherheitsseitig entschieden.** Der Wortlaut: kein Override, alle
Widerrufe wirken wie bisher, „das ist der Pfad, den alle bestehenden Aufrufer nehmen" — dazu die
Eingangszeile des Prompts, die Bestandstests grün halten wollte, weil `policy=None` „exakt die
heutige Semantik" sei. Das ist eine **Migrationsaussage** aus einem Schritt, in dem der Resolver
noch fehlte (`01a §4`: der Resolver kommt mit `03`, D72). Seit D72 gibt es ihn; M-5 und C-1
konservieren einen Übergangszustand, dessen Grund entfallen ist.

**C-1 ist der schärfste Beleg gegen sich selbst:** Obligation plus eigener Widerruf, ohne Policy,
Ergebnis `revoked`. Das Schulden-Lösch-Loch aus D57, als Vektor festgeschrieben.

**Verworfen — `policy=None` bleibt override-frei.** Dann müsste `resolve_current_key` eine Policy
verlangen, der Aufrufer müsste `resolve_policy` bemühen, und die Autoritätsauflösung hinge an der
Verfügbarkeit einer Verfassung — obwohl D153 die Rotationsprädikate gerade als
verfassungsunabhängigen Protokoll-Default gesetzt hat. Das zöge `00a` in genau das Layer 03/04,
das D151 herausgehalten hat.

**Beschluss.** Die drei Tests werden abgelöst und umbenannt; `..._never_irrevocable` kodiert die
alte Norm im Namen. Nach der Trennung aus D157 bleiben die Vektortabellen in
`01a-policy-prompt.md` unverändert stehen und bekommen eine Hinweiszeile: erteilte Aufträge sind
Belege, keine lebenden Erwartungswerte.

**Trennschärfe.** Die neuen Tests müssen belegen, dass ohne Policy **nicht** jeder Widerruf
wirkungslos ist, sondern nur der auf Bodenprädikate. Ohne einen Gegenvektor mit einem
Nicht-Bodenprädikat verkommt die Aussage zu „ohne Policy wirkt kein Widerruf", und das wäre
falsch in die andere Richtung.

**Zweite berichtigte Begründung in dieser Sitzung** (nach D158). Beide Male trug der Beschluss
und die genannte Stelle nicht. Ein Beschluss, dessen Begründung erst beim Widerspruch geprüft
wird, ist so weit gehärtet wie der erste Widerspruch reicht.

### D160 — Abschluss `00a`: gebaut, aber ohne Aufrufer

**Was steht.** `mensch_als_republik/keys.py` mit `resolve_current_key`, der Protokoll-Boden auch
ohne Policy (D156), die Rotationsprädikate im Boden (D153). 526 Tests, vierzehn Eigenschaftstests.
Vier Commits: `0c3f9ad` der Lauf, `11658b4` die Nachbesserung, `2ca9f51` die Ablösung der
`01a`-Vektoren, `768361e` die Verweiskorrektur.

**Die tragende Grenze: niemand ruft die Funktion.** `03 §4` nimmt `authorized_keys` weiterhin als
Parameter von außen entgegen; kein Produktivpfad im Paket füllt ihn aus der Kette. Die
Autoritätsauflösung ist damit rechenbar, aber unwirksam — ein Aufrufer, der eine veraltete Menge
übergibt, bekommt weiterhin ein veraltetes Ergebnis, wie `03 §5` es schon beschreibt.

Das ist **nicht** dieselbe Lage wie `FOREIGN_LIFECYCLE` ohne Produktivträger (D138). Dort wurde
ein Träger bewusst entfernt; hier ist einer neu entstanden und noch nicht angeschlossen. Die Naht
gehört zu `00b`: wer den Anker aus Genesis und Verfassung herleitet, ist auch der Ort, an dem
`authorized_keys` gefüllt wird.

**Zweite getragene Grenze.** Die Equivocation-Prüfung in `_head_from` sieht nur equivozierte
**Rotationen** eines Schlüssels, nicht eine an anderer Stelle gespaltene Autorenkette. `§6.4`
Schritt 3 sagt „die Kette", `§6.3` definiert nur den Rotationsfall. Ob eine Spaltung außerhalb
der Rotationen die Wurzel ebenfalls entwerten soll, ist offen und wird in `00b` entschieden.

**Der Supervisor war fünfmal die Fehlerquelle, das Werkzeug null mal.** Ein unerfüllbares
Nicht-Ziel (D157), zwei Begründungen, die den Beschluss nicht trugen (D158, D159), eine
mehrdeutig beschriebene Testlage, deren naheliegende Lesart am Prüfobjekt vorbeiging (Lage 11),
und ein `classify_all`-Aufruf ohne Policy im Prompt. Das Werkzeug hat jeden dieser Fälle gemeldet
statt still zu reparieren — auch den, den es umgehen musste, um den Auftrag überhaupt auszuführen.

Daraus zwei Prüfregeln:

**Prüfregel 24 — ein Nicht-Ziel, das eine beschlossene Norm verletzt, ist keines.** Vor jedem
„keine Änderung an X" wird geprüft, ob eine Norm desselben Laufs X zwangsläufig bewegt. In `00a`
stand D153 im selben Prompt wie „keine Änderung an den Golden Anchors irgendeiner Schicht"; das
Werkzeug hatte keinen Weg, beides zu erfüllen, und der einzige verbleibende war, die Tests von
den Ankern zu lösen. Ein unerfüllbares Nicht-Ziel erzeugt genau den stillen Umbau, den es
verhindern soll.

**Prüfregel 25 — die Begründung wird beim Beschluss geprüft, nicht beim Widerspruch.** Zweimal in
einer Sitzung hat ein Beschluss getragen und die genannte Stelle nicht: D152 nannte einen
Angriff, den `FOREIGN_LIFECYCLE` ausschließt, D156 einen Paragraphen, der einen anderen Fall
regelt. Beide fielen erst auf, als eine Messung widersprach. Für jede zitierte Stelle wird gefragt,
ob sie den Fall des Beschlusses regelt oder einen benachbarten — ein Beschluss ist nur so weit
gehärtet, wie seine Begründung geprüft wurde, und eine ungeprüfte Begründung sieht aus wie eine
geprüfte.

Der Anlass für 25 war im letzten Sitzungsstart als offen geführt: „ob das eine eigene Regel
braucht, ist beim nächsten Vorfall zu entscheiden — zweimal derselbe Fehlertyp war bisher das
Kriterium". Er trat zweimal in derselben Sitzung ein.

### D161 — Zuschnitt `00b`: der Anker wird hergeleitet, die Epochenkette nicht

**Befund.** Keine Funktion liefert die jüngste ratifizierte Epoche. `verify_ratification` prüft
**einen** Schritt und bekommt `epoch`, `proposal` und `tally` vom Aufrufer; die Kette baut
ausschließlich `tools/example_nucleus.py` von Hand (`Epoch(scope=…, index=1, …)`, dann `index=2`).
`00 §6.4` Schritt 1 sagt „die Verfassung der jüngsten ratifizierten Epoche" und versprach damit
eine Herleitung, die nirgends stattfindet.

**Beschluss.** Die Verfassung wird übergeben, nicht hergeleitet. Der Herleitungsort ist

```
resolve_authorized_keys(store, *, scope, genesis_obj, constitution_hash,
                        constitution_obj=None, now, policy=None)
    -> KeyResolution(keys: frozenset[bytes], findings: tuple[Finding, ...])
```

in `mensch_als_republik/keys.py`. Er rechnet Schritt 1 und reicht das Ergebnis als `anchor_keys`
an `resolve_current_key` weiter, das unverändert bleibt (D151). `scope` wird gegen
`SHA-256(DOM_NUC_GEN || cbor(genesis_obj))` nachgerechnet, `constitution_hash` gegen
`H(constitution_obj)`, sofern das Objekt übergeben wird; beide Abweichungen sind `ValueError`,
kein Vermerk — ein fehlzugeordnetes Objekt ist ein Aufruferfehler und keine Lage der Welt
(D82, D92, D109). Der Typ heißt nach dem, was er trägt: die aufgelösten Schlüssel, nicht den
Anker.

**Ein formwidriges `genesis_obj[1]` ist ebenfalls `ValueError`.** Fehlt der Schlüssel, ist der
Wert keine Liste, oder ist ein Eintrag nicht `bytes` der Länge 32, bricht die Auflösung ab. Der
Unterschied zu `nucleus_keys` (D163) ist der **Ort**: die Verfassung ist ein Fund der Welt, den
ein Leser vorfindet und dessen Defekte er ertragen muss; der Genesis ist das Objekt, aus dem
derselbe Aufrufer eine Zeile vorher den Scope gerechnet hat. Ein Defekt dort ist kein Fund,
sondern ein Widerspruch im eigenen Aufruf. Eine leere Liste ist kein Defekt und liefert einen
leeren Anker.

**Begründung.** `03 §4` hat denselben Fork bereits entschieden und begründet: „`constitution_hash`
ist Parameter, keine Auflösung … welche Version gilt, entscheidet die Ratifizierung … eine
Governance-Frage. Diese Schicht vergleicht byte-weise." `resolve_policy` und `membership` tragen
dieselbe Naht in derselben Signaturform. Eine dritte Bauform an derselben Stelle wäre genau die
Asymmetrie, nach der Prüfregel 8 sucht.

**Warum `constitution_hash` neben `constitution_obj` steht.** `genesis[4]` trägt die Verfassung
der **ersten** Epoche; nach einem Amendment weicht die geltende Fassung zulässig davon ab, und es
gibt lokal nichts, wogegen sie zu prüfen wäre. Der Hash ist deshalb Parameter und nicht aus dem
Genesis ableitbar. Er trägt zugleich das Subjekt des Vermerks aus D164 — dieselbe Rolle wie
`declared_hash` in `resolve_policy`.

**`membership` behält seinen Parameter.** `authorized_keys` intern aufzulösen bräche die normative
Signatur in `03 §4`; stünde beides im selben Prompt, wäre es ein unerfüllbares Nicht-Ziel nach
Prüfregel 24.

**Benannte Grenze: die Epochenkette bleibt ungebaut.** Wer `resolve_authorized_keys` eine veraltete
Verfassung übergibt, bekommt einen veralteten Anker. Das ist dieselbe Grenze, die `03 §4` für
`constitution_hash` schon trägt, und sie wandert mit dieser Entscheidung nicht weiter nach unten.

**Was „angeschlossen" hier heißen kann.** Im Paket ruft **niemand** `membership` auf; gegrept sind
die Aufrufer `tests/profiles/test_membership.py`, `tests/profiles/test_invariants.py`,
`tests/governance/test_vectors.py`, `tools/example_nucleus.py` (Zeilen 459 und 658) und
`tools/sim/szenario.py` (Zeile 221). Das Paket ist eine Bibliothek von Auflösern, komponiert wird
am Rand. Angeschlossen heißt deshalb: es gibt genau **eine** Stelle, die Schritt 1 rechnet, und der
Beispielnukleus benutzt sie. Dort steht heute `authorized_keys=frozenset()`, und die Mitgliedschaft
läuft über `participants`; die hergeleitete Menge ist `{BRUNO, ANNA}` aus `genesis_gov[1]` und
ändert am Zustand nichts. Die Wirkung liegt in der **Prüfung** der hergeleiteten Menge, nicht im
Durchreichen — ein falscher Schritt 1 fiele an der Mitgliedschaft dieses Nukleus nicht auf, weil
er kein `grant-membership@1` führt.

### D162 — Eine Spaltung der Autorenkette an beliebiger Stelle entwertet die Wurzel

**Messung.** `_is_in_equivocation_pair` prüft **den Claim** — Autor und `h_prev` —, nicht den
Autor. `_predecessor_known_and_valid` prüft nur, ob der Vorgänger vorliegt und denselben Autor
hat; ein geflaggter Vorgänger vererbt nichts. Nachfahren einer Spaltung sind `ACTIVE`. Damit
behält heute ein nachweislich verdoppelter Nukleusschlüssel seinen Kopf, und jedes
`grant-membership@1`, das er signiert, ist autorisiert.

**Beschluss.** Hat `k` irgendeinen Claim im Zustand `EQUIVOCATION_FLAGGED`, liefert `k` keinen
Kopf. Ohne Einschränkung auf Rotationen und ohne Einschränkung auf den Scope: die Autorenkette
ist identitäts- und nicht scopegebunden, eine Spaltung ist die Spaltung dieser Identität.

**Begründung.** `§6.3` unterstellt, der Diebstahl zeige sich an einer doppelten Rotation. Das ist
der **späte** Fall. Ein Dieb benutzt den Schlüssel für Akte, lange bevor er um eine Rotation
rennt, und solange beide Halter schreiben, entstehen Paare überall in der Kette. Die Regel „nur
Rotationen" deckt den auffälligen Angreifer und lässt den geduldigen durch.

**Was nicht trägt.** „D155 fängt das ohnehin" gilt nur, wenn zwei Rotationen auf verschiedenen
Zweigen liegen und dadurch unvergleichbar werden. Bei **einer** Rotation und einer Spaltung
anderswo greift D155 nicht — und das ist genau der Fall, um den es geht (Prüfregel 25).

**Preis.** Ein ehrlicher Nukleus, dessen Client einmal zwei Claims auf dieselbe Spitze schreibt,
verliert seine Autorität. Der Ausweg ist `§6.2`, derselbe wie beim Diebstahl, und die
Governance-Rotation braucht den Nukleusschlüssel nicht: `ratify@1` kommt aus `P`. Der Preis ist
also ein bereits vorhandener, erreichbarer Pfad und kein neuer Schaden.

**Richtung.** Monoton in der sicheren Richtung: mehr Wissen nimmt Autorität, gibt keine. Dieselbe
Klasse wie D154.

**Umsetzung.** Die neue Prüfung subsumiert die bisherige — eine equivozierte Rotation ist ein
Claim ihres Autors. Eine Änderung von `nucleus_keys` löst den Fall nicht dadurch auf, dass sie
denselben Schlüssel erneut nennt; sie löst ihn, indem sie einen anderen nennt.

**Literaturprüfung (Prüfregel 15).** Die Fork-Regel von Secure Scuttlebutt wäre der Präzedenzfall.
Eine Suche hat sie nicht belegt; sie wird deshalb nicht als Begründung geführt.

### D163 — Ein gesetztes `nucleus_keys` fällt nie auf den Genesis zurück

**Frage.** Was tut ein Eintrag in `nucleus_keys`, der kein `bytes32` ist.

**Der Bestand kennt beide Muster.** `irrevocable_predicates` verwirft eintragsweise und behält den
Rest (D95); `participants` in `profiles/membership.py` verwirft bei einem einzigen defekten Eintrag
die **ganze** Liste. Das Unterscheidungskriterium ist die sichere Richtung des jeweiligen Feldes,
nicht die Form.

**Hier ist sie eindeutig.** Die ganze Liste zu verwerfen hieße nach `§5.4` „Feld fehlt" und damit
`genesis.root_keys`. Ein einziges formwidriges Byte holte die abgesetzten Wurzelschlüssel zurück.
Das ist die Absetzungs-Umgehung und dieselbe Bauform wie das Schulden-Lösch-Loch aus D57 und D156:
eine Deklaration, die durch ihre eigene Fehlerhaftigkeit den Schutz aufhebt, den sie setzt.

**Beschluss.** Wohlgeformt ist ein Eintrag, der `bytes` der Länge 32 ist. Formwidrige Einträge
werden verworfen und vermerkt (`MALFORMED_NUCLEUS_KEY`), die übrigen bleiben wirksam. Duplikate
fallen wortlos zusammen: `nucleus_keys` bezeichnet eine Menge und ist keine Auszählungsgrundlage —
anders als `participants`, wo ein zu kleiner Nenner jede Schwelle senkt (D96). Eine
Sortierpflicht gibt es aus demselben Grund nicht.

**Ein gesetztes Feld fällt nie auf den Genesis zurück.** Sind alle Einträge formwidrig, oder ist
der Wert gar keine Liste, ist der Anker die **leere** Menge und die Nukleus-Autorität stillgelegt.

**Der Vermerk ist einer je Verfassung.** Subjekt ist `constitution_hash`, nicht der defekte
Eintrag — er ist im Allgemeinen kein `bytes` und passt nicht in `Finding.subject`. Mehrere
formwidrige Einträge erzeugen denselben Vermerk, den `dedupe_sort` zusammenzieht. Die Anzahl geht
verloren; das ist entschieden und kein Versehen.

**Der Preis steht schon in `§5.4`:** „Der Preis ist, dass eine Verfassung den Nukleus per Amendment
handlungsunfähig machen kann. Das ist ausdrückbar und wird nicht verhindert." Dieselbe Zeile trägt
den Tippfehlerfall mit, und der Ausweg ist `§6.2`.

### D164 — Die lokal unbekannte Verfassung ist nicht „die Verfassung nennt kein Feld"

**Befund.** `§6.4` Schritt 1 kennt zwei Lagen — das Feld ist genannt oder nicht. Es gibt eine
dritte: die Verfassung liegt lokal nicht vor. `resolve_policy` führt für sie
`CONSTITUTION_UNAVAILABLE`; im Anker fiel sie stillschweigend in denselben Zweig wie „nennt kein
Feld" und lieferte `genesis.root_keys` — genau die Menge, die eine Absetzung ersetzt haben könnte.
Prüfregel 25: der Satz, auf den man sich berief, regelt den Nachbarfall.

**Beschluss.** Genesis-Rückfall **mit Vermerk** `CONSTITUTION_UNAVAILABLE`, Subjekt
`constitution_hash`. Nicht die leere Menge.

**Begründung gegen die leere Menge.** `nucleus_keys = []` bedeutet seit D150 „die Mitglieder haben
abgesetzt" — eine Aussage. Unwissen als dieselbe Aussage zu kodieren wäre genau die Verwechslung,
die D163 an der anderen Flanke behebt. Der Vermerk trägt den Zweifel; ein Aufrufer, der Findings
als fatal behandelt, bekommt die sichere Richtung, ohne dass die Auflösung sie ihm aufzwingt.

**Damit hat Schritt 1 drei Lagen und nicht zwei.** Der Wortlaut wird nachgezogen.

### D165 — Abnahme `00b`: der Anschluss steht, der Satz über die Kette war verengt

**Was steht.** `mensch_als_republik/findings.py` mit `NucleusFinding`,
`resolve_authorized_keys` und `KeyResolution` in `keys.py`, die auf jede Spaltung erweiterte
Prüfung in `_head_from`, und im Beispielnukleus `check_anchor_resolution` samt `_member`, das die
hergeleitete Menge weiterreicht. Commit `1115281`, gemergt. **541 Tests** und **14**
Eigenschaftstests unter `voll`, kalt auf `main` gemessen. Die Tabelle aus
`tools/example_nucleus.py` ist bytegleich zum Stand davor.

**Befund 1: der neue Satz in `§6.4` Schritt 3 war enger als der alte.** Die abgelöste Fassung
sagte „ist die Kette von k **an einem Punkt** equivoziert"; meine Neufassung sagte „hat k
irgendeinen Claim". Der Code prüft — richtig, und schon vor `00b` — bei **jedem** Schlüssel, den
Schritt 2 auf der Kette erreicht, nicht nur beim Anker. Damit stand die Spec hinter dem Code, und
zwar in der sicheren Richtung, was den Fall nicht besser macht: ein Leser, der `§6.4` umsetzt,
hätte weniger gebaut als das, was gilt. **Der Satz wird mit diesem Eintrag berichtigt**, `00
§6.4` Schritt 3.

Daraus ein Zusatz zu Prüfregel 18: er galt bisher für Aufzählungen, die neben einem Satz stehen.
Er gilt ebenso für einen Satz, der einen älteren **ersetzt**. Der Geltungsbereich des alten wird
zuerst benannt und gegen den Code geprüft, der ihn umsetzt.

**Befund 2: zwei Nähte, zwei Fehlertypen, keine Notiz.** `resolve_authorized_keys` wirft bei
einer Hash-Abweichung `ValueError`, `resolve_policy` gibt an derselben Stelle
`CONSTITUTION_HASH_MISMATCH` als Vermerk zurück. Der Unterschied ist begründet und das Kriterium
ist, **wer den Hash geliefert hat**: `resolve_policy` zieht ihn selbst aus `genesis[4]`, eine
Abweichung ist dort eine Lage der Welt. Bei `resolve_authorized_keys` kommen Hash und Objekt
beide vom Aufrufer, eine Abweichung ist ein Widerspruch im eigenen Aufruf — dieselbe Behandlung
wie in `membership` (D82, D92, D109). Das steht hier, weil eine unbegründete Asymmetrie zwischen
zwei benachbarten Funktionen genau die Stelle ist, an der später jemand harmonisiert (Prüfregel 8).

**Der Supervisor war dreimal die Fehlerquelle, das Werkzeug null mal — zweite Sitzung in Folge.**
Der Prompt sagte „Elf Lagen" und zählte zwölf auf; Abnahmekriterium 4 nannte `python3` statt
`.venv/bin/python`; die Rücknahmeproben 2 und 3 nannten je einen roten Test, wo eine ganze Gruppe
dieselbe Aussage trägt. Das Werkzeug hat alle drei gemeldet und keinen still repariert. Die
Proben selbst haben getragen: jede hat den Test rot gefärbt, für den sie gebaut war, und die
zusätzlich roten hingen nachweislich an derselben Ursache.

**Getragene Grenzen nach `00b`.** Die Epochenkette bleibt ungebaut; wer eine veraltete Verfassung
übergibt, bekommt einen veralteten Anker (D161). `membership` bekommt `authorized_keys` weiterhin
von außen — neu ist, dass es genau **eine** Herleitungsstelle dafür gibt und der Beispielnukleus
sie benutzt. Ein Nukleus mit einem echten `grant-membership@1` würde den Anschluss zum ersten Mal
wirksam machen; der Beispielnukleus führt keines, und `check_anchor_resolution` prüft deshalb die
hergeleitete Menge selbst statt ihrer Wirkung.

### D166 — Autoritätslisten tragen keine Schwelle; die Frage wird umformuliert, nicht beantwortet

**Herkunft.** D126 ließ offen, ob ein Nukleus statt „einer genügt" ein `k`-von-`n` verlangen
können soll. D149 verortete die Frage in der Verfassung, D150 schuf mit `nucleus_keys` das Feld,
an dem eine Schwelle hinge.

**Befund: die Frage war falsch gestellt.** Es gibt drei Autoritätslisten, und alle drei sagen
dasselbe. `genesis.root_keys` und `nucleus_keys` über `§7` — „bei mehreren autorisierten
Schlüsseln genügt einer" —, `arbitration.arbitrators` über `§5.1`, wo ein `verdict@1` bindet,
sobald sein Autor in der Liste steht, ohne Zahl. Eine Schwelle nur für `nucleus_keys` wäre genau
die Asymmetrie, nach der Prüfregel 8 sucht: dieselbe Bauform, verschieden behandelt, ohne
benannten Grund. **Die Frage wird deshalb von `nucleus_keys` gelöst und auf alle drei Listen
gestellt.** Beantwortet wird sie einmal, oder gar nicht.

**Beschluss.** In v1 trägt keine Autoritätsliste eine Schwelle. `§7` wird auf diesen Stand
gezogen.

**Warum nicht jetzt.** Zwei Wege geben einem Nukleus heute `k`-von-`n`: `key_mode = 1` mit FROST
(`§6.5`) auf der Signaturebene, und der Governance-Pfad `propose`/`vote`/`ratify` gegen
`thresholds` (Gov-Spec §5). `grant-membership@1` unter dem Nukleusschlüssel ist die **Abkürzung**
für Nuklei, die keine Abstimmung fahren wollen; eine Schwelle darauf zu legen machte daraus eine
langsame Abstimmung mit weniger Maschinerie — eine zweite, schwächere Kopie von `04`.

**Was ein protokollseitiges `k`-von-`n` zusätzlich entscheiden müsste.** Die Bauform selbst ist
nicht fremd — `rotate-ack@1` (D152) und die Auszählung in `04` sind sie zweimal. Offen wären vier
Wechselwirkungen, jede eine eigene Entscheidung:

1. Ein Assent wird später widerrufen — fällt der Akt rückwirkend?
2. Ein Signierender equivoziert später und verliert nach D162 seine Autorität. Verliert der Akt,
   der bereits zählte, sie auch?
3. `nucleus_keys` schrumpft per Amendment unter `k`. Was gilt für Akte davor, was für danach?
4. Sind Assents scopelokal und fristgebunden, oder gelten sie unbefristet?

Das ist eine Schicht, kein Knopf.

**Der tragende Grund ist `08 §2.2`, nicht der Aufwand.** Es gibt keinen Nukleus, der die Frage
stellt. Ein Mechanismus ohne Kollisionsdichte ist Spezifikationstiefe, und die ist in diesem
Projekt der teurere Fehler.

**Die Gegenposition, ausdrücklich (Prüfregel 15).** TUF entscheidet an derselben Stelle anders:
jede Rolle trägt `keys` **und** `threshold`, `k`-von-`n` auf der Metadatenebene statt per
Schwellensignatur, und die Begründung dort ist, dass ein einzelner kompromittierter Root-Key
nicht allein handeln können soll. Das ist derselbe Bedrohungsfall, der D162 getragen hat. Ist
Diebstahl die Bedrohung, dann **ist** „einer genügt" die Lücke, und die Schwelle ist die
Standardantwort. Dazu kommt, dass FROST für zwei Gründer schwer ist — eine DKG-Zeremonie — und
dass `key_mode` im Genesis steht: später wechseln heißt neuer Nukleus. Der Beispielnukleus hat
heute genau diese Lage; jeder seiner zwei Gründer kann allein aufnehmen, und es ist nicht
belegt, dass sie das gemeint haben.

**Diese Zurückstellung ist deshalb kein erledigtes Nein.** Wer sie aufhebt, beantwortet sie für
alle drei Listen zugleich und entscheidet die vier Wechselwirkungen. Der Anlass, auf den zu warten
sich lohnt, ist der erste Nukleus mit mehr als einem Halter, der einen Diebstahl fürchtet — nicht
der erste, der die Schwelle hübsch fände.

**Zwei Nebenbefunde mitgezogen.** `§7` verwies für den Verfassungsknopf auf `§4`; das ist das
Genesis-Schema, die Verfassung ist `§5`. Und `§9` zählte „nur vier Verfassungsfelder" als
normativ; seit D150 sind es fünf, wie die Tabelle in `§5` schon zeigt.

### D167 — Die Auflösungskette in `03 §1.2` hatte keinen Epochenschritt

**Befund.** `03 §1.2` schreibt die Auflösung normativ als `C.N → Genesis → constitution_hash →
Verfassungsobjekt → irrevocable_predicates`. Diese Kette führt auf `genesis[4]`, und `genesis[4]`
ist nach `00 §4` der Hash der **initialen** Verfassung. `resolve_policy` setzt das genau so um:
ein Verfassungsobjekt, das nicht zu `genesis[4]` passt, ergibt den Boden und den Vermerk
`CONSTITUTION_HASH_MISMATCH`.

Gleichzeitig sagt `00 §5.3`, ein Verfassungsupdate erzeuge ein neues Objekt mit neuem Hash, und
die Ratifizierung sei die Re-Akzeptanz auf diesen Hash. `membership` honoriert das — im
Beispielnukleus wird DORA gegen `constitution_hash_2` gerechnet. **Derselbe Nukleus hatte damit
zwei geltende Verfassungen, je nachdem, welche Funktion man fragt.** Wer `resolve_policy` die
ratifizierte Fassung 2 übergibt, bekommt einen Vermerk, der behauptet, das Objekt gehöre nicht zu
diesem Nukleus. Es gehört dazu; es ist die aktuelle.

Der Beispielnukleus trägt die Frage bereits, ohne sie zu stellen: `_policy(ex)` baut die Policy
immer aus `constitution_gov`, auch für die Prüfungen der Epoche 2.

**Beschluss.** `constitution_hash` wird Parameter von `resolve_policy`, wie in D161 für den Anker
entschieden. Die Kette in `§1.2` bekommt den fehlenden Schritt: welche Fassung gilt, entscheidet
die Ratifizierung, nicht das Genesis. `genesis[4]` bindet die **Epoche 1** und wird von
`resolve_policy` nicht mehr gelesen.

**Verworfen — genesisgebunden lassen und `§5.3` einschränken.** Die Begründung wäre D35 gewesen:
läge `D` in der änderbaren Verfassung, würde ein Amendment Bestandssignaturen still umbewerten.
Sie trägt hier nicht. `D` steckt als `n/D` **in** jeder Vouch-Signatur; `irrevocable_predicates`
steckt in keiner Signatur, es wird beim Lesen angewandt. Prüfregel 25: die zitierte Begründung
regelt den Nachbarfall.

**Verworfen — monotone Vereinigung über die Epochenkette.** Wirksam wäre die Vereinigung aller
ratifizierten Fassungen; mehr Wissen fügte Schutz hinzu und nähme nie welchen. Das ist die
Designmonotonie dieses Projekts und parallel zu `§5.2`. Sie verlangt aber den Kettenlauf, den
D161 ausdrücklich nicht gebaut hat, und sie macht jede Fehldeklaration unwiderruflich — eine
Governance, die nichts zurücknehmen kann, ist die Capture-Fläche, die `00 §9` bei
`amendment_rule` vermeiden wollte.

**`CONSTITUTION_HASH_MISMATCH` entfällt ersatzlos.** Sind Hash und Objekt beide vom Aufrufer, ist
eine Abweichung ein Widerspruch im eigenen Aufruf und damit `ValueError` — dieselbe Behandlung wie
in `membership` und `resolve_authorized_keys` (D82, D92, D109, D161). Damit löst sich auch die in
D165 als Befund 2 notierte Asymmetrie auf: drei Nähte, eine Bauform.

Der Fall, den der Vermerk abdeckte, verschwindet nicht, er wandert: liefert ein Peer ein Objekt,
dessen Hash nicht zum erwarteten passt, **hat man die Verfassung nicht** — der Aufrufer übergibt
`None` und bekommt `CONSTITUTION_UNAVAILABLE`. Das ist die zutreffendere Aussage, weil sie den
Zustand des Lesers benennt und nicht die Zugehörigkeit eines Objekts.

**Was `genesis[4]` damit trägt.** Es ist der Hash, den ein Aufrufer in Epoche 1 übergibt. Das ist
sein Träger, und die in D146 als ungebunden notierte Grenze ist damit beantwortet — als
Nebenprodukt, nicht als Ziel. `GV-24` bleibt konstruierbar wie bisher; die Entscheidung berührt
die Auszählung nicht.

**Nicht in diesem Eintrag, eigene Frage:** ob ein Amendment ein in der Vorgängerfassung
deklariertes Prädikat **weglassen** darf. Heute entschützt es damit Bestandsclaims, und zwar
nicht sichtbar, sondern erst beim Widerruf. Das gehört an `04 §5` und hat mit dem Auflösungsort
nichts zu tun.

**Der Code folgt in einem eigenen Lauf.** `resolve_policy`s Signatur ist in `§1.2` normativ, und
rund fünfzehn Testaufrufstellen hängen daran. Die Spec geht voran, damit der Prompt „die Spec
steht" sagen kann, ohne nach Prüfregel 24 unerfüllbar zu werden.

### D168 — Ein Auflöser prüft, was er liest; die P-Vektoren folgen

**Was D167 nicht ausgesprochen hat.** Die Lagentabelle in `03 §1.2` führte eine Zeile „Genesis
ohne `constitution_hash` oder mit falschem Typ darin → `ValueError`". D167 hat sie gestrichen,
weil `resolve_policy` `genesis[4]` nicht mehr liest. Die Folge stand nirgends: **wer das Feld
nicht liest, prüft es auch nicht.** Ein Genesis ohne Key `4` ist nach `00 §4` defekt, aber das
festzustellen ist nicht Aufgabe dieses Auflösers — sonst stünde die Wohlgeformtheit aus `00 §4`
ein zweites Mal im Code, und genau das haben D111 und D147 abgeräumt.

**Die Regel, die dahintersteht.** `resolve_authorized_keys` prüft `genesis[1]` streng, weil es
den Wert liest, und prüft Key `4` überhaupt nicht (D161). `resolve_policy` prüft den Scope, weil
es das ganze Genesis hasht. Beide prüfen genau ihre Eingabe. Das ist kein Sparen an Sorgfalt: eine
Prüfung ohne Lesegrund ist eine zweite Kopie einer fremden Norm, und Kopien laufen auseinander.

**Zwei Vektoren in `03-golden-anchors.md` §4 werden nachgezogen.** `P-E` erwartete den Boden plus
`CONSTITUTION_HASH_MISMATCH` und erwartet jetzt `ValueError` — der Vermerk entfällt mit D167.
`P-G` erwartete `ValueError` für ein Genesis ohne Key `4` und erwartet jetzt das **normale**
Ergebnis; er ist damit der Vektor, der belegt, dass die Prüfung fort ist. Nachgezogen, weil die
Norm sich geändert hat, nicht um einen Test grün zu bekommen (D157). Wäre eine Erwartung zu
ändern gewesen, ohne dass eine Norm sie bewegt, wäre das der Abbruchgrund.

**`P-G` ist nach der Änderung kein Doppel von `P-A`.** Beide liefern den Boden ohne Vermerk, aber
`P-A` sagt „die Verfassung sagt es" und `P-G` sagt „das Genesis ist unvollständig und der
Auflöser stört sich nicht daran". Der zweite Satz ist die Aussage, die ohne diesen Vektor
niemand prüft.

**Zwei erteilte Prompt-Dateien bekommen Nachträge, keine Korrekturen** (D157-Konvention).
`03-prompt.md` führt die alte Lagentabelle und die alte Subjektregel; `03a-korrektur-prompt.md`
begründet ausdrücklich, warum ein Genesis ohne `constitution_hash` `ValueError` sei. Beide
bleiben im Wortlaut stehen — sie sind erteilt und ihre Zahlen waren zum Zeitpunkt der Erteilung
richtig —, und jede bekommt eine Zeile, die auf `03 §1.2` als normative Fassung zeigt. Nach
Prüfregel 17 sind sie normativer Text, solange Code auf sie zeigt; ein stiller Umbau erteilter
Prompts nähme jeder späteren Abnahme ihren Vergleichspunkt.

### D169 — Abnahme `03b`: der Epochenschritt steht, die Zählung war abgelaufen

**Was steht.** `resolve_policy` nimmt `constitution_hash` als Pflichtparameter, liest
`genesis_obj[4]` nicht mehr und wirft bei Hash-Abweichung `ValueError`.
`ProfileFinding.CONSTITUTION_HASH_MISMATCH` ist entfernt, zwanzig Aufrufstellen sind ergänzt,
`P-E` und `P-G` sind nachgezogen, `P-H` ist neu, und `_policy` im Beispielnukleus geht durch den
Auflöser statt die Policy von Hand zu bauen. Commits `fd408dd` und `c6d63e4`, gemergt. **542
Tests** und **14** Eigenschaftstests unter `voll`, kalt auf `main` gemessen. Die Tabelle aus
`tools/example_nucleus.py` ist bytegleich zum Stand davor.

**Befund 1: eine Zahl im Prompt war nicht falsch getippt, sondern abgelaufen.** Der Prompt nannte
sechs `_policy`-Aufrufstellen; gemessen waren es zehn. Die Zahl stammte aus einem `grep` über die
Projektkopie, und die Kopie hing auf `c32b6e6` — dem Stand **vor** dem `00b`-Merge, der
`check_anchor_resolution` überhaupt erst angelegt hat. Der Hashabgleich zu Sitzungsbeginn war
richtig und galt für diesen Commit; ich habe die Datei danach über zwei Merges hinweg
weiterbenutzt, ohne den Abgleich zu erneuern. Die übrigen Zahlen des Prompts stimmten genau
deshalb, weil `00b` jene Dateien nicht angefasst hatte — die Methode war nicht teilweise richtig,
sie war zufällig nicht falsch. Daraus **Prüfregel 26**.

**Befund 2: eine Aufzählung im Prompt hat einen Fall mitgerissen.** Der Satz „die übrigen fünf
übergeben `constitution_hash_gov, constitution_gov`" traf auch Lage 2 in
`check_anchor_resolution` — den Aufruf, der den Anker gegen die **zweite** Epoche auflöst. Damit
stand die Verschränkung zweier Epochen ausgerechnet in dem Vektor, der sie trennen soll, und zwar
aus dem Grund, den D167 zwei Einträge vorher im selben Beispielnukleus beschrieben hat. Behoben in
`c6d63e4` auf demselben Branch, vor dem Merge.

Kein Ergebnis hat sich dadurch bewegt, und das ist der eigentliche Punkt: `constitution_2`
entsteht als `dict(constitution_gov)` mit geändertem `participants`, `irrevocable_predicates` ist
in beiden Fassungen dieselbe Liste, und der Store dieser Prüfung ist leer. **Zufällige
Harmlosigkeit ist keine Richtigkeit.** Eine Rücknahmeprobe war deshalb nicht möglich; ein Test,
der den Unterschied sähe, müsste die zwei Fassungen in `irrevocable_predicates` auseinanderziehen.

**Getragene Grenze.** Genau das ist der Beispielnukleus heute nicht: er kann eine Policy der
Epoche 1 nicht von einer der Epoche 2 unterscheiden, weil seine beiden Verfassungen in dem Feld
übereinstimmen, um das es geht. Der Epochenschritt aus D167 wird deshalb ausschließlich von `P-H`
gemessen. Ein Beispielnukleus, dessen Amendment `irrevocable_predicates` bewegt, wäre der zweite
Messpunkt — eine eigene Entscheidung, weil er die dokumentierten Hashes in `example-nucleus.md`
bewegt.

**Der Supervisor war zweimal die Fehlerquelle, das Werkzeug null mal — dritte Sitzung in Folge.**
Beide Male hat das Werkzeug gemessen und gemeldet statt still zu reparieren, und beide Male war
die gemeldete Abweichung der Befund. Die Zahl `20` für die Aufrufstellen von `resolve_policy` hat
gestimmt; sie kam aus Dateien, die seit dem Abgleich niemand angefasst hatte.

### D170 — Die Prompt-Verweise im Paketcode: fünf sind richtig, einer zeigt auf eine Spec-Lücke

**Anlass.** Die offene Liste führte „`03-prompt.md`-Verweise im Paketcode — vier Stellen unter
`mensch_als_republik/profiles/` und `policy.py`". Gemessen sind es **sieben**, und sie sind nicht
eine Sorte.

**Fünf nennen die Spec zuerst und den Prompt als zweiten Zeiger.** `profiles/credit.py`
(`03 §3.3.2`), `profiles/verdict.py` (`03 §2.4.2`), `profiles/policy.py` (`03 §1.2`),
`policy.py` (`00 §3`) und `tools/example_nucleus.py` (`01 §4`). Dort ist der Prompt Beleg, nicht
Quelle; er zeigt, woher eine Entscheidung kam, und die normative Fassung steht davor. Diese fünf
bleiben.

**Einer ist ein reiner Zeigerfehler.** `profiles/payload.py` nennt ausschließlich
`03-prompt.md §3.1`, obwohl `03 §1.3` die Kanonizitätsregel samt `NON_CANONICAL_V` im Volltext
führt. Der Verweis wandert auf die Spec.

**Einer ist kein Fehler, sondern der Beleg für eine Lücke.** `governance/findings.py` nennt
`04-prompt.md §2`, und das ist die einzige Stelle, die es gibt: **`INV-04` kommt in
`04-governance.md` nicht vor.** Die Invariantenreihe der Governance-Schicht lebt in
`04-prompt.md`, `04-golden-anchors.md` und `04-abnahme.md` — also in erteilten Prompt- und
Abnahmedateien, die per Konvention nicht mehr umgeschrieben werden (D157). Genau dafür ist
Prüfregel 17 da: der Prompt ist normativ, **weil** Code auf ihn zeigt. Hier zeigt der Code auf
ihn nicht aus Bequemlichkeit, sondern mangels Alternative.

Das ist der eigentliche Fund dieser Runde und wird nicht hier behoben: die `INV-04`-Reihe in
`04-governance.md` aufzunehmen ist eine Spec-Migration und ein eigener Zug. Sie berührt auch D117,
wo zwei dieser Invarianten als schwächer beschrieben sind, als sie scheinen.

**Nebenbefund: `dedupe_sort` existiert viermal.** `04b-korrektur-prompt.md` notierte drei; die
vierte hat mein `00b`-Prompt beauftragt, ohne dass mir die Notiz präsent war. `profiles`,
`governance` und die Nukleus-Schicht führen je eine für `Finding`, `policy.py` eine für
`PolicyNote`. `trust/findings.py` hat **keine** und schreibt dieselbe Operation in
`derive.py:80` inline aus: `tuple(sorted(set(a) | set(b) | set(c)))`.

**Gemessen, nicht vermutet: kein Determinismusbruch.** `trust/graph.py` gibt
`tuple(sorted(findings))` zurück — sortiert, aber nicht dedupliziert, was zunächst nach der Klasse
`B-9` aus `04-abnahme.md` aussieht. Es ist keine: `sorted` ist unabhängig von der
Eingabereihenfolge, und Duplikate sind dort strukturell unmöglich, weil jede
`(author, subject)`-Gruppe im BFS genau einmal besucht wird (`seen` verhindert die
Wiederaufnahme) und `kante_claim_id` je Gruppe eindeutig ist. Vier Schichten, vier Praxen, kein
Schaden.

**Beschluss.** Der Zeigerfehler in `payload.py` und die fehlende Zitatzeile für `dedupe_sort` in
`mensch_als_republik/findings.py` sind zwei Docstrings; sie reiten beim nächsten Lauf mit, statt
einen eigenen zu bekommen. Eine Zusammenlegung der vier `dedupe_sort` findet **nicht** statt: die
vier Enums sind bewusst getrennt (D90), und eine gemeinsame Hilfsfunktion über vier
`Finding`-Typen hinweg bräuchte entweder ein gemeinsames Protokoll oder `Any` — beides teurer als
vier Zeilen, die je zwei Zeilen lang sind.

**Zur Methode.** „Vier Stellen" stand seit Monaten in der offenen Liste und war schon beim
Aufschreiben eine Zählung. Prüfregel 26 gilt auch für die eigene Merkliste: eine Zahl darin ist
ein Messwert mit Verfallsdatum, kein Merkposten. Aufgefallen ist es nur, weil der Grep neu
gelaufen ist — und ein zweiter Grep derselben Runde wäre beinahe untergegangen, weil eine Pipe
auf `tail` seinen roten Status verschluckt hat. Dass `INV-04` nirgends in `04-governance.md`
steht, war ein **leeres** Ergebnis, und leere Ergebnisse sind die, die eine Maskierung frisst.
