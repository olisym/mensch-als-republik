# Governance-Schicht — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Layer: Governance (über Trust-Flow und Profile)

Diese Schicht regelt, wie ein Nukleus seine eigenen Regeln ändert, ohne dass jemand befragt
werden muss, der über ihm steht. Sie fügt kein Atom-Feld hinzu. Vorschläge und Verfassungen sind
content-adressierte Objekte, auf die Claims zeigen; die Stimmen sind die Claims.

Zwei Sätze tragen die ganze Schicht:

> **Ein Nukleus lebt in Epochen.** Jede Epoche beginnt mit einer ratifizierten Verfassung; diese
> Verfassung sagt, wer stimmberechtigt ist und wie hoch die Schwelle liegt. Der Genesis ist
> Epoche 1.
>
> **Es gibt genau einen Loop.** Vorschlag, Stimme, Auszählung, Materialisierung. `§6` und `§7`
> sind Belegungen seiner Parameter, keine eigenen Verfahren.

Was diese Schicht **nicht** tut, steht in `08 §3`: sie verteilt keine Macht. Schwellen,
Mitgliederkreis, Amtsdauern und Losverfahren sind Verfassungsinhalt eines konkreten Nukleus, nicht
Protokoll.

---

## 1. Objekte und Epochen

### 1.1 Die drei Objekte

**Genesis (unveränderlich).** Definiert `N` als stabilen Scope, die Wurzelschlüssel, das initiale
Ankerset, den Hash der initialen Verfassung, die Änderungsklasse, den Gewichtungsmodus und den
Stimmmodus (`00 §4`). Der Genesis ändert sich nie; wer ihn ändern will, gründet einen anderen
Nukleus.

**Verfassung (versioniert).** Die inhaltlichen Regeln, content-adressiert. Sie trägt in dieser
Schicht zwei zusätzliche Felder gegenüber `00 §5`:

| Feld | Typ | Pflicht | Bedeutung |
|---|---|---|---|
| `participants` | array of bstr (32 B), sortiert, duplikatfrei | optional | Die stimmberechtigte Menge `P` der Epoche |
| `thresholds` | map text zu `[num, den]` | Pflicht | Schwellen je Klasse, exakte Integer |

`participants` ist **optional**, damit das kanonische Beispiel aus `00 §3.1` es weglässt und `N`
byte-identisch bleibt. Ein Nukleus ohne deklariertes `participants` ist nicht auszählbar (`§3.5`).

`P` wird **deklariert, nie abgeleitet.** Eine aus dem Bestand abgeleitete Menge wäre unter
Teilwissen unter-bekannt; ein zu kleiner Nenner macht jede Schwelle leichter erreichbar, und das
ist die Über-Ratifizierungsrichtung (D96).

**`irrevocable_predicates` MUSS `vote@1` und `ratify@1` enthalten.** Ohne den ersten greifen Widerruf und
Supersede nach `01 §5.4` auch auf Stimmen, die Stimmenmenge schrumpft, und die Auszählung ist
nicht mehr monoton — womit D96, D101 und D102 zugleich fallen. Ohne den zweiten kann eine bereits
etablierte Epoche wieder verschwinden, weil ihr einziger Beleg widerrufbar bleibt (D107). Ein
Nukleus ohne beide Deklarationen ist nicht auszählbar (`§3.5`).

**`propose@1` ist ausdrücklich nicht geschützt und wird nicht geprüft.** Eine Stimme zeigt auf den
`proposal_hash`, nie auf den `propose@1`-Claim; dieser dient allein der Auffindbarkeit. Sein
Zustand hat auf keine Auszählung Einfluss, und eine Aktivitätsprüfung auf ihn wäre ein Fehler.

Die Unwiderruflichkeit wird damit **nicht in dieser Schicht definiert**, sondern über den bereits
bestehenden Schutz aus D70/D72 erreicht. Es gibt keine zweite Lesart von „aktiv" neben
`classify()` und `classify_all()`; die Drift, gegen die `T-02.4` gebaut wurde, entsteht hier nicht.

Die Aufnahme von `vote@1` widerspricht D58 nicht. Die Negativliste dort nennt `vouch@1`, und das
Kriterium lautet, ob Fortbestehen die konservative Lesart ist. Eine Stimme gewährt keine
fortdauernde Autorität; sie ist ein einmaliger Akt an einem einzelnen Objekt (D97).

