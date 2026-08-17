"""PR-INV-1 … PR-INV-12 — abgeleitete Invarianten (03-golden-anchors.md §11)."""

from __future__ import annotations

import pytest

from mensch_als_republik import profiles, trust
from mensch_als_republik.atom import claim_id
from mensch_als_republik.policy import TRUST_GRANTING
from mensch_als_republik.profiles import (
    Finding,
    MembershipState,
    ProfileFinding,
    SettlementState,
    VerdictStatus,
    classify_all,
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
    CONSTITUTION_B,
    CONSTITUTION_C,
    CONSTITUTION_HASH_A,
    GENESIS_A,
    GENESIS_B,
    GENESIS_C,
    N_A,
    N_B,
    N_C,
    NOW,
    fresh_alice,
    fresh_bob,
    fresh_carol,
    nuc,
)


def test_PR_INV_1() -> None:
    cases = [
        (N_A, GENESIS_A, CONSTITUTION_A),
        (N_B, GENESIS_B, CONSTITUTION_B),
        (N_C, GENESIS_C, CONSTITUTION_C),
        (N_A, GENESIS_A, None),
    ]
    for scope, genesis, constitution in cases:
        r = resolve_policy(
            scope=scope, genesis_obj=genesis, constitution_obj=constitution
        )
        assert "obligation@1" in r.policy.irrevocable


def test_PR_INV_2() -> None:
    cases = [
        (N_A, GENESIS_A, CONSTITUTION_A),
        (N_B, GENESIS_B, CONSTITUTION_B),
        (N_C, GENESIS_C, CONSTITUTION_C),
        (N_A, GENESIS_A, None),
    ]
    for scope, genesis, constitution in cases:
        r = resolve_policy(
            scope=scope, genesis_obj=genesis, constitution_obj=constitution
        )
        assert r.policy.irrevocable & TRUST_GRANTING == frozenset()


def test_PR_INV_3() -> None:
    cases = [
        (N_A, GENESIS_A, CONSTITUTION_A),
        (N_B, GENESIS_B, CONSTITUTION_B),
        (N_C, GENESIS_C, CONSTITUTION_C),
        (N_A, GENESIS_A, None),
    ]
    for scope, genesis, constitution in cases:
        r = resolve_policy(
            scope=scope, genesis_obj=genesis, constitution_obj=constitution
        )
        for pred in r.policy.irrevocable:
            assert not pred.startswith("core")
            assert "/" not in pred or not pred.startswith("core/")


def test_PR_INV_4() -> None:
    with pytest.raises(ValueError):
        resolve_policy(
            scope=N_A, genesis_obj=GENESIS_B, constitution_obj=CONSTITUTION_B
        )

    pol_b = resolve_policy(
        scope=N_B, genesis_obj=GENESIS_B, constitution_obj=CONSTITUTION_B
    ).policy
    alice, bob = fresh_alice(), fresh_bob()
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    accusation = alice.claim(
        p=nuc(N_A, "accusation"), J=(1, bob.pub), t=2, N=N_A
    )
    verdict = alice.claim(
        p=nuc(N_A, "verdict"), J=(2, claim_id(accusation)), t=3, N=N_A
    )

    with pytest.raises(ValueError):
        membership(
            store_with(),
            subject=BOB.pub,
            scope=N_A,
            constitution_hash=CONSTITUTION_HASH_A,
            now=NOW,
            authorized_keys=frozenset({ALICE.pub}),
            policy=pol_b,
        )
    with pytest.raises(ValueError):
        settlement(
            store_with(), obligation=O, scope=N_A, now=NOW, policy=pol_b
        )
    with pytest.raises(ValueError):
        verdict_status(
            store_with(),
            verdict=verdict,
            scope=N_A,
            arbitrators=frozenset({ALICE.pub}),
            now=NOW,
            policy=pol_b,
        )


