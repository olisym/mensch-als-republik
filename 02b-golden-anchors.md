# Golden Anchors — Layer 02b (PageRank-Relaxation, `02 §5`)

Revision 2 · Status: gerechnet, zweifach gegengerechnet und gegen die Implementierung
geprüft · gilt gegen `02-trust-flow.md` nach Anwendung von D45–D54
Zweck: normative Testvektoren für `02b-pagerank`. Alle Werte exakt, ganzzahlig, ohne Rundung.

Diese Datei setzt `02-golden-anchors.md` (Rev 3) fort. Konventionen werden von `K9` an
weitergezählt, Invarianten als `PR-INV-n` geführt, damit `INV-1`–`INV-8` der harten Sicht
unberührt bleiben.

## Änderungen gegenüber Revision 1

| # | Was | Warum |
|---|---|---|
| 1 | **Massenschranke in Produktform** (`K9`, `K14`, `§1`, `§9`, `§10`) | `Δ − Δ // 2^K` ist nur für `α = ½` exakt — und `α = ½` ist der Default, also der einzige Wert, unter dem der Fehler unsichtbar bleibt (D54) |
| 2 | **Knotenmenge des Ergebnisses in `§1` ergänzt** | fehlte ganz; „alle mit `u > 0`" wäre falsch gewesen, weil bei kleinem `K` erreichbare Knoten legitim `0` tragen |
| 3 | **`§10.1`: Schnittstelle der geteilten Ableitung** auf `Derivation(bfs, findings)` nachgezogen | die Tupelform hätte einen der 144 eingefrorenen `02a`-Tests angefasst; die Implementierung hat die bessere Form gewählt |
| 4 | **`§11`: offener `PR-INV-9`-Vektor begründet**, zwei weitere offene Vektoren ergänzt | der isolierte zweite Anker ist der einzige Fall, in dem eine falsche und eine richtige Begründung ununterscheidbar sind |
| 5 | `§9`: `PR-INV-1` auf `2⁵ = 32` Teilgraphen festgenagelt, `PR-INV-4` um die tragende Assertion ergänzt | beide Tests waren in der ersten Fassung schwächer als ihre Behauptung |

---

## 0. Festgelegte Konventionen

| ID | Frage | Entscheidung |
|---|---|---|
| K9 | Normalisierung von `P` | **Sub-stochastisch**, `P[J][I] = n_kante(I,J) / D`. Keine Normalisierung über `Σw`, keine Rückführung des Defizits. `mass ≤ Δ − \|A\|·D^K·(b−a)^K` (D45, D54). |
| K10 | Arithmetik | Exakte Integer-Zähler `u` über festem Nenner `Δ_K = \|A\|·(b·D)^K`. Kein `Fraction`, kein `float`, **keine Rundung an keiner Stelle** (D46). |
| K11 | Abbruch | Feste Rundenzahl `K`, `t₀ = 0`. `t_K` ist die abgeschnittene Neumann-Reihe; Fehler `≤ (1−α)^K`, monoton von unten (D47). |
| K12 | `α` | `α = 1 − γ` als Profilkopplung. Für `γ = ½` also `α = ½`, `a = 1`, `b = 2` (D48). |
| K13 | Kantensatz | **Identisch zu `§4`**: Gruppen-Aggregation `max n` (D40), `E⁺`-Filter (D36), Flag-Anwendung (D39). **Kein Knoten-Splitting.** Das Budget-Set spielt keine Rolle (D49). |
| K14 | Über-Commitment | **Kein Clamp.** `Σn_I > D` bleibt unangetastet; `mass > Δ − \|A\|·D^K·(b−a)^K` ist ein einseitiger Indikator (D53, D54). |
| K15 | Ankerset | `e_a = 1/\|A\|` gleichverteilt. Ein zusätzlicher Anker kann einen Wert **senken** — anders als in `§4` (D51). |
| K16 | Oberfläche | Eigenes Modul, eigener Name, eigener Rückgabetyp. Nicht `trust`, nicht `TrustResult` (D52). |

