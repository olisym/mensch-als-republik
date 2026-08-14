"""Governance-Schicht — Epochen, Auszählung, Ratifizierung (04-governance.md)."""

from __future__ import annotations

from mensch_als_republik.governance.epoch import RatificationResult, verify_ratification
from mensch_als_republik.governance.findings import Finding, GovernanceFinding
from mensch_als_republik.governance.objects import Epoch, Proposal, epoch_id, proposal_hash
from mensch_als_republik.governance.tally import TallyResult, TallyState, decide

__all__ = [
    "Epoch",
    "Finding",
    "GovernanceFinding",
    "Proposal",
    "RatificationResult",
    "TallyResult",
    "TallyState",
    "decide",
    "epoch_id",
    "proposal_hash",
    "verify_ratification",
]
