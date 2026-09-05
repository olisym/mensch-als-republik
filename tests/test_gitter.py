"""Mutantenmenge der Stufe 1 (D289, D297, D303, D309, 01 §2, 01 §B.2, 01 §3)."""

from __future__ import annotations

import sys

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from symbolon import cbor_canon
from symbolon.domains import DOM_SIG
from symbolon.errors import ErrorCode
from tools.gitter import C_OPERATORS, main, mutant_lines
from tools.korpus import seed_lines
from tools.verdikt import verdikt_line

_SEED_NAMES = frozenset({"TV1", "TV2", "TV3", "TV4", "TV5", "TV6"})
_AUTHOR_SEEDS = (bytes([0x01] * 32), bytes([0x02] * 32))
_NAMED_ABSENT = frozenset({ErrorCode.FOREIGN_LIFECYCLE})


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


def _is_cbor_uint(value: object) -> bool:
    """True gdw. type(value) is int und nicht negativ (D272, D308)."""
    return type(value) is int and value >= 0


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


def test_reject_codes_are_all_error_classes_minus_foreign_lifecycle() -> None:
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


def test_family_c_is_noncanonical_reencoding_of_the_seed() -> None:
    seed_wires = {
        name: bytes.fromhex(wire_hex)
        for name, wire_hex in seed_lines()
        if name in _SEED_NAMES
    }
    for label, wire_hex in mutant_lines():
        wire = bytes.fromhex(wire_hex)
        if label.startswith("C/"):
            seed = seed_wires[label.split("/", 2)[1]]
            assert cbor_canon.reserialize(wire) == seed
            assert wire != seed
        else:
            assert cbor_canon.is_canonical(wire)


def test_family_c_operators_each_yield_noncanonical_encoding() -> None:
    seen = {name: 0 for name in C_OPERATORS}
    for label, wire_hex in mutant_lines():
        if not label.startswith("C/"):
            continue
        operator = label.split("/")[2]
        assert operator in seen
        assert verdikt_line(wire_hex) == "reject NON_CANONICAL_ENCODING"
        seen[operator] += 1
    assert all(count > 0 for count in seen.values()), seen


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


def test_foreign_version_requires_a_readable_uint() -> None:
    readable = 0
    unreadable = 0
    for label, wire_hex in mutant_lines():
        decoded = cbor_canon.decode(bytes.fromhex(wire_hex))
        version = decoded.get(0) if isinstance(decoded, dict) else None
        if _is_cbor_uint(version) and version == 1:
            continue
        verdikt = verdikt_line(wire_hex)
        if _is_cbor_uint(version):
            assert verdikt == "reject UNSUPPORTED_VERSION", label
            readable += 1
        else:
            assert verdikt == "reject MALFORMED_CBOR", label
            unreadable += 1
    assert readable >= 1
    assert unreadable >= 1


def test_feldkopf_breiter_labels_match_reachable_value_heads() -> None:
    """Ein Etikett je Schlüssel, dessen Wertkopf Major ≠ 7 und AI < 27 trägt (D309)."""
    operator = "feldkopf_breiter"
    expected: set[str] = set()
    for name, wire_hex in seed_lines():
        if name not in _SEED_NAMES:
            continue
        decoded = cbor_canon.decode(bytes.fromhex(wire_hex))
        for key, value in decoded.items():
            head = cbor_canon.encode(value)[0]
            major = head >> 5
            ai = head & 0x1F
            if major != 7 and ai < 27:
                expected.add(f"C/{name}/{operator}/{key}")
    actual = {
        label
        for label, _wire_hex in mutant_lines()
        if label.startswith("C/") and label.split("/")[2] == operator
    }
    assert actual == expected
