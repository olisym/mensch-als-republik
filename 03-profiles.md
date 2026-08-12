# Claim-Profile II — Verdikt · Wert · Mitgliedschaft — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Erweitert: Atom-Spec §7 (Profile)

Diese drei Profil-Cluster vervollständigen die radiale Sicht. **Keiner** ändert das Atom:
kein neues Feld, kein neuer `J`-Typ — der Enum `{identity, claim-ref, object-hash}` deckt
alles ab. Das ist der Beweis des radialen Prinzips: verschiedene soziale Akte, ein Primitiv.

Diese Schicht ist **reine Komposition** über Layer 01 plus Policy. Kein Graph, keine Anker,
keine Kapazitäten, kein `TrustParams` — wer hier eine Flussrechnung sucht, ist in der
Trust-Flow-Spec richtig. Drei getrennte Cluster ergeben drei getrennte Funktionen (§6).

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
- **Normativ ist der Typ, nicht die Bedeutung.** Wo diese Schicht `v` liest, prüft sie die
  Kodierung und den Typ eines reservierten Keys — nie, was der Wert *bedeutet* (§1.3). Beträge
  werden nie verglichen, Einheiten nie aufgelöst.
- **Kein Zustand ohne Scope.** Jede Beziehung zwischen zwei Claims verlangt denselben `N`
  (§1.4). Die Bindungsregel des Atoms erzwingt das nicht.

### 1.1 Was „aktiv" heißt

**Aktiv** heißt in dieser ganzen Datei: der Zustand `active` der Zustandsmaschine aus
Atom-Spec §6 und Anhang B, ausgewertet **unter der Policy** aus §1.2. `pending` zählt nicht.
Das ist dieselbe Definition wie Trust-Flow-Spec §2; sie steht hier ein zweites Mal, weil sie
sonst beim nächsten Prädikat auseinanderläuft.

Da weder `accept-rules@1` noch `grant-membership@1` noch `receipt@1` noch
`submit-arbitration@1` irrevocable sind, fällt „aktiv unter der Policy" für sie mit „aktiv"
zusammen. Für `obligation@1` fällt es nicht zusammen — dort ist der Unterschied der ganze
Punkt (§3.3.3).

**Diese Schicht fragt ausschließlich auf `active` und unterscheidet die inaktiven Zustände
nicht.** Atom-Spec Anhang B legt zwischen `revoked`, `superseded` und `expired` bewusst keine
Rangfolge fest; solange nur „aktiv/inaktiv" gefragt wird, ist das folgenlos. **Ausnahme:**
`settlement()` unterscheidet `EXPIRED` von `OPEN` (§3.3.2) — dort ist die Frage nicht
„aktiv?", sondern „warum nicht?", und die Antwort ist normativ festgelegt.

### 1.2 Die Policy (Auflösung, Boden, Scope)

Der Verifizierer **wählt** die Policy nicht; sie wird aus dem Claim aufgelöst (Atom-Spec
§5.4.1):

```
C.N  →  Genesis-Objekt  →  constitution_hash  →  Verfassungsobjekt
                                              →  irrevocable_predicates   (Nukleus-Spec §5)
```

Jede Stufe ist content-adressiert und lokal nachrechenbar. Der Typ `NucleusPolicy` liegt in
**Layer 01** — er muss von dort importierbar sein, sonst wird der Import zyklisch. Die
**Auflösung** liegt hier, weil sie ein Objektmodell für Genesis und Verfassung braucht, das
Layer 01 nicht kennt.

```python
def resolve_policy(*, scope, genesis_obj, constitution_obj=None) -> PolicyResolution
```

`PolicyResolution` trägt `policy: NucleusPolicy` und `findings: tuple[Finding, ...]`.

**Der Resolver rechnet nach, statt zu glauben** (Nukleus-Spec §3): er prüft
`scope == SHA-256(DOM_NUC_GEN ‖ cbor(genesis_obj))` und, falls ein Verfassungsobjekt vorliegt,
`genesis_obj.constitution_hash == SHA-256(cbor(constitution_obj))`. Sonst wäre die
Content-Adressierung eine Behauptung.

| Lage | Antwort |
|---|---|
| Genesis passt nicht zu `scope` | `ValueError` |
| Verfassungsobjekt fehlt (Partition) | Sicherheits-Default, Vermerk `CONSTITUTION_UNAVAILABLE` |
| Verfassungsobjekt passt nicht zum `constitution_hash` | Sicherheits-Default, Vermerk `CONSTITUTION_HASH_MISMATCH` |
| beides passt | `irrevocable_predicates` der Verfassung, normalisiert |

