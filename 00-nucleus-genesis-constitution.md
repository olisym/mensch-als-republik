# Nukleus-Fundament — Genesis · Verfassung · Schlüssel-Autorität — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Layer: Scope-Fundament (unter Governance, definiert `N`)

Diese Schicht definiert, **was ein Nukleus-Scope `N` eigentlich ist**, bevor Trust-Flow, Profile,
Governance und Enforcement darauf partitionieren. Sie schließt die Design-Forks **DF-0** (Scope-
Identität), **DF-3** (Verfassungs-/irrevocable-Schema) und liefert die Träger für **DF-2**
(Arbitrationsbindung) und **DF-4** (Schwellen). Sie führt **kein** Atom-Feld ein: Genesis und
Verfassung sind content-adressierte Objekte (wie die Verfassung schon in Atom-Spec §7.2), Rotation
ist ein Profil.

> **Numerierungshinweis.** Konzeptuell sitzt dieses Kapitel *zwischen* Atom (das `N` als opaken
> 32-Byte-Scope kennt, Atom-Spec §2.3) und Governance (das auf Mitgliedschaft baut). Es kann als
> `00-…` vorangestellt oder in `04-governance.md §1` gezogen werden. Bis zur Entscheidung: `00`.

---

## 1. Leitsätze (Geltungsrahmen)

- **F1 — Scope = Genesis-Hash, nicht Schlüssel (DF-0, entschieden).** Die stabile Scope-ID `N`
  ist der Hash eines **unveränderlichen Genesis-Objekts**, **nie** ein Signierschlüssel. Ein
  Nukleus behält seine Identität, während seine Schlüssel rotieren und seine Verfassung sich
  ändert. Das ist die einzige Wahl, die mit Schlüsselrotation **und** FROST-Re-Keying konsistent
  ist (§6).
- **F2 — Drei-Objekt-Modell.** Ein Nukleus besteht aus drei getrennten Objekten nach Lebensdauer:
  **Genesis** (unveränderlich, definiert `N`), **Verfassung** (versioniert, per Governance
  geändert), **Schlüssel-Nachfolge** (verkettet, per Rotation fortgeschrieben). Keines ist ein
  Atom-Feld.
- **F3 — Schlüssel ≠ Identität des Nukleus.** Wer *als* der Nukleus handeln darf, ist eine
  auflösbare Frage (`resolve_current_key`, §6.4), nicht eine feste Bytefolge. `grant-membership`
  und jeder andere Nukleus-Akt wird vom **aktuell autorisierten** Schlüssel signiert, nicht von
  „`I == N`" (§7).
- **F4 — Gewaltenteilung bei der Rotation (DF-0-Folgeentscheidung).** Der Schlüssel reicht sich im
  Normalfall selbst weiter (Key-Chain, billig, kein Quorum). Bei Verlust/Diebstahl entscheiden die
  **Mitglieder** per Governance-Akt. Der Konfliktfall (zwei konkurrierende Nachfolger) fällt
  mechanisch auf denselben Equivocation-Beweis wie jeder andere Fork zurück (§6.3).
- **F5 — Verfassung hat ein Minimal-Schema, bleibt sonst opak (DF-3).** Damit sicherheitskritische
  Policy (irrevocable Prädikate, Schwellen, Arbitration, Stimmmodus) **maschinenlesbar
  durchgesetzt** werden kann, definiert dieses Kapitel eine normative Teilstruktur des
  Verfassungsobjekts. Alles darüber hinaus bleibt uninterpretiert (A2).

---

## 2. Die drei Objekte

| Objekt | Lebensdauer | Adressierung | Ändert sich per |
|--------|-------------|--------------|-----------------|
| **Genesis** | unveränderlich | `N = H(genesis)` (§3) | nie |
| **Verfassung** | versioniert | Content-Hash, `accept-rules@1` zeigt darauf | Governance-Amendment (Gov-Spec §5) |
| **Schlüssel-Nachfolge** | fortlaufend | Kette von `rotate-key@1`-Claims ab Genesis-Key | Rotation / Governance (§6) |

