# Abnahme `02a-maxflow` — Befund und Nachzug

Stand: Implementierung vollständig, 144 Tests grün, Layer 01 unangetastet.
Grundlage: `graph.py`, `groups.py`, `flow.py`, `test_anchors.py`, `test_disjoint.py`,
`test_invariants.py`, `test_groups.py` sowie die sieben Rückfragen des Implementierers.

## Urteil

**Der Code ist abnahmefähig.** Die vier kritischen Vektoren sind echt getestet, mit Literalen
statt abgeleiteten Erwartungswerten:

| Vektor | erwartet | im Test | prüft |
|---|---|---|---|
| A′ simultan | 16 | `== 16`, `cut == (ALICE,)` | Quellanbindung `a_in` (K4); `a_out` gäbe 48 |
| F | 4/3/3, Σ 10, sim 4 | Literale in `EXPECTED` | Rundung, Rekursion durch `S` |
| G-Erneuerung | kein Finding | `overcommitted is False` | `max n` statt Summe (D40) |
| TP-FAN | `disjoint_paths == 2` | `== 2`, `value == 16` | Endpunkt-Regel (K5) |

Vier der sieben Rückfragen decken **Fehler in meinen Vorgaben** auf, nicht in der
Implementierung. Zwei davon in Zahlen, die normativ geworden wären. Die Abweichungen vom Prompt
sind durchweg Verbesserungen und werden hier normativ nachgezogen.

---

## Teil A — Registereinträge D41–D44

Anhängen an Abschnitt J in `07-decisions.md`.

### D41 — Budget-Austritt ist ein `t_exp`-Prädikat, kein Zustand

Der `02a`-Prompt verkürzte den Austritt aus dem Budget-Set in §2.6 auf `state == EXPIRED`. Das
ist falsch, und die Spec sagt bereits das Richtige: `02 §3.1` definiert das Budget-Set als „nicht
abgelaufen (widerrufen, supersediert und `pending` eingeschlossen)". **„Nicht abgelaufen" ist ein
Prädikat über `t_exp` und `now`, kein Zustand der Layer-01-Zustandsmaschine.**

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
`now ≤ t_exp` und stimmt mit `verifier.py` überein — gleiche Konvention, zwei Auswertungsstellen.
Anker 5 (S1 `now = 1000`, S2 `now = 2001`, `t_exp = 2000`) belegt beide Seiten.

**Layer 01 wird nicht angefasst.** Die Doppelung ist der Preis dafür, dass Layer 01 eingefroren
ist; sie ist dokumentiert und getestet, aber sie ist eine Kopplung. Ändert Layer 01 je seine
Ablaufkonvention, muss `groups.py` mitgezogen werden.

### D42 — Vouch-Kanten tragen im Disjunktheitslauf Kapazität 1, nicht ∞ ⚠️ (korrigiert D32/K5)

D32 belegte den Einheitskapazitäts-Lauf mit „interne Kanten `1`, Vouch-Kanten `∞`". Diese Fassung
ist **defekt**, aus zwei unabhängigen Gründen.

**Der Sentinel ist nicht wohldefiniert.** `INF = Σ(endliche Kapazitäten) + 1` war gegen den
Kapazitätslauf definiert. Im Einheitslauf sind die Vouch-Kanten selbst die ∞-Kanten; „Summe der
endlichen" ist dort zirkulär.

**Ohne Zwischenknoten degeneriert jeder Pfad.** Anker intern ∞ (D31/D32), Vouch-Kante ∞, Ziel
intern wegen D30 nicht auf dem Pfad — jede Kante des Pfades trägt ∞, und der Solver liefert den
Sentinel statt einer Pfadzahl. In `TP-BOOT` bürgen die Gründer **direkt** für die Neulinge; es
gibt keinen Zwischenknoten. Gemessen wurden 219 statt 1. In `TP-02` fällt es nicht auf, weil BOB
und CAROL dazwischenliegen — die Konvention wurde an einem Graphen entworfen, der den Fehler
nicht zeigen kann, und `TP-BOOT` stand mit seiner Disjunktheitsspalte (1/2/0) danebem, ohne dass
der Widerspruch auffiel.

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

Die Endpunkt-Regel aus D32 bleibt unberührt: die internen Kanten der Anker tragen weiterhin `INF`.
`TP-FAN` prüft, dass die Kappung sie nicht mitgekappt hat (`disjoint_paths == 2`, nicht `1`).

### D43 — Equivocation ist global, Über-Commitment ist scope-gebunden

`include_flagged` (D39) nennt zwei Flags, ohne ihren Geltungsbereich zu klären. Sie
unterscheiden sich, und zwar zwingend:

- **Equivocation** ist eine Aussage über die **Hash-Kette einer Identität** — zwei Claims mit
  demselben `h_prev`. Die Kette ist scope-übergreifend, also ist der Befund es auch. Ein Autor,
  der in *irgendeinem* Scope äquivoziert, hat seine Kette gebrochen; das ist keine Eigenschaft
  eines Scopes.
- **Über-Commitment** ist `Σ n_budget ≤ D` je Scope, und `D` ist scope-fest (D35). Der Befund
  kann gar nicht anders als scope-gebunden sein.

Normativ: bei `include_flagged = False` trägt keine Kante eines Autors, der (a) in irgendeinem
Scope `equivocation-flagged` ist **oder** (b) im **abgefragten** Scope über-committet ist.

Das Budget-Set bleibt in beiden Fällen unberührt (D39).

### D44 — `SUBGRANULAR_VOUCH` gilt nur für erreichbare Autoren

Der Prompt sagte „Kanten mit `cap == 0` erzeugen `SUBGRANULAR_VOUCH`" ohne Einschränkung. Die
BFS besucht unerreichbare Autoren nie; ihre Kanten werden nie geprüft und erzeugen kein Finding.

**Das ist richtig so, und die Vorgabe war zu weit.** Bei `C(I) = 0` wegen Unerreichbarkeit ist
die Ursache nicht Granularität, sondern Position. Ein `SUBGRANULAR_VOUCH` wäre eine
Falschaussage über die Ursache und würde bei jeder Abfrage für jeden nicht erreichten Teil des
Stores feuern — Rauschen proportional zur Store-Größe.

Normativ: `SUBGRANULAR_VOUCH` entsteht genau dann, wenn ein Autor mit `d(I) < ∞` eine Gruppe mit
`n_kante ≥ 1` trägt, deren Kapazität `⌊n_kante·C(I)/D⌋` null ist. Das Finding beschreibt den
**ausgewerteten** Graphen, nicht den Store.

Folge, die in `include_flagged` hineinspielt: Das Finding ist damit **flag-abhängig** — siehe die
Korrektur an INV-8 in Teil B.

---

## Teil B — Korrekturen an `02-golden-anchors.md`

### B.1 INV-2 ist eine Schranke, keine Gleichheit ⚠️

Die bisherige Fassung („C, D und C+1000 liefern alle simultan `3`") ist falsch, sobald die
zusätzlichen Sybils in die Zielmenge aufgenommen werden — und genau das prüft die
`|S|`-Unabhängigkeit. Nachgerechnet: 1000 Sybils hinter CAROL mit je `n = 1`, alle 1003 als
Ziel, ergibt

```
min( Rumpf 4, C(CAROL) 4, Σ Kanten-Caps 1003 ) = 4
```

also **4, nicht 3**. Der Satz in `§4` sagt `≤`, nicht `=`. Die 3 war nie die interessante Zahl:
sie ist die Summe der drei Kanten-Caps, nicht die Schranke.

Ersatz:

> **INV-2 — `|S|`-Unabhängigkeit ist eine Schranke.** Der simultane Fluss in die Sybil-Region ist
> durch `Σ_{h ∈ Grenze} C(h)` beschränkt, **unabhängig von `|S|`** — er wächst nicht mit der Zahl
> der Sybils. Bei `TP-02` ist diese Schranke `C(CAROL) = 4`.
> *Test:* C mit Zielmenge `{g₁,g₂,g₃}` liefert `3`; C plus 1000 weitere Sybils **hinter CAROL**,
> alle 1003 in der Zielmenge, liefert `4` und damit weiterhin `≤ 4`. Der Wert steigt, die
> Schranke hält. D liefert `3` wie C — die Topologie innerhalb `S` ist ohne Wirkung.

Der Vektor wird dadurch stärker als beabsichtigt: CAROL kann bei `D = 4` höchstens vier Subjekte
bebürgen, 1003 sind notwendig über-committet. Der Test prüft damit zugleich, dass die Schranke
gegen einen über-committeten Grenzknoten hält.

### B.2 INV-8 verengen — `SUBGRANULAR_VOUCH` ist flag-abhängig ⚠️

Die bisherige Fassung behauptet, *alle* Findings seien flag-invariant. Das gilt für drei von
vier. `SUBGRANULAR_VOUCH` entsteht in Schritt 6 der Auswertungsreihenfolge, **nach** der
Flag-Anwendung: fällt die Kante eines geflaggten Autors weg, verschlechtern sich stromabwärts die
Distanzen, sinken die Kapazitäten, und Kanten rutschen unter die Granularitätsgrenze. Das Finding
beschreibt den ausgewerteten Graphen (D44) und *muss* mitgehen.

Ersatz:

> **INV-8 — Das Flag ändert den Kantensatz, nicht die Budgetrechnung.** `Σ n_budget`,
> `OVERCOMMITTED_AUTHOR`, `INVALID_VOUCH_WEIGHT` und `UNPARSABLE_VOUCH_PAYLOAD` sind identisch,
> ob `include_flagged` `True` oder `False` ist — sie entstehen in den Schritten 2–4 der
> Auswertungsreihenfolge, vor der Flag-Anwendung. `SUBGRANULAR_VOUCH` entsteht in Schritt 6 und
> ist flag-abhängig; das ist konstruktiv so und kein Defekt (D44). Ändert sich eines der ersten
> vier mit dem Flag, ist die Reihenfolge verletzt.

### B.3 Variante E erzeugt vier `SUBGRANULAR_VOUCH`, nicht eines

Der bisherige Text nennt eine Kante (`cap(g₂→g₃) == 0`). Es sind vier: `d(g₂) = d(g₃) = 4`,
`C = 1`, also sind `g₂→g₁`, `g₂→g₃`, `g₃→g₁`, `g₃→g₂` alle null. Nur `g₁→g₂` und `g₁→g₃` tragen
(`C(g₁) = 2`, `cap = ⌊2·2/4⌋ = 1`).

Gleiche Fehlerklasse wie „17 × `SUBGRANULAR_VOUCH`" bei `TP-BOOT` (richtig: **51**, drei Gründer
× 17 Neulinge, das Finding hängt an der Gruppe).

