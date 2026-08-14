"""Fixtures für Layer-04-Vektoren (04-golden-anchors.md §2–§3)."""

from __future__ import annotations

import hashlib

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import Claim
from mensch_als_republik.domains import DOM_NUC_GEN
from mensch_als_republik.governance.objects import Epoch, Proposal
from mensch_als_republik.policy import NucleusPolicy, constitution_hash
from tests.helpers import SEED_ALICE, SEED_BOB, SEED_CAROL, Identity

SEED_DAVE = bytes([0x04] * 32)
SEED_EVE = bytes([0x05] * 32)

ALICE = Identity("ALICE", seed=SEED_ALICE)
BOB = Identity("BOB", seed=SEED_BOB)
CAROL = Identity("CAROL", seed=SEED_CAROL)
DAVE = Identity("DAVE", seed=SEED_DAVE)
EVE = Identity("EVE", seed=SEED_EVE)

DOC_CONSTITUTION_HASH_1 = bytes.fromhex(
    "8e7762ef9a8b9a414cbec44ad0b4658e3ae17d2663c6d3fc12af64a8ac78f3b0"
)
DOC_CONSTITUTION_HASH_2 = bytes.fromhex(
    "3ba90e8c98aca71654c2559ed4affde521e2860e228bf9ae57a07a3d1f92d2d0"
)
DOC_CONSTITUTION_HASH_3 = bytes.fromhex(
    "09c2441d09546d7546f043bb57be2349709fc9fca5db69d66245aa82fd505e86"
)
DOC_N_D = bytes.fromhex(
    "a15c70c4829e7a296b5af56656e0a94b9ea9391096515c9cc592e18bd2d9f7ef"
)
DOC_EPOCH_ID_1 = bytes.fromhex(
    "56915063c07ce1e6b74e10712e8f17b9f381af359a3e12b9719e90a52483d724"
)
DOC_PROPOSAL_HASH_1 = bytes.fromhex(
    "38edfd6b0ba90ade0b96746c21ead9e631c1dac883150a15ed923dd1aaf6db6b"
)
DOC_EPOCH_ID_2 = bytes.fromhex(
    "50a33beff78aae27f6ac8da621879a686055190eabcb7832867f9b7b00d5c182"
)
DOC_PROPOSAL_HASH_2 = bytes.fromhex(
    "8350006de0acc4089a347920748a70cc72068eb20e0995a8960d58e6581fd018"
)
DOC_EPOCH_ID_3 = bytes.fromhex(
    "c052fd3b7c81d4d0a65adb892476a830666ae3ffebb928b355806c882fc9589a"
)

DOC_STOCK_CONSTITUTION_HASH = bytes.fromhex(
    "890b21e7cd43fc4226938ce0b6eae1d00efa04ef9e6585c352dcf19ccad5ea7e"
)
DOC_STOCK_N = bytes.fromhex(
    "65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557"
)

NOW = 1000

P1 = [BOB.pub, ALICE.pub, DAVE.pub, CAROL.pub]
P2 = [EVE.pub, BOB.pub, ALICE.pub, DAVE.pub, CAROL.pub]


def _thresholds() -> dict:
    return {
        "ordinary": [1, 2],
        "membership": [2, 3],
        "amendment": [3, 4],
    }


def _constitution(
    *,
    participants: list[bytes],
    thresholds: dict | None = None,
    arbitrators: list[bytes] | None = None,
    irrevocable: list[str] | None = None,
) -> dict:
    return {
        "irrevocable_predicates": irrevocable
        if irrevocable is not None
        else ["obligation@1", "ratify@1", "vote@1"],
        "thresholds": thresholds if thresholds is not None else _thresholds(),
        "arbitration": {"arbitrators": arbitrators if arbitrators is not None else [ALICE.pub]},
        "participants": participants,
    }


C1 = _constitution(participants=P1)
C2 = _constitution(participants=P2)
C3 = _constitution(participants=P2, arbitrators=[BOB.pub, ALICE.pub])
C1_AMEND = _constitution(participants=P1, arbitrators=[BOB.pub])
C2_LOWER = _constitution(
    participants=P2,
    thresholds={"ordinary": [1, 2], "membership": [2, 3], "amendment": [1, 2]},
)
C2_HALF = _constitution(
    participants=P2,
    thresholds={"ordinary": [1, 2], "membership": [2, 3], "amendment": [1, 2]},
)
C2_HIGH = _constitution(
    participants=P2,
    thresholds={"ordinary": [1, 2], "membership": [2, 3], "amendment": [4, 5]},
)
C2_ALT_A = _constitution(participants=P2, arbitrators=[BOB.pub])
C2_ALT_B = _constitution(participants=P2, arbitrators=[CAROL.pub])

CONSTITUTION_HASH_1 = constitution_hash(C1)
CONSTITUTION_HASH_2 = constitution_hash(C2)
CONSTITUTION_HASH_3 = constitution_hash(C3)

