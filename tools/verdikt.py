#!/usr/bin/env python3
"""Zeilenschnittstelle des Verifizierers (D293, D269, 01 §B.2, 01 §6)."""

from __future__ import annotations

import sys
from typing import TextIO

from symbolon.atom import claim_id
from symbolon.errors import ErrorCode
from symbolon.verifier import read_claim


def line_bytes(line: str) -> bytes | None:
    """Rohe Zeile zu Bytes; None, wenn sie keine Bytefolge bezeichnet (D293, D269)."""
    trimmed = line.rstrip("\r\n\t ")
    if len(trimmed) % 2 == 1:
        return None
    for ch in trimmed:
        if ch not in "0123456789abcdefABCDEF":
            return None
    return bytes.fromhex(trimmed)


def verdikt_line(line: str) -> str:
    """Verdiktzeile aus einer rohen Zeile (D293, 01 §B.2, 01 §6)."""
    data = line_bytes(line)
    if data is None:
        return "reject MALFORMED_CBOR"
    result = read_claim(data)
    if isinstance(result, ErrorCode):
        return f"reject {result.value}"
    return f"ok {claim_id(result).hex()}"


def write_verdikte(src: TextIO, dst: TextIO) -> None:
    """Je Eingabezeile genau eine Verdiktzeile (D293, D269)."""
    for line in src:
        dst.write(verdikt_line(line) + "\n")


def main() -> None:
    write_verdikte(sys.stdin, sys.stdout)


if __name__ == "__main__":
    main()
