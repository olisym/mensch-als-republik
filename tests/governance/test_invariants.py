"""INV-04.1 … INV-04.8 — Governance-Invarianten (04-golden-anchors.md §8)."""

from __future__ import annotations

from symbolon.atom import claim_id
from symbolon.governance import verify_ratification
from symbolon.governance.tally import TallyState
from tests.helpers import store_with

from .fixtures import (
    C1,
    C1_AMEND,
    C2,
    C3,
    EPOCH_1,
    EPOCH_2,
    NOW,
    PROPOSAL_1,
    PROPOSAL_2,
    PROPOSAL_AMEND_E1,
    _tally,
    fresh_p1,
    fresh_p2,
    policy_of,
    propose_claim,
    ratify_claim,
    vote,
)


def test_INV_04_1_absorbing() -> None:
    alice, bob, carol, dave = fresh_p1()
    passed_store = store_with(
        vote(alice, PROPOSAL_AMEND_E1, choice=1, t=1),
        vote(bob, PROPOSAL_AMEND_E1, choice=1, t=1),
        vote(carol, PROPOSAL_AMEND_E1, choice=1, t=1),
        vote(dave, PROPOSAL_AMEND_E1, choice=1, t=1),
    )
    passed = _tally(passed_store, proposal=PROPOSAL_AMEND_E1, target=C1_AMEND)
    assert passed.state is TallyState.PASSED
    from tests.helpers import Identity

    extra = vote(Identity("extra-inv1"), PROPOSAL_AMEND_E1, choice=1, t=1)
    passed_store.add(extra)
    still = _tally(passed_store, proposal=PROPOSAL_AMEND_E1, target=C1_AMEND)
    assert still.state is TallyState.PASSED

    alice, bob, carol, _dave = fresh_p1()
    failed_store = store_with(
        vote(alice, PROPOSAL_AMEND_E1, choice=0, t=1),
        vote(bob, PROPOSAL_AMEND_E1, choice=0, t=1),
    )
    failed = _tally(failed_store, proposal=PROPOSAL_AMEND_E1, target=C1_AMEND)
    assert failed.state is TallyState.FAILED
    failed_store.add(vote(carol, PROPOSAL_AMEND_E1, choice=1, t=2))
    still_failed = _tally(failed_store, proposal=PROPOSAL_AMEND_E1, target=C1_AMEND)
    assert still_failed.state is TallyState.FAILED


def test_INV_04_3_partial_knowledge_never_passed() -> None:
    missing_old = _tally(
        store_with(), constitution=None, proposal=PROPOSAL_1, target=C2
    )
    assert missing_old.state is TallyState.UNEVALUABLE
    assert missing_old.state is not TallyState.PASSED
    missing_new = _tally(
        store_with(), constitution=C1, proposal=PROPOSAL_1, target=None
    )
    assert missing_new.state is TallyState.UNEVALUABLE
    assert missing_new.state is not TallyState.PASSED


def test_INV_04_4_same_epoch_id() -> None:
    alice, bob, carol, dave = fresh_p1()
    votes = [
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
        vote(carol, PROPOSAL_1, choice=1, t=1),
        vote(dave, PROPOSAL_1, choice=1, t=1),
    ]
    store = store_with(*votes)
    tally = _tally(store)
    yes = [claim_id(v) for v in votes]
    r1 = ratify_claim(alice, PROPOSAL_1, witnesses=yes[:3], t=10)
    r2 = ratify_claim(bob, PROPOSAL_1, witnesses=yes[1:], t=10)
    store.add(r1)
    store.add(r2)
    policy = policy_of(C1)
    a = verify_ratification(
        store, ratify=r1, epoch=EPOCH_1, proposal=PROPOSAL_1, tally=tally, target_constitution_obj=C2, now=NOW, policy=policy
    )
    b = verify_ratification(
        store, ratify=r2, epoch=EPOCH_1, proposal=PROPOSAL_1, tally=tally, target_constitution_obj=C2, now=NOW, policy=policy
    )
    assert a.next_epoch is not None and b.next_epoch is not None
    assert a.next_epoch.epoch_id == b.next_epoch.epoch_id


def test_INV_04_5_now_irrelevant() -> None:
    alice, bob, carol, _dave, _eve = fresh_p2()
    store = store_with(
        vote(alice, PROPOSAL_2, choice=1, t=1),
        vote(bob, PROPOSAL_2, choice=1, t=1),
        vote(carol, PROPOSAL_2, choice=1, t=1, t_exp=10**9),
    )
    a = _tally(store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3, now=1000)
    b = _tally(store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3, now=10**12)
    assert a == b


def test_INV_04_7_counting_set_monotonic() -> None:
    alice, bob, carol, dave, eve = fresh_p2()
    sequence = [
        vote(alice, PROPOSAL_2, choice=1, t=1),
        vote(bob, PROPOSAL_2, choice=0, t=1),
        vote(carol, PROPOSAL_2, choice=1, t=1),
        vote(dave, PROPOSAL_2, choice=1, t=1),
        vote(eve, PROPOSAL_2, choice=0, t=1),
        propose_claim(alice, PROPOSAL_2, t=2),
    ]
    store = store_with()
    seen: set[bytes] = set()
    for claim in sequence:
        store.add(claim)
        result = _tally(
            store, epoch=EPOCH_2, proposal=PROPOSAL_2, constitution=C2, target=C3
        )
        current = set(result.yes) | set(result.no)
        assert seen <= current
        seen = current


def test_INV_04_8_established_epoch_persists() -> None:
    alice, bob, carol, dave = fresh_p1()
    votes = [
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
        vote(carol, PROPOSAL_1, choice=1, t=1),
    ]
    store = store_with(*votes)
    tally = _tally(store)
    r = ratify_claim(alice, PROPOSAL_1, witnesses=[claim_id(v) for v in votes], t=10)
    store.add(r)
    policy = policy_of(C1)
    established = verify_ratification(
        store, ratify=r, epoch=EPOCH_1, proposal=PROPOSAL_1, tally=tally, target_constitution_obj=C2, now=NOW, policy=policy
    )
    assert established.next_epoch is not None
    extras = [
        alice.revoke(r, t=11),
        propose_claim(dave, PROPOSAL_1, t=12),
        vote(dave, PROPOSAL_1, choice=1, t=13),
    ]
    for claim in extras:
        store.add(claim)
        again = verify_ratification(
            store, ratify=r, epoch=EPOCH_1, proposal=PROPOSAL_1, tally=tally, target_constitution_obj=C2, now=NOW, policy=policy
        )
        assert again.next_epoch is not None
        assert again.next_epoch.epoch_id == established.next_epoch.epoch_id


def test_ratify_requires_passed_tally() -> None:
    alice, bob, _carol, _dave = fresh_p1()
    votes = [
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
    ]
    store = store_with(*votes)
    tally = _tally(store)
    assert tally.state is TallyState.PENDING
    r = ratify_claim(alice, PROPOSAL_1, witnesses=[claim_id(v) for v in votes], t=10)
    store.add(r)
    result = verify_ratification(
        store, ratify=r, epoch=EPOCH_1, proposal=PROPOSAL_1, tally=tally, target_constitution_obj=C2, now=NOW, policy=policy_of(C1)
    )
    assert result.next_epoch is None
