"""Kanonische CBOR-Enkodierung und Re-Serialisierungs-Check (01 §3)."""

from __future__ import annotations

import cbor2


def encode(obj: object) -> bytes:
    """Deterministische CBOR-Kodierung (RFC 8949 Core Deterministic Encoding)."""
    return cbor2.dumps(obj, canonical=True)


def decode(data: bytes) -> object:
    """CBOR dekodieren."""
    return cbor2.loads(data)


def reserialize(data: bytes) -> bytes:
    """Empfangene Bytes dekodieren und kanonisch re-enkodieren."""
    return encode(decode(data))


def is_canonical(data: bytes) -> bool:
    """True gdw. data bereits kanonisch kodiert ist."""
    return data == reserialize(data)