---

## 1. Die Norm in fünf Zeilen

Mit `α = a/b`, Ankerset `A`, wirksamem Kantensatz `E⁺` und Gruppengewichten `n_kante`:

```
u_0[J]      = 0
u_{k+1}[J]  = a·D·(b·D)^k · [J in A]  +  (b−a) · Sum_{(I,J) in E+} u_k[I] · n_kante(I,J)
t[J]        = u_K[J] / Delta_K            Delta_K = |A| · (b·D)^K
```

Ein Integer-Vektor, `K` Durchläufe, **eine Multiplikation und eine Addition je Kante**.

**Knotenmenge des Ergebnisses:** `A` vereinigt mit allen Endpunkten von `E⁺`. Wer nicht darin
liegt, erscheint **gar nicht** — nicht als `0` (PR-INV-7). Die Menge ist **strukturell**
definiert und hängt **nicht** von `K` ab: bei kleinem `K` tragen erreichbare Knoten legitim
`u = 0`, ohne aus dem Ergebnis zu fallen. Nur so ist PR-INV-8 über `K` hinweg formulierbar.

**Leeres Ankerset ist keine gültige Anfrage.** `Δ = |A|·(bD)^K` wäre `0` und der berichtete
Bruch `u/Δ` damit `0/0`. Die Implementierung weist es zurück, statt schweigend Unsinn zu
liefern. `§4` unterscheidet sich hier legitim: dort ist Max-Flow aus leerer Quelle trivial und
korrekt `0`.

### Herleitung

`§5` in Iterationsform mit `t₀ = 0`:

```
t_{k+1} = alpha · e_s + (1 − alpha) · P^T · t_k
```

Setze `u_k = Δ_k · t_k` mit `Δ_k = |A|·(bD)^k`. Der Streckfaktor je Runde ist
`Δ_{k+1}/Δ_k = bD`. Damit:

- Restart-Term: `bD · Δ_k · (a/b) · e_J = a·D·Δ_k/|A| = a·D·(bD)^k` für `J ∈ A`, sonst `0`.
- Transfer-Term: `bD · ((b−a)/b) · Σ_I u_I·n_IJ/D = (b−a) · Σ_I u_I·n_IJ`.

Beide Terme sind ganzzahlig, und `|A|` kürzt sich aus der Rekursion heraus — es steht nur
noch im Nenner. Es gibt an keiner Stelle eine Division und damit keine Rundungsrichtung.

### Warum kein Leck

`§5` in der Fassung mit Rückführung des Defizits auf den Restart-Vektor hat den Fixpunkt
`t = (α + (1−α)·ℓ(t)) · T · e_s` mit `T = (I − (1−α)Pᵀ)⁻¹`; ohne Rückführung
`t' = α · T · e_s`. Weil `ℓ(t)` ein **Skalar** ist, gilt `t = (s/α)·t'` — beide Fixpunkte
sind proportional. Die Rückführung ändert nur die Normierung, nicht die Ordnung und nicht
ein einziges Verhältnis. Sie kostet einen Rang-1-Term je Iteration und ein `min()` je Knoten.

Sie ist zudem ein Informationsverlust: ohne Rückführung ist `1 − Σt` das **ungenutzte
Budget**, sichtbar als Zahl (§5 dieser Datei).

Dangling Nodes sind damit kein Fall: ein Knoten ohne ausgehende Kanten in `E⁺` reicht nichts
weiter, und die bei ihm angekommene Masse bleibt bei ihm.

### Fehlerschranke

Mit `t₀ = 0` ist

```
t_K = alpha · Sum_{i=0}^{K−1} (1 − alpha)^i · (P^T)^i · e_s
```