**Epoche (abgeleitet).** Kein Objekt, sondern eine Identität:

```
DOM_NUC_EPOCH = "claim-atom/v1/nucleus-epoch"

epoch_id = SHA-256( DOM_NUC_EPOCH || cbor_deterministic([N, i, constitution_hash]) )
```

`i` ist die Epochennummer, beginnend bei 1. Epoche 1 ist der Genesis:

```
epoch_id_1 = SHA-256( DOM_NUC_EPOCH || cbor_deterministic([N, 1, genesis[4]]) )
```

Die Identität hasht das **Ergebnis**, nie den Beleg (D99). Zwei Mitglieder, die dieselbe
Entscheidung unabhängig materialisieren, erzeugen damit zwei Claims über **dieselbe** Epoche und
keinen Widerspruch.

### 1.2 Was eine Epoche festlegt

Für die Dauer einer Epoche stehen fest: `P`, alle Schwellen, `irrevocable_predicates`, die
Arbitratorenliste — der gesamte Verfassungsinhalt. Eine Auszählung in Epoche `i` rechnet
ausschließlich gegen die Verfassung von `i`.

**Getragene Grenze.** Wer nach der Ratifizierung einer Epoche aufgenommen wird, stimmt erst in der
folgenden Epoche mit. Die Epochenverfassung ist ein Stand, kein Livewert.

---

## 2. Profile

Drei Prädikate. Alle drei sind `nuc:`-gescoped und tragen `N` als Pflichtfeld.

### 2.1 `nuc:N/propose@1`

| Feld | Belegung |
|---|---|
| `I` | ein Element von `P` der laufenden Epoche |
| `N` | `N` des Nukleus |
| `J` | `[object-hash, proposal_hash]` (Tag 3) |
| `v` | leer |

Führt einen Vorschlag ein. Erzeugt für sich keinen Zustand und verdrängt nichts.

### 2.2 `nuc:N/vote@1`

| Feld | Belegung |
|---|---|
| `I` | ein Element von `P` der laufenden Epoche |
| `N` | `N` des Nukleus |
| `J` | `[object-hash, proposal_hash]` (Tag 3) |
| `v` | `{0: choice}` |

`v` Key `0` ist **typ-normativ**: `choice` ist ein `uint`, `0` bedeutet Nein, `1` bedeutet Ja.
Andere Werte sind unbekannt und zählen weder als Ja noch als Nein; sie erzeugen den Vermerk
`UNKNOWN_VOTE_CHOICE`. Weitere Keys sind für spätere Durchgänge reserviert und werden ignoriert.

Es gibt **keinen dritten Wert** für Enthaltung. Wer sich nicht äußert, gibt keine Stimme ab; das
ist von einer Nein-Stimme in der Wirkung nicht unterschieden (`§3.2`), aber in der Diagnose (D94).

### 2.3 `nuc:N/ratify@1`

| Feld | Belegung |
|---|---|
| `I` | ein Element von `P` der laufenden Epoche |
| `N` | `N` des Nukleus |
| `J` | `[object-hash, proposal_hash]` (Tag 3) |
| `v` | `{0: [claim_id, ...]}` — die zählenden Ja-Stimmen |

Materialisiert eine gesättigte Entscheidung (`§4`). Die Zeugenmenge in `v` Key `0` ist ein
**austauschbarer Beleg**, kein Teil der Epochenidentität.

### 2.4 Das Vorschlagsobjekt

Content-adressiert, kein Claim:

```
DOM_NUC_PROPOSAL = "claim-atom/v1/nucleus-proposal"

proposal = {
  0 scope             : N
  1 predecessor       : epoch_id der Vorepoche
  2 constitution_hash : SHA-256(cbor_deterministic(constitution_neu))
}

proposal_hash = SHA-256( DOM_NUC_PROPOSAL || cbor_deterministic(proposal) )
```

Ein Vorschlag ist damit eine **vollständige Verfassungsversion**, nicht eine einzelne
Regeländerung. Das Verfassungsobjekt selbst reist neben dem Vorschlag; wer es nicht hat, kann den
Vorschlag nicht bewerten (`§3.5`).

Der eigene Domänen-Separator verhindert, dass ein `proposal_hash` je mit einem
`constitution_hash`, einer `claim_id` oder einem `epoch_id` kollidiert.

---

## 3. Der Kern-Loop

### 3.1 Welche Stimmen zählen

