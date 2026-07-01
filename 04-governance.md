# Governance-Schicht — Spezifikation v1

Status: Entwurf · Protokollversion: 1 · Layer: Governance (über Trust-Flow & Profile)

Diese Schicht macht aus Regelannahmen (Profil `accept-rules@1`) plus Trust-Flow die
**Konsens-Stufe 1** eines Nukleus und die Föderation darüber. Der zentrale Satz:

> **Der Nukleus ist ein rekursives Primitiv.** Mensch → Nukleus → Föderation ist dreimal
> dieselbe Struktur. Und: **Governance = Vorschlag + Abstimmung + Auszählung.** Eine
> Verfassungsänderung ist nur der Spezialfall mit der höchsten Schwelle.

Kein neues Atom-Feld. Vorschläge und Verfassungen sind **content-adressierte Objekte** (wie
schon die Verfassung in Profil 7.2), auf die Claims zeigen; die Stimmen sind die Claims.

---

## 1. Nukleus-Objekte

Zwei Objekte, getrennt nach Lebensdauer:

**Genesis (unveränderlich).** Definiert:
- `N` = Hash des Genesis-Objekts = der **stabile Scope** (für immer, auch wenn sich Regeln ändern);
- die Gründungs-Charta und das **initiale Ankerset** (der Nukleus-Seed, §4);
- die **Änderungsregel** (wie die Verfassung geändert werden darf, §5);
- den **Gewichtungsmodus** (Kopfzahl **oder** zweck-gescopt gewichtet — hier: gewichtet, §4);
- den **Stimmmodus** (Komposition-Default **oder** FROST-Opt-in, §3).

**Verfassung (versioniert).** Die aktuellen inhaltlichen Regeln, content-adressiert, geändert
per Supersede über den Governance-Prozess. `accept-rules@1` zeigt auf die *aktuelle Version*
(Re-Akzeptanz bei Änderung). Mitgliedschaft und Trust bleiben auf `N` = Genesis-Hash gescoped,
der **stabil bleibt** — die Regeln wandeln sich, ohne dass der Nukleus seine Identität verliert.

---

## 2. Vorschlag · Stimme · Auszählung (der Kern-Loop)

| Profil | Belegung |
|--------|----------|
| `nuc:N/propose@1` | `I` = ein Mitglied; `J = [object-hash, vorschlag_obj]`; führt einen Vorschlag ein. |
| `nuc:N/vote@1`    | `I` = ein Mitglied; `J = [object-hash, vorschlag_obj]`; `v` = Wahl. |

**Vorschlags-Objekt** (content-adressiert, kein Claim) enthält: die Entscheidung/Änderung,
den **Zweck-Kontext `π`** für die Gewichtung, die **Snapshot-Bindung** (§4.2) und die
**Schwellenklasse**, die er aufruft.

**Schwellenklassen** (Policy, in der Verfassung deklariert): z. B. gewöhnliche Entscheidung,
Mitgliedschaft, Verfassungsänderung — jede mit eigenem Quorum. Änderung = höchste Klasse.

---

## 3. Die Stimme des Nukleus

Ein **Nukleus-Akt** (`grant-membership@1`, `verdict@1`, Föderationsstimme, Ratifizierung) ist
gültig gdw.:

- **(Komposition, Default)** eine Menge aktiver `vote@1`/`accept-rules@1`-Claims für den Akt
  die deklarierte Schwelle unter der kanonischen gewichteten Auszählung (§4) überschreitet —
  jeder Verifizierer tallyt selbst, maximal lokal, keine in Krypto gegossene Autorität; **oder**
- **(FROST, Opt-in)** der Akt **eine** Gruppensignatur unter dem Nukleus-Schlüssel trägt —
  billiger zu prüfen, Preis: Re-Keying bei Mitgliederwechsel; die Off-Protocol-Einigung ersetzt
  die On-Protocol-Auszählung.