die abgeschnittene Neumann-Reihe. Bei sub-stochastischem `P` gilt
`||t_K − t_*||_1 ≤ (1 − alpha)^K`, und die Folge ist **monoton wachsend** in `K` — jeder
Abbruch ist eine Untergrenze und damit die sichere Richtung.

**Normativ ist `t_K`, nicht `t_*`.** Der Fixpunkt ist die Motivation, nicht die Definition.
Nur so ist der Wert exakt und byte-reproduzierbar.

### Massenbilanz als Über-Commitment-Indikator

Bei budgetgültigem Kantensatz ist `P` spaltenweise durch `1` beschränkt, also per Induktion
`Σt_k ≤ 1 − (1−α)^k`. Ganzzahlig ausgeschrieben ist das ein **Produkt ohne Division**, weil
sich `b^K` vollständig gegen `Δ` kürzt (D54):

```
Delta * (1-alpha)^K  =  |A| * (b*D)^K * (b-a)^K / b^K  =  |A| * D^K * (b-a)^K

mass  <=  Delta - |A| * D^K * (b-a)^K
```

Diese Form ist für **jedes** `α` exakt. `Δ − Δ // 2^K` ist es nur für `α = ½` — und das ist
der Default (D48), also der einzige Wert, unter dem der Fehler unsichtbar bleibt.
Umkehrschluss:

```
mass > Delta - |A| * D^K * (b-a)^K   ==>   ein einbezogener Autor ist ueber-committet
```

Einseitig: kein Falschalarm, nur Unter-Erkennung. Dieselbe Richtung, die `§3.1` für das
beobachtete `Σw` schon festhält (D3).

---

## 2. Testprofil `TP-02-PR`

```
gamma = 1/2   C0 = 16   D = 4   alpha = 1/2 (a = 1, b = 2)   K = 20
Scope N = "test"   now = 1000   t_exp = 5000
|A| = 1 (Anker ALICE)
Delta = 1 · (2·4)^20 = 8^20 = 2^60 = 1152921504606846976
```

`Δ = 2⁶⁰` liegt unter `2⁶³` — die Vektoren sind auch in einer Sprache ohne Bigints
darstellbar. Das ist kein Zufall, sondern der Grund für `K = 20` gegenüber `K = 24`:
`(1−α)^20 = 2⁻²⁰` ist als Genauigkeit reichlich, und der Nenner bleibt maschinenwortgroß.

Graph, Varianten und `E⁺` sind **unverändert** aus `02-golden-anchors.md §1–§2`
zu übernehmen. `d` und `C` sind dieselben; `§5` liest sie nur über den `E⁺`-Filter,
nie als Faktor.

---

## 3. Anker PR-1 — die Varianten

Alle Werte bei `include_flagged = True`, gekürzt als Bruch und als Integer-Zähler über `Δ`.

| Var | ALICE | BOB | CAROL | `t(g1)` | `t(g2)` | `t(g3)` | `Sigma t` |
|---|---|---|---|---|---|---|---|
| **B** | `1/2` | `1/4` | `1/8` | `1/64` | `1/64` | `1/64` | `59/64` |
| **C** | `1/2` | `1/4` | `1/8` | `131071/4194304` | dito | dito | `4063229/4194304` |
| **D** | `1/2` | `1/4` | `1/8` | `17/64` | `17/64` | `17/64` | **`107/64`** |
| **E** | `1/2` | `1/4` | `1/8` | `1/16` | `1/64` | `1/64` | `31/32` |
| **E0** | `1/2` | `1/4` | `1/8` | `1/16` | — | — | `15/16` |
| **F** | `1/2` | `1/4` | `1/8` | `6871903983/137438953472` | `10307834129/274877906944` | dito | `1048575/1048576` |
| **A** | `1/2` | `1/4` | `1/8` | `1/16` | `1/16` | `1/16` | **`17/16`** |

Integer-Zähler über `Δ = 2⁶⁰` (das, was die Implementierung produziert):