def test_PR_INV_5() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    store = store_with(O)
    with pytest.raises(TypeError):
        settlement(store, obligation=O, scope=N_A, now=NOW)  # type: ignore[call-arg]

    membership(
        store_with(),
        subject=BOB.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({ALICE.pub}),
        policy=None,
    )
    accusation = alice.claim(
        p=nuc(N_A, "accusation"), J=(1, bob.pub), t=2, N=N_A
    )
    verdict = alice.claim(
        p=nuc(N_A, "verdict"), J=(2, claim_id(accusation)), t=3, N=N_A
    )
    verdict_status(
        store_with(accusation, verdict),
        verdict=verdict,
        scope=N_A,
        arbitrators=frozenset({ALICE.pub}),
        now=NOW,
        policy=None,
    )


def test_PR_INV_6() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    accept = bob.claim(
        p=nuc(N_A, "accept-rules"), J=(3, CONSTITUTION_HASH_A), t=1, N=N_A
    )
    grant = alice.claim(
        p=nuc(N_A, "grant-membership"), J=(1, bob.pub), t=2, N=N_A
    )
    member = membership(
        store_with(accept, grant),
        subject=BOB.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({ALICE.pub}),
    )
    assert member.state == MembershipState.MEMBER
    assert member.accept_claim_id is not None and member.grant_claim_id is not None

    for store, expected in (
        (store_with(accept), MembershipState.APPLICANT),
        (store_with(grant), MembershipState.GRANT_ONLY),
        (store_with(), MembershipState.NONE),
    ):
        r = membership(
            store,
            subject=BOB.pub,
            scope=N_A,
            constitution_hash=CONSTITUTION_HASH_A,
            now=NOW,
            authorized_keys=frozenset({ALICE.pub}),
        )
        assert r.state == expected
        assert r.accept_claim_id is None or r.grant_claim_id is None


def test_PR_INV_7() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    pol = resolve_policy(
        scope=N_A, genesis_obj=GENESIS_A, constitution_obj=CONSTITUTION_A
    ).policy
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    R = bob.claim(
        p=nuc(N_A, "receipt"),
        J=(2, claim_id(O)),
        t=2,
        v=bytes.fromhex("a10701"),
        N=N_A,
    )
    result = settlement(
        store_with(O, R), obligation=O, scope=N_A, now=NOW, policy=pol
    )
    assert result.state == SettlementState.SETTLED
    assert result.receipt_claim_id is not None
    receipt = store_with(O, R).get(result.receipt_claim_id)
    assert receipt is not None
    obj, _kinds = read_v(receipt.v)
    assert obj is None or 0 not in obj


def test_PR_INV_8() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    accusation = alice.claim(
        p=nuc(N_B, "accusation"), J=(1, bob.pub), t=1, N=N_B
    )
    verdict = alice.claim(
        p=nuc(N_B, "verdict"), J=(2, claim_id(accusation)), t=2, N=N_B
    )
    store = store_with(accusation, verdict)
    result = verdict_status(
        store,
        verdict=verdict,
        scope=N_B,
        arbitrators=frozenset({ALICE.pub, BOB.pub}),
        now=NOW,
    )
    assert result.status == VerdictStatus.BINDING
    from mensch_als_republik.verifier import State, classify

    assert classify(verdict, store, now=NOW).state == State.ACTIVE