Die drei sind bewusst entkoppelt: **`N` bleibt fix**, während Verfassung und Schlüssel wandern.
Das ist der ganze Punkt von DF-0.

---

## 3. Scope-Ableitung

```
DOM_NUC_GEN = "claim-atom/v1/nucleus-genesis"

N = SHA-256( DOM_NUC_GEN || cbor_deterministic(genesis_obj) )     ; 32 B
```

- Eigener Domänen-Separator, damit `N` **nie** mit dem Identity-Genesis-Anker (`DOM_ID_GEN`,
  Atom-Spec §4) oder einer `claim_id` kollidiert, selbst bei sonst gleichen Bytes.
- `genesis_obj` wird in **kanonischem CBOR** (Atom-Spec §3) kodiert — ohne Determinismus wäre `N`
  nicht reproduzierbar.
- Ein Verifizierer, der `genesis_obj` kennt, rechnet `N` selbst nach und prüft, dass jeder
  Claim mit Feld `N` tatsächlich zu **diesem** Genesis gehört. Kein Nachschlagen einer Autorität.

### 3.1 Worked Example (real gerechnet, geteilt mit `01` Anhang C)

Ein vollständig durchgerechnetes, **schema-valides** Beispiel-Nukleus. `N` und `constitution_hash`
hier sind **byte-identisch** mit den Test-Vektoren in `01-claim-atom.md §Anhang C` — die ganze
Spec-Reihe testet gegen *denselben* Anker. Reproduzierbar via kanonischem CBOR (RFC 8949).

Ed25519-Identitäten (Seeds `01×32` / `02×32`):
```
ALICE = 8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c
BOB   = 8139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b394
```

**Verfassungsobjekt** (Text-Keys, Minimal-Schema §5; Ratios als `[num, den]`, floatfrei):
```
constitution = {
  irrevocable_predicates: ["obligation@1"],
  thresholds:            { ordinary: [1,2], membership: [2,3], amendment: [3,4] },
  arbitration:           { arbitrators: [ALICE] }
}
cbor(constitution)      = a36a7468726573686f6c6473a3686f7264696e61727982010269616d656e646d
                          656e748203046a6d656d626572736869708202036b6172626974726174696f6e
                          a16b61726269747261746f72738158208a88e3dd7409f195fd52db2d3cba5d72
                          ca6709bf1d94121bf3748801b40f6f5c7669727265766f6361626c655f707265
                          64696361746573816c6f626c69676174696f6e4031
constitution_hash       = SHA-256(cbor(constitution))
                        = 890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e6585c352dcf19ccad5ea7e
```

**Genesis-Objekt** (uint-Keys, Schema §4; `parent_scope` weggelassen ⇒ Top-Level-Nukleus):
```
genesis = {
  0 version           : 1
  1 root_keys         : [ALICE]
  2 key_mode          : 0            ; Einzelschlüssel
  3 anchor_set        : [ALICE]      ; Nukleus-Seed (Trust-Flow §6.3)
  4 constitution_hash : 890b21e7cd43fc42…
  5 amendment_rule    : 2            ; Schwellenklasse-Index (Policy)
  6 weight_mode       : 1            ; zweck-gescopt gewichtet (Gov §4)
  7 vote_mode         : 0            ; Komposition (Gov §3)
}
cbor(genesis)           = a80001018158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3
                          748801b40f6f5c0200038158208a88e3dd7409f195fd52db2d3cba5d72ca6709
                          bf1d94121bf3748801b40f6f5c045820890b21e7cd43fc4226938ce0b6eae1d0
                          0efa04ef9e6585c352dcf19ccad5ea7e050206010700
N = SHA-256(DOM_NUC_GEN ‖ cbor(genesis))
  = 65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557
```

Ein Verifizierer, der `genesis` kennt, rechnet `N` selbst nach (oben) und prüft, dass jeder
Claim mit Feld `N == 65309fe2…` zu genau diesem Genesis gehört — ohne Autorität zu befragen.

---

## 4. Genesis-Objekt — normatives Schema

