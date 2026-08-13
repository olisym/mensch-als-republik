# Layer 04 — Golden Anchors

Erwartungswerte für die Implementierung der Governance-Schicht. Alle Zahlen sind exakte Integer
und vor dem Schreiben dieses Dokuments gerechnet, nicht danach.

---

## 1. Methode

**Zweifach verifiziert.** Die kanonische CBOR-Kodierung wurde eigenständig implementiert und
**gegen die vier Bestandsanker aus `00 §3.1` validiert**, bevor irgendein neuer Wert entstand:
`cbor(constitution)`, `constitution_hash = 890b21e7…`, `cbor(genesis)` und
`N = 65309fe2…` reproduzieren byte-identisch. Die Schwellenarithmetik ist zusätzlich in
Integer-Form und über `Fraction` gerechnet; beide Wege stimmen in jedem Fall überein.

**Kein Float, keine Division.** Jeder Vergleich zweier Verhältnisse läuft über Kreuzmultiplikation.

**Der Bestandsanker bleibt unberührt.** `65309fe2…` und `890b21e7…` sind nicht Teil dieses
Profils. Der Nukleus aus `00 §3.1` trägt kein `participants` und setzt `weight_mode = 1`; er ist
nach `04 §3.5` nicht auszählbar. Layer 04 bekommt deshalb ein eigenes Profil.

---

## 2. Profil D

### 2.1 Identitäten

Ed25519, Seeds `01×32` bis `05×32`. Die ersten drei sind Bestand.

```
ALICE = 8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c
BOB   = 8139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b394
CAROL = ed4928c628d1c2c6eae90338905995612959273a5c63f93636c14614ac8737d1
DAVE  = ca93ac1705187071d67b83c7ff0efe8108e8ec4530575d7726879333dbdabe7c
EVE   = 6e7a1cdd29b0b78fd13af4c5598feff4ef2a97166e3ca6f2e4fbfccd80505bf1
```

`participants` ist byteweise aufsteigend sortiert und duplikatfrei. Die Sortierung folgt **nicht**
der Namensreihenfolge:

```
P1 (Epoche 1, n = 4)  =  BOB, ALICE, DAVE, CAROL
                         8139…  8a88…  ca93…  ed49…

P2 (Epoche 2 und 3, n = 5)  =  EVE, BOB, ALICE, DAVE, CAROL
                               6e7a…  8139…  8a88…  ca93…  ed49…
```

Ein Vektor, der die Sortierung nach Namen statt nach Bytes vornimmt, erzeugt einen anderen
`constitution_hash` und damit eine andere Epoche. Das ist Absicht: die Reihenfolge ist Teil der
Identität.

### 2.2 Die drei Verfassungen

```
C1 = {
  irrevocable_predicates: ["obligation@1"],
  thresholds:             { ordinary: [1,2], membership: [2,3], amendment: [3,4] },
  arbitration:            { arbitrators: [ALICE] },
  participants:           [BOB, ALICE, DAVE, CAROL]
}

C2 = C1, aber participants = [EVE, BOB, ALICE, DAVE, CAROL]      (Aufnahme von EVE)

C3 = C2, aber arbitration = { arbitrators: [BOB, ALICE] }        (zweiter Arbitrator)
```

```
constitution_hash_1 = 5a1db51257084870e541c0e6f0aef99af4e2331eba86f1cd26c6308120792d5e
constitution_hash_2 = 8bc6be3556cb867066d2adac795c01e67403d6d9a38210a37e31b6ba6789607b
constitution_hash_3 = c5111d414c3c2e73404a5c26ba0bd336ec6c4b0b95a2e1b8d65ff674f5fa1b04
```

`C1` nach `C2` unterscheidet sich ausschließlich in `participants` — Klasse **`membership`**,
Schwelle `[2,3]`. `C2` nach `C3` unterscheidet sich in `arbitration` — Klasse **`amendment`**,
Schwelle `[3,4]`. Die Klasse wird abgeleitet, nicht gewählt (`04 §3.4`).

### 2.3 Das Genesis-Objekt

```
genesis_D = {
  0 version           : 1
  1 root_keys         : [ALICE]
  2 key_mode          : 0
  3 anchor_set        : [ALICE]
  4 constitution_hash : 5a1db512…
  5 amendment_rule    : 2
  6 weight_mode       : 0            ; Kopfzahl (D98)
  7 vote_mode         : 0            ; Epochenpfad
}

cbor(genesis_D) =
  a80001018158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c
  0200038158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c
  0458205a1db51257084870e541c0e6f0aef99af4e2331eba86f1cd26c6308120792d5e
  050206000700

N_D = SHA-256(DOM_NUC_GEN || cbor(genesis_D))
    = 7794d26f7f4d45634aa1f08bfba8763e16eaf9d64f88fcbb36aae8b756fc388b
```

