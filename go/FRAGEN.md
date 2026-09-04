# FRAGEN.md

Entscheidungen an Stellen, an denen `spec/01-claim-atom.md` mehrdeutig, unvollständig
oder mit dem Auftrag (zustandslose Einzelclaim-Prüfung) nicht wörtlich vereinbar ist.
Kein Eintrag ist eine Rückfrage.

---

## 1. §3 / §6 Regel 2 — Byte-Vergleich „Core“ gegen empfangene Bytes

**Offen:** Der Verifizierer muss den dekodierten Core kanonisch neu serialisieren und
mit den *empfangenen Bytes* byte-genau vergleichen. Die empfangenen Bytes eines Claims
sind das *signierte* Objekt und enthalten `σ` (Key 9). Der Core ist die Map *ohne* `σ`.
Ein Vergleich Core-Bytes == empfangene Bytes ist daher immer falsch.

**Lesart:** Die empfangene CBOR-Map (Keys 0–9, inklusive `σ`) wird als Ganzes kanonisch
neu kodiert und mit den Rohbytes verglichen. Der Core (Keys 0–8) wird separat kanonisch
kodiert, aber nur als Signatur-Preimage und als `claim_id`-Eingabe, nicht als
Kodierungs-Soll.

**Verworfen:** Core neu kodieren und mit den vollen Empfangbytes vergleichen — das
würde jedes wohlgeformte Claim mit Signatur als `NON_CANONICAL_ENCODING` ablehnen.
Verworfen, Core-Anteil aus dem Wire zu schneiden und nur diesen zu vergleichen: ohne
vorheriges Dekodieren ist der Schnitt nicht definiert, und die Kanonizität von `σ`
bliebe ungeprüft.