Eine `vote@1`-Stimme zählt für einen Vorschlag genau dann, wenn alle Bedingungen gelten:

1. `vote.N == scope`
2. `vote.J == (3, proposal_hash)`
3. `vote.I` ist Element von `P` — sonst Vermerk `NON_MEMBER_VOTE`
4. `vote.t_exp` ist nicht gesetzt — sonst Vermerk `VOTE_WITH_EXPIRY`
5. `vote.v[0]` ist `0` oder `1` — sonst Vermerk `UNKNOWN_VOTE_CHOICE`
6. Der Claim ist `ACTIVE` nach `classify_all` unter der scope-lokalen Policy (D91). Weil
   `vote@1` nach `§2.1` geschützt ist, führen Widerruf und Supersede hier nie aus `ACTIVE`
   heraus; die Bedingung schließt damit fehlenden Vorgänger, Equivocation und Ablauf aus, nicht
   den Widerruf.

Die Formprüfungen 4 und 5 stehen **vor** der Zustandsprüfung 6. Wirkung identisch, Diagnose
besser: eine abgelaufene Stimme mit gesetztem `t_exp` bekommt so `VOTE_WITH_EXPIRY`, statt lautlos
zu verschwinden (D94, D110).

Zu Bedingung 4: eine Stimme mit Ablaufdatum wäre eine Stimme, die durch Zeitablauf aus der Menge
verschwindet, und genau das darf nicht sein (D97). Sie wird deshalb **ungültig**, nicht still
umgedeutet. Ein Feld, dessen Wert wortlos ignoriert wird, ist die Stummheit, die D95 gekostet hat.

Die Zugehörigkeit des Vorschlags zur Epoche ist **keine Stimmbedingung**, sondern eine Eigenschaft
des Paares aus Epoche und Vorschlag. Sie wird einmal vorweg geprüft (`§3.5`), nicht je Stimme.

Der Ablauf aus Bedingung 5 bleibt trotzdem erreichbar, wenn ein Nukleus `t_exp` über eine
Policy-Maximallaufzeit erzwingt (`02 §6.2`). Ein solcher Nukleus kann keine Stimmen führen; das
ist eine Verfassungsfrage und keine Protokollfrage.

**Zwei aktive Stimmen desselben Autors auf denselben Vorschlag zählen nicht** — weder die eine
noch die andere. Vermerk `AMBIGUOUS_VOTE`, Subjekt sind beide `claim_id`. Die Parallele ist
`02 §2`: trägt kein Gruppenmitglied eine gültige Belegung, entsteht keine Kante.

> **Abgrenzung zu `03`, ausdrücklich.** `membership()` löst mehrere aktive `accept-rules` mit
> `min(claim_id)` auf. Das ist dort richtig, weil alle dasselbe sagen. Zwei Stimmen sagen
> Verschiedenes. Wer das Muster aus `03` überträgt, erzeugt ein Ergebnis aus einer Aussage, die
> niemand gemacht hat (D101).

### 3.2 Die Auszählung

Sei `n = |P|`, sei `[num, den]` die anzuwendende Schwelle (`§3.4`), seien `Ja` und `Nein` die
Mengen der zählenden Stimmen je Wahl. Alles exakte Integer, keine Division:

```
durchgekommen:   |Ja| * den        >   num * n
gescheitert:     (n - |Nein|) * den   <=   num * n
```

Der Nenner ist `n`, nie `|Ja| + |Nein|`. Wer nicht abstimmt, senkt den Nenner nicht;
Nichtteilnahme wirkt wie Ablehnung. Die Schwelle gilt gegenüber den **Berechtigten**, nicht
gegenüber den Erschienenen.

Beide Mengen wachsen nur (D97), beide Bedingungen sind einmal wahr für immer wahr, und sie
schließen einander aus. Ein Vorschlag scheitert daran, dass genug Berechtigte ihn ausdrücklich
ablehnen — nicht daran, dass eine Frist abgelaufen ist.

### 3.3 Zustände

| Zustand | Bedingung |
|---|---|
| `PASSED` | `durchgekommen` |
| `FAILED` | `gescheitert` |
| `PENDING` | weder noch |
| `UNEVALUABLE` | die Auszählung kann nicht laufen (`§3.5`) |

`PASSED` und `FAILED` sind absorbierend. `PENDING` ist die Voreinstellung und bedeutet, dass
weiteres Wissen das Ergebnis noch drehen kann.

