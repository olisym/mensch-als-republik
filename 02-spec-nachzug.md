# Spec-Nachzug Layer 02 — Patch-Text

Revision 2 · Branch: `spec/02-vouch-weight-and-sybil-fix` · anzuwenden vor dem Merge nach `main`
Betroffen: `07-decisions.md`, `01-claim-atom.md`, `02-trust-flow.md`

## Was sich gegenüber Revision 1 geändert hat

Die Prüfung von Rev 1 gegen den Spec-Stand hat fünf Blocker gefunden. Drei davon waren
Zahlenfehler in Texten, die normativ geworden wären.

| # | Befund | Folge |
|---|---|---|
| 1 | „Budgetregel senkt 12→9 und 4→3, 25 %" ist falsch. Variante F (budgetgültig) liefert 4/3/3, Σ 10, simultan 4. Der simultane Wert fällt **gar nicht** (A: 4, E: 4, F: 4). | B.5c neu geschrieben |
| 2 | „Optimale Angriffsform hängt vom Verifizierer ab" hält nicht: F dominiert C und E in jeder Spalte. Gegen naive Summierung ist der Angriff zudem **unbeschränkt**, weil `\|S\|` frei ist. | B.5d neu geschrieben |
| 3 | `S* → a_out` (D31 alt) umgeht die interne Kante des Ankers ⇒ der `§4`-Satz ist für einen über-committeten Anker **falsch** (Anker A′: 48 gegen behauptete 16). | **D31 neu: `S* → a_in`**, D32 um die Endpunkt-Regel ergänzt |
| 4 | D38 + D4 machten die ehrliche Erneuerung oder Herabstufung eines Vouch zu einem selbst-validierenden Beweis gegen den Autor — `05 §3` Stufe 3, mechanischer Slash ohne Verdikt. | **D40 neu: Aggregation je `(I, J, N)` über `max n`** |
| 5 | D37 kollidierte mit `§2` (Kante je aktivem Claim) und mit `v.bond_ref` / Zweck-Tag. | B.0 neu, B.1 um Key-Vergabe ergänzt |

Kleinere Korrekturen, eingearbeitet: D34s Kurzformel `⌊n·γ^d⌋` ist bei doppelter Rundung
falsch; `nukleus-fest` → `scope-fest` durchgezogen; D36s Beispiel braucht ein Profil mit
`D > C(2)`; `t_exp` in `01 §7.1`; Zeiger auf D38 in Abschnitt E; `Σ_k M_k` durch die Zahl ersetzt.

---

## Teil A — Registereinträge für `07-decisions.md`

Neuer Abschnitt **J** hinter Abschnitt I. Auslöser: die Berechnung der Golden Anchors und ihre
Gegenprüfung. Dreizehn Entscheidungen, davon drei Korrekturen an Sätzen aus derselben Sitzung
(D34 korrigiert eine zu starke Empfehlung, D37 ersetzt einen veralteten Vorschlag in Layer 01,
D31 revidiert eine Konvention, die den Satz in `§4` gebrochen hätte).

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

### D31 — Super-Source hängt an `a_in` ⚠️ (ersetzt die Fassung „`a_out`")

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

### D40 — Aggregation je `(I, J, N)` über `max n` ⚠️ (neu)

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

---

## Teil B — Textänderungen

### B.0 `02-trust-flow.md §2` — Kantenbildung (neu)

Die Kanten-Zeile ergänzen:

> **Eine Kante je `(I, J)`.** Mehrere Vouches derselben Identität auf dasselbe Subjekt im selben
> Scope erzeugen **eine** Kante mit `n_kante = max n` über die aktiven Gruppenmitglieder (§3.1) —
> keine parallelen Kanten, keine addierten Kapazitäten. Eine Beziehung ist eine Kante. Trägt kein
> Gruppenmitglied eine gültige Belegung nach §3.1, entsteht **keine** Kante, auch wenn der Claim
> nach Atom-Spec §6 `active` ist.

