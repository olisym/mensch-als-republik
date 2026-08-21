"""Governance-Schicht — Epochen, Auszählung, Ratifizierung (04-governance.md)."""

from __future__ import annotations

from mensch_als_republik.governance.chain import EpochResolution, resolve_epoch
from mensch_als_republik.governance.epoch import RatificationResult, verify_ratification
from mensch_als_republik.governance.findings import Finding, GovernanceFinding
from mensch_als_republik.governance.objects import Epoch, Proposal, epoch_id, proposal_hash
from mensch_als_republik.governance.tally import TallyResult, TallyState, decide

__all__ = [
    "Epoch",
    "EpochResolution",
    "Finding",
    "GovernanceFinding",
    "Proposal",
    "RatificationResult",
    "TallyResult",
    "TallyState",
    "decide",
    "epoch_id",
    "proposal_hash",
    "resolve_epoch",
    "verify_ratification",
]
