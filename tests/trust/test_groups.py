"""T-02.2 (Budget-Fall: Widerruf/Supersede, zwei Uhren) und T-02.2b (Gruppen-Aggregation, K7)."""

from __future__ import annotations

import pytest

from symbolon.atom import claim_id
from symbolon.index import classify_all
from symbolon.trust import TrustFinding, TrustParams, trust
from symbolon.trust.derive import derive
from symbolon.verifier import State

from tests.helpers import Identity, scope_id, store_with
from .tp02 import T_EXP

PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=4)


def _mesh(g1, g2, g3, n, scope, t_exp):
    pairs = [(g1, g2), (g2, g1), (g1, g3), (g3, g1), (g2, g3), (g3, g2)]
    return [a.vouch(b, n=n, scope=scope, t=1, t_exp=t_exp) for a, b in pairs]


def _rump(alice, bob, carol, scope, t_exp):
    return [
        alice.vouch(bob, n=4, scope=scope, t=1, t_exp=t_exp),
        bob.vouch(carol, n=4, scope=scope, t=1, t_exp=t_exp),
    ]


@pytest.mark.parametrize("via_supersede", [False, True])
def test_S1_revoked_vouch_leaves_active_set_keeps_budget(via_supersede: bool) -> None:
    """Basis C, CAROL->g1 mit t_exp=2000, widerrufen (oder supersediert) bei t=900."""
    suffix = "supersede" if via_supersede else "revoke"
    scope = scope_id(f"T-02.2-{suffix}")
    ALICE, BOB, CAROL = Identity(f"A-{suffix}"), Identity(f"B-{suffix}"), Identity(f"C-{suffix}")
    g1, g2, g3 = Identity(f"g1-{suffix}"), Identity(f"g2-{suffix}"), Identity(f"g3-{suffix}")

    claims = _rump(ALICE, BOB, CAROL, scope, T_EXP)
    g1v = CAROL.vouch(g1, n=1, scope=scope, t=1, t_exp=2000)
    g2v = CAROL.vouch(g2, n=1, scope=scope, t=1, t_exp=T_EXP)
    g3v = CAROL.vouch(g3, n=1, scope=scope, t=1, t_exp=T_EXP)
    if via_supersede:
        lifecycle = CAROL.supersede(g1v, t=900)
    else:
        lifecycle = CAROL.revoke(g1v, t=900)
    claims += [g1v, g2v, g3v, lifecycle]
    claims += _mesh(g1, g2, g3, 2, scope, T_EXP)
    store = store_with(*claims)

    anchors = frozenset({ALICE.pub})
    for target, expected in ((g1, 2), (g2, 2), (g3, 2)):
        r = trust(
            store, anchors=anchors, targets=frozenset({target.pub}), scope=scope,
            now=1000, params=PARAMS, include_flagged=True,
        )
        assert r.value == expected, target.label

    r_sim = trust(
        store, anchors=anchors, targets=frozenset({g1.pub, g2.pub, g3.pub}), scope=scope,
        now=1000, params=PARAMS, include_flagged=True,
    )
    assert r_sim.value == 2

    # S1: d(g1)=4, C(g1)=1, cap(g1->gj) = floor(2*1/4) = 0 -> zwei SUBGRANULAR_VOUCH
    # (g1->g2, g1->g3); Anker 5 in 02-golden-anchors.md.
    subgranular = [f for f in r_sim.findings if f.kind == TrustFinding.SUBGRANULAR_VOUCH]
    assert len(subgranular) == 2

    # Budgetwirkung bei now=1000: Sigma n_budget(CAROL) = 3 (g1 weiterhin im Budget-Set)
    for n, overcommitted in ((2, True), (1, False)):
        dave = Identity(f"DAVE-{suffix}-{n}")
        dave_store = store_with(*claims, CAROL.vouch(dave, n=n, scope=scope, t=5, t_exp=T_EXP))
        r = trust(
            dave_store, anchors=anchors, targets=frozenset({dave.pub}), scope=scope,
            now=1000, params=PARAMS, include_flagged=True,
        )
        found = any(
            f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == CAROL.pub
            for f in r.findings
        )
        assert found is overcommitted, f"n={n}"

    # S2: now=2001, der widerrufene/supersedierte Vouch ist abgelaufen -> Budget frei
    dave2 = Identity(f"DAVE2-{suffix}")
    dave_store = store_with(*claims, CAROL.vouch(dave2, n=2, scope=scope, t=5, t_exp=T_EXP))
    r = trust(
        dave_store, anchors=anchors, targets=frozenset({dave2.pub}), scope=scope,
        now=2001, params=PARAMS, include_flagged=True,
    )
    assert not any(
        f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == CAROL.pub
        for f in r.findings
    )


