"""MB-1 … MB-9 — Mitgliedschaft (03-golden-anchors.md §7)."""

from __future__ import annotations

from symbolon.atom import claim_id
from symbolon.profiles import (
    Finding,
    MembershipState,
    ProfileFinding,
    membership,
)

from .fixtures import (
    ALICE,
    BOB,
    CONSTITUTION_HASH_A,
    CONSTITUTION_HASH_C,
    N_A,
    N_B,
    NOW,
    fresh_alice,
    fresh_bob,
    fresh_carol,
    nuc,
)
from tests.helpers import store_with


def test_MB_1() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    accept = bob.claim(
        p=nuc(N_A, "accept-rules"), J=(3, CONSTITUTION_HASH_A), t=1, N=N_A
    )
    grant = alice.claim(
        p=nuc(N_A, "grant-membership"), J=(1, bob.pub), t=2, N=N_A
    )
    result = membership(
        store_with(accept, grant),
        subject=BOB.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({ALICE.pub}),
    )
    assert result.state == MembershipState.MEMBER
    assert result.accept_claim_id == claim_id(accept)
    assert result.grant_claim_id == claim_id(grant)
    assert result.findings == ()


def test_MB_2() -> None:
    bob = fresh_bob()
    accept = bob.claim(
        p=nuc(N_A, "accept-rules"), J=(3, CONSTITUTION_HASH_A), t=1, N=N_A
    )
    result = membership(
        store_with(accept),
        subject=BOB.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({ALICE.pub}),
    )
    assert result.state == MembershipState.APPLICANT
    assert result.accept_claim_id == claim_id(accept)
    assert result.grant_claim_id is None
    assert result.findings == ()


def test_MB_3() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    grant = alice.claim(
        p=nuc(N_A, "grant-membership"), J=(1, bob.pub), t=1, N=N_A
    )
    result = membership(
        store_with(grant),
        subject=BOB.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({ALICE.pub}),
    )
    assert result.state == MembershipState.GRANT_ONLY
    assert result.accept_claim_id is None
    assert result.grant_claim_id == claim_id(grant)
    assert result.findings == ()


def test_MB_4() -> None:
    result = membership(
        store_with(),
        subject=BOB.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({ALICE.pub}),
    )
    assert result.state == MembershipState.NONE
    assert result.accept_claim_id is None
    assert result.grant_claim_id is None
    assert result.findings == ()


def test_MB_5() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    accept = bob.claim(
        p=nuc(N_A, "accept-rules"), J=(3, CONSTITUTION_HASH_A), t=1, N=N_A
    )
    rev = bob.revoke(accept, t=2)
    grant = alice.claim(
        p=nuc(N_A, "grant-membership"), J=(1, bob.pub), t=3, N=N_A
    )
    result = membership(
        store_with(accept, rev, grant),
        subject=BOB.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({ALICE.pub}),
    )
    assert result.state == MembershipState.GRANT_ONLY
    assert result.accept_claim_id is None
    assert result.grant_claim_id == claim_id(grant)
    assert result.findings == ()


def test_MB_6() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    grant = alice.claim(
        p=nuc(N_A, "grant-membership"), J=(1, bob.pub), t=1, N=N_A
    )
    rev = alice.revoke(grant, t=2)
    accept = bob.claim(
        p=nuc(N_A, "accept-rules"), J=(3, CONSTITUTION_HASH_A), t=3, N=N_A
    )
    result = membership(
        store_with(grant, rev, accept),
        subject=BOB.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({ALICE.pub}),
    )
    assert result.state == MembershipState.APPLICANT
    assert result.accept_claim_id == claim_id(accept)
    assert result.grant_claim_id is None
    assert result.findings == ()


def test_MB_7() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    accept = bob.claim(
        p=nuc(N_A, "accept-rules"), J=(3, CONSTITUTION_HASH_C), t=1, N=N_A
    )
    grant = alice.claim(
        p=nuc(N_A, "grant-membership"), J=(1, bob.pub), t=2, N=N_A
    )
    result = membership(
        store_with(accept, grant),
        subject=BOB.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({ALICE.pub}),
    )
    assert result.state == MembershipState.GRANT_ONLY
    assert result.accept_claim_id is None
    assert result.grant_claim_id == claim_id(grant)
    assert result.findings == (
        Finding(ProfileFinding.CONSTITUTION_VERSION_MISMATCH, claim_id(accept)),
    )


def test_MB_8() -> None:
    bob, carol = fresh_bob(), fresh_carol()
    accept = bob.claim(
        p=nuc(N_A, "accept-rules"), J=(3, CONSTITUTION_HASH_A), t=1, N=N_A
    )
    grant = carol.claim(
        p=nuc(N_A, "grant-membership"), J=(1, bob.pub), t=2, N=N_A
    )
    result = membership(
        store_with(accept, grant),
        subject=BOB.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({ALICE.pub}),
    )
    assert result.state == MembershipState.APPLICANT
    assert result.accept_claim_id == claim_id(accept)
    assert result.grant_claim_id is None
    assert result.findings == (
        Finding(ProfileFinding.UNAUTHORIZED_GRANT_AUTHOR, claim_id(grant)),
    )


def test_MB_9() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    accept = bob.claim(
        p=nuc(N_B, "accept-rules"), J=(3, CONSTITUTION_HASH_A), t=1, N=N_B
    )
    grant = alice.claim(
        p=nuc(N_A, "grant-membership"), J=(1, bob.pub), t=2, N=N_A
    )
    result = membership(
        store_with(accept, grant),
        subject=BOB.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({ALICE.pub}),
    )
    assert result.state == MembershipState.GRANT_ONLY
    assert result.accept_claim_id is None
    assert result.grant_claim_id == claim_id(grant)
    assert result.findings == (
        Finding(ProfileFinding.SCOPE_MISMATCH, claim_id(accept)),
    )
