"""T-02.4 — Kopplung an Layer 01: classify_all == classify, trust_usable == (state == ACTIVE).

PR-INV-11: derselbe Kopplungsfall mit policy-Parameter (03-prompt §0 / D87).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from symbolon.atom import claim_from_bytes, claim_id
from symbolon.policy import NucleusPolicy
from symbolon.trust import classify_all
from symbolon.verifier import InMemoryStore, State, classify

from tests.helpers import Identity, scope_id, store_with
from .tp02 import T_EXP, build

VECTORS = json.loads(
    (Path(__file__).resolve().parent.parent / "vectors" / "vectors_01.json").read_text()
)


def _layer01_store() -> InMemoryStore:
    store = InMemoryStore()
    for v in VECTORS["vectors"]:
        try:
            store.add(claim_from_bytes(bytes.fromhex(v["signed_bytes"])))
        except Exception:
            continue
    return store


def _assert_coupled(
    store: InMemoryStore,
    now: int,
    policy: NucleusPolicy | None = None,
) -> None:
    """PR-INV-11 zweiteilig: fremder nuc-Scope ↔ classify(..., None), sonst mit policy."""
    fast = classify_all(store, now, policy)
    for c in store.all_claims():
        cid = claim_id(c)
        if (
            policy is not None
            and c.p.startswith("nuc:")
            and c.N != policy.scope
        ):
            slow = classify(c, store, now, None)
        else:
            slow = classify(c, store, now, policy)
        assert fast[cid] == slow, cid.hex()
        assert slow.trust_usable == (slow.state == State.ACTIVE)


def test_coupling_layer01_vectors() -> None:
    store = _layer01_store()
    _assert_coupled(store, now=1_700_000_100)
    _assert_coupled(store, now=1_800_000_000)


def test_coupling_trust_flow_graph_with_lifecycle_claims() -> None:
    g = build("C")
    scope = scope_id("T-02.4-lifecycle")
    A, B, C = Identity("cpl-A"), Identity("cpl-B"), Identity("cpl-C")
    target = Identity("cpl-target")
    v1 = C.vouch(target, n=2, scope=scope, t=1, t_exp=2000)
    revoke = C.revoke(v1, t=5)
    v2 = C.vouch(target, n=1, scope=scope, t=6, t_exp=T_EXP)
    supersede = C.supersede(v2, t=7)
    v3 = C.vouch(target, n=3, scope=scope, t=8, t_exp=T_EXP)

    claims = [
        A.vouch(B, n=4, scope=scope, t=1, t_exp=T_EXP),
        B.vouch(C, n=4, scope=scope, t=1, t_exp=T_EXP),
        v1,
        revoke,
        v2,
        supersede,
        v3,
    ]
    store = store_with(*claims)
    _assert_coupled(store, now=1000)
    _assert_coupled(store, now=2001)

    # PR-INV-11 / T-02.4 mit Policy (03-prompt §0, D91)
    policy = NucleusPolicy(scope=scope)
    _assert_coupled(store, now=1000, policy=policy)
    _assert_coupled(store, now=2001, policy=policy)

    # irrevocable-Pfad (obligation@1 bleibt ACTIVE trotz revoke)
    obl_scope = scope_id("T-02.4-policy")
    alice, bob = Identity("cpl-pol-A"), Identity("cpl-pol-B")
    obl = alice.claim(
        p=f"nuc:{obl_scope.hex()}/obligation@1", J=(1, bob.pub), t=1, N=obl_scope,
    )
    rev = alice.revoke(obl, t=2)
    obl_store = store_with(obl, rev)
    obl_policy = NucleusPolicy(scope=obl_scope)
    _assert_coupled(obl_store, now=100, policy=obl_policy)
    _assert_coupled(obl_store, now=100, policy=None)


def test_classify_all_never_raises_on_mixed_scopes() -> None:
    """PR-INV-12: classify_all wirft nie, egal wie viele Nuklei der Store trägt."""
    s1, s2, s3 = scope_id("mix-A"), scope_id("mix-B"), scope_id("mix-C")
    a, b = Identity("mix-A"), Identity("mix-B")
    claims = [
        a.claim(p=f"nuc:{s1.hex()}/obligation@1", J=(1, b.pub), t=1, N=s1),
        a.claim(p=f"nuc:{s2.hex()}/obligation@1", J=(1, b.pub), t=2, N=s2),
        a.claim(p=f"nuc:{s3.hex()}/vouch@1", J=(1, b.pub), t=3, N=s3),
    ]
    store = store_with(*claims)
    policy = NucleusPolicy(scope=s1)
    result = classify_all(store, 100, policy)
    assert len(result) == 3
    _assert_coupled(store, now=100, policy=policy)


def test_classify_all_superseded() -> None:
    """Ziel eines eigenen core/supersede@1 ist State.SUPERSEDED (01 §B.1, D278)."""
    scope = hashlib.sha256(b"scope:d278").digest()
    alice = Identity("alice")
    bob = Identity("bob")
    v = alice.vouch(bob, n=1, scope=scope, t=100)
    sup = alice.supersede(v, t=200)
    store = store_with(v, sup)
    result = classify_all(store, 300)
    assert result[claim_id(v)].state == State.SUPERSEDED


def test_classify_all_revoked() -> None:
    """Gegenprobe: Ziel eines eigenen core/revoke@1 ist State.REVOKED (01 §B.1, D278)."""
    scope = hashlib.sha256(b"scope:d278").digest()
    alice = Identity("alice")
    bob = Identity("bob")
    v = alice.vouch(bob, n=1, scope=scope, t=100)
    rev = alice.revoke(v, t=200)
    store = store_with(v, rev)
    result = classify_all(store, 300)
    assert result[claim_id(v)].state == State.REVOKED