Kanonische CBOR-Map. Unveränderlich (jede Änderung erzeugt ein **anderes** `N` = einen anderen
Nukleus). Pflichtfelder:

| Key | Feld | Typ | Bedeutung |
|----:|------|-----|-----------|
| 0 | `version` | uint (=1) | Genesis-Format-Version. |
| 1 | `root_keys` | array[bytes32] | **Initial** autorisierte Signierschlüssel (§6.4). Ein Key **oder** ein FROST-Gruppenschlüssel. |
| 2 | `key_mode` | uint | `0` = Einzelschlüssel, `1` = FROST-Gruppenschlüssel. |
| 3 | `anchor_set` | array[bytes32] | Der **Nukleus-Seed** (Trust-Flow-Spec §6.3): das out-of-band etablierte Ankerset. |
| 4 | `constitution_hash` | bytes32 | Hash der **initialen** Verfassung (§5). Spätere Versionen superseden per Governance. |
| 5 | `amendment_rule` | uint | Schwellenklasse für Verfassungsänderung (§5, Gov-Spec §5). `0` = `ordinary`, `1` = `membership`, `2` = `amendment` (D104). |
| 6 | `weight_mode` | uint | `0` = Kopfzahl, `1` = zweck-gescopt gewichtet (Gov-Spec §4). |
| 7 | `vote_mode` | uint | `0` = Komposition (Default), `1` = FROST-Opt-in (Gov-Spec §3). Löst DR-015. |
| 8 | `parent_scope` | bytes32 (optional) | **Rein deklarativ.** Behauptete Zugehörigkeit oder Nachfolge; ohne mechanische Folge (§4.1, D114). |
| 9 | `trust_params` | map (optional) | `{0: C₀, 1: γ_num, 2: γ_den, 3: D}`, alle uint. Kalibrierung des Trust-Flow (Trust-Flow-Spec §8, D115). Fehlt der Key, sind die Parameter out-of-band. |

- `root_keys` trennt **Identität** (= `N`, aus dem *ganzen* Genesis) von **Autorität** (= die
  Schlüssel, die *innerhalb* stehen). Genau diese Trennung erlaubt Rotation ohne Identitätsverlust.
- `vote_mode`/`weight_mode`/`amendment_rule` im Genesis machen die Konsens-Parameter **vor** der
  ersten Abstimmung fest und prüfbar — kein „Modus-Wechsel mittendrin" ohne Amendment.
- Die Änderungsregel ist **nicht** unveränderlich, aber nicht kaperbar: die anzuwendende Schwelle
  ist das Maximum aus alter und neuer (Gov-Spec §3.4). Anheben verlangt die neue, Senken die alte.

### 4.0 `trust_params` — warum im Genesis

`D` steckt über `n/D` in jedem signierten Vouch. Läge es in der änderbaren Verfassung, würde ein
Amendment Bestandssignaturen still umbewerten; D35 verlangt deshalb Unveränderlichkeit über die
Lebensdauer eines Scopes, und unveränderlich ist nur das Genesis. `C₀` und `γ` reisen mit, weil ein
Nukleus, der die eine Hälfte der Kalibrierung festlegt und die andere nicht, keine reproduzierbare
Kapazität hat.

Wohlgeformt bei Anwesenheit: `C₀ >= 1`, `D >= 1`, `1 <= γ_num < γ_den`. SHOULD: `D >= C₀`
(Trust-Flow-Spec §8), damit stets `C(I)` bindet und nicht `D`.

Die harte Reichweite folgt: `r_max = ⌊log_{1/γ} C₀⌋`. Jenseits davon ist `⌊C₀γ^d⌋ = 0`, und kein
Vouch trägt mehr — die quantitative Fassung von „maximal lokal".

Das Protokoll fixiert **keinen Default**. Ein Reichweitenparameter verteilt Macht und ist damit
Verfassungsinhalt (`08 §3`); das Genesis ist nur der Ort der Festlegung, nicht der Ort der Wahl.

### 4.1 `parent_scope` ist eine Behauptung, keine Beziehung

