"""Verdikt-Bindungskraft (03-profiles.md §2.4, D67/D78/D89)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from mensch_als_republik.atom import Claim, claim_id
from mensch_als_republik.index import classify_all
from mensch_als_republik.policy import NucleusPolicy
from mensch_als_republik.predicates import parse_predicate
from mensch_als_republik.profiles.findings import Finding, ProfileFinding, _dedupe_sort
from mensch_als_republik.verifier import Classification, ClaimStore, State


class VerdictStatus(str, Enum):
    BINDING = "BINDING"
    ATTRIBUTED_OPINION = "ATTRIBUTED_OPINION"


@dataclass(frozen=True, slots=True)
class VerdictResult:
    """Status plus Vermerke (03-profiles.md §2.4.2, D89)."""

    status: VerdictStatus
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


def _active_submission(
    store: ClaimStore,
    classifications: dict[bytes, Classification],
    *,
    party: bytes,
    arbitrator: bytes,
    scope: bytes,
    findings: list[Finding],
) -> bool:
    """Wahr gdw. eine aktive submit-arbitration@1 von party auf arbitrator im Scope existiert."""
    found = False
    for c in store.all_claims():
        if not _is_nuc_name(c, "submit-arbitration"):
            continue
        if c.I != party or c.J != (1, arbitrator):
            continue
        cid = claim_id(c)
        if c.N != scope:
            findings.append(
                Finding(kind=ProfileFinding.SCOPE_MISMATCH, subject=cid)
            )
            continue
        if classifications[cid].state == State.ACTIVE:
            found = True
    return found


def verdict_status(
    store: ClaimStore,
    *,
    verdict: Claim,
    scope: bytes,
    arbitrators: frozenset[bytes],
    now: int,
    policy: NucleusPolicy | None = None,
) -> VerdictResult:
    """Entscheidet BINDING vs. ATTRIBUTED_OPINION (03-profiles.md §2.4.2, 03-prompt.md §7)."""
    if policy is not None and policy.scope != scope:
        raise ValueError("policy scope does not match scope")

    by_cid = classify_all(store, now, policy)
    findings: list[Finding] = []
    v_cid = claim_id(verdict)
    verdict_active = by_cid[v_cid].state == State.ACTIVE

    path_i = verdict.I in arbitrators

    parties: tuple[bytes, bytes] | None = None
    if verdict.J[0] != 2:
        findings.append(
            Finding(kind=ProfileFinding.UNKNOWN_ACCUSATION, subject=v_cid)
        )
    else:
        accusation = store.get(verdict.J[1])
        if accusation is None:
            findings.append(
                Finding(kind=ProfileFinding.UNKNOWN_ACCUSATION, subject=verdict.J[1])
            )
        elif accusation.N != scope:
            findings.append(
                Finding(
                    kind=ProfileFinding.UNKNOWN_ACCUSATION,
                    subject=claim_id(accusation),
                )
            )
        else:
            if accusation.J[0] == 1:
                parties = (accusation.I, accusation.J[1])
            elif accusation.J[0] == 2:
                disputed = store.get(accusation.J[1])
                if disputed is None:
                    findings.append(
                        Finding(
                            kind=ProfileFinding.UNRESOLVED_ACCUSED,
                            subject=accusation.J[1],
                        )
                    )
                else:
                    parties = (accusation.I, disputed.I)
            else:
                findings.append(
                    Finding(
                        kind=ProfileFinding.UNRESOLVED_ACCUSED,
                        subject=claim_id(accusation),
                    )
                )

    path_ii = False
    if parties is not None:
        accuser, accused = parties
        sub_accuser = _active_submission(
            store,
            by_cid,
            party=accuser,
            arbitrator=verdict.I,
            scope=scope,
            findings=findings,
        )
        sub_accused = _active_submission(
            store,
            by_cid,
            party=accused,
            arbitrator=verdict.I,
            scope=scope,
            findings=findings,
        )
        path_ii = sub_accuser and sub_accused

    if not verdict_active:
        findings.append(
            Finding(kind=ProfileFinding.INACTIVE_VERDICT, subject=v_cid)
        )
        return VerdictResult(
            status=VerdictStatus.ATTRIBUTED_OPINION,
            findings=_dedupe_sort(findings),
        )

    if path_i or path_ii:
        return VerdictResult(
            status=VerdictStatus.BINDING,
            findings=_dedupe_sort(findings),
        )

    return VerdictResult(
        status=VerdictStatus.ATTRIBUTED_OPINION,
        findings=_dedupe_sort(findings),
    )
