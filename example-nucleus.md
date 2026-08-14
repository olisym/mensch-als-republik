# Beispielnukleus — „Zwei und eine Dritte"

Ein rechenbares Paar aus Governance- und Ressourcen-Scope. Alle Objekte sind byte-genau
angegeben und mit demselben Kodierungsweg gerechnet, der die Bestandsanker aus `00 §3.1`
byte-identisch reproduziert.

Dies ist **kein Spec-Layer.** Es wählt Zahlen, und Zahlen sind nach `08 §3` Verfassungsinhalt.
Jede Wahl hier ist begründet und keine ist normativ.

---

## 1. Die Lage, die abgebildet wird

Zwei Menschen gründen etwas. Sie werden sich irgendwann uneins sein — das ist kein Randfall,
sondern der Regelfall, und Aldi wie Vapiano sind die bekannten Beispiele.

**Bei zwei Mitgliedern gibt es keine Wahl.** Jede nach D108 zulässige Schwelle verlangt
Einstimmigkeit; das folgt aus `2·num ≥ den` und ist nicht parametrierbar. Ein Nein, und die
Verfassung steht für immer — Vorlagen laufen nicht ab (D100), Nein-Stimmen sind unwiderruflich
(D97), und wer den Blockierenden entfernen will, braucht seine Zustimmung.

Deshalb sind es hier **drei**: zwei Gründer und eine Dritte. Nicht als Instanz über ihnen — die
gibt es in MaR nicht (`04 §8`) —, sondern als Mitglied unter Gleichen. Bei `n = 3` und
Amendment-Klasse `1/2` sind zwei von drei nötig. Jede strengere Klasse fällt wieder auf
Einstimmigkeit zurück; `1/2` ist bei drei Mitgliedern die **einzige** Wahl, die eine ist.

---

## 2. Identitäten

Ed25519, Seeds `0x11×32`, `0x12×32`, `0x13×32`.

```
ANNA  = d04ab232742bb4ab3a1368bd4615e4e6d0224ab71a016baf8520a332c9778737
BRUNO = 204040e364c10f2bec9c1fe500a1cd4c247c89d650a01ed7e82caba867877c21
CHRIS = 66cd608b928b88e50e0efeaa33faf1c43cefe07294b0b87e9fe0aba6a3cf7633
```

Dazu die Kandidatin aus `§5`, Seed `0x14×32`:

```
DORA  = 20828bf5c5bdcacb684863336c202fb5599da48be5596615742170705beca9f7
```

Byteweise sortiert — und die Reihenfolge ist **nicht** die der Namen:

```
Gründungsmenge:   BRUNO (2040…), CHRIS (66cd…), ANNA (d04a…)
nach der Aufnahme: BRUNO (2040…), DORA (2082…), CHRIS (66cd…), ANNA (d04a…)
```

DORA sortiert zwischen BRUNO und CHRIS ein, nicht ans Ende. Wer die Liste anhängt statt sie zu
sortieren, erzeugt `MALFORMED_PARTICIPANTS` und einen nicht auszählbaren Nukleus.

Das ist Teil der Objektidentität. Wer nach Namen sortiert, bekommt einen anderen
`constitution_hash` und damit einen anderen Nukleus.

---

## 3. Der Governance-Scope

Er regiert genau eine Sache: sich selbst. Wer Mitglied ist, wie hoch die Schwellen liegen, wer
schlichtet. Sonst nichts.

### 3.1 Verfassung

```
constitution_gov = {
  irrevocable_predicates: ["obligation@1", "ratify@1", "vote@1"],
  thresholds:             { ordinary: [1,2], membership: [1,2], amendment: [1,2] },
  arbitration:            { arbitrators: [BRUNO, CHRIS, ANNA] },
  participants:           [BRUNO, CHRIS, ANNA]
}

constitution_hash_gov = f5cddafcaa18068aba72079a7a8c87194a13b0dcd6d5c22bfcacbe2c3991e923
```

`vote@1` und `ratify@1` stehen in `irrevocable_predicates`, weil `04 §2.1` es verlangt — ohne
sie ist der Nukleus nicht auszählbar (`VOTE_REVOCABLE`, `RATIFY_REVOCABLE`).

Alle drei Schwellen stehen auf `1/2`. Nach D108 zulässig, weil `2·1 ≥ 2`; die Grenze ist nicht
strikt. Bei `n = 3` verlangt das zwei Ja.

Arbitratoren sind alle drei. In einem Scope ohne Substanz gibt es wenig zu schlichten, und wer
sonst sollte es tun.

### 3.2 Genesis

