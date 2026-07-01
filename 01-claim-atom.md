# Claim-Atom — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Layer: Identity/Claim (Konvergenzpunkt des Stacks)

Das Claim-Atom ist das einzige Primitiv der oberen Schichten. Bürgschaft, Regelannahme,
Verdikt, Wert-Transfer und Mitgliedschaft sind keine eigenen Objekte, sondern *Profile* —
Nutzungskonventionen über genau diesem Atom. Ein Profil fügt **niemals** ein Feld hinzu.

---

## 1. Leitsätze (Geltungsrahmen)

- **A1 — Selbstenthalten.** Ein Claim ist ein in sich geschlossenes Objekt. Es trägt alles,
  was zur Verifikation nötig ist, und reist über RNS, QR oder Papier. Transport steht nie
  im Atom.
- **A2 (geschärft) — Lebenszyklus, nicht Bedeutung.** Das Protokoll versteht den *Lebenszyklus
  von Claims und Keys* (Gültigkeit, Ordnung, Verkettung, Widerruf der eigenen Claims).
  Es versteht **niemals** die *Bedeutung von Aussagen*. Alles Soziale ist Policy und bleibt
  in der Interpretationsschicht.
- **A3 — Erkennen statt verhindern.** Kein globaler Konsens. Jede Identity führt einen
  hash-verketteten, append-only Log. Manipulation ist evident; Forks (Equivocation) sind
  kryptografisch beweisbar, werden aber nicht verhindert.
- **Ein-Signierer.** Jedes Atom hat genau einen Signierer. Mehrparteiigkeit ist entweder
  Krypto (FROST/Threshold kollabiert eine Gruppe zu *einer* Identity unter einem
  Gruppenschlüssel) oder Komposition (mehrere Atome + Interpretationsregel) — nie ein Feld.
- **v1-Sparsamkeit.** Keine Key-Rotation, keine Delegation im Core (siehe §8).

---

## 2. Feldsatz

| CBOR-Key | Feld     | Typ / Größe              | Pflicht | Bedeutung |
|---------:|----------|--------------------------|:-------:|-----------|
| 0        | `version`| uint (= 1)               | ja      | Formatversion. |
| 1        | `I`      | bytes[32]                | ja      | Signierer-Identity = Ed25519-Verify-Key. |
| 2        | `J`      | array `[tag, value]`     | ja      | Subjekt, polymorph (§2.1). |
| 3        | `p`      | text                     | ja      | Prädikat-ID, namensraum-qualifiziert + versioniert (§2.2). |
| 4        | `v`      | bytes                    | nein    | Opaker, prädikat-definierter Wert. Protokoll parst ihn nie. |
| 5        | `N`      | bytes[32]                | nein    | Scope = Nukleus-Identity. Strukturell erstklassig (§2.3). |
| 6        | `t`      | uint (Unix-Sekunden)     | ja      | Vom Autor behaupteter Zeitstempel. **Kein** Ordnungsprimitiv. |
| 7        | `t_exp`  | uint (Unix-Sekunden)     | nein    | Harte strukturelle Decke. Danach ist der Claim void (§5.3). |
| 8        | `h_prev` | bytes[32]                | ja      | Hash des vorherigen Claims desselben Autors. Genesis = 32×0x00. |
| 9        | `σ`      | bytes[64]                | ja*     | Ed25519-Signatur über das Preimage (§4). |

\* `σ` (Key 9) ist im *signierten* Objekt Pflicht und im *Signatur-Preimage* abwesend.

Alle Referenzen sind einheitlich 32 Byte (Ed25519-Key **oder** SHA-256-Hash), die Signatur
64 Byte. Das hält die Wire-Form kompakt — wichtig für LoRa.

### 2.1 `J` — Subjekt (polymorph)

`J = [tag: uint, value: bytes[32]]`. Der Tag ist ein geschlossener Enum; er ist Mechanismus,
weil der Verifizierer wissen *muss*, worauf der Claim zeigt:

| Tag  | Name         | `value` ist … |
|-----:|--------------|---------------|
| 1    | `identity`   | Ed25519-Verify-Key der referenzierten Identity. |
| 2    | `claim-ref`  | `claim_id` (SHA-256) eines konkreten Claims (§4). |
| 3    | `object-hash`| SHA-256 eines externen Objekts (z. B. Regeldokument, Datei). |

Mehr Typisierung wäre bereits Semantik und bleibt draußen.

### 2.2 `p` — Prädikat

Format: `<namespace>/<name>@<version>`, z. B. `nuc:hasenpfote/vouch@1`.