Das Feld wird von **keiner** Funktion dieser Referenzimplementierung gelesen. Es begründet keine
Autorität, keine Übertragung, keinen Vorrang und keine Sichtbarkeit über Scope-Grenzen hinweg —
`02 §2` ist unverändert bindend: es gibt einen Graphen je `N`, und Vertrauen aus einem Scope
fließt nicht in einen anderen.

Was es leistet: Es **behauptet** eine Zugehörigkeit oder eine Nachfolge, prüfbar über die
Genesis-Kette, bewertet vom Leser. Das Protokoll erzwingt Zurechenbarkeit, nicht Wahrheit
(`08 §2.1`).

Daraus folgt ausdrücklich: **mehrere Nuklei dürfen dieselbe Elternschaft behaupten**, und keiner
kann einen anderen daran hindern. Spaltet sich eine Gemeinschaft, berufen sich beide Hälften auf
denselben Vorgänger; welche als Fortsetzung gilt, entscheiden die Beteiligten und nicht ein
Register. Das Protokoll bildet den Streit ab, statt ihn zu entscheiden.

Es gibt **keine Stilllegungsmarkierung** und soll keine geben. Ein Nukleus, in dem niemand mehr
signiert, ist stillgelegt; das erkennt jeder Beobachter an seinem eigenen Bestand. Eine Markierung
wäre eine globale Aussage über etwas, das nur lokal beobachtbar ist.

### 4.2 Empfehlung: Governance und Substanz in getrennte Scopes

Keine Prüfung, eine Empfehlung — und die folgenreichste Entscheidung bei der Gründung.

Vouches, Obligationen und Quittungen gehören **nicht** in den Scope, dessen `participants`
abgestimmt werden. Ein Governance-Scope regiert genau eine Sache: sich selbst. Die Substanz lebt
in einem eigenen Scope, der keine `participants` deklariert und damit nicht auszählbar ist — er
braucht auch keine, denn Bürgen, sich verpflichten und quittieren sind zweiseitige Akte ohne
Kollektivbeschluss.

**Der Schnitt entscheidet, was eine Trennung später kostet.** Liegt die Substanz im
Governance-Scope, kostet ein Zerwürfnis die gesamte gescopte Geschichte. Liegt sie daneben, kostet
es das Regelwerk — die Vertrauenskanten und Kreditbeziehungen tragen ein anderes `N` und bleiben
unberührt, egal wie fest der Governance-Scope steckt.

Der Preis der Trennung: ein Scope ohne Governance hat **unveränderliche Arbitratoren**, weil
`03 §2.4` sie aus der Verfassung des eigenen Scopes nimmt. Wer beides will — änderbare Regeln und
unangreifbare Substanz — braucht drei Scopes oder muss einen der beiden Nachteile tragen.

---

## 5. Verfassungs-Minimal-Schema (DF-3)

Die Verfassung ist ein content-adressiertes, **versioniertes** Objekt. Ihr **Großteil bleibt
opak/Policy** (A2). Aber vier Felder sind **normativ** und **MÜSSEN** von Verifizierern honoriert
werden, weil an ihnen Sicherheit hängt:

| Feld | Typ | Zweck | Schließt |
|------|-----|-------|----------|
| `irrevocable_predicates` | array[text] | Prädikate, deren `core/revoke`/`core/supersede` **ignoriert** werden (Atom-Spec §5.4). Profilnamen ohne Scope-Präfix. `obligation@1` gilt auch ungenannt (§5.2); trust-gewährende Prädikate werden verworfen (Atom-Spec §5.4.3 b). | **P-1 / DR-030** |
| `thresholds` | map{text→ratio} | Quorum je Schwellenklasse (`ordinary`, `membership`, `amendment`, …). | DR-012 |
| `arbitration` | map | Zuständige Schiedsrichter / Klausel (§5.1). | **E-1 / DR-029** |
| `enforcement_policy` | map (optional) | Cure-Kurve, terminale Fehler (Enf-Spec §4, §8). | DR-022 |

### 5.1 `arbitration` (Träger für DF-2)

