# Trust-Flow-Schicht — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Layer: Trust / Reputation (über Identity/Claim)

Diese Schicht verwandelt den Graphen aus **aktiven** Bürgschafts-Claims (Atom-Spec §7.1,
Aktiv-Set nach Atom-Spec §6) in einen *personalisierten, Sybil-resistenten* Vertrauenswert.
Sie führt **kein** neues Claim-Feld ein — sie ist reine Auswertung über dem Atom.

---

## 1. Leitsätze (Geltungsrahmen)

- **Fluss ist Fundament, PageRank ist Näherung.** Jede *harte* Entscheidung läuft über
  Max-Flow / Min-Cut (beweisbare Schranke). PageRank ist die erlaubte kapazitätsvergessende
  Relaxation für *billiges* Massen-Ranking. Ein Graph, zwei Sichten (§4, §5).
- **Geldblinde Kapazität.** Basis-Kapazität ist rein strukturell (Distanz-Decay). Ein Bond
  hebt Kapazität **niemals** an — seine einzige Protokollwirkung ist Slashbarkeit (§6.1).
  Geld kann Vertrauen *verpfänden*, nie *kaufen*.
- **Geschichtete Seeds, kein globaler.** Der individuelle Seed ist Grundwahrheit (immer
  lokal, unentziehbar). Der Nukleus-Seed ist eine optionale geteilte *Linse*, nie ein
  objektiver Score (§6.3).
- **Per-Verifizierer, per-Sicht, nie global.** Jeder rechnet von *seinem* Seed über *seinen
  aktuell bekannten* Teilgraphen. Es muss kein globaler Graph existieren. Die Lokalität der
  Metrik *erzeugt* die Partitionstoleranz (§7).
- **Vertrauen ist Zustand, kein Vermögen.** `C(x)` ist rein *positional* — durch Wohlverhalten
  lässt sich kein höheres `C` erarbeiten, und ein erfolgreicher Vouch erhöht die Kapazität des
  Bürgen **nicht**. `t_s` ist ein Zustand des aktuell bekannten Kantensets, kein Integral über
  die Vergangenheit: widerrufen die Bürgen, fällt der Wert sofort. Nicht akkumulierbar, nicht
  hortbar, nicht übertragbar. Damit existiert kein Guthaben, das als Puffer gegen Sanktionen
  dienen könnte.

---

## 2. Graphmodell

Für eine Anfrage `(Scope N, Zweck π)`:

- **Knoten** `V` = Identitäten (Ed25519-Verify-Keys).
- **Kanten** `E` = gerichtete Kante `I → J` für jeden **aktiven** `nuc:N/vouch@1`-Claim
  mit Autor `I`, Subjekt `J`. „Aktiv" heißt: strukturell gültig, nicht abgelaufen, nicht
  widerrufen, nicht supersediert (Atom-Spec §6). Ein **partial-sync**-Vouch, dessen Vorgänger
  noch fehlt, ist erst `pending` (Atom-Spec §6) und trägt **noch keine** Kante bei — er wird
  aufgenommen, sobald er `active` wird. Das ist dieselbe sichere Richtung wie §7: fehlendes
  Wissen senkt nur, es erfindet keine Kante.
- **Eine Kante je `(I, J)`.** Mehrere Vouches derselben Identität auf dasselbe Subjekt im
  selben Scope erzeugen **eine** Kante mit `n_kante = max n` über die aktiven
  Gruppenmitglieder (§3.1) — keine parallelen Kanten, keine addierten Kapazitäten. Eine
  Beziehung ist eine Kante. Trägt kein Gruppenmitglied eine gültige Belegung nach §3.1,
  entsteht **keine** Kante, auch wenn der Claim nach Atom-Spec §6 `active` ist.
- **Scope-Partition.** Es gibt einen Graphen *pro* `N`. Vertrauen aus Scope A fließt nicht
  nach Scope B (Kontextbindung).
- **Zweck-Filter.** Trägt der Vouch in `v` einen Zweck-Tag, werden für Zweck `π` nur passende
  (oder per Policy untypisierte) Kanten einbezogen. Gleiche Metrik, gefilterter Graph —
  ein Filter, kein neuer Mechanismus.
- **Torwächter-Zwecke getrennt führen (Policy-Default).** `t_s` trägt zwei verschiedene Dinge:
  *Gehört-werden* (epistemische Autorität, nicht-rival — dass viele einem guten Denker zuhören,
  nimmt niemandem etwas weg) und *Torwächterschaft* (Aufnahme, Zugang, Bürgschaft — rival und
  zwingend). Nur die zweite Sorte ist ein lohnendes Unterwanderungsziel. Die Referenz-Policy
  führt Torwächter-Zwecke daher in eigenen Scopes; das Budget aus §3.1 bindet dann nur die
  Torwächterschaft, nicht das Zuhören. Ein Nukleus darf beides zusammenlegen — er macht sich
  damit angreifbar.

---

## 3. Kapazitätsmodell (Distanz-Decay)

Die Kapazität bestimmt, wie viel Vertrauen *durch* einen Knoten fließen kann. Sie klingt
mit der Distanz vom Seed ab — und genau das erzeugt die Sybil-Schranke und die
„Neuling ≈ 0"-Eigenschaft **strukturell, ohne Sonderregel**.

