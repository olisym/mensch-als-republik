"""Schlüsselkette: resolve_current_key (00-nucleus-genesis-constitution.md §6.4, D151–D156)."""

from __future__ import annotations

from mensch_als_republik.atom import Claim, claim_id
from mensch_als_republik.index import classify_all
from mensch_als_republik.policy import NucleusPolicy
from mensch_als_republik.predicates import parse_predicate
from mensch_als_republik.verifier import ClaimStore, State

_J_TAG_IDENTITY = 1
_J_TAG_CLAIM_REF = 2
_COUNTING = frozenset({State.ACTIVE, State.EXPIRED})


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


def _on_author_chain(earlier: Claim, later: Claim, store: ClaimStore) -> bool:
    """True gdw. ``earlier`` auf dem ``h_prev``-Pfad von ``later`` liegt (D154, D155 a)."""
    target = claim_id(earlier)
    seen: set[bytes] = set()
    cid = later.h_prev
    while cid not in seen:
        if cid == target:
            return True
        seen.add(cid)
        pred = store.get(cid)
        if pred is None:
            return False
        cid = pred.h_prev
    return False


def _earliest_on_chain(
    rotates: list[Claim], store: ClaimStore
) -> Claim | None:
    for candidate in rotates:
        if all(
            other is candidate or _on_author_chain(candidate, other, store)
            for other in rotates
        ):
            return candidate
    return None


def resolve_current_key(
    store: ClaimStore,
    *,
    scope: bytes,
    anchor_keys: frozenset[bytes],
    now: int,
    policy: NucleusPolicy | None = None,
) -> frozenset[bytes]:
    """Köpfe der vollständigen Rotationsketten ab ``anchor_keys`` (00 §6.4 Schritt 2–4).

    ``policy`` wird unverändert an ``classify_all`` gereicht (03 §4, D156).
    """
    by_cid = classify_all(store, now, policy)
    claims = store.all_claims()

    def _head_from(k: bytes) -> bytes | None:
        visited: set[bytes] = set()
        k_cur = k
        while True:
            if k_cur in visited:
                return None
            visited.add(k_cur)
            flagged = False
            complete: list[Claim] = []
            for claim in claims:
                if not _is_nuc_name(claim, "rotate-key"):
                    continue
                if claim.I != k_cur or claim.N != scope:
                    continue
                if by_cid[claim_id(claim)].state is State.EQUIVOCATION_FLAGGED:
                    flagged = True
                    break
                if claim.J[0] != _J_TAG_IDENTITY:
                    continue
                if by_cid[claim_id(claim)].state not in _COUNTING:
                    continue
                rid = claim_id(claim)
                ack_ok = False
                for ack in claims:
                    if not _is_nuc_name(ack, "rotate-ack"):
                        continue
                    if ack.J != (_J_TAG_CLAIM_REF, rid):
                        continue
                    if ack.I != claim.J[1]:
                        continue
                    if ack.N != claim.N:
                        continue
                    if by_cid[claim_id(ack)].state not in _COUNTING:
                        continue
                    ack_ok = True
                    break
                if ack_ok:
                    complete.append(claim)
            if flagged:
                return None
            if not complete:
                return k_cur
            if len(complete) == 1:
                k_cur = complete[0].J[1]
                continue
            earliest = _earliest_on_chain(complete, store)
            if earliest is None:
                return None
            k_cur = earliest.J[1]

    heads: set[bytes] = set()
    for k in anchor_keys:
        head = _head_from(k)
        if head is not None:
            heads.add(head)
    return frozenset(heads)
