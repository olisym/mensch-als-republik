"""VS-1 … VS-11 — Verdikt-Status (03-golden-anchors.md §9)."""

from __future__ import annotations

from mensch_als_republik.atom import claim_id
from mensch_als_republik.profiles import (
    Finding,
    ProfileFinding,
    VerdictStatus,
    verdict_status,
)
from tests.helpers import store_with

from .fixtures import (
    ALICE,
    BOB,
    N_A,
    N_B,
    NOW,
    fresh_alice,
    fresh_bob,
    fresh_carol,
    nuc,
)

ARBITRATORS = frozenset({ALICE.pub, BOB.pub})


def test_VS_1() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    accusation = alice.claim(
        p=nuc(N_B, "accusation"), J=(1, bob.pub), t=1, N=N_B
    )
    verdict = alice.claim(
        p=nuc(N_B, "verdict"), J=(2, claim_id(accusation)), t=2, N=N_B
    )
    result = verdict_status(
        store_with(accusation, verdict),
        verdict=verdict,
        scope=N_B,
        arbitrators=ARBITRATORS,
        now=NOW,
    )
    assert result.status == VerdictStatus.BINDING
    assert result.findings == ()


def test_VS_2() -> None:
    alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()
    accusation = alice.claim(
        p=nuc(N_B, "accusation"), J=(1, bob.pub), t=1, N=N_B
    )
    verdict = carol.claim(
        p=nuc(N_B, "verdict"), J=(2, claim_id(accusation)), t=2, N=N_B
    )
    result = verdict_status(
        store_with(accusation, verdict),
        verdict=verdict,
        scope=N_B,
        arbitrators=ARBITRATORS,
        now=NOW,
    )
    assert result.status == VerdictStatus.ATTRIBUTED_OPINION
    assert result.findings == ()


def test_VS_3() -> None:
    alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()
    accusation = alice.claim(
        p=nuc(N_B, "accusation"), J=(1, bob.pub), t=1, N=N_B
    )
    sub_a = alice.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=2, N=N_B
    )
    sub_b = bob.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=3, N=N_B
    )
    verdict = carol.claim(
        p=nuc(N_B, "verdict"), J=(2, claim_id(accusation)), t=4, N=N_B
    )
    result = verdict_status(
        store_with(accusation, sub_a, sub_b, verdict),
        verdict=verdict,
        scope=N_B,
        arbitrators=ARBITRATORS,
        now=NOW,
    )
    assert result.status == VerdictStatus.BINDING
    assert result.findings == ()


def test_VS_4() -> None:
    alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()
    X = bob.claim(p=nuc(N_B, "vouch"), J=(1, alice.pub), t=1, N=N_B)
    accusation = alice.claim(
        p=nuc(N_B, "accusation"), J=(2, claim_id(X)), t=2, N=N_B
    )
    sub_a = alice.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=3, N=N_B
    )
    sub_b = bob.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=4, N=N_B
    )
    verdict = carol.claim(
        p=nuc(N_B, "verdict"), J=(2, claim_id(accusation)), t=5, N=N_B
    )
    result = verdict_status(
        store_with(X, accusation, sub_a, sub_b, verdict),
        verdict=verdict,
        scope=N_B,
        arbitrators=ARBITRATORS,
        now=NOW,
    )
    assert result.status == VerdictStatus.BINDING
    assert result.findings == ()


def test_VS_5() -> None:
    alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()
    accusation = alice.claim(
        p=nuc(N_B, "accusation"), J=(1, bob.pub), t=1, N=N_B
    )
    sub_a = alice.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=2, N=N_B
    )
    verdict = carol.claim(
        p=nuc(N_B, "verdict"), J=(2, claim_id(accusation)), t=3, N=N_B
    )
    result = verdict_status(
        store_with(accusation, sub_a, verdict),
        verdict=verdict,
        scope=N_B,
        arbitrators=ARBITRATORS,
        now=NOW,
    )
    assert result.status == VerdictStatus.ATTRIBUTED_OPINION
    assert result.findings == ()


def test_VS_6() -> None:
    alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()
    accusation = alice.claim(
        p=nuc(N_B, "accusation"), J=(1, bob.pub), t=1, N=N_B
    )
    sub_a = alice.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=2, N=N_B
    )
    sub_b = bob.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=3, N=N_B
    )
    rev = bob.revoke(sub_b, t=4)
    verdict = carol.claim(
        p=nuc(N_B, "verdict"), J=(2, claim_id(accusation)), t=5, N=N_B
    )
    result = verdict_status(
        store_with(accusation, sub_a, sub_b, rev, verdict),
        verdict=verdict,
        scope=N_B,
        arbitrators=ARBITRATORS,
        now=NOW,
    )
    assert result.status == VerdictStatus.ATTRIBUTED_OPINION
    assert result.findings == ()


