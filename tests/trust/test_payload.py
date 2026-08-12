"""T-02.7 — Payload-Randfaelle (02a §2.3)."""

from __future__ import annotations

from mensch_als_republik import cbor_canon
from mensch_als_republik.atom import claim_id
from mensch_als_republik.trust import Finding, TrustFinding, TrustParams, trust

from tests.helpers import Identity, scope_id, store_with
from .tp02 import NOW, T_EXP

PARAMS = TrustParams(C0=16, gamma_num=1, gamma_den=2, D=4)


def _single_vouch_result(v: bytes | None, label: str):
    scope = scope_id(f"T-02.7-{label}")
    ALICE, BOB = Identity(f"pA-{label}"), Identity(f"pB-{label}")
    claim = ALICE.vouch_raw(BOB, v=v, scope=scope, t=1, t_exp=T_EXP)
    store = store_with(claim)
    r = trust(
        store, anchors=frozenset({ALICE.pub}), targets=frozenset({BOB.pub}), scope=scope,
        now=NOW, params=PARAMS, include_flagged=True,
    )
    return r, claim


def test_v_absent_defaults_to_D() -> None:
    r, _ = _single_vouch_result(None, "absent")
    # n = D = 4, cap(ALICE->BOB) = floor(4*16/4) = 16
    assert r.value == 16
    assert r.findings == ()


def test_v_with_extra_keys_is_valid_and_ignored() -> None:
    v = cbor_canon.encode({0: 2, 1: 99})
    r, _ = _single_vouch_result(v, "extra-keys")
    # n = 2, cap = floor(2*16/4) = 8
    assert r.value == 8
    assert r.findings == ()


def test_v_n_zero_is_invalid_weight() -> None:
    v = cbor_canon.encode({0: 0})
    r, claim = _single_vouch_result(v, "n-zero")
    assert r.value == 0
    assert r.findings == (Finding(TrustFinding.INVALID_VOUCH_WEIGHT, claim_id(claim)),)


def test_v_n_greater_than_D_is_invalid_weight() -> None:
    v = cbor_canon.encode({0: 5})  # D = 4
    r, claim = _single_vouch_result(v, "n-too-big")
    assert r.value == 0
    assert r.findings == (Finding(TrustFinding.INVALID_VOUCH_WEIGHT, claim_id(claim)),)


def test_v_undecodable_bytes_is_unparsable() -> None:
    r, claim = _single_vouch_result(b"\xff", "undecodable")
    assert r.value == 0
    assert r.findings == (Finding(TrustFinding.UNPARSABLE_VOUCH_PAYLOAD, claim_id(claim)),)


def test_v_missing_key_0_is_unparsable() -> None:
    v = cbor_canon.encode({1: 4})
    r, claim = _single_vouch_result(v, "missing-key-0")
    assert r.value == 0
    assert r.findings == (Finding(TrustFinding.UNPARSABLE_VOUCH_PAYLOAD, claim_id(claim)),)


def test_false_accusation_guard() -> None:
    """Ein Autor mit unlesbarem + zwei gueltigen n=2-Vouches auf verschiedene Subjekte:
    Sigma n_budget = 4 <= D, kein OVERCOMMITTED_AUTHOR."""
    scope = scope_id("T-02.7-guard")
    ALICE = Identity("guard-A")
    B1, B2, B3 = Identity("guard-B1"), Identity("guard-B2"), Identity("guard-B3")
    ok1 = ALICE.vouch(B1, n=2, scope=scope, t=1, t_exp=T_EXP)
    ok2 = ALICE.vouch(B2, n=2, scope=scope, t=1, t_exp=T_EXP)
    bad = ALICE.vouch_raw(B3, v=b"\xff", scope=scope, t=1, t_exp=T_EXP)
    store = store_with(ok1, ok2, bad)
    r = trust(
        store, anchors=frozenset({ALICE.pub}), targets=frozenset({B1.pub, B2.pub, B3.pub}),
        scope=scope, now=NOW, params=PARAMS, include_flagged=True,
    )
    assert not any(f.kind == TrustFinding.OVERCOMMITTED_AUTHOR for f in r.findings)
