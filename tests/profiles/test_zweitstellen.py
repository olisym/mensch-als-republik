"""Träger für fünf Doppelerzeuger der Profile (D287)."""

from __future__ import annotations

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import claim_id
from mensch_als_republik.profiles import (
    Finding,
    ProfileFinding,
    membership,
    resolve_policy,
    settlement,
    verdict_status,
)
from mensch_als_republik.profiles.payload import read_v
from tests.helpers import store_with

from .fixtures import (
    ALICE,
    BOB,
    CONSTITUTION_A,
    CONSTITUTION_HASH_A,
    GENESIS_A,
    N_A,
    NOW,
    fresh_alice,
    fresh_bob,
    nuc,
)


def test_read_v_canonical_non_map() -> None:
    """Kanonische Zahl statt Map: UNPARSABLE_V (03 §1.3, D276, D287)."""
    obj, kinds = read_v(cbor_canon.encode(1))
    assert obj is None
    assert kinds == (ProfileFinding.UNPARSABLE_V,)


def test_obligation_v1_wrong_type() -> None:
    """obligation v[1] keine Bytefolge: INVALID_V_TYPE (03 §3.3.2, D287)."""
    alice, bob = fresh_alice(), fresh_bob()
    policy = resolve_policy(
        scope=N_A,
        genesis_obj=GENESIS_A,
        constitution_hash=CONSTITUTION_HASH_A,
        constitution_obj=CONSTITUTION_A,
    ).policy
    obligation = alice.claim(
        p=nuc(N_A, "obligation"),
        J=(1, bob.pub),
        t=1,
        v=cbor_canon.encode({1: 5}),
        N=N_A,
    )
    result = settlement(
        store_with(obligation),
        obligation=obligation,
        scope=N_A,
        now=NOW,
        policy=policy,
    )
    assert Finding(ProfileFinding.INVALID_V_TYPE, claim_id(obligation)) in result.findings


def test_receipt_v0_wrong_type() -> None:
    """receipt v[0] kein uint: INVALID_V_TYPE (03 §3.3.2, D287)."""
    alice, bob = fresh_alice(), fresh_bob()
    policy = resolve_policy(
        scope=N_A,
        genesis_obj=GENESIS_A,
        constitution_hash=CONSTITUTION_HASH_A,
        constitution_obj=CONSTITUTION_A,
    ).policy
    obligation = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    receipt = bob.claim(
        p=nuc(N_A, "receipt"),
        J=(2, claim_id(obligation)),
        t=2,
        v=cbor_canon.encode({0: "x"}),
        N=N_A,
    )
    result = settlement(
        store_with(obligation, receipt),
        obligation=obligation,
        scope=N_A,
        now=NOW,
        policy=policy,
    )
    assert Finding(ProfileFinding.INVALID_V_TYPE, claim_id(receipt)) in result.findings


def test_grant_membership_foreign_scope() -> None:
    """grant-membership mit fremdem N: SCOPE_MISMATCH (03 §4, D287)."""
    alice, bob = fresh_alice(), fresh_bob()
    grant = alice.claim(
        p=nuc(N_A, "grant-membership"),
        J=(1, bob.pub),
        t=1,
        N=b"\xff" * 32,
    )
    result = membership(
        store_with(grant),
        subject=BOB.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({ALICE.pub}),
    )
    assert Finding(ProfileFinding.SCOPE_MISMATCH, claim_id(grant)) in result.findings


def test_verdict_unknown_accusation() -> None:
    """Verdikt auf unbekannten Claim: UNKNOWN_ACCUSATION mit Subjekt h (03 §2.4.2, D287)."""
    alice = fresh_alice()
    h = b"\x11" * 32
    verdict = alice.claim(p=nuc(N_A, "verdict"), J=(2, h), t=1, N=N_A)
    result = verdict_status(
        store_with(verdict),
        verdict=verdict,
        scope=N_A,
        arbitrators=frozenset({ALICE.pub}),
        now=NOW,
    )
    assert Finding(ProfileFinding.UNKNOWN_ACCUSATION, h) in result.findings
    assert Finding(ProfileFinding.UNKNOWN_ACCUSATION, claim_id(verdict)) not in result.findings