| Var | `u(ALICE)` | `u(BOB)` | `u(CAROL)` | `u(g1)` | `u(g2)` | `u(g3)` |
|---|---|---|---|---|---|---|
| B | `576460752303423488` | `288230376151711744` | `144115188075855872` | `18014398509481984` | dito | dito |
| C | dito | dito | dito | `36028522141057024` | dito | dito |
| D | dito | dito | dito | `306244774661193728` | dito | dito |
| E | dito | dito | dito | `72057594037927936` | `18014398509481984` | `18014398509481984` |
| E0 | dito | dito | dito | `72057594037927936` | — | — |
| F | dito | dito | dito | `57645708727025664` | `43234189918601216` | `43234189918601216` |
| A | dito | dito | dito | `72057594037927936` | dito | dito |

Der Rumpf `ALICE 2⁵⁹ / BOB 2⁵⁸ / CAROL 2⁵⁷` ist in allen Varianten identisch — er hängt
nicht davon ab, was hinter CAROL passiert. Das ist die Gegenprobe darauf, dass die
Rekursion vorwärts läuft und kein Fixpunktlöser dahintersteckt.

### Rechenwege

Die azyklischen Ketten sind **von Hand nachrechenbar**:

```
t(ALICE) = alpha                                  = 1/2
t(BOB)   = (1−alpha) · t(ALICE) · (4/4)           = 1/4
t(CAROL) = (1−alpha) · t(BOB)   · (4/4)           = 1/8
t(g)  [B]= (1−alpha) · t(CAROL) · (1/4)           = 1/64
```

**C** hat einen Zyklus in `S`. Fixpunkt: `x = ½·(⅛·¼ + 2x·½) = 1/64 + x/2 ⇒ x = 1/32`.
Der abgeschnittene Wert ist `131071/4194304 = 1/32 − 2⁻²²`, also `2¹⁷−1` über `2²²`.
Die Differenz zum Fixpunkt ist der Abschnittsfehler und **gehört zur Definition**.

**D** ist der Vektor, der `K14` trägt. Die `gᵢ` sind über-committet (`Σn = 8 > 4`), `P` ist
in diesen Spalten nicht mehr sub-stochastisch, und die Relaxation **erzeugt Masse**:
`Σt = 107/64 > 1`. `§4` sagt für dieselbe Variante `3/3/3` — identisch zu C (INV-5: das
Über-Commitment innerhalb `S` kauft dem Angreifer null). Die schnelle Sicht sagt: es kauft
das Achtfache. Das ist keine Panne, sondern die dokumentierte Grenze der Relaxation, und der
Default `include_flagged = False` entfernt den Fall (§4 dieser Datei).

**E** — `d(g₂) = d(g₃) = 4`, `C = 1`, vier der sechs `S`-internen Kanten sind subgranular und
liegen nicht in `E⁺`. Ohne den `E⁺`-Filter kämen sie zurück und `g₂`/`g₃` stiegen. Der Vektor
prüft `K13`.

**E0** — `g₂`, `g₃` sind unerreichbar und tauchen im Ergebnisvektor **gar nicht** auf.
„Neuling ≈ 0" aus `§4` wird in `§5` zu **exakt 0**.

**F** — der schärfste Ordnungsvektor. Fixpunkte: `g₁ = 1/20`, `g₂ = g₃ = 3/80`, Verhältnis
**exakt 4:3** — dasselbe Verhältnis, das `§4` mit `4/3/3` liefert. Zusätzlich schöpfen hier
alle Knoten ihr Budget voll aus, also `Σt = 1 − 2⁻²⁰ = 1048575/1048576`, **exakt** die
Fehlerschranke. Der empfindlichste Einzeltest der ganzen Datei: jede Schludrigkeit in der
Rekursion färbt ihn rot.

---

## 4. Anker PR-2 — Flag-Läufe (D39, `K14`)