Die Asymmetrie ist beabsichtigt. Ein falsches **Genesis** ist eine falsche Zuordnung — der
Zustand ist nicht unvollständig, sondern falsch, und dafür gibt es keine sichere
Voreinstellung (Präzedenz: Scope-Fehlpaarung in Atom-Spec §5.4). Eine fehlende oder nicht
passende **Verfassung** ist Teilwissen, und Teilwissen hat hier eine konservative Antwort:
`{"obligation@1"}` und sonst nichts (Nukleus-Spec §5.2).

**Normalisierung** geschieht im Konstruktor von `NucleusPolicy`, nicht hier — Boden setzen
(Nukleus-Spec §5.2), trust-gewährende Prädikate entfernen (Atom-Spec §5.4.3 b), `core`-Einträge
ignorieren (Atom-Spec §5.4.2). Der Resolver reicht `declared` durch und liest die Vermerke ab.

**Der Scope ist Pflichtfeld der Policy.** Eine Policy des Nukleus A auf einen Claim aus Nukleus
B anzuwenden wirft `ValueError` (Atom-Spec §5.4). Alle Funktionen dieser Schicht nehmen `scope`
und `policy`; stimmen `policy.scope` und `scope` nicht überein, wirft die Funktion, **bevor**
sie den Store anfasst.

### 1.3 `v`-Kodierung: typ-normativ, bedeutungsblind

Der Keyraum von `v` ist **prädikat-lokal**. `v` ist für das Atom opak; ein Key trägt nur
innerhalb seines Profils Bedeutung. Key `0` in `vouch@1` und Key `0` in `obligation@1` sind
verschiedene Dinge und kollidieren nicht.

| Profil | Key | Typ | Feld | gelesen? |
|---|---:|---|---|---|
| `obligation@1` | 0 | uint | `amount` | nein — uninterpretiert |
| | 1 | bstr | `unit_ref` | nein — byte-vergleichbar, nie geparst |
| `receipt@1` | 0 | uint | `amount` | **ja** — Anwesenheit verhindert Tilgung (§3.3.2) |
| `verdict@1` | 0 | uint | `outcome` | nein — Bedeutung ist Policy |
| | 1 | bstr | `reason_ref` | nein |
| `accusation@1` | — | — | keine reservierten Keys | vollständig opak |
| `submit-arbitration@1` | — | — | keine reservierten Keys | vollständig opak |

Die Keys von `vouch@1` stehen in Atom-Spec §7.1 und Trust-Flow-Spec §3.1 und werden hier nicht
wiederholt.

**Drei Regeln, alle in der Bauform von Atom-Spec §7.1** (geprüft wird der Key, nicht die Map
als Ganzes):

1. **Fehlt ein reservierter Key, ist das kein Fehler.** Kein Key dieser Schicht ist Pflicht.
2. **Ist er vorhanden, MUSS er den deklarierten Typ tragen.** Ein Verstoß erzeugt einen
   Vermerk (`INVALID_V_TYPE`), **keinen** Reject — das Atom hat den Claim bereits akzeptiert
   und wird nicht nachträglich strenger.
3. **Weitere Keys sind zulässig und opak.** Sie werden nicht gelesen und nicht bewertet.

**Kanonizität.** Ist `v` vorhanden und nicht kanonisch kodiert, gilt es als **unlesbar**:
Vermerk `NON_CANONICAL_V`, und kein reservierter Key wird gelesen. Die Prüfung steht **nach**
dem Dekodieren (ein undekodierbares `v` erzeugt bereits `UNPARSABLE_V`) und **vor** jeder
Typprüfung (Kodierung geht der Interpretation voraus). Begründung, Verstoßklassen und der
Grund, warum der Re-Serialisierungs-Check des Atoms `v` nicht abdeckt: Trust-Flow-Spec §3.1.

Für `receipt@1` ist die Folge **die sichere Richtung** und nicht folgenlos: ein unlesbares `v`
könnte einen Key `0` tragen, also **tilgt die Quittung nicht** (§3.3.2). Für `obligation@1`,
`verdict@1`, `accusation@1` und `submit-arbitration@1` bleibt es beim Vermerk — dort wird
nichts gelesen, was eine Wirkung hätte.

### 1.4 Scope-Bindung

Alle Prädikate dieser Schicht führen `N` als **Pflichtfeld**. Darüber hinaus gilt:

> **Normativ:** Wo zwei Claims in Beziehung gesetzt werden, MÜSSEN beide dasselbe `N` tragen,
> und dieses `N` MUSS der ausgewertete Scope sein.

Atom-Spec §2.2 Regel 3 erzwingt nur, dass `N` gesetzt und selbstkonsistent ist — **nicht**,
dass zwei Claims denselben Scope teilen. Ohne diesen Absatz quittiert eine Identität in
Nukleus B eine Schuld aus Nukleus A, und eine Unterwerfung aus Nukleus B bindet einen Streit
in Nukleus A. Betroffen sind: `receipt` ↔ `obligation` (§3.3.2), `verdict` ↔ `accusation` ↔
`submit-arbitration` (§2.4), `accept-rules` ↔ `grant-membership` (§4). Vermerk bei Verstoß:
`SCOPE_MISMATCH`.