```
arbitration = {
  arbitrators:  [bytes32],     ; Identities, die im Scope urteilen dürfen
  clause_hash?: bytes32,       ; optional: Verweis auf eine ausführlichere Schlichtungsordnung
}
```

Ein `verdict@1` **bindet** nur, wenn sein Autor entweder (i) in `arbitration.arbitrators` steht,
**oder** (ii) beide Parteien vorab per `submit-arbitration@1` (Profile-II §2.4) auf ihn
gezeigt haben. Fehlt beides, ist das Verdikt **attributed_opinion** ohne Statuswechsel
(Enforcement-Spec §3, geänderte Fassung — siehe DF-2). Das ist die maschinenlesbare Antwort
auf E-1.

### 5.2 Sicherheits-Default: ein Boden, keine Rückfallebene

`obligation@1` ist **immer** irrevocable (Protokoll-Default, Profile-II §3.3.3).
`irrevocable_predicates` kann die Menge nur **erweitern**, nie verkleinern:

```
wirksame Menge  =  { "obligation@1" }  ∪  irrevocable_predicates  ∖  unsicher (Atom-Spec §5.4.3 b)
```

Damit gilt der Schutz in drei Fällen gleichermaßen: die Verfassung schweigt; sie nennt
`obligation@1`; sie nennt **andere** Prädikate und lässt `obligation@1` weg. Eine
Formulierung, in der der Default nur bei Schweigen greift, wäre durch das bloße Nennen einer
beliebigen anderen Zeile aushebelbar gewesen — genau das Schulden-Lösch-Loch, das dieser
Abschnitt schließen soll, nur mit einem Zwischenschritt.

**Unsichere Deklarationen fallen heraus, ohne die übrigen zu entwerten.** Nennt eine Verfassung
`vouch@1`, bleibt der Rest der Liste wirksam; der unsichere Eintrag wird verworfen und
vermerkt (`UNSAFE_IRREVOCABLE_PREDICATE`, Atom-Spec §5.4.3 b). Ein Alles-oder-nichts wäre
schlechter: eine einzelne Fehldeklaration nähme dem Nukleus auch den Schuldenschutz.

### 5.3 Lebenszyklus

Verfassungsupdate ⇒ neues Objekt ⇒ neuer Hash. Ratifizierung *ist* die Re-Akzeptanz per
`accept-rules@1` auf den neuen Hash über die `amendment`-Schwelle (Gov-Spec §5). **`N` bleibt
fix**, weil `N` aus dem *Genesis*, nicht aus der Verfassung abgeleitet ist.

---

## 6. Schlüssel-Autorität & Rotation (DF-0-Folgeentscheidung: „Beides")

Zwei Pfade, wie in F4 festgelegt.

### 6.1 Normalpfad — Key-Chain (`rotate-key@1`)

Ein **Profil**, kein `core` (Frozen-Primitive-Check §8): Rotation macht eine Aussage über *wer als
der Nukleus handeln darf* — soziale Autorität, kein selbst-bezüglicher Lebenszyklus im Sinne von
Atom-Spec §5.1. Fällt damit korrekt durch den `core`-Aufnahmetest.

| `nuc:N/rotate-key@1` | Belegung |
|----------------------|----------|
| `I` | der **aktuell autorisierte** Schlüssel `K_{n-1}` |
| `J` | `[identity, K_n]` — der Nachfolgeschlüssel |
| `N` | der Scope |
| `v` | optional: `{ effective?, note? }` |

**Kettenregel (Nachfolge, autor-verkettet):**
```
R_1 ist gültig  ⟺  R_1.I ∈ genesis.root_keys
R_n ist gültig  ⟺  R_n.I == (der von R_{n-1} benannte K_{n-1})
```
Die Nachfolge ist damit eine Kette über **Autorschaft**: jeder Schlüssel benennt genau seinen
Nachfolger. Ordnung kommt aus dieser Kette, **nie** aus Wall-Clock `t` (Atom-Spec §5.3).