- **Distanz** `d(s, x)` = kürzeste Pfadlänge in Hops von Seed `s` zu `x` über dem
  **wirksamen** Kantenset `E⁺ = { e ∈ E : cap(e) ≥ 1 }` (BFS). Unerreichbar ⇒ `d = ∞`. Wer
  keine Kapazitätseinheit weiterreicht, reicht auch keine Position weiter. Die Definition ist
  wohlfundiert: `cap(I→J)` hängt nur von `d(I)` ab, das feststeht, wenn die BFS `I`
  expandiert — ein Durchlauf, kein Fixpunkt.
- **Knotenbudget** `C(x) = ⌊ C₀ · γ^{d(s,x)} ⌋`, mit `γ = γ_num/γ_den ∈ (0,1)` und
  Seed-Budget `C₀ > 0` bei `d = 0`. **Einmal am Ende abgerundet, nicht pro Schritt** —
  iteratives Runden machte das Ergebnis von der Auswertungsreihenfolge abhängig. Es gilt
  `C(x) = 0` für unerreichbare `x` und für alle `d` mit `C₀·γ^d < 1`.
- **Knoten-Splitting (Advogato-Konstruktion).** Jeder Knoten `x` wird in `x_in → x_out`
  gespalten, mit interner Kantenkapazität `C(x)`. Jede Vouch-Kante `I → J` wird zu
  `I_out → J_in` mit Kapazität **`⌊ n_kante · C(I) / D ⌋`** (§3.1).
- **Ankerset statt einzelnem Seed.** Ist der Seed eine Menge (§6.3), gilt
  `d(x) = min_a d(a,x)`, und die Quelle im Flussgraphen ist ein Super-Source `S*` mit
  ∞-Kanten auf jedes `a_in`. Die interne Kante des Ankers liegt damit auf dem Pfad: sein
  Budget `C(a)` bindet auch auf der Quellseite. Bei gültigem Budget ist das identisch zur
  Anbindung an `a_out` (`Σ_e cap(e) ≤ C(a)`); es unterscheidet sich genau bei
  über-committetem Anker, und dort in Richtung Unter-Vertrauen.

> **Warum Knoten- und nicht Kantenkapazität (bewusste Wahl).** Nur die Kapazität *am Knoten*
> macht die Schranke unabhängig von der Zahl der Sybils: der Engpass ist die endliche
> Kapazität der **ehrlichen Grenzknoten**, nicht die Zahl der Kanten oder Knoten dahinter.
> Das ist das tragende Element des Bounds in §4. Die Kantenkapazitäten aus §3.1 kommen
> additiv hinzu: sie können den Fluss nur weiter **senken** und berühren die
> `|S|`-Unabhängigkeit nicht.
>
> **Nachtrag seit D1.** Gilt die Budgetregel, ist `Σ_e ⌊n_e·C(I)/D⌋ ≤ (Σn_e)·C(I)/D ≤ C(I)`
> — die interne Knotenkante ist dann nie **allein** bindend (Gleichheit ist möglich,
> striktes Überschreiten nicht), und die Schranke wird gleichermaßen von den Kanten-Caps
> getragen. Sie bindet ausschließlich bei über-committeten Knoten, und auch dort nur, wenn
> tatsächlich mehr Fluss ankommt als `C(I)`. Das entwertet die Konstruktion nicht: sie ist
> weiterhin nötig, um Über-Commitment überhaupt sichtbar zu machen, und der
> Einheitskapazitäts-Lauf (§8) lebt vollständig auf ihr.

### 3.1 Vouch-Gewicht `w` und Selbstbindungsbudget

Ein Vouch deklariert in `v`, wie viel Vertrauen er weiterreicht.

- **Gewicht.** `w = n / D` mit `n ∈ [1, D]`; `D` ist Policy des Scopes (§8), Default `n = D`
  (also `w = 1`). Untypisierte Vouches gelten als `w = 1`.
- **Kantenkapazität.** `I_out → J_in` erhält `⌊ n_kante · C(I) / D ⌋`. Abrunden ist die
  sichere Richtung (Unter-Vertrauen) und erhält die exakte Integer-Arithmetik der harten
  Sicht.
- **Selbstbindungsbudget.** Für jede Identität `I` und jeden Scope `N` gilt `Σ wᵢ ≤ 1`,
  gleichbedeutend `Σ_J n_budget ≤ D`, über alle Gruppen `(I, J, N)` im Budget-Set.

> **Aggregation je `(I, J, N)`.** Mehrere Vouches derselben Identität auf dasselbe Subjekt im
> selben Scope bilden **eine** Gruppe. Es zählen `n_budget = max n` über die
> Gruppenmitglieder im Budget-Set und `n_kante = max n` über die im Aktiv-Set; die Kante
> trägt `cap(I→J) = ⌊n_kante·C(I)/D⌋`, das Budget prüft `Σ_J n_budget ≤ D`. Weil
> Aktiv-Set ⊆ Budget-Set gilt, ist stets `n_kante ≤ n_budget`. **Maximum, nicht Summe** —
> sonst wäre die bloße Erneuerung eines Vouch ein selbst-validierender Beweis gegen den
> eigenen Autor (§6.2), und zwei aktive Vouches auf dasselbe Subjekt trügen doppelte
> Kapazität bei einfachem Budget.

