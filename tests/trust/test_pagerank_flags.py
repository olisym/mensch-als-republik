"""T-02b.2 — Flag-Laeufe (Anker PR-2, D39/K14)."""

from __future__ import annotations

from symbolon.trust import rank

from .pr02 import RP
from .tp02 import NOW, build


def test_A_false_drops_gi_and_sigma_is_7_over_8() -> None:
    g = build("A")
    r = rank(
        g.store(), anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
        include_flagged=False,
    )
    identities = {identity for identity, _ in r.scores}
    assert g.g1.pub not in identities
    assert g.g2.pub not in identities
    assert g.g3.pub not in identities
    assert r.mass == 7 * (r.denominator // 8)  # exakt, weil 8 den Nenner 2**60 teilt


def test_A_true_gi_present_sigma_17_over_16() -> None:
    g = build("A")
    r = rank(
        g.store(), anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
        include_flagged=True,
    )
    scores = dict(r.scores)
    assert scores[g.g1.pub] == scores[g.g2.pub] == scores[g.g3.pub] == 72057594037927936
    assert r.mass == 1224979098644774912


def test_D_false_is_byte_identical_to_B() -> None:
    """'Byte-gleich' meint Vektor und Summe (02b-golden-anchors.md §4) -- nicht Findings:
    D hat unabhaengig vom Flag ein eigenes OVERCOMMITTED_AUTHOR unter den gi (Sigma n=8>4
    innerhalb S), B hat keins. Zwei verschiedene Graphen mit verschiedenen Pubkeys je
    Rolle -- daher Vergleich pro Rolle (ALICE/BOB/CAROL/g1/g2/g3), nicht der rohen
    Bytes-sortierten Liste.
    """
    g_d = build("D")
    g_b = build("B")
    r_d = rank(
        g_d.store(), anchors=frozenset({g_d.ALICE.pub}), scope=g_d.scope, now=NOW, params=RP,
        include_flagged=False,
    )
    r_b = rank(
        g_b.store(), anchors=frozenset({g_b.ALICE.pub}), scope=g_b.scope, now=NOW, params=RP,
        include_flagged=True,
    )
    scores_d = dict(r_d.scores)
    scores_b = dict(r_b.scores)
    roles = ("ALICE", "BOB", "CAROL", "g1", "g2", "g3")
    by_role_d = {role: scores_d[getattr(g_d, role).pub] for role in roles}
    by_role_b = {role: scores_b[getattr(g_b, role).pub] for role in roles}
    assert by_role_d == by_role_b

    assert r_d.denominator == r_b.denominator
    assert r_d.mass == r_b.mass


def test_D_true_values() -> None:
    g = build("D")
    r = rank(
        g.store(), anchors=frozenset({g.ALICE.pub}), scope=g.scope, now=NOW, params=RP,
        include_flagged=True,
    )
    scores = dict(r.scores)
    assert scores[g.g1.pub] == scores[g.g2.pub] == scores[g.g3.pub] == 306244774661193728
    assert r.mass == 1927540640514572288
