"""Mitgliedschaft als Konjunktion zweier aktiver Claims (03-profiles.md §4)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from mensch_als_republik.atom import Claim, claim_id
from mensch_als_republik.policy import NucleusPolicy
from mensch_als_republik.predicates import parse_predicate
from mensch_als_republik.profiles.findings import Finding, ProfileFinding, dedupe_sort
from mensch_als_republik.index import classify_all
from mensch_als_republik.verifier import ClaimStore, State


class MembershipState(str, Enum):
    MEMBER = "MEMBER"
    APPLICANT = "APPLICANT"
    GRANT_ONLY = "GRANT_ONLY"
    NONE = "NONE"


@dataclass(frozen=True, slots=True)
class MembershipResult:
    """Zustand der Mitgliedschaft plus zählende claim_ids (03-profiles.md §4)."""

    state: MembershipState
    accept_claim_id: bytes | None
    grant_claim_id: bytes | None
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


def membership(
    store: ClaimStore,
    *,
    subject: bytes,
    scope: bytes,
    constitution_hash: bytes,
    now: int,
    authorized_keys: frozenset[bytes],
    policy: NucleusPolicy | None = None,
    participants: frozenset[bytes] | None = None,
) -> MembershipResult:
    """Wertet accept-rules ∧ grant-membership aus (03-profiles.md §4, 03-prompt.md §5)."""
    if policy is not None and policy.scope != scope:
        raise ValueError("policy scope does not match scope")

    by_cid = classify_all(store, now, policy)
    findings: list[Finding] = []
    accept_ids: list[bytes] = []
    grant_ids: list[bytes] = []

    for c in store.all_claims():
        cid = claim_id(c)

        if _is_nuc_name(c, "accept-rules") and c.I == subject:
            if c.N != scope:
                findings.append(
                    Finding(kind=ProfileFinding.SCOPE_MISMATCH, subject=cid)
                )
                continue
            if c.J != (3, constitution_hash):
                if c.J[0] == 3:
                    findings.append(
                        Finding(
                            kind=ProfileFinding.CONSTITUTION_VERSION_MISMATCH,
                            subject=cid,
                        )
                    )
                continue
            if by_cid[cid].state != State.ACTIVE:
                continue
            accept_ids.append(cid)
            continue

        if _is_nuc_name(c, "grant-membership") and c.J == (1, subject):
            if c.N != scope:
                findings.append(
                    Finding(kind=ProfileFinding.SCOPE_MISMATCH, subject=cid)
                )
                continue
            if c.I not in authorized_keys:
                findings.append(
                    Finding(
                        kind=ProfileFinding.UNAUTHORIZED_GRANT_AUTHOR,
                        subject=cid,
                    )
                )
                continue
            if by_cid[cid].state != State.ACTIVE:
                continue
            grant_ids.append(cid)

    accept_claim_id = min(accept_ids) if accept_ids else None
    grant_claim_id = min(grant_ids) if grant_ids else None
    has_accept = accept_claim_id is not None
    has_grant = grant_claim_id is not None or (
        participants is not None and subject in participants
    )

    if has_accept and has_grant:
        state = MembershipState.MEMBER
    elif has_accept:
        state = MembershipState.APPLICANT
    elif has_grant:
        state = MembershipState.GRANT_ONLY
    else:
        state = MembershipState.NONE

    return MembershipResult(
        state=state,
        accept_claim_id=accept_claim_id,
        grant_claim_id=grant_claim_id,
        findings=dedupe_sort(findings),
    )
