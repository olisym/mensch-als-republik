"""Tests für kanonische CBOR-Enkodierung."""

import pytest

from mensch_als_republik import cbor_canon


def test_encode_decode_roundtrip():
    obj = {0: 1, 1: b"\x01" * 32, 3: "core/revoke@1"}
    data = cbor_canon.encode(obj)
    assert cbor_canon.decode(data) == obj


def test_is_canonical_sorted_keys():
    canonical = cbor_canon.encode({0: 1, 2: 3, 5: 6})
    assert cbor_canon.is_canonical(canonical)


def test_non_canonical_rejected_by_reserialize():
    import cbor2

    obj = {8: b"\x00" * 32, 0: 1, 3: "x"}
    noncanonical = cbor2.dumps(obj, canonical=False)
    assert not cbor_canon.is_canonical(noncanonical)
    assert cbor_canon.reserialize(noncanonical) == cbor_canon.encode(
        cbor_canon.decode(noncanonical)
    )
