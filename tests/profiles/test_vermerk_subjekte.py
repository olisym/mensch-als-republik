"""Subjekte der Verdiktvermerke (03-profiles.md §2.4.4, D207)."""

from __future__ import annotations

from symbolon.atom import claim_id
from symbolon.profiles import (
    Finding,
    ProfileFinding,
    VerdictStatus,
    verdict_status,
)
from tests.helpers import store_with

from .fixtures import (
    ALICE,
    BOB,
    N_B,
    NOW,
    fresh_alice,
    fresh_bob,
    fresh_carol,
    nuc,
)

ARBITRATORS = frozenset({ALICE.pub, BOB.pub})


def test_accusation_j_neither_identity_nor_claim_ref() -> None:
    """accusation.J.tag ist weder identity noch claim-ref: UNRESOLVED_ACCUSED auf die Anklage (03 §2.4.4, D207)."""
    alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()
    acc = alice.claim(p=nuc(N_B, "accusation"), J=(3, bytes(32)), t=1, N=N_B)
    sub_a = alice.claim(p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=2, N=N_B)
    sub_b = bob.claim(p=nuc(N_B, "submit-arbitration"), J=(1, carol.pub), t=3, N=N_B)
    verdict = carol.claim(p=nuc(N_B, "verdict"), J=(2, claim_id(acc)), t=4, N=N_B)
    result = verdict_status(
        store_with(acc, sub_a, sub_b, verdict),
        verdict=verdict,
        scope=N_B,
        arbitrators=ARBITRATORS,
        now=NOW,
    )
    assert result.status == VerdictStatus.ATTRIBUTED_OPINION
    assert result.findings == (
        Finding(ProfileFinding.UNRESOLVED_ACCUSED, claim_id(acc)),
    )
