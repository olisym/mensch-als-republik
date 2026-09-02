"""Paarmutanten der Stufe 2 (D305, D306, D289, 01 §B.2)."""

from __future__ import annotations

import sys

import pytest

from mensch_als_republik import cbor_canon
from tools.gitter import mutant_lines as gitter_lines
from tools.korpus import seed_lines
from tools.paare import main, mutant_lines
from tools.verdikt import verdikt_line

_SEED_NAMES = frozenset({"TV1", "TV2", "TV3", "TV4", "TV5", "TV6"})
_SIG_KEY = 9
_UNSUPPORTED = "reject UNSUPPORTED_VERSION"
_MALFORMED = "reject MALFORMED_CBOR"


def _seed_maps() -> dict[str, dict]:
    maps: dict[str, dict] = {}
    for name, wire_hex in seed_lines():
        if name not in _SEED_NAMES:
            continue
        maps[name] = cbor_canon.decode(bytes.fromhex(wire_hex))
    return maps


def _changed_keys(seed: dict, mutant: dict, *, core_only: bool) -> list[int]:
    """Auftrag 3: hinzugekommen, weggefallen oder anders belegt."""
    if core_only:
        seed_f = {k: v for k, v in seed.items() if k != _SIG_KEY}
        mut_f = {k: v for k, v in mutant.items() if k != _SIG_KEY}
    else:
        seed_f = seed
        mut_f = mutant
    out: list[int] = []
    for key in sorted(set(seed_f) | set(mut_f)):
        if key not in seed_f or key not in mut_f:
            out.append(key)
        elif cbor_canon.encode(seed_f[key]) != cbor_canon.encode(mut_f[key]):
            out.append(key)
    return out


def _einzel_etiketten(label: str) -> tuple[str, str]:
    _art, family, seed_name, rest = label.split("/", 3)
    a, b = rest.split("+", 1)
    return f"{family}/{seed_name}/{a}", f"{family}/{seed_name}/{b}"


def test_each_line_differs_from_seed_in_exactly_two_keys() -> None:
    seeds = _seed_maps()
    for label, wire_hex in mutant_lines():
        _art, family, seed_name, _rest = label.split("/", 3)
        decoded = cbor_canon.decode(bytes.fromhex(wire_hex))
        assert isinstance(decoded, dict)
        keys = _changed_keys(seeds[seed_name], decoded, core_only=family == "A")
        assert len(keys) == 2, label


def test_labels_and_bytes_are_pairwise_distinct_and_no_seed() -> None:
    seed_hexes = {wire_hex for name, wire_hex in seed_lines() if name in _SEED_NAMES}
    pairs = mutant_lines()
    labels = [label for label, _hex in pairs]
    wires = [wire_hex for _label, wire_hex in pairs]
    assert len(labels) == len(set(labels))
    assert len(wires) == len(set(wires))
    assert seed_hexes.isdisjoint(wires)


def test_each_class_and_vorrangprobe_has_a_line() -> None:
    labels = [label for label, _hex in mutant_lines()]
    assert any(label.startswith("P1/") for label in labels)
    assert any(label.startswith("P2/") for label in labels)
    assert any(label.startswith("P3/") for label in labels)
    assert any(label.startswith("PV/") for label in labels)


def test_vorrangprobe_verdict_is_derived_from_the_two_singles() -> None:
    singles = {label: wire_hex for label, wire_hex in gitter_lines()}
    for label, wire_hex in mutant_lines():
        if not label.startswith("PV/"):
            continue
        a, b = _einzel_etiketten(label)
        v1 = verdikt_line(singles[a])
        v2 = verdikt_line(singles[b])
        expected = _UNSUPPORTED if v1 == _UNSUPPORTED or v2 == _UNSUPPORTED else _MALFORMED
        assert verdikt_line(wire_hex) == expected, label


def test_manifest_and_hex_match_and_two_calls_agree(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sys, "argv", ["paare.py"])
    main()
    hex_lines = capsys.readouterr().out.splitlines()
    monkeypatch.setattr(sys, "argv", ["paare.py", "--manifest"])
    main()
    label_lines = capsys.readouterr().out.splitlines()
    assert len(label_lines) == len(hex_lines)
    assert mutant_lines() == mutant_lines()
