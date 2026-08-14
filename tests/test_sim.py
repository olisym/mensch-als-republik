"""Simulation — sechs Szenarien mit getrennten Beobachter-Stores (sim-prompt.md §6)."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from tools.sim import run_scenario

_SCENARIOS = Path(__file__).resolve().parent.parent / "tools" / "sim" / "scenarios"


def _run(name: str) -> None:
    raw = (_SCENARIOS / f"{name}.json").read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / f"{name}.json"
        path.write_text(raw.replace("PLACEHOLDER", tmp), encoding="utf-8")
        run_scenario(path)


@pytest.mark.parametrize("name", ["s1", "s2", "s3", "s4", "s5", "s6"])
def test_scenario(name: str) -> None:
    _run(name)
