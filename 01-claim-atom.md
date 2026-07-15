# Claim-Atom — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Layer: Identity/Claim (Konvergenzpunkt des Stacks)

Das Claim-Atom ist das einzige Primitiv der oberen Schichten. Bürgschaft, Regelannahme,
Verdikt, Wert-Transfer und Mitgliedschaft sind keine eigenen Objekte, sondern *Profile* —
Nutzungskonventionen über genau diesem Atom. Ein Profil fügt **niemals** ein Feld hinzu.

---

## 1. Leitsätze (Geltungsrahmen)

- **A1 — Selbstenthalten & transport-agnostisch.** Ein Claim ist ein in sich geschlossenes
  Objekt aus Bytes. Es trägt alles, was zur Verifikation nötig ist, und reist über **beliebige**
  Medien (Funk-Mesh, QR, Papier, …). Transport steht **nie** im Atom; die Bindung an ein
  konkretes Transportnetz (z. B. Reticulum/LXMF) ist ein separates **Transport-Profil**, kein
  Kern-Bestandteil.
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
- **v1-Sparsamkeit.** Keine Key-Rotation im Core, keine Delegation im Core (siehe §8).

> **Selektive Stille (non-normativ, gehört zur Bedeutung — siehe VISION.md §4).** Das Atom
> ist ein *Mechanismus*, kein Gebot zu signieren. Der Default ist **Schweigen**: Ein Claim
> entsteht nur, wenn der Einsatz es rechtfertigt, nicht bei jeder Alltagshandlung. Das
> Protokoll kann Schweigen nicht erzwingen (das wäre Bedeutung), aber diese Spezifikation
> hält fest, dass „kein Claim" der Normalzustand ist — sonst liest sich die Schicht wie
> Totalüberwachung, die sie nicht ist. Verankerung der Norm: `VISION.md`; hier steht sie nur,
> weil der Leser dem Mechanismus zuerst hier begegnet.

---

## 2. Feldsatz

| CBOR-Key | Feld     | Typ / Größe              | Pflicht | Bedeutung |
|---------:|----------|--------------------------|:-------:|-----------|
| 0        | `version`| uint (= 1)               | ja      | Formatversion. |
| 1        | `I`      | bytes[32]                | ja      | Signierer-Identity = Ed25519-Verify-Key. |
| 2        | `J`      | array `[tag, value]`     | ja      | Subjekt, polymorph (§2.1). |
| 3        | `p`      | text                     | ja      | Prädikat-ID, namensraum-qualifiziert + versioniert (§2.2, Anhang A). |
| 4        | `v`      | bytes                    | nein    | Opaker, prädikat-definierter Wert. Protokoll parst ihn nie. |
| 5        | `N`      | bytes[32]                | nein    | Scope = 32-Byte-Nukleus-Scope-ID. Strukturell erstklassig (§2.3). |
| 6        | `t`      | uint (Unix-Sekunden)     | ja      | Vom Autor behaupteter Zeitstempel. **Kein** Ordnungsprimitiv. |
| 7        | `t_exp`  | uint (Unix-Sekunden)     | nein    | Lokale strukturelle Gültigkeitsdecke. Danach ist der Claim void (§5.3, §6). |
| 8        | `h_prev` | bytes[32]                | ja      | Hash des vorherigen Claims desselben Autors; Genesis = `SHA-256(DOM_ID_GEN ‖ I)` (§4). |
| 9        | `σ`      | bytes[64]                | ja*     | Ed25519-Signatur über das Preimage (§4). |

\* `σ` (Key 9) ist im *signierten* Objekt Pflicht und im *Signatur-Preimage* abwesend.

Alle Referenzen sind einheitlich 32 Byte (Ed25519-Key **oder** SHA-256-Hash), die Signatur
64 Byte. Das hält die Wire-Form kompakt — wichtig für LoRa. **Keine Truncation, nirgends**
(Scope-Sicherheit §2.4, Invariante 1).

### 2.1 `J` — Subjekt (polymorph)

`J = [tag: uint, value: bytes[32]]`. Der Tag ist ein **geschlossener** Enum; er ist Mechanismus,
weil der Verifizierer wissen *muss*, worauf der Claim zeigt:

| Tag  | Name         | `value` ist … |
|-----:|--------------|---------------|
| 1    | `identity`   | Ed25519-Verify-Key der referenzierten Identity. |
| 2    | `claim-ref`  | `claim_id` (SHA-256) eines konkreten Claims (§4). |
| 3    | `object-hash`| SHA-256 eines externen Objekts (z. B. Regeldokument, Datei). |

Mehr Typisierung wäre bereits Semantik und bleibt draußen. Ein **unbekannter Tag** ist
strukturell ungültig → Reject (§6, Anhang B): Der Verifizierer kann nicht raten, worauf ein
Claim zeigt.

### 2.2 `p` — Prädikat

Format: `<namespace>/<name>@<version>`, z. B. `nuc:hasenpfote/vouch@1`. Die vollständige
formale Grammatik steht in **Anhang A**; dieser Abschnitt bleibt normativ maßgeblich.

**Scope-Isolation (normativ, v1):**

1. **Kanonische Kodierung (empfohlen, interoperabel):**
   `namespace = nuc:<scope_id_hex>`, wobei `scope_id_hex` **exakt 64 Kleinbuchstaben-Hexziffern**
   (= 32-Byte-Scope-ID) sind, z. B. `nuc:a1b2…ff/vouch@1`.
