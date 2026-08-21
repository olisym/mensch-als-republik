"""Epochenkette aus aufeinanderfolgenden Übergängen (04-governance.md §4.5, D174)."""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from dataclasses import dataclass

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import Claim
from mensch_als_republik.domains import DOM_NUC_GEN
from mensch_als_republik.governance.epoch import verify_ratification
from mensch_als_republik.governance.findings import (
    Finding,
    GovernanceFinding,
    dedupe_sort,
)
from mensch_als_republik.governance.objects import Epoch, Proposal
from mensch_als_republik.governance.tally import decide
from mensch_als_republik.policy import constitution_hash
from mensch_als_republik.predicates import parse_predicate
from mensch_als_republik.profiles.policy import resolve_policy
from mensch_als_republik.verifier import ClaimStore


@dataclass(frozen=True, slots=True)
class EpochResolution:
    """Ergebnis von ``resolve_epoch`` (04-governance.md §4.5, D174)."""

    epoch: Epoch
    constitution_obj: dict | None
    findings: tuple[Finding, ...]


def _is_nuc_name(claim: Claim, name: str) -> bool:
    try:
        parsed = parse_predicate(claim.p)
    except Exception:
        return False
    return (
        parsed.namespace == "nuc"
        and parsed.name == name
        and parsed.version == "1"
    )


def _known_constitution(known: Mapping[bytes, dict], h: bytes) -> dict | None:
    obj = known.get(h)
    if obj is None or constitution_hash(obj) != h:
        return None
    return obj


def _known_proposal(known: Mapping[bytes, Proposal], h: bytes) -> Proposal | None:
    value = known.get(h)
    if value is None or value.proposal_hash != h:
        return None
    return value


def resolve_epoch(
    store: ClaimStore,
    *,
    scope: bytes,
    genesis_obj: dict,
    known_constitutions: Mapping[bytes, dict],
    known_proposals: Mapping[bytes, Proposal],
    now: int,
) -> EpochResolution:
    """Leitet die geltende Epoche aus der Kette der Übergänge her (04-governance.md §4.5)."""
    computed = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis_obj)).digest()
    if scope != computed:
        raise ValueError("genesis_obj does not match scope")

    epoch = Epoch(scope=scope, index=1, constitution_hash=genesis_obj[4])
    ratifies = [
        c
        for c in store.all_claims()
        if _is_nuc_name(c, "ratify") and c.N == scope
    ]

    while True:
        constitution_obj = _known_constitution(
            known_constitutions, epoch.constitution_hash
        )
        policy = resolve_policy(
            scope=scope,
            genesis_obj=genesis_obj,
            constitution_hash=epoch.constitution_hash,
            constitution_obj=constitution_obj,
        ).policy

        findings: list[Finding] = []
        by_proposal: dict[bytes, tuple[Proposal, list[Claim]]] = {}
        for claim in ratifies:
            proposal = _known_proposal(known_proposals, claim.J[1])
            if proposal is None:
                findings.append(
                    Finding(
                        kind=GovernanceFinding.EPOCH_PROPOSAL_UNAVAILABLE,
                        subject=claim.J[1],
                    )
                )
                continue
            if proposal.predecessor != epoch.epoch_id:
                continue
            group = by_proposal.get(proposal.proposal_hash)
            if group is None:
                by_proposal[proposal.proposal_hash] = (proposal, [claim])
            else:
                group[1].append(claim)

        carrying: dict[bytes, Epoch] = {}
        for proposal, claims in by_proposal.values():
            target = _known_constitution(
                known_constitutions, proposal.constitution_hash
            )
            tally = decide(
                store,
                epoch=epoch,
                proposal=proposal,
                genesis_obj=genesis_obj,
                constitution_obj=constitution_obj,
                target_constitution_obj=target,
                known_proposals=known_proposals,
                now=now,
                policy=policy,
            )
            for claim in claims:
                result = verify_ratification(
                    store,
                    ratify=claim,
                    epoch=epoch,
                    proposal=proposal,
                    tally=tally,
                    now=now,
                    policy=policy,
                )
                if result.next_epoch is None:
                    findings.extend(result.findings)
                else:
                    carrying[result.next_epoch.epoch_id] = result.next_epoch

        if len(carrying) == 1:
            epoch = next(iter(carrying.values()))
            continue
        if len(carrying) > 1:
            for successor_id in carrying:
                findings.append(
                    Finding(kind=GovernanceFinding.EPOCH_FORK, subject=successor_id)
                )
        return EpochResolution(
            epoch=epoch,
            constitution_obj=constitution_obj,
            findings=dedupe_sort(findings),
        )