| Lauf | `t(g1/g2/g3)` | `Sigma t` |
|---|---|---|
| **A**, `include_flagged = True` | `1/16` je | `17/16` |
| **A**, `include_flagged = False` | *nicht im Vektor* | `7/8` |
| **D**, `include_flagged = True` | `17/64` je | `107/64` |
| **D**, `include_flagged = False` | `1/64` je | `59/64` |

*Test:* `D(False)` ist **byte-gleich mit `B`** — Vektor und Summe. Der über-committete
Knoten sitzt in `S`, seine Kanten fallen weg, und übrig bleibt genau der isolierte Fall.

*Test:* `A(True)` und `D(True)` sind die einzigen Läufe mit `Σt > 1 − 2⁻²⁰`. In allen
budgetgültigen Läufen gilt die Schranke.

---

## 5. Anker PR-3 — Gruppen-Aggregation (D40, INV-6)

Basis: Variante B, zwei Claims der Gruppe `(CAROL, g₁, N)`.

| Fall | `n_kante` | `t(g1)` | `t(g2)` | `t(g3)` | `Sigma t` |
|---|---|---|---|---|---|
| Erneuerung (V1 supersediert, V2 aktiv) | 2 | `1/32` | `1/64` | `1/64` | `15/16` |
| beide aktiv | 2 | `1/32` | `1/64` | `1/64` | `15/16` |
| Herabstufung | 1 | `1/64` | `1/64` | `1/64` | `59/64` |

*Test:* Erneuerung und „beide aktiv" liefern **identische Vektoren**. Das ist INV-6 in der
schnellen Sicht: `§5` liest `n_kante` als Gruppenmaximum, nicht je Claim und nicht als Summe.
Eine Implementierung, die je Claim eine Kante zieht, liefert für die Erneuerung `n = 4` und
damit `t(g₁) = 1/16`.

*Test:* Die Herabstufung wirkt **sofort** (`n_kante` fällt auf 1), obwohl `n_budget` bis
`t_exp` bei 2 bleibt. Fluss folgt dem Willen, Budget folgt der Uhr — auch hier.

---

## 6. Anker PR-4 — `TP-FAN` (kein Knoten-Splitting, `K13`)

```
ALICE -> BOB n=2      ALICE -> BOB2 n=2       (Sigma n = 4)
BOB   -> X   n=4      BOB2  -> X    n=4       (je Sigma n = 4)
```

| Knoten | `t` | `u` über `Δ` |
|---|---|---|
| ALICE | `1/2` | `576460752303423488` |
| BOB | `1/8` | `144115188075855872` |
| BOB2 | `1/8` | `144115188075855872` |
| X | `1/8` | `144115188075855872` |
| | `Σt = 7/8` | |

*Test:* `t(BOB) == t(BOB2)` exakt (Symmetrie). *Test:* `t(X) == 1/8` — über den
**gespaltenen** Graphen aus `02a` fällt der Wert anders aus, weil jeder Pfad einen
zusätzlichen Knoten durchläuft und damit einen weiteren `(1−α)`-Faktor bekäme. Das ist der
Vektor, der `K13`s letzten Satz prüft: `02b` teilt die Ableitung mit `02a`, **nicht** die
Split-Konstruktion.

Handrechnung: `t(BOB) = ½·½·(2/4) = 1/8`; `t(X) = ½·(2·⅛·(4/4)) = 1/8`.

---

## 7. Anker PR-5 — Leck (ungenutztes Budget)

Ein einzelner Vouch `ALICE → BOB` mit `n = 1` bei `D = 4`:

| Knoten | `t` |
|---|---|
| ALICE | `1/2` |
| BOB | `1/16` |
| | `Σt = 9/16` |

