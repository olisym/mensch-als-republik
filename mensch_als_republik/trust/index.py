"""classify_all: schneller Zwilling von verifier.classify (02a §3, classify_all).

structural_check läuft genau einmal pro core/revoke@1- bzw. core/supersede@1-Claim
(Index-Aufbau), statt einmal pro Kandidat-Suche innerhalb jedes classify()-Aufrufs.
classify() aus Layer 01 bleibt die normative Wahrheit; dieses Modul dupliziert ihre
Logik absichtlich 1:1, mit den beiden linearen Kandidatensuchen durch Index-Lookups
ersetzt. Der Kopplungstest (T-02.4) stellt sicher, dass beide nie auseinanderlaufen.
"""

from __future__ import annotations

from mensch_als_republik.atom import Claim, claim_id, signed_bytes
from mensch_als_republik.errors import ForeignLifecycle, VerifierError
from mensch_als_republik.predicates import is_core_predicate, parse_predicate
from mensch_als_republik.verifier import (
    Classification,
    ClaimStore,
    State,
    _is_in_equivocation_pair,
    _is_temporally_valid,
    _predecessor_known_and_valid,
    structural_check,
)

_J_TAG_CLAIM_REF = 2


def _build_lifecycle_index(
    claims: list[Claim],
) -> tuple[dict[bytes, list[Claim]], dict[bytes, list[Claim]]]:
    """revokes_by_target, supersedes_by_target: nur strukturell gültige Kandidaten."""
    revokes_by_target: dict[bytes, list[Claim]] = {}
    supersedes_by_target: dict[bytes, list[Claim]] = {}

    for c in claims:
        if not is_core_predicate(c):
            continue
        parsed = parse_predicate(c.p)
        if parsed.name not in ("revoke", "supersede"):
            continue
        if c.J[0] != _J_TAG_CLAIM_REF:
            continue
        try:
            structural_check(signed_bytes(c))
        except VerifierError:
            continue
        index = revokes_by_target if parsed.name == "revoke" else supersedes_by_target
        index.setdefault(c.J[1], []).append(c)

    return revokes_by_target, supersedes_by_target


def _classify_one(
    claim: Claim,
    store: ClaimStore,
    now: int | None,
    revokes_by_target: dict[bytes, list[Claim]],
    supersedes_by_target: dict[bytes, list[Claim]],
) -> Classification:
    if is_core_predicate(claim):
        target = store.get(claim.J[1])
        if target is not None and target.I != claim.I:
            raise ForeignLifecycle()

    if _is_in_equivocation_pair(claim, store):
        return Classification(state=State.EQUIVOCATION_FLAGGED, trust_usable=False)

    pred_ok, _ = _predecessor_known_and_valid(claim, store)
    if not pred_ok:
        return Classification(state=State.PENDING, trust_usable=False)

    temporal = _is_temporally_valid(claim, now)

    cid = claim_id(claim)

    superseding = [c for c in supersedes_by_target.get(cid, []) if c.I == claim.I]
    if superseding:
        return Classification(state=State.SUPERSEDED, trust_usable=False)

    revoking = [c for c in revokes_by_target.get(cid, []) if c.I == claim.I]
    if revoking:
        return Classification(state=State.REVOKED, trust_usable=False)

    if temporal is None:
        return Classification(state=State.LINKED, trust_usable=False)

    if temporal is False:
        return Classification(state=State.EXPIRED, trust_usable=False)

    return Classification(state=State.ACTIVE, trust_usable=True)


def classify_all(store: ClaimStore, now: int) -> dict[bytes, Classification]:
    """Ein Durchlauf über den Store; klassifiziert jeden Claim (02a §3)."""
    claims = store.all_claims()
    revokes_by_target, supersedes_by_target = _build_lifecycle_index(claims)

    result: dict[bytes, Classification] = {}
    for claim in claims:
        result[claim_id(claim)] = _classify_one(
            claim, store, now, revokes_by_target, supersedes_by_target
        )
    return result