2. **Alias-Kodierung (nicht interoperabel ohne `N`):**
   Ein Alias aus `[a-z0-9_-]+` (Anhang A) ist erlaubt, aber der **autoritative Scope** eines
   Claims lebt dann ausschließlich im Feld `N`. Zwei Nuklei mit identischem `p`-String
   (`nuc:custom/vouch@1`) kollidieren **nicht**, solange `N` unterschiedlich ist und Verifizierer
   `N` bindend auswerten. Ein Alias **MUSS** das kanonische Muster `^[0-9a-f]{64}$` **nicht**
   matchen (§2.4, Invariante 3) — sonst wäre die Kodierungs-Erkennung mehrdeutig.
3. **Bindungsregel:** Für jedes `nuc:…`-Profil **MUSS** `N` gesetzt sein und **MUSS** dem
   aufgelösten Scope entsprechen. Bei kanonischer Kodierung **MUSS** `N == bytes.fromhex(scope_id_hex)`
   gelten; bei Alias-Kodierung ist `N` die einzige Scope-Quelle. Diese Prüfung ist reine
   **Byte-Gleichheit** — das Atom bleibt blind für die *Herkunft* von `N` (§2.3).
4. **Evaluator-Partitionierung:** Trust-Flow, Profile und Governance partitionieren
   Claim-Mengen nach dem **aufgelösten Scope** (`resolve_scope(N)`), nicht nach dem
   rohen `p`-String allein (§2.4, Invariante 2).

- **Genau zwei gültige Namensräume in v1:** das geschlossene **`core`** und das offene
  **`nuc:<scope>`** (Anhang A). Ein Prädikat, dessen Namensraum **weder** `core` **noch** `nuc:`
  ist, ist **strukturell ungültig → Reject** (`UNKNOWN_NAMESPACE`, Anhang B). Das hält die
  Scope-Autorität einzig an `N` (§2.4, Invariante 2) und verhindert einen wildwachsenden
  Namensraum-Zoo neben `N`.
- Namensraum **`core`** ist protokoll-reserviert und **geschlossen**: genau `core/revoke@1` und
  `core/supersede@1` (§5). Jedes andere `core/*` ist strukturell ungültig → Reject (§2.4,
  Invariante 4).
- **Innerhalb `nuc:<scope>` ist der Prädikat-*Name* opak/Policy.** Das Protokoll behandelt ihn
  als undurchsichtigen Identifier; seine Bedeutung lebt vollständig in der Interpretationsschicht.
  Neue Profile (`vouch`, `accept-rules`, `validation`, `timestamp`, …) sind genau das: neue
  **Namen** unter `nuc:`, **kein** neuer Namensraum — deshalb wächst die Grammatik nie mit.

### 2.3 `N` — Scope (Atom bleibt blind für die Herleitung)

Optionaler 32-Byte-Verweis auf die Scope-ID eines Nukleus. **Strukturell** erstklassig: Der
Verifizierer partitioniert die Trust-Flow-Berechnung pro `N` (Vertrauen ist kontextgebunden).
`N` abwesend = kontextfreier Claim (z. B. ein reiner Identity-Announce oder ein `core/*`-Claim).

**Das Atom kennt die *Herleitung* von `N` nicht.** Dass `N` der Hash eines unveränderlichen
Nukleus-Genesis-Objekts ist — `N = SHA-256(DOM_NUC_GEN ‖ cbor(genesis_obj))` —, ist eine
**Governance-/Fundament-Definition** (siehe `00-nucleus-genesis-constitution.md §3`) und lebt bewusst *nicht* hier. Für das
Atom ist `N` ein opaker 32-Byte-Bezeichner; seine einzige atom-lokale Regel ist die
Byte-Gleichheit aus §2.2 Regel 3. So bleibt die Scope-ID stabil über FROST-Re-Keying und
Schlüsselrotation hinweg (der Grund, warum sie ein Objekt-Hash und **kein** Pubkey ist), ohne
dass das bedeutungsblinde Atom davon etwas wissen muss.

### 2.4 Scope-Sicherheit (normativ — sechs Invarianten)

Die Autorität eines Scopes hängt **einzig** an `N` (32 Byte, 256-bit-kollisionssicher). Es gibt
keinen globalen Namensraum, also nichts zu squatten, und kurze/ratbare Alias-Strings tragen
**null** Sicherheitsgewicht. Der reale Angriffsvektor ist nicht Krypto, sondern *menschliche
Verwechslung*. Die folgenden Invarianten machen die Auflösung wasserdicht:

1. **Keine Truncation.** Alle Referenzen (`I`, `N`, `claim_id`, `h_prev`) sind volle 32 Byte.
   Schließt Birthday-/Truncation-Kollisionen aus (die Begründung aus §4 als globale Invariante).
2. **`N` ist die einzige Autorität.** Partitionierung und Auflösung laufen immer über
   `resolve_scope(N)`, nie über den rohen `p`-String. Ein Homoglyph- oder Doppel-Alias kann
   keinen Scope kapern.
3. **64-Hex reserviert.** Aliase **MÜSSEN** `^[0-9a-f]{64}$` **nicht** matchen; dieses Muster
   ist kanonischer Kodierung vorbehalten.
4. **`core` ist geschlossen.** Verifizierer **MÜSSEN** jedes `core/*` außer `{revoke@1,
   supersede@1}` ablehnen. Fremd-adressierte Revokes sind über `R.I == C.I` (§5.1) ohnehin
   ungültig.
5. **Kanonische Re-Serialisierung ist Pflicht** (§3, §6). Dadurch ist `claim_id` eine echte
   Inhaltsadresse; es gibt keine CBOR-Malleability und kein „Grinding" mehrerer IDs für
   denselben logischen Claim (das würde Dedup und Equivocation-Erkennung vergiften).
6. **Alias-Display SHOULD auflösen.** Für sicherheitstragende Anzeige oder Cross-Nukleus-Aktion
   zeigt/handelt die Implementierung auf dem aufgelösten `N`, nicht auf dem Alias-String.

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

