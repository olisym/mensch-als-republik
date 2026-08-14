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

Zwei Claims mit gleichem `h_prev` erzeugt `fork: true` in `Teilnehmer.claim_signieren` —
die Autorenkette wird nicht fortgeschrieben.
