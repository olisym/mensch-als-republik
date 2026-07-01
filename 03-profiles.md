# Claim-Profile II — Verdikt · Wert · Mitgliedschaft — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Erweitert: Atom-Spec §7 (Profile)

Diese drei Profil-Cluster vervollständigen die radiale Sicht. **Keiner** ändert das Atom:
kein neues Feld, kein neuer `J`-Typ — der Enum `{identity, claim-ref, object-hash}` deckt
alles ab. Das ist der Beweis des radialen Prinzips: verschiedene soziale Akte, ein Primitiv.

---

## 1. Leitsätze (zusätzlich zu Atom-Spec §1)

- **Objektiv schlitzt mechanisch, subjektiv verlangt ein Verdikt.** Ein selbst-validierender
  Beweis (Equivocation) braucht kein Urteil; ein oracle-abhängiger Streit braucht eines (§2).
- **Zwei getrennte Wertregime.** Trägerwert bleibt extern (Cashu, §3.2). Claim-natives Wert =
  gegenseitiger Kredit (§3.3). Das Protokoll ist **preisblind** — Preis ist Bedeutung (A2) und
  bleibt bei den handelnden Menschen.
- **Mitgliedschaft ist gegenseitig.** Aufnahme in N = Konjunktion aus Einwilligung des
  Individuums *und* des Nukleus (§4). Gehen — Austritt wie Ausschluss — ist selbst-bezüglicher
  Widerruf (Atom-Spec §5).

---

## 2. Verdikt-Cluster

Ein Streit ist ein Thread aus Claims, die auf Claims zeigen. Beteiligte Profile:

### 2.1 `nuc:N/accusation@1`

| Feld | Belegung |
|------|----------|
| `I`  | der Ankläger |
| `J`  | `[identity, beschuldigte]` **oder** `[claim-ref, bestrittener_claim]` |
| `v`  | opak: Vorwurf + **self-contained Beweise** (z. B. bei Equivocation beide widersprüchlichen Claims), damit A1 hält |
| `N`  | der Schlichtungs-Kontext |

### 2.2 `nuc:N/verdict@1`

| Feld | Belegung |
|------|----------|
| `I`  | der Schiedsrichter — oder ein FROST-Panel, das als **eine** Identity co-signiert |
| `J`  | `[claim-ref, accusation.claim_id]` — löst eine konkrete Anklage auf |
| `v`  | opak: Urteil (Ausgang, Begründungs-Ref) |
| `N`  | der Schlichtungs-Kontext |

`p` liegt im Policy-Namensraum (kein `core`) — Urteilen ist soziales Bewerten. Das Atom
erlaubt jedes `J`; das Obige ist die empfohlene Konvention, kein Zwang.

### 2.3 Wann ein Bond schlitzt (V2)

- **Objektiver Fehler** (Equivocation): der Beweis ist selbst-validierend — zwei gültige
  Signaturen, gleiches `(I, h_prev)`, verschiedene `claim_id` (Atom-Spec §4). Es braucht
  **kein** Verdikt; der Slash läuft **mechanisch** in der ökonomischen Schicht.
- **Subjektiver Fehler** ("nicht geliefert", "Regel gebrochen"): oracle-abhängig, **braucht**
  ein Verdikt (§2.2). Erst das Verdikt triggert den Slash.

### 2.4 Bindungskraft (V3, aus C2 abgeleitet)

Ein Verdikt führt sich **nie** selbst aus. Seine Wirkung entsteht aus:
1. dem Trust-Gewicht des Schiedsrichters aus *Sicht des jeweiligen Beobachters*
   (Trust-Flow-Spec — jeder gewichtet selbst; das *ist* die Nicht-Monopol-Eigenschaft), und
2. **Vorab-Bindung**: beide Parteien haben sich vorab diesem Schiedsspruch unterworfen.
   - *Stehend:* via `accept-rules@1` auf eine Verfassung, die die Schlichtung benennt.
   - *Ad-hoc:* via optionalem `nuc:N/submit-arbitration@1` (`J = [identity, schiedsrichter]`).

Ohne Vorab-Bindung ist ein Verdikt bloß eine signierte Meinung.

---

## 3. Wert

### 3.1 Preisblindheit (Marktneutralität)

Das Protokoll bestimmt nie, was etwas *wert* ist. Es trägt Behauptungen *über* Wert und
referenziert externen Trägerwert; Preisbildung (Angebot/Nachfrage echter Menschen) ist
Bedeutung und bleibt per A2 draußen. „Frei" betrifft den *Preis*; *Regeln* (gegen Betrug,
Nichtlieferung) bleiben lokal/konsensuell und werden von Trust- und Durchsetzungsschicht
getragen.

### 3.2 W1 — Trägerwert bleibt extern (Cashu-Linie)

Ein Cashu-Token *ist* der Wert: Inhaberinstrument, gültig durch die **Blindsignatur der
Mint**, übertragbar durch bloßes Weiterreichen des Geheimnisses, spurlos (Privacy). Das in
einen signierten Claim zu gießen würde genau die Bearer- und Privacy-Eigenschaft
**zerstören**.

- Das Atom transportiert **nie** Trägerwert.
- Kopplung: ein Claim darf ein externes Token per Hash **referenzieren** (`object-hash` in
  `J`, oder ein Hash in `v`) — z. B. eine Quittung, die auf das zahlende Token zeigt —, das
  Atom **validiert** es nie (das tut die Mint).
