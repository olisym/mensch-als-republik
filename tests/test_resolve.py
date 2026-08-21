"""resolve_state — Fassade über Kette, Policy und Schlüssel (D183)."""

from __future__ import annotations

import pytest

from mensch_als_republik.atom import claim_id
from mensch_als_republik.governance.chain import resolve_epoch
from mensch_als_republik.keys import resolve_authorized_keys
from mensch_als_republik.profiles.policy import resolve_policy
from mensch_als_republik.resolve import resolve_state
from tests.helpers import store_with
from tests.governance.fixtures import (
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
    P1,
    P2,
    PROPOSAL_1,
    PROPOSAL_2,
    STOCK_N,
    fresh_p2,
    ratify_claim,
    vote,
)


def _two_transitions():
    alice, bob, carol, dave, eve = fresh_p2()
    v1 = [
        vote(alice, PROPOSAL_1, choice=1, t=1),
        vote(bob, PROPOSAL_1, choice=1, t=1),
        vote(carol, PROPOSAL_1, choice=1, t=1),
        vote(dave, PROPOSAL_1, choice=1, t=1),
    ]
    r1 = ratify_claim(alice, PROPOSAL_1, witnesses=[claim_id(v) for v in v1][:3], t=10)
    v2 = [
        vote(alice, PROPOSAL_2, choice=1, t=20),
        vote(bob, PROPOSAL_2, choice=1, t=20),
        vote(carol, PROPOSAL_2, choice=1, t=20),
        vote(dave, PROPOSAL_2, choice=1, t=20),
        vote(eve, PROPOSAL_2, choice=1, t=20),
    ]
    r2 = ratify_claim(alice, PROPOSAL_2, witnesses=[claim_id(v) for v in v2][:4], t=30)
    return store_with(*v1, r1, *v2, r2)


def _known(*, constitutions: dict | None = None):
    if constitutions is None:
        constitutions = {
            CONSTITUTION_HASH_1: C1,
            CONSTITUTION_HASH_2: C2,
            CONSTITUTION_HASH_3: C3,
        }
    proposals = {
        PROPOSAL_1.proposal_hash: PROPOSAL_1,
        PROPOSAL_2.proposal_hash: PROPOSAL_2,
    }
    return constitutions, proposals


def _resolve(store, *, constitutions: dict | None = None, scope: bytes = N_D):
    known_constitutions, known_proposals = _known(constitutions=constitutions)
    return resolve_state(
        store,
        scope=scope,
        genesis_obj=GENESIS_D,
        known_constitutions=known_constitutions,
        known_proposals=known_proposals,
        now=NOW,
    )


def test_resolve_state_two_transitions() -> None:
    state = _resolve(_two_transitions())
    assert state.epoch == EPOCH_3


def test_resolve_state_policy_from_current_constitution() -> None:
    """Policy aus der geltenden Verfassung, nicht aus der ersten (D183)."""
    assert C1["participants"] == P1
    assert C3["participants"] == P2
    state = _resolve(_two_transitions())
    from_c3 = resolve_policy(
        scope=N_D,
        genesis_obj=GENESIS_D,
        constitution_hash=EPOCH_3.constitution_hash,
        constitution_obj=C3,
    ).policy
    assert state.policy == from_c3


def test_resolve_state_authorized_keys_match_direct() -> None:
    store = _two_transitions()
    state = _resolve(store)
    direct = resolve_authorized_keys(
        store,
        scope=N_D,
        genesis_obj=GENESIS_D,
        constitution_hash=EPOCH_3.constitution_hash,
        constitution_obj=C3,
        now=NOW,
        policy=state.policy,
    )
    assert state.authorized_keys == direct.keys


def test_resolve_state_missing_c3_keeps_findings_separate() -> None:
    state = _resolve(
        _two_transitions(),
        constitutions={
            CONSTITUTION_HASH_1: C1,
            CONSTITUTION_HASH_2: C2,
        },
    )
    assert state.epoch == EPOCH_2
    assert state.epoch_findings != ()
    assert state.key_findings == ()


def test_resolve_state_wrong_scope_raises_like_resolve_epoch() -> None:
    store = _two_transitions()
    constitutions, proposals = _known()
    kwargs = dict(
        store=store,
        scope=STOCK_N,
        genesis_obj=GENESIS_D,
        known_constitutions=constitutions,
        known_proposals=proposals,
        now=NOW,
    )
    with pytest.raises(ValueError) as epoch_exc:
        resolve_epoch(**kwargs)
    with pytest.raises(ValueError) as state_exc:
        resolve_state(**kwargs)
    assert type(state_exc.value) is type(epoch_exc.value)
    assert state_exc.value.args == epoch_exc.value.args
