"""Fixtures für Layer-03-Vektoren (03-golden-anchors.md §2–§3, D88)."""

from __future__ import annotations

import hashlib

from symbolon import cbor_canon
from symbolon.domains import DOM_NUC_GEN
from tests.helpers import SEED_ALICE, SEED_BOB, SEED_CAROL, Identity

ALICE = Identity("ALICE", seed=SEED_ALICE)
BOB = Identity("BOB", seed=SEED_BOB)
CAROL = Identity("CAROL", seed=SEED_CAROL)

# Dokumentierte Ankerwerte (03-golden-anchors.md) — nur zum Prüfen, nicht zum Bauen.
DOC_CONSTITUTION_HASH_A = bytes.fromhex(
    "890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e6585c352dcf19ccad5ea7e"
)
DOC_CONSTITUTION_HASH_B = bytes.fromhex(
    "9053909b466d60dd8d97947db67513af01a1ddeb32c6fa48dd3f584a4d74f026"
)
DOC_CONSTITUTION_HASH_C = bytes.fromhex(
    "f306b62560cbf3c5253a4a0dc0ca5744fe815cfa100b924b0ff9202873e25e08"
)
DOC_N_A = bytes.fromhex(
    "65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557"
)
DOC_N_B = bytes.fromhex(
    "7ce9653872a4143b85ff00d8d8af4ebc7dcb5da19d8d9907a423b477534bbb0c"
)
DOC_N_C = bytes.fromhex(
    "dffbe29a24c55594f387ea8d33fb5f0534424a3dfe828f9b0d91a4e072ad0069"
)

UNIT_REF = hashlib.sha256(b"mar/example/unit-of-account/Stunde").digest()
REASON_REF = hashlib.sha256(b"mar/example/verdict-reason/nichtlieferung").digest()

NOW = 1000


def _thresholds() -> dict:
    return {
        "ordinary": [1, 2],
        "membership": [2, 3],
        "amendment": [3, 4],
    }


CONSTITUTION_A: dict = {
    "irrevocable_predicates": ["obligation@1"],
    "thresholds": _thresholds(),
    "arbitration": {"arbitrators": [ALICE.pub]},
}

CONSTITUTION_B: dict = {
    "thresholds": _thresholds(),
    "arbitration": {"arbitrators": [ALICE.pub, BOB.pub]},
    "irrevocable_predicates": ["vouch@1"],
}

CONSTITUTION_C: dict = {
    "thresholds": _thresholds(),
    "arbitration": {"arbitrators": [ALICE.pub]},
}


def _constitution_hash(obj: dict) -> bytes:
    return hashlib.sha256(cbor_canon.encode(obj)).digest()


def _genesis(constitution_hash: bytes) -> dict:
    return {
        0: 1,
        1: [ALICE.pub],
        2: 0,
        3: [ALICE.pub],
        4: constitution_hash,
        5: 2,
        6: 1,
        7: 0,
    }


def _scope(genesis_obj: dict) -> bytes:
    return hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis_obj)).digest()


CONSTITUTION_HASH_A = _constitution_hash(CONSTITUTION_A)
CONSTITUTION_HASH_B = _constitution_hash(CONSTITUTION_B)
CONSTITUTION_HASH_C = _constitution_hash(CONSTITUTION_C)

GENESIS_A = _genesis(CONSTITUTION_HASH_A)
GENESIS_B = _genesis(CONSTITUTION_HASH_B)
GENESIS_C = _genesis(CONSTITUTION_HASH_C)

N_A = _scope(GENESIS_A)
N_B = _scope(GENESIS_B)
N_C = _scope(GENESIS_C)


def fresh_alice() -> Identity:
    return Identity("ALICE", seed=SEED_ALICE)


def fresh_bob() -> Identity:
    return Identity("BOB", seed=SEED_BOB)


def fresh_carol() -> Identity:
    return Identity("CAROL", seed=SEED_CAROL)


def nuc(scope: bytes, name: str) -> str:
    return f"nuc:{scope.hex()}/{name}@1"
