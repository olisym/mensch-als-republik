"""T-02.4 — Kopplung an Layer 01: classify_all == classify, trust_usable == (state == ACTIVE)."""

from __future__ import annotations

import json
from pathlib import Path

from mensch_als_republik.atom import claim_from_bytes, claim_id
from mensch_als_republik.trust import classify_all
from mensch_als_republik.verifier import InMemoryStore, State, classify

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


def _assert_coupled(store: InMemoryStore, now: int) -> None:
    fast = classify_all(store, now)
    for c in store.all_claims():
        cid = claim_id(c)
        slow = classify(c, store, now)
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
