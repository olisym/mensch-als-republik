"""T-02.3 — Disjunktheit (Einheitskapazitaets-Lauf, K5), inkl. TP-FAN (Endpunkt-Regel)."""

from __future__ import annotations

from mensch_als_republik.trust import TrustParams, trust

from .helpers import Identity, scope_id, store_with
from .tp02 import NOW, PARAMS, T_EXP, build


def test_disjoint_paths_variant_C() -> None:
    g = build("C")
    store = g.store()
    anchors = frozenset({g.ALICE.pub})

    r = trust(
        store, anchors=anchors, targets=frozenset({g.g1.pub}), scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=True,
    )
    assert r.disjoint_paths == 1

    r_sim = trust(
        store, anchors=anchors, targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}), scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=True,
    )
    assert r_sim.disjoint_paths == 1


def test_disjoint_paths_invariant_to_1000_extra_sybils() -> None:
    """D24: alle Pfade laufen durch BOB, unabhaengig von |S|.

    Die Sybils haengen an CAROL (dem ehrlichen Grenzknoten) und sind selbst Ziele --
    sonst prueft der Test nichts: stromabwaerts vom Ziel kann nichts wirken.
    """
    g = build("C")
    claims = list(g.claims)
    extra_targets = []
    for i in range(1000):
        h = Identity(f"sybil-{i}")
        claims.append(g.CAROL.vouch(h, n=1, scope=g.scope, t=1, t_exp=T_EXP))
        extra_targets.append(h.pub)
    store = store_with(*claims)

    r = trust(
        store,
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.g1.pub}) | frozenset(extra_targets),
        scope=g.scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    assert r.disjoint_paths == 1


def test_TP_FAN_endpoint_rule() -> None:
    """Ohne Endpunkt-Regel (Anker gespalten) kaeme 1 statt 2 heraus."""
    scope = scope_id("TP-FAN")
    params = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=4)
    A, B1, B2, X = (Identity(n) for n in ("FAN-A", "FAN-B1", "FAN-B2", "FAN-X"))
    claims = [
        A.vouch(B1, n=2, scope=scope, t=1, t_exp=T_EXP),
        A.vouch(B2, n=2, scope=scope, t=1, t_exp=T_EXP),
        B1.vouch(X, n=4, scope=scope, t=1, t_exp=T_EXP),
        B2.vouch(X, n=4, scope=scope, t=1, t_exp=T_EXP),
    ]
    store = store_with(*claims)
    r = trust(
        store, anchors=frozenset({A.pub}), targets=frozenset({X.pub}), scope=scope,
        now=NOW, params=params, include_flagged=True,
    )
    assert r.value == 16
    assert r.disjoint_paths == 2
