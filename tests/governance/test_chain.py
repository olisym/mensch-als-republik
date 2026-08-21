"""Epochenkette — resolve_epoch (04-governance.md §4.5, D174, D175)."""

from __future__ import annotations

import pytest

from mensch_als_republik.atom import claim_id
from mensch_als_republik.governance import (
    Finding,
    GovernanceFinding,
    resolve_epoch,
)
from mensch_als_republik.governance.tally import TallyState
from tests.helpers import store_with

from .fixtures import (
    C1,
    C2,
    C3,
    CONSTITUTION_HASH_1,
    CONSTITUTION_HASH_2,
    CONSTITUTION_HASH_3,
    EPOCH_2,
    EPOCH_3,
    GENESIS_D,
    N_D,
    NOW,
    PROPOSAL_1,
    PROPOSAL_2,
    PROPOSAL_ALT_A,
    STOCK_N,
    _tally,
    fresh_p2,
    ratify_claim,
    vote,
)


def _two_transitions(*, extra_epoch1_ratify: bool = False):
    alice, bob, carol, dave, eve = fresh_p2()
    v1 = [
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
        vote(carol, PROPOSAL_1, choice=1, t=1),
        vote(dave, PROPOSAL_1, choice=1, t=1),
    ]
    yes1 = [claim_id(v) for v in v1]
    r1 = ratify_claim(alice, PROPOSAL_1, witnesses=yes1[:3], t=10)
    claims = [*v1, r1]
    if extra_epoch1_ratify:
        claims.append(ratify_claim(bob, PROPOSAL_1, witnesses=[], t=11))
    v2 = [
        vote(alice, PROPOSAL_2, choice=1, t=20),
        vote(bob, PROPOSAL_2, choice=1, t=20),
        vote(carol, PROPOSAL_2, choice=1, t=20),
        vote(dave, PROPOSAL_2, choice=1, t=20),
        vote(eve, PROPOSAL_2, choice=1, t=20),
    ]
    yes2 = [claim_id(v) for v in v2]
    r2 = ratify_claim(alice, PROPOSAL_2, witnesses=yes2[:4], t=30)
    claims.extend([*v2, r2])
    return store_with(*claims)


def _resolve(
    store,
    *,
    constitutions: dict | None = None,
    proposals: dict | None = None,
    scope: bytes = N_D,
    genesis: dict = GENESIS_D,
):
    if constitutions is None:
        constitutions = {
            CONSTITUTION_HASH_1: C1,
            CONSTITUTION_HASH_2: C2,
            CONSTITUTION_HASH_3: C3,
        }
    if proposals is None:
        proposals = {
            PROPOSAL_1.proposal_hash: PROPOSAL_1,
            PROPOSAL_2.proposal_hash: PROPOSAL_2,
        }
    return resolve_epoch(
        store,
        scope=scope,
        genesis_obj=genesis,
        known_constitutions=constitutions,
        known_proposals=proposals,
        now=NOW,
    )


def test_chain_two_transitions() -> None:
    result = _resolve(_two_transitions())
    assert result.epoch.epoch_id == EPOCH_3.epoch_id
    assert result.constitution_obj == C3
    assert result.findings == ()


def test_chain_without_ratification_stays_at_epoch_1() -> None:
    alice, bob, carol, dave, _eve = fresh_p2()
    store = store_with(
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
        vote(carol, PROPOSAL_1, choice=1, t=1),
        vote(dave, PROPOSAL_1, choice=1, t=1),
    )
    result = _resolve(store)
    assert result.epoch.index == 1
    assert result.constitution_obj == C1
    assert result.findings == ()


def test_chain_missing_c3_still_reaches_epoch_3() -> None:
    result = _resolve(
        _two_transitions(),
        constitutions={
            CONSTITUTION_HASH_1: C1,
            CONSTITUTION_HASH_2: C2,
        },
    )
    assert result.epoch.epoch_id == EPOCH_3.epoch_id
    assert result.constitution_obj is None
    assert result.findings == ()


def test_chain_missing_proposal_2() -> None:
    result = _resolve(
        _two_transitions(),
        proposals={PROPOSAL_1.proposal_hash: PROPOSAL_1},
    )
    assert result.epoch.epoch_id == EPOCH_2.epoch_id
    assert result.findings == (
        Finding(
            GovernanceFinding.EPOCH_PROPOSAL_UNAVAILABLE,
            PROPOSAL_2.proposal_hash,
        ),
    )


def test_chain_miskeyed_c3_like_missing() -> None:
    result = _resolve(
        _two_transitions(),
        constitutions={
            CONSTITUTION_HASH_1: C1,
            CONSTITUTION_HASH_2: C3,
        },
    )
    assert result.epoch.epoch_id == EPOCH_3.epoch_id
    assert result.constitution_obj is None
    assert result.findings == ()


def test_chain_wrong_scope_raises() -> None:
    with pytest.raises(ValueError):
        _resolve(_two_transitions(), scope=STOCK_N)


def test_chain_stale_epoch_findings_absent() -> None:
    result = _resolve(_two_transitions(extra_epoch1_ratify=True))
    assert result.epoch.epoch_id == EPOCH_3.epoch_id
    assert result.findings == ()


def test_decide_miskeyed_proposal_is_unknown() -> None:
    alice, *_rest = fresh_p2()
    on_this = vote(alice, PROPOSAL_2, choice=1, t=1)
    other = vote(alice, PROPOSAL_ALT_A, choice=1, t=2)
    store = store_with(on_this, other)
    result = _tally(
        store,
        epoch=EPOCH_2,
        proposal=PROPOSAL_2,
        constitution=C2,
        target=C3,
        known={
            PROPOSAL_2.proposal_hash: PROPOSAL_2,
            PROPOSAL_ALT_A.proposal_hash: PROPOSAL_1,
        },
    )
    assert result.state is TallyState.PENDING
    assert result.yes == ()
    assert Finding(GovernanceFinding.UNKNOWN_PROPOSAL, claim_id(other)) in result.findings
    kinds = {f.kind for f in result.findings}
    assert GovernanceFinding.CONFLICTING_APPROVAL not in kinds
