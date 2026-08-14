"""VOUCH_WITHOUT_TEXP: Vermerk ohne Wirkung (D119, 02 §6.2)."""

from __future__ import annotations

from mensch_als_republik.atom import claim_id
from mensch_als_republik.index import classify_all
from mensch_als_republik.trust import Finding, TrustFinding, TrustParams, trust
from mensch_als_republik.trust.derive import derive
from mensch_als_republik.trust.groups import build_groups
from mensch_als_republik.verifier import State

from tests.helpers import Identity, scope_id, store_with
from .tp02 import NOW, T_EXP

PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=4)


def test_vouch_without_texp_finding_fires() -> None:
    scope = scope_id("vouch-no-texp")
    alice, bob = Identity("no-texp-A"), Identity("no-texp-B")
    claim = alice.vouch(bob, n=1, scope=scope, t=1)
    store = store_with(claim)
    r = trust(
        store,
        anchors=frozenset({alice.pub}),
        targets=frozenset({bob.pub}),
        scope=scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    assert r.findings == (
        Finding(kind=TrustFinding.VOUCH_WITHOUT_TEXP, subject=claim_id(claim)),
    )


def test_vouch_without_texp_is_inert() -> None:
    scope = scope_id("vouch-texp-inert")

    def run(*, t_exp: int | None):
        alice, bob = Identity("inert-A"), Identity("inert-B")
        claim = alice.vouch(bob, n=2, scope=scope, t=1, t_exp=t_exp)
        store = store_with(claim)
        classifications = classify_all(store, NOW)
        groups, findings = build_groups(
            store.all_claims(), classifications, scope, PARAMS.D, NOW
        )
        derivation = derive(
            store,
            anchors=frozenset({alice.pub}),
            scope=scope,
            now=NOW,
            params=PARAMS,
        )
        return groups, findings, derivation.bfs.node_capacity, claim

    groups_wo, findings_wo, cap_wo, claim_wo = run(t_exp=None)
    groups_w, findings_w, cap_w, _claim_w = run(t_exp=T_EXP)

    assert set(groups_wo) == set(groups_w)
    for key in groups_wo:
        assert groups_wo[key].n_budget == groups_w[key].n_budget
        assert groups_wo[key].n_kante == groups_w[key].n_kante
    assert cap_wo == cap_w
    assert findings_w == ()
    assert findings_wo == (
        Finding(kind=TrustFinding.VOUCH_WITHOUT_TEXP, subject=claim_id(claim_wo)),
    )


def test_no_vouch_without_texp_on_unparsable_v() -> None:
    scope = scope_id("vouch-no-texp-bad-v")
    alice, bob = Identity("bad-v-A"), Identity("bad-v-B")
    claim = alice.vouch_raw(bob, v=b"\xff", scope=scope, t=1)
    store = store_with(claim)
    r = trust(
        store,
        anchors=frozenset({alice.pub}),
        targets=frozenset({bob.pub}),
        scope=scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    cid = claim_id(claim)
    assert r.findings == (
        Finding(kind=TrustFinding.UNPARSABLE_VOUCH_PAYLOAD, subject=cid),
    )
    assert not any(f.kind == TrustFinding.VOUCH_WITHOUT_TEXP for f in r.findings)


def test_no_vouch_without_texp_outside_budget_set() -> None:
    scope = scope_id("vouch-no-texp-outside")
    a1 = Identity("out-A")
    a2 = Identity("out-A")
    bob = Identity("out-B")
    carol = Identity("out-C")
    v1 = a1.vouch(bob, n=1, scope=scope, t=1)
    v2 = a2.vouch(carol, n=1, scope=scope, t=1)
    store = store_with(v1, v2)
    classifications = classify_all(store, NOW)
    assert classifications[claim_id(v1)].state == State.EQUIVOCATION_FLAGGED
    assert classifications[claim_id(v2)].state == State.EQUIVOCATION_FLAGGED
    _groups, findings = build_groups(
        store.all_claims(), classifications, scope, PARAMS.D, NOW
    )
    assert not any(f.kind == TrustFinding.VOUCH_WITHOUT_TEXP for f in findings)