### B.4 Anker 5b, Zeile „beide aktiv" ersetzen

Die bisherige Zeile ist in sich widersprüchlich: die Trust-Werte `3/1/1` setzen `n_budget = 3`
voraus, die Summenspalte sagt `4`. Mit `max(2,3) = 3` plus `g₂`/`g₃` (je 1) sind es `5 > 4`, also
dieselbe Rechnung wie „Heraufstufung" — die Zeile testete nichts Eigenes.

| Fall | `n(V1)` | Zustand V1 | `n(V2)` | `n_budget` | `n_kante` | `cap` | `Σ n_budget` | `→g₁/g₂/g₃` | simultan | Finding |
|---|---|---|---|---|---|---|---|---|---|---|
| beide aktiv | 2 | **ACTIVE** | 2 | 2 | 2 | 2 | **4** | 2 / 1 / 1 | 4 | keins |

Damit prüft die Zeile, was sie soll: zwei gleichzeitig aktive Vouches auf dasselbe Subjekt sind
**eine** Kante mit `n = 2`, nicht zwei Kanten und nicht `Σn = 4` aus dieser Gruppe. Und sie
liefert dieselben Werte wie die Erneuerungszeile — womit belegt ist, dass Duplikat und
Supersede-Kette identisch behandelt werden.

---

## Teil C — Korrekturen an den Tests

Reihenfolge nach Wirkung. C.1 und C.2 sind Tests, die derzeit nichts prüfen.

### C.1 `test_invariants.py::test_INV2_sybil_count_independence` — wirkungslos

Die Sybils hängen an `g1` (stromabwärts vom Ziel) und sind nie selbst Ziel. Beides zusammen
macht den Test leer: der Wert könnte sich gar nicht ändern. Neu:

```python
def test_INV2_sybil_count_independence() -> None:
    """|S|-Unabhaengigkeit ist eine Schranke, keine Gleichheit (§4).

    Sybils haengen hinter CAROL (dem ehrlichen Grenzknoten) und sind selbst Ziele --
    sonst prueft der Test nichts: stromabwaerts vom Ziel kann nichts wirken.
    """
    g_c, g_d = build("C"), build("D")
    anchors_c = frozenset({g_c.ALICE.pub})
    targets_c = frozenset({g_c.g1.pub, g_c.g2.pub, g_c.g3.pub})
    targets_d = frozenset({g_d.g1.pub, g_d.g2.pub, g_d.g3.pub})

    r_c = trust(g_c.store(), anchors=anchors_c, targets=targets_c, scope=g_c.scope,
                now=NOW, params=PARAMS, include_flagged=True)
    r_d = trust(g_d.store(), anchors=frozenset({g_d.ALICE.pub}), targets=targets_d,
                scope=g_d.scope, now=NOW, params=PARAMS, include_flagged=True)
    assert r_c.value == r_d.value == 3        # Topologie in S ist ohne Wirkung

    claims = list(g_c.claims)
    extra = []
    for i in range(1000):
        h = Identity(f"inv2-sybil-{i}")
        claims.append(g_c.CAROL.vouch(h, n=1, scope=g_c.scope, t=1, t_exp=T_EXP))
        extra.append(h.pub)
    store_plus = store_with(*claims)

    r_plus = trust(store_plus, anchors=anchors_c,
                   targets=targets_c | frozenset(extra), scope=g_c.scope,
                   now=NOW, params=PARAMS, include_flagged=True)
    assert r_plus.value == 4                    # steigt von 3 auf 4
    assert r_plus.value <= capacity(PARAMS, 2)  # aber nie ueber C(CAROL)
```

