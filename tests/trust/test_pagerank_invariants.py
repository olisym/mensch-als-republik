"""T-02b.7 — abgeleitete Invarianten (02b-golden-anchors.md §9)."""

from __future__ import annotations

import itertools

import pytest

from symbolon.trust import RelaxParams, rank, trust
from symbolon.trust.derive import derive

from tests.helpers import Identity, scope_id, store_with
from .pr02 import RP, mass_bound
from .tp02 import NOW, PARAMS, T_EXP, build


def test_PR_INV1_monotonicity_exhaustive_over_variant_B() -> None:
    """Entfernen einer beliebigen Kante senkt jeden u-Wert oder laesst ihn gleich, nie
    Anstieg. Fehlende Knoten zaehlen als 0 (Neuling ≈ 0, PR-INV-7).

    Alle fuenf Kanten von Variante B variieren (2^5 = 32 Teilgraphen, 02b §9), nicht nur die
    drei Sybil-Kanten -- sonst blieben der Rumpf ALICE->BOB->CAROL fest und der Fall, in dem
    eine ganze Kette wegfaellt, waere ungeprueft.
    """
    scope = scope_id("PR-INV1")
    ALICE, BOB, CAROL = Identity("prinv1-A"), Identity("prinv1-B"), Identity("prinv1-C")
    g1, g2, g3 = Identity("prinv1-g1"), Identity("prinv1-g2"), Identity("prinv1-g3")
    edges = {
        BOB.pub: ALICE.vouch(BOB, n=4, scope=scope, t=1, t_exp=T_EXP),
        CAROL.pub: BOB.vouch(CAROL, n=4, scope=scope, t=1, t_exp=T_EXP),
        g1.pub: CAROL.vouch(g1, n=1, scope=scope, t=1, t_exp=T_EXP),
        g2.pub: CAROL.vouch(g2, n=1, scope=scope, t=1, t_exp=T_EXP),
        g3.pub: CAROL.vouch(g3, n=1, scope=scope, t=1, t_exp=T_EXP),
    }
    keys = [BOB.pub, CAROL.pub, g1.pub, g2.pub, g3.pub]
    anchors = frozenset({ALICE.pub})

    def values(subset: frozenset) -> dict:
        claims = [edges[k] for k in keys if k in subset]
        store = store_with(*claims)
        r = rank(store, anchors=anchors, scope=scope, now=NOW, params=RP, include_flagged=True)
        return dict(r.scores)

    all_subsets = [
        frozenset(s) for r in range(len(keys) + 1) for s in itertools.combinations(keys, r)
    ]
    assert len(all_subsets) == 32
    results = {s: values(s) for s in all_subsets}
    all_identities = set().union(*(set(v) for v in results.values()))

    violations = 0
    for sub, sup in itertools.product(all_subsets, all_subsets):
        if not sub <= sup:
            continue
        for identity in all_identities:
            v_sub = results[sub].get(identity, 0)
            v_sup = results[sup].get(identity, 0)
            if v_sub > v_sup:
                violations += 1
    assert violations == 0


def test_PR_INV2_mass_bound_holds_at_valid_budget() -> None:
    for variant in ("B", "C", "E", "E0", "F"):
        g = build(variant)
        r = rank(
            g.store(), anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
            include_flagged=True,
        )
        assert r.mass <= mass_bound(r.denominator, 1, RP)


def test_PR_INV2_F_meets_the_bound_exactly() -> None:
    g = build("F")
    r = rank(
        g.store(), anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
        include_flagged=True,
    )
    assert r.mass == mass_bound(r.denominator, 1, RP)


def test_PR_INV3_overcommit_indicator_is_one_sided() -> None:
    for variant in ("A", "D"):
        g = build(variant)
        r = rank(
            g.store(), anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
            include_flagged=True,
        )
        assert r.mass > mass_bound(r.denominator, 1, RP)

    # D mit False: der über-committete Knoten sitzt in S, seine Kanten fallen weg; kein
    # Falschalarm mehr, obwohl die gi weiterhin ueber-committet SIND (nur nicht im Lauf).
    g_d = build("D")
    r_d_false = rank(
        g_d.store(), anchors=frozenset({g_d.ALICE.pub}), scope=g_d.scope, now=NOW,
        params=RP, include_flagged=False,
    )
    assert r_d_false.mass <= mass_bound(r_d_false.denominator, 1, RP)

    for variant in ("B", "C", "E", "E0", "F"):
        g = build(variant)
        r = rank(
            g.store(), anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
            include_flagged=True,
        )
        assert r.mass <= mass_bound(r.denominator, 1, RP)