Es gibt **kein Zeitfenster und keinen Abschluss**. Eine Abstimmung wird geschlossen, indem eine
Entscheidung materialisiert wird und damit die Epoche wechselt (`§4.3`), nicht indem ein Datum
vergeht. Die Begründung steht in D100: ein Stichtag verlangt Einigkeit darüber, welche Stimmen
davor abgegeben wurden, und die gibt es zwischen zwei Autoren nicht (`01 §5.3`).

### 3.4 Welche Schwelle gilt

Die Klasse wird aus dem **Unterschied** zwischen alter und neuer Verfassung abgeleitet, nicht vom
Vorschlagenden gewählt:

| Unterschied | Klasse |
|---|---|
| ausschließlich `participants` | `membership` |
| alles andere | `amendment` (Index aus `genesis[5]`) |

Die Klasse `ordinary` ist in v1 unbenutzt und für nicht-verfassungsbezogene Entscheidungen
reserviert; die Protokollschicht kennt keine.

**Die Reihenfolge der Klassen ist normativ** und bindet `genesis[5]` an einen Namen in
`thresholds`:

| Index | Klasse |
|---|---|
| `0` | `ordinary` |
| `1` | `membership` |
| `2` | `amendment` |

Fehlt der benannte Schlüssel in `thresholds`, ist der Vorschlag nicht auszählbar (`§3.5`). Ein
Index über `2` ist ebenfalls nicht auszählbar; er wird nicht auf `amendment` zurückgeführt.

**Selbstbezügliche Sperre.** Ändert ein Vorschlag die Schwelle der Klasse, die er selbst aufruft,
gilt das **Maximum** aus alter und neuer Schwelle:

```
angewandt = max( thresholds_alt[klasse], thresholds_neu[klasse] )

Vergleich zweier Ratios exakt:   num_a * den_n   gegen   num_n * den_a
```

Anheben verlangt damit die neue, höhere Schwelle; Senken verlangt die alte, höhere. Eine Fraktion
kann die Hürde nicht unter dem Niveau nehmen, das sie ohnehin überschreiten müsste. Das ist die
h-Regel für den binären Fall.

**Damit ist die Änderungsregel änderbar und trotzdem nicht kaperbar.** Der Satz aus der Vorfassung
— die Änderungsregel sei in v1 unveränderlich, wer sie ändern wolle, forke — entfällt.

### 3.5 Wann die Auszählung nicht läuft

`UNEVALUABLE`, jeweils mit Vermerk, in dieser Reihenfolge geprüft. Die Reihenfolge ist normativ:
sonst erzeugt dieselbe Lage je nach Umsetzung verschiedene Diagnosen.

**Ganz vorweg — die Scope-Zugehörigkeit.** Weicht `proposal.scope` von `epoch.scope` ab, ist das
ein **`ValueError`**, kein Vermerk: ein Vorschlagsobjekt eines fremden Nukleus ist ein
Aufruferfehler und keine Lage der Welt (D82, D92, D112). Dasselbe gilt in `§4.1`.

`Proposal` behauptet mit drei Feldern eine Zugehörigkeit, und alle drei werden geprüft: `scope`
gegen `epoch.scope`, `predecessor` gegen `epoch.epoch_id`, `constitution_hash` gegen das gereichte
Zielobjekt.

**Dann die Paarprüfung.**

| Lage | Vermerk |
|---|---|
| `proposal.predecessor != epoch.epoch_id` | `STALE_EPOCH_VOTE`, Subjekt `proposal_hash` |

Ein nicht zusammengehöriges Paar aus Epoche und Vorschlag ist kein Stimmenproblem, und es darf
nicht davon abhängen, ob überhaupt jemand abgestimmt hat: stünde die Prüfung in der Stimmschleife,
liefe eine Auszählung über ein unpassendes Paar **ohne** Stimmen glatt durch und meldete `PENDING`.

**Dann die Objektidentitäten, vor jedem Zugriff auf ihren Inhalt.**

| Lage | Vermerk |
|---|---|
| Verfassung der Epoche fehlt oder ihr Hash passt nicht zu `epoch.constitution_hash` | `CONSTITUTION_UNAVAILABLE` |
| neues Verfassungsobjekt fehlt oder sein Hash passt nicht zu `proposal.constitution_hash` | `PROPOSAL_CONSTITUTION_UNAVAILABLE` |

**Dann der Inhalt.**