ALICE setzt ein Viertel ihres Budgets ein, also erreicht BOB ein Viertel dessen, was er bei
`n = D` bekäme (`1/4`). **Die fehlende Masse ist das ungenutzte Budget.** Genau das ist die
Eigenschaft, die die spaltenstochastische Fassung nicht hat: dort wäre `t(BOB) = 1/4`, weil
die Normalisierung den absoluten Pegel von `w` löscht, sobald der Autor nur eine Kante trägt.

*Test:* `t(BOB) == 1/16` und nicht `1/4`. **Der Vektor, der D45 gegen die alte Fassung von
D27 entscheidet.**

---

## 8. Anker PR-6 — `TP-BOOT`

```
gamma = 1/2   C0 = 16   D = 24   alpha = 1/2   K = 20
A = {F0, F1, F2} (drei Gruender, |A| = 3)
17 Neulinge, je m = 2 Buergen, n = 2       cap = floor(2·16/24) = 1 >= 1
Delta = 3 · 48^20 = 12645791069395286513294994705481728
```

Kantenverteilung 11/12/11 über die Gründer (34 Kanten), `Σn = 22/24/22 ≤ 24`.

| Klasse | `t` | `u` über `Δ` |
|---|---|---|
| Gründer (alle drei) | `1/6` | `2107631844899214418882499117580288` |
| Neulinge (alle 17) | `1/72` | `175635987074934534906874926465024` |
| | `Σt = 53/72` | |

Handrechnung: `t(F) = α/|A| = 1/6`; `t(N) = ½ · 2 · (1/6) · (2/24) = 1/72`.

*Test:* Die **asymmetrische** Kantenverteilung (11/12/11) wirkt sich **nicht** aus — die
Gründer haben keine eingehenden Kanten und tragen nur den Restart. Unter der
spaltenstochastischen Fassung wäre das anders: dort hinge der Anteil je Kante an der
Out-Degree, und `F1` verteilte weniger je Neuling als `F0` und `F2`.

*Test:* `min(t Gründer) > max(t Neuling)`, strikt.

---

## 9. Abgeleitete Invarianten (als Tests zu implementieren)

**PR-INV-1 — Monotonie (`§7`) gilt in der schnellen Sicht.**
Entfernen einer beliebigen Kante senkt jeden `t`-Wert oder lässt ihn gleich. Nie Anstieg.
*Test:* alle `2^|E| = 2⁵ = 32` Teilgraphen von B, erschöpfend — **einschließlich der
Rumpfkanten** `ALICE→BOB` und `BOB→CAROL` —, und paarweise über alle `sub ⊆ sup`, nicht nur
gegen den vollen Graphen.
Gerechnet: **0 Verletzungen** unter K9; **9 Verletzungen** unter spaltenstochastischer
Normalisierung. Das ist der empirische Beleg für D45 und der einzige Test, der unter der
alten Fassung von `§5` gar nicht existieren könnte.

**PR-INV-2 — Massenbilanz.** `mass ≤ Δ − |A|·D^K·(b−a)^K` für jeden budgetgültigen
Kantensatz, mit Gleichheit genau dann, wenn jeder erreichte Knoten sein Budget voll ausschöpft
und keine Kante subgranular ist. Die Schranke ist als **Produkt** zu schreiben, nie als
`Δ − Δ // 2^K` — letzteres ist nur für `α = ½` exakt (D54).
*Test:* F liefert exakt `1048575/1048576`; B, C, E, E0 liegen strikt darunter; A und D
(jeweils `True`) liegen darüber und sind die einzigen.

**PR-INV-3 — Über-Commitment-Indikator ist einseitig.**
`mass > Δ − |A|·D^K·(b−a)^K ⇒ ein einbezogener Autor ist über-committet.` Die Umkehrung gilt
nicht.
*Test:* A und D mit `True` schlagen an; D mit `False` nicht, obwohl die `gᵢ` weiterhin
über-committet sind (ihre Kanten sind nur nicht im Lauf). Kein Falschalarm in B, C, E, E0, F.

