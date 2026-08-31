"""Claim-Verifizierer: strukturelle Prüfung und Zustandsmaschine (01 §6, Anhang B)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import (
    Claim,
    claim_from_map,
    claim_id,
    has_null_hprev,
    is_equivocation_pair,
    is_genesis,
    verify_sig,
)
from mensch_als_republik.errors import (
    BadScopeBinding,
    BadSignature,
    ErrorCode,
    ForeignLifecycle,
    IncoherentExpiry,
    InvalidGenesisAnchor,
    MalformedCbor,
    NonCanonicalEncoding,
    ReservedCorePredicate,
    UnknownJTag,
    UnknownNamespace,
    UnsupportedVersion,
    VerifierError,
)
from mensch_als_republik.policy import NucleusPolicy, is_irrevocable
from mensch_als_republik.predicates import check_scope_binding, is_core_predicate, parse_predicate

_SUPPORTED_VERSION = 1
_VALID_J_TAGS = frozenset({1, 2, 3})
_J_TAG_CLAIM_REF = 2


class State(str, Enum):
    MALFORMED = "malformed"
    PENDING = "pending"
    LINKED = "linked"
    ACTIVE = "active"
    REVOKED = "revoked"
    SUPERSEDED = "superseded"
    EXPIRED = "expired"
    EQUIVOCATION_FLAGGED = "equivocation_flagged"


@dataclass(frozen=True, slots=True)
class Classification:
    """Ergebnis der Zustandsklassifikation inkl. Trust-Nutzbarkeit."""

    state: State
    trust_usable: bool


class ClaimStore(Protocol):
    def get(self, cid: bytes) -> Claim | None: ...

    def by_author_hprev(self, I: bytes, h_prev: bytes) -> list[Claim]: ...

    def add(self, claim: Claim) -> None: ...

    def all_claims(self) -> list[Claim]: ...


class InMemoryStore:
    """Einfacher In-Memory-Claim-Store für Tests."""

    def __init__(self) -> None:
        self._by_id: dict[bytes, Claim] = {}
        self._by_author_hprev: dict[tuple[bytes, bytes], list[Claim]] = {}

    def get(self, cid: bytes) -> Claim | None:
        return self._by_id.get(cid)

    def by_author_hprev(self, I: bytes, h_prev: bytes) -> list[Claim]:
        return list(self._by_author_hprev.get((I, h_prev), []))

    def add(self, claim: Claim) -> None:
        cid = claim_id(claim)
        if cid in self._by_id:
            return
        self._by_id[cid] = claim
        key = (claim.I, claim.h_prev)
        siblings = self._by_author_hprev.setdefault(key, [])
        siblings.append(claim)

    def all_claims(self) -> list[Claim]:
        return list(self._by_id.values())


def _validate_field_types(m: dict) -> None:
    """Feldtypen aus 01 §2 prüfen."""
    if not isinstance(m.get(0), int):
        raise MalformedCbor()
    if not isinstance(m.get(1), bytes) or len(m[1]) != 32:
        raise MalformedCbor()
    j = m.get(2)
    if not isinstance(j, list) or len(j) != 2:
        raise MalformedCbor()
    if not isinstance(j[0], int) or not isinstance(j[1], bytes) or len(j[1]) != 32:
        raise MalformedCbor()
    if not isinstance(m.get(3), str):
        raise MalformedCbor()
    if 4 in m and not isinstance(m[4], bytes):
        raise MalformedCbor()
    if 5 in m and (not isinstance(m[5], bytes) or len(m[5]) != 32):
        raise MalformedCbor()
    if not isinstance(m.get(6), int):
        raise MalformedCbor()
    if 7 in m and not isinstance(m[7], int):
        raise MalformedCbor()
    if not isinstance(m.get(8), bytes) or len(m[8]) != 32:
        raise MalformedCbor()
    if 9 not in m or not isinstance(m[9], bytes) or len(m[9]) != 64:
        raise MalformedCbor()


def _check_foreign_lifecycle(claim: Claim, store: ClaimStore | None) -> None:
    """FOREIGN_LIFECYCLE wenn Ziel-Claim bekannt und ziel.I != C.I."""
    if not is_core_predicate(claim):
        return
    if claim.J[0] != _J_TAG_CLAIM_REF:
        return
    if store is None:
        return
    target = store.get(claim.J[1])
    if target is not None and target.I != claim.I:
        raise ForeignLifecycle()


def structural_check(data: bytes, store: ClaimStore | None = None) -> Claim:
    """
    Strukturelle Gültigkeit 01 §6 Punkte 1–7 in normativer Reihenfolge.

    Raises VerifierError-Subklassen bei Reject.
    """
    # 2a: dekodierbar
    try:
        obj = cbor_canon.decode(data)
    except Exception as exc:
        raise MalformedCbor() from exc

    if not isinstance(obj, dict):
        raise MalformedCbor()

    # 2b: uint-Keys, keine doppelten (decode garantiert letzteres bei cbor2)
    for k in obj:
        if not isinstance(k, int):
            raise MalformedCbor()

    # 2c: kanonische Kodierung (01 §3, D130)
    try:
        canonical = cbor_canon.is_canonical(data)
    except Exception as exc:
        raise MalformedCbor() from exc
    if not canonical:
        raise NonCanonicalEncoding()

    # 2d: Feldtypen
    required = {0, 1, 2, 3, 6, 8, 9}
    if not required.issubset(obj.keys()):
        raise MalformedCbor()
    _validate_field_types(obj)

    claim = claim_from_map(obj)

    # 1: version
    if claim.version != _SUPPORTED_VERSION:
        raise UnsupportedVersion()

    # 3: J.tag
    if claim.J[0] not in _VALID_J_TAGS:
        raise UnknownJTag()

    # 4: Prädikat-Namensraum, Scope-Bindung, core-Lifecycle-Form
    try:
        parsed = parse_predicate(claim.p)
    except VerifierError:
        raise

    if parsed.namespace == "core":
        if claim.J[0] != _J_TAG_CLAIM_REF:
            raise MalformedCbor()
    elif parsed.namespace == "nuc":
        check_scope_binding(claim)

    _check_foreign_lifecycle(claim, store)

    # 5: Signatur
    if not verify_sig(claim):
        raise BadSignature()

    # 6: h_prev != 32×0x00
    if has_null_hprev(claim):
        raise InvalidGenesisAnchor()

    # 7: t < t_exp
    if not is_core_predicate(claim) and claim.t_exp is not None and claim.t >= claim.t_exp:
        raise IncoherentExpiry()

    return claim


def read_claim(data: bytes, store: ClaimStore | None = None) -> Claim | ErrorCode:
    """Einlesepfad: liefert einen Claim oder einen Reject-Code, wirft nie (D131)."""
    try:
        return structural_check(data, store)
    except VerifierError as exc:
        return exc.code


def _is_temporally_valid(claim: Claim, now: int | None) -> bool | None:
    """
    Zeitliche Gültigkeit gegen t_exp.

    Returns True/False wenn entscheidbar, None wenn now fehlt und t_exp gesetzt.
    core/* ignoriert t_exp (01 §5.3).
    """
    if is_core_predicate(claim):
        return True
    if claim.t_exp is None:
        return True
    if now is None:
        return None
    return now <= claim.t_exp


def _predecessor_known_and_valid(
    claim: Claim, store: ClaimStore
) -> tuple[bool, Claim | None]:
    """Vorgänger im Store und strukturell konsistent."""
    if is_genesis(claim):
        return True, None
    pred = store.get(claim.h_prev)
    if pred is None:
        return False, None
    if pred.I != claim.I:
        return False, pred
    return True, pred


def _find_revoking_claim(target: Claim, store: ClaimStore) -> Claim | None:
    """Gültiger selbst-bezüglicher core/revoke@1 für target."""
    from mensch_als_republik.atom import signed_bytes

    for c in store.all_claims():
        if not is_core_predicate(c):
            continue
        parsed = parse_predicate(c.p)
        if parsed.name != "revoke":
            continue
        if c.I != target.I:
            continue
        if c.J[0] != _J_TAG_CLAIM_REF or c.J[1] != claim_id(target):
            continue
        try:
            structural_check(signed_bytes(c))
        except VerifierError:
            continue
        return c
    return None


def _find_superseding_claim(target: Claim, store: ClaimStore) -> Claim | None:
    """Gültiger selbst-bezüglicher core/supersede@1, der target ersetzt."""
    from mensch_als_republik.atom import signed_bytes

    for c in store.all_claims():
        if not is_core_predicate(c):
            continue
        parsed = parse_predicate(c.p)
        if parsed.name != "supersede":
            continue
        if c.I != target.I:
            continue
        if c.J[0] != _J_TAG_CLAIM_REF or c.J[1] != claim_id(target):
            continue
        try:
            structural_check(signed_bytes(c))
        except VerifierError:
            continue
        return c
    return None


def _is_in_equivocation_pair(claim: Claim, store: ClaimStore) -> bool:
    siblings = store.by_author_hprev(claim.I, claim.h_prev)
    cid = claim_id(claim)
    for other in siblings:
        if claim_id(other) != cid and is_equivocation_pair(claim, other):
            return True
    return False


def classify(
    claim: Claim,
    store: ClaimStore,
    now: int | None = None,
    policy: NucleusPolicy | None = None,
) -> Classification:
    """
    Zustandsmaschine aus Anhang B, optional mit Nukleus-Policy-Override (01 §5.4).

    Voraussetzung: claim ist strukturell gültig (structural_check bestanden).
    """
    # Scope-Prüfung (01 §5.4): eine Policy fremden Scopes wird nie still ignoriert.
    if policy is not None and claim.p.startswith("nuc:") and claim.N != policy.scope:
        raise ValueError("policy scope does not match claim scope")

    # FOREIGN_LIFECYCLE bei bekannter Ziel-Identity
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

    protected = is_irrevocable(claim.p, policy)

    if not protected and _find_superseding_claim(claim, store) is not None:
        return Classification(
            state=State.SUPERSEDED,
            trust_usable=False,
        )

    if not protected and _find_revoking_claim(claim, store) is not None:
        return Classification(
            state=State.REVOKED,
            trust_usable=False,
        )

    if temporal is None:
        return Classification(state=State.LINKED, trust_usable=False)

    if temporal is False:
        return Classification(state=State.EXPIRED, trust_usable=False)

    return Classification(state=State.ACTIVE, trust_usable=True)


__all__ = [
    "BadScopeBinding",
    "BadSignature",
    "Classification",
    "ClaimStore",
    "ErrorCode",
    "ForeignLifecycle",
    "IncoherentExpiry",
    "InMemoryStore",
    "InvalidGenesisAnchor",
    "MalformedCbor",
    "NonCanonicalEncoding",
    "ReservedCorePredicate",
    "State",
    "UnknownJTag",
    "UnknownNamespace",
    "UnsupportedVersion",
    "VerifierError",
    "classify",
    "read_claim",
    "structural_check",
]