Gegenüber `00 §3.1` unterscheidet sich `genesis_D` in zwei Bytes des Endes — `06 00` statt
`06 01` — und im `constitution_hash`. Das ist ein nützlicher Vektor für sich: derselbe
Schlüsselsatz, ein anderer Gewichtungsmodus, ein anderer Nukleus.

---

## 3. Die Epochenkette

```
DOM_NUC_EPOCH    = "claim-atom/v1/nucleus-epoch"
DOM_NUC_PROPOSAL = "claim-atom/v1/nucleus-proposal"

epoch_id      = SHA-256( DOM_NUC_EPOCH    || cbor([N, i, constitution_hash]) )
proposal_hash = SHA-256( DOM_NUC_PROPOSAL || cbor({0: N, 1: predecessor, 2: constitution_hash}) )
```

```
epoch_id_1      = b22eba4020aafbd9932e0835675561671b29f240ba8d2b6fc901bd6a2c4b5d84
                  ( [N_D, 1, constitution_hash_1] — der Genesis ist Epoche 1 )

proposal_hash_1 = 2a6055011f8886f4d25faa2f9292b195f5a9351b0c5c7a695c9df6b807212b46
                  ( predecessor = epoch_id_1, Ziel = constitution_hash_2 )

epoch_id_2      = b64d51ca9be9976c55bb6380dc28ad1b77970db3def8dbc0d819041e64cc8bb4
                  ( [N_D, 2, constitution_hash_2] )

proposal_hash_2 = c941cc1e5968a1aeeee8f2397949217225e1ff085ea1b371e9fee1dc872f3c9b
                  ( predecessor = epoch_id_2, Ziel = constitution_hash_3 )

epoch_id_3      = 2e93ad45c32b11cd7c3dad35ccafc77cb0487a09a87db3f3583ebfba2cb3fd4e
                  ( [N_D, 3, constitution_hash_3] )
```

**Vektor `GV-1`.** Zwei `ratify@1`-Claims für `proposal_hash_1`, von verschiedenen Autoren, mit
verschiedenen Zeugenmengen. Beide liefern `epoch_id_2 = b64d51ca…`. Kein Widerspruch, keine
zweite Epoche. Das ist D99 in einer Zahl.

**Vektor `GV-2`.** Ein `ratify@1` mit `v[0]` als Zeugenmenge, die einen zusätzlichen, nicht
zählenden Claim enthält. Der `epoch_id` ändert sich nicht; die Ratifizierung scheitert an
`04 §4.1` Bedingung 3, Vermerk `UNSUPPORTED_RATIFICATION`.

---

## 4. Schwellenarithmetik

```
durchgekommen:   |Ja| * den          >   num * n
gescheitert:     (n - |Nein|) * den   <=  num * n
```

### 4.1 Die Kante des strikten Größer

Epoche 1, `n = 4`, Klasse `amendment`, `[3,4]`:

| Vektor | Ja | Nein | Rechnung | Zustand |
|---|---|---|---|---|
| `GV-3` | 3 | 0 | `3*4 = 12` gegen `3*4 = 12` | `PENDING` |
| `GV-4` | 4 | 0 | `4*4 = 16` gegen `12` | `PASSED` |

`GV-3` ist der wichtigste Vektor dieses Dokuments. Ein `>=` statt `>` macht aus drei von vier
Stimmen eine Verfassungsänderung. Der Unterschied ist ein Zeichen im Quelltext.

### 4.2 Scheitern ohne vollständige Beteiligung

Epoche 1, `n = 4`, `[3,4]`:

| Vektor | Ja | Nein | Rechnung | Zustand |
|---|---|---|---|---|
| `GV-5` | 0 | 2 | `(4-2)*4 = 8` gegen `12` | `FAILED` |
| `GV-6` | 1 | 2 | `(4-2)*4 = 8` gegen `12` | `FAILED` |

Zwei Mitglieder haben sich noch gar nicht geäußert, und der Vorschlag ist trotzdem endgültig
erledigt: das erreichbare Ja ist zu klein. Ohne die zweite Ungleichung bliebe er auf `PENDING`
hängen, bis jemand eine Frist erfindet.