```
genesis_gov = {
  0 version           : 1
  1 root_keys         : [BRUNO, ANNA]
  2 key_mode          : 0
  3 anchor_set        : [BRUNO, ANNA]
  4 constitution_hash : f5cddafc…
  5 amendment_rule    : 2            ; amendment (D104)
  6 weight_mode       : 0            ; Kopfzahl (D98)
  7 vote_mode         : 0            ; Epochenpfad
}

N_gov      = 50ecec77a0fc064b8404f1ea74d5f85ed9ea4abc49e477e3c98a9c59525a8f63
epoch_id_1 = 7f4b12a76f41c4d10aa58b6c8a9f7a7575eb271132d08708e053fba3494823a0
```

Kein `trust_params`: hier wird nichts geflossen. Das ist zugleich der Vektor dafür, dass Key 9
wirklich optional ist (D115).

`root_keys` und `anchor_set` sind die beiden Gründer, nicht alle drei. Chris ist Mitglied und
Schlichterin, aber keine Wurzel — sie kam dazu, um zu entscheiden, nicht um zu gründen.

---

## 4. Der Ressourcen-Scope

Hier lebt die Substanz: Vouches, Obligationen, Quittungen. **Keine Governance.**

### 4.1 Verfassung

```
constitution_res = {
  irrevocable_predicates: ["obligation@1"],
  thresholds:             { ordinary: [1,2], membership: [1,2], amendment: [1,2] },
  arbitration:            { arbitrators: [BRUNO, CHRIS, ANNA] }
}

constitution_hash_res = 3af74c182d52af10afd8828120703fdf7672ad9f0c21381af47650fcc40dc502
```

**Kein `participants`.** Damit ist der Scope nach `04 §3.5` nicht auszählbar
(`PARTICIPANTS_UNDECLARED`) — und braucht es nicht: Bürgen, sich verpflichten und quittieren sind
zweiseitige Akte ohne Kollektivbeschluss. Wer nichts abstimmen kann, gerät in keine Sackgasse.

`thresholds` steht nur da, weil `00 §5` es als normatives Feld führt. Es ist hier inert.

### 4.2 Genesis

```
genesis_res = {
  0 version           : 1
  1 root_keys         : [BRUNO, ANNA]
  2 key_mode          : 0
  3 anchor_set        : [BRUNO, ANNA]
  4 constitution_hash : 3af74c18…
  5 amendment_rule    : 2
  6 weight_mode       : 0
  7 vote_mode         : 0
  9 trust_params      : { 0: 100, 1: 1, 2: 2, 3: 100 }   ; C₀=100, γ=1/2, D=100
}

N_res = 4d78bcea4a44af89c0728fbc5f3a0300a853291f744a1657b3ecc2926717f355
```

`D = C₀ = 100` erfüllt das SHOULD aus `02 §8`: es bindet stets `C(I)`, nie `D`.

### 4.3 Was diese Zahlen bedeuten

Knotenkapazität `C(x) = ⌊C₀·γ^d⌋`, einmal am Ende gerundet (`02 §2`):

```
d      0    1    2    3    4    5    6    7
C    100   50   25   12    6    3    1    0
```

Sechs Hops Reichweite, `r_max = ⌊log₂ 100⌋ = 6`. Jenseits davon trägt kein Vouch mehr — das ist
die harte Grenze aus `02 §8` und keine Panne.

Bei `D = 100` und vollem Vouch trägt jede Kante genau die Kapazität ihres Ausgangsknotens. Die
Out-Degree-Schranke `min(D, C(I))` liest sich dann als Satz:

| Distanz zum Seed | kann bürgen für |
|---|---|
| 0 (Anker) | 100 Menschen |
| 1 | 50 |
| 2 | 25 |
| 3 | 12 |
| 4 | 6 |
| 5 | 3 |
| 6 | 1 |

Das ist `02 §3.1`s Satz „die Zahl der Menschen, für die man bürgen kann, ist die eigene Position",
in Zahlen, die man einem Gründer vorlegen kann.

**Chris steht in Distanz 1** zu den beiden Ankern, sobald einer für sie bürgt: `C = 50`. Sie ist
Mitglied im Governance-Scope, aber das trägt hier nichts bei — Mitgliedschaft in einem Scope ist
in einem anderen unsichtbar (`02 §2`, Scope-Partition). Wer im Ressourcen-Scope gelten soll,
braucht dort Bürgen.

---

## 5. Der Konfliktfall, durchgerechnet

Anna will DORA aufnehmen. Bruno ist dagegen.

Die Zielverfassung ist `constitution_gov` mit einem einzigen Unterschied — `participants` enthält
zusätzlich DORA:

```
constitution_hash_2 = 6cbcd33f2f82257153517d565a821d6d069129826efbfe1b737ff2c3a80f6f1b

proposal = { 0: N_gov, 1: epoch_id_1, 2: constitution_hash_2 }
proposal_hash = 7dfb88e9a6b2b9b8ef5a2e5b6b5e8e429033da12274fa4480e5a1a42f8a1b089

epoch_id_2 = bfcf27681adf4bbadc71f0e04238cee9a58bc7b3ff22ff12a940b007b5771eef
```

Weil sich beide Verfassungen **ausschließlich** in `participants` unterscheiden, ist die Klasse
**`membership`** nach `04 §3.4`, Schwelle `[1,2]`. Wäre auch nur ein weiteres Feld berührt, wäre
es `amendment` — hier dieselbe Zahl, aber nicht dieselbe Regel.

```
n = 3,  [num, den] = [1, 2]

durchgekommen:   |Ja| · 2  >  1 · 3     ->   |Ja| >= 2
gescheitert:     (3 − |Nein|) · 2  <=  3  ->   |Nein| >= 2
```

| Anna | Bruno | Chris | Zustand |
|---|---|---|---|
| Ja | Nein | — | `PENDING` — ein Ja, ein Nein, offen |
| Ja | Nein | Ja | **`PASSED`** — zwei Ja |
| Ja | Nein | Nein | **`FAILED`** — zwei Nein, erreichbares Ja ist 1 |

**Das ist der ganze Punkt des Dritten.** Ohne Chris stünde die erste Zeile für immer: kein
Zeitablauf, kein Widerruf, keine Instanz darüber. Mit ihr fällt eine Entscheidung — in beide
Richtungen, und ohne dass jemand über den anderen gestellt wird.

Materialisiert wird sie durch ein `ratify@1` eines Mitglieds mit der Zeugenmenge der zählenden
Ja-Stimmen. Danach beginnt Epoche 2 mit `constitution_hash_2` und vier Mitgliedern. **DORA ist
damit noch nicht Mitglied** — sie steht in `participants`, aber ohne ihre eigene `accept-rules` auf
`6cbcd33f…` ist ihr Zustand `GRANT_ONLY` (D60). Eine Mehrheit kann niemandem eine Mitgliedschaft
samt Pflichten zuschreiben, die er nicht eingegangen ist. Zwei Mitglieder dürfen unabhängig materialisieren; sie erzeugen denselben `epoch_id`,
weil dessen Identität das Ergebnis hasht und nicht den Beleg (D99).

---

## 6. Der Trennungsfall

Nehmen wir an, es geht doch nicht weiter.

**Was nichts kostet.** Die Vouches, Obligationen und Quittungen tragen `N_res`. Nichts an ihnen
verweist auf `N_gov`. Der Governance-Scope kann feststecken, verwaisen oder sich spalten — an den
Kanten im Graphen ändert das kein Byte. Beide Hälften gründen je einen neuen Governance-Scope und
bleiben im gemeinsamen Ressourcen-Scope: verschiedene Regelwerke, dieselbe Wirtschaft. **Niemand
fängt bei null an, weil niemand etwas verloren hat.**

Der neue Governance-Scope darf `parent_scope = N_gov` setzen. Das ist eine Behauptung, keine
Übertragung (D114) — und **beide** Hälften dürfen sie erheben. Wer als Fortsetzung gilt,
entscheiden die Beteiligten, nicht ein Register.

**Was der alte Scope tut.** Nichts. Ein Nukleus lässt sich nicht löschen; er wird unbenutzt. Es
gibt keine Stilllegungsmarkierung und soll keine geben (D114). Können sich die beiden noch auf
eine letzte Sache einigen, ist es diese: eine Änderung, die `participants` auf eine Hälfte setzt.
Der Vergleich in Protokollform.

**Was teuer ist.** Wollen die Hälften auch getrennte Wirtschaften, gründet eine einen neuen
Ressourcen-Scope und beginnt dort bei null. Vertrauen aus Scope A fließt nicht nach Scope B
(`02 §2`); Kontextbindung ist die Eigenschaft, wegen der das Ganze funktioniert, und sie lässt
sich für den Trennungsfall nicht aussetzen.

**Der Preis dieser Bauform**, offen benannt: `N_res` hat **unveränderliche Arbitratoren**, weil
`03 §2.4` sie aus der Verfassung des eigenen Scopes nimmt und diese Verfassung nie geändert werden
kann. Stirbt eine Arbitratorin oder wird sie befangen, hilft nichts. Wer beides will — änderbare
Regeln **und** unangreifbare Substanz — braucht einen dritten Scope, der nur die Schlichtung trägt,
oder muss einen der beiden Nachteile tragen.