Das folgt exakt dem Flow/PageRank-Metamuster: Komposition ist Fundament, FROST erlaubte Optimierung.

---

## 4. Zweck-gescopte gewichtete Auszählung

### 4.1 Gewicht

Für einen Vorschlag mit Zweck-Kontext `π`:

```
gewicht(wähler) = trust_flow(nukleus_seed → wähler, im Zweck-π-Graphen)
```

- **Nicht** roher globaler Nukleus-Flow (der misst allgemeines Standing und läuft beim Gründer
  zusammen, egal ob er an der Sache beteiligt war). **Zweck-gescopt:** wer für `π` gevoucht/
  beigetragen hat, wiegt bei `π`-Entscheidungen schwer, bei fremden Themen leicht. Das trifft
  „Expertise + Investment an der konkreten Sache" und entschärft die Gründer-Zementierung.
- **Vom Nukleus-Seed**, nie vom eigenen Seed — man kann sich nicht selbst hochvouchen.
- **Geldblind** (Trust-Flow-Spec §6.1) — gewichtetes ≠ geld-gewichtetes Abstimmen. Keine
  Plutokratie durch die Hintertür.

**Zweischichtiges Tor:** *ob* man abstimmt → Mitgliedschaft (`grant-membership`, Konsens der
Bestehenden; hier sitzt der Sybil-Schutz). *Wie schwer* die Stimme wiegt → zweck-gescopter Flow.

### 4.2 Kanonischer Seed + Snapshot (Determinismus)

Gewichtetes Abstimmen **verlangt** eine kanonische Auszählung, sonst rechnet jeder ein anderes
Gewicht:

- Tallies laufen gegen den **genesis-deklarierten Nukleus-Seed** → alle bekommen denselben
  Startpunkt.
- Der Vorschlag committet sich auf einen **Graph-Snapshot**: eine Merkle-Wurzel über die
  sortierten `claim_id` der in-scope (Zweck-`π`, aktiven) Vouch-Kanten zum Zeitpunkt der
  Vorschlagserstellung. Gewichte werden **gegen diesen eingefrorenen Kantensatz** gerechnet.
- Ergebnis: die Auszählung ist **deterministisch gegeben den Snapshot**. Uneinigkeit reduziert
  sich auf „hast du die Snapshot-Claims" (eventually consistent), nicht auf „rechnen wir gleich".

**Ehrlicher Preis:** gewichtetes Abstimmen ist **partitions-fragiler** als Kopfzahl (die nur die
Stimm-Claims braucht). Der Snapshot fängt das ab; ohne ihn lösen sich divergente Tallies über
dasselbe Fork-und-Exit-Ventil wie ein Verfassungs-Fork (§6) — Backstop, nicht Alltag.

---

## 5. Verfassungsänderung (Spezialfall)

- **Vorschlag** einer neuen Verfassungsversion via `propose@1`.
- **Stimme** = `accept-rules@1` auf den **neuen** Verfassungs-Hash (die Ratifizierung *ist* die
  Re-Akzeptanz — kein separater Mechanismus).
- Überschreitet die gewichtete Ratifizierung die **Amendment-Schwelle** (höchste Klasse), gilt
  die neue Verfassung als angenommen und **supersediert** die alte (Nukleus-Akt §3).
- **Die Änderungsregel selbst ist in v1 unveränderlich.** Wer die Meta-Regeln ändern will,
  **forkt** einen neuen Nukleus und nimmt Mitglieder per Re-Akzeptanz mit. Das ist konsistent mit
  Exit/Fork als ultimativem Ventil und verhindert **Governance-Capture** (eine Fraktion senkt die
  Hürde und übernimmt). Trade-off: weniger Flexibilität, dafür keine Capture-Fläche.

---

## 6. Konstitutioneller Fork (abgeleitet, kein neuer Mechanismus)

