"""Zeilenschnittstelle und Saatkorpus (D293, D269, 01 §B.2)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.korpus import seed_lines
from tools.verdikt import verdikt_line

_VECTORS = json.loads(
    (Path(__file__).resolve().parent / "vectors" / "vectors_01.json").read_text()
)
_BY_NAME = {v["name"]: v for v in _VECTORS["vectors"]}
_SEED = seed_lines()


def _expected(entry: dict) -> str:
    if "expect_reject" in entry:
        return f"reject {entry['expect_reject']}"
    return f"ok {entry['claim_id']}"


def test_seed_names_match_vector_order() -> None:
    assert [name for name, _hex in _SEED] == [v["name"] for v in _VECTORS["vectors"]]


@pytest.mark.parametrize("name,wire_hex", _SEED, ids=[n for n, _ in _SEED])
def test_verdikt_matches_derived_expectation(name: str, wire_hex: str) -> None:
    assert verdikt_line(wire_hex) == _expected(_BY_NAME[name])


@pytest.mark.parametrize("_name,wire_hex", _SEED, ids=[n for n, _ in _SEED])
def test_uppercase_hex_same_verdikt(_name: str, wire_hex: str) -> None:
    assert verdikt_line(wire_hex.upper()) == verdikt_line(wire_hex)


@pytest.mark.parametrize(
    "line",
    [
        "",
        "   ",
        "a1",
        "aabbccd",
        "zz",
        "aabb ccdd",
        "aa bb cc dd",
    ],
)
def test_non_byte_lines_reject_malformed_cbor(line: str) -> None:
    assert verdikt_line(line) == "reject MALFORMED_CBOR"


def test_trailing_newline_same_verdikt() -> None:
    wire_hex = _SEED[0][1]
    assert verdikt_line(wire_hex + "\n") == verdikt_line(wire_hex)


def test_trailing_space_tab_same_verdikt() -> None:
    wire_hex = _SEED[0][1]
    assert verdikt_line(wire_hex + " \t") == verdikt_line(wire_hex)


def test_inner_whitespace_is_not_a_byte_sequence() -> None:
    wire_hex = _SEED[0][1]
    spaced = wire_hex[:8] + " " + wire_hex[8:16] + " " + wire_hex[16:]
    assert len(spaced) % 2 == 0
    assert verdikt_line(spaced) == "reject MALFORMED_CBOR"
