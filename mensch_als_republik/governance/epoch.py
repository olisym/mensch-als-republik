"""Materialisierung einer gesättigten Entscheidung (04-governance.md §4)."""

from __future__ import annotations

from dataclasses import dataclass

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import Claim, claim_id
from mensch_als_republik.governance.findings import (
    Finding,
    GovernanceFinding,
    dedupe_sort,
)
from mensch_als_republik.governance.objects import Epoch, Proposal
from mensch_als_republik.governance.tally import (
    TallyResult,
    TallyState,
    constitution_governable,
    reached,
)
from mensch_als_republik.index import classify_all
from mensch_als_republik.policy import NucleusPolicy, constitution_hash
from mensch_als_republik.predicates import is_nuc_name
from mensch_als_republik.verifier import ClaimStore, State


@dataclass(frozen=True, slots=True)
class RatificationResult:
    """Ergebnis von ``verify_ratification`` (04-governance.md §4.1, D99)."""

    next_epoch: Epoch | None
    findings: tuple[Finding, ...]


def _cited(ratify: Claim) -> list[object] | None:
    if ratify.v is None:
        return None
    try:
        obj = cbor_canon.decode(ratify.v)
    except Exception:
        return None
    if not isinstance(obj, dict):
        return None
    cited = obj.get(0)
    if not isinstance(cited, list):
        return None
    return cited


def _unsupported(ratify: Claim) -> RatificationResult:
    return RatificationResult(
        next_epoch=None,
        findings=dedupe_sort(
            [Finding(kind=GovernanceFinding.UNSUPPORTED_RATIFICATION, subject=claim_id(ratify))]
        ),
    )


def verify_ratification(
    store: ClaimStore,
    *,
    ratify: Claim,
    epoch: Epoch,
    proposal: Proposal,
    tally: TallyResult,
    target_constitution_obj: dict | None,
    now: int,
    policy: NucleusPolicy | None = None,
) -> RatificationResult:
    """Prüft ein ``ratify@1`` gegen eine Auszählung (04-governance.md §4.1, D106, D109, D112, D200)."""
    if (
        proposal.scope != epoch.scope
        or tally.epoch_id != epoch.epoch_id
        or tally.proposal_hash != proposal.proposal_hash
    ):
        raise ValueError("tally does not match epoch and proposal")
    if tally.state is TallyState.UNEVALUABLE:
        return RatificationResult(
            next_epoch=None,
            findings=dedupe_sort(
                [
                    Finding(
                        kind=GovernanceFinding.TALLY_UNEVALUABLE,
                        subject=claim_id(ratify),
                    ),
                    *tally.findings,
                ]
            ),
        )
    if tally.participants is None:
        return RatificationResult(
            next_epoch=None,
            findings=dedupe_sort(
                [
                    Finding(
                        kind=GovernanceFinding.TALLY_UNEVALUABLE,
                        subject=claim_id(ratify),
                    )
                ]
            ),
        )
    if (
        target_constitution_obj is None
        or constitution_hash(target_constitution_obj) != proposal.constitution_hash
    ):
        raise ValueError("target_constitution_obj does not match proposal")
    participants = tally.participants
    if ratify.N != epoch.scope or ratify.J != (3, proposal.proposal_hash):
        return _unsupported(ratify)
    if not is_nuc_name(ratify, "ratify"):
        return _unsupported(ratify)
    if ratify.I not in participants:
        return _unsupported(ratify)
    if ratify.t_exp is not None:
        return RatificationResult(
            next_epoch=None,
            findings=dedupe_sort(
                [Finding(kind=GovernanceFinding.RATIFY_WITH_EXPIRY, subject=claim_id(ratify))]
            ),
        )
    by_cid = classify_all(store, now, policy)
    rid = claim_id(ratify)
    if rid not in by_cid or by_cid[rid].state is not State.ACTIVE:
        return _unsupported(ratify)
    cited = _cited(ratify)
    if cited is None:
        return _unsupported(ratify)
    witness_findings: list[Finding] = []
    authors: list[bytes] = []
    for cid in cited:
        if not isinstance(cid, bytes):
            witness_findings.append(
                Finding(kind=GovernanceFinding.UNSUPPORTED_RATIFICATION, subject=rid)
            )
            continue
        present = store.get(cid)
        if present is None:
            witness_findings.append(
                Finding(kind=GovernanceFinding.UNKNOWN_WITNESS_VOTE, subject=cid)
            )
        elif cid not in tally.yes:
            witness_findings.append(
                Finding(kind=GovernanceFinding.UNSUPPORTED_RATIFICATION, subject=cid)
            )
        else:
            authors.append(present.I)
    if witness_findings:
        return RatificationResult(
            next_epoch=None, findings=dedupe_sort(witness_findings)
        )
    if len(authors) != len(set(authors)):
        return _unsupported(ratify)
    if tally.threshold is None or tally.n is None:
        return _unsupported(ratify)
    num, den = tally.threshold
    if not reached(len(cited), tally.n, num, den):
        return _unsupported(ratify)
    kind = constitution_governable(target_constitution_obj)
    if kind is not None:
        return RatificationResult(
            next_epoch=None,
            findings=dedupe_sort(
                [Finding(kind=kind, subject=proposal.constitution_hash)]
            ),
        )
    return RatificationResult(
        next_epoch=Epoch(
            scope=epoch.scope,
            index=epoch.index + 1,
            constitution_hash=proposal.constitution_hash,
        ),
        findings=(),
    )
