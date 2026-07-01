# Mensch als Republik — Protokoll-Spezifikation

Ein **neutrales Substrat** für freiwillige, lokale, föderierte Koordination zwischen Menschen.
Nicht *eine* Gesellschaftsordnung, sondern die Infrastruktur, auf der beliebig viele lokal und
freiwillig nebeneinander bestehen — global gesehen ein **Markt der Gesellschaftssysteme**,
dessen Auswahl über Exit/Fork läuft, nicht über Zwang.

**Status:** Entwurf · **Protokollversion:** 1

---

## Der eine Leitgedanke

> Alles Globale wird vermieden, alles Lokale wird ermächtigt.

Kein globaler Score, kein globaler Konsens, kein globales Gewaltmonopol, keine globale Wahrheit,
kein globaler Preis. Aus dieser einen Entscheidung folgen alle anderen.

## Leitsätze (die Verfassung des Protokolls)

- **A1 — Selbstenthalten.** Ein Claim reist über RNS/LXMF/QR/Papier; Transport ist nie Teil des Objekts.
- **A2 — Lebenszyklus, nicht Bedeutung.** Das Protokoll versteht Gültigkeit, Ordnung und Widerruf —
  nie den sozialen Sinn. **Mechanismus ins Protokoll, Policy nach oben.**
- **A3 — Erkennen statt Verhindern.** Kein globaler Konsens; hash-verkettete Logs, Equivocation
  beweisbar; Uneinigkeit löst sich über Exit/Fork.
- **C1 — Gewalt ist Letztinstanz, nicht Basis.** Fünfstufige Eskalation; physischer Vollzug so
  selten wie möglich.
- **C2 — Physisches nie im Protokoll.** Das Protokoll koordiniert und beweist, Menschen handeln;
  kein Monopol.
- **D1 — Das Oracle-Problem bleibt offen.** Non-Repudiation ja, Wahrheit nie.
- **D2 — Das Seed-Set ist die wertbildende Entscheidung**, kein technisches Detail.
- **Der eine nicht-neutrale Commitment:** Freiwilligkeit und Konsens — Mitgliedschaft ist
  beidseitig, Exit ist real. Ein System, das seine Mitglieder nicht gehen lässt, kann das
  Protokoll nicht sauber abbilden. Das ist Absicht.

## Das Ergebnis in einem Satz

**Nach dem Atom kommt kein einziges neues Feld hinzu.** Jede Schicht ist Komposition oder
Auswertung über dem einen Primitiv — das war die Wette, und sie ist über vier Schichten
aufgegangen.

---

## Der Schichtenstack (Lesereihenfolge)

| # | Datei | Schicht | Kern |
|---|-------|---------|------|
| 01 | [01-claim-atom.md](01-claim-atom.md) | Fundament | Das eine signierte, verkettete Primitiv + erste Profile (Bürgschaft, Regelannahme) |
| 02 | [02-trust-flow.md](02-trust-flow.md) | Vertrauen | Sybil-resistenter Fluss (Min-Cut), lokal geseedet |
| 03 | [03-profiles.md](03-profiles.md) | Soziale Akte | Weitere Profile: Verdikt, Wert/Kredit, Mitgliedschaft |
| 04 | [04-governance.md](04-governance.md) | Konsens & Föderation | Vorschlag + Abstimmung + Auszählung; rekursiver Nukleus |
| 05 | [05-enforcement.md](05-enforcement.md) | Durchsetzung | Fünfstufige, kurierbare Eskalation |

## Bewusst offene Grenzen

Das Oracle-Problem (D1), der physische Vollzug (C2), die Seed-Integrität (D2) — und der
irreduzible Rest: gegen eine hinreichend große fehlgeleitete Koalition hilft kein Protokoll.
Kryptografie koordiniert, beweist, bindet und eskaliert; den Rest tragen Menschen.