### C.2 `test_disjoint.py::test_disjoint_paths_invariant_to_1000_extra_sybils` — derselbe Defekt

Sybils an `g1`, Ziel `g1`. Auf CAROL umhängen und `g1` als Ziel behalten (der Wert bleibt `1`,
weil BOB Schnittknoten bleibt) oder die Sybils als Ziele aufnehmen — dann ist der Wert weiterhin
`1`, weil alle Pfade durch BOB laufen. Die zweite Form ist die aussagekräftigere.

### C.3 `test_anchors.py::test_E_subgranular_between_g2_g3` — Anzahl prüfen

```python
subgranular = [f for f in r.findings if f.kind == TrustFinding.SUBGRANULAR_VOUCH]
assert len(subgranular) == 4
```

`any(...)` ist grün, solange ein Finding kommt. Bei einem Finding, dessen Menge normativ ist, ist
das die falsche Form.

### C.4 `test_groups.py::_CASES["both_active"]` — auf `(2, "active", 2)` ändern

Erwartung dann `(2, 1, 1, 4, False)`. Siehe B.4. Der erklärende Kommentar bleibt wertvoll und
sollte auf die Korrektur umgeschrieben werden statt gelöscht zu werden.

### C.5 `test_groups.py::test_INV6_aggregation_is_idempotent` — Vergleich statt Literale

Der Test baut nur den einfachen Graphen und prüft Literale; die Gleichheit zur G-Erneuerung
behauptet nur der Docstring. Beide Graphen bauen und die `TrustResult`-Werte direkt vergleichen —
dann prüft er Idempotenz statt zweimal dieselbe Zahl.

### C.6 `test_groups.py` S1 — `SUBGRANULAR_VOUCH` fehlt

Anker 5 S1 sagt: `d(g₁) = 4`, `C(g₁) = 1`, `cap(g₁→gⱼ) = ⌊2·1/4⌋ = 0` ⇒ zwei
`SUBGRANULAR_VOUCH` (`g₁→g₂`, `g₁→g₃`). Ungeprüft.

### C.7 `graph.py::infinity()` — Argument festhalten

`inf` wird aus dem Flusslauf berechnet und für beide Läufe verwendet. Es trägt, weil jede Kante
in `edges` per Filter `cap ≥ 1` hat, also `inf > |edges| ≥ maxflow` im Einheitslauf. Das Argument
steht nirgends. Eine Kommentarzeile oder `assert inf > len(bfs_result.edges)`.

### C.8 `groups.py::Group` — Scope-Verkürzung dokumentieren

Der Schlüssel ist `(author, subject)`, D40 spricht von `(I, J, N)`. Korrekt, weil
`_is_scope_vouch` den Scope vorher filtert — aber ohne Kommentar liest der Nächste einen Fehler.

---

## Teil D — Offen, nicht blockierend

- **Kanonizität von `v`.** Lehnt `cbor_canon.decode` nicht-kanonische Kodierungen ab? D37 verlangt
  kanonisches CBOR; falls `decode` nur dekodiert, ist die Anforderung nicht durchgesetzt. D37 sagt
  dazu nichts Explizites — echte Lücke, kein Fehler.
- **`t_exp is None` bindet Budget unbegrenzt.** Konservativ, aber `02 §6.2` macht `t_exp` in
  Budget-Scopes zur Pflicht. Ein Vouch ohne `t_exp` ist dort spec-widrig; ihn stillschweigend als
  unbegrenzt zu behandeln verdeckt das. Ein eigenes Finding wäre ehrlicher.
- **INV-8-Vektor fehlt.** Kein Golden-Vektor zeigt einen geflaggten Autor, dessen Wegfall eine
  fremde Kante unter die Granularitätsgrenze drückt. Nach D44 ist das der interessante Fall.
- **`TP-BOOT`-Eigenschaftstest.** Vom Implementierer verschoben. Nicht streichen: er ist die
  einzige Prüfung der Kalibrierungs-Ungleichung, und `§7` der Anchors zeigt, dass sie optimistisch
  ist (nominell 48 Einheiten, real 36). Nachgerechnet: `(3,17)` → `θ=2`, 34 gegen 36; `(3,24)` →
  48 gegen 48; `(1,8)` → 16 gegen 16. Zwei von drei sind auf die Einheit ausgereizt.
- **`store.all_claims()` nach `classify_all`** ist ein zweiter Durchlauf über denselben Store.
  Kosmetisch.