---

## 2. Verdikt-Cluster

Ein Streit ist ein Thread aus Claims, die auf Claims zeigen. Beteiligte Profile:

### 2.1 `nuc:N/accusation@1`

| Feld | Belegung |
|------|----------|
| `I`  | der Ankläger |
| `J`  | `[identity, beschuldigte]` **oder** `[claim-ref, bestrittener_claim]` |
| `v`  | **vollständig opak** — keine reservierten Keys |
| `N`  | **Pflicht** — der Schlichtungs-Kontext |

Die Konvention, in `v` self-contained Beweise mitzuführen (z. B. bei Equivocation beide
widersprüchlichen Claims), bleibt sinnvoll und ist **an Menschen und Werkzeuge gerichtet, nicht
an Verifizierer**. Diese Schicht prüft sie nicht. Equivocation wird von Layer 01 ohnehin aus
dem Store erkannt (Atom-Spec §4); ein zweiter Prüfpfad hier wäre Redundanz mit eigener
Fehlerfläche.

### 2.2 `nuc:N/verdict@1`

| Feld | Belegung |
|------|----------|
| `I`  | der Schiedsrichter — oder ein FROST-Panel, das als **eine** Identity co-signiert |
| `J`  | `[claim-ref, accusation.claim_id]` — löst eine konkrete Anklage auf |
| `v`  | opak; reserviert: `0 : uint` Ausgang, `1 : bstr` Begründungs-Ref (§1.3) |
| `N`  | **Pflicht** — der Schlichtungs-Kontext |

`p` liegt im Policy-Namensraum (kein `core`) — Urteilen ist soziales Bewerten. Der **Ausgang**
wird von dieser Schicht nie gelesen: welche Severity ein Ausgang trägt und welche Antwort ihm
gebührt, ist Policy und Enforcement-Spec §3. Was diese Schicht beantwortet, ist eine einzige
Frage: **bindet dieses Verdikt?** (§2.4)

### 2.3 Wann ein Bond schlitzt (V2)

- **Objektiver Fehler** (Equivocation): der Beweis ist selbst-validierend — zwei gültige
  Signaturen, gleiches `(I, h_prev)`, verschiedene `claim_id` (Atom-Spec §4). Es braucht
  **kein** Verdikt; der Slash läuft **mechanisch** in der ökonomischen Schicht.
- **Über-Commitment** (`Σw > 1` im Scope, Trust-Flow-Spec §3.1): ebenfalls selbst-validierend,
  ebenfalls mechanisch. **Nicht zu verwechseln mit ungedeckter Emission** (§3.3.4), die genau
  das nicht ist.
- **Subjektiver Fehler** („nicht geliefert", „Regel gebrochen"): oracle-abhängig, **braucht**
  ein Verdikt (§2.2). Erst das Verdikt triggert den Slash — und nur, wenn es bindet (§2.4).

### 2.4 Bindungskraft und `submit-arbitration@1` (V3, aus C2 abgeleitet)

Ein Verdikt führt sich **nie** selbst aus. Seine Wirkung entsteht aus:

1. dem Trust-Gewicht des Schiedsrichters aus *Sicht des jeweiligen Beobachters*
   (Trust-Flow-Spec — jeder gewichtet selbst; das *ist* die Nicht-Monopol-Eigenschaft), und
2. **Bindung** nach Nukleus-Spec §5.1, und die ist maschinell entscheidbar.

#### 2.4.1 Das Profil

| `nuc:N/submit-arbitration@1` | Belegung |
|------|----------|
| `I`  | die sich unterwerfende Partei |
| `J`  | `[identity, schiedsrichter]` |
| `v`  | **vollständig opak** |
| `N`  | **Pflicht** — der Schlichtungs-Kontext |

Lebenszyklus über `core/revoke@1`, selbst-bezüglich. Die Bindung ist selbst ein Claim — das ist
die Komposition, die dieser Abschnitt behauptet, sauber durchgezogen. `submit-arbitration@1`
ist **nicht** irrevocable und darf es nicht sein: es verleiht Befugnis über eine Person, und
Fortbestehen ist dafür nicht die konservative Lesart (Atom-Spec §5.4.3 b).

#### 2.4.2 Die Funktion

```python
def verdict_status(store, *, verdict, scope, arbitrators, now,
                   policy=None) -> VerdictStatus     # BINDING | ATTRIBUTED_OPINION
```

