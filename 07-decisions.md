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