### 4.3 Die Aufnahme (Epoche 1, Klasse `membership`)

`n = 4`, `[2,3]`, Ziel `constitution_hash_2`:

| Vektor | Ja | Rechnung | Zustand |
|---|---|---|---|
| `GV-7` | 2 | `2*3 = 6` gegen `2*4 = 8` | `PENDING` |
| `GV-8` | 3 | `3*3 = 9` gegen `8` | `PASSED` |

Die Aufnahme von EVE kostet drei von vier Stimmen. Dieselbe Aufnahme unter der
Änderungsschwelle hätte alle vier gekostet — das ist der Grund für die Klassenableitung aus
`04 §3.4`.

**EVE ist nach `GV-8` noch kein Mitglied.** Sie steht in `participants` von `C2`, aber
`membership()` verlangt zusätzlich ihre aktive `accept-rules@1` auf `constitution_hash_2`. Ohne
sie lautet der Zustand `GRANT_ONLY` (`04 §6.1`, D60).

### 4.4 Die Änderung (Epoche 2, Klasse `amendment`)

`n = 5`, `[3,4]`, Ziel `constitution_hash_3`:

| Vektor | Ja | Rechnung | Zustand |
|---|---|---|---|
| `GV-9`  | 3 | `3*4 = 12` gegen `3*5 = 15` | `PENDING` |
| `GV-10` | 4 | `4*4 = 16` gegen `15` | `PASSED` |

---

## 5. Die Maximum-Regel

Alle Fälle in Epoche 2, `n = 5`. `angewandt = max(alt, neu)`, Vergleich über
`num_a * den_n` gegen `num_n * den_a`.

### 5.1 Senken — der tragende Fall

Ein Vorschlag setzt `thresholds.amendment` von `[3,4]` auf `[1,2]`.

```
max([3,4], [1,2]):   3*2 = 6   >=   1*4 = 4   ->   angewandt = [3,4]
```

| Vektor | Ja | angewandte Schwelle | Rechnung | Zustand |
|---|---|---|---|---|
| `GV-11` | 3 | `[3,4]` | `3*4 = 12` gegen `15` | `PENDING` |
| `GV-12` | 3 | `[1,2]` (Gegenbild ohne Regel) | `3*2 = 6` gegen `5` | `PASSED` |

**Das ist die Anti-Capture-Eigenschaft in zwei Zahlen.** Drei von fünf Mitgliedern können die
Änderungsschwelle nicht auf die Hälfte senken, obwohl drei von fünf nach der *neuen* Schwelle
eine Mehrheit wären. `GV-12` ist der Vektor, der grün werden muss, wenn die Regel fehlt — er
gehört als Gegenbild in die Testsuite, nicht nur als Kommentar.

### 5.2 Anheben

Ein Vorschlag setzt `thresholds.amendment` von `[1,2]` auf `[4,5]`.

```
max([1,2], [4,5]):   1*5 = 5   <   4*2 = 8   ->   angewandt = [4,5]
```

| Vektor | Ja | angewandte Schwelle | Rechnung | Zustand |
|---|---|---|---|---|
| `GV-13` | 4 | `[4,5]` | `4*5 = 20` gegen `4*5 = 20` | `PENDING` |
| `GV-14` | 4 | `[1,2]` (Gegenbild ohne Regel) | `4*2 = 8` gegen `5` | `PASSED` |

`GV-13` trifft zugleich die Kante aus `4.1`: bei `[4,5]` und `n = 5` verlangt das strikte Größer
Einstimmigkeit. Eine Minderheit kann der Mehrheit keine strengere Regel auferlegen.

Die Ausgangsschwelle `[1,2]` in `5.2` gehört zu keiner der drei Verfassungen aus `2.2`; der
Vektor prüft die Regel, nicht die Kette.

---

## 6. Ausschluss rivalisierender Nachfolger

Epoche 2, `n = 5`, Klasse `amendment`, `[3,4]`.

```
nötige Ja je Vorschlag:                     4
zwei Vorschläge verlangen zusammen:         8 Ja-Stimmen
verfügbare Mitglieder:                      5
Mitglieder mit zwei Ja, mindestens:         8 - 5 = 3
```