**PR-INV-4 — Der Kantensatz ist der von `§4`.** Für jede Variante und beide Flag-Werte ist
der Kantensatz, über den `§5` rechnet, byte-gleich mit dem, den `§4` nach `E⁺`- und
Flag-Anwendung benutzt.
*Test:* die tragende Assertion ist der **Identitätsvergleich der Funktionsobjekte** — `derive`
in `flow` ist dasselbe Objekt wie `derive` in `relax`. Er kann nicht zufällig grün sein, ein
Datenvergleich schon. Vergleiche der Knotenmengen sind Zusatz und prüfen nur, dass `rank()`
die Menge korrekt aus `edges` bildet.
⚠️ Die Gleichheit gilt nur **innerhalb eines Parametersatzes**: nichts erzwingt, dass
`RelaxParams.base` denselben `TrustParams` entspricht, mit dem `trust()` läuft. Verschiedene
Parameter sind verschiedene Graphen und legitim — „ein Graph, zwei Sichten" sagt dann nur
nichts mehr aus.

**PR-INV-5 — Findings sind identisch.** `OVERCOMMITTED_AUTHOR`, `INVALID_VOUCH_WEIGHT`,
`UNPARSABLE_VOUCH_PAYLOAD` und `SUBGRANULAR_VOUCH` sind byte-gleich zwischen `§4`- und
`§5`-Lauf bei gleichen Parametern. Sie entstehen vor der Sichttrennung.

**PR-INV-6 — Aggregation ist idempotent.** Siehe §5: Erneuerung und „beide aktiv" liefern
identische Vektoren.

**PR-INV-7 — Unerreichbares ist exakt null.** Ein Knoten ohne eingehenden Pfad in `E⁺` aus
`A` erscheint nicht im Ergebnis bzw. trägt `u = 0`. Kein Epsilon, keine Näherung.
*Test:* E0 (`g₂`, `g₃`), sowie EVE in jeder Variante.

**PR-INV-8 — Monotonie in `K`.** `u_K[J] ≤ u_{K+1}[J]·(bD)⁻¹`-normalisiert, d. h.
`t_K[J] ≤ t_{K+1}[J]` für alle `J`. Jeder frühere Abbruch unter-vertraut.
*Test:* `K = 1..20` für B und F, keine Senkung.

**PR-INV-9 — Anker-Asymmetrie ist real und benannt (D51).** Das Hinzufügen eines zweiten
Ankers kann einen `t`-Wert **senken**, während `§4` bei zusätzlichen Ankern nie sinkt.
*Test:* `TP-02` mit `A = {ALICE}` gegen `A = {ALICE, ALICE₂}`, wobei ALICE₂ isoliert ist:
jeder Wert halbiert sich. Kein `§7`-Bruch — `§7` handelt von Kanten, nicht von Ankern.

---

## 10. Effizienzhinweise für `02b`

1. **Die Ableitung wird geteilt, nicht wiederholt.** Eine Funktion `derive()` liefert
   `Derivation(bfs, findings)`; `bfs` trägt Distanzen, Knotenkapazitäten und den `E⁺`-Satz mit
   `n_kante`. `trust()` liest daraus `node_capacity` für den Split; `rank()` liest
   **ausschließlich** `bfs.edges` und entpackt sie unmittelbar hinter dem Aufruf in eine
   lokale Variable. Dass `node_capacity` für `§5` in Reichweite liegt, ist eine Kopplung, die
   durch Konvention getragen wird und nicht durch den Typ (D49, K13, PR-INV-4).
2. **Kein Knoten-Splitting.** Der Split ist eine Max-Flow-Konstruktion für Knotenkapazitäten;
   `§5` hat keine. Wer den Split-Graphen wiederverwendet, bekommt verdoppelte Pfadlängen und
   Werte, die nichts bedeuten (PR-INV-4, Anker PR-4).