- Namensraum **`core`** ist protokoll-reserviert und geschlossen. In v1 existieren dort
  genau zwei Prädikate: `core/revoke@1` und `core/supersede@1` (§5).
- Jeder andere Namensraum ist **opak/Policy**. Das Protokoll behandelt `p` als
  undurchsichtigen Identifier; seine Bedeutung lebt vollständig in der Interpretationsschicht.

### 2.3 `N` — Scope

Optionaler 32-Byte-Verweis auf die Identity eines Nukleus. **Strukturell** erstklassig:
der Verifizierer partitioniert die Trust-Flow-Berechnung pro `N` (Vertrauen ist
kontextgebunden). Die *Regeln*, die `N` bedeutet, bleiben uninterpretiert. `N` abwesend =
kontextfreier Claim (z. B. ein reiner Identity-Announce).

---

## 3. Kanonische Serialisierung

Signiert und gehasht wird **immer** eine deterministische CBOR-Kodierung (RFC 8949,
Core Deterministic Encoding). Ohne Determinismus bricht die Verifikation — das ist
keine Designwahl, sondern Pflicht.

Regeln:

1. Top-Level ist eine CBOR-**Map** mit **uint-Keys** (kompakter als Text-Keys).
2. Definite-Length only. Keine indefinite-length Items.
3. Integer in kürzester Form.
4. Map-Einträge in **aufsteigender** Key-Reihenfolge.
5. Optionale Felder, die abwesend sind, **lassen ihren Key weg** (kein `null`).
   Anwesend ⟺ Key vorhanden.
6. Keine doppelten Keys. Keine Floats im Atom (`v` ist opake Bytes).

---

## 4. Domänen-Separation, Signatur, Claim-ID & Verkettung

**Core** = die deterministische CBOR-Map aller Felder **außer** `σ` (Keys 0–8). Das ist das
signierte *und* das adressierte Objekt; `σ` steht nie im Core.

**Domänen-Separatoren** (verhindern, dass eine Signatur oder ein Hash je über Protokoll- oder
Zweckgrenzen wiederverwendet werden kann):

```
DOM_SIG     = "claim-atom/v1/sig"
DOM_CID     = "claim-atom/v1/cid"
DOM_GENESIS = "claim-atom/v1/genesis"
```

**Berechnung:**

```
bytes    = cbor_deterministic(core)
claim_id = SHA-256( DOM_CID || bytes )                ; 32 B, Inhaltsadresse
σ        = Ed25519-Sign( sk_I, DOM_SIG || bytes )     ; 64 B, im Claim, nie im Core
```

`claim_id` adressiert den **Inhalt** und ist **signatur-unabhängig** — es hasht nur den Core,
nicht `σ`. `σ` beweist getrennt die **Urheberschaft** der Bytes. Verifikation:
`Ed25519-Verify(I, DOM_SIG || bytes, σ)`.

> **Offline-selbstenthalten (A1).** Weil `I` der volle 32-Byte-Ed25519-Verify-Key ist, trägt der
> Core sein eigenes Verifikationsmaterial — ein Claim ist ohne Nachschlagen prüfbar (Papier/QR).
> Preis ist Größe: 32 statt 16 Byte je Identity-Referenz. Die kompaktere Alternative (16-Byte-
> RNS-Hash + separat mitgeführter Pubkey) wurde bewusst verworfen: sie knüpft Offline-Prüfung an
> eine Nachschlage-Vorbedingung und öffnet einen 128-bit-Truncation-Kollisionsspielraum — bei
> einem sicherheitstragenden Identitätsverweis nicht akzeptabel.

**Verkettung.** `h_prev` ist die `claim_id` des unmittelbar vorhergehenden Claims *desselben
Autors*. Der erste Claim einer Identity (Genesis) setzt einen **identity-gebundenen Anker**:

```
h_prev_genesis = SHA-256( DOM_GENESIS || I )
```

Das bindet selbst den Genesis an die Identity — keine Cross-Identity-Verwechslung und kein über
alle Identities identischer Null-Anker. Jede Identity bildet damit genau **einen** linearen,
hash-verketteten Log.

**Equivocation.** Existieren zwei strukturell gültige Claims `C1 ≠ C2` (verschiedene `claim_id`)
mit gleichem `(I, h_prev)`, dann hat der Autor seinen Log geforkt. Das ungeordnete Paar
`{C1, C2}` ist ein selbstenthaltener, kryptografischer Equivocation-Beweis gegen `I`. Beide
bleiben gespeichert; nichts wird gelöscht. Die *Konsequenz* (z. B. Slashing) ist Sache der
ökonomischen/Policy-Schicht.