**Gegenzeichnung (D125).** Ein `rotate-key@1` allein wirkt nicht. Eine Rotation ist
**vollständig**, wenn `K_n` sie gegenzeichnet — ein Claim in `K_n`s **eigener** Kette, der die
`claim_id` des Rotate-Claims nennt. Eine unvollständige Rotation ist wirkungslos: kein Zustand,
kein eigener Vermerk, sie zählt nicht. Es bindet der **erste vollständige** Rotate.

```
R_n wirkt  ⟺  R_n ist nach der Kettenregel gültig
              UND es existiert ein Claim C mit C.I == (der von R_n benannte K_n)
                  und C verweist auf claim_id(R_n)
```

Beide Signaturen sind selbstenthalten und reisen zusammen; die Regel braucht **weder Uhr noch
globale Ordnung**. Sie schließt drei Fälle, die die Kettenregel offen ließ: die einseitige
Einsetzung eines Dritten, den Rotate auf einen Schlüssel, dessen Halter nichts davon weiß, und den
Vertipper. Ein Altschlüssel bekommt die Kette dadurch nicht zurück — wirkt der erste vollständige
Rotate, ist `K_{n-1}` nicht mehr autorisiert, und ein späterer Rotate von ihm ist kein Akt eines
autorisierten Schlüssels mehr.

Das Prädikat der Gegenzeichnung ist hier **benannt, aber nicht kodiert**; die Belegung fällt mit
`00a` und trägt bis dahin keinen Testvektor.

### 6.2 Notfallpfad — Governance-Rotation

Ist `K_{n-1}` **verloren** (kann keinen `rotate-key` mehr signieren) oder die Kette **umstritten**
(§6.3), installieren die **Mitglieder** einen neuen Schlüssel per Governance-Akt: ein
`propose@1`/Abstimmung, dessen Payload den neuen autorisierten Schlüssel deklariert, ratifiziert
über die **`amendment`-Schwelle** (hoch, gegen Routine-Capture). Kein neues Primitiv — reiner
Governance-Loop (Gov-Spec §2).

### 6.3 Präzedenz & umstrittene Rotation (der Diebstahlfall)

- **Governance schlägt Key-Chain.** Existiert eine ratifizierte Governance-Rotation, **supersediert**
  sie die Key-Chain ab ihrem Effektivpunkt. Begründung: die Mitglieder sind die letzte Autorität;
  der Schlüssel ist ihr Delegat.
- **Doppel-Nachfolger = Equivocation.** Signiert `K_{n-1}` zwei verschiedene Nachfolger, haben beide
  `I == K_{n-1}` und dieselbe `h_prev` in `K_{n-1}`s eigener Kette ⇒ **Equivocation-Beweis nach
  Atom-Spec §4**, ohne neue Mechanik. Der Verifizierer sieht eine *umstrittene* Autorität und
  behandelt Nukleus-Akte beider konkurrierender Schlüssel als **unaufgelöst**, bis die
  Governance-Rotation (§6.2) entscheidet **oder** das Mitglied per Exit/Fork ausweicht (Gov-Spec §6).
- Das ist genau der Grund für „Beides": ein **gestohlener** Schlüssel produziert einen zweiten
  Nachfolger → Equivocation → die Entscheidung fällt zwangsläufig an die Mitglieder, nicht an den
  Dieb.

### 6.4 `resolve_current_key(N)` — der autoritative Auflösungsalgorithmus

```
1.  Starte mit genesis.root_keys (aus dem Objekt, dessen Hash == N).
2.  Folge der längsten NICHT-equivozierten rotate-key-Kette (§6.1).
3.  Existiert eine ratifizierte Governance-Rotation (§6.2) mit Effektivpunkt ≥ dem
    aktuellen Kettenende, ersetzt ihr Schlüssel das Kettenende.
4.  Ist die Key-Chain an einem Punkt equivoziert UND keine Governance-Rotation löst
    ihn auf → Autorität ist UNAUFGELÖST; Nukleus-Akte ab dem Fork gelten als nicht
    autorisiert, bis Auflösung vorliegt (Detect-not-Prevent, Atom-Spec §A3).
```
Der Rückgabewert ist die Menge der aktuell autorisierten Schlüssel. Jeder Verifizierer rechnet das
lokal über seinen bekannten Claim-Teilgraphen (Partitionstoleranz wie Trust-Flow-Spec §7).

