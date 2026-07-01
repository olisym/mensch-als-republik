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

---

## 2. Graphmodell

Für eine Anfrage `(Scope N, Zweck π)`:

- **Knoten** `V` = Identitäten (Ed25519-Verify-Keys).
- **Kanten** `E` = gerichtete Kante `I → J` für jeden **aktiven** `nuc:N/vouch@1`-Claim
  mit Autor `I`, Subjekt `J`. „Aktiv" heißt: strukturell gültig, nicht abgelaufen, nicht
  widerrufen, nicht supersediert (Atom-Spec §6).
- **Scope-Partition.** Es gibt einen Graphen *pro* `N`. Vertrauen aus Scope A fließt nicht
  nach Scope B (Kontextbindung).
- **Zweck-Filter.** Trägt der Vouch in `v` einen Zweck-Tag, werden für Zweck `π` nur passende
  (oder per Policy untypisierte) Kanten einbezogen. Gleiche Metrik, gefilterter Graph —
  ein Filter, kein neuer Mechanismus.

---

## 3. Kapazitätsmodell (Distanz-Decay)

Die Kapazität bestimmt, wie viel Vertrauen *durch* einen Knoten fließen kann. Sie klingt
mit der Distanz vom Seed ab — und genau das erzeugt die Sybil-Schranke und die
„Neuling ≈ 0"-Eigenschaft **strukturell, ohne Sonderregel**.

- **Distanz** `d(s, x)` = kürzeste Pfadlänge in Hops von Seed `s` zu `x` über `E` (BFS).
  Unerreichbar ⇒ `d = ∞`.
- **Knotenbudget** `C(x) = C₀ · γ^{d(s,x)}`, mit Decay `γ ∈ (0,1)` und Seed-Budget `C₀ > 0`
  bei `d = 0`. Es gilt `C(x) = 0` für unerreichbare `x`.
- **Knoten-Splitting (Advogato-Konstruktion).** Jeder Knoten `x` wird in `x_in → x_out`
  gespalten, mit interner Kantenkapazität `C(x)`. Jede Vouch-Kante `I → J` wird zu
  `I_out → J_in` mit Kapazität **∞**.

> **Warum Knoten- und nicht Kantenkapazität (bewusste Wahl).** Nur die Kapazität *am Knoten*
> macht die Schranke unabhängig von der Zahl der Sybils: der Engpass ist die endliche
> Kapazität der **ehrlichen Grenzknoten**, nicht die Zahl der Kanten oder Knoten dahinter.
> Das ist das tragende Element des Bounds in §4.

---

## 4. Vertrauen als Fluss & der Min-Cut-Bound

**Definition.** `trust(s → T) = maxflow(s_out → T_in)` im gespaltenen, kapazitierten Graphen.

**Schranke gegen Sybils.** Sei `H` die ehrliche Region (enthält `s`), `S` die Sybil-Region
(beliebig viele vom Angreifer erzeugte Identitäten). Eine **Angriffskante** ist ein Vouch
`h → g` von einem ehrlichen `h ∈ H` zu einem `g ∈ S` (der einzige Weg, wie Vertrauen `H`
verlassen kann).

> **Satz.** Der gesamte Vertrauensfluss in die Sybil-Region ist beschränkt durch die
> Kapazität der ehrlichen Endpunkte der Angriffskanten:
> ```
> Σ_{T ∈ S} trust(s → T)  ≤  Σ_{h ∈ Grenze} C(h)
> ```
> wobei `Grenze` = die ehrlichen Knoten mit mindestens einer Angriffskante.

**Herleitung.** Führe einen Super-Sink `T*` mit ∞-Kanten von jedem `g ∈ S` ein; dann ist
der Gesamtfluss in `S` gleich `maxflow(s → T*)`. Nach dem Max-Flow-Min-Cut-Theorem ist
das gleich der minimalen Schnittkapazität. Da alle Vouch-Kanten Kapazität ∞ haben, kann
kein minimaler Schnitt sie durchtrennen — er durchtrennt nur **interne** Knotenkanten
(endliche Kapazität `C(·)`). Jeder Pfad von `s` nach `T*` muss einen ehrlichen Grenzknoten
`h` passieren, dessen Durchsatz durch sein internes Budget `C(h)` gedeckelt ist. Also
`maxflow(s → T*) ≤ Σ_{h ∈ Grenze} C(h)`. ∎

**Korollar (das eigentliche Resultat).** Die Schranke hängt **nur** von den ehrlichen
Grenzknoten ab — **nicht von `|S|`**. Sind es `g` Angriffskanten mit Grenz-Kapazität
`≤ C_max`, gilt `Σ trust ≤ g · C_max`. Eine Million zusätzliche Sybils teilen dasselbe
feste Budget; sie *verdünnen*, sie addieren nicht. Das ist „Identitäten gratis, Kanten
teuer" — **bewiesen**, nicht erhofft. Und weil `C(h) = C₀ γ^{d(s,h)}` mit der Distanz fällt,
ist eine seed-ferne Angriffskante ohnehin billig: doppelter Schutz.

**Neuling ≈ 0.** Eine frische Identity ohne eingehende Vouch-Kante ist von `s` unerreichbar
(`d = ∞`), trägt also `C = 0` und empfängt Fluss 0 — strukturell, ohne Sonderfall.

---

## 5. PageRank-Relaxation (die schnelle Sicht)

Personalisierter Random-Walk-mit-Restart vom Seed:

```
t_s = α · e_s + (1−α) · Cᵀ · t_s     ⇔     t_s = α (I − (1−α) Cᵀ)⁻¹ · e_s
```

mit spaltenstochastischer Übergangsmatrix `C` (normalisierte Vouch-Adjazenz),
Restart-Vektor `e_s` (der Seed, §6.3) und Restart-Wahrscheinlichkeit `α`.

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
(§7). Strukturell, ohne Policy.

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

Jeder rechnet über seinen *aktuell bekannten* Teilgraphen (die via Gossip/LXMF erhaltenen
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
- `C₀` (Seed-Budget): skaliert nur, ändert keine Verhältnisse.
- Schwelle & Gate pro Aktion: die Metrik **exponiert** nur einen Wert; ob er „reicht", ist
  Policy. (Der Neuling hat Null — die anderen *sehen* das und entscheiden selbst.)
- Zweck-Filter, Bond-Pflicht für Hochrisiko: Filter, keine neuen Mechanismen.

---

## 9. Bewusst getragene v1-Grenzen & gemachte Designentscheidungen

- **Geometrischer Decay** `C₀ γ^d` ist eine *gewählte* Form (ein Knopf, saubere Monotonie);
  Advogatos Original nutzt ein gestuftes Schema. Austauschbar, solange monoton fallend.
- **Hop-Distanz** (BFS) als Default; gewichtete Distanz wäre ein Knopf.
- **PageRank nur als Relaxation** — bei Missbrauch für harte Gates verliert man die Schranke
  aus §4. Diese Trennlinie ist nicht verhandelbar.
- **Berechnungskosten.** Max-Flow ist paarweise/on-demand teurer als ein PageRank-Lauf —
  bewusst akzeptiert, weil „paarweise und lokal" exakt zum Lokal-Ethos passt. Caching der
  Aktiv-Sets und der BFS-Distanzen ist Implementierungssache.
- **Seed-Integrität** bleibt die wertbildende Voraussetzung (Atom-Spec §8): die gesamte
  Schranke aus §4 setzt voraus, dass das initiale Ankerset out-of-band sauber etabliert ist.
