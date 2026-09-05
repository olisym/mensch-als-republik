"""Claim-Atom: Datenstruktur, Core, Signatur, Claim-ID (01 §2, 01 §4)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, replace
from typing import Any

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from symbolon import cbor_canon
from symbolon.domains import DOM_CID, DOM_ID_GEN, DOM_SIG

_NULL_HPREV = bytes(32)


@dataclass(frozen=True, slots=True)
class Claim:
    """Claim-Atom mit Feldern aus 01 §2 (CBOR-Keys 0–9)."""

    version: int
    I: bytes
    J: tuple[int, bytes]
    p: str
    t: int
    h_prev: bytes
    v: bytes | None = None
    N: bytes | None = None
    t_exp: int | None = None
    sigma: bytes | None = None

    def __post_init__(self) -> None:
        if len(self.I) != 32:
            raise ValueError("I must be 32 bytes")
        if len(self.J[1]) != 32:
            raise ValueError("J.value must be 32 bytes")
        if len(self.h_prev) != 32:
            raise ValueError("h_prev must be 32 bytes")
        if self.N is not None and len(self.N) != 32:
            raise ValueError("N must be 32 bytes")
        if self.sigma is not None and len(self.sigma) != 64:
            raise ValueError("sigma must be 64 bytes")


def core_map(claim: Claim) -> dict[int, Any]:
    """Keys 0–8 ohne σ; abwesende optionale Felder lassen ihren Key weg (01 §3 Regel 5)."""
    m: dict[int, Any] = {
        0: claim.version,
        1: claim.I,
        2: list(claim.J),
        3: claim.p,
        6: claim.t,
        8: claim.h_prev,
    }
    if claim.v is not None:
        m[4] = claim.v
    if claim.N is not None:
        m[5] = claim.N
    if claim.t_exp is not None:
        m[7] = claim.t_exp
    return m


def signed_map(claim: Claim) -> dict[int, Any]:
    """Vollständige CBOR-Map inkl. σ (Key 9)."""
    m = core_map(claim)
    if claim.sigma is not None:
        m[9] = claim.sigma
    return m


def core_bytes(claim: Claim) -> bytes:
    """Kanonische CBOR-Kodierung des Cores."""
    return cbor_canon.encode(core_map(claim))


def signed_bytes(claim: Claim) -> bytes:
    """Kanonische CBOR-Kodierung des signierten Objekts (Keys 0–9)."""
    return cbor_canon.encode(signed_map(claim))


def claim_id(claim: Claim) -> bytes:
    """SHA-256(DOM_CID ‖ core_bytes); signatur-unabhängig (01 §4)."""
    return hashlib.sha256(DOM_CID + core_bytes(claim)).digest()


def sign_preimage(claim: Claim) -> bytes:
    """DOM_SIG ‖ core_bytes."""
    return DOM_SIG + core_bytes(claim)


def sign(sk: Ed25519PrivateKey, claim: Claim) -> bytes:
    """Ed25519-Sign(sk, DOM_SIG ‖ core_bytes) (01 §4)."""
    return sk.sign(sign_preimage(claim))


def build_signed(
    sk: Ed25519PrivateKey,
    *,
    J: tuple[int, bytes],
    p: str,
    t: int,
    h_prev: bytes,
    v: bytes | None = None,
    N: bytes | None = None,
    t_exp: int | None = None,
) -> Claim:
    """Signierten Claim bauen: I aus sk, version 1, sigma via replace (D122, 01 §2/01 §4)."""
    unsigned = Claim(
        version=1,
        I=sk.public_key().public_bytes_raw(),
        J=J,
        p=p,
        t=t,
        h_prev=h_prev,
        v=v,
        N=N,
        t_exp=t_exp,
    )
    return replace(unsigned, sigma=sign(sk, unsigned))


def verify_sig(claim: Claim) -> bool:
    """Ed25519-Verify(I, DOM_SIG ‖ core_bytes, σ)."""
    if claim.sigma is None:
        return False
    try:
        Ed25519PublicKey.from_public_bytes(claim.I).verify(
            claim.sigma, sign_preimage(claim)
        )
        return True
    except Exception:
        return False


def id_genesis_anchor(I: bytes) -> bytes:
    """SHA-256(DOM_ID_GEN ‖ I) (01 §4)."""
    if len(I) != 32:
        raise ValueError("I must be 32 bytes")
    return hashlib.sha256(DOM_ID_GEN + I).digest()


def is_equivocation_pair(c1: Claim, c2: Claim) -> bool:
    """Verschiedene claim_id, gleiches (I, h_prev) (01 §4)."""
    return (
        claim_id(c1) != claim_id(c2)
        and c1.I == c2.I
        and c1.h_prev == c2.h_prev
    )


def is_genesis(claim: Claim) -> bool:
    """True gdw. h_prev == SHA-256(DOM_ID_GEN ‖ I)."""
    return claim.h_prev == id_genesis_anchor(claim.I)


def has_null_hprev(claim: Claim) -> bool:
    """True gdw. h_prev == 32×0x00 (verboten, 01 §4)."""
    return claim.h_prev == _NULL_HPREV


def claim_from_map(m: dict[int, Any]) -> Claim:
    """Claim aus dekodierter CBOR-Map (Keys 0–9) bauen."""
    return Claim(
        version=m[0],
        I=m[1],
        J=(m[2][0], m[2][1]),
        p=m[3],
        t=m[6],
        h_prev=m[8],
        v=m.get(4),
        N=m.get(5),
        t_exp=m.get(7),
        sigma=m.get(9),
    )


def claim_from_bytes(data: bytes) -> Claim:
    """Claim aus kanonischen oder beliebigen CBOR-Bytes dekodieren."""
    obj = cbor_canon.decode(data)
    if not isinstance(obj, dict):
        raise ValueError("expected CBOR map")
    return claim_from_map(obj)