3. **Adjazenz nach Ziel indizieren.** Die Rekursion summiert je `J` über eingehende Kanten;
   ein `dict[J] -> [(I, n)]`, einmal gebaut, `K`-mal durchlaufen.
4. **`a·D·(bD)^k` ist ein Präfix.** Einmal je Runde berechnen, nicht je Anker.
5. **`Δ` nicht kürzen.** Der gemeinsame Teiler wäre graphabhängig und machte Läufe
   untereinander unvergleichbar. Kürzen ist eine Anzeigehilfe für Tests, keine Kernfunktion.
6. **Kein `min`, kein `σ`, kein Dangling-Zweig.** Wer einen davon im Code findet, hat die
   Leckform implementiert.
7. **Cache-Schlüssel wie `02a`**, plus `(alpha, K)`. Der abgeleitete Graph ist derselbe.
8. **Die Massenschranke ist ein Produkt, keine Division.** `Δ − |A|·D^K·(b−a)^K`, einmal als
   Helfer, nicht an jeder Prüfstelle neu geschrieben (D54).

---

## 11. Forkstand

**Entschieden (D45–D54):** Normalisierungsform, Arithmetik, Abbruch, `α`, Kantensatz,
Clamp, Ankergewichtung, Oberfläche, Präzisierung von „nie über-vertrauend".

**Bewusst getragen:**

- **`§4` und `§5` sind nicht kommensurabel.** Fluss in Kapazitätseinheiten gegen stationäre
  Masse. „Nie über-vertrauend" ist eine Aussage über die **Signalkanäle** (`w`, `E⁺`,
  Gruppen-`max n`, Flag), nicht über die Werte (D50). Ein punktweiser Vergleich ist nicht
  formulierbar und darf nicht getestet werden.
- **Über-committete Autoren werden in `§5` überzeichnet** (Variante D, `Σt = 107/64`). Der
  Default `include_flagged = False` entfernt sie; `True` ist eine bewusste Entscheidung des
  Verifizierers. Ein Clamp wurde geprüft und **verworfen**, weil jede Form davon den Anteil
  einer Kante an die übrigen Kanten desselben Autors koppelt und damit D9 reaktiviert:
  bei Teilwissen greift der Clamp nicht, und fehlendes Wissen hübe Werte.
- **Der Abschnittsfehler gehört zur Definition.** `t_K` ist normativ, `t_*` ist Motivation.
  Variante C zeigt es: `1/32 − 2⁻²²` statt `1/32`.

**Offen, nicht blockierend:**

- Ob eine Policy `α` unabhängig von `γ` setzen darf, oder ob `K12` ein MUST wird. Bis dahin
  SHOULD, mit der Begründung aus D48 (`§5` darf nicht langsamer abklingen als `§3`).
- Ein Vektor für `PR-INV-9` mit einem **nicht** isolierten zweiten Anker. Der isolierte Fall
  zeigt die Asymmetrie, aber er ist der einzige, in dem „die `u` bleiben gleich" und „die
  Rekursion hängt nicht vom Ankerset ab" ununterscheidbar sind. Die zweite Aussage ist
  **falsch**: der Restart-Term wird je Anker addiert, und `|A|` kürzt sich allein aus dem
  Restart-Term heraus (D51, `02b-abnahme.md` §C.1).
- Ein Vektor für `α` in **nicht gekürzter** Form: `(a,b) = (1,2)` und `(2,4)` liefern
  verschiedene `Δ` und verschiedene `u`, aber denselben Bruch `u/Δ`. Nachgerechnet, ungetestet.
- Ein Vektor für `trust()` mit leerem Ankerset auf Variante A: `OVERCOMMITTED_AUTHOR` entsteht
  in Schritt 4 von `derive()`, vor der BFS, und muss auch ohne Anker erscheinen (INV-8). Nur
  `SUBGRANULAR_VOUCH` darf wegfallen (D44).
