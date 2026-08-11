"""Öffentliche API: trust() (02a §3, §2.10)."""

from __future__ import annotations

from dataclasses import dataclass

from mensch_als_republik.atom import claim_id
from mensch_als_republik.verifier import ClaimStore, State

from .dinic import Dinic
from .findings import Finding, TrustFinding
from .graph import (
    SINK,
    SOURCE,
    bfs_capacities,
    build_flow_graph,
    infinity,
    source_side_cut,
)
from .groups import build_groups
from .index import classify_all
from .params import TrustParams


@dataclass(frozen=True, slots=True)
class TrustResult:
    value: int
    disjoint_paths: int
    cut: tuple[bytes, ...]
    findings: tuple[Finding, ...]


def trust(
    store: ClaimStore,
    *,
    anchors: frozenset[bytes],
    targets: frozenset[bytes],
    scope: bytes,
    now: int,
    params: TrustParams,
    include_flagged: bool = False,
) -> TrustResult:
    if anchors & targets:
        raise ValueError("anchors and targets must be disjoint")

    # 1. classify_all
    classifications = classify_all(store, now)
    claims = store.all_claims()

    # 2-3. Vouch-Claims des Scopes sammeln, v dekodieren, Gruppen bilden
    groups, payload_findings = build_groups(claims, classifications, scope, params.D, now)

    # 4. Budget je Autor prüfen -> OVERCOMMITTED_AUTHOR
    budget_by_author: dict[bytes, int] = {}
    for (author, _subject), group in groups.items():
        budget_by_author[author] = budget_by_author.get(author, 0) + group.n_budget
    overcommitted_authors = {
        author for author, total in budget_by_author.items() if total > params.D
    }
    overcommit_findings = tuple(
        Finding(kind=TrustFinding.OVERCOMMITTED_AUTHOR, subject=author)
        for author in overcommitted_authors
    )

    equivocation_flagged_authors = {
        c.I
        for c in claims
        if classifications[claim_id(c)].state == State.EQUIVOCATION_FLAGGED
    }
    flagged_authors = overcommitted_authors | equivocation_flagged_authors

    # 5. Flags anwenden -> Kantenkandidaten
    if include_flagged:
        candidate_groups = groups
    else:
        candidate_groups = {
            key: group for key, group in groups.items() if group.author not in flagged_authors
        }

    # 6. BFS über E+ -> d, C, cap, SUBGRANULAR_VOUCH
    bfs_result = bfs_capacities(anchors, candidate_groups, params)

    all_findings = tuple(
        sorted(set(payload_findings) | set(overcommit_findings) | set(bfs_result.findings))
    )

    identities = frozenset(bfs_result.node_capacity) | anchors | targets
    inf = infinity(bfs_result)

    # 7-8a. Graph bauen (Split, S*, T*), Dinic (Fluss-Belegung) -> value, cut
    flow_solver = build_flow_graph(
        Dinic, bfs_result, anchors, targets, inf, unit_capacities=False
    )
    value = flow_solver.max_flow(SOURCE, SINK)
    cut = source_side_cut(flow_solver, identities)

    # 8b. Dinic (Einheitskapazitäts-Belegung) -> disjoint_paths
    disjoint_solver = build_flow_graph(
        Dinic, bfs_result, anchors, targets, inf, unit_capacities=True
    )
    disjoint_paths = disjoint_solver.max_flow(SOURCE, SINK)

    return TrustResult(
        value=value,
        disjoint_paths=disjoint_paths,
        cut=cut,
        findings=all_findings,
    )