| Lage | Vermerk |
|---|---|
| `participants` nicht deklariert | `PARTICIPANTS_UNDECLARED` |
| `participants` formwidrig: kein Array, leer, Eintrag nicht 32 B, unsortiert, Duplikate | `MALFORMED_PARTICIPANTS` |
| `irrevocable_predicates` führt `vote@1` nicht | `VOTE_REVOCABLE` |
| `irrevocable_predicates` führt `ratify@1` nicht | `RATIFY_REVOCABLE` |
| `genesis[6] != 0` (Gewichtungsmodus nicht Kopfzahl) | `UNSUPPORTED_WEIGHT_MODE` |
| `genesis[5] > 2`, Schwellenklasse fehlt, oder Schwelle nicht wohlgeformt | `MALFORMED_THRESHOLD` |

**Eine leere `participants`-Liste ist formwidrig.** Sie ist sortiert und duplikatfrei und käme
sonst durch; mit `n = 0` wäre jeder Vorschlag sofort `FAILED`, und die Diagnose sagte „abgelehnt",
wo „niemand konnte abstimmen" gemeint ist.

**Wohlgeformtheit einer Schwelle** (D108). Sei `[num, den]` die Schwelle der **angewandten**
Klasse, in beiden Verfassungen geprüft:

```
den >= 1     0 <= num <= den     2 * num >= den
```

Geprüft wird auf den **Rohwerten** beider Verfassungen, bevor irgendeine Umwandlung stattfindet.
Eine Schwelle mit Textwerten muss `MALFORMED_THRESHOLD` ergeben und darf den Aufruf nicht
abreißen (D112).

Die Klasse wird für diese Prüfung gebraucht und **einmal** bestimmt, vor der Validierung. Die
Ableitung der Klasse und die Ermittlung der angewandten Schwelle sind zwei getrennte Schritte;
keiner von beiden wird wiederholt (D113).

Die letzte Bedingung ist die tragende. Seien `A` und `B` disjunkte Ja-Mengen, die beide
durchkommen; dann gilt `|A| * den > num * n` und `|B| * den > num * n`, und mit `|A| + |B| <= n`:

```
n * den   >=   (|A| + |B|) * den   >   2 * num * n        ->        den > 2 * num
```

Zwei disjunkte Ja-Mengen sind also genau dann unmöglich, wenn `2 * num >= den`. Die Grenze ist
nicht strikt — `[1,2]` bleibt zulässig, `[1,3]` nicht. Ohne diese Bedingung fällt D102: zwei
rivalisierende Nachfolger derselben Epoche könnten beide durchkommen, ohne dass jemand doppelt
gestimmt hat.

Die übrigen Bedingungen sind nicht bloß Hygiene: bei `num < 0` vergleicht `reached(0, n, num, den)`
den Ausdruck `0 > num * n` und ist **wahr** — ein Vorschlag wäre `PASSED`, ohne dass eine einzige
Stimme abgegeben wurde.

Geprüft wird ausschließlich die **angewandte** Klasse, nie der gesamte `thresholds`-Eintrag: eine
Verfassung soll nicht daran scheitern, dass ein in v1 unbenutzter Eintrag unglücklich gesetzt ist.

`UNEVALUABLE` ist **nie** `PASSED`. Kein Teilwissen führt zu einer Ratifizierung.

Zur letzten Zeile: `00 §4` Key 6 lässt `weight_mode = 1` weiterhin zu, aber v1 wertet es nicht
aus (D98). Ein Nukleus, der es setzt, bekommt kein Ergebnis statt eines falschen.

---

## 4. Materialisierung und Epochenwechsel

### 4.1 Prüfung eines `ratify@1`

Ein `ratify@1`-Claim etabliert die Folgeepoche genau dann, wenn:

0. `proposal.scope == epoch.scope`, sonst **`ValueError`** (D112). Die Auszählung gehört zu
   **dieser** Epoche und **diesem** Vorschlag. Weicht `tally.epoch_id`
   von `epoch.epoch_id` oder `tally.proposal_hash` von `proposal.proposal_hash` ab, ist das ein
   **`ValueError`**, kein Vermerk: ein fehlzugeordnetes Objekt ist ein Aufruferfehler und keine
   Lage der Welt (D82, D92, D109). Ist `tally.state` gleich `UNEVALUABLE`, entsteht keine Epoche;
   Vermerk `TALLY_UNEVALUABLE` — „ich konnte nicht auswerten", nicht „die Behauptung stimmt nicht".