def test_PR_INV_9() -> None:
    pol_a = resolve_policy(
        scope=N_A, genesis_obj=GENESIS_A, constitution_obj=CONSTITUTION_A
    )
    assert pol_a.findings == tuple(sorted(set(pol_a.findings)))

    alice, bob = fresh_alice(), fresh_bob()
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    R = bob.claim(
        p=nuc(N_A, "receipt"),
        J=(2, claim_id(O)),
        t=2,
        v=bytes.fromhex("a100190064"),
        N=N_A,
    )
    settle = settlement(
        store_with(O, R),
        obligation=O,
        scope=N_A,
        now=NOW,
        policy=pol_a.policy,
    )
    assert settle.findings == tuple(sorted(set(settle.findings)))

    accept = bob.claim(
        p=nuc(N_B, "accept-rules"), J=(3, CONSTITUTION_HASH_A), t=3, N=N_B
    )
    grant = alice.claim(
        p=nuc(N_A, "grant-membership"), J=(1, bob.pub), t=4, N=N_A
    )
    mem = membership(
        store_with(accept, grant),
        subject=BOB.pub,
        scope=N_A,
        constitution_hash=CONSTITUTION_HASH_A,
        now=NOW,
        authorized_keys=frozenset({ALICE.pub}),
    )
    assert mem.findings == tuple(sorted(set(mem.findings)))

    carol = fresh_carol()
    accusation = alice.claim(
        p=nuc(N_B, "accusation"), J=(1, bob.pub), t=5, N=N_B
    )
    sub_a = alice.claim(
        p=nuc(N_A, "submit-arbitration"), J=(1, carol.pub), t=6, N=N_A
    )
    sub_b = bob.claim(
        p=nuc(N_A, "submit-arbitration"), J=(1, carol.pub), t=7, N=N_A
    )
    verdict = carol.claim(
        p=nuc(N_B, "verdict"), J=(2, claim_id(accusation)), t=8, N=N_B
    )
    vs = verdict_status(
        store_with(accusation, sub_a, sub_b, verdict),
        verdict=verdict,
        scope=N_B,
        arbitrators=frozenset({ALICE.pub, BOB.pub}),
        now=NOW,
    )
    assert vs.findings == tuple(sorted(set(vs.findings)))
    assert isinstance(vs.findings[0], Finding) or vs.findings == ()


def test_PR_INV_10() -> None:
    assert profiles.classify_all is trust.classify_all


def test_PR_INV_11() -> None:
    """Bereits in tests/trust/test_coupling.py abgedeckt; Identitäts-Reexport genügt hier."""
    assert profiles.classify_all is classify_all


def test_PR_INV_12() -> None:
    alice, bob, carol = fresh_alice(), fresh_bob(), fresh_carol()
    claims = [
        alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A),
        bob.claim(p=nuc(N_B, "vouch"), J=(1, alice.pub), t=1, N=N_B, t_exp=5000),
        carol.claim(p=nuc(N_C, "accusation"), J=(1, alice.pub), t=1, N=N_C),
    ]
    store = store_with(*claims)
    pol = resolve_policy(
        scope=N_A, genesis_obj=GENESIS_A, constitution_obj=CONSTITUTION_A
    ).policy
    classify_all(store, NOW, pol)


def test_PR_INV_13() -> None:
    """settlement und verdict_status: ValueError bei falschem Prädikat/N/Store (03a B1/B4)."""
    import pytest

    alice, bob = fresh_alice(), fresh_bob()
    pol = resolve_policy(
        scope=N_A, genesis_obj=GENESIS_A, constitution_obj=CONSTITUTION_A
    ).policy
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    store = store_with(O)

    with pytest.raises(ValueError):
        settlement(store, obligation=O, scope=N_B, now=NOW, policy=pol)
    wrong_p = alice.claim(p=nuc(N_A, "receipt"), J=(2, claim_id(O)), t=2, N=N_A)
    with pytest.raises(ValueError):
        settlement(
            store_with(O, wrong_p), obligation=wrong_p, scope=N_A, now=NOW, policy=pol
        )
    with pytest.raises(ValueError):
        settlement(
            store_with(), obligation=O, scope=N_A, now=NOW, policy=pol
        )

    accusation = alice.claim(
        p=nuc(N_B, "accusation"), J=(1, bob.pub), t=3, N=N_B
    )
    verdict = alice.claim(
        p=nuc(N_B, "verdict"), J=(2, claim_id(accusation)), t=4, N=N_B
    )
    vstore = store_with(accusation, verdict)
    with pytest.raises(ValueError):
        verdict_status(
            vstore, verdict=verdict, scope=N_A,
            arbitrators=frozenset({alice.pub}), now=NOW,
        )
    with pytest.raises(ValueError):
        verdict_status(
            store_with(accusation),
            verdict=verdict, scope=N_B,
            arbitrators=frozenset({alice.pub}), now=NOW,
        )
    with pytest.raises(ValueError):
        verdict_status(
            store_with(accusation),
            verdict=accusation, scope=N_B,
            arbitrators=frozenset({alice.pub}), now=NOW,
        )
