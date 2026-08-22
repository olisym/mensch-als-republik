"""Subjekte der Auszählungsvermerke (04-governance.md §3.5, D198)."""

from __future__ import annotations

import hashlib

from mensch_als_republik import cbor_canon
from mensch_als_republik.domains import DOM_NUC_GEN
from mensch_als_republik.governance.findings import GovernanceFinding
from mensch_als_republik.governance.objects import Epoch, Proposal
from mensch_als_republik.governance.tally import TallyState
from mensch_als_republik.policy import constitution_hash
from tests.helpers import store_with

from .fixtures import C2, C3, GENESIS_D, N_D, _tally


def _paar(cons, ziel, *, scope=N_D, index=2):
    epoch = Epoch(
        scope=scope, index=index, constitution_hash=constitution_hash(cons)
    )
    proposal = Proposal(
        scope=scope,
        predecessor=epoch.epoch_id,
        constitution_hash=constitution_hash(ziel),
    )
    return epoch, proposal


def test_malformed_threshold_in_target_addresses_proposal() -> None:
    """Formwidrige Schwelle in der Zielverfassung adressiert deren Hash (04 §3.5, D198)."""
    ziel = dict(C2)
    ziel["thresholds"] = dict(C2["thresholds"])
    ziel["thresholds"]["amendment"] = [3, 2]
    epoch, proposal = _paar(C2, ziel)
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=C2,
        target=ziel,
        known={proposal.proposal_hash: proposal},
    )
    assert result.state is TallyState.UNEVALUABLE
    assert len(result.findings) == 1
    assert result.findings[0].kind == GovernanceFinding.MALFORMED_THRESHOLD
    assert result.findings[0].subject == proposal.constitution_hash
    assert result.findings[0].subject != epoch.constitution_hash


def test_unsupported_weight_mode_addresses_scope() -> None:
    """genesis[6] ≠ 0 adressiert den Scope (04 §3.5, D198)."""
    genesis = dict(GENESIS_D)
    genesis[6] = 1
    scope = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    epoch, proposal = _paar(C2, C3, scope=scope)
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=C2,
        target=C3,
        genesis=genesis,
        known={proposal.proposal_hash: proposal},
    )
    assert result.state is TallyState.UNEVALUABLE
    assert len(result.findings) == 1
    assert result.findings[0].kind == GovernanceFinding.UNSUPPORTED_WEIGHT_MODE
    assert result.findings[0].subject == epoch.scope


def test_malformed_genesis_threshold_addresses_scope() -> None:
    """genesis[5] außerhalb der Klassen adressiert den Scope (04 §3.5, D198)."""
    genesis = dict(GENESIS_D)
    genesis[5] = 3
    scope = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis)).digest()
    epoch, proposal = _paar(C2, C3, scope=scope)
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=C2,
        target=C3,
        genesis=genesis,
        known={proposal.proposal_hash: proposal},
    )
    assert result.state is TallyState.UNEVALUABLE
    assert len(result.findings) == 1
    assert result.findings[0].kind == GovernanceFinding.MALFORMED_THRESHOLD
    assert result.findings[0].subject == epoch.scope


def test_participants_undeclared_addresses_epoch_constitution() -> None:
    """participants fehlt in der Epochenverfassung: Subjekt ist deren Hash (D200)."""
    cons = dict(C2)
    del cons["participants"]
    epoch, proposal = _paar(cons, C3)
    result = _tally(
        store_with(),
        epoch=epoch,
        proposal=proposal,
        constitution=cons,
        target=C3,
        known={proposal.proposal_hash: proposal},
    )
    assert result.state is TallyState.UNEVALUABLE
    assert len(result.findings) == 1
    assert result.findings[0].kind == GovernanceFinding.PARTICIPANTS_UNDECLARED
    assert result.findings[0].subject == epoch.constitution_hash
    assert result.findings[0].subject != proposal.constitution_hash