> **Out-Degree folgt aus dem Budget.** Aus `n ≥ 1` und `Σn ≤ D` folgt: höchstens `D`
> gleichzeitig bebürgte **Subjekte** pro Identität und Scope — gezählt werden Gruppen im
> Budget-Set, nicht Claims. Aus `cap ≥ 1 ⟺ n·C(I) ≥ D` folgt schärfer
> `wirksame Out-Degree(I) ≤ min(D, C(I))`. Bei `D ≥ C₀` (§8) bindet stets `C(I)`: **die Zahl
> der Menschen, für die man bürgen kann, ist die eigene Position** — keine gezählte
> Rationierung, sondern dieselbe positionale Größe wie alles andere in dieser Schicht.

> **Obergrenze, kein Anteil (bewusste Wahl).** Der Cap einer Kante hängt **nur von dieser
> Kante** ab — es gibt keine Normalisierung über `Σw`. Andernfalls wäre bei Teilwissen das
> beobachtete `Σw` zu klein, jeder bekannte Anteil zu groß, und **fehlendes Wissen erhöhte das
> errechnete Vertrauen** — ein Bruch der Monotonie aus §7. Der Defekt läge in der Kopplung, nicht
> in der Formel; keine Normalisierungsregel repariert ihn.

**Zwei Mengen, nicht eine.** Aktiv-Set und Budget-Set sind verschieden:

| Menge | Inhalt | Verwendung |
|---|---|---|
| **Aktiv-Set** | nicht widerrufen, nicht abgelaufen | Kantensatz für den Fluss (§2) |
| **Budget-Set** | nicht abgelaufen (**widerrufen, supersediert und `pending` eingeschlossen**), aggregiert je `(I, J, N)` über `max n` | Prüfung `Σ n_budget ≤ D` |

**`pending` bindet Budget.** Ein Vouch, dessen Vorgänger in der Autorenkette noch fehlt, trägt
keine Kante bei (§2), gehört aber ins **Budget-Set**: Er ist signiert, und der
Über-Commitment-Beweis beruht auf Signaturen, nicht auf Aktivität. Andernfalls ließe sich die
Budgetregel umgehen, indem ein Autor Vorgänger absichtlich zurückhält — alle Vouches blieben
`pending` und budgetfrei, bis der fehlende Vorgänger nachgereicht wird und sie gleichzeitig
`active` werden.

**Widerruf, Supersede und Freigabe.** Ein Widerruf stoppt den Fluss sofort (die Kante
verlässt das Aktiv-Set) und beendet die Haftung des Bürgen — **gibt das Budget aber nicht
frei**. Für Supersede gilt dasselbe. Frei wird Budget erst bei `t_exp` (§6.2), und erst, wenn
**alle** Vouches der Gruppe `(I, J, N)` abgelaufen sind. **Kein selbst-bezüglicher
Lebenszyklus-Akt gibt Budget frei; Budget folgt der Uhr, nicht dem Willen des Autors.**
Andernfalls ließe sich eine lange Laufzeit — das stärkste Signal — beliebig oft per Supersede
zurückholen, und die Knappheit wäre eine Formalität. Weil innerhalb einer Gruppe das
**Maximum** zählt und nicht die Summe, sind Erneuerung und Herabstufung dennoch frei: Ein
Autor kann seine Aussage jederzeit korrigieren, er kann nur ihr Gewicht nicht vorzeitig
anderswo einsetzen. Budget ist vorwärtsgerichtet, Haftung rückwärtsgerichtet; sie folgen
verschiedenen Uhren. Eine Nachhaftungsfrist wäre nicht auswertbar, weil sie eine
Cross-Chain-Zeitordnung verlangte, die es nicht gibt.

**Wirkung.** `w` ist dreifach gekoppelt: es bestimmt den Durchsatz der Kante, es verbraucht
Budget, und es bemisst die Haftung des Bürgen bei Defektion des Gebürgten (Enf-Spec §6). Damit
ist die **Deklaration selbst der Einsatz** — hohes Vertrauen lässt sich nicht billig behaupten.
Ein erfolgreicher Vouch bringt dem Bürgen umgekehrt **keine** Kapazitätsprämie (§1): der Ertrag
liegt in der Beziehung, nicht in der Metrik.

**Über-Commitment ist selbst-validierend.** Liegen mehrere signierte Vouches derselben Identität im
selben Scope mit `Σw > 1` vor, ist das ein unabhängig nachrechenbarer Beweis — dieselbe Klasse
wie Equivocation (Atom-Spec §4), mechanisch slashbar, ohne Verdikt. Bei Teilwissen ist das
beobachtete `Σw` zu klein: eine Verletzung wird möglicherweise **nicht erkannt**, aber nie eine
erfunden.

**Unlesbares oder ungültiges `n`.** Ist `v` keine CBOR-Map, fehlt der Key `0`, ist sein Wert
kein `uint`, oder liegt `n` außerhalb `[1, D]`, trägt dieser Vouch **keine Kante** und
**keinen Budget-Beitrag**. Weitere Keys sind unschädlich — geprüft wird Key `0`, nicht die
Map als Ganzes. Kein Beitrag, weil eine geratene Zahl eine Falschbeschuldigung wegen
Über-Commitment erzeugen könnte; keine Kante, weil das Unter-Vertrauen ist. Beides ist die
sichere Richtung, in verschiedene Richtungen.

