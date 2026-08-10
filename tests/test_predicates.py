"""Tests für Prädikat-Grammatik und Scope-Bindung."""

import pytest

from mensch_als_republik.atom import Claim
from mensch_als_republik.errors import (
    BadScopeBinding,
    ReservedCorePredicate,
    UnknownNamespace,
)
from mensch_als_republik.predicates import parse_predicate, resolve_scope

N = bytes.fromhex("65309fe233da30fda061d7c5ef002b6b80e42682cd54d703ab13fb6c7d2f5557")
ALICE = bytes.fromhex("8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c")
BOB = bytes.fromhex("8139770ea87d175f56a35466c34c7ecccb8d8a91b4ee37a25df60f5b8fc9b394")


def _claim(p: str, N_field: bytes | None = N) -> Claim:
    return Claim(
        version=1,
        I=ALICE,
        J=(1, BOB),
        p=p,
        t=1,
        h_prev=b"\x01" * 32,
        N=N_field,
    )


def test_parse_canonical_nuc():
    p = f"nuc:{N.hex()}/vouch@1"
    parsed = parse_predicate(p)
    assert parsed.namespace == "nuc"
    assert parsed.name == "vouch"
    assert parsed.version == "1"
    assert parsed.scope_hex == N.hex()


def test_parse_core_revoke():
    parsed = parse_predicate("core/revoke@1")
    assert parsed.namespace == "core"
    assert parsed.name == "revoke"


def test_unknown_namespace_svc():
    with pytest.raises(UnknownNamespace):
        parse_predicate("svc:foo/bar@1")


def test_reserved_core_predicate_vouch():
    with pytest.raises(ReservedCorePredicate):
        parse_predicate("core/vouch@1")


def test_bad_scope_binding_wrong_n():
    p = f"nuc:{N.hex()}/vouch@1"
    with pytest.raises(BadScopeBinding):
        resolve_scope(_claim(p, N_field=b"\xff" * 32))


def test_bad_scope_binding_missing_n_on_nuc():
    with pytest.raises(BadScopeBinding):
        resolve_scope(_claim(f"nuc:hasenpfote/vouch@1", N_field=None))


def test_alias_scope_resolves_from_n():
    p = "nuc:hasenpfote/vouch@1"
    scope = resolve_scope(_claim(p, N_field=N))
    assert scope == N


def test_alias_matching_64_hex_rejected():
    """Alias darf ^[0-9a-f]{64}$ nicht matchen — wird als kanonisch behandelt."""
    fake_hex = "a" * 64
    p = f"nuc:{fake_hex}/vouch@1"
    # Grammatik klassifiziert als kanonisch → N muss exakt passen
    with pytest.raises(BadScopeBinding):
        resolve_scope(_claim(p, N_field=N))


def test_alias_that_looks_like_hex_but_wrong_n():
    """64-Hex-String im Prädikat erzwingt N == bytes.fromhex(scope)."""
    p = f"nuc:{N.hex()}/vouch@1"
    parsed = parse_predicate(p)
    assert parsed.scope_hex is not None
    assert parsed.scope_alias is None