---

## 7. Das Claim-Set

Struktur, nicht Bytes. Die Bytes erzeugt `tools/example_nucleus.py` aus der Implementierung und
prüft sie gegen die Objekt-Hashes oben — damit belegt derselbe Lauf, dass Dokument und Code
übereinstimmen.

**Im Governance-Scope** (`N = N_gov`, alle `p = nuc:50ecec77…/…`):

| # | Autor | Prädikat | `J` | `v` |
|---|---|---|---|---|
| 1–3 | ANNA, BRUNO, CHRIS | `accept-rules@1` | `[3, constitution_hash_gov]` | — |
| 4 | ANNA | `propose@1` | `[3, proposal_hash]` | — |
| 5 | ANNA | `vote@1` | `[3, proposal_hash]` | `{0: 1}` |
| 6 | BRUNO | `vote@1` | `[3, proposal_hash]` | `{0: 0}` |
| 7 | CHRIS | `vote@1` | `[3, proposal_hash]` | `{0: 1}` |
| 8 | ANNA | `ratify@1` | `[3, proposal_hash]` | `{0: [cid₅, cid₇]}` |
| 9 | DORA | `accept-rules@1` | `[3, constitution_hash_2]` | — |

Nach 1–3 sind alle drei `MEMBER`: in `participants` **und** mit aktiver `accept-rules` auf genau
diesen Hash (D60, `04 §6.1`). Nach 8 ist DORA `GRANT_ONLY`, nach 9 `MEMBER` — aber gegen
`constitution_hash_2`, nicht gegen den ersten. Die drei Gründer sind in Epoche 2 ihrerseits
`GRANT_ONLY`, bis sie die neue Fassung ihrerseits annehmen. Fehlt eines von beidem, ist der Zustand `GRANT_ONLY` oder
`APPLICANT` — nie `MEMBER`.

**Im Ressourcen-Scope** (`N = N_res`): wechselseitige `vouch@1` zwischen ANNA und BRUNO, je ein
`vouch@1` beider auf CHRIS, `n = D = 100`. Ergebnis: CHRIS in Distanz 1, `C = 50`.

Kein Claim des einen Scopes ist im anderen sichtbar. Das ist keine Einschränkung der
Implementierung, sondern `02 §2`.

---

## 8. Was hier gewählt wurde und warum

| Wahl | Wert | Grund |
|---|---|---|
| Mitglieder | 3 | bei 2 ist jede Schwelle Einstimmigkeit; unparametrierbar |
| alle Schwellen | `[1,2]` | bei `n = 3` die einzige Klasse ohne Einstimmigkeit |
| `weight_mode` | `0` | D98; Stimmgewicht wäre eine handelbare Größe |
| `C₀` | 100 | Granularitätsboden fein genug für `D = 100` |
| `γ` | `1/2` | kurz und scharf: sechs Hops, weit über dem Durchmesser einer kleinen Gemeinschaft |
| `D` | 100 | `D ≥ C₀` erfüllt; feinste Vouch-Abstufung ein Hundertstel |
| Scopes | 2 | der Schnitt entscheidet, was eine Trennung kostet (D114) |

### 8.1 Betriebswarnung

**Jede Verfassungsänderung entzieht allen still den `MEMBER`-Status.** Nach der Ratifizierung in
`§5` zeigen die `accept-rules` der drei Gründer auf `f5cddafc…`, die geltende Verfassung ist aber
`6cbcd33f…`. `membership()` liefert für alle drei `GRANT_ONLY`, bis jede und jeder einzeln neu
annimmt. Abstimmen dürfen sie weiter — `participants` gilt unverändert (D116, `04 §6.3`).

Wer eine Anwendung auf `MEMBER` gründet, muss das einplanen: nach jeder Änderung braucht es eine
Runde Signaturen, bevor der Zustand wieder trägt.

### 8.2 Was nicht gewählt wurde

Weil Layer 05 es noch nicht trägt: `k_slash`, die Cure-Kurve,
`unit_ref` und die terminalen Fehler. Sie gehören in `enforcement_policy` und kommen mit `05`.

---

## 9. Nachrechnen

Jede Zahl in diesem Dokument entsteht aus deterministischer CBOR-Kodierung (RFC 8949, Core
Deterministic) und SHA-256 mit den Separatoren aus `00 §3` und `04 §1.1`. Derselbe Kodierungsweg
reproduziert die Bestandsanker `890b21e7…` und `65309fe2…` aus `00 §3.1` byte-identisch; bricht
diese Probe, ist die Kodierung falsch und nicht der Beispielnukleus.