**Vektor `GV-15`.** Zwei Vorschläge auf `epoch_id_2`, jeder mit vier Ja. Nach `04 §4.4` zählen
die Ja-Stimmen der drei doppelt stimmenden Mitglieder bei **keinem** von beiden; Vermerk
`CONFLICTING_APPROVAL`. Beide Zählungen landen bei einem Ja und damit auf `PENDING`. Es entsteht
keine Epoche 3, kein Fork und keine Auflösungsregel.

Damit ist D102 an einer Zahl geprüft: nicht „der erste gewinnt", sondern „der Fall tritt nicht
ein".

---

## 7. Ausschlussfälle mit Vermerk

Alle in Epoche 2 gegen `proposal_hash_2`, Erwartung jeweils: der Zustand bleibt `PENDING`, der
Vermerk erscheint, und die Stimme zählt nicht.

| Vektor | Lage | Vermerk |
|---|---|---|
| `GV-16` | zwei aktive Stimmen desselben Autors auf denselben Vorschlag | `AMBIGUOUS_VOTE` |
| `GV-17` | Stimme eines Schlüssels, der nicht in `participants` steht | `NON_MEMBER_VOTE` |
| `GV-18` | Stimme auf einen Vorschlag mit `predecessor = epoch_id_1` | `STALE_EPOCH_VOTE` |
| `GV-19` | `vote.v[0] = 2` | `UNKNOWN_VOTE_CHOICE` |
| `GV-20` | `vote.N != N_D` | `SCOPE_MISMATCH` |
| `GV-21` | Verfassungsobjekt zu `constitution_hash_2` lokal unbekannt | `CONSTITUTION_UNAVAILABLE`, Zustand `UNEVALUABLE` |
| `GV-22` | Verfassung ohne `participants` | `PARTICIPANTS_UNDECLARED`, Zustand `UNEVALUABLE` |
| `GV-23` | `participants` unsortiert oder mit Duplikat | `MALFORMED_PARTICIPANTS`, Zustand `UNEVALUABLE` |
| `GV-24` | `genesis[6] = 1` | `UNSUPPORTED_WEIGHT_MODE`, Zustand `UNEVALUABLE` |

`GV-24` ist mit dem Bestandsnukleus aus `00 §3.1` unmittelbar prüfbar: `N = 65309fe2…` setzt
`weight_mode = 1` und liefert damit `UNEVALUABLE`, nie ein Ergebnis.

---

## 8. Invarianten

| Kennung | Aussage |
|---|---|
| `INV-04.1` | `PASSED` und `FAILED` sind absorbierend: mehr Stimmen ändern einen erreichten Zustand nie. |
| `INV-04.2` | `PASSED` und `FAILED` schließen einander aus, für jedes `n`, `num`, `den`, `Ja`, `Nein`. |
| `INV-04.3` | Kein Teilwissen führt zu `PASSED`. Fehlt ein Objekt, ist der Zustand `UNEVALUABLE`. |
| `INV-04.4` | Zwei `ratify@1` für denselben Vorschlag liefern denselben `epoch_id`. |
| `INV-04.5` | Die Auszählung liest keine Uhr. Kein Pfad wertet `t` oder `t_exp` einer Stimme aus. |
| `INV-04.6` | Bei `num/den > 1/2` gibt es zu einer Epoche höchstens einen Vorschlag im Zustand `PASSED`. |

`INV-04.2` und `INV-04.6` sind als Eigenschaftstests über einem Bereich zu prüfen, nicht an
Einzelvektoren: `n` von 1 bis 12, `[num,den]` über allen gekürzten Brüchen mit `den <= 8` und
`1/2 <= num/den < 1`, alle Belegungen von `Ja` und `Nein` mit `Ja + Nein <= n`.

`INV-04.5` ist negativ zu prüfen: ein Lauf mit zwei verschiedenen `now`-Werten muss byte-identische
Ergebnisse liefern.

---

## 9. Was hier nicht steht

- **Keine Gewichte.** `weight_mode = 1` ist nicht ausgewertet (D98); es gibt keine Trust-Flow-Zahl
  in diesem Dokument.
- **Keine Signaturvektoren.** Die Claims selbst folgen `01` Anhang C; dieses Profil liefert die
  Objekte und die Arithmetik, nicht die Atome.
- **Kein `resolve_current_key`.** Der Schlüsselpfad aus `04 §5` ist vertagt (D62); alle Vektoren
  laufen über `vote_mode = 0`.
- **Keine Föderationszahlen.** `04 §7.2` ist eine Belegung desselben Loops; ein zweites Profil auf
  Föderationsebene bringt keine neue Arithmetik.