1. `ratify.N == scope`, `ratify.J == (3, proposal_hash)`, `ratify.I` ist Element von `P`
2. der Claim ist `ACTIVE`
3. jede `claim_id` in `v[0]` bezeichnet eine Stimme, die nach `§3.1` zählt, mit `choice == 1`
4. keine zwei bezeichnen Stimmen desselben Autors
5. die Anzahl überschreitet die Schwelle nach `§3.2` und `§3.4`

Trifft eine Bedingung nicht zu, etabliert der Claim keine Epoche. Er ist deshalb kein Angriff und
kein Protokollverstoß, sondern eine Behauptung, die sich nicht bestätigt.

Zwei Vermerke, weil die Diagnose verschieden ist (D94, D106):

| Lage | Vermerk |
|---|---|
| eine zitierte `claim_id` ist lokal nicht vorhanden | `UNKNOWN_WITNESS_VOTE` |
| alles Übrige — der Claim ist da und trägt nicht | `UNSUPPORTED_RATIFICATION` |

Die Wirkung ist in beiden Fällen dieselbe: keine Epoche. Im ersten Fall weiß der Beobachter, welche
`claim_id` er holen muss; im zweiten weiß er, dass Holen nichts nützt.

Die Prüfung ist **offline und vollständig lokal**: wer den Vorschlag, das neue Verfassungsobjekt
und die zitierten Stimmen hat, rechnet das Ergebnis nach, ohne jemanden zu fragen und ohne eine
Uhr zu lesen.

### 4.2 Die Folgeepoche

```
i_neu             = i + 1
constitution_neu  = das Objekt zu proposal[2]
epoch_id_neu      = SHA-256( DOM_NUC_EPOCH || cbor_deterministic([N, i_neu, proposal[2]]) )
```

Zwei `ratify@1`-Claims für denselben Vorschlag ergeben denselben `epoch_id_neu`. Sie sind zwei
Belege für dieselbe Tatsache.

### 4.3 Was der Wechsel erledigt

Mit der Etablierung von `i+1` sind alle Stimmen und alle Vorschläge, deren `predecessor` auf `i`
zeigt, gegenstandslos. Ein Vorschlag, der in `i` nicht durchkam, muss in `i+1` neu eingebracht
werden und behauptet sich dort gegen den geänderten Status quo.

### 4.4 Höchstens ein Ja je Mitglied je Epoche

Ein Mitglied darf in einer Epoche höchstens einen Vorschlag mit `choice == 1` bedenken. Zwei
aktive Ja-Stimmen desselben Autors auf **verschiedene** Vorschläge derselben Epoche zählen beide
nicht; Vermerk `CONFLICTING_APPROVAL`, Subjekt sind alle beteiligten `claim_id`.

Nein-Stimmen sind unbeschränkt. Gegen mehrere Vorschläge gleichzeitig zu sein ist kohärent; zwei
verschiedene Dokumente gleichzeitig als das geltende zu benennen ist es nicht.

**Diese Regel ist sicherheitstragend, nicht ordnungspolitisch.** Aus ihr folgt, dass zwei
rivalisierende Nachfolger derselben Epoche arithmetisch unmöglich sind: bei einer Schwelle über
der Hälfte müssten sich ihre Ja-Mengen überschneiden. Ohne sie entstünde genau das Split Brain,
das Raft bei nebenläufigen Konfigurationswechseln beschreibt (D102).

Niemand muss Nein zu A sagen, um Ja zu B sagen zu können, und ein Ja zu A wird B **nicht** als
Nein angerechnet.

**Wenn die Epoche einer fremden Ja-Stimme nicht auflösbar ist.** Die Zugehörigkeit eines
Vorschlags zu einer Epoche steht in `proposal[1]`; ist das Vorschlagsobjekt lokal unbekannt, kann
sie nicht bestimmt werden. Eine aktive Ja-Stimme auf einen unbekannten Vorschlag gilt dann als
**möglicherweise epochengleich** und blockiert die andere Ja-Stimme desselben Autors; Vermerk
`UNKNOWN_PROPOSAL`, Subjekt die `claim_id` der unauflösbaren Stimme.

Die Richtung ist erzwungen, nicht gewählt: die Gegenannahme lässt bei Teilwissen zwei Nachfolger
derselben Epoche entstehen, und das ist die Über-Ratifizierungsrichtung. Geheilt wird der Fall,
indem jemand das Vorschlagsobjekt nachreicht — es ist content-adressiert und damit nicht
fälschbar (D103).

