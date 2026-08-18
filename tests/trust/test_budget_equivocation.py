"""EQUIVOCATION_FLAGGED gehoert ins Budget-Set (D135)."""

from __future__ import annotations

from mensch_als_republik.atom import claim_id, is_equivocation_pair
from mensch_als_republik.index import classify_all
from mensch_als_republik.trust import Finding, TrustFinding, trust
from mensch_als_republik.trust.groups import build_groups
from mensch_als_republik.verifier import State

from tests.helpers import Identity, scope_id, store_with
from .tp02 import NOW, PARAMS, T_EXP


def test_equivocation_pair_overcommits() -> None:
    scope = scope_id("budget-reset")
    a1 = Identity("budget-reset-A")
    a2 = Identity("budget-reset-A")
    bob, carol = Identity("budget-reset-B"), Identity("budget-reset-C")

    v1 = a1.vouch(bob, n=PARAMS.D, scope=scope, t=1, t_exp=T_EXP)
    v2 = a2.vouch(carol, n=PARAMS.D, scope=scope, t=1, t_exp=T_EXP)

    assert is_equivocation_pair(v1, v2)
    store = store_with(v1, v2)
    classifications = classify_all(store, NOW)
    assert classifications[claim_id(v1)].state == State.EQUIVOCATION_FLAGGED
    assert classifications[claim_id(v2)].state == State.EQUIVOCATION_FLAGGED

    groups, _findings = build_groups(
        store.all_claims(), classifications, scope, PARAMS.D, NOW
    )
    assert len(groups) == 2
    assert sum(g.n_budget for g in groups.values()) == 2 * PARAMS.D

    r = trust(
        store,
        anchors=frozenset({a1.pub}),
        targets=frozenset({bob.pub, carol.pub}),
        scope=scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    assert r.findings == (
        Finding(kind=TrustFinding.OVERCOMMITTED_AUTHOR, subject=a1.pub),
    )
