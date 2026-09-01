"""Träger für vier Doppelerzeuger der Governance (D287)."""

from __future__ import annotations

import hashlib

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import claim_id
from mensch_als_republik.domains import DOM_NUC_GEN
from mensch_als_republik.governance import verify_ratification
from mensch_als_republik.governance.findings import GovernanceFinding
from mensch_als_republik.governance.objects import Epoch, Proposal
from mensch_als_republik.governance.tally import (
    TallyResult,
    TallyState,
    constitution_governable,
    decide,
    read_v,
)
from mensch_als_republik.policy import constitution_hash
from tests.helpers import store_with

from .fixtures import (
    ALICE,
    C1,
    C2,
    CONSTITUTION_HASH_2,
    EPOCH_1,
    NOW,
    PROPOSAL_1,
    fresh_alice,
    policy_of,
    ratify_claim,
)


def test_read_v_canonical_non_map() -> None:
    """Kanonische Zahl statt Map: UNPARSABLE_V (03 §1.3, D276, D287)."""
    obj, kind = read_v(cbor_canon.encode(1))
    assert obj is None
    assert kind is GovernanceFinding.UNPARSABLE_V


def test_participants_is_map() -> None:
    """participants als Map: MALFORMED_PARTICIPANTS (04 §3.5, D287)."""
    constitution = dict(C1)
    constitution["participants"] = {ALICE.pub: 1}
    assert constitution_governable(constitution) is GovernanceFinding.MALFORMED_PARTICIPANTS


def test_threshold_class_missing() -> None:
    """thresholds keine Map: MALFORMED_THRESHOLD (04 §3, D287)."""
    constitution = dict(C1)
    constitution["thresholds"] = 1
    ch = constitution_hash(constitution)
    genesis = {
        0: 1,
        1: [ALICE.pub],
        2: 0,
        3: [ALICE.pub],
        4: ch,
        5: 2,
        6: 0,
        7: 0,
    }
    scope = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    epoch = Epoch(scope=scope, index=1, constitution_hash=ch)
    proposal = Proposal(
        scope=scope,
        predecessor=epoch.epoch_id,
        constitution_hash=CONSTITUTION_HASH_2,
    )
    result = decide(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        genesis_obj=genesis,
        constitution_obj=constitution,
        target_constitution_obj=C2,
        known_proposals={proposal.proposal_hash: proposal},
        now=NOW,
    )
    assert result.state is TallyState.UNEVALUABLE
    assert result.findings[0].kind is GovernanceFinding.MALFORMED_THRESHOLD


def test_tally_without_participants() -> None:
    """Auszählung ohne Teilnehmermenge: TALLY_UNEVALUABLE (04 §3, D287)."""
    alice = fresh_alice()
    ratify = ratify_claim(alice, PROPOSAL_1, witnesses=[], t=10)
    tally = TallyResult(
        state=TallyState.PASSED,
        yes=(),
        no=(),
        participants=None,
        threshold=None,
        findings=(),
        epoch_id=EPOCH_1.epoch_id,
        proposal_hash=PROPOSAL_1.proposal_hash,
    )
    result = verify_ratification(
        store_with(ratify),
        ratify=ratify,
        epoch=EPOCH_1,
        proposal=PROPOSAL_1,
        tally=tally,
        target_constitution_obj=C2,
        now=NOW,
        policy=policy_of(C1),
    )
    assert result.next_epoch is None
    assert result.findings[0].kind is GovernanceFinding.TALLY_UNEVALUABLE
    assert result.findings[0].subject == claim_id(ratify)