---

## 4. Vertrauen als Fluss & der Min-Cut-Bound

**Definition.** `trust(s → T) = maxflow(s_in → T_in)` im gespaltenen, kapazitierten Graphen.
Die Quelle hängt an `s_in`, damit die interne Kante des Ankers — sein Budget `C(s)` — auf dem
Pfad liegt. Bei gültigem Budget ist das identisch zur Anbindung an `s_out`, weil
`Σ_e cap(e) ≤ C(s)` gilt; es unterscheidet sich genau dann, wenn der Anker über-committet
ist, und dann in Richtung Unter-Vertrauen.

**Schranke gegen Sybils.** Sei `H` die ehrliche Region (enthält `s`), `S` die Sybil-Region
(beliebig viele vom Angreifer erzeugte Identitäten). Eine **Angriffskante** ist ein Vouch
`h → g` von einem ehrlichen `h ∈ H` zu einem `g ∈ S` (der einzige Weg, wie Vertrauen `H`
verlassen kann).

> **Satz (simultaner Fluss).** Der **gleichzeitige** Vertrauensfluss in die Sybil-Region ist
> beschränkt durch die Kapazität der ehrlichen Endpunkte der Angriffskanten:
> ```
> maxflow(s → S)  ≤  Σ_{h ∈ Grenze} C(h)
> ```
> wobei `maxflow(s → S)` der Multi-Sink-Fluss über der **gesamten** Menge `S` ist und
> `Grenze` = die ehrlichen Knoten mit mindestens einer Angriffskante.

**Herleitung.** Führe einen Super-Sink `T*` mit ∞-Kanten von jedem `gᵢ_in` ein — an `T_in`,
nicht an `T_out`, sonst zählte die interne Kante des Ziels mit und die Multi-Sink-Semantik
wiche von der Einzelabfrage ab. Dann ist der simultane Gesamtfluss in `S` gleich
`maxflow(s_in → T*)`. Nach dem Max-Flow-Min-Cut-Theorem ist das gleich der minimalen
Schnittkapazität. Jeder Pfad von der Quelle nach `T*` passiert einen ehrlichen Grenzknoten
`h` — **einschließlich des Ankers selbst** —, dessen Durchsatz durch seine interne Kante
`C(h)` gedeckelt ist. Also `maxflow(s → T*) ≤ Σ_{h ∈ Grenze} C(h)`. Die endlichen
Kantenkapazitäten `⌊n·C(·)/D⌋` aus §3.1 können den Fluss nur weiter **senken**, nie anheben;
die Schranke gilt daher erst recht. ∎

Hinge die Quelle an `a_out`, wäre der Satz **falsch**: drei Kanten mit `n = D` von einem
Anker mit `C₀ = 16, D = 4` tragen je `⌊4·16/4⌋ = 16` und simultan 48 gegen eine behauptete
Schranke von 16. Die Anbindung an `a_in` ist kein Konventionsdetail, sondern die
Voraussetzung des Beweises.

> **⚠️ Die Summe der Einzelabfragen ist nicht beschränkt.** `Σ_{T ∈ S} trust(s → T)` ist eine
> **andere Größe** als `maxflow(s → S)` und kann diese überschreiten. Gegenbeispiel: `C(h) = 10`,
> `h` bürgt für `g₁` und `g₂`; einzeln berechnet ist `trust(s→g₁) = trust(s→g₂) = 10`, Summe 20,
> simultaner Fluss 10. Innerhalb von `S` verteilt sich der bei `g` ankommende Fluss über die
> internen Kanten auf jedes Ziel — **bei Einzelabfrage verdünnt nichts.**

> **Zwei unabhängige Divergenzursachen.** `Σ trust(s→Tᵢ)` übersteigt `maxflow(s→S)`, wenn
> (i) ein gemeinsamer Engpass stromaufwärts bindet, **oder** (ii) eine Einzelabfrage Knoten
> aus `S` als Zwischenknoten benutzt — im simultanen Lauf wird der Fluss dort schon an
> `gᵢ_in` absorbiert. Jede Ursache erzeugt für sich allein Divergenz (Golden Anchors: A nur
> (i), E nur (ii)); greift keine, sind beide Größen gleich (B, E₀). Wer nur einen der beiden
> Fälle testet, hat VR-02.1 halb getestet.

> **VR-02.1 — Aggregation MUSS simultan rechnen.** Jede Entscheidung, die Vertrauen über
> **mehrere** Identitäten verrechnet (Quorum, Abstimmung, „N unabhängige Attestierungen",
> Versicherungspool), MUSS den Multi-Sink-Fluss über der gesamten Anfragemenge berechnen.
> Die Summe einzeln berechneter `trust(s→Tᵢ)` ist **keine** gültige Näherung und trägt
> **keine** Sybil-Schranke.

