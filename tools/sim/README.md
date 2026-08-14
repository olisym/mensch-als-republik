# Simulation mit getrennten Beobachtern

Werkzeug unter `tools/sim/` — kein Paketmodul. Mehrere Teilnehmer mit **getrennten Stores,
getrennten Uhren und getrennten Schlüsseln**; alles Rechnende kommt aus `mensch_als_republik`.

## Verzeichnis je Teilnehmer

```
<welt>/<name>/
  key.bin       32-Byte-Seed (Klartext — nur Simulation)
  now           Unix-Sekunden als Text
  h_prev        letzter claim_id-Hex (Autorenkette)
  inbox/*.cbor  Claims, Dateiname = claim_id
```

Nichts synchronisiert von selbst. Zustellung nur über Szenarioschritte `zustellen`. Optional `nur: ["label", …]` kopiert
nur die benannten Claims (S5 Equivocation).

## Szenarien ausführen

```python
from tools.sim import run_scenario

run_scenario("tools/sim/scenarios/s1.json")  # pfad in JSON anpassen
```

Jeder `zeige`-Schritt trägt `erwarte` mit; Abweichung bricht ab.

Tests: `tests/test_sim.py` (alle sechs JSON-Dateien unter `scenarios/`).

## Equivocation (S5)

Zwei Claims mit gleichem `h_prev` erzeugt `kette_fortschreiben: false` in
`Teilnehmer.claim_signieren` — die Autorenkette wird nicht fortgeschrieben. Ob daraus
Equivocation folgt, entscheidet allein `_is_in_equivocation_pair` aus Layer 01.

Anna hält beide eigenen Stimmen von Anfang an und sieht ihre Equivocation deshalb sofort:
`EQUIVOCATION_FLAGGED` für beide, `yes = 1` aus Chris' Stimme. **Der Equivocierende ist der
einzige Beobachter, der von Anfang an die Wahrheit sieht** — die Getäuschten sehen sie erst,
wenn sie einander zustellen. Das ist `08 §2.2`: nicht verhindert, sondern unbestreitbar, und
zwar genau in dem Moment, in dem zwei Betrogene reden.