# --- T-02.2b: Gruppen-Aggregation (Variante G) ---

_CASES = {
    # (n_v1, state_v1, n_v2) -> (g1, g2, g3, simultan, overcommitted)
    "renewal": (2, "superseded", 2, (2, 1, 1, 4, False)),
    "downgrade": (2, "superseded", 1, (1, 1, 1, 3, False)),
    "upgrade": (1, "superseded", 3, (3, 1, 1, 4, True)),
    # War zuvor (2, "active", 3, ...): das war ein rechnerisches Duplikat von "upgrade"
    # (n_budget(g1)=max(2,3)=3 in beiden Faellen) und stammte aus einer widerspruechlichen
    # Vorgabe (02a-maxflow-prompt.md T-02.2b nannte Sigma n_budget=4 bei "keins", obwohl
    # 3+1+1=5>4 dieselbe Rechnung wie bei "Heraufstufung" ist, das OVERCOMMITTED_AUTHOR
    # ergibt). Aufloesung siehe 02a-abnahme.md Teil B.4: n(V1)=n(V2)=2 prueft das Eigentliche
    # -- zwei gleichzeitig aktive Vouches auf dasselbe Subjekt sind eine Kante mit n=2, nicht
    # zwei Kanten und nicht Sigma n=4 aus dieser Gruppe. Liefert dieselben Werte wie
    # "renewal": Duplikat und Supersede-Kette werden identisch behandelt.
    "both_active": (2, "active", 2, (2, 1, 1, 4, False)),
}


@pytest.mark.parametrize("case", sorted(_CASES))
def test_group_aggregation_variant_G(case: str) -> None:
    n_v1, v1_state, n_v2, (e1, e2, e3, esim, overcommitted) = _CASES[case]
    scope = scope_id(f"T-02.2b-{case}")
    ALICE, BOB, CAROL = Identity(f"A-{case}"), Identity(f"B-{case}"), Identity(f"C-{case}")
    g1, g2, g3 = Identity(f"g1-{case}"), Identity(f"g2-{case}"), Identity(f"g3-{case}")

    claims = _rump(ALICE, BOB, CAROL, scope, T_EXP)
    claims += [
        CAROL.vouch(g2, n=1, scope=scope, t=1, t_exp=T_EXP),
        CAROL.vouch(g3, n=1, scope=scope, t=1, t_exp=T_EXP),
    ]
    v1 = CAROL.vouch(g1, n=n_v1, scope=scope, t=1, t_exp=T_EXP)
    v2 = CAROL.vouch(g1, n=n_v2, scope=scope, t=2, t_exp=T_EXP)
    claims += [v1, v2]
    if v1_state == "superseded":
        claims.append(CAROL.supersede(v1, t=3))

    store = store_with(*claims)
    anchors = frozenset({ALICE.pub})

    for target, expected in ((g1, e1), (g2, e2), (g3, e3)):
        r = trust(
            store, anchors=anchors, targets=frozenset({target.pub}), scope=scope,
            now=1000, params=PARAMS, include_flagged=True,
        )
        assert r.value == expected, f"{case} -> {target.label}"

    r_sim = trust(
        store, anchors=anchors, targets=frozenset({g1.pub, g2.pub, g3.pub}), scope=scope,
        now=1000, params=PARAMS, include_flagged=True,
    )
    assert r_sim.value == esim, f"{case} simultan"

    is_overcommitted = any(
        f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == CAROL.pub
        for f in r_sim.findings
    )
    assert is_overcommitted is overcommitted, case