**Korollar (`|S|`-Unabhängigkeit).** Die simultane Schranke hängt **nur** von den ehrlichen
Grenzknoten ab — **nicht von `|S|`**. Sind es `g` Angriffskanten mit Grenz-Kapazität `≤ C_max`,
gilt `maxflow(s → S) ≤ g · C_max`. Eine Million zusätzliche Sybils teilen dasselbe feste Budget.
Das ist „Identitäten gratis, Kanten teuer" — **bewiesen**, nicht erhofft. Und weil
`C(h) = ⌊C₀ γ^{d(s,h)}⌋` mit der Distanz fällt, ist eine seed-ferne Angriffskante ohnehin
billig: doppelter Schutz.

> **Schärfere Schranke.** Unter gültigem Budget gilt zusätzlich
> `maxflow(s → S) ≤ Σ_{h ∈ Grenze} Σ_{e Angriffskante von h} ⌊n_e·C(h)/D⌋ ≤ Σ_{h} C(h)`.
> Die Kanten-Caps sind die tatsächlich bindende Größe; `Σ C(h)` ist die schwächere, aber
> budget-unabhängige Form.

**Wirkung des Gewichts auf die Einzelabfrage.** Auch ohne Verdünnung über `|S|` ist der Wert
eines einzelnen Sybils nicht durch `C(h)` gedeckelt, sondern durch `w_e` — durch das, was der
ehrliche Bürge **dieser einen Kante** explizit zugewiesen hat (§3.1). Um Sybils über eine
Schwelle zu heben, braucht ein Angreifer daher ein großes `w`; ein großes `w` bindet das Budget
des Bürgen und aktiviert seine Haftung. Identitäten bleiben gratis — ohne teuer gebundenes
fremdes `w` bleiben sie wertlos.

> **Was `Σw ≤ 1` kostet — und was nicht.** Am kanonischen Testgraphen (Golden Anchors §3)
> senkt die Budgetregel den **simultanen** Fluss in die Sybil-Region **nicht**: 4 mit
> über-committetem Bürgen (Variante A), 4 mit gültigem Budget (E, F). Sie senkt allein die
> Summe der Einzelabfragen, und auch die nur von 12 auf 10. Der Ertrag liegt nicht in der
> Unterdrückung, sondern darin, dass A mechanisch beweisbar wird (Über-Commitment, §3.1) und
> F nicht. Das ist L2 in Zahlen — wer `Σw ≤ 1` für eine Sybil-Abwehr hält, hat den
> Mechanismus falsch verstanden.
>
> **Die Angriffsform hängt nicht vom Verifizierer ab — die Schranke tut es.** Bei fester
> Sybil-Zahl ist eine gemischte Belegung (`n = 2,1,1` auf drei Ziele, `S` vernetzt) gegen
> **beide** Verifiziererformen optimal: Summe 10, simultan 4, drei Identitäten über einer
> Schwelle von 2. Es gibt keinen Trade-off zwischen Streuung und Konzentration, den ein
> Angreifer zu treffen hätte. Der Unterschied liegt allein beim Verifizierer: gegen die Summe
> der Einzelabfragen ist der Angriff **unbeschränkt**, weil `|S|` frei ist und jeder weitere
> erreichbare Sybil addiert; gegen den simultanen Fluss greift die Schranke dieses
> Abschnitts. Wer VR-02.1 verletzt, wählt nicht eine ungenauere Zahl — er wählt eine Größe
> ohne obere Schranke.

> **⚠️ Die Sybil-Schranke ist keine Kollusions-Schranke.** Der Beweis setzt voraus, dass
> zwischen `H` und `S` **wenige** Angriffskanten liegen. Bei echter Unterwanderung gilt das
> nicht: kollaborierende Menschen haben je ihre eigenen, *echten* Beziehungen — der Schnitt ist
> nicht dünn, er existiert nicht als Schnitt. Die bewiesene Schranke schützt gegen **gefälschte
> Identitäten**, nicht gegen **echte Menschen, die sich abstimmen**. Das ist keine Schwäche
> dieser Konstruktion, sondern die Grenze der gesamten Klasse sozialgraph-basierter Abwehren
> (Viswanath et al., SIGCOMM 2010: solche Verfahren betreiben im Kern lokale
> Community-Erkennung; die Erkennungsgenauigkeit fällt, je näher am vertrauten Knoten der
> Angreifer seine Kanten platziert). Für MaR folgt daraus die Form des optimalen Angriffs:
> **nicht viele Kanten, sondern wenige nahe** — ein Komplize bei `d = 1` ist mehr wert als
> hundert bei `d = 4`. Gegenmittel sind Pfad-Disjunktheit und die Kennzahlen aus §8, nicht die
> Schranke dieses Abschnitts.

**Neuling ≈ 0.** Eine frische Identity ohne eingehende Vouch-Kante ist von `s` unerreichbar
(`d = ∞`), trägt also `C = 0` und empfängt Fluss 0 — strukturell, ohne Sonderfall.

---

## 5. PageRank-Relaxation (die schnelle Sicht)

Personalisierter Random-Walk-mit-Restart vom Seed:

```
t_s = α · e_s + (1−α) · Pᵀ · t_s     ⇔     t_s = α (I − (1−α) Pᵀ)⁻¹ · e_s
```

mit spaltenstochastischer Übergangsmatrix `P` (**gewichtete**, normalisierte Vouch-Adjazenz),
Restart-Vektor `e_s` (der Seed, §6.3) und Restart-Wahrscheinlichkeit `α`.

