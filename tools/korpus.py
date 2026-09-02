#!/usr/bin/env python3
"""Saatkorpus: Namen und Drahtbytes aus der committeten Vektordatei (D293, D295)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

_VECTORS = Path(__file__).resolve().parent.parent / "tests" / "vectors" / "vectors_01.json"


def seed_lines() -> list[tuple[str, str]]:
    """Paare aus Name und Drahtbytes in Hex, Reihenfolge der Vektordatei (D293)."""
    data = json.loads(_VECTORS.read_text())
    pairs: list[tuple[str, str]] = []
    for entry in data["vectors"]:
        if "wire_bytes" in entry:
            wire_hex = entry["wire_bytes"]
        elif "signed_bytes" in entry:
            wire_hex = entry["signed_bytes"]
        else:
            raise ValueError(entry["name"])
        pairs.append((entry["name"], wire_hex))
    return pairs


def main() -> None:
    pairs = seed_lines()
    if "--manifest" in sys.argv[1:]:
        for name, _wire_hex in pairs:
            print(name)
        return
    for _name, wire_hex in pairs:
        print(wire_hex)


if __name__ == "__main__":
    main()
