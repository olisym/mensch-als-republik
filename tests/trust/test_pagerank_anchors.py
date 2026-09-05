"""T-02b.1 — Varianten (Anker PR-1). Literale aus 02b-golden-anchors.md §3."""

from __future__ import annotations

import pytest

from symbolon.trust import rank

from .pr02 import RP, mass_bound
from .tp02 import NOW, build

RUMPF = {
    "ALICE": 576460752303423488,
    "BOB": 288230376151711744,
    "CAROL": 144115188075855872,
}

# variant -> (u(g1), u(g2) or None, u(g3) or None, mass)
EXPECTED = {
    "B": (18014398509481984, 18014398509481984, 18014398509481984, 1062849512059437056),
    "C": (36028522141057024, 36028522141057024, 36028522141057024, 1116891882954162176),
    "D": (306244774661193728, 306244774661193728, 306244774661193728, 1927540640514572288),
    "E": (72057594037927936, 18014398509481984, 18014398509481984, 1116892707587883008),
    "E0": (72057594037927936, None, None, 1080863910568919040),
    "F": (57645708727025664, 43234189918601216, 43234189918601216, 1152920405095219200),
    "A": (72057594037927936, 72057594037927936, 72057594037927936, 1224979098644774912),
}


@pytest.mark.parametrize("variant", sorted(EXPECTED))
def test_rumpf_is_identical_across_variants(variant: str) -> None:
    g = build(variant)
    r = rank(
        g.store(), anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
        include_flagged=True,
    )
    scores = dict(r.scores)
    assert scores[g.ALICE.pub] == RUMPF["ALICE"]
    assert scores[g.BOB.pub] == RUMPF["BOB"]
    assert scores[g.CAROL.pub] == RUMPF["CAROL"]


@pytest.mark.parametrize("variant", sorted(EXPECTED))
def test_variant_values_and_mass(variant: str) -> None:
    g = build(variant)
    r = rank(
        g.store(), anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
        include_flagged=True,
    )
    scores = dict(r.scores)
    e1, e2, e3, emass = EXPECTED[variant]

    assert scores.get(g.g1.pub) == e1
    assert scores.get(g.g2.pub) == e2
    assert scores.get(g.g3.pub) == e3
    assert r.mass == emass
    assert r.denominator == 8**20


def test_E0_g2_g3_absent_from_scores() -> None:
    g = build("E0")
    r = rank(
        g.store(), anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
        include_flagged=True,
    )
    identities = {identity for identity, _ in r.scores}
    assert g.g2.pub not in identities
    assert g.g3.pub not in identities


def test_F_is_the_sharpest_ordering_vector() -> None:
    """Sigma t = 1 - 2**-20 exakt -- die empfindlichste Einzelzahl der Datei."""
    g = build("F")
    r = rank(
        g.store(), anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
        include_flagged=True,
    )
    assert r.mass == 1152920405095219200
    assert r.mass == mass_bound(r.denominator, 1, RP)