> **Die Relaxation liest `w` (§3.1).** Der Übergangsanteil von `I` nach `J` ist proportional zum
> Gewicht `w` der Kante `I → J`, anschließend spaltenstochastisch normalisiert — **nicht**
> gleichverteilt über die ausgehenden Kanten. Andernfalls behandelte die schnelle Sicht einen
> Probe-Vouch mit `w = 0.05` wie eine volle Bürgschaft und wäre damit **großzügiger** als die
> harte Sicht (§4). Eine Relaxation darf ungenauer sein, nie über-vertrauend.
>
> Die hier nötige Normalisierung über `Σw` wäre in §4 **verboten** (sie koppelt Kanten
> aneinander und bricht damit die Monotonie aus §7, siehe das Blockzitat in §3.1). In §5 ist sie
> zulässig, **weil dieser Abschnitt ohnehin keine harte Schranke trägt** und für Gates verboten
> ist. Das ist kein Widerspruch, sondern genau die Trennlinie zwischen beiden Sichten.
>
> Der Buchstabe `P` ersetzt das frühere `C`, um die Kollision mit der Knotenkapazität `C(x)`
> (§3) zu vermeiden. Reine Umbenennung, keine inhaltliche Änderung.

- **Garantie:** nur **weich/probabilistisch** sybil-resistent — Walks überqueren wenige
  Angriffskanten selten, also erreicht `S` wenig stationäre Masse, aber **keine harte
  Schranke**.
- **Erlaubt für:** billiges Ranking/Gewichten vieler Knoten, „wer ist grob vertraut".
- **Verboten für:** harte Admission-/Gate-Entscheidungen — die laufen über §4.

Beide Sichten teilen denselben Graphen. Keine zwei Welten, nur eine harte und eine schnelle
Projektion.

---

## 6. Bond, Seeds & harte Decke — wie sie präzise eingehen

### 6.1 Bond: Oberseite verboten, Unterseite erlaubt

- Die Kapazitätsfunktion `C(·)` liest `v.bond_ref` **nicht**. Zwei Menschen an gleicher
  struktureller Position bekommen identische Kapazität, egal ob reich oder arm.
- Die **einzige** Protokollwirkung eines Bonds: er macht den Vouch unter einem
  Defektions-/Equivocation-Beweis **slashbar** (ökonomische Schicht). Bonden ist
  selbst-auferlegtes Risiko (Costly Signal), kein Privileg — der Ehrliche gewinnt nichts,
  nur der Defektor verliert.
- Eine Policy darf für Hochrisiko-Kontexte verlangen, dass *nur gebondete* Kanten **zählen**
  (ein Filter wie der Zweck-Tag). Auch dann erhält die gebondete Kante dieselbe strukturelle
  Kapazität wie ungebondet — Bond ist nie ein Multiplikator.
- **Ehrlicher Residual (offen benannt):** Glaubwürdigkeit-durch-Risiko ist mild „kaufbar" —
  ein Armer kann nicht so teuer bewehren. Aber das ist *Risiko*, nicht *Kapazität*; der
  Ehrliche verliert nie, egal wie arm. Größenordnungen milder als „Geld kauft Standing".

### 6.2 Harte Decke `t_exp`

Ein Vouch mit `t_exp` voidet sich selbst nach Ablauf — **auch wenn sein Widerruf nie
ankommt**. Das ist der partitionstolerante Backstop gegen den steckengebliebenen Revoke
(§7). Strukturell, ohne Policy. **Ausgewertet wird `t_exp` lokal** gegen die subjektive
Verifizierer-Zeit `now` (Atom-Spec §6): zwei Verifizierer dürfen legitim uneins sein, ob ein
Vouch schon abgelaufen ist — die sichere Richtung ist stets Unter-Vertrauen. „Voidet sich
selbst" meint also *strukturell definiert*, nicht *global synchron*.

**`t_exp` ist für Vouches verpflichtend.** In Scopes mit Budgetregel (§3.1) MUSS ein Vouch
`t_exp` tragen, oder die Policy setzt eine Maximallaufzeit als Default — andernfalls bindet er
Budget unbefristet. Damit wird `t_exp` zur ökonomischen Entscheidung und nicht bloß zum
Sicherheits-Backstop: kurze Laufzeit bedeutet liquides Budget, häufige Erneuerung und ein
schwächeres Signal; lange Laufzeit bedeutet ein starkes Signal bei gebundener Kapazität.
Erneuerung ist wiederholte aktive Bestätigung und damit frischere Evidenz als ein alter,
nie widerrufener Vouch.

### 6.3 Geschichtete Seeds

Der Restart-/Quellvektor unterscheidet die Sichten; die Berechnung ist identisch:

- **Individuell:** `e_s` setzt Masse auf das eigene, out-of-band verifizierte Ankerset.
  Grundwahrheit, immer verfügbar, unentziehbar.
- **Nukleus:** `e_N` setzt Masse auf das vom Nukleus deklarierte Ankerset. Optionale
  geteilte Linse für billige Koordination, explizit „die Sicht des Nukleus".
- **Fallback:** fehlt die Nukleus-Linse (Partition), fällt der Verifizierer sauber auf `e_s`
  zurück. Ein globaler Seed existiert nie.

