"""T-02.5 — abgeleitete Invarianten (02-golden-anchors.md §8)."""

from __future__ import annotations

import itertools

import pytest

from mensch_als_republik.trust import trust
from mensch_als_republik.trust.dinic import Dinic
from mensch_als_republik.trust.graph import (
    SINK,
    SOURCE,
    bfs_capacities,
    capacity,
    infinity,
    node_in,
    node_out,
)
from mensch_als_republik.trust.groups import build_groups
from mensch_als_republik.trust.index import classify_all

from .helpers import Identity, scope_id, store_with
from .tp02 import NOW, PARAMS, T_EXP, build, build_A_prime


def _maxflow_without_split(store, anchors, targets, scope, now, params):
    """Kein Knoten-Split: interne Kapazitaet = INF ueberall (fuer INV-1)."""
    classifications = classify_all(store, now)
    groups, _ = build_groups(store.all_claims(), classifications, scope, params.D, now)
    bfs_result = bfs_capacities(anchors, groups, params)
    inf = infinity(bfs_result)

    solver = Dinic()
    identities = set(bfs_result.node_capacity) | anchors | targets
    for identity in identities:
        solver.add_edge(node_in(identity), node_out(identity), inf)
    for a in sorted(anchors):
        solver.add_edge(SOURCE, node_in(a), inf)
    for t in sorted(targets):
        solver.add_edge(node_in(t), SINK, inf)
    for e in bfs_result.edges:
        solver.add_edge(node_out(e.author), node_in(e.subject), e.cap)
    return solver.max_flow(SOURCE, SINK)


@pytest.mark.parametrize("variant", ["B", "C", "D", "E", "E0", "F"])
def test_INV1_split_redundant_at_valid_budget(variant: str) -> None:
    g = build(variant)
    store = g.store()
    anchors = frozenset({g.ALICE.pub})

    for target in (g.g1, g.g2, g.g3):
        with_split = trust(
            store, anchors=anchors, targets=frozenset({target.pub}), scope=g.scope,
            now=NOW, params=PARAMS, include_flagged=True,
        ).value
        without_split = _maxflow_without_split(
            store, anchors, frozenset({target.pub}), g.scope, NOW, PARAMS
        )
        assert with_split == without_split, f"{variant} -> {target.label}"

    with_split_sim = trust(
        store, anchors=anchors, targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}), scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=True,
    ).value
    without_split_sim = _maxflow_without_split(
        store, anchors, frozenset({g.g1.pub, g.g2.pub, g.g3.pub}), g.scope, NOW, PARAMS
    )
    assert with_split_sim == without_split_sim, variant


def test_INV1_differs_for_A_simultaneous_only() -> None:
    g = build("A")
    store = g.store()
    anchors = frozenset({g.ALICE.pub})
    targets = frozenset({g.g1.pub, g.g2.pub, g.g3.pub})

    with_split = trust(
        store, anchors=anchors, targets=targets, scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=True,
    ).value
    without_split = _maxflow_without_split(store, anchors, targets, g.scope, NOW, PARAMS)
    assert with_split == 4
    assert without_split == 8

    # Einzelabfrage von A: beide Laeufe sind 4
    for target in (g.g1, g.g2, g.g3):
        with_split_one = trust(
            store, anchors=anchors, targets=frozenset({target.pub}), scope=g.scope,
            now=NOW, params=PARAMS, include_flagged=True,
        ).value
        without_split_one = _maxflow_without_split(
            store, anchors, frozenset({target.pub}), g.scope, NOW, PARAMS
        )
        assert with_split_one == without_split_one == 4


def test_INV1_differs_for_A_prime_simultaneous() -> None:
    g = build_A_prime()
    store = g.store()
    anchors = frozenset({g.ALICE.pub})
    targets = frozenset({g.g1.pub, g.g2.pub, g.g3.pub})

    with_split = trust(
        store, anchors=anchors, targets=targets, scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=True,
    ).value
    without_split = _maxflow_without_split(store, anchors, targets, g.scope, NOW, PARAMS)
    assert with_split == 16
    assert without_split == 48


def test_INV2_sybil_count_independence() -> None:
    """|S|-Unabhaengigkeit ist eine Schranke, keine Gleichheit (§4).

    Sybils haengen hinter CAROL (dem ehrlichen Grenzknoten) und sind selbst Ziele --
    sonst prueft der Test nichts: stromabwaerts vom Ziel kann nichts wirken.
    """
    g_c, g_d = build("C"), build("D")
    anchors_c = frozenset({g_c.ALICE.pub})
    targets_c = frozenset({g_c.g1.pub, g_c.g2.pub, g_c.g3.pub})
    targets_d = frozenset({g_d.g1.pub, g_d.g2.pub, g_d.g3.pub})

    r_c = trust(g_c.store(), anchors=anchors_c, targets=targets_c, scope=g_c.scope,
                now=NOW, params=PARAMS, include_flagged=True)
    r_d = trust(g_d.store(), anchors=frozenset({g_d.ALICE.pub}), targets=targets_d,
                scope=g_d.scope, now=NOW, params=PARAMS, include_flagged=True)
    assert r_c.value == r_d.value == 3        # Topologie in S ist ohne Wirkung

    claims = list(g_c.claims)
    extra = []
    for i in range(1000):
        h = Identity(f"inv2-sybil-{i}")
        claims.append(g_c.CAROL.vouch(h, n=1, scope=g_c.scope, t=1, t_exp=T_EXP))
        extra.append(h.pub)
    store_plus = store_with(*claims)

    r_plus = trust(store_plus, anchors=anchors_c,
                   targets=targets_c | frozenset(extra), scope=g_c.scope,
                   now=NOW, params=PARAMS, include_flagged=True)
    assert r_plus.value == 4                    # steigt von 3 auf 4
    assert r_plus.value <= capacity(PARAMS, 2)  # aber nie ueber C(CAROL)


