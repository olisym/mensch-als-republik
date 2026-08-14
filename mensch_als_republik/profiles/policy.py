"""Policy-Auflösung aus Genesis und Verfassung (03-profiles.md §1.2, D82/D84/D90)."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass

from mensch_als_republik import cbor_canon
from mensch_als_republik.domains import DOM_NUC_GEN
from mensch_als_republik.policy import NucleusPolicy, constitution_hash
from mensch_als_republik.profiles.findings import Finding, ProfileFinding, dedupe_sort


@dataclass(frozen=True, slots=True)
class PolicyResolution:
    """Ergebnis von ``resolve_policy``: Policy plus Auflösungsbefunde (03-profiles.md §1.2)."""

    policy: NucleusPolicy
    findings: tuple[Finding, ...]


def resolve_policy(
    *,
    scope: bytes,
    genesis_obj: dict,
    constitution_obj: dict | None = None,
) -> PolicyResolution:
    """Rechnet Scope und constitution_hash nach; Sicherheits-Default bei Teilwissen.

    Siehe 03-profiles.md §1.2 und 03-prompt.md §4. ``UNSAFE_IRREVOCABLE_PREDICATE``
    entsteht im Konstruktor von ``NucleusPolicy`` (D84), nicht hier.
    """
    computed_scope = hashlib.sha256(
        DOM_NUC_GEN + cbor_canon.encode(genesis_obj)
    ).digest()
    if scope != computed_scope:
        raise ValueError("genesis_obj does not match scope")

    declared_hash = genesis_obj.get(4)
    if not isinstance(declared_hash, bytes) or len(declared_hash) != 32:
        raise ValueError("genesis_obj missing or invalid constitution_hash (key 4)")

    if constitution_obj is None:
        return PolicyResolution(
            policy=NucleusPolicy(scope, declared=frozenset()),
            findings=dedupe_sort(
                [
                    Finding(
                        kind=ProfileFinding.CONSTITUTION_UNAVAILABLE,
                        subject=declared_hash,
                    )
                ]
            ),
        )

    computed_hash = constitution_hash(constitution_obj)
    if declared_hash != computed_hash:
        return PolicyResolution(
            policy=NucleusPolicy(scope, declared=frozenset()),
            findings=dedupe_sort(
                [
                    Finding(
                        kind=ProfileFinding.CONSTITUTION_HASH_MISMATCH,
                        subject=declared_hash,
                    )
                ]
            ),
        )

    raw = constitution_obj.get("irrevocable_predicates", [])
    return PolicyResolution(
        policy=NucleusPolicy(scope, declared=raw),
        findings=(),
    )
