"""Ankerreproduktion — Profil D und Bestandsanker aus 00 §3.1 (04-prompt.md §8.1)."""

from __future__ import annotations

import hashlib

from mensch_als_republik import cbor_canon
from mensch_als_republik.domains import DOM_NUC_GEN

from .fixtures import (
    CONSTITUTION_HASH_1,
    CONSTITUTION_HASH_2,
    CONSTITUTION_HASH_3,
    DOC_CONSTITUTION_HASH_1,
    DOC_CONSTITUTION_HASH_2,
    DOC_CONSTITUTION_HASH_3,
    DOC_EPOCH_ID_1,
    DOC_EPOCH_ID_2,
    DOC_EPOCH_ID_3,
    DOC_N_D,
    DOC_PROPOSAL_HASH_1,
    DOC_PROPOSAL_HASH_2,
    DOC_STOCK_CONSTITUTION_HASH,
    DOC_STOCK_N,
    EPOCH_1,
    EPOCH_2,
    EPOCH_3,
    GENESIS_D,
    N_D,
    PROPOSAL_1,
    PROPOSAL_2,
    STOCK_CONSTITUTION_HASH,
    STOCK_GENESIS,
    STOCK_N,
)


def test_profil_d_hashes_match_documented() -> None:
    assert CONSTITUTION_HASH_1 == DOC_CONSTITUTION_HASH_1
    assert CONSTITUTION_HASH_2 == DOC_CONSTITUTION_HASH_2
    assert CONSTITUTION_HASH_3 == DOC_CONSTITUTION_HASH_3
    assert N_D == DOC_N_D
    assert EPOCH_1.epoch_id == DOC_EPOCH_ID_1
    assert PROPOSAL_1.proposal_hash == DOC_PROPOSAL_HASH_1
    assert EPOCH_2.epoch_id == DOC_EPOCH_ID_2
    assert PROPOSAL_2.proposal_hash == DOC_PROPOSAL_HASH_2
    assert EPOCH_3.epoch_id == DOC_EPOCH_ID_3


def test_genesis_d_cbor_matches_documented() -> None:
    assert cbor_canon.encode(GENESIS_D).hex() == (
        "a80001018158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c"
        "0200038158208a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c"
        "0458208e7762ef9a8b9a414cbec44ad0b4658e3ae17d2663c6d3fc12af64a8ac78f3b0"
        "050206000700"
    )


def test_stock_anchors_00() -> None:
    """Bestandsanker aus 00 §3.1 über denselben Kodierungsweg."""
    assert STOCK_CONSTITUTION_HASH == DOC_STOCK_CONSTITUTION_HASH
    assert STOCK_N == DOC_STOCK_N
    assert hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(STOCK_GENESIS)).digest() == STOCK_N
