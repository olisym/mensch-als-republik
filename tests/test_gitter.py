"""Mutantenmenge der Stufe 1 (D289, D297, 01 §2, 01 §B.2)."""

from __future__ import annotations

import sys

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mensch_als_republik import cbor_canon
from mensch_als_republik.domains import DOM_SIG
from mensch_als_republik.errors import ErrorCode
from tools.gitter import main, mutant_lines
from tools.korpus import seed_lines
from tools.verdikt import verdikt_line

_SEED_NAMES = frozenset({"TV1", "TV2", "TV3", "TV4", "TV5", "TV6"})
_AUTHOR_SEEDS = (bytes([0x01] * 32), bytes([0x02] * 32))
_NAMED_ABSENT = frozenset(
    {ErrorCode.NON_CANONICAL_ENCODING, ErrorCode.FOREIGN_LIFECYCLE}
)


def _author_sk(identity: bytes) -> Ed25519PrivateKey:
    for seed in _AUTHOR_SEEDS:
        sk = Ed25519PrivateKey.from_private_bytes(seed)
        if sk.public_key().public_bytes_raw() == identity:
            return sk
    raise ValueError(identity.hex())


def _seed_maps() -> dict[str, dict]:
    maps: dict[str, dict] = {}
    for name, wire_hex in seed_lines():
        if name not in _SEED_NAMES:
            continue
        maps[name] = cbor_canon.decode(bytes.fromhex(wire_hex))
    return maps


def test_labels_are_pairwise_distinct_and_outputs_match() -> None:
    pairs = mutant_lines()
    labels = [label for label, _hex in pairs]
    hexes = [wire_hex for _label, wire_hex in pairs]
    assert len(labels) == len(set(labels))
    assert len(labels) == len(hexes)


def test_main_label_and_hex_line_counts_match(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(sys, "argv", ["gitter.py"])
    main()
    hex_lines = capsys.readouterr().out.splitlines()
    monkeypatch.setattr(sys, "argv", ["gitter.py", "--manifest"])
    main()
    label_lines = capsys.readouterr().out.splitlines()
    assert len(label_lines) == len(hex_lines)
    assert len(label_lines) == len(set(label_lines))


def test_no_wire_equals_a_seed_and_none_repeats() -> None:
    seed_hexes = {wire_hex for name, wire_hex in seed_lines() if name in _SEED_NAMES}
    pairs = mutant_lines()
    wires = [wire_hex for _label, wire_hex in pairs]
    assert seed_hexes.isdisjoint(wires)
    assert len(wires) == len(set(wires))


def test_two_calls_are_identical() -> None:
    assert mutant_lines() == mutant_lines()


def test_family_a_signature_is_seed_author_over_mutant_core() -> None:
    seeds = _seed_maps()
    for label, wire_hex in mutant_lines():
        if not label.startswith("A/"):
            continue
        seed_name = label.split("/", 2)[1]
        mutant = cbor_canon.decode(bytes.fromhex(wire_hex))
        core = {k: v for k, v in mutant.items() if k != 9}
        sk = _author_sk(seeds[seed_name][1])
        expected = sk.sign(DOM_SIG + cbor_canon.encode(core))
        assert mutant[9] == expected


def test_reject_codes_are_all_error_classes_minus_two_named() -> None:
    expected = {code.value for code in ErrorCode} - {c.value for c in _NAMED_ABSENT}
    seen: set[str] = set()
    for _label, wire_hex in mutant_lines():
        line = verdikt_line(wire_hex)
        if line.startswith("reject "):
            seen.add(line.split(" ", 1)[1])
    assert seen == expected


def test_accepted_mutants_carry_claim_id() -> None:
    accepted = 0
    for _label, wire_hex in mutant_lines():
        line = verdikt_line(wire_hex)
        if not line.startswith("ok "):
            continue
        accepted += 1
        claim_hex = line.split(" ", 1)[1]
        assert len(claim_hex) == 64
        assert all(ch in "0123456789abcdef" for ch in claim_hex)
    assert accepted >= 1


def test_each_added_operator_yields_an_accepted_mutant() -> None:
    added = ("wert", "rekursion", "kopie")
    seen = {name: 0 for name in added}
    for label, wire_hex in mutant_lines():
        if not verdikt_line(wire_hex).startswith("ok "):
            continue
        operator = label.split("/")[3]
        if operator in seen:
            seen[operator] += 1
    assert all(count > 0 for count in seen.values()), seen