def test_INV6_aggregation_is_idempotent() -> None:
    """G-Erneuerung == einfacher Graph mit CAROL->g1 n=2 (S isoliert).

    Beide Graphen bauen und die Ergebnisse direkt vergleichen (nicht nur je gegen ein
    Literal), damit der Test nicht gruen wird, wenn beide Seiten gemeinsam falsch sind.
    """
    scope = scope_id("INV6-simple")
    ALICE, BOB, CAROL = Identity("INV6-A"), Identity("INV6-B"), Identity("INV6-C")
    g1, g2, g3 = Identity("INV6-g1"), Identity("INV6-g2"), Identity("INV6-g3")
    claims = _rump(ALICE, BOB, CAROL, scope, T_EXP)
    claims += [
        CAROL.vouch(g1, n=2, scope=scope, t=1, t_exp=T_EXP),
        CAROL.vouch(g2, n=1, scope=scope, t=1, t_exp=T_EXP),
        CAROL.vouch(g3, n=1, scope=scope, t=1, t_exp=T_EXP),
    ]
    store = store_with(*claims)
    anchors = frozenset({ALICE.pub})
    targets = (g1, g2, g3)

    simple_values = [
        trust(
            store, anchors=anchors, targets=frozenset({t.pub}), scope=scope,
            now=1000, params=PARAMS, include_flagged=True,
        ).value
        for t in targets
    ]
    simple_sim = trust(
        store, anchors=anchors, targets=frozenset(t.pub for t in targets), scope=scope,
        now=1000, params=PARAMS, include_flagged=True,
    ).value

    # Literale als zusaetzliche Zusicherung -- siehe Docstring.
    assert simple_values == [2, 1, 1]
    assert simple_sim == 4

    scope_g = scope_id("INV6-renewal")
    ALICE_g, BOB_g, CAROL_g = Identity("INV6g-A"), Identity("INV6g-B"), Identity("INV6g-C")
    g1_g, g2_g, g3_g = Identity("INV6g-g1"), Identity("INV6g-g2"), Identity("INV6g-g3")
    claims_g = _rump(ALICE_g, BOB_g, CAROL_g, scope_g, T_EXP)
    claims_g += [
        CAROL_g.vouch(g2_g, n=1, scope=scope_g, t=1, t_exp=T_EXP),
        CAROL_g.vouch(g3_g, n=1, scope=scope_g, t=1, t_exp=T_EXP),
    ]
    v1 = CAROL_g.vouch(g1_g, n=2, scope=scope_g, t=1, t_exp=T_EXP)
    v2 = CAROL_g.vouch(g1_g, n=2, scope=scope_g, t=2, t_exp=T_EXP)
    claims_g += [v1, v2, CAROL_g.supersede(v1, t=3)]
    store_g = store_with(*claims_g)
    anchors_g = frozenset({ALICE_g.pub})
    targets_g = (g1_g, g2_g, g3_g)

    renewal_values = [
        trust(
            store_g, anchors=anchors_g, targets=frozenset({t.pub}), scope=scope_g,
            now=1000, params=PARAMS, include_flagged=True,
        ).value
        for t in targets_g
    ]
    renewal_sim = trust(
        store_g, anchors=anchors_g, targets=frozenset(t.pub for t in targets_g),
        scope=scope_g, now=1000, params=PARAMS, include_flagged=True,
    ).value

    assert renewal_values == simple_values
    assert renewal_sim == simple_sim


def test_tied_active_vouches_name_minimum_claim_id() -> None:
    """Gleichstand: die Kante traegt min(claim_id) (01 §4.1, 02 §3.1, D172)."""
    scope = scope_id("benennung-A")
    alice = Identity("ben-A-alice")
    bob = Identity("ben-A-bob")
    v1 = alice.vouch(bob, n=2, scope=scope, t=1, t_exp=T_EXP)
    v2 = alice.vouch(bob, n=2, scope=scope, t=2, t_exp=T_EXP)
    store = store_with(v1, v2)
    now = 1000
    classified = classify_all(store, now)
    id1, id2 = claim_id(v1), claim_id(v2)
    assert classified[id1].state is State.ACTIVE
    assert classified[id2].state is State.ACTIVE
    candidates = {id1, id2}
    der = derive(
        store, anchors=frozenset({alice.pub}), scope=scope, now=now,
        params=PARAMS, include_flagged=True,
    )
    group_edges = [
        e for e in der.bfs.edges
        if e.author == alice.pub and e.subject == bob.pub
    ]
    assert len(group_edges) == 1
    assert group_edges[0].claim_id == min(candidates)
