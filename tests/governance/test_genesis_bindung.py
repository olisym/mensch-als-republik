"""D145 — Genesis-Bindung: was die Prüfung in ``decide`` verhindert."""

from __future__ import annotations

import pytest

from mensch_als_republik.governance.tally import reached
from tests.helpers import store_with

from .fixtures import (
    C1_AMEND,
    EPOCH_1,
    GENESIS_D,
    P1,
    PROPOSAL_AMEND_E1,
    _tally,
    _thresholds,
    fresh_p1,
    vote,
)


def test_D145_unbound_ordinary_genesis_does_not_pass_amendment() -> None:
    genesis = dict(GENESIS_D)
    genesis[5] = 0
    n = len(P1)
    ordinary = _thresholds()["ordinary"]
    amendment = _thresholds()["amendment"]
    yes_count = next(
        k
        for k in range(n + 1)
        if reached(k, n, ordinary[0], ordinary[1])
        and not reached(k, n, amendment[0], amendment[1])
    )
    identities = fresh_p1()[:yes_count]
    store = store_with(
        *(vote(identity, PROPOSAL_AMEND_E1, choice=1, t=1) for identity in identities)
    )
    with pytest.raises(ValueError, match="genesis_obj does not match epoch scope"):
        _tally(
            store,
            epoch=EPOCH_1,
            proposal=PROPOSAL_AMEND_E1,
            target=C1_AMEND,
            genesis=genesis,
        )
