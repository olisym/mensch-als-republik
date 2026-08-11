"""T-02.8 — include_flagged (Default False, D39). INV-8: Findings/Budget unveraendert."""

from __future__ import annotations

import pytest

from mensch_als_republik.trust import TrustFinding, trust

from .tp02 import NOW, PARAMS, build, build_A_prime

# variant -> (values with True, values with False)
_TABLE = {
    "A": ((4, 4, 4, 4), (0, 0, 0, 0)),
    "D": ((3, 3, 3, 3), (1, 1, 1, 3)),
}


@pytest.mark.parametrize("variant", sorted(_TABLE))
def test_include_flagged_changes_values(variant: str) -> None:
    g = build(variant)
    store = g.store()
    anchors = frozenset({g.ALICE.pub})
    targets_individual = (g.g1, g.g2, g.g3)
    targets_all = frozenset({g.g1.pub, g.g2.pub, g.g3.pub})

    (e1t, e2t, e3t, esimt), (e1f, e2f, e3f, esimf) = _TABLE[variant]

    for target, expected in zip(targets_individual, (e1t, e2t, e3t)):
        r = trust(
            store, anchors=anchors, targets=frozenset({target.pub}), scope=g.scope,
            now=NOW, params=PARAMS, include_flagged=True,
        )
        assert r.value == expected

    for target, expected in zip(targets_individual, (e1f, e2f, e3f)):
        r = trust(
            store, anchors=anchors, targets=frozenset({target.pub}), scope=g.scope,
            now=NOW, params=PARAMS, include_flagged=False,
        )
        assert r.value == expected

    r_sim_true = trust(
        store, anchors=anchors, targets=targets_all, scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=True,
    )
    r_sim_false = trust(
        store, anchors=anchors, targets=targets_all, scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=False,
    )
    assert r_sim_true.value == esimt
    assert r_sim_false.value == esimf


@pytest.mark.parametrize("variant", ["C", "F"])
def test_include_flagged_no_effect_without_flags(variant: str) -> None:
    g = build(variant)
    store = g.store()
    anchors = frozenset({g.ALICE.pub})
    targets_all = frozenset({g.g1.pub, g.g2.pub, g.g3.pub})

    r_true = trust(
        store, anchors=anchors, targets=targets_all, scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=True,
    )
    r_false = trust(
        store, anchors=anchors, targets=targets_all, scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=False,
    )
    assert r_true.value == r_false.value
    assert r_true.findings == r_false.findings


def test_include_flagged_A_prime() -> None:
    g = build_A_prime()
    anchors = frozenset({g.ALICE.pub})
    targets = frozenset({g.g1.pub, g.g2.pub, g.g3.pub})
    store = g.store()

    r_true = trust(
        store, anchors=anchors, targets=targets, scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=True,
    )
    r_false = trust(
        store, anchors=anchors, targets=targets, scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=False,
    )
    assert r_true.value == 16
    assert r_false.value == 0


@pytest.mark.parametrize("variant", sorted(_TABLE) + ["C", "F"])
def test_INV8_findings_and_budget_identical_across_flag(variant: str) -> None:
    g = build(variant)
    store = g.store()
    anchors = frozenset({g.ALICE.pub})
    targets_all = frozenset({g.g1.pub, g.g2.pub, g.g3.pub})

    r_true = trust(
        store, anchors=anchors, targets=targets_all, scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=True,
    )
    r_false = trust(
        store, anchors=anchors, targets=targets_all, scope=g.scope,
        now=NOW, params=PARAMS, include_flagged=False,
    )
    assert r_true.findings == r_false.findings

    overcommitted_true = {
        f.subject for f in r_true.findings if f.kind == TrustFinding.OVERCOMMITTED_AUTHOR
    }
    overcommitted_false = {
        f.subject for f in r_false.findings if f.kind == TrustFinding.OVERCOMMITTED_AUTHOR
    }
    assert overcommitted_true == overcommitted_false