Erreichen in einer Partition zwei konkurrierende Amendments je das Quorum, hat der Nukleus über
seine Verfassung **equivociert** — beweisbar wie jede Equivocation (Atom-Spec §4). Auflösung über
dasselbe Detect-und-Exit-Ventil: der Nukleus **spaltet sich**. Konstitutionelle Forks reduzieren
auf Fork-Erkennung + Exit, die wir schon haben.

---

## 7. Föderation & Rechtsweg

**Eine Föderation *ist* ein Nukleus, dessen Mitglieder Nuklei sind.** Dasselbe Primitiv, eine
Ebene höher:

- eigene Genesis `N_fed`, eine **kleinere gemeinsame Verfassung** (nur die Regeln, die die
  Konstituenten gemeinsam halten wollen);
- „Mitglieder" sind Nuklei; jeder stimmt über **seine** Stimme (Komposition/FROST, §3);
- Ratifizierung auf Föderationsebene = die **Nuklei** akzeptieren die gemeinsame Teilmenge, nicht
  die einzelnen Menschen.

Damit fällt der Subsidiaritätsturm heraus — Mensch → Nukleus → Föderation → Föderation-von-
Föderationen, ein rekursives Objekt auf jeder Ebene (Ostroms „nested enterprises").

**Standing & Appeal (Nicht-Monopol-Ventil).** Standing fließt durch den eigenen Nukleus
(Subsidiarität). Aber reine Subsidiarität würde ein Individuum einsperren, dessen eigener Nukleus
der Bad Actor ist. Deshalb **eingebauter Appeal-Pfad nach oben**: ein Mensch kann eine Entscheidung
seines Nukleus auf die Föderationsebene eskalieren, wo **andere** Nuklei urteilen (ein `verdict@1`
im Föderations-Scope). Das ist genau die Antwort auf „privater Schutz ohne Monopol — man muss sich
an jemanden wenden können".

---

## 8. Bewusst getragene Grenzen & Designentscheidungen

- **Snapshot als Merkle-Commitment** über den in-scope Kantensatz ist eine *gewählte* Form
  (deterministisch, prüfbar). Zeit-Cutoffs wären untauglich (Wall-Clock ist über Mesh wertlos,
  Atom-Spec §5.3).
- **Agenda-Setting-Fläche (offen benannt).** Der Vorschlagende stellt Snapshot **und** `π`
  zusammen — das ist Agenda-Macht (welche Kanten/welcher Zweck zählen). Mitigation: der Snapshot
  ist ein **prüfbares** Commitment — Wähler verifizieren Vollständigkeit gegen ihre eigene Sicht
  und **verwerfen** einen gerrymanderten/unvollständigen Vorschlag; die Verfassung kann
  einschränken, wer vorschlägt und wie `π` auf Entscheidungs-Domänen abbildet. **Residual:**
  „Vollständigkeit" ist in einer Partition sicht-relativ. Agenda-Macht ist keine Eigenheit dieses
  Entwurfs, aber sie ist da und wird von der Verfassung begrenzt, nicht vom Protokoll eliminiert.
- **Quantifizierter Einfluss (ehrlicher Preis deiner Wahl).** Es bleibt ein reputationsgewichteter
  Einfluss — aber **lokal, zweck-gescopt, per-Nukleus, nie global**. Kein Mensch wird auf *eine*
  öffentliche Zahl reduziert; es gibt nur kontextuelle Stimmgewichte pro Thema pro Nukleus.
  Größenordnungen milder als ein globaler Social-Score, aber bewusst zu tragen.
- **Gründer-Zementierung reduziert, nicht null.** Die Gründer seeden die Zweck-Graphen anfangs;
  zweck-gebundenes Vertrauen ist aber *pro Domäne verdienbar* und verschiebt sich über Beiträge.
- **Partitions-Fragilität** von gewichtetem vs. Kopfzahl-Abstimmen (§4.2) — akzeptiert, per
  Snapshot abgefedert.
- **FROST-Re-Keying** bei Mitgliederwechsel ist der Preis des Stimmmodus-Opt-ins (§3).