`arbitrators` ist **Parameter**, kein Auflösungsergebnis: es ist `arbitration.arbitrators` aus
der Verfassung (Nukleus-Spec §5.1), und welche Verfassungsversion gilt, entscheidet die
Ratifizierung — eine Governance-Frage. Diese Schicht löst sie nicht auf, sie vergleicht
byte-weise. Aus demselben Grund findet hier **keine Schlüsselauflösung** statt: ein
FROST-Panel verifiziert als gewöhnliche Ed25519-Signatur unter seinem Gruppenschlüssel, und
`resolve_current_key` liegt außerhalb dieser Schicht (§5).

**`BINDING` gdw. das Verdikt aktiv ist und mindestens einer der beiden Pfade trägt:**

```
(i)   verdict.I ∈ arbitrators

(ii)  für beide Parteien P existiert ein aktiver Claim S mit
          S.p      == nuc:scope/submit-arbitration@1
          S.I      == P
          S.J      == [identity, verdict.I]
          S.N      == scope
```

Sonst `ATTRIBUTED_OPINION`. Ein Verdikt ohne Bindung ist eine signierte Meinung und löst
**keinen** Statuswechsel aus, unabhängig von seinem Ausgang (Enforcement-Spec §3).

#### 2.4.3 „Vorab" heißt „aktiv zum Bewertungszeitpunkt"

Nukleus-Spec §5.1 verlangt, dass beide Parteien sich **vorab** unterworfen haben. Zwischen zwei
verschiedenen Autoren gibt es keine Ordnung: Ordnung kommt aus der Autorenkette, nie aus
Wall-Clock `t` (Atom-Spec §5.3), und zwei Autoren teilen keine Kette. „Vorab" ist damit nicht
auswertbar.

> **Normativ:** Pfad (ii) verlangt, dass beide Unterwerfungen zum Bewertungszeitpunkt `now`
> **aktiv** sind. Ein Widerruf entzieht die Bindung; eine nachgereichte Unterwerfung stellt sie
> her.

Das ist auch die richtige Regel und nicht nur die berechenbare: wer eine Unterwerfung widerruft
und dabei bleibt, trägt sie nicht mehr, und wer sie später ausstellt, trägt sie. Beobachter
können über `now` uneins sein — dieselbe legitime Uneinigkeit wie bei `t_exp` (Atom-Spec §6),
und die sichere Richtung ist auch hier die schwächere Aussage: `ATTRIBUTED_OPINION`.

#### 2.4.4 Wer die Parteien sind

Nukleus-Spec §5.1 spricht von „beiden Parteien", ohne sie zu benennen. Normativ:

| Partei | Auflösung |
|---|---|
| Ankläger | `accusation.I` |
| Beschuldigter, `accusation.J.tag == identity` | `accusation.J.value` |
| Beschuldigter, `accusation.J.tag == claim-ref` | der **Autor** des bestrittenen Claims |

Die Anklage wird über `verdict.J` gefunden. Ist sie nicht auflösbar — `verdict.J.tag` ist nicht
`claim-ref`, die Anklage ist lokal unbekannt, ihr `N` ist nicht `scope`, oder der bestrittene
Claim ist lokal unbekannt —, ist **Pfad (ii) nicht auswertbar**; Pfad (i) bleibt es. Trägt auch
er nicht, lautet die Antwort `ATTRIBUTED_OPINION` mit dem entsprechenden Vermerk. Teilwissen
senkt, was ich behaupten kann, und die schwächere Behauptung ist hier die sichere.

**Der Zustand der Anklage ist irrelevant.** Sie wird nur gelesen, um die Parteien zu
bestimmen; ob der Ankläger sie inzwischen widerrufen hat, ändert nichts daran, wer die Parteien
*waren*. Aktiv sein müssen die Unterwerfungen und das Verdikt selbst.

---

## 3. Wert

### 3.1 Preisblindheit (Marktneutralität)

Das Protokoll bestimmt nie, was etwas *wert* ist. Es trägt Behauptungen *über* Wert und
referenziert externen Trägerwert; Preisbildung (Angebot/Nachfrage echter Menschen) ist
Bedeutung und bleibt per A2 draußen. „Frei" betrifft den *Preis*; *Regeln* (gegen Betrug,
Nichtlieferung) bleiben lokal/konsensuell und werden von Trust- und Durchsetzungsschicht
getragen.

Konkret in dieser Datei: `amount` wird nie gelesen, nie verglichen, nie summiert; `unit_ref`
wird nie dereferenziert. Beide sind byte-vergleichbar und sonst nichts (§1.3).

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
| `v`    | opak; reserviert: `0 : uint` Betrag, `1 : bstr` `unit_ref` (§1.3) |
| `N`    | **Pflicht** — der Kredit-Kontext / die Unit-of-Account |
| `t_exp`| optional — befristete Verpflichtung; erzeugt `EXPIRING_OBLIGATION` |

