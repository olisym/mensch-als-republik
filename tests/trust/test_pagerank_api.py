"""Oeffentliche API: Determinismus (Abnahme Punkt 6) und Eingabevalidierung."""

from __future__ import annotations

import pytest

from mensch_als_republik.trust import RelaxParams, TrustResult, rank

from tests.helpers import Identity, scope_id, store_with
from .pr02 import RP
from .tp02 import NOW, PARAMS, T_EXP, build


def test_two_runs_are_byte_identical() -> None:
    g = build("F")
    store = g.store()
    r1 = rank(
        store, anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
        include_flagged=True,
    )
    r2 = rank(
        store, anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
        include_flagged=True,
    )
    assert r1 == r2


def test_rank_result_is_not_a_trust_result() -> None:
    """D52: eigener Rueckgabetyp, kein zusaetzliches Feld an TrustResult."""
    g = build("B")
    r = rank(
        g.store(), anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
        include_flagged=True,
    )
    assert not isinstance(r, TrustResult)
    assert not hasattr(TrustResult, "scores")
    assert not hasattr(TrustResult, "denominator")
    assert not hasattr(TrustResult, "mass")


@pytest.mark.parametrize(
    "alpha_num,alpha_den,rounds",
    [(0, 2, 20), (2, 2, 20), (3, 2, 20), (1, 2, 0)],
)
def test_relax_params_rejects_invalid_values(alpha_num, alpha_den, rounds) -> None:
    with pytest.raises(ValueError):
        RelaxParams(base=PARAMS, alpha_num=alpha_num, alpha_den=alpha_den, rounds=rounds)


def test_rank_rejects_empty_anchors() -> None:
    """denominator = len(anchors) * (bD**K) waere bei anchors=frozenset() gleich 0 --
    rank() wuerde sonst schweigend ein RankingResult mit undefiniertem Bruch liefern."""
    scope = scope_id("PR-empty-anchors")
    ALICE, BOB = Identity("pr-empty-A"), Identity("pr-empty-B")
    store = store_with(ALICE.vouch(BOB, n=4, scope=scope, t=1, t_exp=T_EXP))
    with pytest.raises(ValueError):
        rank(
            store, anchors=frozenset(), scope=scope, now=NOW, params=RP,
            include_flagged=True,
        )
