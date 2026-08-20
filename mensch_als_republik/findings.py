"""Nukleus-Findings: eigener Enum, kein Claim-Reject (00 §5.4, D163, D164)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class NucleusFinding(str, Enum):
    CONSTITUTION_UNAVAILABLE = "CONSTITUTION_UNAVAILABLE"
    MALFORMED_NUCLEUS_KEY = "MALFORMED_NUCLEUS_KEY"


@dataclass(frozen=True, slots=True, order=True)
class Finding:
    """Vermerk mit Subjekt — constitution_hash (00 §5.4, D163, D164)."""

    kind: NucleusFinding
    subject: bytes


def dedupe_sort(findings: list[Finding] | tuple[Finding, ...]) -> tuple[Finding, ...]:
    """Findings sortiert und dedupliziert (04-prompt.md §2)."""
    return tuple(sorted(set(findings)))