**Zu `t_exp`.** Die Obligation ist irrevocable (§3.3.3), aber Irrevocability schützt gegen den
**nachträglichen** Willen des Schuldners, nicht gegen den bei Ausstellung vorprogrammierten
Verfall (Atom-Spec §5.4.3 a). Ein Schuldner kann seine Schuld also nicht widerrufen, wohl aber
so ausstellen, dass sie von selbst erlischt.

Verboten wird das nicht — befristete Verpflichtungen sind ein legitimer Fall (Service-Spec §5,
SLA-Fenster), und ein Verbot verlöre mehr, als es schützt. Entschärft ist es dadurch, dass die
Obligation **einseitig** ist: es gibt keine signierte Annahme des Gläubigers, er trägt die
Prüfpflicht ohnehin, und `t_exp` steht ihm vor der Gegenleistung sichtbar im Claim. Der Vermerk
macht die Falle für Werkzeuge lesbar, ohne ihr Bedeutung zuzuschreiben.

#### 3.3.2 `nuc:N/receipt@1` und die Tilgung

| Feld | Belegung |
|------|----------|
| `I`  | der **Gläubiger** (nur er kann Zahlung quittieren) |
| `J`  | `[claim-ref, obligation.claim_id]` |
| `v`  | opak; reserviert: `0 : uint` Betrag — **verhindert die Tilgung** |
| `N`  | **Pflicht** — derselbe Scope wie die Obligation |

**„Passend" ist ein vierteiliges strukturelles Prädikat.** Eine Quittung `R` passt zu einer
Obligation `O` gdw.:

```
R.J  == [claim-ref, O.claim_id]
R.I  == O.J.value      und  O.J.tag == identity
R.N  == O.N            und  O.N == scope
R aktiv  und  O aktiv (unter der Policy)
```

Die dritte Zeile ist **nicht** redundant (§1.4). Ohne sie quittiert eine Identität in Nukleus B
eine Schuld aus Nukleus A.

**Teil-Tilgung tilgt nicht.**

> **Normativ:** Trägt `receipt.v` den Key `0` — oder ist `receipt.v` unlesbar, könnte ihn also
> tragen (§1.3) —, **tilgt die Quittung nicht**. Vermerk `PARTIAL_RECEIPT_UNSUPPORTED`. Die
> Schuld bleibt stehen.

Die naive Auflösung — `receipt.v` opak lassen und jede Quittung als Voll-Tilgung werten — ist
die gefährliche: ein Gläubiger, der einen Teilbetrag meint, quittierte versehentlich die ganze
Schuld. Über-Tilgung, also die falsche Richtung. Der Erweiterungspfad bleibt offen, ohne dass
v1 rät.

**Die Funktion.**

```python
def settlement(store, *, obligation, scope, now, policy) -> SettlementResult
```

`policy` ist **Pflicht-Keyword ohne Default**, als einzige Funktion dieser Schicht. Begründung
in §5.

| Zustand | Lage |
|---|---|
| `SETTLED` | Obligation aktiv, passende aktive Quittung ohne Key `0` |
| `OPEN` | Obligation aktiv, keine passende Quittung — oder eine, die nicht tilgt |
| `EXPIRED` | Obligation durch `t_exp` erloschen |
| `INDETERMINATE` | Obligation `pending` oder unverlinkt — Teilwissen |

**Kein `bool`.** `EXPIRED` ist nicht kosmetisch: da `obligation@1` nach Nukleus-Spec §5.2
**immer** irrevocable ist, ist `t_exp` der einzige Weg, auf dem eine Obligation inaktiv wird —
der Fall ist nicht selten, sondern der einzige, und er verlangt vom Gläubiger etwas anderes als
`OPEN`. `INDETERMINATE` folgt derselben Linie wie Trust-Flow-Spec §7: auf Teilwissen `OPEN` zu
behaupten hieße, eine Schuld zu behaupten, die es vielleicht nicht gibt — die
Falschbeschuldigungsrichtung.

Ist `obligation` kein aktiver oder inaktiver `obligation@1`-Claim im Scope — falsches Prädikat,
falsches `N`, gar kein Claim —, wirft die Funktion `ValueError`. Das ist keine unvollständige
Lage, sondern eine falsche Zuordnung, und dafür gibt es keine sichere Voreinstellung.

**Die Zustände `revoked` und `superseded` sind für `obligation@1` unerreichbar**, weil der Boden
aus Nukleus-Spec §5.2 unbedingt gilt. Das ist keine Semantik, die getestet werden kann, sondern
eine Unmöglichkeit, die zugesichert wird — ein `assert` im Modul, kein Vektor.

**Die Quittung bleibt widerrufbar, Tilgung ist nicht monoton.** Siehe §5.

#### 3.3.3 Verpflichtungen sind irrevocable

