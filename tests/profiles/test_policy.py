"""P-A … P-F — Policy-Auflösung (03-golden-anchors.md §4)."""

from __future__ import annotations

import pytest

from mensch_als_republik.policy import PROTOCOL_IRREVOCABLE, PolicyWarning
from mensch_als_republik.profiles import Finding, ProfileFinding, resolve_policy

from .fixtures import (
    CONSTITUTION_A,
    CONSTITUTION_B,
    CONSTITUTION_C,
    CONSTITUTION_HASH_A,
    DOC_CONSTITUTION_HASH_A,
    DOC_CONSTITUTION_HASH_B,
    DOC_CONSTITUTION_HASH_C,
    DOC_N_A,
    DOC_N_B,
    DOC_N_C,
    GENESIS_A,
    GENESIS_B,
    GENESIS_C,
    N_A,
    N_B,
    N_C,
)


def test_documented_hashes_match_computed() -> None:
    """Anker: berechnete Hashes == dokumentierte Werte (03-prompt.md §8.1)."""
    assert CONSTITUTION_HASH_A == DOC_CONSTITUTION_HASH_A
    assert N_A == DOC_N_A
    assert N_B == DOC_N_B
    assert N_C == DOC_N_C
    from .fixtures import CONSTITUTION_HASH_B, CONSTITUTION_HASH_C

    assert CONSTITUTION_HASH_B == DOC_CONSTITUTION_HASH_B
    assert CONSTITUTION_HASH_C == DOC_CONSTITUTION_HASH_C


def test_P_A() -> None:
    r = resolve_policy(scope=N_A, genesis_obj=GENESIS_A, constitution_obj=CONSTITUTION_A)
    assert r.policy.irrevocable == PROTOCOL_IRREVOCABLE
    assert r.findings == ()


def test_P_B() -> None:
    r = resolve_policy(scope=N_B, genesis_obj=GENESIS_B, constitution_obj=CONSTITUTION_B)
    assert r.policy.irrevocable == PROTOCOL_IRREVOCABLE
    assert r.findings == ()
    assert len(r.policy.warnings) == 1
    assert r.policy.warnings[0].code == PolicyWarning.UNSAFE_IRREVOCABLE_PREDICATE
    assert r.policy.warnings[0].predicate == "vouch@1"


def test_P_C() -> None:
    r = resolve_policy(scope=N_C, genesis_obj=GENESIS_C, constitution_obj=CONSTITUTION_C)
    assert r.policy.irrevocable == PROTOCOL_IRREVOCABLE
    assert r.findings == ()


def test_P_D() -> None:
    r = resolve_policy(scope=N_A, genesis_obj=GENESIS_A, constitution_obj=None)
    assert r.policy.irrevocable == PROTOCOL_IRREVOCABLE
    assert r.findings == (
        Finding(ProfileFinding.CONSTITUTION_UNAVAILABLE, CONSTITUTION_HASH_A),
    )


def test_P_E() -> None:
    r = resolve_policy(scope=N_A, genesis_obj=GENESIS_A, constitution_obj=CONSTITUTION_B)
    assert r.policy.irrevocable == PROTOCOL_IRREVOCABLE
    assert r.findings == (
        Finding(ProfileFinding.CONSTITUTION_HASH_MISMATCH, CONSTITUTION_HASH_A),
    )


def test_P_F() -> None:
    with pytest.raises(ValueError):
        resolve_policy(scope=N_A, genesis_obj=GENESIS_B, constitution_obj=CONSTITUTION_B)


def test_P_G() -> None:
    """Genesis ohne Key 4 — ValueError (03a B6)."""
    import hashlib

    from mensch_als_republik import cbor_canon
    from mensch_als_republik.domains import DOM_NUC_GEN

    broken = {
        0: 1,
        1: [bytes.fromhex(
            "8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c"
        )],
        2: 0,
        3: [bytes.fromhex(
            "8a88e3dd7409f195fd52db2d3cba5d72ca6709bf1d94121bf3748801b40f6f5c"
        )],
        5: 2,
        6: 1,
        7: 0,
    }
    scope = hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(broken)).digest()
    with pytest.raises(ValueError):
        resolve_policy(scope=scope, genesis_obj=broken, constitution_obj=None)
