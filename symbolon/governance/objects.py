"""Epochen- und Vorschlagsidentität (04 §1.1, 04 §2.4)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from symbolon import cbor_canon
from symbolon.domains import DOM_NUC_EPOCH, DOM_NUC_PROPOSAL


def epoch_id(scope: bytes, index: int, constitution_hash: bytes) -> bytes:
    """SHA-256(DOM_NUC_EPOCH || cbor([scope, index, constitution_hash]))."""
    return hashlib.sha256(
        DOM_NUC_EPOCH + cbor_canon.encode([scope, index, constitution_hash])
    ).digest()


def proposal_hash(scope: bytes, predecessor: bytes, constitution_hash: bytes) -> bytes:
    """SHA-256(DOM_NUC_PROPOSAL || cbor({0: scope, 1: predecessor, 2: constitution_hash}))."""
    return hashlib.sha256(
        DOM_NUC_PROPOSAL
        + cbor_canon.encode({0: scope, 1: predecessor, 2: constitution_hash})
    ).digest()


@dataclass(frozen=True, slots=True)
class Epoch:
    """Abgeleitete Epochenidentität (04-governance.md §1.1)."""

    scope: bytes
    index: int
    constitution_hash: bytes

    @property
    def epoch_id(self) -> bytes:
        return epoch_id(self.scope, self.index, self.constitution_hash)


@dataclass(frozen=True, slots=True)
class Proposal:
    """Content-adressiertes Vorschlagsobjekt (04-governance.md §2.4)."""

    scope: bytes
    predecessor: bytes
    constitution_hash: bytes

    @property
    def proposal_hash(self) -> bytes:
        return proposal_hash(self.scope, self.predecessor, self.constitution_hash)