**Zustand vor `00a`.** Solange `resolve_current_key` nicht gebaut ist, gilt
`resolve_current_key(N) = genesis.root_keys`, und ein vorgefundenes `rotate-key@1` wird **nicht**
ausgewertet. Rotation ist bis dahin nicht verfügbar. Der zweite Halbsatz ist die eigentliche Regel:
ohne ihn führte ein Leser eine ihm vorliegende Rotation still nicht nach und vertraute weiter dem
alten Schlüssel — die unsichere Richtung. Als benannte Grenze ist der Fall tragbar, als Schweigen
wäre er eine Lücke.

**Zwei Punkte in Schritt 2 und 3 sind offen und fallen mit `00a`:**

- **„Längste" ist unterbestimmt.** Ist die Kette nicht equivoziert, benennt jeder Schlüssel genau
  einen Nachfolger und es gibt nichts zu maximieren. Mehrere Kandidaten entstehen nur bei
  Teilwissen (Lücke in der Mitte) oder bei `|root_keys| > 1`, also mehreren parallelen Ketten. Für
  den zweiten Fall ist auch ungeklärt, ob eine Rotation die Menge verkleinern oder Ketten
  verschmelzen darf.
- **Der Effektivpunkt ist nicht rechenbar.** „≥ dem aktuellen Kettenende" vergleicht eine
  Governance-Größe mit einer Position in einer Autorenkette. Über `t` ist das nach Atom-Spec §5.3
  verboten. Der uhrfreie Weg ist, die Governance-Rotation den ersetzten Schlüssel bzw. die ersetzte
  `claim_id` **explizit** nennen zu lassen; entschieden ist er nicht.

### 6.5 FROST-Re-Keying

In `key_mode = 1` ist der autorisierte „Schlüssel" ein **Gruppen**schlüssel. Mitgliederwechsel ⇒
neuer Gruppenschlüssel ⇒ derselbe `rotate-key@1`: der **alte** Gruppenschlüssel co-signiert (per
FROST) die Rotation auf den **neuen**. Scheitert die Schwellen-Signatur (zu viele Mitglieder weg),
greift der Notfallpfad §6.2. **`N` bleibt in allen Fällen fix** — das war die Kernanforderung, an
der Variante A (Pubkey = Scope) gescheitert wäre.

**Die Gegenzeichnung aus §6.1 gilt hier unverändert:** der **neue** Gruppenschlüssel zeichnet die
Rotation gegen. Ohne diesen Satz nähme `key_mode = 1` sich still von D125 aus, und die Bauform der
Rotation wäre in den zwei Modi verschieden.

---

## 7. Auswirkung auf `grant-membership` & Nukleus-Akte

**Geänderte Autorisierungsregel** (ersetzt „`I == N`"): Ein Nukleus-Akt (`grant-membership@1`,
`verdict@1` eines Panels, Föderationsstimme, Ratifizierung, `rotate-key@1`) ist autorisiert gdw.:

```
akt.I ∈ resolve_current_key(akt.N)
```

- `∈` ist Mengenzugehörigkeit und für jede Mächtigkeit definiert. **`key_mode` unterscheidet die
  Signaturform, nicht die Zahl der autorisierten Schlüssel.** Für `key_mode = 0` ist das eine
  gewöhnliche Ed25519-Signatur, für `key_mode = 1` eine FROST-Gruppensignatur unter dem aktuellen
  Gruppenschlüssel; in beiden Fällen trägt der Akt **eine** Signatur.
- **Bei mehreren autorisierten Schlüsseln genügt einer.** `root_keys` ist eine Liste — der
  Beispiel-Nukleus in `example-nucleus.md` hat zwei (D149) —, und jeder von ihnen darf allein
  handeln. Ob ein Nukleus stattdessen eine Schwelle verlangen können soll, ist **nicht
  entschieden** und wäre ein Verfassungsknopf nach §4, kein Protokolldefault.
