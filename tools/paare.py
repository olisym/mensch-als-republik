#!/usr/bin/env python3
"""Paarmutanten der Stufe 2 (D305, D306, D289, 01 §B.2)."""

from __future__ import annotations

import sys
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from symbolon import cbor_canon
from tools.gitter import (
    SEED_NAMES,
    SIG_KEY,
    author_sk,
    clone,
    sign_a,
    mutant_lines as gitter_lines,
)
from tools.korpus import seed_lines
from tools.verdikt import verdikt_line

_MALFORMED = "reject MALFORMED_CBOR"


def _load_seeds() -> tuple[dict[str, dict[int, Any]], dict[str, Ed25519PrivateKey]]:
    maps: dict[str, dict[int, Any]] = {}
    keys: dict[str, Ed25519PrivateKey] = {}
    for name, wire_hex in seed_lines():
        if name not in SEED_NAMES:
            continue
        decoded = cbor_canon.decode(bytes.fromhex(wire_hex))
        if not isinstance(decoded, dict):
            raise TypeError(name)
        maps[name] = decoded
        keys[name] = author_sk(decoded[1])
    return maps, keys


def _changed_keys(
    seed: dict[int, Any], mutant: dict[int, Any], *, core_only: bool
) -> list[int]:
    """Schlüssel, die hinzugekommen, weggefallen oder anders belegt sind (Auftrag 3)."""
    if core_only:
        seed_f = {k: v for k, v in seed.items() if k != SIG_KEY}
        mut_f = {k: v for k, v in mutant.items() if k != SIG_KEY}
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


def _einzelcode(verdikt: str) -> str:
    if verdikt.startswith("ok "):
        return "ok"
    return verdikt.split(" ", 1)[1]


def _mangelteil(label: str) -> str:
    return label.split("/", 2)[2]


def _paar_etikett(art: str, familie: str, saat: str, a: str, b: str) -> str:
    x, y = sorted((_mangelteil(a), _mangelteil(b)))
    return f"{art}/{familie}/{saat}/{x}+{y}"


def _apply_two(
    seed: dict[int, Any],
    mut_a: dict[int, Any],
    key_a: int,
    mut_b: dict[int, Any],
    key_b: int,
    family: str,
    sk: Ed25519PrivateKey,
) -> bytes:
    out = {k: clone(v) for k, v in seed.items()}
    for key, mut in ((key_a, mut_a), (key_b, mut_b)):
        if key not in mut:
            del out[key]
        else:
            out[key] = clone(mut[key])
    if family == "A":
        return sign_a(out, sk)
    return cbor_canon.encode(out)


def _klasse(v1: str, v2: str) -> int | None:
    if v1 == _MALFORMED or v2 == _MALFORMED:
        return None
    ok1 = v1.startswith("ok ")
    ok2 = v2.startswith("ok ")
    if ok1 and ok2:
        return 1
    if ok1 or ok2:
        return 2
    return 3


def _build() -> tuple[list[tuple[str, str]], list[str], int]:
    """Paare, nicht paarbare Etiketten, Zahl der verworfenen Doppelten (D305, D306)."""
    seeds, seed_sk = _load_seeds()
    unpaarbar: list[str] = []
    grouped: dict[tuple[str, str], list[tuple[str, int, dict[int, Any], str]]] = {}
    for label, wire_hex in gitter_lines():
        family, _, rest = label.partition("/")
        if family == "C":
            continue
        seed_name, _, _body = rest.partition("/")
        decoded = cbor_canon.decode(bytes.fromhex(wire_hex))
        if not isinstance(decoded, dict):
            unpaarbar.append(label)
            continue
        keys = _changed_keys(seeds[seed_name], decoded, core_only=family == "A")
        if len(keys) != 1:
            unpaarbar.append(label)
            continue
        verdikt = verdikt_line(wire_hex)
        grouped.setdefault((family, seed_name), []).append(
            (label, keys[0], decoded, verdikt)
        )

    vorrang: list[tuple[str, bytes]] = []
    klassen: list[tuple[str, bytes]] = []
    for (family, seed_name), recs in grouped.items():
        seed = seeds[seed_name]
        sk = seed_sk[seed_name]
        by_code: dict[str, list[tuple[str, int, dict[int, Any], str]]] = {}
        malformed: list[tuple[str, int, dict[int, Any], str]] = []
        for rec in recs:
            code = _einzelcode(rec[3])
            if code == "MALFORMED_CBOR":
                malformed.append(rec)
            else:
                by_code.setdefault(code, []).append(rec)
        malformed.sort(key=lambda r: r[0])
        for code in sorted(by_code):
            candidates = sorted(by_code[code], key=lambda r: r[0])
            rep = candidates[0]
            partner = next((m for m in malformed if m[1] != rep[1]), None)
            if partner is None:
                continue
            wire = _apply_two(
                seed, rep[2], rep[1], partner[2], partner[1], family, sk
            )
            label = _paar_etikett("PV", family, seed_name, rep[0], partner[0])
            vorrang.append((label, wire))
        n = len(recs)
        for i in range(n):
            for j in range(i + 1, n):
                if recs[i][1] == recs[j][1]:
                    continue
                kls = _klasse(recs[i][3], recs[j][3])
                if kls is None:
                    continue
                wire = _apply_two(
                    seed,
                    recs[i][2],
                    recs[i][1],
                    recs[j][2],
                    recs[j][1],
                    family,
                    sk,
                )
                label = _paar_etikett(
                    f"P{kls}", family, seed_name, recs[i][0], recs[j][0]
                )
                klassen.append((label, wire))

    pairs: list[tuple[str, str]] = []
    seen: set[bytes] = set()
    discarded = 0
    for label, wire in (*vorrang, *klassen):
        if wire in seen:
            discarded += 1
            continue
        seen.add(wire)
        pairs.append((label, wire.hex()))
    return pairs, unpaarbar, discarded


def mutant_lines() -> list[tuple[str, str]]:
    """Paare aus Etikett und Drahtbytes in Hex, stabile Reihenfolge (D305, D306)."""
    pairs, _unpaarbar, _discarded = _build()
    return pairs


def main() -> None:
    pairs, unpaarbar, _discarded = _build()
    if "--manifest" in sys.argv[1:]:
        for label, _wire_hex in pairs:
            print(label)
    else:
        for _label, wire_hex in pairs:
            print(wire_hex)
    for label in unpaarbar:
        print(f"nicht paarbar: {label}", file=sys.stderr)


if __name__ == "__main__":
    main()
