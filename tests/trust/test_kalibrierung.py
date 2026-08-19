"""resolve_trust_params — fünf Lagen aus 02-trust-flow.md §8.1 plus formwidriger Schlüssel 9 (D147)."""

from __future__ import annotations

import hashlib

import pytest

from mensch_als_republik import cbor_canon
from mensch_als_republik.domains import DOM_NUC_GEN
from mensch_als_republik.trust.params import TrustParams, resolve_trust_params
from tools.example_nucleus import build

_RAW = {0: 100, 1: 1, 2: 2, 3: 100}
_GENESIS_WITH = {9: dict(_RAW)}
_GENESIS_WITHOUT = {0: 1}


def _scope(genesis_obj: dict) -> bytes:
    return hashlib.sha256(DOM_NUC_GEN + cbor_canon.encode(genesis_obj)).digest()


def _params_from(genesis_obj: dict) -> TrustParams:
    raw = genesis_obj[9]
    return TrustParams(C0=raw[0], gamma_num=raw[1], gamma_den=raw[2], D=raw[3])


def test_genesis_does_not_match_scope() -> None:
    with pytest.raises(ValueError, match="genesis_obj does not match scope"):
        resolve_trust_params(
            scope=bytes(32), genesis_obj=_GENESIS_WITH, out_of_band=None
        )


def test_key9_present_no_out_of_band() -> None:
    expected = _params_from(_GENESIS_WITH)
    result = resolve_trust_params(
        scope=_scope(_GENESIS_WITH), genesis_obj=_GENESIS_WITH, out_of_band=None
    )
    assert result == expected


def test_key9_present_out_of_band_differs() -> None:
    from_genesis = _params_from(_GENESIS_WITH)
    out_of_band = TrustParams(
        C0=from_genesis.C0,
        gamma_num=from_genesis.gamma_num,
        gamma_den=from_genesis.gamma_den,
        D=from_genesis.D + 1,
    )
    with pytest.raises(ValueError, match="out_of_band does not match genesis trust_params"):
        resolve_trust_params(
            scope=_scope(_GENESIS_WITH),
            genesis_obj=_GENESIS_WITH,
            out_of_band=out_of_band,
        )


def test_key9_missing_out_of_band_present() -> None:
    raw = _GENESIS_WITH[9]
    out_of_band = TrustParams(C0=raw[0], gamma_num=raw[1], gamma_den=raw[2], D=raw[3])
    result = resolve_trust_params(
        scope=_scope(_GENESIS_WITHOUT),
        genesis_obj=_GENESIS_WITHOUT,
        out_of_band=out_of_band,
    )
    assert result == out_of_band


def test_key9_missing_no_out_of_band() -> None:
    with pytest.raises(
        ValueError, match="genesis_obj missing trust_params and no out_of_band"
    ):
        resolve_trust_params(
            scope=_scope(_GENESIS_WITHOUT),
            genesis_obj=_GENESIS_WITHOUT,
            out_of_band=None,
        )


def test_key9_malformed() -> None:
    genesis = {9: {0: 100, 1: 1, 2: 2}}
    raw = _GENESIS_WITH[9]
    out_of_band = TrustParams(C0=raw[0], gamma_num=raw[1], gamma_den=raw[2], D=raw[3])
    with pytest.raises(ValueError, match="genesis_obj key 9 is malformed"):
        resolve_trust_params(
            scope=_scope(genesis), genesis_obj=genesis, out_of_band=out_of_band
        )


def test_example_nucleus_genesis_res_agrees_with_params() -> None:
    ex = build()
    result = resolve_trust_params(
        scope=_scope(ex.genesis_res),
        genesis_obj=ex.genesis_res,
        out_of_band=ex.params,
    )
    assert result == ex.params