---

## 7. Partitionstoleranz

Jeder rechnet über seinen *aktuell bekannten* Teilgraphen (die per Gossip erhaltenen
Vouch-Claims). Die Partition ist kein zu behebender Defekt — die Lokalität *macht* die
Toleranz.

- **Monotonie (sichere Richtung).** Max-Flow ist monoton in den Kanten. Fehlende Vouch-Kanten
  können den berechneten Fluss nur **senken** ⇒ das Ergebnis ist eine konservative
  **Untergrenze** des wahren Flusses. Im Zweifel wird **unter**-vertraut — die sichere
  Richtung für Sybil-Resistenz. (Distanz analog: fehlende Kanten ⇒ geschätzte Distanz ≥ wahre
  ⇒ wieder Unter-Vertrauen.)
- **Die einzige gefährliche Richtung:** ein fehlender *Widerruf* (nicht eine fehlende
  Bürgschaft). Hast du den Vouch, aber sein `revoke` steckt in einer Partition, dann
  **über**-vertraust du. Drei gestaffelte Abwehren:
  1. `t_exp` — strukturelle harte Decke (§6.2).
  2. Widerrufe propagieren mit **Priorität** (sicherheitskritisch) — Policy.
  3. Für Hochrisiko: **frische positive Evidenz** verlangen, nicht bloße Abwesenheit eines
     Widerrufs — denn über eine Mesh ist Abwesenheit von Evidenz keine Evidenz der
     Abwesenheit. Policy.

---

## 8. Policy-Knöpfe (parametrisiert, nicht im Protokoll fixiert)

Der *Mechanismus* ist festgelegt; die *Werte* sind Interpretation (A2):

- `γ` (Distanz-Decay) und `α` (PageRank-Restart): Default eher **schnelles** Abklingen —
  passt zum Lokal-Ethos und verbessert die Sybil-Resistenz (weniger Fluss in die Peripherie).
- `C₀` (Seed-Budget): skaliert die Leiter. **Nicht mehr verhältniserhaltend**, seit die
  Kantenkapazität abrundet: bei `C₀ = 16` ist `⌊1·2/4⌋ = 0`, bei `C₀ = 160` ist
  `⌊1·20/4⌋ = 5`. `C₀` bestimmt zusammen mit `D` den Granularitätsboden und damit, wie weit
  vom Seed noch gebürgt werden kann.
- Schwelle & Gate pro Aktion: die Metrik **exponiert** nur einen Wert; ob er „reicht", ist
  Policy. (Der Neuling hat Null — die anderen *sehen* das und entscheiden selbst.)
- Zweck-Filter, Bond-Pflicht für Hochrisiko: Filter, keine neuen Mechanismen.
- `D` (Nenner des Vouch-Gewichts, §3.1): bestimmt die Granularität von `w`. **Über die
  Lebensdauer eines Scopes unveränderlich** — ein anderes `D` bedeutet einen neuen Scope,
  sonst würden bestehende signierte Vouches still umbewertet. **SHOULD `D ≥ C₀`**, damit die
  Out-Degree an der Position hängt (§3.1) und nicht an einer gezählten Grenze. Eine
  geschlossene Kurzform der Kantenkapazität gibt es **nicht**: `⌊n·⌊C₀γ^d⌋/D⌋` ist doppelt
  gerundet und lässt sich nur bei ganzzahligem `C₀γ^d` zu `⌊n·γ^d⌋` zusammenziehen
  (Gegenbeispiel `C₀ = D = 16, γ = ⅔, d = 2, n = 9`: `3` gegen `4`).
- **⚠️ Granularitätsboden.** `cap(I→J) = 0`, sobald `n·C(I) < D`. Ein Knoten mit kleiner
  Kapazität kann nur noch für wenige — am Rand für genau einen — mit vollem Budget bürgen,
  oder für niemanden. `D` schneidet die Peripherie ab, unabhängig von `γ`.
- **Budgetgrenze:** Default `Σw ≤ 1`. Ein Nukleus darf lockerer oder strenger setzen.
- **Pfad-Disjunktheit statt bloßer Anzahl.** Eine Policy kann „N Attestierungen über
  **knoten-disjunkte** Pfade vom Seed" verlangen statt nur „N Attestierungen". Berechnung:
  derselbe Max-Flow mit **Einheitskapazitäten auf den internen Knotenkanten** und ∞ auf den
  Vouch-Kanten — also **knoten**-disjunkt, nicht kantendisjunkt. Zwei Pfade durch denselben
  Bürgen sind ein Bürge. **Endpunkte werden nicht gespalten:** die internen Kanten der Anker
  tragen ∞, die des Ziels liegt ohnehin nicht auf dem Pfad (§4). Sonst wäre die Zahl von
  einem einzelnen Anker aus trivial 1. Wirkung: eine Koalition, die über *einen*
  Bürgen eingesickert ist, hat Min-Cut 1 — egal wie viele Mitglieder sie hat. Das ist die
  strukturelle Fassung von „Zeugen dürfen nicht voneinander abhängen".
