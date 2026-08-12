"""T-02b.3 — Gruppen-Aggregation (Anker PR-3, D40/PR-INV-6)."""

from __future__ import annotations

from mensch_als_republik.trust import rank

from tests.helpers import Identity, scope_id, store_with
from .pr02 import RP
from .tp02 import NOW, T_EXP


def _build(n_v1: int, v1_state: str, n_v2: int, label: str):
    scope = scope_id(f"PR-3-{label}")
    ALICE, BOB, CAROL = Identity(f"pr3A-{label}"), Identity(f"pr3B-{label}"), Identity(f"pr3C-{label}")
    g1, g2, g3 = Identity(f"pr3g1-{label}"), Identity(f"pr3g2-{label}"), Identity(f"pr3g3-{label}")
    claims = [
        ALICE.vouch(BOB, n=4, scope=scope, t=1, t_exp=T_EXP),
        BOB.vouch(CAROL, n=4, scope=scope, t=1, t_exp=T_EXP),
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
    r = rank(store, anchors=anchors, scope=scope, now=1000, params=RP, include_flagged=True)
    return r, {"ALICE": ALICE, "BOB": BOB, "CAROL": CAROL, "g1": g1, "g2": g2, "g3": g3}


def test_renewal_and_both_active_are_identical_rankingresult() -> None:
    """INV-6 in der schnellen Sicht: n_kante ist das Gruppenmaximum, nicht je Claim, nicht
    die Summe. Objekte direkt vergleichen, nicht zweimal dieselben Literale."""
    r_renewal, ids_renewal = _build(2, "superseded", 2, "renewal")
    r_active, ids_active = _build(2, "active", 2, "both-active")

    roles = ("ALICE", "BOB", "CAROL", "g1", "g2", "g3")
    scores_renewal = dict(r_renewal.scores)
    scores_active = dict(r_active.scores)
    by_role_renewal = {role: scores_renewal[ids_renewal[role].pub] for role in roles}
    by_role_active = {role: scores_active[ids_active[role].pub] for role in roles}

    assert by_role_renewal == by_role_active
    assert r_renewal.denominator == r_active.denominator
    assert r_renewal.mass == r_active.mass

    # Literale als zusaetzliche Zusicherung, damit der Test nicht gruen wird, wenn beide
    # Seiten gemeinsam falsch sind.
    assert by_role_renewal["g1"] == 36028797018963968
    assert r_renewal.mass == 1080863910568919040


def test_naive_per_claim_edge_would_give_wrong_n() -> None:
    """Eine Implementierung, die je Claim eine Kante zieht, liefert fuer die Erneuerung
    n=4 und damit u(g1)=72057594037927936. Das MUSS NICHT der gemessene Wert sein."""
    r, ids = _build(2, "superseded", 2, "renewal-naive-check")
    scores = dict(r.scores)
    assert scores[ids["g1"].pub] != 72057594037927936


def test_downgrade_falls_to_n_kante_1() -> None:
    """n_kante faellt sofort auf 1 (Fluss folgt dem Willen), obwohl n_budget bis t_exp
    bei 2 bleibt (Budget folgt der Uhr)."""
    r, ids = _build(2, "superseded", 1, "downgrade")
    scores = dict(r.scores)
    assert scores[ids["g1"].pub] == 18014398509481984
    assert scores[ids["g2"].pub] == 18014398509481984
    assert scores[ids["g3"].pub] == 18014398509481984
    assert r.mass == 1062849512059437056
