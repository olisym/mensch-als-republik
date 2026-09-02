# Abnahme `02b-pagerank` — Befund und Nachzug

Stand: Implementierung vollständig, 214 Tests grün, die 144 aus `02a` unverändert, Layer 01
unangetastet.
Grundlage: `relax.py`, `derive.py`, die Diffs an `graph.py`/`flow.py`/`__init__.py`,
`pr02.py`, `test_pagerank_invariants.py`, `test_pagerank_leak.py`, `test_pagerank_fan.py`
sowie die drei Rückfragen des Implementierers.

## Urteil

**Der Code ist abnahmefähig.** Die Rekursion stimmt zeilengenau mit der Norm überein, die
Extraktion nach `derive.py` ist verhaltensneutral, und die vier Vektoren, die die
Entscheidungen tragen, prüfen mit Literalen:

| Vektor | erwartet | im Test | prüft |
|---|---|---|---|
| PR-5 (Leck) | `u(BOB) = 72057594037927936` | Literal, plus Gegenwert `!= 1/4` | D45 gegen die spaltenstochastische Fassung |
| PR-4 (`TP-FAN`) | `u(X) = u(B1) = u(B2)` | Literale | kein Knoten-Split (D49) |
| F (Massenbilanz) | `mass = Δ − Δ·(1−α)^K` | Gleichheit | Rekursion vollständig |
| PR-INV-4 | geteilte Ableitung | `derive_in_flow is derive_in_relax` | ein Graph, zwei Sichten |

**Bemerkenswert gegenüber `02a`:** keine der drei Rückfragen deckte einen Fehler in den
*Zahlen* der Vorgaben auf. Alle sieben Ankergruppen stimmten beim ersten Versuch. Die zwei
Vorgabefehler dieser Runde liegen beide in **Formulierungen** (§B.1, §B.2). Das ist der Ertrag
davon, dass die Golden Numbers diesmal exakt und ohne Rundung waren — es gab nichts zu
verrechnen.

Zwei Verbesserungen gegenüber dem Prompt werden hier normativ nachgezogen: die
Schnittstellenform von `derive()` (`02b-abnahme §B.4`) und die Identitätsprüfung in
PR-INV-4 (`02b-abnahme §C.3`).

---

## Teil A — Registereintrag D54

Anhängen an Abschnitt J in `07-decisions.md`.

### D54 — Die Massenschranke exakt und profilunabhängig

Die Schranke aus D45/PR-INV-2 lautet `Σt ≤ 1 − (1−α)^K`. `02b-golden-anchors.md §9` gab dafür
keine ganzzahlige Form an, und die naheliegende Umsetzung `Δ − Δ // 2^K` ist **profilabhängig**:
sie ist nur exakt, wenn `2^K` den Nenner `Δ = |A|·(b·D)^K` teilt, also genau für `α = ½`.

Der Implementierer hat das gemeldet. Die allgemeine Form ist exakt und für jedes `α`
ganzzahlig:

```
Delta · (1-alpha)^K  =  |A| · (b·D)^K · (b-a)^K / b^K  =  |A| · D^K · (b-a)^K

mass  <=  Delta − |A| · D^K · (b-a)^K
```

Der Faktor `b^K` kürzt sich vollständig gegen `Δ` — es bleibt ein Produkt aus Ganzzahlen, ohne
Division und ohne Fallunterscheidung.

Nachgerechnet bei `TP-02` (`|A|=1, D=4, K=20, b−a=1`): `2⁶⁰ − 2⁴⁰ = 1152920405095219200`,
identisch zur profilabhängigen Form, und Variante F erreicht sie mit **Gleichheit**.
Gegenprobe an einem Profil, in dem die alte Form bricht (`α = 1/3, D = 6, K = 7, |A| = 2`):
`Δ = 1224440064`, Schranke `1152776448`; `Δ // 2^K` ist dort bedeutungslos, weil `(1−α)^K` den
Nenner `3^7` trägt.

**Dieselbe Klasse wie D41/D42:** eine Zahl in den Vorgaben, die durch den Testgraphen nicht
widerlegt werden konnte, weil das kanonische Profil den Sonderfall ist. `α = ½` ist der einzige
Wert, unter dem der Fehler unsichtbar bleibt — und es ist der Default (D48).

Normativ ist die Produktform. Sie ersetzt jede Fassung mit `//`.

---

## Teil B — Korrekturen an `02b-golden-anchors.md`

### B.1 §9, PR-INV-2 und PR-INV-3 — Schranke in Produktform ⚠️

Ersatz für beide Formulierungen:

> **PR-INV-2 — Massenbilanz.** `mass ≤ Δ − |A|·D^K·(b−a)^K` für jeden budgetgültigen
> Kantensatz, mit Gleichheit genau dann, wenn jeder erreichte Knoten sein Budget voll
> ausschöpft und keine Kante subgranular ist. Die Schranke ist als **Produkt** zu schreiben,
> nie als `Δ − Δ // 2^K` — letzteres ist nur für `α = ½` exakt (D54).
>
> **PR-INV-3 — Über-Commitment-Indikator ist einseitig.**
> `mass > Δ − |A|·D^K·(b−a)^K ⇒ ein einbezogener Autor ist über-committet.` Die Umkehrung gilt
> nicht.