`obligation@1` ist irrevocable — **immer**, als Protokoll-Boden, nicht als Pflicht des
Nukleus. Die Verfassung kann die Menge erweitern, nie verkleinern; die drei Fälle „sie
schweigt", „sie nennt `obligation@1`", „sie nennt anderes und lässt `obligation@1` weg" sind
identisch geschützt (Nukleus-Spec §5.2, Atom-Spec §5.4).

Ohne das könnte ein Schuldner seine eigene Schuld per selbst-bezüglichem `core/revoke@1`
löschen — der weiche Default „autoren-widerrufbar" ist *hier* das Sicherheitsloch. Tilgung
läuft **ausschließlich** über die Gläubiger-Quittung (§3.3.2), nie über Schuldner-Widerruf.

Der Widerruf bleibt gültig, gespeichert und sichtbar (A3, Atom-Spec §5.2); er hat nur keine
Wirkung auf den Zustand seines Ziels. Ein Schuldner, der es versucht, hinterlässt eine
signierte Spur des Versuchs — das ist selbst soziale Information.

**Die frühere Formulierung „eine Nukleus-Policy MUSS `obligation@1` als irrevocable markieren"
ist überholt** und war das Loch, das sie schließen wollte: eine Pflicht, die man vergessen
kann, ist kein Schutz.

#### 3.3.4 Ungedeckte Emission (Detect statt Prevent)

Mehr IOUs auszustellen, als man decken kann, ist in einer Partition möglich und danach
**auditierbar**: der signierte Schuldgraph ist vollständig nachvollziehbar. Es kostet
Reputation und Trust-Flow; Settlement läuft sozial über die Trust-Schicht. Kein Konsens nötig.

**Auditierbar ist nicht selbst-validierend.** Über-Commitment (§2.3) trägt die Deckungsgrenze
`Σn ≤ D` und ist damit mechanisch nachrechenbar; ungedeckte Emission hat keine solche Grenze.
Es gibt daher **keinen mechanischen Slash und keinen Stufe-3-Auslöser** aus diesem Titel
(Enforcement-Spec §3).

Eine Schranke `Σ amount ≤ credit_limit(I)` aus der Verfassung wurde erwogen und verworfen. Der
Grund ist nicht der Aufwand — die Prüfung wäre in genau dem Sinn bedeutungsblind, in dem
`n ≤ D` es ist. Der Grund ist, dass die Grenze willkürlich wäre: `Σw ≤ 1` ist ökonomisch
begründet, weil es **Haftung** bindet; eine Emissionsgrenze bindet nichts. In einem
Mutual-Credit-System setzt der **Gläubiger** das Limit pro Trustline, nicht die Verfassung pro
Person. Diese Form gehört in eine Wert-/Exchange-Schicht, die es nicht gibt (L4).

*Namensbereinigung:* was frühere Fassungen „Über-Emission" nannten, heißt durchgängig
**ungedeckte Emission**. „Über-Commitment" ist das andere Ding — zwei Silben Unterschied und
die gesamte Konsequenz.

### 3.4 Atomarer Tausch (Vorgriff, hier nicht spezifiziert)

„Reibungslos **und** sicher" über die Regime hinweg (Ware↔IOU, IOU↔Cashu) verlangt atomares
Settlement, damit keine Partei betrogen wird. Das ist **kein** Atom-Feld, sondern
Adaptor-Signatur-Kopplung (`s' = s + t`) auf der Anwendungsschicht. Wird mit der
Wert-/Exchange-Schicht eigens spezifiziert.

---

## 4. Mitgliedschaft (M1 — gegenseitig)

Mitgliedschaft in N ist **keine** eigene Aussage, sondern die **Konjunktion zweier aktiver
Claims** — reine Komposition, null neuer Mechanismus:

1. `nuc:N/accept-rules@1` von X für N — X *willigt ein*, gebunden zu sein (Atom-Spec §7.2).
2. `nuc:N/grant-membership@1` von N für X — N *willigt ein*, X aufzunehmen.

| `nuc:N/grant-membership@1` | Belegung |
|----------------------|----------|
| `I`  | ein zum Handeln für N **autorisierter** Schlüssel |
| `J`  | `[identity, X]` |
| `v`  | opak |
| `N`  | **Pflicht** — N |

**Die Autorisierungsregel ist `I ∈ authorized_keys`, nicht `I == N`.** Nukleus-Spec §7 ersetzt
die alte Regel: `N` ist der Hash des Genesis und identifiziert den Nukleus, während die
Autorität bei den Schlüsseln liegt, die *innerhalb* des Genesis stehen — genau diese Trennung
erlaubt Rotation ohne Identitätsverlust. Für `key_mode = 1` ist der autorisierte Schlüssel ein
FROST-Gruppenschlüssel, und eine FROST-Signatur verifiziert als gewöhnliche
Ed25519-Signatur unter ihm; das Atom bleibt unberührt.