---

## 5. Der gesegnete Kern: `core/revoke` & `core/supersede`

Diese zwei Prädikate sind die einzige Stelle, an der das Protokoll einem Prädikat eine
kanonische Bedeutung gibt. Das ist **kein** Bruch von A2, weil ihre *gesamte* Bedeutung
im Lebenszyklus der **eigenen** Claims des Autors aufgeht — exakt das, was A2 dem Protokoll
zuspricht.

**Geschlossenes Aufnahmekriterium für `core`:** Gesegnet wird ausschließlich eine Operation,
deren vollständige Bedeutung im selbst-bezüglichen Lebenszyklus aufgeht. Genau zwei Operationen
bestehen diesen Test. `vouch`, `verdict`, `membership` u. a. machen Aussagen mit *sozialem
Wert* und fallen durch — sie können sich nicht in `core` schmuggeln.

### 5.1 Selbst- vs. fremd-bezüglich

- **Selbst-bezüglich** (`R.I == C.I`, wobei `R.J = [claim-ref, C.claim_id]`): rein strukturell
  prüfbar (gleicher Schlüssel, gültige Kette). Das ist Lebenszyklus → **verstanden**.
- **Fremd-bezüglich** („Alice erklärt Bobs Claim für ungültig"): erfordert soziale Befugnis.
  Das ist in Wahrheit ein **Verdikt/Sanktion** → reine Policy, opak, **nicht** Core.

### 5.2 `core/revoke@1`

`J = [claim-ref, ziel.claim_id]`, `ziel.I == revoke.I`. Markiert den eigenen Ziel-Claim
in der Default-Sicht als **inaktiv**. Löscht oder versteckt nichts — sowohl der Claim als
auch sein Widerruf bleiben sichtbar (das ist selbst soziale Information und von A3 ohnehin
verlangt).

### 5.3 `core/supersede@1`

`J = [claim-ref, ziel.claim_id]`, `ziel.I == supersede.I`. Ersetzt den eigenen Ziel-Claim;
der supersedierende Claim repräsentiert fortan die lebende Version. **Ordnung kommt aus der
Autorenkette (`h_prev`), nie aus Wall-Clock `t`** — über eine partitionierbare Mesh ist
`t` als globale Ordnung wertlos.

### 5.4 Default-Sicht & Policy-Override

- **Weicher Default:** Claims sind durch ihre Autoren widerrufbar/supersedierbar.
- **Opt-out:** Eine Nukleus-Policy darf bestimmte Prädikate für *irrevocable* erklären;
  Verifizierer unter dieser Policy ignorieren dann `revoke`/`supersede`, die auf solche
  Prädikate zielen. (Beispiel: ein Nukleus, der unwiderrufliche Selbstbindungen will.)

`revoke`/`supersede` sind selbst Claims in der Autorenkette — sie sind also geordnet und
gegen Equivocation geschützt wie alles andere.

---

## 6. Verifizierer-Pflichten (reiner Mechanismus)

Ein Claim `C` ist **strukturell gültig** gdw.:

1. `version` wird unterstützt;
2. `Ed25519-Verify(C.I, P(C), C.σ)` ist wahr;
3. falls `t_exp` vorhanden: `now ≤ t_exp`;
4. `h_prev` referenziert die bekannte vorige `claim_id` des Autors (oder 32×0x00 bei Genesis).

`C` ist **aktiv** (Default-Sicht) gdw. strukturell gültig **und**:

- kein strukturell gültiger `core/revoke@1`-Claim `R` mit `R.I == C.I` und
  `R.J == [claim-ref, C.claim_id]` existiert, **und**
- `C` nicht durch einen strukturell gültigen `core/supersede@1`-Claim desselben Autors
  ersetzt ist.

Eine Nukleus-Policy MAY die Aktiv-Sicht überschreiben (§5.4). **Alles jenseits davon** —
was ein Vouch wert ist, ob Mitgliedschaft ratifiziert ist — ist Policy und liegt außerhalb
dieser Spezifikation.

---

## 7. Profile (erste Ableitungen)

Ein Profil legt fest: welches `p`, welcher `J`-Typ, was in `v`, ob `N` Pflicht — plus die
Interpretation (Policy). Es fügt **kein Feld** hinzu. Das ist das radiale Prinzip konkret.

### 7.1 Bürgschaft — `nuc:<N>/vouch@1`

| Feld   | Belegung |
|--------|----------|
| `I`    | der Bürge |
| `J`    | `[identity, verbürgte_identity]` |
| `v`    | opak, Policy-geparst; Vorschlag: `{ weight ∈ [0,1], bond_ref?, note? }` |
| `N`    | **Pflicht** — Vertrauen ist kontextgebunden |
| `t_exp`| optional — zeitlich begrenzte Bürgschaft (harte Decke) |

- **Lebenszyklus:** Rücknahme via `core/revoke@1` (`J = [claim-ref, vouch.claim_id]`).
  Selbst-bezüglich → verstanden → in **jeder** Default-Sicht inaktiv. (Genau das schließt
  das Missbrauchs-Szenario: zieht Alice ihren Vouch für Bob zurück, verleiht er nirgends
  mehr Vertrauen — die Korrektheit hängt nicht an der Sorgfalt einzelner Implementierer.)
- **Interpretation (Policy, außerhalb Protokoll):** Kante im Trust-Graph; speist den
  personalisierten PageRank vom eigenen Seed; Bond & Slashing leben in der ökonomischen
  Schicht; eine inaktive (zurückgezogene) Kante trägt 0 Fluss bei.

### 7.2 Regelannahme — `nuc:<N>/accept-rules@1`

| Feld | Belegung |
|------|----------|
| `I`  | das Mitglied |
| `J`  | `[object-hash, H(Verfassungsobjekt vR)]` |
| `v`  | optional (z. B. Versionskennung), opak |
| `N`  | **Pflicht** — der Nukleus, den die Verfassung regiert |

- **Lebenszyklus:** Verfassungsupdate ⇒ neues Objekt ⇒ neuer Hash. Das Mitglied stellt
  `accept-rules@1` für den neuen Hash aus **und** supersediert (`core/supersede@1`,
  `J = [claim-ref, alte_annahme.claim_id]`) die vorige Annahme. Ordnung via eigene Kette,
  nie Wall-Clock.
- **Kollektive Ratifizierung — zwei Wege, beide außerhalb des Atoms:**
  1. *Komposition:* N Einzel-Annahmen + Interpretationsregel „ab t-of-n gilt ratifiziert".
  2. *FROST:* der Nukleus-Gruppenschlüssel co-signiert **eine** Ratifizierungs-Annahme.
- **Interpretation (Policy):** Mitgliedschaft / Konsens-Stufe 1.

---

## 8. Bewusst getragene v1-Grenzen

- **Ein-Schreiber-Annahme.** Eine Identity = ein logischer Schreiber = eine Kette. Mehrere
  Geräte mit demselben Schlüssel forken die eigene Kette ⇒ Selbst-Equivocation. Multi-Device
  erfordert daher eines von: (a) alle Signaturen über *ein* Gerät routen, (b) jedes Gerät als
  *eigene* Identity, oder (c) FROST über die Geräte. Reale operative Einschränkung, kein Bug —
  der Preis für triviale Tamper-Evidence ohne Konsens. Sauberer Fix später via Delegation
  (Sub-Keys), bewusst vertagt.
- **Keine Key-Rotation.** Schlüsselverlust = soziales Re-Bootstrap (neu verbürgen lassen),
  wie der Verlust eines physischen Schlüssels.
- **Keine Delegation im Core.** „Schlüssel A signiert für Identity B" schmuggelt Scope-Semantik
  ein; bleibt in der Interpretationsschicht, bis sich zeigt, dass Verifikation ohne sie nicht geht.
- **Oracle-Problem & physische Durchsetzung** liegen außerhalb des Atoms. Das Protokoll
  garantiert *Non-Repudiation* und *Record-Integrität* — nie die *Wahrheit* einer Behauptung
  und nie die *Durchsetzung* eines Verdikts.
- **Seed-Set.** Die gesamte Sybil-Resistenz steht und fällt mit der Integrität des initialen,
  out-of-band etablierten Ankersets. Das ist die wertbildende Entscheidung des Systems,
  kein technisches Detail.

---

## 9. Versionierung

`version` (Key 0) sitzt im Core und damit unter `σ`. Eine **inkompatible** Änderung erhöht
`version` **und** die Domänen-Separatoren (`claim-atom/v2/sig` usw.) — dadurch kollidiert eine
Signatur oder ein `claim_id` **nie** über Versionsgrenzen, selbst bei sonst gleichen Bytes.

Neue **Prädikate** brauchen dagegen **keinen** Version-Bump — sie sind Profile (§7) und ändern
weder Core noch Serialisierung, Signatur oder Validität. Genau das ist die radiale Einheit:
das Format wächst nicht, nur die Menge der Konventionen darüber.