- Bekannter Preis: die Mint muss beim Einlösen erreichbar und ist ein Trust-Anchor (kann
  verweigern/inflationieren, aber nicht stehlen oder deanonymisieren).

### 3.3 W2 — Claim-natives Regime: gegenseitiger Kredit (LETS/Trustline-Linie)

Mintlos, voll auditierbar, im Trust-Graphen verankert. Kein Bearer-Double-Spend möglich —
eine signierte Schuld kann man nicht „doppelt ausgeben".

#### 3.3.1 `nuc:N/obligation@1`

| Feld   | Belegung |
|--------|----------|
| `I`    | der Schuldner |
| `J`    | `[identity, gläubiger]` |
| `v`    | opak; Vorschlag `{ unit_ref?, amount }` — die Recheneinheit definiert die Nukleus-Policy |
| `N`    | der Kredit-Kontext / die Unit-of-Account |
| `t_exp`| optional — befristete Verpflichtung (harte Decke) |

#### 3.3.2 `nuc:N/receipt@1`

| Feld | Belegung |
|------|----------|
| `I`  | der **Gläubiger** (nur er kann Zahlung quittieren) |
| `J`  | `[claim-ref, obligation.claim_id]` |
| `v`  | optional (z. B. Teilbetrag — siehe Grenzen) |

Tilgung = aktive `obligation` **plus** passende aktive `receipt` des Gläubigers ⇒ Policy
interpretiert die Schuld als beglichen.

#### 3.3.3 Verpflichtungen sind irrevocable (kritischer Punkt)

Hier greift der **Opt-out aus Atom-Spec §5.4**: Eine Nukleus-Policy MUSS `obligation@1` als
**irrevocable** markieren. Sonst könnte ein Schuldner seine eigene Schuld per
selbst-bezüglichem `core/revoke` löschen — der weiche Default „autoren-widerrufbar" ist
*hier* das Sicherheitsloch. Tilgung läuft **ausschließlich** über die Gläubiger-Quittung
(§3.3.2), nie über Schuldner-Widerruf. Das ist genau der Fall, für den wir den Opt-out gebaut
haben.

#### 3.3.4 Über-Emission (Detect statt Prevent)

Mehr IOUs auszustellen als man decken kann, ist in einer Partition möglich, danach aber
**beweisbar** (der signierte Schulden-Graph ist auditierbar) und kostet Reputation und
Trust-Flow. Settlement läuft sozial über die Trust-Schicht. Kein Konsens nötig.

### 3.4 Atomarer Tausch (Vorgriff, hier nicht spezifiziert)

„Reibungslos **und** sicher" über die Regime hinweg (Ware↔IOU, IOU↔Cashu) verlangt atomares
Settlement, damit keine Partei betrogen wird. Das ist **kein** Atom-Feld, sondern
Adaptor-Signatur-Kopplung (`s' = s + t`) auf der Anwendungsschicht. Wird mit der
Wert-/Exchange-Schicht eigens spezifiziert.

---

## 4. Mitgliedschaft (M1 — gegenseitig)

Mitgliedschaft in N ist **keine** eigene Aussage, sondern die **Konjunktion zweier aktiver
Claims** — reine Komposition, null neuer Mechanismus:

1. `accept-rules@1` von X für N — X *willigt ein*, gebunden zu sein (Atom-Spec §7.2).
2. `nuc:N/grant-membership@1` von N für X — N *willigt ein*, X aufzunehmen.

| `grant-membership@1` | Belegung |
|----------------------|----------|
| `I`  | N (Nukleus-Identity / FROST-Gruppenschlüssel) |
| `J`  | `[identity, X]` |
| `N`  | N |

Keiner allein genügt: Akzeptanz ohne Grant = Anwärter; Grant ohne Akzeptanz = ungültig
(niemand wird ohne Konsens gebunden).

**Gehen ist gesegneter Widerruf (Atom-Spec §5):**
- **Austritt** = X widerruft seine `accept-rules` (selbst-bezüglich → verstanden).
- **Ausschluss** = N widerruft sein `grant-membership` (selbst-bezüglich → verstanden).

Self-Sovereignty bleibt gewahrt: die eigene Identity ist unentziehbar, ein eigener Nukleus
jederzeit gründbar — nur die *Aufnahme in ein bestimmtes N* ist beidseitig. Das ist
Hirschmans Exit, strukturell verankert.

---

## 5. Bewusst getragene Grenzen & gemachte Designentscheidungen

- **`obligation@1` irrevocable** ist eine *Pflicht*-Policy, kein bloßer Default (§3.3.3). Ein
  Nukleus, der das vergisst, baut ein Schulden-Lösch-Loch.
- **Verdikt braucht Vorab-Bindung** (§2.4), sonst ist es Meinung. Das Protokoll erzwingt das
  nicht — es ist Komposition; die Bindung selbst ist ein Claim.
- **Atomarer Tausch ist vertagt** (§3.4) — Anwendungsschicht, Adaptor-Signaturen, kein
  Atom-Feld.
- **Teil-Tilgung** ist in v1 nicht modelliert; Default ist Voll-Tilgung pro `receipt`.
  Teilzahlung = mehrere kleinere `obligation`s oder ein `amount` im receipt-`v` (Policy-Erweiterung).
- **Recheneinheit** (`unit_ref`) ist Nukleus-Policy — das Protokoll parst Beträge nie (A2).
- **Preisblindheit** (§3.1) ist Absicht, nicht Lücke: ein freier Markt verlangt eine
  preisneutrale Schicht darunter.
