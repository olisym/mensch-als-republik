"""Kettenbauer: Verfassungen zu Speicher, Genesis und Epochen (D190)."""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import claim_id
from mensch_als_republik.domains import DOM_NUC_GEN
from mensch_als_republik.governance.objects import Epoch, Proposal
from mensch_als_republik.policy import constitution_hash
from mensch_als_republik.verifier import InMemoryStore
from tests.governance.fixtures import nuc, vote
from tests.helpers import Identity, store_with


@dataclass(frozen=True, slots=True)
class Kettenwelt:
    """Fertige Kette aus Identitäten, Wurzelschlüsseln und Verfassungen (D190)."""

    scope: bytes
    genesis_obj: dict
    verfassungen: tuple[dict, ...]
    verfassungs_hashes: tuple[bytes, ...]
    epochen: tuple[Epoch, ...]
    vorschlaege: tuple[Proposal, ...]
    store: InMemoryStore
    known_constitutions: dict[bytes, dict]
    known_proposals: dict[bytes, Proposal]


def kettenwelt(
    *,
    identitaeten: Sequence[Identity],
    root_keys: Sequence[bytes],
    verfassungen: Sequence[dict],
    now: int = 1000,
) -> Kettenwelt:
    """Baut Genesis, Übergänge und Speicher aus einer Folge von Verfassungen (D190)."""
    if not verfassungen:
        raise ValueError("verfassungen must not be empty")
    if len(verfassungen) > 1 and not identitaeten:
        raise ValueError("identitaeten must not be empty")

    hashes = tuple(constitution_hash(obj) for obj in verfassungen)
    genesis_obj = {
        0: 1,
        1: sorted(root_keys),
        2: 0,
        3: sorted(root_keys),
        4: hashes[0],
        5: 2,
        6: 0,
        7: 0,
    }
    scope = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis_obj)).digest()
    epochen = [Epoch(scope=scope, index=1, constitution_hash=hashes[0])]
    vorschlaege: list[Proposal] = []
    claims = []
    t = 1
    for i in range(1, len(verfassungen)):
        proposal = Proposal(
            scope=scope,
            predecessor=epochen[i - 1].epoch_id,
            constitution_hash=hashes[i],
        )
        vorschlaege.append(proposal)
        claims.append(
            identitaeten[0].claim(
                p=nuc(scope, "propose"),
                J=(3, proposal.proposal_hash),
                t=t,
                N=scope,
            )
        )
        t += 1
        votes = [
            vote(identitaet, proposal, choice=1, t=t, scope=scope)
            for identitaet in identitaeten
        ]
        claims.extend(votes)
        t += 1
        claims.append(
            identitaeten[0].claim(
                p=nuc(scope, "ratify"),
                J=(3, proposal.proposal_hash),
                t=t,
                N=scope,
                v=cbor_canon.encode({0: [claim_id(v) for v in votes]}),
            )
        )
        t += 1
        epochen.append(Epoch(scope=scope, index=i + 1, constitution_hash=hashes[i]))

    objs = tuple(verfassungen)
    return Kettenwelt(
        scope=scope,
        genesis_obj=genesis_obj,
        verfassungen=objs,
        verfassungs_hashes=hashes,
        epochen=tuple(epochen),
        vorschlaege=tuple(vorschlaege),
        store=store_with(*claims),
        known_constitutions=dict(zip(hashes, objs)),
        known_proposals={p.proposal_hash: p for p in vorschlaege},
    )