GENESIS_D = {
    0: 1,
    1: [ALICE.pub],
    2: 0,
    3: [ALICE.pub],
    4: CONSTITUTION_HASH_1,
    5: 2,
    6: 0,
    7: 0,
}

N_D = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(GENESIS_D)).digest()

EPOCH_1 = Epoch(scope=N_D, index=1, constitution_hash=CONSTITUTION_HASH_1)
PROPOSAL_1 = Proposal(
    scope=N_D, predecessor=EPOCH_1.epoch_id, constitution_hash=CONSTITUTION_HASH_2
)
EPOCH_2 = Epoch(scope=N_D, index=2, constitution_hash=CONSTITUTION_HASH_2)
PROPOSAL_2 = Proposal(
    scope=N_D, predecessor=EPOCH_2.epoch_id, constitution_hash=CONSTITUTION_HASH_3
)
EPOCH_3 = Epoch(scope=N_D, index=3, constitution_hash=CONSTITUTION_HASH_3)
PROPOSAL_AMEND_E1 = Proposal(
    scope=N_D, predecessor=EPOCH_1.epoch_id, constitution_hash=constitution_hash(C1_AMEND)
)
PROPOSAL_LOWER = Proposal(
    scope=N_D, predecessor=EPOCH_2.epoch_id, constitution_hash=constitution_hash(C2_LOWER)
)
EPOCH_2_HALF = Epoch(scope=N_D, index=2, constitution_hash=constitution_hash(C2_HALF))
PROPOSAL_HIGH = Proposal(
    scope=N_D,
    predecessor=EPOCH_2_HALF.epoch_id,
    constitution_hash=constitution_hash(C2_HIGH),
)
PROPOSAL_ALT_A = Proposal(
    scope=N_D, predecessor=EPOCH_2.epoch_id, constitution_hash=constitution_hash(C2_ALT_A)
)
PROPOSAL_ALT_B = Proposal(
    scope=N_D, predecessor=EPOCH_2.epoch_id, constitution_hash=constitution_hash(C2_ALT_B)
)

STOCK_CONSTITUTION = {
    "irrevocable_predicates": ["obligation@1"],
    "thresholds": _thresholds(),
    "arbitration": {"arbitrators": [ALICE.pub]},
}
STOCK_CONSTITUTION_HASH = constitution_hash(STOCK_CONSTITUTION)
STOCK_GENESIS = {
    0: 1,
    1: [ALICE.pub],
    2: 0,
    3: [ALICE.pub],
    4: STOCK_CONSTITUTION_HASH,
    5: 2,
    6: 1,
    7: 0,
}
STOCK_N = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(STOCK_GENESIS)).digest()


def fresh_alice() -> Identity:
    return Identity("ALICE", seed=SEED_ALICE)


def fresh_bob() -> Identity:
    return Identity("BOB", seed=SEED_BOB)


def fresh_carol() -> Identity:
    return Identity("CAROL", seed=SEED_CAROL)


def fresh_dave() -> Identity:
    return Identity("DAVE", seed=SEED_DAVE)


def fresh_eve() -> Identity:
    return Identity("EVE", seed=SEED_EVE)


def fresh_p1() -> tuple[Identity, Identity, Identity, Identity]:
    return fresh_alice(), fresh_bob(), fresh_carol(), fresh_dave()


def fresh_p2() -> tuple[Identity, Identity, Identity, Identity, Identity]:
    return fresh_alice(), fresh_bob(), fresh_carol(), fresh_dave(), fresh_eve()


def nuc(scope: bytes, name: str) -> str:
    return f"nuc:{scope.hex()}/{name}@1"


def policy_of(constitution_obj: dict, scope: bytes = N_D) -> NucleusPolicy:
    return NucleusPolicy(
        scope, declared=constitution_obj.get("irrevocable_predicates", [])
    )


def vote(
    identity: Identity,
    proposal: Proposal,
    *,
    choice: int,
    t: int,
    scope: bytes | None = None,
    t_exp: int | None = None,
) -> Claim:
    use_scope = scope if scope is not None else N_D
    return identity.claim(
        p=nuc(use_scope, "vote"),
        J=(3, proposal.proposal_hash),
        t=t,
        N=use_scope,
        v=cbor_canon.encode({0: choice}),
        t_exp=t_exp,
    )


def ratify_claim(
    identity: Identity,
    proposal: Proposal,
    *,
    witnesses: list[bytes],
    t: int,
    t_exp: int | None = None,
) -> Claim:
    return identity.claim(
        p=nuc(N_D, "ratify"),
        J=(3, proposal.proposal_hash),
        t=t,
        N=N_D,
        v=cbor_canon.encode({0: witnesses}),
        t_exp=t_exp,
    )


def propose_claim(identity: Identity, proposal: Proposal, *, t: int) -> Claim:
    return identity.claim(
        p=nuc(N_D, "propose"),
        J=(3, proposal.proposal_hash),
        t=t,
        N=N_D,
    )
