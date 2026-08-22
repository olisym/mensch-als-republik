"""Beispielnukleus — Dokument und Implementierung (example-nucleus.md)."""

from __future__ import annotations

from tools.example_nucleus import (
    build,
    check_anchor_resolution,
    check_edge_capacity,
    check_malformed_appended_dora,
    check_membership_epoch1,
    check_membership_epoch2,
    check_overcommit,
    check_ratification,
    check_resolved_chain,
    check_scope_separation,
    check_tally,
    check_trust_flow,
    probe_stock_anchors,
    verify_all,
)


def test_stock_anchors() -> None:
    probe_stock_anchors()


def test_objects_match_document() -> None:
    build()


def test_anchor_resolution() -> None:
    check_anchor_resolution(build())


def test_membership_epoch1() -> None:
    check_membership_epoch1(build())


def test_tally_three_runs() -> None:
    check_tally(build())


def test_ratification() -> None:
    check_ratification(build())


def test_resolved_chain() -> None:
    check_resolved_chain(build())


def test_membership_epoch2() -> None:
    check_membership_epoch2(build())


def test_trust_flow() -> None:
    check_trust_flow(build())


def test_overcommit() -> None:
    check_overcommit(build())


def test_edge_capacity() -> None:
    check_edge_capacity(build())


def test_scope_separation() -> None:
    check_scope_separation(build())


def test_malformed_appended_dora() -> None:
    check_malformed_appended_dora(build())


def test_verify_all() -> None:
    verify_all()