---

## 5. Der Nukleus-Akt

Ein Nukleus-Akt ist eine Handlung, die dem Nukleus selbst zugerechnet wird und nicht einem
Menschen. `00 §7` zählt sie auf: `grant-membership@1`, das Verdikt eines Panels, die
Föderationsstimme, die Ratifizierung, `rotate-key@1`.

Es gibt **zwei Pfade**, und `00 §4` Key 7 wählt zwischen ihnen. Beide Pfade waren bisher an drei
Stellen verschieden formuliert; die folgende Zuordnung ist die normative:

| `vote_mode` | Pfad | Autorisierung | Normiert in |
|---|---|---|---|
| `0` | Epochenpfad | die Verfassung der Epoche trägt die Wirkung; jedes Mitglied darf materialisieren | `04 §4` |
| `1` | Schlüsselpfad | `akt.I` ist Element von `resolve_current_key(akt.N)` | `00 §7`, umgesetzt in `03 §4` |

`03 §4` implementiert damit den **Schlüsselpfad**: sein Parameter `authorized_keys` ist die Menge
aus `resolve_current_key`. Das war nie ausgeschrieben und ist der Grund, aus dem `03 §5` eine
Lücke melden musste.

`resolve_current_key` selbst bleibt vertagt (`00a-rotate-key`, D62).

---

## 6. Mitgliedschaft

### 6.1 Im Epochenpfad

Mitgliedschaft ist weiterhin die Konjunktion aus fremder Aufnahme und eigener Annahme (D60). Nur
die Herkunft der Aufnahme ändert sich: sie ist kein Claim, sondern ein Eintrag im
Verfassungsobjekt, das der `constitution_hash` adressiert.

```
MEMBER  gdw.  subject ist Element von constitution.participants
        und   eine aktive accept-rules@1 des subject auf genau diesen constitution_hash
```

Beide Konjunkte zeigen damit auf **dasselbe** content-adressierte Objekt. Die vier Zustände aus
`03 §4` bleiben unverändert: fehlt die Annahme, ist der Zustand `GRANT_ONLY`; fehlt die Aufnahme,
`APPLICANT`.

Die eigene Annahme ist keine Formalie. Sie verhindert, dass eine Mehrheit jemandem eine
Mitgliedschaft samt Pflichten zuschreibt, die er nicht eingegangen ist.

### 6.2 Anschluss an `03`

`membership()` bekommt einen zusätzlichen optionalen Parameter:

```
constitution_obj: dict | None = None
```

Ist er gesetzt, prüft die Funktion zuerst `constitution_hash(constitution_obj)` gegen den bereits
vorhandenen Parameter `constitution_hash` und wirft bei Abweichung `ValueError` (D111). Danach
gilt `subject in constitution_obj["participants"]` als zweite Aufnahmequelle neben einer aktiven
`grant-membership@1`. Die `accept-rules`-Strecke bleibt unverändert.

Die Teilnehmerliste wird **nicht** getrennt gereicht. Beide Konjunkte der Mitgliedschaft zeigen so
auf dasselbe content-adressierte Objekt; eine Liste aus einer anderen Epoche kann nicht mit dem
Hash dieser verbunden werden.

Kein neues Prädikat, kein neuer Zustand, keine zweite Mitgliedschaftsfunktion. Zwei Funktionen,
die dasselbe tun, waren die Fehlerform der `03`-Abnahme (D92).

### 6.3 Aufnahme als Verfassungsänderung

Eine Aufnahme ist damit ein Vorschlag, dessen neue Verfassung sich von der alten ausschließlich in
`participants` unterscheidet — Klasse `membership` nach `§3.4`. Es gibt in v1 kein eigenes
Aufnahmeverfahren.

---

## 7. Verfassungsänderung und Föderation als Belegungen

### 7.1 Verfassungsänderung

Der Loop aus `§3` mit Klasse `amendment` und der selbstbezüglichen Sperre aus `§3.4`. Kein eigener
Mechanismus, keine eigene Prosa. Die Ratifizierung ist `ratify@1`; die Re-Akzeptanz der Mitglieder
ist ihre `accept-rules@1` auf den neuen Hash und entscheidet über ihre eigene Mitgliedschaft in
der Folgeepoche (`§6.1`), nicht über das Zustandekommen der Änderung.