- `akt.N` MUSS gesetzt sein und zum aufgelösten Scope passen (Atom-Spec §2.2, Bindungsregel).

Das ist die konkrete Code-Konsequenz von DF-0: die heutige Prüfung `atom.I == scope` in
`parse_grant_membership` wird zu `atom.I ∈ resolve_current_key(scope)`.

---

## 8. Frozen-Primitive-Konformität (Nachweis)

Dieses Kapitel fügt **kein** Atom-Feld hinzu. Prüfung Punkt für Punkt:

- **Genesis & Verfassung** sind content-adressierte externe Objekte, referenziert per Hash
  (`accept-rules@1.J = [object-hash, …]`) — exakt das Muster aus Atom-Spec §7.2. Kein neues Feld.
- **`rotate-key@1`** ist ein Profil über bestehenden Feldern (`I`, `J=[identity,…]`, `N`, `v`).
  Es besteht den `core`-Aufnahmetest **nicht** (es macht eine Autoritäts-Aussage, keinen
  selbst-bezüglichen Lifecycle) und bleibt daher korrekt außerhalb von `core` — konsistent mit
  der Ablehnung von `vouch`/`verdict`/`membership` in Atom-Spec §5.
- **Governance-Rotation** ist ein gewöhnlicher `propose`/`vote`-Loop; die Auszählung ist bestehende
  Governance-Mechanik.
- **Equivocation umstrittener Rotation** nutzt `Atom.is_equivocation_pair` unverändert.
- **Verfassungs-Schema** lebt im *Objekt hinter dem Hash*, nicht im Atom; das Atom sieht weiterhin
  nur einen opaken 32-Byte-`object-hash`.

Ergebnis: Das Fundament wächst rein additiv über Profile und content-adressierte Objekte. Das
radiale Prinzip bleibt intakt.

---

## 9. Bewusst getragene Grenzen & Designentscheidungen

- **Genesis-Bootstrapping bleibt der wertbildende Akt (DR-026).** `N`, `root_keys` und `anchor_set`
  entstehen out-of-band. Die gesamte Sybil- und Autoritätssicherheit steht und fällt mit der
  Integrität dieser Gründungszeremonie — kein Protokollmechanismus kann eine vergiftete Gründung
  intern erkennen. Bewusst akzeptiert; eine Multi-Party-Seed-Zeremonie ist Policy, kein v1-Core.
- **`amendment_rule` in v1 unveränderlich** (Gov-Spec §5): Wer die Meta-Regel ändern will, **forkt**
  einen neuen Nukleus (neues `N`) und nimmt Mitglieder per Re-Akzeptanz mit. Verhindert
  Governance-Capture der Änderungsregel selbst. Trade-off: weniger Flexibilität, keine Capture-Fläche.
- **Governance-Rotation als Capture-Vektor.** Der Notfallpfad §6.2 könnte theoretisch von einer
  Mehrheit missbraucht werden, um einen legitimen Schlüsselhalter zu enteignen. Mitigation: hohe
  (`amendment`-)Schwelle + der Halter kann per Exit/Fork ausweichen (er behält seine *eigene*
  Identität, Profile-II §4). Residual bewusst getragen — es ist dieselbe irreduzible „Mehrheit kann
  irren"-Grenze wie in Enforcement-Spec §7.
- **Unaufgelöste Autorität unter Partition (§6.4 Schritt 4).** Solange eine umstrittene Rotation
  nicht per Governance aufgelöst ist, sind Nukleus-Akte ab dem Fork *nicht autorisiert* — die
  sichere Richtung (lieber kein gültiger Akt als ein falsch autorisierter), konsistent mit dem
  „Unter-Vertrauen"-Prinzip aus Trust-Flow-Spec §7.
- **Schema-Minimalismus (DF-3).** Nur vier Verfassungsfelder sind normativ; alles andere bleibt
  opak. Das ist ein *bewusster, begrenzter* Bruch der „Verfassung = reiner opaker Hash"-Linie — der
  minimal nötige, um P-1/E-1 maschinenlesbar zu schließen, ohne die Interpretationsschicht ins
  Protokoll zu ziehen.