def test_VS_7() -> None:
    alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()
    accusation = alice.claim(
        p=nuc(N_B, "accusation"), J=(1, bob.pub), t=1, N=N_B
    )
    sub_a = alice.claim(
        p=nuc(N_A, "submit-arbitration"), J=(1, carol.pub), t=2, N=N_A
    )
    sub_b = bob.claim(
        p=nuc(N_A, "submit-arbitration"), J=(1, carol.pub), t=3, N=N_A
    )
    verdict = carol.claim(
        p=nuc(N_B, "verdict"), J=(2, claim_id(accusation)), t=4, N=N_B
    )
    result = verdict_status(
        store_with(accusation, sub_a, sub_b, verdict),
        verdict=verdict,
        scope=N_B,
        arbitrators=ARBITRATORS,
        now=NOW,
    )
    assert result.status == VerdictStatus.ATTRIBUTED_OPINION
    assert result.findings == tuple(
        sorted(
            {
                Finding(ProfileFinding.SCOPE_MISMATCH, claim_id(sub_a)),
                Finding(ProfileFinding.SCOPE_MISMATCH, claim_id(sub_b)),
            }
        )
    )


def test_VS_8() -> None:
    alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()
    unknown = bytes(32)
    accusation = alice.claim(
        p=nuc(N_B, "accusation"), J=(2, unknown), t=1, N=N_B
    )
    sub_a = alice.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=2, N=N_B
    )
    sub_b = bob.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=3, N=N_B
    )
    verdict = carol.claim(
        p=nuc(N_B, "verdict"), J=(2, claim_id(accusation)), t=4, N=N_B
    )
    result = verdict_status(
        store_with(accusation, sub_a, sub_b, verdict),
        verdict=verdict,
        scope=N_B,
        arbitrators=ARBITRATORS,
        now=NOW,
    )
    assert result.status == VerdictStatus.ATTRIBUTED_OPINION
    assert result.findings == (
        Finding(ProfileFinding.UNRESOLVED_ACCUSED, unknown),
    )


def test_VS_9() -> None:
    alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()
    accusation = alice.claim(
        p=nuc(N_B, "accusation"), J=(1, bob.pub), t=1, N=N_B
    )
    sub_a = alice.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=2, N=N_B
    )
    sub_b = bob.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=3, N=N_B
    )
    verdict = carol.claim(
        p=nuc(N_B, "verdict"), J=(2, claim_id(accusation)), t=4, N=N_B
    )
    rev = carol.revoke(verdict, t=5)
    result = verdict_status(
        store_with(accusation, sub_a, sub_b, verdict, rev),
        verdict=verdict,
        scope=N_B,
        arbitrators=ARBITRATORS,
        now=NOW,
    )
    assert result.status == VerdictStatus.ATTRIBUTED_OPINION
    assert result.findings == (
        Finding(ProfileFinding.INACTIVE_VERDICT, claim_id(verdict)),
    )


def test_VS_10() -> None:
    alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()
    accusation = alice.claim(
        p=nuc(N_B, "accusation"), J=(1, bob.pub), t=1, N=N_B
    )
    rev_acc = alice.revoke(accusation, t=2)
    sub_a = alice.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=3, N=N_B
    )
    sub_b = bob.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=4, N=N_B
    )
    verdict = carol.claim(
        p=nuc(N_B, "verdict"), J=(2, claim_id(accusation)), t=5, N=N_B
    )
    result = verdict_status(
        store_with(accusation, rev_acc, sub_a, sub_b, verdict),
        verdict=verdict,
        scope=N_B,
        arbitrators=ARBITRATORS,
        now=NOW,
    )
    assert result.status == VerdictStatus.BINDING
    assert result.findings == ()


def test_VS_11() -> None:
    alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()
    accusation = alice.claim(
        p=nuc(N_B, "accusation"), J=(1, bob.pub), t=1, N=N_B
    )
    sub_a = alice.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=2, N=N_B
    )
    sub_b = bob.claim(
        p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=3, N=N_B
    )
    verdict = carol.claim(
        p=nuc(N_B, "verdict"), J=(1, bob.pub), t=4, N=N_B
    )
    result = verdict_status(
        store_with(accusation, sub_a, sub_b, verdict),
        verdict=verdict,
        scope=N_B,
        arbitrators=ARBITRATORS,
        now=NOW,
    )
    assert result.status == VerdictStatus.ATTRIBUTED_OPINION
    assert result.findings == (
        Finding(ProfileFinding.UNKNOWN_ACCUSATION, claim_id(verdict)),
    )
