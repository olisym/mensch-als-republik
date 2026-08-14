"""P-3 — Die Vorbehalte von P-2, positiv (fuzz-prompt.md §3).

P-3a: mit ``erlaube_ueberzeichnung = True`` existieren Welten, in denen eine
Teilmenge höheres Vertrauen liefert (D118). Kleinstes Gegenbeispiel: zwei
Vouches mit n = 51 bei D = 100.

P-3b: mit ``erlaube_equivocation = True`` existieren Welten, in denen ein
zusätzlicher Claim eine zählende Stimme entfernt und PASSED auf PENDING
zurückfällt (D117).

Beide sind erwartete Verletzungen. Ein Lauf, der keine findet, ist der Befund.
"""

from __future__ import annotations

from hypothesis import find, settings

from mensch_als_republik.governance.tally import TallyState
from mensch_als_republik.trust.params import TrustParams

from tests.property.welten import (
    EX,
    Welt,
    _SEEDS,
    _Signer,
    _nuc,
    _vote_v,
    _vouch_v,
    auszaehlung,
    hoeheres_vertrauen,
    speicher,
    teilmengen,
    welten,
)


def _p3a_verletzt(welt: Welt) -> bool:
    claims = welt.vouches
    if len(claims) < 2:
        return False
    voll = speicher(*claims)
    for subset in teilmengen(claims, welt):
        if hoeheres_vertrauen(speicher(*subset), voll, welt):
            return True
    return False


def _p3b_verletzt(welt: Welt) -> bool:
    claims = welt.claims
    if not welt.votes:
        return False
    voll = auszaehlung(speicher(*claims), welt)
    if voll.state is not TallyState.PENDING:
        return False
    for subset in teilmengen(claims, welt):
        if auszaehlung(speicher(*subset), welt).state is TallyState.PASSED:
            return True
    return False


def test_p3a_finds_overcommit_violation() -> None:
    welt = find(
        welten(erlaube_ueberzeichnung=True, erlaube_equivocation=False),
        _p3a_verletzt,
        settings=settings(),
    )
    assert _p3a_verletzt(welt)
    assert len(welt.vouches) >= 2


def test_p3a_smallest_vector_two_vouches_n51() -> None:
    """D118, mitgeliefert: zwei Vouches n=51, D=100 — Teilmenge über-vertraut."""
    anna = _Signer(_SEEDS[0])
    bruno = _Signer(_SEEDS[1])
    chris = _Signer(_SEEDS[2])
    v1 = anna.claim(
        p=_nuc(EX.N_res, "vouch"),
        J=(1, bruno.pub),
        v=_vouch_v(51),
        N=EX.N_res,
    )
    v2 = anna.claim(
        p=_nuc(EX.N_res, "vouch"),
        J=(1, chris.pub),
        v=_vouch_v(51),
        N=EX.N_res,
    )
    welt = Welt(
        pubs=(anna.pub, bruno.pub, chris.pub),
        anchors=frozenset({anna.pub}),
        params=TrustParams(C0=100, gamma_num=1, gamma_den=2, D=100),
        vouches=(v1, v2),
        votes=(),
        delivery=(frozenset({0}), frozenset({0, 1}), frozenset()),
        now=1000,
    )
    assert hoeheres_vertrauen(speicher(v1), speicher(v1, v2), welt)


def test_p3b_finds_equivocation_passed_to_pending() -> None:
    welt = find(
        welten(erlaube_ueberzeichnung=False, erlaube_equivocation=True),
        _p3b_verletzt,
        settings=settings(),
    )
    assert _p3b_verletzt(welt)


def test_p3b_vector_twin_vote_drops_passed() -> None:
    """D117, mitgeliefert: Anna ja+nein dasselbe h_prev, Chris ja — PASSED fällt."""
    anna = _Signer(_SEEDS[0])
    _bruno = _Signer(_SEEDS[1])
    chris = _Signer(_SEEDS[2])
    yes = anna.claim(
        p=_nuc(EX.N_gov, "vote"),
        J=(3, EX.proposal.proposal_hash),
        v=_vote_v(1),
        N=EX.N_gov,
        kette_fortschreiben=False,
    )
    no = anna.claim(
        p=_nuc(EX.N_gov, "vote"),
        J=(3, EX.proposal.proposal_hash),
        v=_vote_v(0),
        N=EX.N_gov,
    )
    chris_yes = chris.claim(
        p=_nuc(EX.N_gov, "vote"),
        J=(3, EX.proposal.proposal_hash),
        v=_vote_v(1),
        N=EX.N_gov,
    )
    welt = Welt(
        pubs=(anna.pub, _bruno.pub, chris.pub),
        anchors=frozenset({anna.pub, _bruno.pub}),
        params=TrustParams(C0=100, gamma_num=1, gamma_den=2, D=100),
        vouches=(),
        votes=(yes, no, chris_yes),
        delivery=(frozenset(), frozenset({0, 2}), frozenset({1, 2})),
        now=1000,
    )
    assert auszaehlung(speicher(yes, chris_yes), welt).state is TallyState.PASSED
    assert auszaehlung(speicher(yes, no, chris_yes), welt).state is TallyState.PENDING
