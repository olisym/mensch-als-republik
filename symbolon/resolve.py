"""Fassade über Epochenkette, Policy und Schlüssel (D183, D180)."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from symbolon import findings as nucleus_findings
from symbolon.governance import findings as governance_findings
from symbolon.governance.chain import resolve_epoch
from symbolon.governance.objects import Epoch, Proposal
from symbolon.keys import resolve_authorized_keys
from symbolon.policy import NucleusPolicy
from symbolon.profiles import findings as profiles_findings
from symbolon.profiles.policy import resolve_policy
from symbolon.verifier import ClaimStore


@dataclass(frozen=True, slots=True)
class NucleusState:
    """Konsistenter Nukleus-Zustand aus einer aufgelösten Kette (D183)."""

    epoch: Epoch
    constitution_obj: dict | None
    policy: NucleusPolicy
    authorized_keys: frozenset[bytes]
    epoch_findings: tuple[governance_findings.Finding, ...]
    policy_findings: tuple[profiles_findings.Finding, ...]
    key_findings: tuple[nucleus_findings.Finding, ...]


def resolve_state(
    store: ClaimStore,
    *,
    scope: bytes,
    genesis_obj: dict,
    known_constitutions: Mapping[bytes, dict],
    known_proposals: Mapping[bytes, Proposal],
    now: int,
) -> NucleusState:
    """Verkettet ``resolve_epoch``, ``resolve_policy`` und ``resolve_authorized_keys`` (D183)."""
    epoch_res = resolve_epoch(
        store,
        scope=scope,
        genesis_obj=genesis_obj,
        known_constitutions=known_constitutions,
        known_proposals=known_proposals,
        now=now,
    )
    policy_res = resolve_policy(
        scope=scope,
        genesis_obj=genesis_obj,
        constitution_hash=epoch_res.epoch.constitution_hash,
        constitution_obj=epoch_res.constitution_obj,
    )
    key_res = resolve_authorized_keys(
        store,
        scope=scope,
        genesis_obj=genesis_obj,
        constitution_hash=epoch_res.epoch.constitution_hash,
        constitution_obj=epoch_res.constitution_obj,
        now=now,
        policy=policy_res.policy,
    )
    return NucleusState(
        epoch=epoch_res.epoch,
        constitution_obj=epoch_res.constitution_obj,
        policy=policy_res.policy,
        authorized_keys=key_res.keys,
        epoch_findings=epoch_res.findings,
        policy_findings=policy_res.findings,
        key_findings=key_res.findings,
    )