**Durchsetzung (normativ):** Ein Verifizierer, der Bytes empfängt, **MUSS** den dekodierten Core
neu kanonisch serialisieren und mit den empfangenen Bytes **byte-genau** vergleichen. Bei
Abweichung → Reject (`NON_CANONICAL_ENCODING`, Anhang B). Ohne diesen Check ist die Kodierung
mehrdeutig und `claim_id` faktisch vom Autor frei wählbar (§2.4, Invariante 5).

---

## 4. Domänen-Separation, Signatur, Claim-ID & Verkettung

**Core** = die deterministische CBOR-Map aller Felder **außer** `σ` (Keys 0–8). Das ist das
signierte *und* das adressierte Objekt; `σ` steht nie im Core.

**Domänen-Separatoren** (verhindern, dass eine Signatur oder ein Hash je über Protokoll- oder
Zweckgrenzen wiederverwendet werden kann):

```
DOM_SIG    = "claim-atom/v1/sig"
DOM_CID    = "claim-atom/v1/cid"
DOM_ID_GEN = "claim-atom/v1/id-genesis"
```

> `DOM_NUC_GEN = "claim-atom/v1/nucleus-genesis"` gehört **nicht** hierher — es ist der
> Separator für die Nukleus-Scope-ID und lebt in `00-nucleus-genesis-constitution.md §3` (§2.3). Das Atom
> definiert nur die drei obigen.

**Berechnung:**

```
bytes    = cbor_deterministic(core)
claim_id = SHA-256( DOM_CID ‖ bytes )                ; 32 B, Inhaltsadresse
σ        = Ed25519-Sign( sk_I, DOM_SIG ‖ bytes )     ; 64 B, im Claim, nie im Core
```

`claim_id` adressiert den **Inhalt** und ist **signatur-unabhängig** — es hasht nur den Core,
nicht `σ`. `σ` beweist getrennt die **Urheberschaft** der Bytes. Verifikation:
`Ed25519-Verify(I, DOM_SIG ‖ bytes, σ)`.

> **Offline-selbstenthalten (A1).** Weil `I` der volle 32-Byte-Ed25519-Verify-Key ist, trägt der
> Core sein eigenes Verifikationsmaterial — ein Claim ist ohne Nachschlagen prüfbar (Papier/QR).
> Preis ist Größe: 32 statt 16 Byte je Identity-Referenz. Die kompaktere Alternative (ein
> 16-Byte-Truncation-Hash + separat mitgeführter Pubkey) wurde bewusst verworfen: sie knüpft
> Offline-Prüfung an eine Nachschlage-Vorbedingung und öffnet einen 128-bit-Truncation-
> Kollisionsspielraum — bei einem sicherheitstragenden Identitätsverweis nicht akzeptabel
> (§2.4, Invariante 1).

**Verkettung.** `h_prev` ist die `claim_id` des unmittelbar vorhergehenden Claims *desselben
Autors*. Der erste Claim einer Identity (Genesis) setzt einen **identity-gebundenen Anker**:

```
h_prev_genesis = SHA-256( DOM_ID_GEN ‖ I )
```

Das bindet selbst den Genesis an die Identity — keine Cross-Identity-Verwechslung und kein über
alle Identities identischer Null-Anker. Jede Identity bildet damit genau **einen** linearen,
hash-verketteten Log.

> **`h_prev = 32×0x00` ist verboten (harter Reject).** Der Null-Vektor ist **kein** gültiger
> Genesis-Anker und **kein** gültiger Vorgänger. Ein Claim mit `h_prev = 32×0x00` wird abgelehnt
> (`INVALID_GENESIS_ANCHOR`, Anhang B), **nicht** als *pending* gehalten. Das sperrt naive
> Implementierungen aus, die einen Null-Genesis nachbauen. Negativer Vektor: **NV1** (Anhang C).

**Equivocation.** Existieren zwei strukturell gültige Claims `C1 ≠ C2` (verschiedene `claim_id`)
mit gleichem `(I, h_prev)`, dann hat der Autor seinen Log geforkt. Das ungeordnete Paar
`{C1, C2}` ist ein selbstenthaltener, kryptografischer Equivocation-Beweis gegen `I`. Beide
bleiben gespeichert; nichts wird gelöscht. Equivocation invalidiert strukturell gültige
Downstream-Claims **nicht** rückwirkend — sie **flaggt den Autor** (Zustand
`equivocation-flagged`, Anhang B). Die *Konsequenz* (z. B. Slashing) ist Sache der
ökonomischen/Policy-Schicht. Positiver Beweis-Vektor: **NV3** (Anhang C, teilt `(I, h_prev)`
mit TV1).

> **Warum das die Schlüssel-Diebstahl-Frage automatisch löst (DF-0).** Ein gestohlener Schlüssel,
> der zwei konkurrierende Nachfolger signiert (etwa zwei `rotate-key@1`, §8), erzeugt exakt diese
> Equivocation — ein selbst-validierender Beweis. Die Entscheidung, welcher Zweig gilt, fällt
> dadurch **zwangsläufig an die Mitglieder** (Governance-Akt), ohne dass der Core dafür ein
> Sonder-Primitiv braucht.

---

## 5. Der gesegnete Kern: `core/revoke` & `core/supersede`

Diese zwei Prädikate sind die einzige Stelle, an der das Protokoll einem Prädikat eine
kanonische Bedeutung gibt. Das ist **kein** Bruch von A2, weil ihre *gesamte* Bedeutung
im Lebenszyklus der **eigenen** Claims des Autors aufgeht — exakt das, was A2 dem Protokoll
zuspricht.

