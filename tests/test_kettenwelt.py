"""Kettenwelt: der Schlüsselsatz wandert mit der Epoche (D183, D190)."""

from __future__ import annotations

from mensch_als_republik.keys import resolve_authorized_keys
from mensch_als_republik.profiles.policy import resolve_policy
from mensch_als_republik.resolve import resolve_state
from tests.helpers import Identity
from tests.kettenwelt import Kettenwelt, kettenwelt


def _welt() -> tuple[Kettenwelt, Identity, Identity, Identity]:
    a = Identity("A")
    b = Identity("B")
    c = Identity("C")
    people = sorted([a.pub, b.pub, c.pub])
    schwellen = {
        "ordinary": [1, 2],
        "membership": [1, 2],
        "amendment": [1, 2],
    }
    basis = {
        "irrevocable_predicates": ["obligation@1", "ratify@1", "vote@1"],
        "thresholds": schwellen,
        "arbitration": {"arbitrators": people},
        "participants": people,
    }
    erste = dict(basis)
    zweite = dict(basis)
    zweite["nucleus_keys"] = [b.pub]
    welt = kettenwelt(
        identitaeten=(a, b, c),
        root_keys=(a.pub,),
        verfassungen=(erste, zweite),
    )
    return welt, a, b, c


def test_kettenwelt_authorized_keys_follow_epoch() -> None:
    """Ein Fehlgriff in der Epoche liefert einen anderen Schlüsselsatz (D183, D190)."""
    welt, a, b, _c = _welt()
    state = resolve_state(
        welt.store,
        scope=welt.scope,
        genesis_obj=welt.genesis_obj,
        known_constitutions=welt.known_constitutions,
        known_proposals=welt.known_proposals,
        now=welt.now,
    )
    assert state.epoch == welt.epochen[1]
    assert state.constitution_obj == welt.verfassungen[1]
    assert state.authorized_keys == frozenset([b.pub])
    from_first = resolve_authorized_keys(
        welt.store,
        scope=welt.scope,
        genesis_obj=welt.genesis_obj,
        constitution_hash=welt.verfassungs_hashes[0],
        constitution_obj=welt.verfassungen[0],
        now=welt.now,
        policy=resolve_policy(
            scope=welt.scope,
            genesis_obj=welt.genesis_obj,
            constitution_hash=welt.verfassungs_hashes[0],
            constitution_obj=welt.verfassungen[0],
        ).policy,
    )
    assert from_first.keys == frozenset(welt.genesis_obj[1])
    assert from_first.keys == frozenset([a.pub])
    assert state.authorized_keys != from_first.keys


def test_kettenwelt_chain_has_no_findings() -> None:
    """Die Kette läuft ohne Vermerke (D190)."""
    welt, _a, _b, _c = _welt()
    state = resolve_state(
        welt.store,
        scope=welt.scope,
        genesis_obj=welt.genesis_obj,
        known_constitutions=welt.known_constitutions,
        known_proposals=welt.known_proposals,
        now=welt.now,
    )
    assert state.epoch_findings == ()
    assert state.policy_findings == ()
    assert state.key_findings == ()
