"""Nukleus-Policy: Override der Widerrufbarkeit für Nukleus-Prädikate (§5.4, 00 §5.2)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

PROTOCOL_IRREVOCABLE = frozenset({"obligation@1"})  # Boden, D70 / 00 §5.2
TRUST_GRANTING = frozenset({"vouch@1"})  # Negativliste, D58 / 01 §5.4.3 b
_CORE_ENTRIES = frozenset({"revoke@1", "supersede@1"})  # D71

assert not (PROTOCOL_IRREVOCABLE & TRUST_GRANTING), (
    "D70/D58: der Boden darf nie in der Negativliste stehen"
)
assert not (PROTOCOL_IRREVOCABLE & _CORE_ENTRIES), (
    "D70/D71: der Boden darf nie ein core-Prädikat sein"
)


class PolicyWarning(str, Enum):
    UNSAFE_IRREVOCABLE_PREDICATE = "UNSAFE_IRREVOCABLE_PREDICATE"


@dataclass(frozen=True, slots=True)
class PolicyNote:
    code: PolicyWarning
    predicate: str


@dataclass(frozen=True, slots=True)
class NucleusPolicy:
    """Policy eines Nukleus: welche Prädikate in ihrem Scope irrevocable sind."""

    scope: bytes
    declared: frozenset[str] = frozenset()
    irrevocable: frozenset[str] = field(init=False, default=frozenset())
    warnings: tuple[PolicyNote, ...] = field(init=False, default=())

    def __post_init__(self) -> None:
        irrevocable = (PROTOCOL_IRREVOCABLE | self.declared) - TRUST_GRANTING - _CORE_ENTRIES
        unsafe = self.declared & TRUST_GRANTING
        warnings = tuple(
            PolicyNote(PolicyWarning.UNSAFE_IRREVOCABLE_PREDICATE, predicate)
            for predicate in sorted(unsafe)
        )
        object.__setattr__(self, "irrevocable", frozenset(irrevocable))
        object.__setattr__(self, "warnings", warnings)


def is_irrevocable(predicate: str, policy: NucleusPolicy | None) -> bool:
    """Wahr gdw. policy gesetzt, predicate ein nuc:-Prädikat ist und dessen Profilname
    (Teil nach dem letzten "/") in policy.irrevocable liegt (§5.4.2)."""
    if policy is None:
        return False
    if not predicate.startswith("nuc:"):
        return False
    name = predicate.rsplit("/", 1)[-1]
    return name in policy.irrevocable


__all__ = [
    "PROTOCOL_IRREVOCABLE",
    "TRUST_GRANTING",
    "NucleusPolicy",
    "PolicyNote",
    "PolicyWarning",
    "is_irrevocable",
]
