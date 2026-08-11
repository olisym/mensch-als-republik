"""T-02.2 (Budget-Fall: Widerruf/Supersede, zwei Uhren) und T-02.2b (Gruppen-Aggregation, K7)."""

from __future__ import annotations

import pytest

from mensch_als_republik.trust import TrustFinding, TrustParams, trust

from .helpers import Identity, scope_id, store_with
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
    # 02a-maxflow-prompt.md T-02.2b listet fuer "beide aktiv" Sigma n_budget=4 und "keins",
    # obwohl n_budget(g1-Gruppe)=max(2,3)=3 und die fest verdrahteten g2/g3 (je n=1) macht
    # 3+1+1=5>4 -- dieselbe Rechnung wie bei "Heraufstufung", das dort OVERCOMMITTED_AUTHOR
    # ergibt. Der Prompt-Tabelleneintrag ist in sich widerspruechlich (Trust-Werte 3/1/1
    # setzen n_budget=3 voraus, die Summenspalte passt nicht dazu); siehe Ruecksprachen im
    # Abnahme-Bericht. Hier folgen wir der Arithmetik, nicht der Summenspalte.
    "both_active": (2, "active", 3, (3, 1, 1, 4, True)),
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
    """G-Erneuerung == einfacher Graph mit CAROL->g1 n=2 (S isoliert)."""
    scope = scope_id("INV6")
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
    for target, expected in ((g1, 2), (g2, 1), (g3, 1)):
        r = trust(
            store, anchors=anchors, targets=frozenset({target.pub}), scope=scope,
            now=1000, params=PARAMS, include_flagged=True,
        )
        assert r.value == expected
    r_sim = trust(
        store, anchors=anchors, targets=frozenset({g1.pub, g2.pub, g3.pub}), scope=scope,
        now=1000, params=PARAMS, include_flagged=True,
    )
    assert r_sim.value == 4
