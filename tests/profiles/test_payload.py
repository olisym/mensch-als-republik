"""TV-/CV-Vektoren — v-Payloads (03-golden-anchors.md §5–§6)."""

from __future__ import annotations

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import claim_id
from mensch_als_republik.profiles import (
    Finding,
    ProfileFinding,
    SettlementState,
    resolve_policy,
    settlement,
)
from tests.helpers import store_with

from .fixtures import (
    CONSTITUTION_A,
    GENESIS_A,
    N_A,
    NOW,
    REASON_REF,
    UNIT_REF,
    fresh_alice,
    fresh_bob,
    nuc,
)


def _settle_with_receipt_v(v):
    alice, bob = fresh_alice(), fresh_bob()
    pol = resolve_policy(
        scope=N_A, genesis_obj=GENESIS_A, constitution_obj=CONSTITUTION_A
    ).policy
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, N=N_A)
    R = bob.claim(p=nuc(N_A, "receipt"), J=(2, claim_id(O)), t=2, v=v, N=N_A)
    store = store_with(O, R)
    return settlement(store, obligation=O, scope=N_A, now=NOW, policy=pol), O, R


def test_TV_O1() -> None:
    v = bytes.fromhex(
        "a200191267015820e3151c99703d8a9723d0e33a1b32234db31826d710f12e3d1b80c6318e859291"
    )
    assert cbor_canon.decode(v) == {0: 4711, 1: UNIT_REF}


def test_TV_V1() -> None:
    v = bytes.fromhex(
        "a20003015820974a63cba3658a639ebd25c469e33365d805c5fd3f55d6859c80a8c4c79d55b4"
    )
    assert cbor_canon.decode(v) == {0: 3, 1: REASON_REF}


def test_TV_R0() -> None:
    result, _O, R = _settle_with_receipt_v(None)
    assert result.state == SettlementState.SETTLED
    assert result.receipt_claim_id == claim_id(R)
    assert result.findings == ()


def test_TV_R1() -> None:
    v = bytes.fromhex("a1001906d6")
    result, _O, R = _settle_with_receipt_v(v)
    assert result.state == SettlementState.OPEN
    assert result.findings == (
        Finding(ProfileFinding.PARTIAL_RECEIPT_UNSUPPORTED, claim_id(R)),
    )


def test_TV_R2() -> None:
    v = bytes.fromhex("a10701")
    result, _O, R = _settle_with_receipt_v(v)
    assert result.state == SettlementState.SETTLED
    assert result.receipt_claim_id == claim_id(R)
    assert result.findings == ()


def test_TV_T1() -> None:
    alice, bob = fresh_alice(), fresh_bob()
    pol = resolve_policy(
        scope=N_A, genesis_obj=GENESIS_A, constitution_obj=CONSTITUTION_A
    ).policy
    v = bytes.fromhex("a1006434373131")
    O = alice.claim(p=nuc(N_A, "obligation"), J=(1, bob.pub), t=1, v=v, N=N_A)
    store = store_with(O)
    result = settlement(store, obligation=O, scope=N_A, now=NOW, policy=pol)
    assert result.state == SettlementState.OPEN
    assert result.findings == (
        Finding(ProfileFinding.INVALID_V_TYPE, claim_id(O)),
    )


def test_CV_1() -> None:
    v = bytes.fromhex("a100190064")
    result, _O, R = _settle_with_receipt_v(v)
    rid = claim_id(R)
    assert result.state == SettlementState.OPEN
    assert result.findings == (
        Finding(ProfileFinding.NON_CANONICAL_V, rid),
        Finding(ProfileFinding.PARTIAL_RECEIPT_UNSUPPORTED, rid),
    )


def test_CV_2() -> None:
    v = bytes.fromhex("bf001864ff")
    result, _O, R = _settle_with_receipt_v(v)
    rid = claim_id(R)
    assert result.state == SettlementState.OPEN
    assert result.findings == (
        Finding(ProfileFinding.NON_CANONICAL_V, rid),
        Finding(ProfileFinding.PARTIAL_RECEIPT_UNSUPPORTED, rid),
    )


def test_CV_3() -> None:
    v = bytes.fromhex("a20901001864")
    result, _O, R = _settle_with_receipt_v(v)
    rid = claim_id(R)
    assert result.state == SettlementState.OPEN
    assert result.findings == (
        Finding(ProfileFinding.NON_CANONICAL_V, rid),
        Finding(ProfileFinding.PARTIAL_RECEIPT_UNSUPPORTED, rid),
    )


def test_CV_4() -> None:
    v = bytes.fromhex("a2001864001865")
    result, _O, R = _settle_with_receipt_v(v)
    rid = claim_id(R)
    assert result.state == SettlementState.OPEN
    assert result.findings == (
        Finding(ProfileFinding.NON_CANONICAL_V, rid),
        Finding(ProfileFinding.PARTIAL_RECEIPT_UNSUPPORTED, rid),
    )


def test_CV_5() -> None:
    v = bytes.fromhex("a1001864")
    result, _O, R = _settle_with_receipt_v(v)
    assert result.state == SettlementState.OPEN
    assert result.findings == (
        Finding(ProfileFinding.PARTIAL_RECEIPT_UNSUPPORTED, claim_id(R)),
    )


def test_CV_6() -> None:
    v = bytes.fromhex("a1")
    result, _O, R = _settle_with_receipt_v(v)
    rid = claim_id(R)
    assert result.state == SettlementState.OPEN
    assert result.findings == (
        Finding(ProfileFinding.PARTIAL_RECEIPT_UNSUPPORTED, rid),
        Finding(ProfileFinding.UNPARSABLE_V, rid),
    )