Ohne diesen Zusatz widerspricht `§2` („eine Kante für jeden aktiven Claim") sowohl D37 als auch
D40 im Wortlaut.

### B.1 `01-claim-atom.md §7.1` — zwei Tabellenzeilen ersetzen

**Alt:**

> | `v` | opak, Policy-geparst; Vorschlag: `{ weight ∈ [0,1], bond_ref?, note? }` |
> | `t_exp`| optional — zeitlich begrenzte Bürgschaft (lokale Gültigkeitsdecke, §6) |

**Neu:**

> | `v` | kanonisches CBOR-Map mit `0: n`, `n : uint`, `1 ≤ n ≤ D` — das Vouch-Gewicht
> (Trust-Flow-Spec §3.1). **Abwesend ⇒ `n = D`, also `w = 1`.** Weitere Keys sind zulässig und
> für das Atom opak. |
> | `t_exp`| optional im Atom; in Scopes mit Budgetregel **Pflicht**, oder die Policy setzt eine
> Maximallaufzeit als Default (Trust-Flow-Spec §6.2) |

Darunter als Hinweis:

> `n` ist ein **uint**, kein Bruch. `w = n/D` mit scope-festem `D` (Trust-Flow-Spec §8) hält die
> gesamte harte Sicht ganzzahlig; ein `weight ∈ [0,1]` als Float verstieße gegen §3 Regel 6.
> Geprüft wird **Key `0`**, nicht die Map als Ganzes. Reservierte Keys: `0` = `n` (normativ),
> `1` = Zweck-Tag (Trust-Flow-Spec §2), `2` = `bond_ref` (Trust-Flow-Spec §6.1); die Kodierung
> von `1` und `2` wird mit `03`/`05` festgelegt. Referenzvektor TV1 trägt `v = h'a1001864'` =
> `{0: 100}` — bei `D = 100` der Default `w = 1`.

### B.2 `02-trust-flow.md §3` — Knotenbudget präzisieren

**Alt:** „Knotenbudget `C(x) = C₀ · γ^{d(s,x)}` …"

**Neu:**

> - **Knotenbudget** `C(x) = ⌊ C₀ · γ^{d(s,x)} ⌋`, mit `γ = γ_num/γ_den ∈ (0,1)` und Seed-Budget
>   `C₀ > 0` bei `d = 0`. **Einmal am Ende abgerundet, nicht pro Schritt** — iteratives Runden
>   machte das Ergebnis von der Auswertungsreihenfolge abhängig. Es gilt `C(x) = 0` für
>   unerreichbare `x` und für alle `d` mit `C₀·γ^d < 1`.

**Distanz-Zeile ersetzen:**

> - **Distanz** `d(s,x)` = kürzeste Pfadlänge in Hops von Seed `s` zu `x` über dem **wirksamen**
>   Kantenset `E⁺ = { e ∈ E : cap(e) ≥ 1 }` (BFS). Unerreichbar ⇒ `d = ∞`. Wer keine
>   Kapazitätseinheit weiterreicht, reicht auch keine Position weiter. Die Definition ist
>   wohlfundiert: `cap(I→J)` hängt nur von `d(I)` ab, das feststeht, wenn die BFS `I` expandiert
>   — ein Durchlauf, kein Fixpunkt.

**Mehrfach-Anker ergänzen:**

> - **Ankerset statt einzelnem Seed.** Ist der Seed eine Menge (§6.3), gilt `d(x) = min_a d(a,x)`,
>   und die Quelle im Flussgraphen ist ein Super-Source `S*` mit ∞-Kanten auf jedes `a_in`. Die
>   interne Kante des Ankers liegt damit auf dem Pfad: sein Budget `C(a)` bindet auch auf der
>   Quellseite. Bei gültigem Budget ist das identisch zur Anbindung an `a_out`
>   (`Σ_e cap(e) ≤ C(a)`); es unterscheidet sich genau bei über-committetem Anker, und dort in
>   Richtung Unter-Vertrauen.

### B.3 `02-trust-flow.md §3` — Blockzitat „Warum Knoten- und nicht Kantenkapazität" ergänzen

Anhängen:

> **Nachtrag seit D1.** Gilt die Budgetregel, ist `Σ_e ⌊n_e·C(I)/D⌋ ≤ (Σn_e)·C(I)/D ≤ C(I)` — die
> interne Knotenkante ist dann nie **allein** bindend (Gleichheit ist möglich, striktes
> Überschreiten nicht), und die Schranke wird gleichermaßen von den Kanten-Caps getragen. Sie
> bindet ausschließlich bei über-committeten Knoten, und auch dort nur, wenn tatsächlich mehr
> Fluss ankommt als `C(I)`. Das entwertet die Konstruktion nicht: sie ist weiterhin nötig, um
> Über-Commitment überhaupt sichtbar zu machen, und der Einheitskapazitäts-Lauf (§8) lebt
> vollständig auf ihr.

### B.4 `02-trust-flow.md §3.1` — vier Ergänzungen

Nach der Gewichts-Definition:

> **Aggregation je `(I, J, N)`.** Mehrere Vouches derselben Identität auf dasselbe Subjekt im
> selben Scope bilden **eine** Gruppe. Es zählen `n_budget = max n` über die Gruppenmitglieder im
> Budget-Set und `n_kante = max n` über die im Aktiv-Set; die Kante trägt
> `cap(I→J) = ⌊n_kante·C(I)/D⌋`, das Budget prüft `Σ_J n_budget ≤ D`. **Maximum, nicht Summe** —
> sonst wäre die bloße Erneuerung eines Vouch ein selbst-validierender Beweis gegen den eigenen
> Autor (§6.2), und zwei aktive Vouches auf dasselbe Subjekt trügen doppelte Kapazität bei
> einfachem Budget.

> **Out-Degree folgt aus dem Budget.** Aus `n ≥ 1` und `Σn ≤ D` folgt: höchstens `D` gleichzeitig
> bebürgte **Subjekte** pro Identität und Scope — gezählt werden Gruppen im Budget-Set, nicht
> Claims. Aus `cap ≥ 1 ⟺ n·C(I) ≥ D` folgt schärfer `wirksame Out-Degree(I) ≤ min(D, C(I))`. Bei
> `D ≥ C₀` (§8) bindet stets `C(I)`: **die Zahl der Menschen, für die man bürgen kann, ist die
> eigene Position** — keine gezählte Rationierung, sondern dieselbe positionale Größe wie alles
> andere in dieser Schicht.

Tabelle „Zwei Mengen" — Zeile Budget-Set ersetzen:

> | **Budget-Set** | nicht abgelaufen (**widerrufen, supersediert und `pending` eingeschlossen**), aggregiert je `(I, J, N)` über `max n` | Prüfung `Σ n_budget ≤ D` |

Absatz „Widerruf und Freigabe" ersetzen:

> **Widerruf, Supersede und Freigabe.** Ein Widerruf stoppt den Fluss sofort (die Kante verlässt
> das Aktiv-Set) und beendet die Haftung des Bürgen — **gibt das Budget aber nicht frei**. Für
> Supersede gilt dasselbe. Frei wird Budget erst bei `t_exp` (§6.2), und erst, wenn **alle**
> Vouches der Gruppe `(I, J, N)` abgelaufen sind. **Kein selbst-bezüglicher Lebenszyklus-Akt gibt
> Budget frei; Budget folgt der Uhr, nicht dem Willen des Autors.** Andernfalls ließe sich eine
> lange Laufzeit — das stärkste Signal — beliebig oft per Supersede zurückholen, und die
> Knappheit aus D3 wäre eine Formalität. Weil innerhalb einer Gruppe das **Maximum** zählt und
> nicht die Summe, sind Erneuerung und Herabstufung dennoch frei: Ein Autor kann seine Aussage
> jederzeit korrigieren, er kann nur ihr Gewicht nicht vorzeitig anderswo einsetzen. Budget ist
> vorwärtsgerichtet, Haftung rückwärtsgerichtet; sie folgen verschiedenen Uhren. Eine
> Nachhaftungsfrist wäre nicht auswertbar, weil sie eine Cross-Chain-Zeitordnung verlangte, die
> es nicht gibt.

Neuer Absatz am Ende:

> **Unlesbares oder ungültiges `n`.** Ist `v` keine CBOR-Map, fehlt der Key `0`, ist sein Wert
> kein `uint`, oder liegt `n` außerhalb `[1, D]`, trägt dieser Vouch **keine Kante** und **keinen
> Budget-Beitrag**. Weitere Keys sind unschädlich — geprüft wird Key `0`, nicht die Map als
> Ganzes. Kein Beitrag, weil eine geratene Zahl eine Falschbeschuldigung wegen Über-Commitment
> erzeugen könnte; keine Kante, weil das Unter-Vertrauen ist. Beides ist die sichere Richtung, in
> verschiedene Richtungen.

### B.5 `02-trust-flow.md §4` — Definition, Herleitung, drei neue Blöcke

**B.5a — Definitionszeile ersetzen:**

> **Definition.** `trust(s → T) = maxflow(s_in → T_in)` im gespaltenen, kapazitierten Graphen. Die
> Quelle hängt an `s_in`, damit die interne Kante des Ankers — sein Budget `C(s)` — auf dem Pfad
> liegt. Bei gültigem Budget ist das identisch zur Anbindung an `s_out`, weil `Σ_e cap(e) ≤ C(s)`
> gilt; es unterscheidet sich genau dann, wenn der Anker über-committet ist, und dann in Richtung
> Unter-Vertrauen.

**B.5b — Herleitung ersetzen:**

> **Herleitung.** Führe einen Super-Sink `T*` mit ∞-Kanten von jedem `gᵢ_in` ein — an `T_in`,
> nicht an `T_out`, sonst zählte die interne Kante des Ziels mit und die Multi-Sink-Semantik wiche
> von der Einzelabfrage ab. Dann ist der simultane Gesamtfluss in `S` gleich
> `maxflow(s_in → T*)`. Nach dem Max-Flow-Min-Cut-Theorem ist das gleich der minimalen
> Schnittkapazität. Jeder Pfad von der Quelle nach `T*` passiert einen ehrlichen Grenzknoten `h`
> — **einschließlich des Ankers selbst** —, dessen Durchsatz durch seine interne Kante `C(h)`
> gedeckelt ist. Also `maxflow(s → T*) ≤ Σ_{h ∈ Grenze} C(h)`. Die endlichen Kantenkapazitäten
> `⌊n·C(·)/D⌋` aus §3.1 können den Fluss nur weiter **senken**, nie anheben; die Schranke gilt
> daher erst recht. ∎
>
> Hinge die Quelle an `a_out`, wäre der Satz **falsch**: drei Kanten mit `n = D` von einem Anker
> mit `C₀ = 16, D = 4` tragen je `⌊4·16/4⌋ = 16` und simultan 48 gegen eine behauptete Schranke
> von 16. Die Anbindung an `a_in` ist kein Konventionsdetail, sondern die Voraussetzung des
> Beweises.

**B.5c — nach dem Korollar einfügen:**

> **Schärfere Schranke.** Unter gültigem Budget gilt zusätzlich
> `maxflow(s → S) ≤ Σ_{h ∈ Grenze} Σ_{e Angriffskante von h} ⌊n_e·C(h)/D⌋ ≤ Σ_{h} C(h)`.
> Die Kanten-Caps sind die tatsächlich bindende Größe; `Σ C(h)` ist die schwächere, aber
> budget-unabhängige Form.

**B.5d — nach dem Blockzitat „Die Summe der Einzelabfragen ist nicht beschränkt" einfügen:**

> **Zwei unabhängige Divergenzursachen.** `Σ trust(s→Tᵢ)` übersteigt `maxflow(s→S)`, wenn (i) ein
> gemeinsamer Engpass stromaufwärts bindet, **oder** (ii) eine Einzelabfrage Knoten aus `S` als
> Zwischenknoten benutzt — im simultanen Lauf wird der Fluss dort schon an `gᵢ_in` absorbiert.
> Jede Ursache erzeugt für sich allein Divergenz (Golden Anchors: A nur (i), E nur (ii)); greift
> keine, sind beide Größen gleich (B, E₀). Wer nur einen der beiden Fälle testet, hat VR-02.1 halb
> getestet.

**B.5e — nach „Wirkung des Gewichts auf die Einzelabfrage" einfügen:**

> **Was `Σw ≤ 1` kostet — und was nicht.** Am kanonischen Testgraphen (Golden Anchors §3) senkt
> die Budgetregel den **simultanen** Fluss in die Sybil-Region **nicht**: 4 mit über-committetem
> Bürgen (Variante A), 4 mit gültigem Budget (E, F). Sie senkt allein die Summe der
> Einzelabfragen, und auch die nur von 12 auf 10. Der Ertrag liegt nicht in der Unterdrückung,
> sondern darin, dass A mechanisch beweisbar wird (Über-Commitment, §3.1) und F nicht. Das ist L2
> in Zahlen — wer `Σw ≤ 1` für eine Sybil-Abwehr hält, hat den Mechanismus falsch verstanden.
>
> **Die Angriffsform hängt nicht vom Verifizierer ab — die Schranke tut es.** Bei fester
> Sybil-Zahl ist eine gemischte Belegung (`n = 2,1,1` auf drei Ziele, `S` vernetzt) gegen
> **beide** Verifiziererformen optimal: Summe 10, simultan 4, drei Identitäten über einer Schwelle
> von 2. Es gibt keinen Trade-off zwischen Streuung und Konzentration, den ein Angreifer zu
> treffen hätte. Der Unterschied liegt allein beim Verifizierer: gegen die Summe der
> Einzelabfragen ist der Angriff **unbeschränkt**, weil `|S|` frei ist und jeder weitere
> erreichbare Sybil addiert; gegen den simultanen Fluss greift die Schranke dieses Abschnitts. Wer
> VR-02.1 verletzt, wählt nicht eine ungenauere Zahl — er wählt eine Größe ohne obere Schranke.

### B.6 `02-trust-flow.md §8` — fünf Änderungen

**`C₀`-Zeile ersetzen** (die alte Aussage ist seit D2 falsch):

> - `C₀` (Seed-Budget): skaliert die Leiter. **Nicht mehr verhältniserhaltend**, seit die
>   Kantenkapazität abrundet: bei `C₀ = 16` ist `⌊1·2/4⌋ = 0`, bei `C₀ = 160` ist `⌊1·20/4⌋ = 5`.
>   `C₀` bestimmt zusammen mit `D` den Granularitätsboden und damit, wie weit vom Seed noch
>   gebürgt werden kann.

**`D`-Zeile ersetzen:**

> - `D` (Nenner des Vouch-Gewichts, §3.1): bestimmt die Granularität von `w`. **Über die
>   Lebensdauer eines Scopes unveränderlich** — ein anderes `D` bedeutet einen neuen Scope, sonst
>   würden bestehende signierte Vouches still umbewertet. **SHOULD `D ≥ C₀`**, damit die
>   Out-Degree an der Position hängt (§3.1) und nicht an einer gezählten Grenze. Eine geschlossene
>   Kurzform der Kantenkapazität gibt es **nicht**: `⌊n·⌊C₀γ^d⌋/D⌋` ist doppelt gerundet und
>   lässt sich nur bei ganzzahligem `C₀γ^d` zu `⌊n·γ^d⌋` zusammenziehen (Gegenbeispiel
>   `C₀ = D = 16, γ = ⅔, d = 2, n = 9`: `3` gegen `4`).

**Granularitätsboden als neuer Punkt:**

> - **⚠️ Granularitätsboden.** `cap(I→J) = 0`, sobald `n·C(I) < D`. Ein Knoten mit kleiner
>   Kapazität kann nur noch für wenige — am Rand für genau einen — mit vollem Budget bürgen, oder
>   für niemanden. `D` schneidet die Peripherie ab, unabhängig von `γ`.

**Bootstrap-Warnung ersetzen:**

> - **⚠️ Kalibrierungs-Nebenbedingung (Bootstrap).** `Σw ≤ 1` macht die Frühphase eng. Für `f`
>   Gründer, `M` Neulinge, `m` Bürgen je Neuling und Admission-Schwelle `θ`:
>   ```
>   θ ≤ f · C₀ / M          (Kapazität — unabhängig von D und m)
>   D ≥ M · m / f           (Granularität — Out-Degree je Gründer)
>   ```
>   Beide Bedingungen sind unabhängig und beide bindend. Für `f = 3, C₀ = 16, M = 17` folgt
>   `θ ≤ 2`; `m = 2` liefert dieselbe Vertrauenshöhe wie `m = 1` bei doppelter Pfad-Disjunktheit
>   (die Rundung frisst den Unterschied — Redundanz ist dort gratis), `m = 3` kollabiert am
>   Granularitätsboden auf null. Die Kapazitätsbedingung ist dabei die **optimistische** Form:
>   nach Rundung sind von `f·C₀ = 48` Einheiten real nur 36 verteilbar (Golden Anchors §7).
>
> - **⚠️ Harte Reichweite.** Ab `d` mit `⌊C₀γ^d⌋ = 0` kann ein Mitglied **keinen** wirksamen Vouch
>   mehr tragen — gleich wie viel Budget es einsetzt und gleich wie viele Bürgen ein Kandidat
>   sammelt. Damit gilt `r_max = ⌊log_{1/γ} C₀⌋`, bei `C₀ = 16, γ = ½` also `r_max = 4` für die
>   Bürgschaftsfähigkeit und `5` für die Mitgliedschaft. Ein Nukleus mit `θ = 2` sättigt bei rund
>   **600 Mitgliedern** und Radius 5; wer mehr will, muss `C₀` oder `γ` ändern. Das ist die
>   quantitative Fassung von „maximal lokal" und keine Panne.

**Pfad-Disjunktheits-Punkt präzisieren:**

> Berechnung: derselbe Max-Flow mit **Einheitskapazitäten auf den internen Knotenkanten** und ∞
> auf den Vouch-Kanten — also **knoten**-disjunkt, nicht kantendisjunkt. Zwei Pfade durch denselben
> Bürgen sind ein Bürge. **Endpunkte werden nicht gespalten:** die internen Kanten der Anker
> tragen ∞, die des Ziels liegt ohnehin nicht auf dem Pfad (§4). Sonst wäre die Zahl von einem
> einzelnen Anker aus trivial 1.

**Neuer Punkt am Ende:**

> - **Geflaggte Autoren.** Ob ein Bürge mit `equivocation-flagged` oder erwiesenem
>   Über-Commitment noch Fluss trägt, ist Policy (`include_flagged`, Default *nein*). Die
>   Budgetrechnung ist davon **unberührt** — ein Flag darf die Grundlage nicht verschieben, auf
>   der es erkannt wurde.

### B.7 `07-decisions.md` Abschnitt G — Tabelle ergänzen

| Datei | Änderung | Quelle |
|---|---|---|
| `01-claim-atom.md §7.1` | `v`-Payload Key `0: n` normativ, Key-Vergabe; Float-Vorschlag entfernt; `t_exp` in Budget-Scopes Pflicht | D37, E-A |
| `02-trust-flow.md §2` | eine Kante je `(I, J)`, `max n`; keine Kante ohne gültiges `n` | D40, D37 |
| `02-trust-flow.md §3` | `⌊·⌋` bei `C`; BFS über `E⁺`; Ankerset und Super-Source an `a_in` | D28, D31, D36 |
| `02-trust-flow.md §3.1` | Aggregation je `(I,J,N)`; Out-Degree aus Budget; Budget-Set inkl. `superseded`; ungültiges `n` | D40, D33, D38, D37 |
| `02-trust-flow.md §4` | Definition auf `s_in`; Super-Sink an `T_in`; schärfere Schranke; zwei Divergenzursachen; Angriffsform | D31, D30 |
| `02-trust-flow.md §8` | `C₀` nicht verhältniserhaltend; `D` scope-fest + SHOULD `≥ C₀`, keine Kurzform; Granularitätsboden; Bootstrap-Ungleichungen; `r_max`; knoten-disjunkt mit Endpunkt-Regel; `include_flagged` | D28, D32–D35, D39 |
| Repo-Wurzel | `02-golden-anchors.md` aufnehmen | J |

### B.8 `07-decisions.md` Abschnitte E und I — Nachträge

Abschnitt **E-B**, unter der Tabelle ergänzen (das Register wird nicht umgeschrieben, nur
weitergezeigt):

> **Korrigiert durch D38 und D40:** Das Budget-Set schließt `superseded` und `pending` ein und
> wird je `(I, J, N)` über `max n` aggregiert. Die Tabelle oben gibt den Stand vor der
> Golden-Anchor-Rechnung wieder.

Abschnitt **I** ergänzen:

> - `D` (D2) ist für den `example-nucleus` auf **100** festgelegt, damit TV1 byte-identisch bleibt
>   und `n` sich als Prozent liest. `C₀ ≤ 100` folgt aus D34. Die konkreten Werte für `c`, `m`,
>   `t_ref`, `k_slash` bleiben offen.

---

## Teil C — Reihenfolge

Layer 01 ist bereits auf `main` (`1993486..2715859`, 61 grün). Die Begründung für die alte
Schritt-3-vor-4-Regel — die Spec-Änderung an `01 §7.1` soll gegen einen Codestand landen, in dem
TV1 existiert und grün ist — ist damit erfüllt.

1. `.gitignore` um `.cursorrules` und `mensch_als_republik.egg-info/` ergänzen
2. Testhygiene: `rootdir` und Importmodus in `pyproject.toml` festnageln (eigener Commit)
3. **TV1-Zusicherung** `cbor2.loads(TV1.v) == {0: 100}` als Test ergänzen — additiv, verträgt sich
   mit dem Einfrieren von Layer 01. Ohne sie belegt „61 grün" die Byte-Neutralität von D37
   **nicht**: kein bestehender Test kodiert je den alten Float-Vorschlag, `v` ist im Atom opake
   Bytes. Grün wäre a priori garantiert.
4. Teil A und B anwenden, Commit je Block auf `spec/02-vouch-weight-and-sybil-fix`
5. `02-golden-anchors.md` auf denselben Branch
6. `spec/02-vouch-weight-and-sybil-fix` → `main`
7. `impl/02-trust-flow` von `main` abzweigen
8. `02a-maxflow`-Prompt laufen lassen

---

## Was danach noch offen ist

- Ist `Σn > D` im Sinne von `05 §4` terminal oder kurierbar? (Policy, Abschnitt I). Mit D40 ist
  die Frage schärfer geworden: Über-Commitment setzt jetzt einen Vorsatz voraus, den eine
  Fehlbedienung nicht mehr simulieren kann.
- `ERR_OVERCOMMIT` ist eine **Layer-02**-Fehlerklasse, kein Reject-Code des Atoms. Layer 01 bleibt
  bei elf Codes und wird nicht angefasst.
- `example-nucleus.md` anlegen: `D = 100`, `C₀ ≤ 100`, `k_slash` niedrig mit Begründung aus
  Abschnitt F
- Zweiter Spec-Durchgang für `05`, `06`, `04`, `00`, `VISION` gemäß Änderungsliste G. `05 §3`
  braucht Über-Commitment als Stufe-3-Auslöser — mit dem Zusatz aus D40, dass die Prüfung über
  Gruppenmaxima läuft.
- `02b-pagerank`: liest `w` (D27), Normalisierung über `Σw` dort **erlaubt**, weil `§5` keine
  harte Schranke trägt. `w` ist dort `n_kante/D` je Gruppe, nicht je Claim.
