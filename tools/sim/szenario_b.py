#!/usr/bin/env python3
"""Szenario B: Vertrauensentzug als Durchsetzung (00as, D313).

Wegwerf-Treiber. Ruft run_scenario auf und druckt die Befunde, die der Rahmen
in den zeige-Schritten ausgibt. Keine Golden Numbers.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from tools.sim import run_scenario

_SCENARIO = Path(__file__).resolve().parent / "scenarios" / "szenario-b.json"


def main() -> None:
    raw = _SCENARIO.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "szenario-b.json"
        path.write_text(raw.replace("PLACEHOLDER", tmp), encoding="utf-8")
        print("Szenario B — Vertrauensentzug als Durchsetzung (D313)")
        print()
        run_scenario(path)


if __name__ == "__main__":
    main()