def test_INV3_monotonicity_exhaustive_over_variant_B() -> None:
    scope = scope_id("INV3")
    ALICE, BOB, CAROL = Identity("INV3-A"), Identity("INV3-B"), Identity("INV3-C")
    g1, g2, g3 = Identity("INV3-g1"), Identity("INV3-g2"), Identity("INV3-g3")
    rump = [
        ALICE.vouch(BOB, n=4, scope=scope, t=1, t_exp=T_EXP),
        BOB.vouch(CAROL, n=4, scope=scope, t=1, t_exp=T_EXP),
    ]
    edges = {
        g1.pub: CAROL.vouch(g1, n=1, scope=scope, t=1, t_exp=T_EXP),
        g2.pub: CAROL.vouch(g2, n=1, scope=scope, t=1, t_exp=T_EXP),
        g3.pub: CAROL.vouch(g3, n=1, scope=scope, t=1, t_exp=T_EXP),
    }
    targets = [g1, g2, g3]
    anchors = frozenset({ALICE.pub})

    def values(subset: frozenset) -> tuple[int, ...]:
        claims = rump + [edges[t.pub] for t in targets if t.pub in subset]
        store = store_with(*claims)
        individual = [
            trust(
                store, anchors=anchors, targets=frozenset({t.pub}), scope=scope,
                now=NOW, params=PARAMS, include_flagged=True,
            ).value
            for t in targets
        ]
        simultan = trust(
            store, anchors=anchors, targets=frozenset(t.pub for t in targets), scope=scope,
            now=NOW, params=PARAMS, include_flagged=True,
        ).value
        return tuple(individual) + (simultan,)

    keys = [g1.pub, g2.pub, g3.pub]
    all_subsets = [
        frozenset(s) for r in range(len(keys) + 1) for s in itertools.combinations(keys, r)
    ]
    results = {s: values(s) for s in all_subsets}

    for sub, sup in itertools.product(all_subsets, all_subsets):
        if not sub <= sup:
            continue
        for v_sub, v_sup in zip(results[sub], results[sup]):
            assert v_sub <= v_sup, (sub, sup)


def test_INV4_simultaneous_le_sum_of_individual() -> None:
    for variant in ("A", "B", "C", "D", "E", "E0", "F"):
        g = build(variant)
        store = g.store()
        anchors = frozenset({g.ALICE.pub})
        individual_sum = sum(
            trust(
                store, anchors=anchors, targets=frozenset({t.pub}), scope=g.scope,
                now=NOW, params=PARAMS, include_flagged=True,
            ).value
            for t in (g.g1, g.g2, g.g3)
        )
        simultan = trust(
            store, anchors=anchors, targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}),
            scope=g.scope, now=NOW, params=PARAMS, include_flagged=True,
        ).value
        assert simultan <= individual_sum, variant


def test_INV4_equality_exactly_in_B_and_E0() -> None:
    for variant, equal in (("B", True), ("E0", True), ("A", False), ("E", False)):
        g = build(variant)
        store = g.store()
        anchors = frozenset({g.ALICE.pub})
        individual_sum = sum(
            trust(
                store, anchors=anchors, targets=frozenset({t.pub}), scope=g.scope,
                now=NOW, params=PARAMS, include_flagged=True,
            ).value
            for t in (g.g1, g.g2, g.g3)
        )
        simultan = trust(
            store, anchors=anchors, targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}),
            scope=g.scope, now=NOW, params=PARAMS, include_flagged=True,
        ).value
        assert (simultan == individual_sum) is equal, variant


def test_INV5_overcommitment_in_S_does_not_change_flow() -> None:
    g_c = build("C")
    g_d = build("D")
    anchors_c = frozenset({g_c.ALICE.pub})
    anchors_d = frozenset({g_d.ALICE.pub})

    for t_c, t_d in zip((g_c.g1, g_c.g2, g_c.g3), (g_d.g1, g_d.g2, g_d.g3)):
        v_c = trust(
            g_c.store(), anchors=anchors_c, targets=frozenset({t_c.pub}), scope=g_c.scope,
            now=NOW, params=PARAMS, include_flagged=True,
        ).value
        v_d = trust(
            g_d.store(), anchors=anchors_d, targets=frozenset({t_d.pub}), scope=g_d.scope,
            now=NOW, params=PARAMS, include_flagged=True,
        ).value
        assert v_c == v_d


def test_INV7_anchor_is_not_a_special_case() -> None:
    g = build_A_prime()
    r = trust(
        g.store(), anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}), scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=True,
    )
    assert r.value == capacity(PARAMS, 0) == 16