```python
def membership(store, *, subject, scope, constitution_hash, now,
               authorized_keys, policy=None) -> MembershipResult
```

| Zustand | Lage |
|---|---|
| `MEMBER` | beide Claims aktiv |
| `APPLICANT` | nur `accept-rules` aktiv |
| `GRANT_ONLY` | nur `grant-membership` aktiv |
| `NONE` | keiner |

**Kein `bool`.** Enforcement-Spec §1 Stufe 4 unterscheidet **Ausschluss** (N widerruft den
Grant ⇒ `APPLICANT`) von **Austritt** (X widerruft die Annahme ⇒ `GRANT_ONLY`); mit einem
Wahrheitswert sind beide `False` und nicht auseinanderzuhalten. `GRANT_ONLY` ist als *Wirkung*
ungültig — niemand wird ohne Konsens gebunden —, aber der Zustand muss benennbar bleiben.

**`constitution_hash` ist Parameter, keine Auflösung.** `accept-rules@1.J =
[object-hash, H(Verfassung)]` bindet eine Mitgliedschaft an eine **Version**. Nach einem
Amendment sind alte Annahmen strukturell weiter aktiv, zeigen aber auf den vorigen Hash;
welche Version gilt, entscheidet die Ratifizierung über die `amendment`-Schwelle
(Nukleus-Spec §5.3) — eine Governance-Frage. Diese Schicht vergleicht byte-weise: eine Annahme
auf einen anderen Hash zählt für die abgefragte Version **gar nicht**. Vermerk
`CONSTITUTION_VERSION_MISMATCH`.

Ein `grant-membership@1` von einem Schlüssel außerhalb `authorized_keys` zählt ebenfalls nicht
und erzeugt `UNAUTHORIZED_GRANT_AUTHOR`.

`MembershipResult` trägt beide `claim_id` (oder `None`) und `findings`, in der Form von
`TrustResult`.

**Gehen ist gesegneter Widerruf (Atom-Spec §5):**
- **Austritt** = X widerruft seine `accept-rules` (selbst-bezüglich → verstanden).
- **Ausschluss** = N widerruft sein `grant-membership` (selbst-bezüglich → verstanden).

Self-Sovereignty bleibt gewahrt: die eigene Identity ist unentziehbar, ein eigener Nukleus
jederzeit gründbar — nur die *Aufnahme in ein bestimmtes N* ist beidseitig. Das ist
Hirschmans Exit, strukturell verankert.

---

## 5. Bewusst getragene Grenzen & gemachte Designentscheidungen

- **Die Quittung bleibt widerrufbar; Tilgung ist nicht monoton.** Die Obligation ist
  irrevocable, die Quittung nicht — der Gläubiger kann quittieren und den Widerruf
  nachschieben, die Schuld lebt wieder auf. Getragen, weil die Quittung per A3 sichtbar bleibt,
  ihr Widerruf selbst Evidenz ist und der Missbrauch ein oracle-abhängiger Streit ist — also
  genau der Fall, für den §2 das Verdikt vorsieht. *Verworfen:* `receipt@1` ebenfalls
  irrevocable zu empfehlen. Das sähe sicherer aus und erzeugte den schlechteren Fehlerzustand —
  eine irrtümliche Quittung wäre unheilbar, und die Korrektur wäre eine neue `obligation@1` des
  Gläubigers, also eine Schuld, die es nie gab.
- **`policy` ist nur in `settlement()` Pflicht.** Der Parameter hat in Layer 01 einen Default
  (`None` = heutige Semantik), und für `membership()` und `verdict_status()` ist er folgenlos,
  weil keines ihrer Prädikate irrevocable ist. Für `settlement()` ist er der ganze Punkt:
  `policy=None` läse den Schuldner-Widerruf als wirksam und öffnete das Schulden-Lösch-Loch
  eine Schicht höher. Die Asymmetrie ist Absicht.
- **`membership()` prüft `constitution_hash` und `policy` nicht gegeneinander.** Ein Aufrufer
  kann eine Policy übergeben, die aus einer anderen Verfassungsversion aufgelöst wurde. Heute
  folgenlos (keines der beiden Prädikate ist irrevocable); wird relevant, sobald es eines wird.
- **Der Kompositionspfad aus Governance-Spec §3 wird nicht gewertet.** Bei `vote_mode = 0`
  entsteht Mitgliedschaft durch Auszählung, ohne einzelnen `grant-membership`-Autor. Diese
  Schicht wertet **nur** den claim-basierten Pfad; ein Nukleus im Kompositionsmodus bekommt für
  seine ratifizierten Mitglieder `APPLICANT`, nicht `MEMBER`.
- **Keine Schlüsselauflösung.** `authorized_keys` ist Parameter; `resolve_current_key` und
  `rotate-key@1` samt Diebstahlsfällen (Nukleus-Spec §6.3) liegen außerhalb. Wer eine veraltete
  Schlüsselmenge übergibt, bekommt ein veraltetes Ergebnis — sichtbar, aber nicht erkannt.
