"""T-02.1 (Anker 1-3, sieben Varianten) und T-02.1b (Quellanbindung, A')."""

from __future__ import annotations

import pytest

from symbolon.trust import TrustFinding, trust

from .tp02 import NOW, PARAMS, build, build_A_prime

# Var -> (trust g1, trust g2, trust g3, simultan)
EXPECTED = {
    "A": (4, 4, 4, 4),
    "B": (1, 1, 1, 3),
    "C": (3, 3, 3, 3),
    "D": (3, 3, 3, 3),
    "E": (4, 1, 1, 4),
    "E0": (4, 0, 0, 4),
    "F": (4, 3, 3, 4),
}


@pytest.mark.parametrize("variant", sorted(EXPECTED))
def test_individual_and_simultaneous(variant: str) -> None:
    g = build(variant)
    store = g.store()
    e1, e2, e3, esim = EXPECTED[variant]

    for target, expected in ((g.g1, e1), (g.g2, e2), (g.g3, e3)):
        r = trust(
            store,
            anchors=frozenset({g.ALICE.pub}),
            targets=frozenset({target.pub}),
            scope=g.scope,
            now=NOW,
            params=PARAMS,
            include_flagged=True,
        )
        assert r.value == expected, f"{variant} -> {target.label}"

    r_sim = trust(
        store,
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}),
        scope=g.scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    assert r_sim.value == esim, f"{variant} simultan"


def test_A_overcommitted_author_carol() -> None:
    g = build("A")
    r = trust(
        g.store(),
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.g1.pub}),
        scope=g.scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    assert any(
        f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == g.CAROL.pub
        for f in r.findings
    )


def test_D_overcommitted_authors_gi() -> None:
    g = build("D")
    r = trust(
        g.store(),
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}),
        scope=g.scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    flagged = {f.subject for f in r.findings if f.kind == TrustFinding.OVERCOMMITTED_AUTHOR}
    assert flagged == {g.g1.pub, g.g2.pub, g.g3.pub}
    assert g.CAROL.pub not in flagged


@pytest.mark.parametrize("variant", ["B", "C", "D", "E", "E0", "F"])
def test_no_overcommitted_carol(variant: str) -> None:
    g = build(variant)
    r = trust(
        g.store(),
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}),
        scope=g.scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    assert not any(
        f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == g.CAROL.pub
        for f in r.findings
    )


def test_E_subgranular_edges() -> None:
    """d(g2)=d(g3)=4, C=1 => g2->g1, g2->g3, g3->g1, g3->g2 sind alle null (vier Findings).

    Nur g1->g2 und g1->g3 tragen (C(g1)=2)."""
    g = build("E")
    r = trust(
        g.store(),
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.g2.pub}),
        scope=g.scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    subgranular = [f for f in r.findings if f.kind == TrustFinding.SUBGRANULAR_VOUCH]
    assert len(subgranular) == 4


@pytest.mark.parametrize("variant", sorted(EXPECTED))
def test_alice_to_eve_is_zero(variant: str) -> None:
    g = build(variant)
    r = trust(
        g.store(),
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.EVE.pub}),
        scope=g.scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    assert r.value == 0


def test_cut_A_simultaneous_is_carol() -> None:
    g = build("A")
    r = trust(
        g.store(),
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}),
        scope=g.scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    assert r.cut == (g.CAROL.pub,)


def test_cut_F_simultaneous_is_carol() -> None:
    g = build("F")
    r = trust(
        g.store(),
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}),
        scope=g.scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    assert r.cut == (g.CAROL.pub,)


def test_cut_B_simultaneous_is_empty() -> None:
    g = build("B")
    r = trust(
        g.store(),
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}),
        scope=g.scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    assert r.cut == ()


# --- T-02.1b: Quellanbindung a_in vs a_out, Vektor A' ---


def test_A_prime_overcommitted_alice() -> None:
    g = build_A_prime()
    r = trust(
        g.store(),
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}),
        scope=g.scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    assert any(
        f.kind == TrustFinding.OVERCOMMITTED_AUTHOR and f.subject == g.ALICE.pub
        for f in r.findings
    )


def test_A_prime_individual_is_16() -> None:
    g = build_A_prime()
    store = g.store()
    for target in (g.g1, g.g2, g.g3):
        r = trust(
            store,
            anchors=frozenset({g.ALICE.pub}),
            targets=frozenset({target.pub}),
            scope=g.scope,
            now=NOW,
            params=PARAMS,
            include_flagged=True,
        )
        assert r.value == 16


def test_A_prime_simultaneous_is_16_not_48() -> None:
    """K4 auf a_in: der Satz aus 02 §4 haelt mit Gleichheit; a_out-Fehler liefert 48."""
    g = build_A_prime()
    r = trust(
        g.store(),
        anchors=frozenset({g.ALICE.pub}),
        targets=frozenset({g.g1.pub, g.g2.pub, g.g3.pub}),
        scope=g.scope,
        now=NOW,
        params=PARAMS,
        include_flagged=True,
    )
    assert r.value == 16
    assert r.cut == (g.ALICE.pub,)