Ebenso in `§1` („Massenbilanz als Über-Commitment-Indikator") und in `§10` als Punkt 8:
*Die Massenschranke ist ein Produkt, keine Division.*

### B.2 §3 — „alle mit `u > 0`" ist falsch ⚠️

Der Satz „Also alle mit `u > 0`" in der Beschreibung der Knotenmenge gilt nicht für kleine `K`:
bei `K = 1` haben BOB, CAROL und die `gᵢ` sämtlich `u = 0` und stehen dennoch in `scores`. Der
PR-INV-8-Test durchläuft `K = 1..20` und trifft das.

Die Knotenmenge ist **strukturell** definiert und `K`-unabhängig. Ersatz:

> **Knotenmenge des Ergebnisses:** `A` vereinigt mit allen Endpunkten von `E⁺`. Wer nicht darin
> liegt, erscheint **gar nicht** — nicht als `0` (PR-INV-7). Die Menge hängt **nicht** von `K`
> ab; bei kleinem `K` tragen entfernte Knoten legitim `u = 0`, ohne aus dem Ergebnis zu fallen.
> Nur so ist PR-INV-8 über `K` hinweg formulierbar.

PR-INV-7 bleibt unverändert richtig: er spricht von *unerreichbaren* Knoten, nicht von solchen
mit Wert null.

### B.3 §11 — den offenen Punkt schärfen

Der zweite Anker in PR-INV-9 ist isoliert, und **genau deshalb** ist der Test gegen eine falsche
Begründung immun (§C.1). Der offene Punkt wird dadurch dringlicher und bekommt seinen Grund:

> - Ein Vektor für `PR-INV-9` mit einem **nicht** isolierten zweiten Anker. Der isolierte Fall
>   zeigt die Asymmetrie, aber er ist der einzige, in dem „die `u` bleiben gleich" und „die
>   Rekursion hängt nicht vom Ankerset ab" ununterscheidbar sind. Die zweite Aussage ist falsch
>   (D51, §C.1 der `02b`-Abnahme).

### B.4 §2 — Schnittstelle der geteilten Ableitung nachziehen

`02b-golden-anchors.md §10` und der Prompt beschreiben die geteilte Funktion als
`-> (d, edges, findings)`. Die Implementierung liefert `Derivation(bfs, findings)` und ist damit
**besser**: `build_flow_graph()` und `infinity()` konsumieren bereits eine `BfsResult`, und
`test_invariants.py` ruft `bfs_capacities()`/`infinity()` direkt damit auf. Die Tupelform hätte
einen der 144 eingefrorenen Tests angefasst — was der Prompt verbietet.

Normativ:

> Die geteilte Ableitung liefert `Derivation(bfs: BfsResult, findings)`. `trust()` liest daraus
> `node_capacity` für den Split; `rank()` liest **ausschließlich** `bfs.edges` und entpackt sie
> unmittelbar hinter dem Aufruf in eine lokale Variable. Dass `node_capacity` für `§5` in
> Reichweite liegt, ist eine Kopplung, die durch Konvention getragen wird und nicht durch den
> Typ (D49, K13).

---

## Teil C — Korrekturen an den Tests

Reihenfolge nach Wirkung. C.1 ist eine falsche Aussage im Code, C.2 ein zu schwacher Test.

### C.1 `test_PR_INV9_anchor_asymmetry_halves_every_value` — Kommentar ist falsch ⚠️

```python
# rohe u-Werte sind unveraendert (die Rekursion selbst haengt nie von |A| ab, siehe
# Herleitung in 02b-golden-anchors.md §1: |A| kuerzt sich heraus)
```

Die Assertions stimmen. Die Begründung nicht, und sie beruft sich auf eine Herleitung, die das
nicht hergibt. Was sich herauskürzt, ist `|A|` aus dem **Restart-Term**
(`Δ·e_J = |A|(bD)^k/|A| = (bD)^k`). Die Rekursion hängt sehr wohl vom Ankerset ab: der Term
`a·D·(bD)^k` wird für **jeden** Anker addiert. Die `u` bleiben hier gleich, **weil ALICE₂
isoliert ist** — mit einem verbundenen zweiten Anker steigen fremde `u`-Werte.

Ersatz:

```python
# Die rohen u-Werte sind hier unveraendert, weil ALICE2 isoliert ist und keine Masse ins
# System bringt. NICHT weil die Rekursion unabhaengig von |A| waere -- der Restart-Term
# wird je Anker addiert. Was sich herauskuerzt, ist |A| aus dem Restart-Term selbst
# (Delta * e_J = (bD)^k), nicht die Zahl der Anker aus der Rekursion. Mit einem
# verbundenen zweiten Anker steigen fremde u-Werte (offener Vektor, Anchors §11).
```

Der Test bleibt sonst unverändert; er belegt die Asymmetrie korrekt über den verdoppelten
Nenner.

### C.2 `test_PR_INV1_monotonicity_exhaustive_over_variant_B` — acht statt zweiunddreißig

Der Rumpf `ALICE→BOB→CAROL` ist fest; variiert werden nur die drei Sybil-Kanten. `2³ = 8` statt
der in `§9` verlangten `2^|E| = 32` Teilgraphen.

Der Test ist **nicht** wirkungslos — die neun Verletzungen der spaltenstochastischen Fassung
sitzen an CAROLs Kanten, also im variierten Bereich. Und der Paarvergleich über alle
`sub ⊆ sup` ist **stärker** als die Vorgabe, die nur gegen den vollen Graphen prüft.

Trotzdem: die beiden Rumpfkanten in `keys` aufnehmen. Vierundzwanzig zusätzliche Läufe, und der
Test prüft, was er behauptet — insbesondere den Fall, in dem eine ganze Kette wegfällt.

### C.3 `test_PR_INV4_edge_set_is_shared_with_paragraph_4` — benennen, was trägt

`rank_nodes == expected_nodes` vergleicht zwei Ableitungen **desselben** `derive()`-Aufrufs; das
prüft nur, dass `rank()` die Knotenmenge korrekt aus `edges` bildet. Die Invariante trägt allein

```python
assert derive_in_flow is derive_in_relax
```

und das ist die **bessere** Form: ein Identitätsvergleich der Funktionsobjekte kann nicht
zufällig grün sein, ein Datenvergleich schon. Der Test bleibt, wie er ist; eine Kommentarzeile
soll sagen, welche Assertion die Arbeit macht und warum die übrigen Zusatz sind.

### C.4 `rank()` — leeres Ankerset ⚠️

`denominator = len(anchors) * (bD**K)` ist bei `anchors = frozenset()` gleich `0`. Alle `u` sind
`0`, `mass` ist `0`, und `rank()` liefert schweigend ein `RankingResult` mit undefiniertem
Bruch. Das ist der einzige Weg, auf dem diese Funktion Unsinn zurückgeben kann, ohne zu murren.

```python
if not anchors:
    raise ValueError("anchors must not be empty")
```

Bei der Gelegenheit prüfen, ob `trust()` dieselbe Lücke trägt — dort steht nur die
`anchors & targets`-Prüfung.

### C.5 `RelaxParams` — Docstring um die Parameterkopplung ergänzen

Nichts koppelt `RelaxParams.base` an die `TrustParams`, mit denen `trust()` läuft. Ein Aufrufer
kann beide Sichten mit verschiedenen `C₀`/`γ`/`D` fahren; dann rechnen sie über verschiedenen
Kantensätzen, und PR-INV-4 fängt es nicht, weil der Test beide mit `PARAMS` aufruft.

Das ist **kein Defekt** — verschiedene Parameter sind verschiedene Graphen, und das ist
legitim. Aber „ein Graph, zwei Sichten" gilt nur *innerhalb* eines Parametersatzes, und das
steht nirgends. Ein Satz im Docstring von `RelaxParams`, kein Registereintrag.

### C.6 `test_pagerank_leak` und `test_pagerank_fan` — `//` durch Produkt ersetzen

`9 * r.denominator // 16` und `7 * r.denominator // 8` sind hier exakt, weil `16` und `8` den
Nenner `2⁶⁰` teilen. Dieselbe Klasse wie D54, nur harmloser. `9 * (r.denominator // 16)` ist
identisch und macht die Teilbarkeit sichtbar statt sie vorauszusetzen.

---

## Teil D — Offen, nicht blockierend

- **`PR-INV-9` mit verbundenem zweitem Anker** (§B.3). Nach C.1 der interessante Fall.
- **`α` in nicht gekürzter Form.** `(a,b) = (1,2)` und `(2,4)` beschreiben dasselbe `α`,
  liefern verschiedene `Δ` und verschiedene `u` — der **Bruch** `u/Δ` ist identisch.
  Nachgerechnet, aber ungetestet. Ein billiger Vektor, der belegt, dass die Norm nicht an einer
  Darstellung hängt.
- **`RelaxParams` erzwingt `α = 1 − γ` nicht** (D48, SHOULD). Richtig so; ob daraus ein MUST
  wird, ist der offene Punkt aus Anchors `§11`.
- Älter, weiterhin offen: Kanonizität von `v`; `t_exp is None` bindet Budget unbegrenzt;
  INV-8-Vektor für Layer 02a; `TP-BOOT`-Eigenschaftstest der Kalibrierungs-Ungleichung;
  `example-nucleus.md`; zweiter Spec-Durchgang für `05`, `06`, `04`, `00`, `VISION`.
