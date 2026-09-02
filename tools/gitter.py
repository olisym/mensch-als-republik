#!/usr/bin/env python3
"""Mutantenmenge der Stufe 1 (D289, D297, 01 §2, 01 §B.2)."""

from __future__ import annotations

import sys
from typing import Any

import cbor2
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from mensch_als_republik import cbor_canon
from mensch_als_republik.domains import DOM_SIG
from tools.korpus import seed_lines

_SEED_NAMES = frozenset({"TV1", "TV2", "TV3", "TV4", "TV5", "TV6"})
_AUTHOR_SEEDS = (bytes([0x01] * 32), bytes([0x02] * 32))
_EXTRA_KEYS = (10, 11, 12)
_SIG_KEY = 9

_TYPE_PATTERNS: tuple[tuple[str, object], ...] = (
    ("uint", 0),
    ("nint", -1),
    ("bstr", b""),
    ("tstr", ""),
    ("array", []),
    ("map", {}),
    ("bool", False),
    ("null", None),
    ("float", 0.0),
    ("tag", cbor2.CBORTag(99, 0)),
)


def _type_class(value: object) -> str:
    """Klasse eines Wertes; Wahrheitswert vor der Ganzzahl (D272, D297)."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "uint" if value >= 0 else "nint"
    if isinstance(value, bytes):
        return "bstr"
    if isinstance(value, str):
        return "tstr"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "map"
    if isinstance(value, float):
        return "float"
    if isinstance(value, cbor2.CBORTag):
        return "tag"
    raise TypeError(type(value))


def _value_variants(value: object) -> list[tuple[str, object]]:
    """Wertvarianten innerhalb der Klasse; dem Ausgangswert gleiche entfallen (D297)."""
    cls = _type_class(value)
    raw: list[tuple[str, object]] = []
    if cls == "uint":
        assert isinstance(value, int)
        raw = [
            ("0", 0),
            ("1", 1),
            ("plus1", value + 1),
            ("minus1", value - 1),
            ("2p32", 2**32),
            ("2p64m1", 2**64 - 1),
        ]
        raw = [(n, v) for n, v in raw if isinstance(v, int) and v >= 0]
    elif cls == "nint":
        assert isinstance(value, int)
        raw = [("neg1", -1), ("plus1", value + 1), ("minus1", value - 1)]
    elif cls == "bstr":
        assert isinstance(value, bytes)
        raw = [
            ("zeros", bytes(len(value))),
            ("ones", bytes(b"\x01" * len(value))),
            ("reverse", value[::-1]),
            ("shorter", value[:-1]),
            ("longer", value + b"\x00"),
        ]
    elif cls == "tstr":
        assert isinstance(value, str)
        raw = [
            ("upper", value.upper()),
            ("lower", value.lower()),
            ("prefix", "x" + value),
            ("suffix", value + "x"),
            ("shorter", value[:-1]),
        ]
    elif cls == "bool":
        raw = [("not", not value)]
    elif cls == "array":
        assert isinstance(value, list)
        raw = [
            ("drop_last", value[:-1]),
            ("append", value + [0]),
            ("reverse", value[::-1]),
        ]
    out: list[tuple[str, object]] = []
    for name, variant in raw:
        if variant == value:
            continue
        out.append((name, variant))
    return out


def _load_seeds() -> list[tuple[str, dict[int, Any]]]:
    seeds: list[tuple[str, dict[int, Any]]] = []
    for name, wire_hex in seed_lines():
        if name not in _SEED_NAMES:
            continue
        decoded = cbor_canon.decode(bytes.fromhex(wire_hex))
        if not isinstance(decoded, dict):
            raise TypeError(name)
        seeds.append((name, decoded))
    return seeds


def _author_sk(identity: bytes) -> Ed25519PrivateKey:
    """Schlüssel des Autors der Saat, nicht des mutierten Feldes (D297 Beschluss 3)."""
    for seed in _AUTHOR_SEEDS:
        sk = Ed25519PrivateKey.from_private_bytes(seed)
        if sk.public_key().public_bytes_raw() == identity:
            return sk
    raise ValueError(identity.hex())


def _clone(value: object) -> object:
    """Wert kopieren; CBORTag ist nicht picklebar."""
    if isinstance(value, cbor2.CBORTag):
        return cbor2.CBORTag(value.tag, _clone(value.value))
    if isinstance(value, dict):
        return {k: _clone(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_clone(v) for v in value]
    return value


def _with_field(m: dict[int, Any], key: int, value: object) -> dict[int, Any]:
    out = {k: _clone(v) for k, v in m.items()}
    out[key] = _clone(value)
    return out


def _without_field(m: dict[int, Any], key: int) -> dict[int, Any]:
    out = {k: _clone(v) for k, v in m.items()}
    del out[key]
    return out


def _core_keys(m: dict[int, Any]) -> list[int]:
    return sorted(k for k in m if k != _SIG_KEY)


def _core_mutants(
    seeds: list[tuple[str, dict[int, Any]]],
) -> list[tuple[str, dict[int, Any]]]:
    """Mutanten der Schlüssel ausser neun, plus drei Fremdschlüssel je Saat (D289, D297)."""
    out: list[tuple[str, dict[int, Any]]] = []
    for name, m in seeds:
        for key in _core_keys(m):
            value = m[key]
            own = _type_class(value)
            for cls, pattern in _TYPE_PATTERNS:
                if cls == own:
                    continue
                out.append((f"{name}/{key}/typ/{cls}", _with_field(m, key, pattern)))
            for detail, variant in _value_variants(value):
                out.append((f"{name}/{key}/wert/{detail}", _with_field(m, key, variant)))
            if isinstance(value, list):
                for idx, elem in enumerate(value):
                    elem_cls = _type_class(elem)
                    for cls, pattern in _TYPE_PATTERNS:
                        if cls == elem_cls:
                            continue
                        arr = [_clone(item) for item in value]
                        arr[idx] = _clone(pattern)
                        out.append(
                            (
                                f"{name}/{key}/rekursion/{idx}/typ/{cls}",
                                _with_field(m, key, arr),
                            )
                        )
                    for detail, variant in _value_variants(elem):
                        arr = [_clone(item) for item in value]
                        arr[idx] = _clone(variant)
                        out.append(
                            (
                                f"{name}/{key}/rekursion/{idx}/wert/{detail}",
                                _with_field(m, key, arr),
                            )
                        )
            out.append((f"{name}/{key}/entfernen", _without_field(m, key)))
            for other_name, other in seeds:
                if other_name == name or key not in other:
                    continue
                if other[key] == value:
                    continue
                out.append(
                    (
                        f"{name}/{key}/fremd/{other_name}",
                        _with_field(m, key, other[key]),
                    )
                )
            for src in _core_keys(m):
                if src == key or m[src] == value:
                    continue
                out.append(
                    (f"{name}/{key}/kopie/{src}", _with_field(m, key, m[src]))
                )
        for extra in _EXTRA_KEYS:
            out.append((f"{name}/{extra}/extra", _with_field(m, extra, 1)))
    return out


def _sigma_mutants(
    seeds: list[tuple[str, dict[int, Any]]],
) -> list[tuple[str, dict[int, Any]]]:
    """Mutationen auf Schlüssel neun: Typ, Wert, Entfernen (D289 Beschluss 3, D297)."""
    out: list[tuple[str, dict[int, Any]]] = []
    for name, m in seeds:
        value = m[_SIG_KEY]
        own = _type_class(value)
        for cls, pattern in _TYPE_PATTERNS:
            if cls == own:
                continue
            out.append((f"{name}/{_SIG_KEY}/typ/{cls}", _with_field(m, _SIG_KEY, pattern)))
        for detail, variant in _value_variants(value):
            out.append(
                (f"{name}/{_SIG_KEY}/wert/{detail}", _with_field(m, _SIG_KEY, variant))
            )
        out.append((f"{name}/{_SIG_KEY}/entfernen", _without_field(m, _SIG_KEY)))
    return out


def _sign_a(m: dict[int, Any], sk: Ed25519PrivateKey) -> bytes:
    core = {k: v for k, v in m.items() if k != _SIG_KEY}
    sigma = sk.sign(DOM_SIG + cbor_canon.encode(core))
    signed = dict(core)
    signed[_SIG_KEY] = sigma
    return cbor_canon.encode(signed)


def _encode(m: dict[int, Any]) -> bytes:
    return cbor_canon.encode(m)


def mutant_lines() -> list[tuple[str, str]]:
    """Paare aus Etikett und Drahtbytes in Hex, stabile Reihenfolge (D289, D297)."""
    seeds = _load_seeds()
    seed_sk = {name: _author_sk(m[1]) for name, m in seeds}
    seed_wires = {cbor_canon.encode(m) for _name, m in seeds}
    seen: set[bytes] = set()
    pairs: list[tuple[str, str]] = []

    def _take(label: str, wire: bytes) -> None:
        if wire in seen or wire in seed_wires:
            return
        seen.add(wire)
        pairs.append((label, wire.hex()))

    core = _core_mutants(seeds)
    for body, m in core:
        seed_name = body.split("/", 1)[0]
        _take(f"A/{body}", _sign_a(m, seed_sk[seed_name]))
    for body, m in core:
        _take(f"B/{body}", _encode(m))
    for body, m in _sigma_mutants(seeds):
        _take(f"B/{body}", _encode(m))
    return pairs


def main() -> None:
    pairs = mutant_lines()
    if "--manifest" in sys.argv[1:]:
        for label, _wire_hex in pairs:
            print(label)
        return
    for _label, wire_hex in pairs:
        print(wire_hex)


if __name__ == "__main__":
    main()
