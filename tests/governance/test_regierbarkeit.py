"""Bedingung 6 — die Zielverfassung muss regieren können (04-governance.md §4.1, D200)."""

from __future__ import annotations

import pytest

from symbolon.atom import claim_id
from symbolon.governance import verify_ratification
from symbolon.governance.findings import GovernanceFinding
from symbolon.governance.objects import Proposal
from symbolon.governance.tally import TallyState
from symbolon.policy import constitution_hash
from tests.helpers import store_with

from .fixtures import C1, C2, EPOCH_1, NOW, _tally, fresh_p1, policy_of, ratify_claim, vote


def _welt(ziel: dict):
    alice, bob, carol, dave = fresh_p1()
    proposal = Proposal(
        scope=EPOCH_1.scope,
        predecessor=EPOCH_1.epoch_id,
        constitution_hash=constitution_hash(ziel),
    )
    votes = [
        vote(alice, proposal, choice=1, t=1),
        vote(bob, proposal, choice=1, t=1),
        vote(carol, proposal, choice=1, t=1),
        vote(dave, proposal, choice=1, t=1),
    ]
    store = store_with(*votes)
    tally = _tally(store, proposal=proposal, constitution=C1, target=ziel)
    r = ratify_claim(alice, proposal, witnesses=[claim_id(v) for v in votes], t=10)
    store.add(r)
    result = verify_ratification(
        store,
        ratify=r,
        epoch=EPOCH_1,
        proposal=proposal,
        tally=tally,
        target_constitution_obj=ziel,
        now=NOW,
        policy=policy_of(C1),
    )
    return proposal, tally, result


def _assert_blocked(ziel: dict, kind: GovernanceFinding) -> None:
    proposal, tally, result = _welt(ziel)
    assert tally.state is TallyState.PASSED
    assert result.next_epoch is None
    assert len(result.findings) == 1
    assert result.findings[0].kind == kind
    assert result.findings[0].subject == proposal.constitution_hash
    assert result.findings[0].subject != EPOCH_1.constitution_hash


def test_target_without_participants() -> None:
    ziel = dict(C2)
    del ziel["participants"]
    _assert_blocked(ziel, GovernanceFinding.PARTICIPANTS_UNDECLARED)


def test_target_with_malformed_participants() -> None:
    ziel = dict(C2)
    ziel["participants"] = sorted(C2["participants"], reverse=True)
    _assert_blocked(ziel, GovernanceFinding.MALFORMED_PARTICIPANTS)


def test_target_with_revocable_vote() -> None:
    ziel = dict(C2)
    ziel["irrevocable_predicates"] = [
        p for p in C2["irrevocable_predicates"] if p != "vote@1"
    ]
    _assert_blocked(ziel, GovernanceFinding.VOTE_REVOCABLE)


def test_target_with_revocable_ratify() -> None:
    ziel = dict(C2)
    ziel["irrevocable_predicates"] = [
        p for p in C2["irrevocable_predicates"] if p != "ratify@1"
    ]
    _assert_blocked(ziel, GovernanceFinding.RATIFY_REVOCABLE)


def test_mismatched_target_object_raises() -> None:
    alice, bob, carol, dave = fresh_p1()
    ziel = C2
    proposal = Proposal(
        scope=EPOCH_1.scope,
        predecessor=EPOCH_1.epoch_id,
        constitution_hash=constitution_hash(ziel),
    )
    votes = [
        vote(alice, proposal, choice=1, t=1),
        vote(bob, proposal, choice=1, t=1),
        vote(carol, proposal, choice=1, t=1),
        vote(dave, proposal, choice=1, t=1),
    ]
    store = store_with(*votes)
    tally = _tally(store, proposal=proposal, constitution=C1, target=ziel)
    r = ratify_claim(alice, proposal, witnesses=[claim_id(v) for v in votes], t=10)
    store.add(r)
    assert tally.state is TallyState.PASSED
    with pytest.raises(ValueError):
        verify_ratification(
            store,
            ratify=r,
            epoch=EPOCH_1,
            proposal=proposal,
            tally=tally,
            target_constitution_obj=C1,
            now=NOW,
            policy=policy_of(C1),
        )


def test_mismatched_target_with_unsupported_ratify() -> None:
    alice, bob, carol, dave = fresh_p1()
    ziel = C2
    proposal = Proposal(
        scope=EPOCH_1.scope,
        predecessor=EPOCH_1.epoch_id,
        constitution_hash=constitution_hash(ziel),
    )
    votes = [
        vote(alice, proposal, choice=1, t=1),
        vote(bob, proposal, choice=1, t=1),
        vote(carol, proposal, choice=1, t=1),
        vote(dave, proposal, choice=1, t=1),
    ]
    store = store_with(*votes)
    tally = _tally(store, proposal=proposal, constitution=C1, target=ziel)
    r = ratify_claim(alice, proposal, witnesses=[], t=10)
    store.add(r)
    assert tally.state is TallyState.PASSED
    with pytest.raises(ValueError):
        verify_ratification(
            store,
            ratify=r,
            epoch=EPOCH_1,
            proposal=proposal,
            tally=tally,
            target_constitution_obj=C1,
            now=NOW,
            policy=policy_of(C1),
        )