**Heute:** Der Text entscheidet das in §3 (Durchsetzung: die dekodierte Map einschließlich
`σ`; Block „Verglichen wird die Map, nicht der Core").

---

## 2. Auftrag vs. §6 Regel 4 / `FOREIGN_LIFECYCLE` — `ziel.I == C.I`

**Offen:** Strukturelle Gültigkeit von `core/revoke@1` und `core/supersede@1` verlangt
`ziel.I == C.I`. `ziel` ist nur als `claim_id` im Feld `J` vorhanden. Die Identity des
Ziels steht in einem anderen Claim. Der Auftrag verbietet Kenntnis anderer Claims.

**Lesart:** Die Gleichheit `ziel.I == C.I` wird nicht geprüft. `FOREIGN_LIFECYCLE` wird
nur ausgelöst, wenn `J.tag != 2` (`claim-ref`) — das ist lokal am Atom sichtbar und
macht die Selbstbezüglichkeit unmöglich.

**Verworfen:** `FOREIGN_LIFECYCLE` nie zu emittieren (dann hätte die Klasse in diesem
Layer keinen Auslöser). Verworfen, den Ziel-Claim nachzuschlagen — das ist Weltwissen.

**Heute:** Der Text entscheidet das in §6 Punkt 4, Anhang B.2 (`J.tag ≠ claim-ref` bei
`core/*` → `MALFORMED_CBOR`; `FOREIGN_LIFECYCLE` nur bei lokal bekanntem Ziel) und im
Absatz „Selbstenthaltene Gültigkeit". Die frühere Lesart, den lokalen Tag-Mangel als
`FOREIGN_LIFECYCLE` zu führen, ist damit verworfen. `FOREIGN_LIFECYCLE` wird in diesem
Layer nicht emittiert.

---

## 3. §6 / Anhang B — `now` / `expired` / unbekannter Vorgänger

**Offen:** Die Spec macht zeitliche Gültigkeit (`now ≤ t_exp`) und Verkettung
(`pending`/`linked`) zu Verifizierer-Pflichten. Der Auftrag verlangt Zustandslosigkeit,
kein Zeit-, Datei- oder Netzwerkzugriff, keine Vorgängerauflösung.

**Lesart:** Beides liegt außerhalb. Kein Vergleich mit einer Uhr. Ein nicht-Null-`h_prev`,
der keinem bekannten Vorgänger entspricht, ist kein Reject (Anhang B.3); ohne Speicher
gibt es kein `pending`. Ausgabe ist nur `ok` plus `claim_id` oder `reject` plus Klasse.

**Verworfen:** `time.Now()` für `t_exp` (Auftrag: keine Zeitzugriffe; `expired` ist
verifizierer-relativ und kein Reject). Verworfen, unbekannten Vorgänger als Reject zu
werten (spec: halten, nicht ablehnen).

**Heute:** Der Text benennt denselben Prüfumfang in §6 als „selbstenthalten gültig"
(Punkte 1–7 ohne den Konjunkt `ziel.I == C.I`). Zeitliche Gültigkeit, `pending` und
`linked` bleiben außerhalb; keines davon ist ein Reject (Anhang B.3).

---

## 4. Anhang B.2 — Reihenfolge der Fehlerklassen

**Offen:** Ein Claim kann mehrere Defekte gleichzeitig tragen. Die Spec nennt keine
Prüfreihenfolge.

**Lesart:**

1. Hex unlesbar / CBOR nicht genau ein Item / Typen der Map-Keys nicht dekodierbar →
   `MALFORMED_CBOR`
2. Re-Serialisierung ≠ Empfangbytes → `NON_CANONICAL_ENCODING`
3. Top-Level keine Map mit uint-Keys, oder Key 0 fehlt / kein uint → `MALFORMED_CBOR`
4. `version != 1` → `UNSUPPORTED_VERSION` (weitere v1-Felder werden nicht verlangt)
5. Extra-Keys oder v1-Feldtypen/-längen/-pflicht → `MALFORMED_CBOR`
6. `J.tag ∉ {1,2,3}` → `UNKNOWN_J_TAG`
7. Prädikat: Namensraum / Grammatik / `core/*` / Bindung / Lifecycle-Tag
8. `h_prev == 32×0x00` → `INVALID_GENESIS_ANCHOR`
9. `t ≥ t_exp` (nur wenn `t_exp` nicht an `core/*` ignoriert wird) → `INCOHERENT_EXPIRY`
10. Signatur → `BAD_SIGNATURE`

Kodierung vor Semantik, weil Anhang C BV3 dekodierbare Indefinite-Length ausdrücklich
als `NON_CANONICAL_ENCODING` führt, nicht als `MALFORMED_CBOR`. Signatur zuletzt: ein
Null-Anker ist unabhängig von der Urheberschaft ungültig.

**Verworfen:** Signatur vor Genesis/Ablauf (würde NV1 mit kaputter Signatur als
`BAD_SIGNATURE` statt `INVALID_GENESIS_ANCHOR` ausgeben). Verworfen, den ersten
Dekodierfehler hinter der Kanonizitätsprüfung zu verstecken.

**Heute:** Der Text entscheidet in Anhang B.2: keine Gesamtordnung der Klassen; verboten
ist nur ein Code, dessen Aussage die Bytefolge nicht trägt. `NON_CANONICAL_ENCODING`
ist falsch, wenn der dekodierte Inhalt einen Mangel trägt, den keine Kodierung behebt
(Nicht-uint-Schlüssel, doppelter Key, falscher Feldtyp). Die Feldtabelle gilt je Version:
bei ununterstützter Version ist der Code `UNSUPPORTED_VERSION`, v1-Pflichtfelder werden
dann nicht geprüft. Die oben stehende Reihenfolge bleibt als Implementierungswahl, soweit
mehrere wahre Aussagen möglich sind; sie wurde an den Vorrang (nicht-uint-Keys und
Nicht-Map vor Kanonizität) und an `J.tag ≠ claim-ref` → `MALFORMED_CBOR` angeglichen.

---

## 5. §5.3 / B.3 — `t_exp` auf `core/*` und `INCOHERENT_EXPIRY`

**Offen:** `t_exp` auf Lifecycle-Claims muss ignoriert werden. Gilt das auch für die
Feldkonsistenz `t < t_exp`?

**Lesart:** Ja. Ist `t_exp` auf `core/revoke@1` oder `core/supersede@1` gesetzt, findet
die Prüfung `t < t_exp` nicht statt — auch wenn `t ≥ t_exp`. Der Claim wird sonst
normal weitergeprüft.

**Verworfen:** `INCOHERENT_EXPIRY` trotzdem zu geben. „Ignorieren“ bedeutet, das Feld
nicht in eine Entscheidung einfließen zu lassen; ein Reject wäre das Gegenteil.
Verworfen, `t_exp` auf `core/*` als `MALFORMED_CBOR` abzulehnen — B.3 sagt bewusst
kein Fehler.

**Heute:** Der Text entscheidet das in §6 Punkt 7, §5.3 und Anhang B.3: auf `core/*`
entfällt die Feld-Konsistenz `t < t_exp`; `t ≥ t_exp` löst dort keinen Reject aus.

---

## 6. Fehlende Fehlerklasse für ungültige Prädikat-Form

**Offen:** Anhang A definiert eine Grammatik. Anhang B.2 hat kein `INVALID_PREDICATE`.
`UNKNOWN_NAMESPACE` gilt dem Namensraum, `RESERVED_CORE_PREDICATE` dem geschlossenen
`core`, `BAD_SCOPE_BINDING` der Bindung an `N`.

**Lesart:**

- String beginnt nicht mit `core/` und nicht mit einem grammatisch gültigen `nuc:…` →
  `UNKNOWN_NAMESPACE` (kein anerkannter Namensraum, einschließlich Großbuchstaben,
  führender Null in der nuc-Version, leerem Scope, Alias mit unzulässigen Zeichen).
- Präfix `core/` aber nicht exakt `core/revoke@1` bzw. `core/supersede@1` →
  `RESERVED_CORE_PREDICATE` (auch `core/revoke@2`, `core/revoke` ohne `@`,
  `core/foo@1`).
- Gültiges `nuc:` ohne `N`, oder kanonische 64-Hex und `N` ungleich jenen Bytes →
  `BAD_SCOPE_BINDING`.

**Verworfen:** Grammatikverstöße als `MALFORMED_CBOR` (der Feldtyp ist Text, die Form
ist Policy der Grammatik, nicht CBOR). Verworfen, eine nicht in B.2 stehende Klasse
zu erfinden.

**Heute:** Der Text entscheidet das in §2.2, Anhang A und Anhang B.2: ein `nuc:`-Präfix,
das die Grammatik verletzt, ist `INVALID_PREDICATE`. Die frühere Lesart, solche
Formverstöße unter `UNKNOWN_NAMESPACE` zu führen, ist damit verworfen.

---

## 7. Extra-Keys, fehlende Pflichtfelder, falsche Längen

**Offen:** Die Feldtabelle ist geschlossen, sagt aber nicht, welcher Code bei Key 10,
fehlendem `σ`, `I` mit 31 Byte oder `J` mit Länge ≠ 2 gilt.

**Lesart:** Alles das ist `MALFORMED_CBOR` („falscher Feldtyp“ weit gelesen: falsche
Major-Type, falsche Array-Länge, falsche Byte-Länge, fehlende Pflicht, unzulässiger
Key). Keys > 9 sind unzulässig. Optionale Keys 4, 5, 7 dürfen fehlen und lassen dann
ihren Key weg.

**Verworfen:** Extra-Keys zu ignorieren (§2.4 Invariante 5 / kanonische Inhaltsadresse:
ein Extra-Key ändert den Core und wäre sonst eine zweite ID-Familie für „denselben“
Claim). Verworfen, Längenfehler als eigene Klasse — B.2 hat keine.

Bei `version != 1` werden Extra-Keys und v1-Pflichtfelder nicht mehr geprüft
(`UNSUPPORTED_VERSION`). Eine fremde Version darf einen anderen Feldsatz haben.

**Heute:** Der Text entscheidet das in Anhang B.2 (`MALFORMED_CBOR`: falscher Feldtyp,
fehlendes Pflichtfeld, Key außerhalb der Feldtabelle, falsche Byte- bzw. Array-Länge)
und im Absatz „Die Feldtabelle gilt je Version".

---

## 8. Hex-Zeilen (Auftrag-Schnittstelle, nicht Spec)

**Offen:** Die Spec kodiert Beispiele lowercase. Der Auftrag sagt „Bytes … in Hex“,
ohne Alphabet, Innen-Whitespace oder Leerzeilen. „Je Eingabezeile genau eine
Ausgabezeile.“

**Lesart:**

- Ausgabe-`claim_id` immer lowercase (`encoding/hex`).
- Eingabe-Hex akzeptiert Groß- und Kleinbuchstaben (Hex ist Transport der Bytes).
- `TrimSpace` nur an den Zeilenenden; Innen-Whitespace macht die Zeile zu ungültigem
  Hex → `MALFORMED_CBOR`.
- Leere oder blanko Zeile: 1:1-Ausgabe `reject MALFORMED_CBOR` (leere Bytefolge ist
  kein Claim).
- Ungerade Länge, Nicht-Hex-Zeichen: `MALFORMED_CBOR`.

**Verworfen:** Leerzeilen zu überspringen (verletzt die 1:1-Vorgabe). Verworfen,
Innen-Whitespace zu streichen (würde eine zweite, nicht spezifizierte Hex-Norm
einführen). Verworfen, eine nicht in B.2 stehende Klasse `BAD_INPUT`.

---

## 9. Trailing-Bytes nach einem CBOR-Item

**Offen:** Ist `claim ‖ 0x00` nicht-kanonisch oder nicht dekodierbar?

**Lesart:** `MALFORMED_CBOR`. Die Eingabe muss *genau ein* CBOR-Item sein. Restbytes
sind kein zweites Encoding desselben Items.

**Verworfen:** Erst das erste Item dekodieren, neu kodieren, mit der *gesamten*
Eingabe vergleichen und `NON_CANONICAL_ENCODING` zu melden — das würde Trailing mit
indefiniter Länge in einen Topf werfen. BV3 ist dekodierbare Indefinite-Length *im*
Item.

**Heute:** Der Text entscheidet das in §3 („Die Eingabe ist genau ein Item") und
Anhang B.2 (`MALFORMED_CBOR`: Restbytes hinter dem Item).

---

## 10. Indefinite-Length, Break, Floats, Tags, Simple Values

**Offen:** B.2 unterscheidet dekodierbare Indefinite-Length (`NON_CANONICAL_ENCODING`,
BV3) von unabgeschlossener Indefinite-Length / Break in Wertposition
(`MALFORMED_CBOR`). Floats sind im Atom verboten (§3 Regel 6), haben aber keinen
eigenen Code.

**Lesart:** Wohlgeformte Indefinite-Length wird zu definite Werten dekodiert, definite
kanonisch neu kodiert; Byte-Differenz → `NON_CANONICAL_ENCODING`. Unabgeschlossen,
Break wo ein Wert sein muss, Major 6 (Tags), Major 7 (Floats, `true`/`false`/`null`,
unassigned simples), ungültiges UTF-8 in tstr, reservierte Additional-Info →
`MALFORMED_CBOR` schon beim Dekodieren. Floats werden nicht re-kodiert.

**Verworfen:** Indefinite-Length sofort als `MALFORMED_CBOR` (widerspricht BV3).
Verworfen, Floats kanonisch zu re-kodieren und als `NON_CANONICAL_ENCODING` zu
führen — sie sind im Atom nicht vorgesehen, und B.2 packt falsche Typen unter
`MALFORMED_CBOR`.

**Heute:** Der Text bindet die drei Längenform-Fälle in Anhang B.2 und C.8: dekodierbare
indefinite-length als einziger Mangel → `NON_CANONICAL_ENCODING`; unabgeschlossen oder
Break in Wertposition → `MALFORMED_CBOR`; indefinite-length plus Nicht-uint-Schlüssel →
`MALFORMED_CBOR` (Vorrang). Floats und Simple Values bleiben ohne eigenen Code;
`MALFORMED_CBOR` als falscher Feldtyp gilt weiter.

---

## 11. Doppelte Map-Keys: semantisch vs. kodiert

**Offen:** „Keine doppelten Keys.“ Sind `0x01` und `0x18 0x01` derselbe Key?

**Lesart:** Semantische Gleichheit der dekodierten Keys (zwei uints mit gleichem Wert,
zwei bstrs mit gleichem Inhalt, …). Bereits beim Dekodieren → `MALFORMED_CBOR`, nicht
erst über die Re-Serialisierung.

**Verworfen:** Nur byte-identische Key-Encodings als Duplikat (dann würde last-wins
plus kanonische Re-Kodierung fälschlich `NON_CANONICAL_ENCODING` liefern). B.2 nennt
doppelte Keys ausdrücklich unter `MALFORMED_CBOR`.

---

## 12. `N` auf `core/*`

**Offen:** „`N` abwesend = kontextfreier Claim (z. B. ein … `core/*`-Claim)“ — Beispiel
oder Verbot?

**Lesart:** Beispiel. `N` auf `core/revoke@1` / `core/supersede@1` ist zulässig und wird
nicht an `p` gebunden. Die Bindungsregel gilt nur für `nuc:`.

**Verworfen:** `N` auf `core/*` als `MALFORMED_CBOR` oder `BAD_SCOPE_BINDING`. Die Spec
verbietet das Feld dort nicht.

---

## 13. Alias vs. 64-Hex (Anhang A / §2.4 Inv. 3)

**Offen:** Die in Anhang A gedruckte nuc-Regex benutzt negativen Lookahead. Go’s RE2
kann das nicht. Außerdem: ist ein 65-Zeichen-Hex-String kanonisch oder Alias?

**Lesart:** Handparser nach ABNF, nicht die Regex. Kanonisch genau dann, wenn der
Scope *exakt* `^[0-9a-f]{64}$` ist. Jeder andere `[a-z0-9_-]+`-String (einschließlich
Länge 63 oder 65) ist Alias; `N` ist dann die einzige Scope-Quelle, ohne
Byte-Vergleich gegen den Alias-Text.

**Verworfen:** 65 Kleinbuchstaben-Hex als kanonisch zu behandeln (Inv. 3 reserviert
genau 64). Verworfen, die Lookahead-Regex wörtlich zu verlangen — die ABNF ist
maßgeblich (§2.2 bei Konflikt).

---

## 14. Profilregeln (§7) — `v`, Vouch-Gewicht, `J`-Typ je Profil

**Offen:** §7 schreibt für `vouch@1` einen `J`-Typ und eine CBOR-Map in `v` vor. §7
sagt zugleich, das Atom liest `v` nicht; ein Verstoß dort ist nie ein Reject.

**Lesart:** Zustandsloser Layer-01-Verifizierer prüft keine Profil-Belegungen. `v` ist
opake Bytes beliebiger Länge (einschließlich innerem nicht-kanonischem CBOR). `J.tag`
darf 1, 2 oder 3 sein, sobald der Namensraum `nuc:` ist. Nur `core/*` zwingt Tag 2.

**Verworfen:** Inneres `v` zu parsen oder Vouch ohne `J.tag==identity` abzulehnen —
das wäre Bedeutung, und der Auftrag hält Weltwissen und Profile draußen. Die
Kanonizität von `v` prüft „die lesende Schicht“ (§7.1).

**Heute:** Der Text hält in §7.1 fest, dass das Atom `v` nicht liest und ein Verstoß
dort nie ein Reject ist. Die Profil-Belegungen bleiben außerhalb.

---

## 15. Signatur-Preimage und Go-Ed25519

**Offen:** `σ = Ed25519-Sign(sk_I, DOM_SIG ‖ bytes)` — ist `DOM_SIG` UTF-8-Text oder
ein CBOR-tstr?

**Lesart:** Rohe ASCII-Bytes der in §4 in Anführungszeichen stehenden Strings,
konkateniert mit den Core-Bytes. Prüfung über `crypto/ed25519` der Standardbibliothek
(RFC 8032). `I` wird unverändert als 32-Byte-Verify-Key übergeben; ein Punkt, den die
Bibliothek zurückweist, ist `BAD_SIGNATURE`.

**Verworfen:** `DOM_SIG` selbst als CBOR zu kodieren (die Spec schreibt `‖`, nicht
`cbor(...)`). Verworfen, eine eigene Feldarithmetik zu bauen (Auftrag: Signatur aus
der Standardbibliothek).

---

## 16. Genesis-Anker außer Null

**Offen:** §6 Regel 6 definiert Genesis als `h_prev == SHA-256(DOM_ID_GEN ‖ I)` und
verbietet nur den Null-Vektor als Reject.

**Lesart:** Nur `h_prev == 32×0x00` ist `INVALID_GENESIS_ANCHOR`. Jeder andere
32-Byte-Wert — Genesis-Anker oder beliebige Folge-Hash — ist strukturell zulässig.
Ob der Vorgänger existiert, ist nicht Gegenstand dieser Prüfung.

**Verworfen:** Einen Nicht-Genesis-Erstclaim ohne Vorgänger abzulehnen (`pending`,
kein Reject). Verworfen, den Genesis-Anker als Pflicht für „den ersten“ Claim zu
erzwingen — ohne Log-Zustand gibt es kein „erster“.

---

## 17. Kanonische Re-Serialisierung: welche Map-Sortierung

**Offen:** RFC 8949 Core Deterministic Encoding sortiert Keys nach *kodierter*
Key-Form, nicht nach numerischem uint-Wert. Für Keys 0–9 fällt beides zusammen.

**Lesart:** Sortierung nach kodierter Key-Form, kürzeste Integer-Kodierung, nur
definite Längen. Negative Integers, Arrays und nicht-uint-Keys werden so re-kodiert,
damit eine unsortierte oder lang kodierte Map `NON_CANONICAL_ENCODING` wird, bevor
die Claim-Semantik greift.

**Verworfen:** Nur uint-Keys 0–9 zu akzeptieren schon im Decoder (dann wäre eine
unsortierte Text-Key-Map `MALFORMED_CBOR` statt ggf. `NON_CANONICAL_ENCODING`).
Encoding-Fehler sollen sichtbar bleiben (BV3-Logik).

**Heute:** Die Sortierung (RFC 8949, kodierte Key-Form) bleibt unentschieden im Text
und wird weiter so gelesen. Der Vorrang in Anhang B.2 ändert den zweiten Teil: eine
Map mit Nicht-uint-Schlüsseln ist `MALFORMED_CBOR`, auch wenn sie zusätzlich nicht
kanonisch kodiert ist. Die frühere Sorge, Text-Keys hinter der Kanonizität zu
verstecken, ist damit vom Text selbst aufgelöst.

---

## 18. §6 Punkt 4 — woran bindet „sonst `MALFORMED_CBOR`“

**Offen:** Punkt 4 schreibt: bei `core/*`: Prädikat ∈ `{revoke@1, supersede@1}` und
`J.tag == claim-ref` (sonst `MALFORMED_CBOR`). Das „sonst“ kann auf die ganze
Konjunktion gehen — dann wäre auch `core/rotate@1` `MALFORMED_CBOR` — oder nur auf
den Tag.

**Lesart:** Nur auf `J.tag`. Ein `core/*` außerhalb `{revoke@1, supersede@1}` ist
`RESERVED_CORE_PREDICATE`. Anhang B.2 und Anhang A sagen das ausdrücklich; §2.2 und
§2.4 Invariante 4 ebenfalls.

**Verworfen:** Die Konjunktion als Ganzes unter `MALFORMED_CBOR` zu führen. Das
würde der Fehlerklasse in B.2 widersprechen.

---

## 19. §6 Punkt 4 / Anhang A — Präfix `core/` und `nuc:` am Rohstring

**Offen:** „`p` beginnt mit `core/` oder `nuc:`“ kann den Rohstring meinen oder den
nach dem ersten `/` geparsten Namensraum. `nuc:/vouch@1` beginnt mit `nuc:`, hat
aber keinen Scope. `CORE/revoke@1` hat nach dem Slash den Namen `revoke`, aber das
Präfix ist nicht `core/`.

**Lesart:** Präfixtest auf den Rohstring. Beginnt `p` mit `nuc:` und verletzt die
Grammatik, ist der Code `INVALID_PREDICATE` — auch ohne `/`, mit leerem Scope, mit
Großbuchstaben im Namen, mit führender Null in der Version. Beginnt `p` mit `core/`,
ist jedes andere Reststück `RESERVED_CORE_PREDICATE`. Alles ohne diese zwei Präfixe
ist `UNKNOWN_NAMESPACE`.

**Verworfen:** Erst in Namensraum und Rest zu splitten und `nuc:` nur am Token zu
prüfen (`nuc:/vouch@1` wäre dann `UNKNOWN_NAMESPACE`, weil der Token `nuc:` mit
leerem Scope kein anerkannter Namensraum wäre). Der Text sagt „beginnt mit“.
Verworfen, `CORE/…` als `core` zu falten — die Grammatik ist kleinschreibungspflichtig.

---

## 20. Anhang B.2 Vorrang — Top-Level keine Map

**Offen:** Der Vorrang nennt als unfixierbare Mängel Nicht-uint-Schlüssel, doppelte
Keys und falschen Feldtyp. Ob eine Top-Level-Array- oder -Bytefolge, die nur in der
Längenform von ihrer kanonischen Kodierung abweicht, `NON_CANONICAL_ENCODING` oder
`MALFORMED_CBOR` ist, steht dort nicht.

**Lesart:** `MALFORMED_CBOR`. §3 Regel 1 verlangt eine Map. `NON_CANONICAL_ENCODING`
behauptet, es gebe eine kanonische Kodierung desselben Inhalts, die gültig wäre;
eine definite Array-Kodierung wäre immer noch kein Claim. C.15 sagt dasselbe für
ein kanonisches Array.

**Verworfen:** Indefinite Arrays als `NON_CANONICAL_ENCODING` zu führen, weil die
Re-Serialisierung andere Bytes liefert. Das wäre dieselbe falsche Aussage, die B.2
an BV2 verbietet.

---

## 21. Anhang B.2 Vorrang — fehlendes Pflichtfeld und Kanonizität

**Offen:** Der Vorrang listet fehlende Pflichtfelder nicht unter den Mängeln, die
`NON_CANONICAL_ENCODING` unwahr machen. Eine nicht-kanonisch kodierte Map ohne `σ`
trägt beides: Encoding-Mangel und fehlendes Pflichtfeld.

**Lesart:** Kanonizität wird nach Map/uint-Keys und vor dem v1-Feldsatz geprüft. Eine
wohlgetypte, nur unsortiert kodierte Map ohne `σ` ist `NON_CANONICAL_ENCODING`. C.7
führt genau diesen Fall (derselbe Core wie TV1, unsortierte Keys, ohne `σ`) unter
jenem Code. Fehlende Pflichtfelder sind ein v1-Tabellenmangel und greifen, sobald
die Kodierung selbst kein eigenes Urteil mehr trägt.

**Verworfen:** Fehlendes `σ` immer als `MALFORMED_CBOR`, auch wenn die Bytes zugleich
nicht kanonisch sind. Der Vorrang nennt diesen Mangel nicht, und C.7 würde sonst einen
falschen Satz über jene Folge erzwingen.

---

## 22. C.8 BV1 — Break in Wertposition, Dekodieren oder Re-Serialisieren

**Offen:** Der begleitende Text zu BV1 beschreibt eine Implementierung, die die Map
`{0: <break>}` dekodiert und erst beim Re-Serialisieren scheitert. Ein Decoder, der
Break außerhalb von Indefinite-Length nicht als Wert akzeptiert, scheitert früher.

**Lesart:** Break in Wertposition ist `MALFORMED_CBOR` schon beim Dekodieren. Anhang B.2
nennt „Break in Wertposition“ unter `MALFORMED_CBOR` und lässt den Schritt frei.

**Verworfen:** Einen eigenen Break-Wert im Decoder zu halten, nur um den Rundlauf
werfen zu lassen. Der Code wäre derselbe; der Text verlangt den Schritt nicht.