### 7.2 Föderation

Eine Föderation ist ein Nukleus, dessen Mitglieder Nuklei sind: eigener Genesis `N_fed`, eigene,
kleinere Verfassung, derselbe Loop.

Ein Nukleus ist allerdings **kein Graphknoten** — Knoten sind Ed25519-Schlüssel (`02 §2`), ein
Nukleus ist ein Genesis-Hash. Für eine Kopfzahl-Auszählung ist das gleichgültig: `participants`
einer Föderationsverfassung enthält die aktuellen Schlüssel der konstituierenden Nuklei, und deren
Stimme entsteht bei jedem von ihnen über `§5`.

**Der Appeal-Pfad ist Opt-in, nicht eingebaut.** Ein Verdikt aus dem Föderations-Scope ist im
Kind-Scope scope-fremd und bindet dort nicht (D81, D92). Es bindet genau dann, wenn die Verfassung
des Kindes das Föderationspanel in `arbitration.arbitrators` führt. Das ist die freiwillige Form
und die einzige, die mit `03` ausdrückbar ist. Die Vorfassung behauptete einen eingebauten Pfad;
das war nicht einlösbar.

Alles Weitere zur Föderation — Losverfahren für Versammlungen, Repräsentationsfairness, Rechtsweg
über mehrere Ebenen — ist Verfassungsinhalt nach `08 §3` und nicht Gegenstand dieser Schicht.

---

## 8. Bewusst getragene Grenzen

- **Ein Vorschlag ist ein Bündel.** Wer nur die Arbitratorenliste ändern will, reicht eine
  vollständige Verfassungsversion ein. Der feinere Weg — Änderungen je Feld mit unabhängiger
  Geltung — bringt Parallelität, erlaubt aber die Teilannahme eines Pakets und braucht eine
  Zerlegung, die niemand gerechnet hat. Grob gebündelt und fein zerlegt sind beide sicher;
  gefährlich ist das Mischen (D101).

- **Vorschläge scheitern oder kommen durch; sie laufen nicht ab.** In einer Epoche, in der nichts
  durchgeht, hängt ein Vorschlag unbegrenzt. Eine Entscheidung bildet damit gesetzte Zustimmung ab
  und nicht, wer an einem bestimmten Tag besser mobilisiert hat.

- **Eine hohe Schwelle bei lauer Beteiligung macht die Verfassung faktisch unveränderlich.** Der
  Nenner ist `|P|`, nicht die Zahl der Abstimmenden. Die Schwelle ist gegen realistische
  Beteiligung zu wählen; das gehört in `example-nucleus.md`, nicht ins Protokoll.

- **Eine Stimme lässt sich nicht zurücknehmen.** Ohne Frist gibt es kein Fenster, nach dem es
  gleichgültig wäre; ohne Unwiderruflichkeit gibt es keine Monotonie (D97). Wer seine Meinung
  ändert, hilft dem einmal bedachten Vorschlag weiter — und nur ihm.

- **Agenda-Macht bleibt, ist aber klein.** Der Vorschlagende wählt den Inhalt. Er wählt weder die
  Wählerschaft noch einen Kantenschnitt noch einen Zweckkontext; all das ist mit dem Snapshot
  entfallen (D96). Wer vorschlagen darf, begrenzt die Verfassung, nicht das Protokoll.

- **Ein zurückgehaltenes Vorschlagsobjekt kann ein Mitglied vorübergehend aussetzen.** Wer eine
  Ja-Stimme auf einen Vorschlag abgibt, dessen Objekt nie verbreitet wird, zählt in dieser Epoche
  nirgends mit (`§4.4`). Das ist die sichere Richtung und heilt, sobald jemand das Objekt
  nachreicht; verhindern kann das Mitglied es nicht.

- **Kein Rechtsweg gegen die eigene Mehrheit.** Wer in `P` überstimmt wird, hat innerhalb des
  Nukleus keine Instanz über sich. Das Ventil ist Austritt und, wenn die Verfassung es vorsieht,
  das Föderationspanel (`§7.2`).

- **Vertagt und ausdrücklich nicht in v1:** gewichtete Auszählung (D98), Zweck-Tag am Vouch
  (D56, `02d`), `resolve_current_key` (D62), Kettenbindung von Ämtern nach VR-04.1 (D26), das
  Zeugenquorum für Fristen (D100).