**Geschlossenes Aufnahmekriterium für `core`:** Gesegnet wird ausschließlich eine Operation,
deren vollständige Bedeutung im selbst-bezüglichen Lebenszyklus aufgeht — strukturell prüfbar
ohne Weltwissen. Genau zwei Operationen bestehen diesen Test. `vouch`, `verdict`, `membership`
u. a. machen Aussagen mit *sozialem Wert* und fallen durch — sie können sich nicht in `core`
schmuggeln.

### 5.1 Selbst- vs. fremd-bezüglich

- **Selbst-bezüglich** (`R.I == C.I`, wobei `R.J = [claim-ref, C.claim_id]`): rein strukturell
  prüfbar (gleicher Schlüssel, gültige Kette). Das ist Lebenszyklus → **verstanden**.
- **Fremd-bezüglich** („Alice erklärt Bobs Claim für ungültig"): erfordert soziale Befugnis.
  Das ist in Wahrheit ein **Verdikt/Sanktion** → reine Policy, opak, **nicht** Core.

### 5.2 `core/revoke@1`

`J = [claim-ref, ziel.claim_id]`, `ziel.I == revoke.I`. Markiert den eigenen Ziel-Claim
in der Default-Sicht als **inaktiv**. Löscht oder versteckt nichts — sowohl der Claim als
auch sein Widerruf bleiben sichtbar (das ist selbst soziale Information und von A3 ohnehin
verlangt). Positiver Vektor: **TV3** (Anhang C).

### 5.3 `core/supersede@1`

`J = [claim-ref, ziel.claim_id]`, `ziel.I == supersede.I`. Ersetzt den eigenen Ziel-Claim;
der supersedierende Claim repräsentiert fortan die lebende Version. **Ordnung kommt aus der
Autorenkette (`h_prev`), nie aus Wall-Clock `t`** — über eine partitionierbare Mesh ist
`t` als globale Ordnung wertlos.

> **Lifecycle-Claims tragen kein `t_exp` (Monotonie, normativ).** `core/revoke@1` und
> `core/supersede@1` **SHOULD** kein `t_exp` setzen; ein Verifizierer **MUSS** ein `t_exp` auf
> einem `core/*`-Claim **ignorieren**. Grund: Ein ablaufender Widerruf würde in einer Partition
> das widerrufene Vertrauen *wiederbeleben* → **Über-Vertrauen**, exakt die eine gefährliche
> Richtung (Trust-Flow §7). Lifecycle ist **monoton**: einmal wirksam gesehen, permanent
> wirksam.

### 5.4 Default-Sicht & Policy-Override

- **Weicher Default:** Claims sind durch ihre Autoren widerrufbar/supersedierbar.
- **Opt-out:** Eine Nukleus-Policy darf bestimmte Prädikate für *irrevocable* erklären;
  Verifizierer unter dieser Policy ignorieren dann `revoke`/`supersede`, die auf solche
  Prädikate zielen. (Beispiel: `obligation@1`, damit ein Schuldner seine Schuld nicht per
  Selbst-Widerruf löscht — Profile-II §3.3.3.)

`revoke`/`supersede` sind selbst Claims in der Autorenkette — sie sind also geordnet und
gegen Equivocation geschützt wie alles andere.

---

## 6. Verifizierer-Pflichten & Zustandsmodell

Ein Claim durchläuft eine **Zustandsmaschine**, deren *sämtliche intrinsischen Zustände ein
einzelnes Gerät offline aus den gehaltenen Bytes plus seiner lokalen Zeit berechnen kann* — ohne
Weltwissen, ohne einen externen Dienst. Diese Offline-Berechenbarkeit ist die tragende
Eigenschaft; sie *erzeugt* die Partitionstoleranz. Die vollständige Fehlerklassen- und
Übergangstabelle steht in **Anhang B**; hier die normative Kurzfassung.

**Strukturell gültig** gdw.:

1. `version` wird unterstützt;
2. der Core ist **kanonisch** kodiert (§3: Re-Serialisierung byte-gleich), dekodierbar, ohne
   doppelte Keys, mit korrekten Feldtypen;
3. `J.tag` ist im geschlossenen Enum (§2.1);
4. Namensraum von `p` ist `core` **oder** `nuc:` (sonst `UNKNOWN_NAMESPACE`, §2.2); bei
   `nuc:…`-Prädikat: Bindungsregel §2.2 Regel 3 erfüllt; bei `core/*`: Prädikat ∈
   `{revoke@1, supersede@1}` und `J.tag == claim-ref` und `ziel.I == C.I`;
5. `Ed25519-Verify(C.I, DOM_SIG ‖ bytes, C.σ)` ist wahr;
6. `h_prev ≠ 32×0x00` (§4); ist `h_prev == SHA-256(DOM_ID_GEN ‖ C.I)`, ist `C` ein
   **Genesis**-Claim;
7. falls `t` **und** `t_exp` vorhanden: `t < t_exp` (reine Feld-Konsistenz — ein Claim, der
   behauptet, vor seiner eigenen Erstellung abzulaufen, ist inkohärent; **kein** Wall-Clock
   nötig).

**Zeit — `now` ist bewusst lokal und subjektiv (normativ).** Die Gültigkeitsprüfung gegen `t_exp`
lautet: falls `t_exp` vorhanden, gilt `C` als *zeitlich gültig* gdw. `now ≤ t_exp`, wobei `now`
die **lokale Zeitquelle des Verifizierers** ist (eigene Uhr **oder** ein Zeitdienst, dem er
vertraut — siehe VISION.md §5). `t_exp` ist **keine Ordnungs-**, sondern eine **lokale
Gültigkeitsaussage**. Konsequenzen:

- **Zwei Verifizierer dürfen legitim uneins sein**, ob ein Claim abgelaufen ist. Das ist kein
  Bug. Die **sichere Richtung** ist stets **Unter-Vertrauen**: Im Zweifel den Claim *nicht* für
  trust-gewährende Zwecke heranziehen.
- **Offline-Fall (keine Zeitquelle).** Ist keine vertraute Zeitquelle verfügbar, ist die
  `t_exp`-Gültigkeit lokal **unentscheidbar** → der Claim wird für trust-gewährende Zwecke
  **nicht** herangezogen (Unter-Vertrauen). Nicht-zeitkritische Verarbeitung (z. B. Verkettung,
  Offline-Pooling, Vorberechnung, die online nur noch validiert werden muss) läuft davon
  unberührt weiter.

**Aktiv** (Default-Sicht) gdw. strukturell gültig, zeitlich gültig, **verlinkt** (Vorgänger
bekannt & gültig) **und**:

- kein strukturell gültiger `core/revoke@1`-Claim `R` mit `R.I == C.I` und
  `R.J == [claim-ref, C.claim_id]` existiert, **und**
- `C` nicht durch einen strukturell gültigen `core/supersede@1`-Claim desselben Autors
  ersetzt ist.

**Pending statt Reject (kritische Klärung).** Ist `C` strukturell gültig, aber sein `h_prev`
referenziert einen **noch unbekannten** Vorgänger (Partial-Sync über Gossip), dann ist `C`
**pending** — es wird **gehalten**, nicht abgelehnt. Das folgt derselben „sichere Richtung"-Logik
wie Trust-Flow §7: Fehlende Vorgänger senken nur, was ich weiß; sie machen einen Claim nicht zu
Müll. Sobald der Vorgänger eintrifft, wird `C` **linked** und (falls nicht neutralisiert)
**active**.

**Idempotenz.** `claim_id` ist inhaltsadressiert; ein doppelt empfangener Claim (Gossip-Replay)
ist ein **idempotenter No-op**, kein Fehler.

Eine Nukleus-Policy MAY die Aktiv-Sicht überschreiben (§5.4). **Alles jenseits davon** —
was ein Vouch wert ist, ob Mitgliedschaft ratifiziert ist — ist Policy und liegt außerhalb
dieser Spezifikation.

> **Validierungs-Nodes sind orthogonal, kein Atom-Zustand.** Die Attestierung eines (gestakten)
> Validierungs-Nodes ist *externe Korroboration* = zusätzliche Claims = ein Profil höherer
> Schicht (ein **Confidence-Signal** für Policy/Trust-Flow). Sie **gatet** die intrinsische
> Zustandsleiter **nicht**. Die intrinsischen Zustände sind endlich (Anhang B); darüber gibt es
> unbegrenzt viele Confidence-Tiers via Attestierung. Sobald ein *intrinsischer* Zustand einen
> externen Dienst *bräuchte*, verlöre das Atom seine Offline-/Partitions-Eigenschaft — deshalb
> die strikte Trennung.

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
| `t_exp`| optional — zeitlich begrenzte Bürgschaft (lokale Gültigkeitsdecke, §6) |

- **Lebenszyklus:** Rücknahme via `core/revoke@1` (`J = [claim-ref, vouch.claim_id]`).
  Selbst-bezüglich → verstanden → in **jeder** Default-Sicht inaktiv. (Genau das schließt
  das Missbrauchs-Szenario: zieht Alice ihren Vouch für Bob zurück, verleiht er nirgends
  mehr Vertrauen — die Korrektheit hängt nicht an der Sorgfalt einzelner Implementierer.)
- **Interpretation (Policy, außerhalb Protokoll):** Kante im Trust-Graph; speist den
  personalisierten PageRank vom eigenen Seed; Bond & Slashing leben in der ökonomischen
  Schicht; eine inaktive (zurückgezogene) Kante trägt 0 Fluss bei.

Referenz-Vektor: **TV1** (Genesis-Vouch Alice → Bob, Anhang C).

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

Referenz-Vektoren: **TV2** (Alice, verkettet auf TV1) und **TV4** (Bob, Genesis; Anhang C).

---

## 8. Bewusst getragene v1-Grenzen

- **Ein-Schreiber-Annahme.** Eine Identity = ein logischer Schreiber = eine Kette. Mehrere
  Geräte mit demselben Schlüssel forken die eigene Kette ⇒ Selbst-Equivocation. Multi-Device
  erfordert daher eines von: (a) alle Signaturen über *ein* Gerät routen, (b) jedes Gerät als
  *eigene* Identity, oder (c) FROST über die Geräte. Reale operative Einschränkung, kein Bug —
  der Preis für triviale Tamper-Evidence ohne Konsens. Sauberer Fix später via Delegation
  (Sub-Keys), bewusst vertagt.
- **Key-Rotation: nicht im Core, aber ausdrückbar (DF-0).** Der Core kennt keine Rotation.
  Der **Normalfall** ist ein verkettetes `rotate-key@1`-**Profil** (Interpretationsschicht,
  **kein** `core`): Der alte Schlüssel signiert als letzten Akt seiner Kette einen Verweis auf
  den neuen. **Verlust/Diebstahl** löst ein **Governance-Akt** (`00 §6.2`). Ein gestohlener Schlüssel,
  der zwei Nachfolger signiert, erzeugt automatisch eine **Equivocation** (§4) — die Wahl des
  gültigen Zweigs fällt damit zwangsläufig an die Mitglieder. Kein neues Atom-Feld nötig.
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

---

## Anhang A — Prädikat-Grammatik (normativ)

Ergänzt §2.2; bei Konflikt gilt §2.2. ABNF (RFC 5234), gefolgt von äquivalenten Regexen.

```abnf
predicate    = namespace "/" name "@" version
namespace    = core-ns / nuc-ns
core-ns      = "core"
nuc-ns       = "nuc:" scope
scope        = canonical-scope / alias-scope
canonical-scope = 64HEXLOW            ; exakt 64 Kleinbuchstaben-Hex = 32-Byte-Scope-ID
alias-scope  = 1*aliaschar            ; MUSS NICHT canonical-scope matchen (§2.4, Inv. 3)
name         = 1*namechar
version      = nonzero *DIGIT         ; keine führende Null (kürzeste Form, §3)

HEXLOW       = DIGIT / %x61-66        ; 0-9 a-f
aliaschar    = %x61-7A / DIGIT / "-" / "_"   ; a-z 0-9 - _
namechar     = %x61-7A / DIGIT / "-" / "_"   ; a-z 0-9 - _
nonzero      = %x31-39                ; 1-9
```

Äquivalente Regexe (implementierungsfreundlich):

```
canonical scope : ^[0-9a-f]{64}$
alias scope     : ^(?![0-9a-f]{64}$)[a-z0-9_-]+$      ; negativer Lookahead sperrt 64-Hex
name            : ^[a-z0-9_-]+$
version         : ^[1-9][0-9]*$
core predicate  : ^core/(revoke|supersede)@[1-9][0-9]*$   ; v1: nur @1 aktiv (§2.2)
nuc predicate   : ^nuc:(?:[0-9a-f]{64}|(?![0-9a-f]{64}$)[a-z0-9_-]+)/[a-z0-9_-]+@[1-9][0-9]*$
```

Bindung an `N`: siehe §2.2 Regel 3 und §2.4 Invarianten 2–3. Die Grammatik prüft **Form**;
die **Autorität** prüft immer `N`.

---

## Anhang B — Verifizierer-Verhalten & Zustandsmaschine (normativ)

### B.1 Intrinsische Zustände (endlich, offline berechenbar)

Alle Zustände sind aus den gehaltenen Bytes + lokaler Zeit ohne Weltwissen bestimmbar.

| Zustand | Bedingung | Verhalten |
|---------|-----------|-----------|
| `malformed` | Signatur/CBOR/Kanonizität/`J`-Tag/Bindungsregel verletzt (§6.1–4) | **Reject**, nicht speichern |
| `pending` | strukturell gültig, aber `h_prev`-Vorgänger unbekannt (Partial-Sync) | **halten**, auf Vorgänger warten |
| `linked` | Vorgänger bekannt & gültig, Kette konsistent | weiter zu active/neutralisiert |
| `active` | linked, zeitlich gültig, nicht revoked/superseded | **Default-Sicht** |
| `revoked` | linked, gültiger selbst-bezüglicher `core/revoke@1` existiert | gültig, **inaktiv** |
| `superseded` | linked, durch eigenen `core/supersede@1` ersetzt | gültig, **inaktiv** |
| `expired` | linked, `t_exp` vorhanden und `now > t_exp` (lokal!) | lokal **inaktiv**; andernorts evtl. active |
| `equivocation-flagged` | zweiter gültiger Claim mit gleichem `(I, h_prev)`, andere `claim_id` | **beide speichern**, Autor flaggen; Downstream nicht rückwirkend invalide |

`expired` ist der einzige Zustand mit legitim **verifizierer-relativer** Belegung (§6, `now`
lokal). Alle anderen sind über Verifizierer hinweg deterministisch gegeben denselben Bytes.

### B.2 Fehlerklassen (Reject-Gründe)

| Code | Auslöser |
|------|----------|
| `UNSUPPORTED_VERSION` | `version` nicht unterstützt |
| `NON_CANONICAL_ENCODING` | Re-Serialisierung ≠ empfangene Bytes (§3) |
| `MALFORMED_CBOR` | nicht dekodierbar / doppelte Keys / falscher Feldtyp / indefinite-length |
| `UNKNOWN_J_TAG` | `J.tag` ∉ `{1,2,3}` (§2.1) |
| `UNKNOWN_NAMESPACE` | Namensraum von `p` ist weder `core` noch `nuc:` (§2.2) |
| `BAD_SCOPE_BINDING` | `nuc:…` ohne `N`, oder `N ≠ bytes.fromhex(scope)` bei kanonischer Kodierung (§2.2 R3) |
| `RESERVED_CORE_PREDICATE` | `core/*` ∉ `{revoke@1, supersede@1}` (§2.4 Inv. 4) |
| `FOREIGN_LIFECYCLE` | `core/revoke`/`supersede` mit `ziel.I ≠ C.I` (§5.1) |
| `BAD_SIGNATURE` | Ed25519-Verifikation schlägt fehl |
| `INVALID_GENESIS_ANCHOR` | `h_prev == 32×0x00` (§4) |
| `INCOHERENT_EXPIRY` | `t` und `t_exp` vorhanden und `t ≥ t_exp` (§6.7) |

### B.3 Nicht-Fehler (bewusst kein Reject)

- **Gossip-Replay**: identische `claim_id` erneut empfangen → **idempotenter No-op**.
- **Unbekannter Vorgänger**: → `pending` (nicht Reject), siehe B.1.
- **`t_exp` auf `core/*`**: → **ignorieren** (Monotonie §5.3), Claim ansonsten normal behandeln.
- **Lokaler Ablauf abweichend von anderen Verifizierern**: legitim, kein Fehler (§6, `now`).

---

## Anhang C — Test-Vektoren (real gerechnet, schema-valide, geteilt mit `00`)

Alle Werte sind **reproduzierbar** aus festen Ed25519-Seeds und kanonischem CBOR (RFC 8949,
`cbor2 canonical=True`). Hex durchgängig lowercase. Signaturen gegen `DOM_SIG ‖ bytes`
verifiziert; `claim_id = SHA-256(DOM_CID ‖ bytes)`. Das Beispiel-Nukleus (`N`, Genesis,
Verfassung) ist **schema-valide zu `00 §4/§5`** und **identisch** mit dem Worked-Example in
`00-nucleus-genesis-constitution.md §3.1` — die gesamte Spec-Reihe teilt damit *einen* Anker.

### C.0 Gemeinsame Parameter

```
DOM_SIG    = "claim-atom/v1/sig"
DOM_CID    = "claim-atom/v1/cid"
DOM_ID_GEN = "claim-atom/v1/id-genesis"
DOM_NUC_GEN= "claim-atom/v1/nucleus-genesis"        ; Nukleus-Scope-Separator (Def. 00 §3)

alice_seed = 01×32   ; Ed25519-Privatkey-Seed (32 Byte 0x01)
bob_seed   = 02×32

ALICE (I)  = 8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c
BOB   (I)  = 8139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b394

; Beispiel-Nukleus — schema-valide, siehe 00 §3.1 (dort mit Objekt-Feldern ausgeschrieben)
constitution_hash (CONST) = 890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e6585c352dcf19ccad5ea7e
N                         = 65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557

h_prev_genesis(ALICE) = SHA-256(DOM_ID_GEN ‖ ALICE)
                      = 62db0b05f44c17e2dfe7f371d631845fdd5858dd94c37d327a28f73b25625430
h_prev_genesis(BOB)   = SHA-256(DOM_ID_GEN ‖ BOB)
                      = d507038f3b07c8642b65e9b3cf559204d9ad7aa0a3faee674d4284a5d9e43abe
```

### C.1 TV1 — Genesis-Vouch (Alice → Bob), `v` und `t_exp` gesetzt

```
core = { 0:1, 1:ALICE, 2:[1, BOB], 3:"nuc:6530…5557/vouch@1",
         4:h'a1001864', 5:N, 6:1700000000, 7:1735689600, 8:h_prev_genesis(ALICE) }

bytes    = a900010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f75636840310444a1001864
           05582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d
           2f5557061a6553f100071a6774858008582062db0b05f44c17e2dfe7f371d631
           845fdd5858dd94c37d327a28f73b25625430
claim_id = f95d430e40df736cbdffd7bf82af4f77e0c7af8692565f3b2a151c2c1ae8660c
σ        = ef3b6674898a1f037bdb58dc485926b4f0de01ef995d6cbf7d6387c4dd33679f
           63da403f2f2d1c4bb39513484dee2c74387ec904bbab0aa22b8bdb376fb1c401
```

### C.2 TV2 — accept-rules (Alice), verkettet auf TV1, kein `v`, kein `t_exp`

```
core = { 0:1, 1:ALICE, 2:[3, CONST], 3:"nuc:6530…5557/accept-rules@1",
         5:N, 6:1700000100, 8:TV1.claim_id }

bytes    = a700010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c0282035820890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e
           6585c352dcf19ccad5ea7e0378536e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f6163636570742d72756c657340
           3105582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c
           7d2f5557061a6553f164085820f95d430e40df736cbdffd7bf82af4f77e0c7af
           8692565f3b2a151c2c1ae8660c
claim_id = 29b66881810bbbf1e254e061c35395e15da6c064327c2d33dfa6aa29d47dc2a6
σ        = 33220d6b1b744a76181311d9e724f5e43ab55608037bef5835f14c061d3fe0fd
           d13b8a54f94a118f698c591a85b06b29bd6dbdbdbdcd63ad3fcf6c278d851207
```

### C.3 TV3 — `core/revoke@1` (Alice widerruft TV1), kein `N`, kein `t_exp` (monoton)

```
core = { 0:1, 1:ALICE, 2:[2, TV1.claim_id], 3:"core/revoke@1",
         6:1700000200, 8:TV2.claim_id }

bytes    = a600010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c0282025820f95d430e40df736cbdffd7bf82af4f77e0c7af8692
           565f3b2a151c2c1ae8660c036d636f72652f7265766f6b654031061a6553f1c8
           08582029b66881810bbbf1e254e061c35395e15da6c064327c2d33dfa6aa29d4
           7dc2a6
claim_id = 8e76a2a9ee6677e6959bf9868dc6d162e5ff7e464a6bb4c6b839f89713e54629
σ        = 88388a4ad5f22d618dafef8a3bd877cd33f0e8899efdab3808cbd194adefb04f
           10123a0b34b3ab29a4f127b419ddde98e86c19417a2538bd31de22ba37df6006
```

Wirkung: TV1 wird in jeder Default-Sicht `revoked` (inaktiv), bleibt aber gespeichert (§5.2).

### C.4 TV4 — accept-rules (Bob, Genesis; zweiter Autor)

```
core = { 0:1, 1:BOB, 2:[3, CONST], 3:"nuc:6530…5557/accept-rules@1",
         5:N, 6:1700000050, 8:h_prev_genesis(BOB) }

bytes    = a700010158208139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df6
           0f5b8fc9b3940282035820890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e
           6585c352dcf19ccad5ea7e0378536e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f6163636570742d72756c657340
           3105582065309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c
           7d2f5557061a6553f132085820d507038f3b07c8642b65e9b3cf559204d9ad7a
           a0a3faee674d4284a5d9e43abe
claim_id = 0bd77591da5e480a8c9a573382d14407a1770e0a7f6d2d09776b630fbd7ca01c
σ        = 87ac5f22c62b87a105eb6b18dd80e0ca014cdfd6c602128be2dd917f35265cbf
           0933001dc891120b9a02a807e5608e29eb622e49252bcc933caf2c9f31f44c05
```

### C.5 NV1 — negativ: `h_prev = 32×0x00` → `INVALID_GENESIS_ANCHOR`

Signatur ist **gültig**; der Claim wird **allein wegen `h_prev`** abgelehnt (§4). Er wird
**nicht** als `pending` gehalten.

```
core = { 0:1, 1:ALICE, 2:[1, BOB], 3:"nuc:6530…5557/vouch@1",
         5:N, 6:1700000300, 8:00…00 (32×0x00) }

bytes    = a700010158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf374
           8801b40f6f5c02820158208139770ea87d175f56a35466c34c7ecccb8d8a91b4
           ee37a25df60f5b8fc9b39403784c6e75633a3635333039666532333364613330
           6664613036316437633565663030326236623830653432363832636435346437
           3033616231336662366337643266353535372f766f756368403105582065309f
           e233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557061a65
           53f22c0858200000000000000000000000000000000000000000000000000000
           000000000000
claim_id = 9b25020fee7da6832416f8bcb61e4a05329776d051a4da282db7e973eb96c453
σ        = 08fb042eae35833c6412cbcc18d73aeb2c9f45fb82a7e24a73351164fc1c0a3e
           c1dc13fb6288cb827d6c10d62afe2d8c17dc945867b14401bf2e99d8684cde07
erwartet = Reject: INVALID_GENESIS_ANCHOR
```

### C.6 NV3 — negativ: Equivocation gegen TV1 (gleiches `(I, h_prev)`)

Alice signiert einen **zweiten** Genesis-Claim auf demselben `h_prev` wie TV1 (nur `t`
differiert) → andere `claim_id`. Das Paar `{TV1, NV3}` **ist** der Equivocation-Beweis (§4).

```
core = { 0:1, 1:ALICE, 2:[1, BOB], 3:"nuc:6530…5557/vouch@1",
         5:N, 6:1700000001, 8:h_prev_genesis(ALICE) }   ; selbes h_prev wie TV1

claim_id = e14ebd82eb172672a4a3ccbc330fef64fecd86e4664f72eab538855c9cef5c8b
σ        = 959245d77a82c6099905ff781e61c917e7a1de4687a4bb8e84504b5191060ef9
           a81203a06e71a51144a66e886db3f62ba9fcd19171adb3f25b2288c4ef9fa403
erwartet = beide Claims speichern; Autor ALICE als equivocation-flagged markieren;
           Konsequenz (Slash) = ökonomische/Policy-Schicht (05)
```

### C.7 NV2 — negativ: nicht-kanonisches CBOR desselben Cores → `NON_CANONICAL_ENCODING`

Derselbe logische Core wie TV1, aber mit **unsortierten Map-Keys** kodiert. Der Verifizierer
dekodiert, re-serialisiert kanonisch und vergleicht — Mismatch → Reject.

```
nicht-kanonisch (Key-Reihenfolge 8,6,5,3,2,1,0,7,4):
           a908582062db0b05f44c17e2dfe7f371d631845fdd5858dd94c37d327a28f73b
           25625430061a6553f10005582065309fe233da30fda061d7c5ef002b6b80e426
           82cd54d703ab13fb6c7d2f555703784c6e75633a363533303966653233336461
           3330666461303631643763356566303032623662383065343236383263643534
           64373033616231336662366337643266353535372f766f756368403102820158
           208139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b3
           940158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801
           b40f6f5c0001071a677485800444a1001864

received == canonical            : false     → Reject
reserialize(received) == canonical: true     → gleicher Core, nur nicht-kanonisch kodiert
erwartet = Reject: NON_CANONICAL_ENCODING
```

## Änderungshistorie ggü. Vorentwurf (v1-Konsolidierung)

- **Genesis-`h_prev` vereinheitlicht** auf `SHA-256(DOM_ID_GEN ‖ I)` (Feldtabelle, §4, §6);
  `32×0x00` ist harter Reject (`INVALID_GENESIS_ANCHOR`, NV1). Drei widersprüchliche
  Definitionen entfernt.
- **`DOM_GENESIS` → `DOM_ID_GEN`** umbenannt (klare Abgrenzung zum Nukleus-Scope-Separator
  `DOM_NUC_GEN`, Def. `00 §3`).
- **`N` auf DF-0 gebracht:** 32-Byte-Scope-ID, Herleitung in `00` (§2.3); Atom prüft nur
  Byte-Gleichheit.
- **Scope-Sicherheit** als sechs normative Invarianten konsolidiert (§2.4).
- **Prädikat-Grammatik** formalisiert (Anhang A); Alias `[a-z0-9_-]+`, 64-Hex kanonisch
  reserviert, Version ohne führende Null.
- **`now`/`t_exp`-Widerspruch aufgelöst:** `now` lokal/subjektiv, `t_exp` lokale Gültigkeit,
  legitime Uneinigkeit, sichere Richtung = Unter-Vertrauen; Offline-Fall definiert (§6).
- **Zustandsmodell & Fehlerbehandlung** als Zustandsmaschine mit Fehlerklassen (§6, Anhang B);
  `pending` statt Reject bei unbekanntem Vorgänger; Replay idempotent; Re-Serialisierung Pflicht.
- **Lifecycle-Claims monoton:** `core/revoke`/`supersede` ohne `t_exp` (§5.3).
- **§8 Key-Rotation** auf DF-0 angeglichen (`rotate-key@1`-Profil / Governance-Akt;
  Diebstahl ⇒ Equivocation).
- **Selektive Stille** als non-normativer §1-Leitsatz mit VISION-Verweis.
- **Namensraum geglättet:** genau `core` + `nuc:` gültig; alles andere Reject
  (`UNKNOWN_NAMESPACE`); Prosa an Anhang-A-Grammatik angeglichen (§2.2, §6, Anhang B).
- **Test-Vektoren** real gerechnet (TV1–TV4, NV1–NV3; Anhang C); Beispiel-Nukleus
  jetzt schema-valide (00 §4/§5) und byte-identisch mit 00 §3.1 geteilt.