- **Beobachtungskennzahlen (keine Schwellen, kein Zwang).** Zwei Zahlen, die jeder Verifizierer
  auf seinem eigenen Teilgraphen rechnet:
  *Quellenunabhängigkeit* — sind die Bürgen von `X` untereinander pfad-disjunkt zum Seed?
  (Tausend Bürgen aus einem Cluster sind ein Bürge.)
  *Ersetzbarkeit* — ist `X` ein Schnittknoten, bricht der Fluss zur Peripherie ohne ihn zusammen?
  Hohe Stellung aus vielen unabhängigen Quellen bei vorhandenen Alternativpfaden ist verdient
  und jederzeit bestreitbar. Hohe Stellung aus einer Quelle ohne Alternative ist ein
  Kaperungsziel, unabhängig von der Verdienstlage der Person. Die Metrik exponiert nur die
  Zahlen; die Deutung bleibt beim Beobachter.
- **⚠️ Kalibrierungs-Nebenbedingung (Bootstrap).** `Σw ≤ 1` macht die Frühphase eng. Für `f`
  Gründer, `M` Neulinge, `m` Bürgen je Neuling und Admission-Schwelle `θ`:
  ```
  θ ≤ f · C₀ / M          (Kapazität — unabhängig von D und m)
  D ≥ M · m / f           (Granularität — Out-Degree je Gründer)
  ```
  Beide Bedingungen sind unabhängig und beide bindend. Für `f = 3, C₀ = 16, M = 17` folgt
  `θ ≤ 2`; `m = 2` liefert dieselbe Vertrauenshöhe wie `m = 1` bei doppelter
  Pfad-Disjunktheit (die Rundung frisst den Unterschied — Redundanz ist dort gratis),
  `m = 3` kollabiert am Granularitätsboden auf null. Die Kapazitätsbedingung ist dabei die
  **optimistische** Form: nach Rundung sind von `f·C₀ = 48` Einheiten real nur 36
  verteilbar (Golden Anchors §7).
- **⚠️ Harte Reichweite.** Ab `d` mit `⌊C₀γ^d⌋ = 0` kann ein Mitglied **keinen** wirksamen
  Vouch mehr tragen — gleich wie viel Budget es einsetzt und gleich wie viele Bürgen ein
  Kandidat sammelt. Damit gilt `r_max = ⌊log_{1/γ} C₀⌋`, bei `C₀ = 16, γ = ½` also
  `r_max = 4` für die Bürgschaftsfähigkeit und `5` für die Mitgliedschaft. Ein Nukleus mit
  `θ = 2` sättigt bei rund **600 Mitgliedern** und Radius 5; wer mehr will, muss `C₀` oder
  `γ` ändern. Das ist die quantitative Fassung von „maximal lokal" und keine Panne.
- **Geflaggte Autoren.** Ob ein Bürge mit `equivocation-flagged` oder erwiesenem
  Über-Commitment noch Fluss trägt, ist Policy (`include_flagged`, Default *nein*). Die
  Budgetrechnung ist davon **unberührt** — ein Flag darf die Grundlage nicht verschieben, auf
  der es erkannt wurde.

---

## 9. Bewusst getragene v1-Grenzen & gemachte Designentscheidungen

- **Geometrischer Decay** `⌊C₀ γ^d⌋` ist eine *gewählte* Form (ein Knopf, saubere Monotonie);
  Advogatos Original nutzt ein gestuftes Schema. Austauschbar, solange monoton fallend.
- **Hop-Distanz** (BFS) als Default; gewichtete Distanz wäre ein Knopf.
- **PageRank nur als Relaxation** — bei Missbrauch für harte Gates verliert man die Schranke
  aus §4. Diese Trennlinie ist nicht verhandelbar.
- **Berechnungskosten.** Max-Flow ist paarweise/on-demand teurer als ein PageRank-Lauf —
  bewusst akzeptiert, weil „paarweise und lokal" exakt zum Lokal-Ethos passt. Caching der
  Aktiv-Sets und der BFS-Distanzen ist Implementierungssache.
- **Seed-Integrität** bleibt die wertbildende Voraussetzung (Atom-Spec §8): die gesamte
  Schranke aus §4 setzt voraus, dass das initiale Ankerset out-of-band sauber etabliert ist.
- **Einzelabfragen verdünnen nicht** (§4). Wer Sybil-Schutz über eine Menge braucht, muss
  simultan rechnen (VR-02.1). Die Summe von Einzelwerten trägt keine Schranke.
- **Kollusion ist nicht Sybil** (§4). Gegen eine hinreichend große, geduldige, echt eingebettete
  Koalition hilft kein Protokoll. Die Mechanismen dieser Schicht erhöhen die nötige
  Koalitionsgröße und machen die Vorbereitung sichtbar — mehr ist nicht zu haben.
- **Restfenster bei Widerruf vor Defektion** (§3.1). Ein Bürge kann kurz vor der Defektion
  seines Komplizen widerrufen und der Haftung entgehen. Bepreist ist das durch den Verlust der
  Bürgschaftskapazität bis `t_exp` — nicht über eine neue Identität rückholbar, weil Standing
  positional ist (§1). Zusätzlich ist das Muster in der Widerrufs-Historie lesbar.
- **Seed-Kompromittierung** (§6.3). Wer `e_N` kompromittiert, kompromittiert jeden, der diese
  Linse benutzt. Der Fallback auf `e_s` ist **Eindämmung, keine Abwehr**.