@pytest.mark.parametrize("include_flagged", [True, False])
@pytest.mark.parametrize("variant", ["B", "C", "D", "E", "E0", "F", "A"])
def test_PR_INV4_edge_set_is_shared_with_paragraph_4(
    variant: str, include_flagged: bool
) -> None:
    """Der Kantensatz, ueber den 02 §5 rechnet, ist byte-gleich mit dem von 02 §4 (D49): beide
    rufen dieselbe derive()-Funktion auf."""
    from symbolon.trust.flow import derive as derive_in_flow
    from symbolon.trust.relax import derive as derive_in_relax

    # Diese Zeile traegt die Invariante -- ein Identitaetsvergleich der Funktionsobjekte
    # kann nicht zufaellig gruen sein. Die folgenden Knotenmengen-Vergleiche sind Zusatz
    # und pruefen nur, dass rank() die Knotenmenge korrekt aus edges bildet.
    assert derive_in_flow is derive_in_relax

    g = build(variant)
    store = g.store()
    anchors = frozenset({g.ALICE.pub})

    derivation = derive(
        store, anchors=anchors, scope=g.scope, now=NOW, params=PARAMS,
        include_flagged=include_flagged,
    )
    expected_nodes = set(anchors)
    for e in derivation.bfs.edges:
        expected_nodes.add(e.author)
        expected_nodes.add(e.subject)

    r = rank(
        store, anchors=anchors, scope=g.scope, now=NOW, params=RP,
        include_flagged=include_flagged,
    )
    rank_nodes = {identity for identity, _ in r.scores}

    assert rank_nodes == expected_nodes
    assert set(derivation.bfs.node_capacity) == expected_nodes


@pytest.mark.parametrize("include_flagged", [True, False])
@pytest.mark.parametrize("variant", ["B", "C", "D", "E", "E0", "F", "A"])
def test_PR_INV5_findings_identical_to_trust(variant: str, include_flagged: bool) -> None:
    g = build(variant)
    store = g.store()
    anchors = frozenset({g.ALICE.pub})
    targets = frozenset({g.g1.pub, g.g2.pub, g.g3.pub})

    r_rank = rank(
        store, anchors=anchors, scope=g.scope, now=NOW, params=RP,
        include_flagged=include_flagged,
    )
    r_trust = trust(
        store, anchors=anchors, targets=targets, scope=g.scope, now=NOW, params=PARAMS,
        include_flagged=include_flagged,
    )
    assert r_rank.findings == r_trust.findings


def test_PR_INV7_unreachable_is_exactly_absent() -> None:
    for variant in ("A", "B", "C", "D", "E", "E0", "F"):
        g = build(variant)
        r = rank(
            g.store(), anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
            include_flagged=True,
        )
        identities = {identity for identity, _ in r.scores}
        assert g.EVE.pub not in identities

    g0 = build("E0")
    r0 = rank(
        g0.store(), anchors=frozenset({g0.ALICE.pub}), scope=g0.scope, now=NOW, params=RP,
        include_flagged=True,
    )
    identities0 = {identity for identity, _ in r0.scores}
    assert g0.g2.pub not in identities0
    assert g0.g3.pub not in identities0


@pytest.mark.parametrize("variant", ["B", "F"])
def test_PR_INV8_monotonicity_in_K(variant: str) -> None:
    """u_K[J] * (bD)^(20-K) <= u_20[J] -- auf gemeinsamen Nenner gebracht, nicht roh
    verglichen: die u verschiedener K leben ueber verschiedenen Delta."""
    g = build(variant)
    store = g.store()
    anchors = frozenset({g.ALICE.pub})
    bD = RP.alpha_den * PARAMS.D

    results: dict[int, dict[bytes, int]] = {}
    for k in range(1, 21):
        rp_k = RelaxParams(base=PARAMS, alpha_num=1, alpha_den=2, rounds=k)
        r = rank(store, anchors=anchors, scope=g.scope, now=NOW, params=rp_k, include_flagged=True)
        results[k] = dict(r.scores)

    u_20 = results[20]
    for k in range(1, 20):
        u_k = results[k]
        for identity, value in u_k.items():
            assert value * (bD ** (20 - k)) <= u_20[identity], (variant, k, identity.hex())


def test_PR_INV9_anchor_asymmetry_halves_every_value() -> None:
    """Ein zweiter, isolierter Anker senkt jeden t-Wert (halbiert ihn hier) -- anders als
    in 02 §4, wo zusaetzliche Anker nie senken (D51). Kein 02 §7-Bruch: 02 §7 handelt von Kanten."""
    g = build("B")
    store = g.store()
    alice2 = Identity("prinv9-alice2-isolated")

    r_one = rank(
        store, anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
        include_flagged=True,
    )
    r_two = rank(
        store, anchors=frozenset({g.ALICE.pub, alice2.pub}), scope=g.scope, now=NOW,
        params=RP, include_flagged=True,
    )

    scores_one = dict(r_one.scores)
    scores_two = dict(r_two.scores)

    assert r_two.denominator == 2 * r_one.denominator
    # Die rohen u-Werte sind hier unveraendert, weil ALICE2 isoliert ist und keine Masse ins
    # System bringt. NICHT weil die Rekursion unabhaengig von |A| waere -- der Restart-Term
    # wird je Anker addiert. Was sich herauskuerzt, ist |A| aus dem Restart-Term selbst
    # (Delta * e_J = (bD)^k), nicht die Zahl der Anker aus der Rekursion. Mit einem
    # verbundenen zweiten Anker steigen fremde u-Werte (offener Vektor, Anchors 02b §11).
    for identity, value in scores_one.items():
        assert scores_two[identity] == value

    assert alice2.pub in scores_two
    assert scores_two[alice2.pub] == scores_two[g.ALICE.pub]
