"""Totalität und Kopplung von read_claim (D131)."""

from __future__ import annotations

from hypothesis import given, strategies as st

from mensch_als_republik.atom import Claim, claim_id, signed_bytes
from mensch_als_republik.errors import ErrorCode, VerifierError
from mensch_als_republik.verifier import read_claim, structural_check

from tests.property.welten import welten


@given(st.binary(min_size=0, max_size=512))
def test_read_claim_totalitaet(data: bytes) -> None:
    result = read_claim(data)
    assert isinstance(result, (Claim, ErrorCode))


@given(welten())
def test_read_claim_kopplung(welt) -> None:
    for c in welt.claims:
        data = signed_bytes(c)
        via_read = read_claim(data)
        try:
            via_check = structural_check(data)
        except VerifierError as exc:
            assert via_read == exc.code
        else:
            assert isinstance(via_read, Claim)
            assert claim_id(via_read) == claim_id(via_check)
