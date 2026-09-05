"""Oeffentliche API: Determinismus (Abnahme Punkt 4) und Eingabevalidierung."""

from __future__ import annotations

import pytest

from symbolon.trust import trust

from .tp02 import NOW, PARAMS, build


def test_two_runs_are_byte_identical() -> None:
    g = build("F")
    store = g.store()
    anchors = frozenset({g.ALICE.pub})
    targets = frozenset({g.g1.pub, g.g2.pub, g.g3.pub})

    r1 = trust(
        store, anchors=anchors, targets=targets, scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=True,
    )
    r2 = trust(
        store, anchors=anchors, targets=targets, scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=True,
    )
    assert r1 == r2


def test_anchors_targets_overlap_raises() -> None:
    g = build("B")
    shared = frozenset({g.ALICE.pub, g.g1.pub})
    with pytest.raises(ValueError):
        trust(
            g.store(), anchors=shared, targets=frozenset({g.g1.pub}), scope=g.scope,
            now=NOW, params=PARAMS,
        )


def test_findings_are_sorted_and_deduplicated() -> None:
    g = build("A")
    r = trust(
        g.store(), anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}), scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=True,
    )
    assert list(r.findings) == sorted(set(r.findings))
    assert len(r.findings) == len(set(r.findings))