- **Keine Emissionsschranke** (§3.3.4). Ungedeckte Emission ist auditierbar und sozial, nicht
  mechanisch.
- **Beweise in `accusation.v` werden nicht geprüft** (§2.1). Die Konvention richtet sich an
  Menschen.
- **Der Zweck-Tag in `vouch.v` Key `1` ist unkodiert.** Er ist Trust-Flow-Semantik und braucht
  einen `purpose`-Parameter in `trust()`/`rank()` sowie einen erweiterten Gruppenschlüssel;
  eigener Durchgang.
- **Keine Rangfolge der inaktiven Zustände.** Diese Schicht fragt auf `active` (§1.1). Sobald
  ein Konsument `revoked`, `superseded` und `expired` *unterscheidet*, muss Atom-Spec Anhang B
  eine Rangfolge bekommen — `settlement()` unterscheidet nur `expired` von „aktiv", und das ist
  hier normativ festgelegt, nicht aus Anhang B abgeleitet.
- **Atomarer Tausch ist vertagt** (§3.4) — Anwendungsschicht, Adaptor-Signaturen, kein
  Atom-Feld.
- **Preisblindheit** (§3.1) ist Absicht, nicht Lücke: ein freier Markt verlangt eine
  preisneutrale Schicht darunter.

---

## 6. Oberfläche und Modulschnitt

```
mensch_als_republik/profiles/
  policy.py      resolve_policy() -> PolicyResolution; Sicherheits-Default (Nukleus-Spec §5.2)
                 NucleusPolicy selbst liegt in Layer 01 — sonst wird der Import zyklisch
  membership.py  membership()     -> MembershipResult
  credit.py      settlement()     -> SettlementResult
  verdict.py     verdict_status() -> VerdictStatus
  findings.py    ProfileFinding, Finding(kind, subject)
```

Drei getrennte Funktionen statt einer, weil §1 drei getrennte Cluster behauptet und die
Trennung sonst nur in der Prosa steht.

`classify_all` aus der Trust-Flow-Schicht wird **geteilt, nicht kopiert**. Zwei Definitionen von
„aktiv" driften; eine geteilte kann es nicht.

`Finding` trägt `kind` und `subject` — ein nackter Code ohne Subjekt sagt dem Betreiber, dass
*etwas* nicht stimmte, nicht *was*. `findings` ist sortiert und dedupliziert. `ProfileFinding`
ist ein eigener Enum, kein Claim-Reject; wo ein Vermerk denselben Defekt bezeichnet wie in einer
anderen Schicht, trägt er **denselben String** (`NON_CANONICAL_V`), aber nicht dasselbe Symbol.

### 6.1 Vermerke

| Vermerk | Ausgelöst durch |
|---|---|
| `NON_CANONICAL_V` | `v` vorhanden, nicht kanonisch kodiert (§1.3) |
| `UNPARSABLE_V` | `v` vorhanden, nicht dekodierbar (§1.3) |
| `INVALID_V_TYPE` | reservierter Key mit falschem Typ (§1.3) |
| `SCOPE_MISMATCH` | zwei in Beziehung gesetzte Claims mit verschiedenem `N` (§1.4) |
| `CONSTITUTION_UNAVAILABLE` | Verfassungsobjekt lokal unbekannt (§1.2) |
| `CONSTITUTION_HASH_MISMATCH` | Verfassungsobjekt passt nicht zum `constitution_hash` (§1.2) |
| `UNSAFE_IRREVOCABLE_PREDICATE` | trust-gewährendes Prädikat in `irrevocable_predicates` (Atom-Spec §5.4.3 b) |
| `EXPIRING_OBLIGATION` | `obligation@1` mit `t_exp` (§3.3.1) |
| `PARTIAL_RECEIPT_UNSUPPORTED` | `receipt.v` trägt oder könnte Key `0` tragen (§3.3.2) |
| `CONSTITUTION_VERSION_MISMATCH` | `accept-rules` auf einen anderen Hash (§4) |
| `UNAUTHORIZED_GRANT_AUTHOR` | `grant-membership.I ∉ authorized_keys` (§4) |
| `UNKNOWN_ACCUSATION` | `verdict.J` löst keine bekannte Anklage im Scope auf (§2.4.4) |
| `UNRESOLVED_ACCUSED` | bestrittener Claim lokal unbekannt (§2.4.4) |
| `INACTIVE_VERDICT` | das bewertete Verdikt ist nicht aktiv (§2.4.2) |

Kein Vermerk erzeugt einen Reject. Das Atom hat den Claim akzeptiert; diese Schicht wird nicht
nachträglich strenger, sie sagt nur, was sie sieht.
